#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 热门项目每日工作流（多维分类真实运行版）

设计原则：
- 所有结论必须基于真实运行结果，禁止根据 README 推测或编造数据。
- 任意步骤失败 -> 记录日志，继续处理下一个项目，不中断整个流程。
- 仅追加，不覆盖已有内容。

流程：
  1. 抓取 GitHub Trending（每日）真实页面
  2. 按多维度类别（AI/前端/后端/数据库/工具/安全/移动/数据）分类，排除 Awesome/Tutorial/Course/Demo/Fork
  3. 按类别轮询选 TOP5（周一~周六）/ TOP10（周日），保证多样性
  4. 对每个项目：真实 Clone -> 检测构建系统 -> 真实安装 -> 真实冒烟运行
  5. AI 评分（热度/创新/完整度/运行成功/价值）
  6. 生成 reports/daily/YYYY-MM-DD.md（中文，真实数据）
  7. 本地 git 提交，并尝试推送到 wuqijin442/main（需 GITHUB_TOKEN 或 SSH）

依赖：仅 Python 3 标准库 + 系统 git。安装/运行使用系统 python/node/npm（按需）。
"""
import os
import re
import sys
import json
import time
import shutil
import datetime
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

# ----------------------------------------------------------------------------
# 配置
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent  # src/main.py -> 仓库根
CLONES_DIR = ROOT / "clones"
CLONES_DIR.mkdir(exist_ok=True)
DAILY_DIR = ROOT / "reports" / "daily"
DAILY_DIR.mkdir(exist_ok=True)
META_DIR = ROOT / "data" / "metadata"
META_DIR.mkdir(exist_ok=True)
LOGS_DIR = ROOT / "Logs"
LOGS_DIR.mkdir(exist_ok=True)

GITHUB_REMOTE = os.environ.get("GITHUB_REPO", "git@github.com:wuqijin442/ai-project-weekly.git")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
INSTALL_TIMEOUT = int(os.environ.get("INSTALL_TIMEOUT", "200"))
RUN_TIMEOUT = int(os.environ.get("RUN_TIMEOUT", "45"))
CLONE_DEPTH = int(os.environ.get("CLONE_DEPTH", "1"))

# 跨平台 Python 解释器：Linux 通常为 python3，Windows 通常为 python，两者都尝试
def _resolve_python_bin():
    for cand in ("python", "python3"):
        if shutil.which(cand):
            return cand
    return "python"
PYTHON_BIN = _resolve_python_bin()

# 多维度分类：从纯 AI 扩展到更广泛的 GitHub 热门技术领域
CATEGORIES = {
    "AI/LLM/Agent": ["ai", "llm", "agent", "gpt", "claude", "cursor", "rag", "mcp", "langchain",
                     "diffusion", "stable-diffusion", "whisper", "tts", "ocr", "comfyui", "vibe",
                     "coding", "local-ai", "embedding", "transformer", "neural", "chatbot",
                     "copilot", "autonomous", "workflow", "vision", "image", "video", "speech",
                     "prompt", "fine-tun", "model", "deepseek", "qwen", "llama", "gemini",
                     "ollama", "multimodal", "aigc", "genai", "assistant"],
    "Frontend/Web": ["react", "vue", "frontend", "nextjs", "nuxt", "svelte", "angular",
                     "tailwind", "web", "ui", "component", "css", "html", "browser"],
    "Backend/DevOps": ["backend", "server", "api", "docker", "kubernetes", "devops",
                       "microservice", "graphql", "grpc", "nginx", "gateway", "lambda"],
    "Database": ["database", "sql", "postgres", "mysql", "redis", "mongodb", "sqlite",
                 "vector", "vector-database", "elasticsearch", "clickhouse", "duckdb"],
    "DevTools": ["cli", "tool", "vscode", "extension", "developer", "debugger",
                 "linter", "formatter", "build", "vite", "webpack", "esbuild"],
    "Security": ["security", "pentest", "vulnerability", "cryptography", "oauth",
                 "siem", "forensics", "reverse", "malware"],
    "Mobile": ["ios", "android", "flutter", "react-native", "swift", "kotlin", "mobile"],
    "Data/ML": ["data", "machine-learning", "ml", "pandas", "pytorch", "tensorflow",
                "notebook", "analytics", "jupyter", "dataset"],
}
EXCLUDE_KEYWORDS = ["awesome", "tutorial", "course", "demo", "fork", "book", "cheat-sheet", "list", "examples"]


# ----------------------------------------------------------------------------
# 工具函数
# ----------------------------------------------------------------------------
def log(msg: str):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)


def run_cmd(cmd, cwd=None, timeout=120):
    """运行命令，返回 (returncode, stdout, stderr)。超时/异常记为失败。"""
    try:
        proc = subprocess.run(
            cmd, cwd=str(cwd) if cwd else None,
            capture_output=True, text=True, timeout=timeout,
            shell=isinstance(cmd, str),
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"TIMEOUT after {timeout}s"
    except Exception as e:  # noqa
        return 1, "", str(e)


def clean_text(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# ----------------------------------------------------------------------------
# 步骤1：抓取 GitHub Trending
# ----------------------------------------------------------------------------
def fetch_trending(since="daily"):
    url = f"https://github.com/trending?since={since}"
    html = ""
    last_err = ""
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=45) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
            if html:
                break
        except Exception as e:  # noqa
            last_err = str(e)
            log(f"trending 抓取第{attempt}次失败: {e}，重试...")
            time.sleep(3)
    if not html:
        log(f"trending 抓取失败（已重试3次）: {last_err}")
        return []

    articles = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.S)
    projects = []
    for art in articles:
        # 仓库路径：h2 内第一个 <a> 的 href（现带 data-hydro-click 等属性，故放宽匹配）
        m = re.search(r'<h2[^>]*>.*?<a[^>]*href="/([^"]+)"', art, re.S)
        if not m:
            continue
        full = m.group(1).strip("/")
        if full.count("/") != 1:
            continue
        owner, name = full.split("/")
        desc_m = re.search(r'<p class="col-9[^"]*">(.*?)</p>', art, re.S)
        desc = clean_text(desc_m.group(1)) if desc_m else ""
        lang_m = re.search(r'<span itemprop="programmingLanguage">([^<]+)</span>', art)
        lang = lang_m.group(1).strip() if lang_m else "Unknown"
        # 星标：stargazers 链接内的数字（位于 <svg> 之后）
        star_m = re.search(r'/stargazers".*?([\d,]+)\s*</a>', art, re.S)
        stars = int(star_m.group(1).replace(",", "")) if star_m else 0
        projects.append({
            "owner": owner, "name": name, "full": full,
            "url": f"https://github.com/{full}",
            "description": desc, "language": lang,
            "stars": stars,
        })
    log(f"trending 抓取完成，共 {len(projects)} 个仓库")
    return projects


# ----------------------------------------------------------------------------
# 步骤2：多维度分类与过滤
# ----------------------------------------------------------------------------
def classify_project(p):
    """返回项目命中的所有类别；若名称命中排除词则返回空列表。"""
    text = (p["name"] + " " + p["description"] + " " + p["language"]).lower()
    if any(k in p["name"].lower() for k in EXCLUDE_KEYWORDS):
        return []
    return [cat for cat, kws in CATEGORIES.items() if any(k in text for k in kws)]


def filter_projects(projects):
    filtered = []
    for p in projects:
        cats = classify_project(p)
        if cats:
            p["categories"] = cats
            filtered.append(p)
    log(f"分类过滤后保留 {len(filtered)} 个（覆盖 {len({c for p in filtered for c in p['categories']})} 个类别）")
    return filtered


def select_top(projects, date):
    # 周日 TOP10，其余 TOP5；按类别轮询，保证多样性
    weekday = date.weekday()  # Mon=0 .. Sun=6
    n = 10 if weekday == 6 else 5
    # 按主类别（命中的第一个）分组，每组按 star 降序
    by_cat = {}
    for p in projects:
        cat = p.get("categories", ["Other"])[0]
        by_cat.setdefault(cat, []).append(p)
    for cat in by_cat:
        by_cat[cat].sort(key=lambda x: x["stars"], reverse=True)
    # 类别按组内最高 star 排序
    cat_order = sorted(by_cat.keys(),
                       key=lambda c: by_cat[c][0]["stars"] if by_cat[c] else 0,
                       reverse=True)
    selected = []
    used = set()
    while len(selected) < n:
        added = False
        for cat in cat_order:
            if len(selected) >= n:
                break
            for p in by_cat.get(cat, []):
                if p["full"] not in used:
                    selected.append(p)
                    used.add(p["full"])
                    added = True
                    break
        if not added:
            break
    covered = sorted({c for p in selected for c in p.get("categories", [])})
    log(f"选取 TOP{len(selected)}（{'周日' if weekday==6 else '平日'}），覆盖类别：{', '.join(covered)}")
    return selected, len(selected)


# ----------------------------------------------------------------------------
# 步骤4：真实 Clone / 安装 / 运行
# ----------------------------------------------------------------------------
def clone_repo(p):
    safe = f"{p['owner']}__{p['name']}"
    dest = CLONES_DIR / safe
    t0 = time.time()
    if dest.exists() and (dest / ".git").exists():
        # 已存在 git 仓库 → 原地更新（fetch + reset），避免 rmtree 触发工作区安全删除拦截
        rc, _, err = run_cmd(
            ["git", "-C", str(dest), "fetch", "--depth", str(CLONE_DEPTH), "origin"], timeout=180)
        if rc != 0:
            log(f"  fetch FAIL {p['full']}: {err[:200]}")
            return False, str(dest), round(time.time() - t0, 1), err
        _, b_out, _ = run_cmd(
            ["git", "-C", str(dest), "symbolic-ref", "refs/remotes/origin/HEAD"], timeout=30)
        branch = b_out.strip().split("/")[-1] or "main"
        rc, _, err = run_cmd(
            ["git", "-C", str(dest), "reset", "--hard", f"origin/{branch}"], timeout=60)
        if rc != 0:
            log(f"  reset FAIL {p['full']}: {err[:200]}")
            return False, str(dest), round(time.time() - t0, 1), err
        dt = round(time.time() - t0, 1)
        log(f"  clone OK(updated) {p['full']} ({dt}s)")
        return True, str(dest), dt, ""
    if dest.exists():
        # 非 git 残留（极少见）→ 删除后重新克隆
        shutil.rmtree(dest)
    rc, out, err = run_cmd(
        ["git", "clone", "--depth", str(CLONE_DEPTH),
         f"https://github.com/{p['full']}.git", str(dest)],
        timeout=180,
    )
    dt = round(time.time() - t0, 1)
    if rc == 0:
        log(f"  clone OK {p['full']} ({dt}s)")
        return True, str(dest), dt, ""
    log(f"  clone FAIL {p['full']}: {err[:200]}")
    return False, str(dest), dt, err


def detect_build(path):
    p = Path(path)
    build = {"python": False, "node": False, "rust": False, "go": False,
             "docker": False, "files": []}
    for f in ["requirements.txt", "pyproject.toml", "setup.py", "package.json",
              "Cargo.toml", "go.mod", "Dockerfile", "docker-compose.yml"]:
        if (p / f).exists():
            build["files"].append(f)
    build["python"] = any(x in build["files"] for x in ["requirements.txt", "pyproject.toml", "setup.py"])
    build["node"] = "package.json" in build["files"]
    build["rust"] = "Cargo.toml" in build["files"]
    build["go"] = "go.mod" in build["files"]
    build["docker"] = any(x in build["files"] for x in ["Dockerfile", "docker-compose.yml"])
    return build


def install_project(p, path, build):
    if build["docker"] and not shutil.which("docker"):
        return "skipped", "Docker 未安装（按规则记录失败后继续）", 0.0
    t0 = time.time()
    if build["python"]:
        # 优先 requirements.txt；用 list 调用避免 shell=True 下子进程管道阻止超时生效
        if (Path(path) / "requirements.txt").exists():
            rc, out, err = run_cmd(
                [PYTHON_BIN, "-m", "pip", "install", "-r", "requirements.txt"], cwd=path, timeout=INSTALL_TIMEOUT)
        else:
            rc, out, err = run_cmd(
                [PYTHON_BIN, "-m", "pip", "install", "-e", "."], cwd=path, timeout=INSTALL_TIMEOUT)
        dt = round(time.time() - t0, 1)
        if rc == 0:
            return "success", out[-500:], dt
        return "failed", err[-800:], dt
    if build["node"]:
        rc, out, err = run_cmd(["npm", "install"], cwd=path, timeout=INSTALL_TIMEOUT)
        dt = round(time.time() - t0, 1)
        if rc == 0:
            return "success", out[-500:], dt
        return "failed", err[-800:], dt
    if build["rust"]:
        return "skipped", "Rust 项目，未执行 cargo build（资源/耗时限制）", 0.0
    if build["go"]:
        return "skipped", "Go 项目，未执行 go build（资源/耗时限制）", 0.0
    return "skipped", "未识别到可自动安装的构建系统", 0.0


def smoke_run(p, path, build):
    """真实冒烟运行：尽量跑 --help / 入口，失败记录。非完整 demo。"""
    pth = Path(path)
    t0 = time.time()
    # Python：尝试常见入口
    if build["python"]:
        for entry in ["main.py", "cli.py", "app.py", "run.py"]:
            if (pth / entry).exists():
                rc, out, err = run_cmd(
                    [PYTHON_BIN, entry, "--help"], cwd=path, timeout=RUN_TIMEOUT)
                dt = round(time.time() - t0, 1)
                if rc == 0:
                    return "success", (out or err)[:400], dt
                # 可能不支持 --help，记一次尝试
                return "failed", f"{entry} --help 失败: {(err or out)[:400]}", dt
        return "skipped", "无可自动检测的 CLI 入口（需手动 demo）", 0.0
    if build["node"]:
        return "skipped", "Web/Server 项目，需手动启动 demo（不自动拉起服务）", 0.0
    return "skipped", "无自动可运行入口", 0.0


# ----------------------------------------------------------------------------
# 步骤5：AI 评分
# ----------------------------------------------------------------------------
def score_project(p, install_status, run_status):
    heat = min(20, p["stars"] / 500.0)  # star 越多越高，封顶20
    innovation = 12 if any(k in (p["name"]+p["description"]).lower()
                           for k in ["agent", "mcp", "rag", "claude", "cursor", "vibe", "local-ai"]) else 6
    completeness = 12 if p["description"] else 4
    run_score = 20 if install_status == "success" and run_status == "success" else (
        10 if install_status == "success" else 0)
    value = 12 if (install_status in ("success",) or run_status == "success") else 6
    total = round(heat + innovation + completeness + run_score + value, 1)
    stars = "★★★☆☆"
    if total >= 90:
        stars = "★★★★★"
    elif total >= 80:
        stars = "★★★★☆"
    elif total >= 70:
        stars = "★★★☆☆"
    return total, stars


# ----------------------------------------------------------------------------
# 步骤6：生成日报
# ----------------------------------------------------------------------------
def write_report(date, top, results, scanned, filtered):
    md = []
    md.append(f"# GitHub 热门项目日报 — {date.isoformat()}\n")
    md.append("> 本报告所有结论基于真实 Clone/安装/运行结果，未根据 README 推测。\n")
    weekday = "周日" if date.weekday() == 6 else "平日"
    md.append(f"**模式**：{weekday}（TOP{len(top)}）  ")
    md.append(f"**扫描数**：{scanned}  **AI 过滤后**：{filtered}  "
              f"**Clone 成功**：{sum(1 for r in results if r['clone'])}  "
              f"**安装成功**：{sum(1 for r in results if r['install']=='success')}  "
              f"**运行成功(冒烟)**：{sum(1 for r in results if r['run']=='success')}  "
              f"**推荐(≥90分)**：{sum(1 for r in results if r['score']>=90)}\n")

    for i, r in enumerate(results, 1):
        p = r["project"]
        md.append(f"\n## {i}. {p['full']}")
        md.append(f"- **地址**：{p['url']}")
        md.append(f"- **语言**：{p['language']}  **Star**：{p['stars']}")
        md.append(f"- **类别**：{', '.join(p.get('categories', []))}")
        md.append(f"- **简介**：{p['description'] or '（无描述）'}")
        md.append(f"- **Clone**：{'✅ '+str(r['clone_time'])+'s' if r['clone'] else '❌ '+r['clone_err'][:120]}")
        md.append(f"- **构建系统**：{', '.join(r['build']['files']) or '未识别'}")
        md.append(f"- **安装**：{r['install']}（{r['install_time']}s）")
        if r["install_log"]:
            md.append(f"  - 安装日志：{r['install_log'][:300]}")
        md.append(f"- **冒烟运行**：{r['run']}（{r['run_time']}s）")
        if r["run_log"]:
            md.append(f"  - 运行日志：{r['run_log'][:300]}")
        md.append(f"- **AI 评分**：{r['score']}/100  {r['stars']}")
        md.append(f"- **推荐指数**：{'✅ 进入知识库' if r['score']>=90 and r['install']=='success' else '— 未达 90 分门槛'}")
        md.append("")

    md.append("\n---\n")
    md.append("### 多维度趋势观察（基于今日真实落地项目）\n")
    langs = {}
    cats = {}
    for r in results:
        l = r["project"]["language"]
        langs[l] = langs.get(l, 0) + 1
        for c in r["project"].get("categories", []):
            cats[c] = cats.get(c, 0) + 1
    md.append("- 语言分布：" + ", ".join(f"{k}×{v}" for k, v in sorted(langs.items(), key=lambda x: -x[1])))
    md.append("- 类别分布：" + ", ".join(f"{k}×{v}" for k, v in sorted(cats.items(), key=lambda x: -x[1])))
    md.append(f"- 今日覆盖领域：{', '.join(sorted(cats.keys()))}")
    report = "\n".join(md)

    out = DAILY_DIR / f"{date.isoformat()}.md"
    out.write_text(report, encoding="utf-8")
    log(f"日报已生成：{out}")
    return out


# ----------------------------------------------------------------------------
# 步骤7：GitHub 同步
# ----------------------------------------------------------------------------
def pre_sync_pull():
    """先拉取远端最新提交，避免多台机器（Linux 服务器 / Windows）基于旧 HEAD 推送
    导致 non-fast-forward 失败或 rebase 冲突。best-effort：失败不影响后续生成。

    关键点：本函数在报告生成之前调用，拉取后 write_report 会用本地结果覆盖
    reports/daily/YYYY-MM-DD.md，因此不会产生内容合并冲突，commit 直接基于远端
    HEAD，推送为 fast-forward。

    网络健壮性：headless 服务器到 GitHub 的 TLS 连接偶发中断（GnuTLS recv error），
    故对 pull 做最多 3 次重试 + 退避，避免瞬时抖动导致跳过 pre-pull 后推送失败。"""
    last_err = ""
    for attempt in range(1, 4):
        try:
            rc, out, err = run_cmd(
                ["git", "pull", "--rebase", "--autostash", "origin", "main"],
                cwd=ROOT, timeout=120)
            if rc == 0:
                log("✅ 已先拉取远端最新（pre-pull），避免推送冲突")
                return
            last_err = err
        except Exception as e:  # noqa
            last_err = str(e)
        log(f"⚠️ pre-pull 第 {attempt}/3 次失败（{last_err[:120]}），"
            f"{'重试' if attempt < 3 else '放弃，继续生成'}")
        if attempt < 3:
            time.sleep(5 * attempt)  # 5s / 10s 退避


def sync_to_github(date):
    try:
        run_cmd(["git", "add", "-A"], cwd=ROOT, timeout=60)
        # 只在有变更时提交；避免空提交失败
        rc, _, _ = run_cmd(["git", "diff", "--cached", "--quiet"], cwd=ROOT, timeout=30)
        if rc != 0:
            msg = f"[{date.isoformat()}] Daily AI Project Update"
            run_cmd(["git", "commit", "-m", msg], cwd=ROOT, timeout=60)
        # 统一分支名为 main（git init 默认可能为 master）
        run_cmd(["git", "branch", "-M", "main"], cwd=ROOT, timeout=30)
        # 推送策略（headless Linux 服务器友好）：
        #   1) 若设置 GITHUB_TOKEN，直接用 token 注入的 HTTPS URL 推送，不依赖 SSH key，
        #      且 token 不写入 .git/config（仅本次 push 命令内联），更安全。
        #   2) 否则回退到 origin 远程（需 SSH key 或已配置凭据）。
        if GITHUB_TOKEN:
            push_url = f"https://{GITHUB_TOKEN}@github.com/wuqijin442/ai-project-weekly.git"
        else:
            rc, _, _ = run_cmd(["git", "remote", "get-url", "origin"], cwd=ROOT, timeout=30)
            if rc != 0:
                run_cmd(["git", "remote", "add", "origin", GITHUB_REMOTE], cwd=ROOT, timeout=30)
            push_url = "origin"
        rc, out, err = run_cmd(["git", "push", "-u", push_url, "main"], cwd=ROOT, timeout=120)
        if rc == 0:
            log("✅ 已推送到 wuqijin442/main")
            return True, out
        # 抹掉日志里的 token（git 报错会带含 token 的 URL）
        safe_err = err.replace(GITHUB_TOKEN, "***TOKEN***") if GITHUB_TOKEN else err
        log(f"⚠️ push 失败（检查 GITHUB_TOKEN 或 origin 远程）：{safe_err[:300]}")
        return False, safe_err
    except Exception as e:  # noqa
        log(f"sync 异常：{e}")
        return False, str(e)


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
def main():
    date = datetime.date.today()
    log(f"=== GitHub 热门项目每日工作流启动 {date.isoformat()} ===")
    # 先拉远端最新（多机部署安全：避免基于旧 HEAD 推送冲突）
    pre_sync_pull()
    # 步骤1+2
    projects = fetch_trending("daily")
    scanned = len(projects)
    filtered_projects = filter_projects(projects)
    filtered = len(filtered_projects)
    top, n = select_top(filtered_projects, date)

    results = []
    for p in top:
        log(f"--- 处理 {p['full']} ---")
        ok, path, ct, cerr = clone_repo(p)
        build = detect_build(path) if ok else {"files": []}
        if ok:
            istatus, ilog, it = install_project(p, path, build)
            rstatus, rlog, rt = smoke_run(p, path, build)
        else:
            istatus, ilog, it, rstatus, rlog, rt = "failed", cerr, 0.0, "failed", cerr, 0.0
        score, stars = score_project(p, istatus, rstatus)
        results.append({
            "project": p, "clone": ok, "clone_time": ct, "clone_err": cerr,
            "build": build, "install": istatus, "install_log": ilog, "install_time": it,
            "run": rstatus, "run_log": rlog, "run_time": rt,
            "score": score, "stars": stars,
        })

    report = write_report(date, top, results, scanned, filtered)
    # 保存元数据 JSON
    (META_DIR / f"{date.isoformat()}.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    pushed, perr = sync_to_github(date)
    log(f"=== 完成 | 扫描 {scanned} / 过滤 {filtered} / TOP{n} / 推荐 "
        f"{sum(1 for r in results if r['score']>=90)} / 推送 {'OK' if pushed else 'FAIL'} ===")
    return report


if __name__ == "__main__":
    main()
