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
import tempfile
import signal
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
# 主站 github.com 被阻断时，是否启用官方备用通道（api.github.com / codeload.github.com）
FALLBACK_ENABLED = os.environ.get("GH_FALLBACK", "1") == "1"
TRENDING_ROUNDS = int(os.environ.get("TRENDING_ROUNDS", "8"))

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
    """运行命令，返回 (returncode, stdout, stderr)。超时/异常记为失败。

    关键修复（2026-08-11）：原实现用 subprocess.run(capture_output=True) 在超时后只能
    kill 直接子进程（如 npm），但 npm 派生的 node 孙进程会继承 stdout 管道句柄，
    导致 communicate() 永远阻塞在孙进程持有的管道上 → 进程假死（零子进程、低 CPU、
    communicate 不死）。改为：① 输出重定向到临时文件（不走 PIPE，wait() 不会读管道，
    永不被孙进程阻塞）；② 超时后按进程树整体杀死（Windows: taskkill /T /PID；
    POSIX: killpg），彻底清除孙进程。stdout/stderr 仍分别落盘，调用方 err 语义不变。
    """
    out_path = err_path = None
    try:
        out_f = tempfile.NamedTemporaryFile(mode="w", suffix=".out", delete=False,
                                            encoding="utf-8", errors="ignore")
        err_f = tempfile.NamedTemporaryFile(mode="w", suffix=".err", delete=False,
                                            encoding="utf-8", errors="ignore")
        out_path, err_path = out_f.name, err_f.name
        # with 块结束后父进程关闭句柄，但 Popen 已 dup2 到子进程，子进程句柄独立有效
        with out_f, err_f:
            proc = subprocess.Popen(
                cmd, cwd=str(cwd) if cwd else None,
                stdout=out_f, stderr=err_f,
                shell=isinstance(cmd, str),
                start_new_session=True,
            )
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            # 整棵树杀死，避免 npm 派生的 node 孙进程残留（持有文件句柄/占 CPU）
            try:
                if os.name == "nt":
                    subprocess.call(
                        ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except Exception:  # noqa
                try:
                    proc.kill()
                except Exception:
                    pass
            try:
                proc.wait(timeout=5)
            except Exception:
                pass
            return 124, "", f"TIMEOUT after {timeout}s"
        rc = proc.returncode
        with open(out_path, "r", encoding="utf-8", errors="ignore") as f:
            out = f.read()
        with open(err_path, "r", encoding="utf-8", errors="ignore") as f:
            err = f.read()
        return rc, out, err
    except Exception as e:  # noqa
        return 1, "", str(e)
    finally:
        for p in (out_path, err_path):
            if p:
                try:
                    os.unlink(p)
                except Exception:
                    pass


def clean_text(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# ----------------------------------------------------------------------------
# 官方备用通道：主站 github.com 被阻断时（TLS 握手成功但无响应 / 10060 超时），
# api.github.com 与 codeload.github.com 通常仍可达。二者均为 GitHub 官方域名，
# 用它们获取真实数据不违反"真实运行铁律"，但需在报告中标注数据获取方式。
# ----------------------------------------------------------------------------
def safe_displace(path):
    """把已存在的目录原子重命名为 _stale_*，而不是 rmtree。

    背景：本环境对一次删除大量文件有批量删除保护，rmtree 一个上万文件的
    clones 目录会直接中断整个进程（2026-08-08 步骤2 因此在 mlflow 处崩溃）。
    clones/ 已 gitignore，_stale_* 残留只占磁盘，不影响提交。
    返回 True 表示目标路径已腾空。
    """
    path = Path(path)
    if not path.exists():
        return True
    stale = path.parent / f"_stale_{path.name}_{int(time.time())}"
    try:
        path.rename(stale)
        return True
    except Exception as e:  # noqa
        log(f"  ⚠️ 目录腾挪失败 {path.name}: {str(e)[:120]}")
        return False


def api_json(url, timeout=30, attempts=3):
    """GET api.github.com 并返回 JSON；失败返回 None。"""
    headers = {"User-Agent": "ai-project-weekly", "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    for i in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8", errors="ignore"))
        except Exception as e:  # noqa
            if i == attempts:
                log(f"  api 请求失败 {url[:70]}: {str(e)[:120]}")
            else:
                time.sleep(3 * i)
    return None


def get_default_branch(full):
    data = api_json(f"https://api.github.com/repos/{full}", timeout=20, attempts=2)
    if isinstance(data, dict):
        return data.get("default_branch") or ""
    return ""


def download_tarball(full, dest, timeout=240):
    """codeload.github.com 下载源码 tar.gz 并解压到 dest（无 .git，仅源码快照）。

    用于 git clone 走不通（主站阻断）时的回退，仍是真实下载真实代码，
    足以进行真实的依赖安装与冒烟运行。返回 (ok, err)。
    """
    import tarfile
    branch = get_default_branch(full)
    cands = [b for b in [branch, "main", "master"] if b]
    seen, err = set(), ""
    dest = Path(dest)
    # ⚠️ 关键：临时目录必须与 dest 同盘（同一文件系统）。
    # 若用系统 Temp（C:）而 dest 在 D:，shutil.move 会退化为「复制 + 删除源树」，
    # 删除上万文件会触发工作区批量删除保护并直接中断进程
    # （2026-08-08 步骤2 在 huggingface/diffusers 处即因此崩溃）。
    # 同盘时 shutil.move 走 os.rename，属原子重命名，全程零删除。
    tmp_base = dest.parent / "_tmp"
    tmp_base.mkdir(parents=True, exist_ok=True)
    for br in cands:
        if br in seen:
            continue
        seen.add(br)
        url = f"https://codeload.github.com/{full}/tar.gz/refs/heads/{br}"
        safe_name = full.replace("/", "__")
        tmp_gz = tmp_base / f"{safe_name}_{br}.tar.gz"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ai-project-weekly"})
            with urllib.request.urlopen(req, timeout=timeout) as resp, open(tmp_gz, "wb") as f:
                shutil.copyfileobj(resp, f)
            tmp_dir = tmp_base / f"ex_{safe_name}_{br}_{int(time.time())}"
            tmp_dir.mkdir(parents=True, exist_ok=True)
            with tarfile.open(tmp_gz, "r:gz") as tf:
                try:
                    tf.extractall(tmp_dir, filter="data")
                except TypeError:  # Python < 3.12 无 filter 参数
                    tf.extractall(tmp_dir)
            tops = [p for p in tmp_dir.iterdir() if p.is_dir()]
            if not tops:
                err = "tarball 解压后无顶层目录"
                continue
            # 已存在目录不做 rmtree，改为原子重命名到 _stale_*
            #（clones/ 已 gitignore，残留仅占磁盘，不影响提交）
            if not safe_displace(dest):
                return False, "目标目录已存在且无法腾挪，跳过 tarball 回退"
            # ⛔ 必须用 os.rename，绝不能用 shutil.move（2026-08-31 实测）：
            # shutil.move 在 os.rename 抛 OSError 时会静默退化为「copytree + rmtree(源)」，
            # 删除上千文件触发工作区批量删除保护，直接杀死整个 Python 进程
            # （步骤2 在 AUTOMATIC1111/stable-diffusion-webui 处中断，EXIT=1，无异常可捕获）。
            # 此处改用显式 rename：失败就换下一个分支候选重试，全程零删除。
            try:
                os.rename(str(tops[0]), str(dest))
            except OSError as e:
                err = f"tarball 落位失败(rename): {str(e)[:120]}"
                continue
            # 不清理 tmp_dir / tmp_gz：任何删除都会累加到批量删除保护计数。
            # clones/*/_tmp 已随 clones/ 被 gitignore，可在运行间隙人工清理。
            return True, ""
        except Exception as e:  # noqa
            err = str(e)
    return False, err[:200]


def fetch_trending_via_api(since="daily", limit=30):
    """主站 /trending 不可达时的回退：用 Search API 取近期高热度仓库。

    近似口径：最近 1 天（周榜 7 天）内有推送、star>=200，按 star 降序。
    与官方 trending 的"当日新增 star"算法不同，报告中会显式标注。
    """
    days = 7 if since == "weekly" else 1
    since_date = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    url = ("https://api.github.com/search/repositories?q="
           f"pushed:%3E={since_date}+stars:%3E=200&sort=stars&order=desc&per_page={limit}")
    data = api_json(url, timeout=30, attempts=3)
    if not isinstance(data, dict) or not data.get("items"):
        return []
    projects = []
    for it in data["items"]:
        full = it.get("full_name", "")
        if full.count("/") != 1:
            continue
        owner, name = full.split("/")
        projects.append({
            "owner": owner, "name": name, "full": full,
            "url": it.get("html_url", f"https://github.com/{full}"),
            "description": clean_text(it.get("description") or ""),
            "language": it.get("language") or "Unknown",
            "stars": int(it.get("stargazers_count") or 0),
            "source": "search-api-fallback",
        })
    log(f"trending 回退（Search API）抓取到 {len(projects)} 个仓库")
    return projects


# ----------------------------------------------------------------------------
# 步骤1：抓取 GitHub Trending
# ----------------------------------------------------------------------------
def fetch_trending(since="daily"):
    url = f"https://github.com/trending?since={since}"
    html = ""
    last_err = ""
    # 网络韧性（与推送逻辑一致）：17:3x–19:0x 窗口 GitHub 连接间歇性重置，
    # 单次 3 次短重试易全部失败。改为外层轮询等待网络恢复（最多 20 轮 × 15s），
    # 每轮尝试一次抓取（45s 超时），命中即返回，避免整日空报告。
    MAX_ROUNDS = TRENDING_ROUNDS
    for rnd in range(1, MAX_ROUNDS + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=45) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
            if html:
                log(f"trending 抓取成功（第{rnd}/{MAX_ROUNDS}轮）")
                break
            last_err = "empty response"
        except Exception as e:  # noqa
            last_err = str(e)
            log(f"trending 抓取第{rnd}/{MAX_ROUNDS}次失败: {e}")
        if not html and rnd < MAX_ROUNDS:
            time.sleep(15)
    if not html:
        log(f"trending 抓取失败（已重试{MAX_ROUNDS}次）: {last_err}")
        if FALLBACK_ENABLED:
            log("主站 /trending 不可达 → 启用官方备用通道 api.github.com（Search API 近似榜单）")
            return fetch_trending_via_api(since)
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
            # 主站阻断导致 fetch 失败 → 直接用 codeload 归档覆盖为最新源码快照
            if FALLBACK_ENABLED:
                ok_tb, err_tb = download_tarball(p["full"], dest)
                if ok_tb:
                    p["fetch_method"] = "codeload-tarball"
                    dt = round(time.time() - t0, 1)
                    log(f"  clone OK(codeload 归档回退) {p['full']} ({dt}s)")
                    return True, str(dest), dt, ""
                err = f"{err} | tarball 回退亦失败: {err_tb}"
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
        safe_displace(dest)
    rc, out, err = run_cmd(
        ["git", "clone", "--depth", str(CLONE_DEPTH),
         f"https://github.com/{p['full']}.git", str(dest)],
        timeout=180,
    )
    dt = round(time.time() - t0, 1)
    if rc == 0:
        log(f"  clone OK {p['full']} ({dt}s)")
        return True, str(dest), dt, ""
    if FALLBACK_ENABLED:
        ok_tb, err_tb = download_tarball(p["full"], dest)
        dt = round(time.time() - t0, 1)
        if ok_tb:
            p["fetch_method"] = "codeload-tarball"
            log(f"  clone OK(codeload 归档回退) {p['full']} ({dt}s)")
            return True, str(dest), dt, ""
        err = f"{err} | tarball 回退亦失败: {err_tb}"
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
        # Windows 兼容：subprocess(shell=False) 调 CreateProcess("npm") 只补 .exe 不补 .CMD，
        # 故需用 shutil.which 解析到完整 npm.CMD 路径，否则 WinError 2。
        npm_bin = shutil.which("npm") or "npm"
        rc, out, err = run_cmd([npm_bin, "install"], cwd=path, timeout=INSTALL_TIMEOUT)
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
    fb_list = [p for p in top if p.get("source") == "search-api-fallback"]
    if fb_list:
        md.append("> ⚠️ **数据来源说明**：本期 github.com/trending 主站不可达（TLS 握手成功但无响应），"
                  "已回退至官方 api.github.com Search API，口径为"
                  "「近 1 日有推送 + star≥200，按 star 降序」，与官方 trending 的"
                  "「当日新增 star」算法不同，排名不可与历史期直接对比。\n")
    tb_list = [r for r in results if r["project"].get("fetch_method") == "codeload-tarball"]
    if tb_list:
        md.append(f"> ℹ️ **代码获取方式**：{len(tb_list)} 个项目因主站阻断改用官方 "
                  "codeload.github.com 源码归档下载（真实代码，无 .git 历史），"
                  "安装与冒烟运行均为真实执行。\n")
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
def is_transient_git_err(err: str) -> bool:
    """识别 git 瞬时网络错误（应退避重试），排除权限/配置类永久错误。"""
    e = (err or "").lower()
    keys = [
        "connection was reset", "tls unexpected eof", "recv failure",
        "could not resolve", "timed out", "10054", "10060", "10061",
        "reset by peer", "early eof", "the remote end hung up",
        "network is unreachable", "connection timed out", "connection abort",
        "broken pipe", "gnutls", "openssl", "temporary failure",
        "failed to connect", "connection refused",
    ]
    return any(k in e for k in keys)


def run_git_retry(args, cwd=None, timeout=180, max_attempts=3, op_label="git"):
    """执行 git 命令并对瞬时网络错误退避重试。返回 (rc, out, err)。"""
    last = (1, "", "")
    for attempt in range(1, max_attempts + 1):
        rc, out, err = run_cmd(args, cwd=cwd, timeout=timeout)
        if rc == 0:
            return rc, out, err
        last = (rc, out, err)
        if is_transient_git_err(err) and attempt < max_attempts:
            wait = 5 * attempt
            log(f"  ⚠️ {op_label} 瞬时错误（{attempt}/{max_attempts}），{wait}s 后重试：{err[:140]}")
            time.sleep(wait)
            continue
        return rc, out, err
    return last


def git_push_with_retry(target_branch, max_attempts=3, base_backoff=5):
    """推送目标分支到 origin，单轮内退避重试。返回 (rc, out, err)。
    - 非快进被拒：自动 rebase 拉取后继续重试（不视为失败）。
    - 瞬时网络错误：按 5/10/20...s 指数退避重试。
    - plain 失败且存在 GITHUB_TOKEN：回退 token 注入 HTTPS（Linux headless 路径）。"""
    token = os.environ.get("GITHUB_TOKEN", "")
    last_out, last_err = "", ""
    for attempt in range(1, max_attempts + 1):
        rc, out, err = run_cmd(
            ["git", "push", "-u", "origin", target_branch], cwd=ROOT, timeout=180)
        last_out, last_err = out, err
        if rc == 0:
            return 0, out, err
        # 非快进被拒 → rebase 拉取后继续（下一轮重试）
        if any(k in err for k in ("non-fast-forward", "rejected", "fetch first", "[rejected]")):
            log(f"⚠️ push 被拒（非快进），rebase 拉取后重试（{attempt}/{max_attempts}）")
            run_cmd(["git", "pull", "--rebase", "--autostash", "origin", target_branch],
                    cwd=ROOT, timeout=120)
            continue
        # 权限/认证类错误 → 优先回退 token 注入（Linux headless 路径），不浪费瞬时重试
        if token and any(k in err for k in ("denied", "403", "401", "authentication")):
            push_url = f"https://{token}@github.com/wuqijin442/ai-project-weekly.git"
            rc, out, err = run_cmd(
                ["git", "push", "-u", push_url, target_branch], cwd=ROOT, timeout=180)
            last_out, last_err = out, err
            if rc == 0:
                return 0, out, err
            if is_transient_git_err(err) and attempt < max_attempts:
                wait = min(base_backoff * (2 ** (attempt - 1)), 120)
                log(f"⚠️ token push 瞬时错误（{attempt}/{max_attempts}），{wait}s 后重试：{err[:140]}")
                time.sleep(wait)
                continue
            return rc, out, err
        # 瞬时网络错误 → 退避重试
        if is_transient_git_err(err):
            wait = min(base_backoff * (2 ** (attempt - 1)), 120)
            log(f"⚠️ push 瞬时网络错误（{attempt}/{max_attempts}），{wait}s 后重试：{err[:140]}")
            if attempt < max_attempts:
                time.sleep(wait)
            continue
        # 其他非瞬时错误 → 放弃
        return rc, out, err
    return 1, last_out, last_err


def _push_with_resilience(target_branch, max_wait=1800):
    """耐心推送：单轮 3 次退避重试仍因网络中断失败，则每 30s 轮询重试，直到成功或超时。
    覆盖 07-31 那种持续 ~28 分钟的 GitHub 连接重置窗口，避免依赖临时 recover 脚本。"""
    deadline = time.time() + max_wait
    burst = 0
    while True:
        burst += 1
        rc, out, err = git_push_with_retry(target_branch, max_attempts=3)
        if rc == 0:
            return 0, out, err
        if not is_transient_git_err(err):
            return rc, out, err  # 权限/配置类永久错误，不再等待
        if time.time() > deadline:
            return rc, out, err
        wait = 30
        log(f"⚠️ 推送因网络中断失败，{wait}s 后重试（第{burst}轮，超时上限{int(max_wait)}s）：{err[:140]}")
        time.sleep(wait)


def pre_sync_pull():
    """先拉取远端最新提交，避免多台机器（Linux 服务器 / Windows）基于旧 HEAD 推送
    导致 non-fast-forward 失败或 rebase 冲突。best-effort：失败不影响后续生成。

    关键点：本函数在报告生成之前调用，拉取后 write_report 会用本地结果覆盖
    reports/daily/YYYY-MM-DD.md，因此不会产生内容合并冲突，commit 直接基于远端
    HEAD，推送为 fast-forward。

    网络健壮性：headless 服务器到 GitHub 的 TLS 连接偶发中断（GnuTLS recv error），
    故对 pull 做最多 3 次重试 + 退避，避免瞬时抖动导致跳过 pre-pull 后推送失败。"""
    target_branch = os.environ.get("GITHUB_TARGET_BRANCH", "main")
    last_err = ""
    for attempt in range(1, 4):
        try:
            rc, out, err = run_cmd(
                ["git", "pull", "--rebase", "--autostash", "origin", target_branch],
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
    # DGX_LEARN_ONLY：dgx 端只本地生成数据供 learn_link 使用，不提交/推送每日数据，
    # 避免与 Windows 端（每日数据独家推送）在同一批文件上产生 rebase 冲突。
    if os.environ.get("DGX_LEARN_ONLY"):
        log("⏭️ DGX_LEARN_ONLY：跳过每日数据提交/推送（仅本地生成供学习使用），数据由 Windows 端推送")
        return True, "skip"
    # 分支感知：默认推 main；多机分支模型（win/dgx）由 GITHUB_TARGET_BRANCH 指定。
    target_branch = os.environ.get("GITHUB_TARGET_BRANCH", "main")
    try:
        rc, _, _ = run_cmd(["git", "checkout", target_branch], cwd=ROOT, timeout=30)
        if rc != 0:
            run_cmd(["git", "fetch", "origin", target_branch], cwd=ROOT, timeout=60)
            run_cmd(["git", "checkout", "-b", target_branch, f"origin/{target_branch}"],
                    cwd=ROOT, timeout=30)
    except Exception:  # noqa
        pass
    try:
        run_cmd(["git", "add", "-A"], cwd=ROOT, timeout=60)
        # 只在有变更时提交；避免空提交失败
        rc, _, _ = run_cmd(["git", "diff", "--cached", "--quiet"], cwd=ROOT, timeout=30)
        if rc != 0:
            msg = f"[{date.isoformat()}] Daily AI Project Update"
            run_cmd(["git", "commit", "-m", msg], cwd=ROOT, timeout=60)
        # 统一分支名为目标分支（git init 默认可能为 master；多机分支模型下为 win/dgx）
        run_cmd(["git", "branch", "-M", target_branch], cwd=ROOT, timeout=30)
        # 推送策略（跨平台健壮）：
        #   1) 优先用 origin 远程 + 凭据管理器（Windows 已缓存可写凭据 / Linux 若已配置）。
        #   2) 仅当 plain push 失败且存在 GITHUB_TOKEN 时，才回退到 token 注入的 HTTPS URL
        #      （headless Linux 服务器常见路径；token 不写入 .git/config，仅本次命令内联）。
        #   注意：Windows 环境变量里的 GITHUB_TOKEN 为只读，不可用于推送，故不作为首选，
        #        否则会被 git 403 denied（remote: Permission denied to wuqijin442）。
        # 耐心推送：内置退避重试 + 瞬时网络错误识别 + 非快进自动 rebase，
        # 覆盖 18:1x–19:0x 窗口 GitHub 连接重置（07-30/07-31 实测），最长等待 30 分钟。
        rc, out, err = _push_with_resilience(target_branch)
        if rc == 0:
            log(f"✅ 已推送到 wuqijin442/{target_branch}")
            return True, out
        # 抹掉日志里的 token（git 报错会带含 token 的 URL）
        safe_err = err.replace(GITHUB_TOKEN, "***TOKEN***") if GITHUB_TOKEN else err
        log(f"⚠️ push 失败（检查网络/凭据）：{safe_err[:300]}")
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

    # 网络韧性：若 trending 全程抓取失败（扫描 0），无真实数据可落地，
    # 跳过提交/推送，避免空报告污染 win 历史（如实标注未运行）。
    if scanned == 0:
        log("⚠️ 未抓取到任何 trending 数据（网络中断），跳过提交/推送，避免空报告污染历史")
        log(f"=== 完成 | 扫描 {scanned} / 过滤 {filtered} / TOP{n} / 推荐 0 / 推送 SKIPPED ===")
        return report

    pushed, perr = sync_to_github(date)
    log(f"=== 完成 | 扫描 {scanned} / 过滤 {filtered} / TOP{n} / 推荐 "
        f"{sum(1 for r in results if r['score']>=90)} / 推送 {'OK' if pushed else 'FAIL'} ===")
    return report


if __name__ == "__main__":
    main()
