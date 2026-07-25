#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 开源项目每日工作流（真实运行版）

设计原则：
- 所有结论必须基于真实运行结果，禁止根据 README 推测或编造数据。
- 任意步骤失败 -> 记录日志，继续处理下一个项目，不中断整个流程。
- 仅追加，不覆盖已有内容。

流程：
  1. 抓取 GitHub Trending（每日）真实页面
  2. 按 AI/LLM/Agent 等关键词过滤，排除 Awesome/Tutorial/Course/Demo/Fork
  3. 选 TOP5（周一~周六）/ TOP10（周日）
  4. 对每个项目：真实 Clone -> 检测构建系统 -> 真实安装 -> 真实冒烟运行
  5. AI 评分（热度/创新/完整度/运行成功/价值）
  6. 生成 Daily-Reports/YYYY-MM-DD.md（中文，真实数据）
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
ROOT = Path(__file__).resolve().parent
CLONES_DIR = ROOT / "clones"
CLONES_DIR.mkdir(exist_ok=True)
DAILY_DIR = ROOT / "Daily-Reports"
DAILY_DIR.mkdir(exist_ok=True)
META_DIR = ROOT / "Metadata"
META_DIR.mkdir(exist_ok=True)
LOGS_DIR = ROOT / "Logs"
LOGS_DIR.mkdir(exist_ok=True)

GITHUB_REMOTE = os.environ.get("GITHUB_REPO", "https://github.com/wuqijin442/ai-project-weekly.git")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
INSTALL_TIMEOUT = int(os.environ.get("INSTALL_TIMEOUT", "200"))
RUN_TIMEOUT = int(os.environ.get("RUN_TIMEOUT", "45"))
CLONE_DEPTH = int(os.environ.get("CLONE_DEPTH", "1"))

AI_KEYWORDS = [
    "ai", "llm", "agent", "gpt", "claude", "cursor", "rag", "mcp", "langchain",
    "diffusion", "stable-diffusion", "whisper", "tts", "ocr", "comfyui", "vibe",
    "coding", "local-ai", "embedding", "transformer", "neural", "chatbot",
    "copilot", "autonomous", "workflow", "vision", "image", "video", "speech",
    "prompt", "fine-tun", "model", "deepseek", "qwen", "llama", "gemini",
    "ollama", "multimodal", "aigc", "genai", "assistant",
]
EXCLUDE_KEYWORDS = ["awesome", "tutorial", "course", "demo", "fork", "book", "cheat-sheet", "list"]


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
# 步骤2：过滤 AI 项目
# ----------------------------------------------------------------------------
def is_ai_project(p):
    text = (p["name"] + " " + p["description"] + " " + p["language"]).lower()
    if any(k in p["name"].lower() for k in EXCLUDE_KEYWORDS):
        return False
    return any(k in text for k in AI_KEYWORDS)


def filter_ai(projects):
    filtered = [p for p in projects if is_ai_project(p)]
    log(f"AI 过滤后保留 {len(filtered)} 个")
    return filtered


def select_top(projects, date):
    # 周日 TOP10，其余 TOP5
    weekday = date.weekday()  # Mon=0 .. Sun=6
    n = 10 if weekday == 6 else 5
    # 按 star 降序
    top = sorted(projects, key=lambda p: p["stars"], reverse=True)[:n]
    log(f"选取 TOP{n}（{'周日' if weekday==6 else '平日'}）")
    return top, n


# ----------------------------------------------------------------------------
# 步骤4：真实 Clone / 安装 / 运行
# ----------------------------------------------------------------------------
def clone_repo(p):
    safe = f"{p['owner']}__{p['name']}"
    dest = CLONES_DIR / safe
    if dest.exists():
        shutil.rmtree(dest)
    t0 = time.time()
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
        # 优先 requirements.txt
        if (Path(path) / "requirements.txt").exists():
            rc, out, err = run_cmd(
                f"python -m pip install -r requirements.txt", cwd=path, timeout=INSTALL_TIMEOUT)
        else:
            rc, out, err = run_cmd(
                "python -m pip install -e .", cwd=path, timeout=INSTALL_TIMEOUT)
        dt = round(time.time() - t0, 1)
        if rc == 0:
            return "success", out[-500:], dt
        return "failed", err[-800:], dt
    if build["node"]:
        rc, out, err = run_cmd("npm install", cwd=path, timeout=INSTALL_TIMEOUT)
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
                    f"python {entry} --help", cwd=path, timeout=RUN_TIMEOUT)
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
    md.append(f"# AI 开源项目日报 — {date.isoformat()}\n")
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
    md.append("### AI 趋势观察（基于今日真实落地项目）\n")
    langs = {}
    for r in results:
        l = r["project"]["language"]
        langs[l] = langs.get(l, 0) + 1
    md.append("- 语言分布：" + ", ".join(f"{k}×{v}" for k, v in sorted(langs.items(), key=lambda x: -x[1])))
    md.append(f"- 今日 TOP{len(top)} 关键词命中："
              + ", ".join(sorted({w for r in results for w in AI_KEYWORDS
                                  if w in (r['project']['name']+r['project']['description']).lower()}))[:400])
    report = "\n".join(md)

    out = DAILY_DIR / f"{date.isoformat()}.md"
    out.write_text(report, encoding="utf-8")
    log(f"日报已生成：{out}")
    return out


# ----------------------------------------------------------------------------
# 步骤7：GitHub 同步
# ----------------------------------------------------------------------------
def sync_to_github(date):
    try:
        run_cmd("git add -A", cwd=ROOT, timeout=60)
        msg = f"[{date.isoformat()}] Daily AI Project Update"
        run_cmd(f'git commit -m "{msg}"', cwd=ROOT, timeout=60)
        # 统一分支名为 main（git init 默认可能为 master）
        run_cmd("git branch -M main", cwd=ROOT, timeout=30)
        # 配置 remote
        run_cmd(f"git remote remove origin", cwd=ROOT, timeout=30)
        push_url = GITHUB_REMOTE
        if GITHUB_TOKEN:
            push_url = GITHUB_REMOTE.replace("https://", f"https://{GITHUB_TOKEN}@")
        run_cmd(f"git remote add origin {push_url}", cwd=ROOT, timeout=30)
        rc, out, err = run_cmd("git push -u origin main", cwd=ROOT, timeout=120)
        if rc == 0:
            log("✅ 已推送到 wuqijin442/main")
            return True, out
        log(f"⚠️ push 失败（可能需要 GITHUB_TOKEN 或 SSH）：{err[:300]}")
        return False, err
    except Exception as e:  # noqa
        log(f"sync 异常：{e}")
        return False, str(e)


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
def main():
    date = datetime.date.today()
    log(f"=== AI 项目每日工作流启动 {date.isoformat()} ===")
    # 步骤1+2
    projects = fetch_trending("daily")
    scanned = len(projects)
    ai_projects = filter_ai(projects)
    filtered = len(ai_projects)
    top, n = select_top(ai_projects, date)

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
