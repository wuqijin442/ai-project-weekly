# -*- coding: utf-8 -*-
"""
GitHub AI 项目归档管线（Obsidian 知识库 + ima 共享库载体）。

单一职责：把「抓 GitHub Trending → 筛选 Vibe Coding → 生成 Obsidian 三层结构
→ 生成 ima 干净载体 → 推 win 分支」整条流水线确定性化，消除原先每步手动跑的脆弱点
（CRLF/Python 路径/手工 patch）。

设计要点：
- 复用 main.py 的底层原语：log / run_cmd / api_json / pre_sync_pull /
  _push_with_resilience / is_transient_git_err（含 GitHub IP 层阻断退避重试）。
- git 推送严格只 add Obsidian_Vault/（绝不 git add -A），落在 win 分支。
- 推送失败写 Logs/PUSH_STUCK.flag（借鉴 dgx push_retry 固化补丁），供每日开头优先补推。
- ima 上传的 MCP 部分（create_media/add_knowledge/search）由 agent 驱动，
  本模块只负责确定性生成载体 + 维护 ima_carrier/.pending_*.json 待推队列（P0-1）。

仅依赖 Python 3 标准库 + 系统 git + main.py。
"""
import os
import re
import sys
import json
import time
import datetime
import subprocess
import urllib.request
from pathlib import Path

# 复用 main.py 的底层原语（main.py 仅有 __main__ 守卫，import 无副作用）
sys.path.insert(0, str(Path(__file__).resolve().parent))
import main  # noqa: E402
import vibe_config as vc  # noqa: E402

log = main.log  # 暴露 log 别名，供编排层调用

ROOT = main.ROOT
OBSIDIAN = ROOT / "Obsidian_Vault"
DAILY_DIR = OBSIDIAN / "Daily"
PROJECTS_DIR = OBSIDIAN / "Projects"
IMA_CARRIER = ROOT / "ima_carrier"
LOGS_DIR = ROOT / "Logs"
for d in (OBSIDIAN, DAILY_DIR, PROJECTS_DIR, IMA_CARRIER, LOGS_DIR):
    d.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------------------
# Token：从内联 PAT 的 remote.origin.url 提取，注入 GITHUB_TOKEN 供 api_json 使用
# ----------------------------------------------------------------------------
def get_token_from_remote():
    rc, out, _ = main.run_cmd(
        ["git", "config", "--get", "remote.origin.url"], cwd=ROOT, timeout=30)
    if rc != 0:
        return ""
    m = re.search(r"https://[^:@/]+:([^@]+)@github\.com", out)
    return m.group(1) if m else ""


def ensure_token_env():
    tok = os.environ.get("GITHUB_TOKEN") or get_token_from_remote()
    if tok:
        os.environ["GITHUB_TOKEN"] = tok
    return tok


# ----------------------------------------------------------------------------
# 步骤1：抓取 GitHub Trending（含当日/本周新增解析）
# ----------------------------------------------------------------------------
def fetch_trending_raw(since="daily"):
    url = f"https://github.com/trending?since={since}"
    html = ""
    for rnd in range(1, main.TRENDING_ROUNDS + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=45) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
            if html:
                main.log(f"trending 抓取成功（第{rnd}/{main.TRENDING_ROUNDS}轮）")
                break
        except Exception as e:  # noqa
            main.log(f"trending 抓取第{rnd}次失败: {e}")
        if not html and rnd < main.TRENDING_ROUNDS:
            time.sleep(15)
    if not html:
        if main.FALLBACK_ENABLED:
            main.log("主站 /trending 不可达 → 官方备用通道 api.github.com（Search API 近似榜单）")
            return fetch_trending_via_api_raw(since)
        return []

    articles = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.S)
    projects = []
    for art in articles:
        m = re.search(r'<h2[^>]*>.*?<a[^>]*href="/([^"]+)"', art, re.S)
        if not m:
            continue
        full = m.group(1).strip("/")
        if full.count("/") != 1:
            continue
        owner, name = full.split("/")
        desc_m = re.search(r'<p class="col-9[^"]*">(.*?)</p>', art, re.S)
        desc = main.clean_text(desc_m.group(1)) if desc_m else ""
        lang_m = re.search(r'<span itemprop="programmingLanguage">([^<]+)</span>', art)
        lang = lang_m.group(1).strip() if lang_m else "Unknown"
        # 当日/本周新增 star（趋势页面 float-right 区块）
        gm = re.search(r'([\d,]+)\s+stars\s+(today|this week)', art, re.S)
        today = int(gm.group(1).replace(",", "")) if gm else 0
        period = gm.group(2) if gm else "today"
        projects.append({
            "owner": owner, "name": name, "full": full,
            "url": f"https://github.com/{full}",
            "description": desc, "language": lang,
            "today_growth": today, "growth_period": period,
            "stars": 0, "forks": 0, "topics": [], "license": "NOASSERTION",
            "created_at": "", "source": "trending-html",
        })
    main.log(f"trending 解析完成，共 {len(projects)} 个仓库")
    return projects


def fetch_trending_via_api_raw(since="daily"):
    items = main.fetch_trending_via_api(since)
    out = []
    for it in items:
        out.append({
            "owner": it["owner"], "name": it["name"], "full": it["full"],
            "url": it["url"], "description": it["description"],
            "language": it["language"], "today_growth": 0, "growth_period": "n/a",
            "stars": it.get("stars", 0), "forks": 0, "topics": [],
            "license": "NOASSERTION", "created_at": "", "source": "search-api-fallback",
        })
    return out


# ----------------------------------------------------------------------------
# 步骤2：GitHub REST API 补全 stars/forks/topics/license/created_at
# ----------------------------------------------------------------------------
def enrich_with_api(projects):
    for p in projects:
        data = main.api_json(f"https://api.github.com/repos/{p['full']}", timeout=20, attempts=2)
        if not isinstance(data, dict):
            main.log(f"  API 补全失败 {p['full']}（保留 HTML 解析值）")
            continue
        p["stars"] = int(data.get("stargazers_count") or 0)
        p["forks"] = int(data.get("forks_count") or 0)
        p["topics"] = data.get("topics") or []
        lic = data.get("license")
        p["license"] = (lic.get("spdx_id") if isinstance(lic, dict) and lic.get("spdx_id")
                        else "NOASSERTION")
        ca = data.get("created_at") or ""
        p["created_at"] = ca[:10] if ca else ""
        p["source"] = "trending+api"


# ----------------------------------------------------------------------------
# 步骤3：Vibe Coding 筛选（严格命中 + 生态打分）
# ----------------------------------------------------------------------------
def _text_blob(p):
    return (p["full"] + " " + p["name"] + " " + p["description"] + " "
            + " ".join(p.get("topics", []))).lower()


def _match(blob, kw):
    """词首边界匹配（2026-08-19 修复）：裸子串 `in` 会把 video 里的 ide、
    inside 里的 ide 等误判为命中 `ide` 信号。改用 \\b{kw}（词首前缀）既能排除
    video/inside/guide 中的 ide，又保留 agent→agents、coding→coders 的召回。"""
    return re.search(r"\b" + re.escape(kw), blob) is not None


def vibe_filter(projects, date):
    weekday = date.weekday()  # Mon=0 .. Sun=6
    n = 10 if weekday == 6 else 5
    strict, eco = [], []
    for p in projects:
        blob = _text_blob(p)
        if any(_match(blob, k) for k in vc.EXCLUDE_KEYWORDS):
            continue
        is_strict = any(_match(blob, k) for k in vc.STRICT_KEYWORDS)
        p["strict_hit"] = is_strict
        if is_strict:
            strict.append(p)
        else:
            score = sum(1 for s in vc.ECOSYSTEM_SIGNALS if _match(blob, s))
            if p["full"] in vc.ECOSYSTEM_WHITELIST:
                score += 5
            p["eco_score"] = score
            eco.append(p)
    strict.sort(key=lambda x: x["today_growth"], reverse=True)
    eco.sort(key=lambda x: x["today_growth"], reverse=True)
    top = list(strict)  # 强制包含严格命中（优先入榜）
    # 2026-08-19 修复：仅从「有生态信号(eco_score>=1)」的候选补充，避免把无信号的高增长
    # 仓库（视频生成 / API 列表 / 下载器等）塞进 Vibe Coding 榜。此前会误将
    # MoneyPrinterTurbo / public-apis / Motrix 列为 Vibe Coding Top5。
    eco_real = [p for p in eco if p.get("eco_score", 0) >= 1]
    for p in eco_real:
        if len(top) >= n:
            break
        if p not in top:
            top.append(p)
    # 兜底：仍不足 n（极稀疏日），如实取现有数量，绝不用无信号仓库虚报满榜
    if len(top) < n:
        main.log(f"Vibe Coding 候选不足 {n}（严格 {len(strict)} + 生态信号 {len(eco_real)}），"
                 f"如实取 {len(top)} 个，不虚报满榜")
    # 最终展示顺序：按当日新增 Star 降序（与表头声明、08-11 口径一致）
    top.sort(key=lambda x: x["today_growth"], reverse=True)
    main.log(f"Vibe Coding 筛选：严格命中 {len(strict)} / 生态候选 {len(eco)} / "
             f"入选 {len(top)}（{'周日 TOP10' if weekday == 6 else '平日 TOP5'}）")
    return top, {"strict": strict, "eco": eco, "n": n, "sunday": weekday == 6}


# ----------------------------------------------------------------------------
# 工具：紧凑 star 记法（13500 -> 13.5k）
# ----------------------------------------------------------------------------
def fmt_star(n):
    if n >= 1000:
        return f"{n/1000:.1f}k".rstrip("0").rstrip(".")
    return str(n)


def _growth_key(p):
    """可比较的当日新增数值；降级/缺失返回 -1（排末尾）。"""
    g = p.get("today_growth", 0)
    return g if isinstance(g, int) and g > 0 else -1


def all_track_top(projects, n):
    """全赛道爆款：GitHub Trending 全部仓库按当日新增 Star 降序取 Top n（不限赛道）。"""
    fb = any(p.get("source") == "search-api-fallback" for p in projects)
    if fb:
        lst = sorted(projects, key=lambda x: x.get("stars", 0), reverse=True)[:n]
    else:
        lst = sorted(projects, key=_growth_key, reverse=True)[:n]
    return lst


def niche_top(projects, n, stars_max, growth_min):
    """爆款小众（短视频同款）：当日 Trending 中「相对小众」= 总 Star 最小的一批
    （排除 stars_max 以上的绝对头部 mega 仓库），取 n 个、按当日新增 Star 降序。
    单日 Trending 通常不足 n 个真正「小」仓库，故以「体量最小 n 个」近似，
    保证榜单稳定出 n 条；🔥 标记由调用方按 growth_min 处理。"""
    fb = any(p.get("source") == "search-api-fallback" for p in projects)
    pool = [p for p in projects if p.get("stars", 0) < stars_max]
    small = sorted(pool, key=lambda x: x.get("stars", 0))[:n]
    if fb:
        return small  # 降级弱近似：直接取总 Star 最小的一批
    small.sort(key=_growth_key, reverse=True)  # 按当日新增降序（小众中更「爆」的排前）
    return small


def _sanitize_cell(s, limit=46):
    """表格单元格清洗：去竖线/换行，超长截断，避免破坏 Markdown 表格。"""
    s = (s or "").replace("|", "/").replace("\n", " ").strip()
    return s[:limit]


# ----------------------------------------------------------------------------
# 步骤4a：生成 Obsidian 三层结构
# ----------------------------------------------------------------------------
def _count_degree(full):
    """扫描历史日报，统计该项目被收录的上榜次数（含本次前）。"""
    cnt = 0
    if not DAILY_DIR.exists():
        return 0
    for f in DAILY_DIR.glob("*.md"):
        try:
            if full in f.read_text(encoding="utf-8", errors="ignore"):
                cnt += 1
        except Exception:  # noqa
            pass
    return cnt


def _degree_label(deg):
    if deg <= 1:
        return "首度上榜"
    return f"{deg}度上榜"


def build_obsidian(date, top, all_projects, full_track=False):
    is_sunday = date.weekday() == 6
    daily_name = ("AI-Weekly" if is_sunday else "Vibe-Coding") + f"-{date.isoformat()}.md"
    mode = "全赛道" if is_sunday else "Vibe Coding 赛道"
    best = top[0] if top else None
    # 回退通道（主站被 IP 阻断）时：Search API 近似榜，无当日新增，必须诚实标注
    used_fallback = any(p.get("source") == "search-api-fallback" for p in top)

    def fmt_growth(p):
        if used_fallback or p.get("today_growth", 0) == 0:
            return "—"
        return f"🔺{p['today_growth']:,}"

    # ---- 日报 ----
    md = []
    md.append("---")
    md.append(f"date: {date.isoformat()}")
    md.append(f"mode: {'weekly' if is_sunday else 'vibe-coding'}")
    md.append(f"project_count: {len(top)}")
    md.append("tags: [github, ai, trending, "
              + ("weekly" if is_sunday else "vibe-coding") + "]")
    src_note = ("GitHub Trending 主站被 IP 阻断 → 官方备用通道 api.github.com（Search API 近似榜，"
                "按总 Star 降序；无当日新增，增长列以 — 表示）" if used_fallback
                else "GitHub Trending 飙升榜 + GitHub REST API")
    md.append(f"source: {src_note}")
    md.append("---")
    md.append("")
    md.append(f"# GitHub AI 项目{'周报' if is_sunday else '日报'} · {mode} · {date.isoformat()}"
              f"（{'周日' if is_sunday else '周二' if date.weekday() == 1 else '工作日'}）")
    md.append("")
    if used_fallback:
        md.append("> ⚠️ **数据源降级**：GitHub Trending 主站本次不可达，改用 api.github.com Search API "
                  "近似榜单（近 1 日有推送 + star≥200，按总 Star 降序）。排名口径与「当日新增 Star」不同，"
                  "**增长列不可用（—）**，结论仅供参考，待主站恢复后重跑以得真实飙升榜。")
    md.append("> 数据源：" + ("api.github.com Search API 近似榜（降级）" if used_fallback
              else "GitHub Trending 全局日榜（飙升榜，按当日新增 Star 降序）"
              " + GitHub REST API 实时补全 stars / topics / license。"))
    if best:
        md.append("")
        md.append("## 🔝 今日最佳开源项目")
        md.append("")
        md.append(f"**{best['full']}** — {fmt_growth(best)} / ⭐{fmt_star(best['stars'])}"
                  f" / {best['language']}")
        md.append(f"- 链接：{best['url']}")
        md.append(f"- 简介：{best['description']}")
        _best_basis = ("✅ 严格命中（topics/关键词）" if best.get("strict_hit")
                       else ("全赛道" if full_track else "生态扩充"))
        md.append(f"- 入选：{_best_basis}")
    md.append("")
    md.append("## 分类速览（" + ("按总 Star 近似降序（降级）" if used_fallback
              else "按当日新增降序") + "）")
    md.append("")
    md.append("| # | 项目 | 语言 | ⭐ | 📈 新增 | 入选依据 |")
    md.append("|---|---|---|---|---|---|")
    for i, p in enumerate(top, 1):
        if p.get("strict_hit"):
            basis = "✅ 严格命中"
        elif full_track:
            basis = "全赛道"
        else:
            basis = f"生态扩充(分{p.get('eco_score',0)})"
        md.append(f"| {i} | [[Projects/{p['owner']}_{p['name']}|{p['full']}]] | "
                  f"{p['language']} | {fmt_star(p['stars'])} | {fmt_growth(p)} | {basis} |")
    md.append("")
    # 始终计算（趋势解读段会引用），仅 full_track 模式跳过其文档小节（避免与全赛道主表重复）
    all_lst = all_track_top(all_projects, vc.ALL_TRACK_TOP_N)
    if not full_track:
        # ---- 全赛道爆款 ----
        md.append("")
        md.append(f"## 🌐 全赛道爆款 Top{len(all_lst)}")
        md.append("")
        md.append("> GitHub Trending 全局（不限 Vibe Coding 赛道），按当日新增 Star 降序"
                  + ("（降级：按总 Star 近似）" if used_fallback else "") + "。")
        md.append("")
        md.append("| # | 项目 | 语言 | ⭐ | 📈 新增 |")
        md.append("|---|---|---|---|---|")
        for i, p in enumerate(all_lst, 1):
            md.append(f"| {i} | [{p['full']}]({p['url']}) | {p['language']} | "
                      f"{fmt_star(p['stars'])} | {fmt_growth(p)} |")
        md.append("")
    # ---- 爆款小众（短视频同款） ----
    niche_lst = niche_top(all_projects, vc.NICHE_TOP_N, vc.NICHE_STARS_MAX, vc.NICHE_GROWTH_MIN)
    md.append(f"## 💡 爆款小众热门（短视频同款）Top{len(niche_lst)}")
    md.append("")
    md.append(f"> 筛选口径：当日 Trending 中总 Star 最小的一批（总 Star < {vc.NICHE_STARS_MAX:,}，"
              f"排除绝对头部 mega 仓库），按当日新增降序取 Top{len(niche_lst)}——这类「小众但爆发」项目正是"
              "抖音/快手/B站/视频号等短视频平台开发者账号最常讲解的品类。🔥 = 当日新增 ≥ "
              f"{vc.NICHE_GROWTH_MIN}。")
    if used_fallback:
        md.append("> ⚠️ 降级通道无当日新增数据，本期以「总 Star 最低」做弱近似，非真实爆款信号。")
    md.append("> 数据说明：本自动化暂以 GitHub Trending 增速近似该信号（无公开短视频平台热榜 API）；"
              "如需真实平台信号可接入数据源（如 HelloGitHub / 今日热榜）续做。")
    md.append("")
    md.append("| # | 项目 | 语言 | ⭐ | 📈 新增 | 一句话亮点 |")
    md.append("|---|---|---|---|---|---|")
    for i, p in enumerate(niche_lst, 1):
        hot = "🔥 " if _growth_key(p) >= vc.NICHE_GROWTH_MIN else ""
        md.append(f"| {i} | {hot}[{p['full']}]({p['url']}) | {p['language']} | "
                  f"{fmt_star(p['stars'])} | {fmt_growth(p)} | {_sanitize_cell(p['description'])} |")
    md.append("")
    md.append("## 趋势解读")
    md.append("")
    langs = {}
    for p in top:
        langs[p["language"]] = langs.get(p["language"], 0) + 1
    md.append(f"- 语言分布：{', '.join(f'{k}×{v}' for k, v in sorted(langs.items(), key=lambda x:-x[1]))}")
    if full_track:
        md.append(f"- 全赛道收录 {len(top)} 个（周日全赛道口径）。")
    else:
        strict_n = sum(1 for p in top if p.get("strict_hit"))
        md.append(f"- 严格关键词命中 {strict_n} 个，生态扩充 {len(top)-strict_n} 个"
                  f"（Vibe Coding 赛道口径）。")
    md.append(f"- 全赛道爆款收录 {len(all_lst)} 个；爆款小众（短视频同款）收录 {len(niche_lst)} 个。")
    md.append("- 注：机械统计由 src/run_daily.py 生成；深度趋势解读可由 agent 在生成后补充。")
    md.append("")
    md.append("## 详细见 Obsidian 项目页")
    md.append("")
    for p in top:
        md.append(f"- [[Projects/{p['owner']}_{p['name']}|{p['full']}]]")

    (DAILY_DIR / daily_name).write_text("\n".join(md) + "\n", encoding="utf-8")
    main.log(f"日报已生成：{DAILY_DIR / daily_name}")

    # ---- 项目页（新建 / 更新） ----
    for p in top:
        _upsert_project_page(p, date, daily_name)

    # ---- 全局索引重建（确定性，避免手工 patch 错位） ----
    _rebuild_index(date, daily_name, is_sunday)
    return DAILY_DIR / daily_name


def _upsert_project_page(p, date, daily_name):
    slug = f"{p['owner']}_{p['name']}"
    path = PROJECTS_DIR / f"{slug}.md"
    deg = _count_degree(p["full"]) + 1  # +1 含本次
    status = _degree_label(deg)
    today = date.isoformat()
    backlink = f"- [[Daily/{daily_name}|{today} 收录]]"

    if not path.exists():
        content = [
            "---",
            f"aliases: [\"{p['full']}\"]",
            "tags: [github, ai, vibe-coding, project]",
            f"stars: {p['stars']}",
            f"today_growth: {p['today_growth']}",
            f"created_at: {p['created_at']}",
            f"status: {status}",
            f"date_accessed: {today}",
            "---",
            "",
            f"# {p['full']}",
            "",
            "## 定位",
            p["description"] or "（待补充）",
            "",
            "## 技术栈",
            f"- 主语言：{p['language']}",
            f"- Topics：{', '.join(p.get('topics', [])) or '—'}",
            f"- License：{p['license']}",
            "",
            "## 外部链接",
            f"- GitHub：{p['url']}",
            f"- Stars：⭐{fmt_star(p['stars'])}（今日 🔺{p['today_growth']:,}）",
            "",
            "## 反向链接",
            backlink,
            "",
        ]
        path.write_text("\n".join(content) + "\n", encoding="utf-8")
        main.log(f"项目页新建：{path}")
        return

    # 更新：保留已有正文，定点刷新 frontmatter 数值 + 追加回链
    text = path.read_text(encoding="utf-8")
    text = _replace_frontmatter(text, "stars", str(p["stars"]))
    text = _replace_frontmatter(text, "today_growth", str(p["today_growth"]))
    text = _replace_frontmatter(text, "status", status)
    text = _replace_frontmatter(text, "date_accessed", today)
    if backlink not in text:
        if "## 反向链接" in text:
            text = text.rstrip() + "\n" + backlink + "\n"
        else:
            text = text.rstrip() + "\n\n## 反向链接\n" + backlink + "\n"
    path.write_text(text, encoding="utf-8")  # 同模式读写，保留原 CRLF
    main.log(f"项目页更新：{path}（{status}）")


def _replace_frontmatter(text, key, value):
    """定点替换 YAML 某字段值（保留其余内容与换行符）。"""
    pattern = re.compile(rf"^{re.escape(key)}: .*$", re.M)
    if pattern.search(text):
        return pattern.sub(f"{key}: {value}", text)
    # 字段不存在则插入到第一个 '---' 块内
    return text


def _rebuild_index(date, daily_name, is_sunday):
    idx = OBSIDIAN / "_Index.md"
    # 收集所有日报
    rows = []
    for f in DAILY_DIR.glob("*.md"):
        name = f.stem
        m = re.match(r"(Vibe-Coding|AI-Weekly)-(\d{4}-\d{2}-\d{2})", name)
        if not m:
            continue
        kind = "周报" if m.group(1) == "AI-Weekly" else "日报"
        rows.append((m.group(2), kind, name))
    rows.sort(key=lambda x: x[0], reverse=True)

    md = []
    md.append("---")
    md.append("title: GitHub AI 项目归档索引")
    md.append("tags: [index, github, ai]")
    md.append("---")
    md.append("")
    md.append("# _Index — GitHub AI 项目归档")
    md.append("")
    md.append("## 日期表")
    md.append("")
    md.append("| 日期 | 类型 | 入口 |")
    md.append("|---|---|---|")
    for d, kind, name in rows:
        md.append(f"| {d} | {kind} | [[Daily/{name}|{name}]] |")
    md.append("")
    md.append("## 项目索引")
    md.append("")
    md.append("> 项目页按首字母聚合于 [[Projects]] 目录。")
    idx.write_text("\n".join(md) + "\n", encoding="utf-8")
    main.log(f"全局索引重建：{idx}（{len(rows)} 篇日报）")


# ----------------------------------------------------------------------------
# 步骤4b：生成 ima 干净载体 + 待推队列
# ----------------------------------------------------------------------------
def build_ima_carrier(date, top, all_projects, full_track=False):
    is_sunday = date.weekday() == 6
    mode = "全赛道" if is_sunday else "Vibe Coding 赛道"
    best = top[0] if top else None
    used_fallback = any(p.get("source") == "search-api-fallback" for p in top)

    def fmt_growth(p):
        if used_fallback or p.get("today_growth", 0) == 0:
            return "—"
        return f"🔺{p['today_growth']:,}"

    md = []
    md.append(f"# GitHub AI 项目{'周报' if is_sunday else '日报'} · {mode} · {date.isoformat()}")
    md.append("")
    if used_fallback:
        md.append("> ⚠️ 数据源降级：GitHub Trending 主站不可达，改用 api.github.com Search API 近似榜"
                  "（按总 Star 降序，无当日新增，增长列以 — 表示）。")
    md.append("> 数据源：GitHub Trending 飙升榜（按当日"
              + "新增 Star 降序）+ GitHub REST API 实时补全。" if not used_fallback
              else "> 数据源：api.github.com Search API 近似榜（降级，无当日新增）。")
    if best:
        md.append("")
        md.append("## 🔝 今日最佳")
        md.append("")
        md.append(f"**{best['full']}** — {fmt_growth(best)} / ⭐{fmt_star(best['stars'])}"
                  f" / {best['language']}")
        md.append(f"- 链接：{best['url']}")
        md.append(f"- 简介：{best['description']}")
    md.append("")
    md.append("## 分类速览（" + ("按总 Star 近似降序（降级）" if used_fallback
              else "按当日新增降序") + "）")
    md.append("")
    md.append("| # | 项目 | 语言 | ⭐ | 📈 新增 | 入选依据 |")
    md.append("|---|---|---|---|---|---|")
    for i, p in enumerate(top, 1):
        if p.get("strict_hit"):
            basis = "严格命中"
        elif full_track:
            basis = "全赛道"
        else:
            basis = f"生态扩充(分{p.get('eco_score',0)})"
        md.append(f"| {i} | [{p['full']}]({p['url']}) | {p['language']} | "
                  f"{fmt_star(p['stars'])} | {fmt_growth(p)} | {basis} |")
    md.append("")
    # 始终计算（趋势解读段会引用），仅 full_track 模式跳过其文档小节（避免与全赛道主表重复）
    all_lst = all_track_top(all_projects, vc.ALL_TRACK_TOP_N)
    if not full_track:
        # ---- 全赛道爆款 ----
        md.append("")
        md.append(f"## 🌐 全赛道爆款 Top{len(all_lst)}")
        md.append("")
        md.append("> GitHub Trending 全局（不限 Vibe Coding 赛道），按当日新增 Star 降序"
                  + ("（降级：按总 Star 近似）" if used_fallback else "") + "。")
        md.append("")
        md.append("| # | 项目 | 语言 | ⭐ | 📈 新增 |")
        md.append("|---|---|---|---|---|")
        for i, p in enumerate(all_lst, 1):
            md.append(f"| {i} | [{p['full']}]({p['url']}) | {p['language']} | "
                      f"{fmt_star(p['stars'])} | {fmt_growth(p)} |")
        md.append("")
    # ---- 爆款小众（短视频同款） ----
    niche_lst = niche_top(all_projects, vc.NICHE_TOP_N, vc.NICHE_STARS_MAX, vc.NICHE_GROWTH_MIN)
    md.append(f"## 💡 爆款小众热门（短视频同款）Top{len(niche_lst)}")
    md.append("")
    md.append(f"> 筛选口径：当日 Trending 中总 Star 最小的一批（总 Star < {vc.NICHE_STARS_MAX:,}，"
              f"排除绝对头部 mega 仓库），按当日新增降序取 Top{len(niche_lst)}——这类「小众但爆发」项目正是"
              "抖音/快手/B站/视频号等短视频平台开发者账号最常讲解的品类。🔥 = 当日新增 ≥ "
              f"{vc.NICHE_GROWTH_MIN}。")
    if used_fallback:
        md.append("> ⚠️ 降级通道无当日新增数据，本期以「总 Star 最低」做弱近似，非真实爆款信号。")
    md.append("> 数据说明：本自动化暂以 GitHub Trending 增速近似该信号（无公开短视频平台热榜 API）；"
              "如需真实平台信号可接入数据源（如 HelloGitHub / 今日热榜）续做。")
    md.append("")
    md.append("| # | 项目 | 语言 | ⭐ | 📈 新增 | 一句话亮点 |")
    md.append("|---|---|---|---|---|---|")
    for i, p in enumerate(niche_lst, 1):
        hot = "🔥 " if _growth_key(p) >= vc.NICHE_GROWTH_MIN else ""
        md.append(f"| {i} | {hot}[{p['full']}]({p['url']}) | {p['language']} | "
                  f"{fmt_star(p['stars'])} | {fmt_growth(p)} | {_sanitize_cell(p['description'])} |")
    md.append("")
    md.append("## 趋势解读")
    md.append("")
    langs = {}
    for p in top:
        langs[p["language"]] = langs.get(p["language"], 0) + 1
    md.append(f"- 语言分布：{', '.join(f'{k}×{v}' for k, v in sorted(langs.items(), key=lambda x:-x[1]))}")
    strict_n = sum(1 for p in top if p.get("strict_hit"))
    md.append(f"- 严格关键词命中 {strict_n} 个，生态扩充 {len(top)-strict_n} 个。")
    md.append(f"- 全赛道爆款收录 {len(all_lst)} 个；爆款小众（短视频同款）收录 {len(niche_lst)} 个。")
    md.append("")
    md.append("---")
    md.append("")
    md.append(f"详细项目页见 Obsidian 知识库：Obsidian_Vault/Daily/"
              f"{'AI-Weekly' if is_sunday else 'Vibe-Coding'}-{date.isoformat()}.md")

    carrier_path = IMA_CARRIER / f"ima_GitHub_VibeCoding_{date.isoformat()}.md"
    carrier_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    size = carrier_path.stat().st_size
    main.log(f"ima 载体已生成：{carrier_path}（{size} 字节）")

    # 待推队列（P0-1：连接器断开时由 agent 恢复后消费）
    pending = IMA_CARRIER / f".pending_{date.isoformat()}.json"
    pending.write_text(json.dumps({
        "date": date.isoformat(),
        "file": str(carrier_path),
        "file_size": size,
        "knowledge_base_id": vc.IMA_KB_ID,
        "knowledge_base_name": vc.IMA_KB_NAME,
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "done": False,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    main.log(f"ima 待推队列已写入：{pending}")
    return carrier_path


# ----------------------------------------------------------------------------
# 步骤5：git 同步（仅 Obsidian_Vault/，win 分支）
# ----------------------------------------------------------------------------
def git_sync_obsidian(date, do_push=True):
    os.environ["GITHUB_TARGET_BRANCH"] = "win"
    main.pre_sync_pull()
    rc, _, _ = main.run_cmd(["git", "checkout", "win"], cwd=ROOT, timeout=30)
    if rc != 0:
        main.run_cmd(["git", "fetch", "origin", "win"], cwd=ROOT, timeout=60)
        main.run_cmd(["git", "checkout", "-b", "win", "origin/win"], cwd=ROOT, timeout=30)
    main.run_cmd(["git", "add", "Obsidian_Vault/"], cwd=ROOT, timeout=60)
    rc, _, _ = main.run_cmd(["git", "diff", "--cached", "--quiet"], cwd=ROOT, timeout=30)
    if rc != 0:
        msg = f"[{date.isoformat()}] Daily AI Project Update"
        main.run_cmd(["git", "commit", "-m", msg], cwd=ROOT, timeout=60)
        main.log("✅ 已提交 Obsidian_Vault/ 变更（win 分支）")
    else:
        main.log("ℹ️ 无 Obsidian_Vault/ 变更，跳过提交")
    if not do_push:
        return True, "dry-run (no push)"
    rc, out, err = main._push_with_resilience("win")
    if rc == 0:
        flag = LOGS_DIR / "PUSH_STUCK.flag"
        if flag.exists():
            flag.unlink()
        return True, out
    (LOGS_DIR / "PUSH_STUCK.flag").write_text(
        f"{date.isoformat()} push failed: {err[:300]}\n", encoding="utf-8")
    return False, err
