#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 开源项目 11 板块测试工作流（真实运行版）

与 main.py 同源：所有结论基于真实运行结果，不根据 README 推测，失败记日志继续。

概念：
- "板块" = 11 个 AI 相关的 GitHub topic（大语言模型 / Agent / RAG / 扩散模型 / 视觉 /
  语音 / 机器人 / MLOps / 向量库 / 提示工程 / 微调）。
- 每个板块通过 GitHub Search API（topic 检索 + 按 star 降序，无需 token，受 10 次/分钟限速，
  板间自动留间隔并带 403 退避重试）抓取真实仓库，取 TOP5，逐一真实 Clone -> 检测构建 ->
  真实安装 -> 真实冒烟。
- 汇总到 reports/boards/YYYY-MM-DD-boards.md 与 data/metadata/YYYY-MM-DD-boards.json。

说明：
- 11×5=55 个项目，整体耗时较长；脚本对单个项目失败不中断，且克隆落在 clones/boards/
  （已 gitignore）。建议由自动化或手动触发，无需每日强跑。
- 复用 main.py 的纯函数，保持真实运行逻辑完全一致。

运行：python src/board_workflow.py [--date YYYY-MM-DD]
"""
import os
import re
import sys
import json
import argparse
import time
import shutil
import datetime
import urllib.request
import urllib.error
from pathlib import Path

# 复用 main.py 的真实运行函数（main.py 有 __main__ 守卫，import 不会触发其主流程）
sys.path.insert(0, str(Path(__file__).resolve().parent))
import main as _main  # noqa
from main import (  # noqa
    log, run_cmd, clean_text, detect_build, install_project,
    smoke_run, score_project, sync_to_github, pre_sync_pull, EXCLUDE_KEYWORDS,
    is_transient_git_err, run_git_retry,
)

# 板块运行使用更短的超时，避免 55 个项目时整体过长
BOARD_INSTALL_TIMEOUT = int(os.environ.get("BOARD_INSTALL_TIMEOUT", "120"))
BOARD_RUN_TIMEOUT = int(os.environ.get("BOARD_RUN_TIMEOUT", "40"))
BOARD_API_PACE = int(os.environ.get("BOARD_API_PACE", "7"))  # 板间间隔，规避 10 次/分钟限速
BOARD_MIN_STARS = int(os.environ.get("BOARD_MIN_STARS", "50"))
_main.INSTALL_TIMEOUT = BOARD_INSTALL_TIMEOUT
_main.RUN_TIMEOUT = BOARD_RUN_TIMEOUT

ROOT = Path(__file__).resolve().parent.parent          # src/board_workflow.py -> 仓库根
BOARDS_DIR = ROOT / "reports" / "boards"
BOARDS_DIR.mkdir(exist_ok=True)
META_DIR = ROOT / "data" / "metadata"
META_DIR.mkdir(exist_ok=True)
CLONES_BOARD_DIR = ROOT / "clones" / "boards"
CLONES_BOARD_DIR.mkdir(parents=True, exist_ok=True)
CLONE_DEPTH = int(os.environ.get("CLONE_DEPTH", "1"))

# 11 个板块：(GitHub topic slug, 中文标签)
BOARDS = [
    ("large-language-models", "大语言模型"),
    ("artificial-intelligence", "人工智能"),
    ("rag", "检索增强生成 RAG"),
    ("stable-diffusion", "扩散模型"),
    ("computer-vision", "计算机视觉"),
    ("speech-recognition", "语音识别"),
    ("robotics", "机器人"),
    ("mlops", "MLOps"),
    ("vector-database", "向量数据库"),
    ("prompt-engineering", "提示工程"),
    ("fine-tuning", "微调"),
]


# ----------------------------------------------------------------------------
# 抓取单个板块（GitHub topic 页，按 star 降序）
# ----------------------------------------------------------------------------
def fetch_board(slug):
    """通过 GitHub Search API 真实检索某 topic 下的仓库（按 star 降序），无需 token。"""
    url = (f"https://api.github.com/search/repositories"
           f"?q=topic:{slug}+stars:%3E{BOARD_MIN_STARS}"
           f"&sort=stars&order=desc&per_page=10")
    last_err = ""
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/vnd.github+json",
            })
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            items = data.get("items", [])
            projects = []
            for it in items:
                full = it.get("full_name", "")
                if full.count("/") != 1:
                    continue
                owner, name = full.split("/")
                projects.append({
                    "owner": owner, "name": name, "full": full,
                    "url": it.get("html_url", f"https://github.com/{full}"),
                    "description": clean_text(it.get("description") or ""),
                    "language": it.get("language") or "Unknown",
                    "stars": int(it.get("stargazers_count", 0) or 0),
                    "topic": slug,
                })
            log(f"  [{slug}] 抓取 {len(projects)} 个仓库（min★{BOARD_MIN_STARS}）")
            return projects
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.code == 403:
                # 速率限制：按 GitHub 返回的 X-RateLimit-Reset 精确等待
                reset = e.headers.get("X-RateLimit-Reset")
                if reset:
                    wait = max(5, int(float(reset)) - int(time.time()) + 2)
                else:
                    wait = 20
                log(f"  [{slug}] 速率限制(403)，{wait}s 后重试({attempt}/3)...")
                time.sleep(wait)
                continue
            log(f"  [{slug}] HTTP 错误 {e.code}: {e}")
            break
        except Exception as e:  # noqa
            last_err = str(e)
            log(f"  [{slug}] 抓取第{attempt}次失败: {e}")
            time.sleep(5)
    log(f"  [{slug}] 抓取失败（已重试）: {last_err}")
    return []


# ----------------------------------------------------------------------------
# 板块内过滤 + 选 TOP5（按 star 降序，排除 awesome/tutorial/demo/fork）
# ----------------------------------------------------------------------------
def select_top5(projects):
    def ok(p):
        nm = p["name"].lower()
        return not any(k in nm for k in EXCLUDE_KEYWORDS)
    filtered = [p for p in projects if ok(p)]
    top = sorted(filtered, key=lambda p: p["stars"], reverse=True)[:5]
    return top


def clone_board_repo(p):
    safe = f"{p['owner']}__{p['name']}"
    dest = CLONES_BOARD_DIR / safe
    t0 = time.time()
    if dest.exists() and (dest / ".git").exists():
        # 已存在 git 仓库 → 原地更新（fetch + reset），避免 rmtree 触发工作区安全删除拦截
        # fetch 走 run_git_retry：18:1x–19:0x 窗口 GitHub 连接重置时自动退避重试，避免整板 0/5
        rc, _, err = run_git_retry(
            ["git", "-C", str(dest), "fetch", "--depth", str(CLONE_DEPTH), "origin"],
            timeout=180, max_attempts=3, op_label=f"fetch {p['full']}")
        if rc != 0:
            # 主站阻断导致 fetch 失败 → 直接用 codeload 归档覆盖为最新源码快照
            if _main.FALLBACK_ENABLED:
                ok_tb, err_tb = _main.download_tarball(p["full"], dest)
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
        # 非 git 残留（极少见）→ 挪走后重新克隆（不用 rmtree，避免批量删除保护中断进程）
        _main.safe_displace(dest)
    # 克隆对瞬时网络错误退避重试（最多 3 次）；重试前挪走半截克隆，避免 "destination exists"
    ok, err = False, ""
    for attempt in range(1, 4):
        rc, _, err = run_cmd(
            ["git", "clone", "--depth", str(CLONE_DEPTH),
             f"https://github.com/{p['full']}.git", str(dest)],
            timeout=180,
        )
        if rc == 0:
            ok = True
            break
        if is_transient_git_err(err) and attempt < 3:
            wait = 5 * attempt
            log(f"  clone 瞬时错误（{attempt}/3），{wait}s 后重试：{err[:140]}")
            if dest.exists():
                _main.safe_displace(dest)
            time.sleep(wait)
            continue
        break
    dt = round(time.time() - t0, 1)
    if ok:
        log(f"  clone OK {p['full']} ({dt}s)")
        return True, str(dest), dt, ""
    # 主站阻断时的官方备用通道：codeload.github.com 下载源码归档（真实代码，可真实安装/冒烟）
    if _main.FALLBACK_ENABLED:
        ok_tb, err_tb = _main.download_tarball(p["full"], dest)
        dt = round(time.time() - t0, 1)
        if ok_tb:
            p["fetch_method"] = "codeload-tarball"
            log(f"  clone OK(codeload 归档回退) {p['full']} ({dt}s)")
            return True, str(dest), dt, ""
        err = f"{err} | tarball 回退亦失败: {err_tb}"
    log(f"  clone FAIL {p['full']}: {err[:200]}")
    return False, str(dest), dt, err


# ----------------------------------------------------------------------------
# 生成板块报告
# ----------------------------------------------------------------------------
def write_board_report(date, all_results, totals):
    md = []
    md.append(f"# AI 开源项目 11 板块测试报告 — {date.isoformat()}\n")
    md.append("> 本报告所有结论基于真实 Clone/安装/运行结果，未根据 README 推测。\n")
    md.append(f"**板块数**：{totals['boards']}  **扫描仓库**：{totals['scanned']}  "
              f"**测试项目**：{totals['tested']}  **Clone 成功**：{totals['clone_ok']}  "
              f"**安装成功**：{totals['install_ok']}  **运行成功(冒烟)**：{totals['run_ok']}  "
              f"**推荐(≥90分)**：{totals['recommended']}\n")

    for slug, info in all_results.items():
        label = info["label"]
        md.append(f"\n## 板块：{label}（`{slug}`）\n")
        if not info["results"]:
            md.append("- （本板块未取到可测试项目）\n")
            continue
        for i, r in enumerate(info["results"], 1):
            p = r["project"]
            md.append(f"### {i}. {p['full']}")
            md.append(f"- **地址**：{p['url']}")
            md.append(f"- **语言**：{p['language']}  **Star**：{p['stars']}")
            md.append(f"- **简介**：{p['description'] or '（无描述）'}")
            md.append(f"- **Clone**：{'✅ ' + str(r['clone_time']) + 's' if r['clone'] else '❌ ' + r['clone_err'][:120]}")
            md.append(f"- **构建系统**：{', '.join(r['build']['files']) or '未识别'}")
            md.append(f"- **安装**：{r['install']}（{r['install_time']}s）")
            md.append(f"- **冒烟运行**：{r['run']}（{r['run_time']}s）")
            md.append(f"- **AI 评分**：{r['score']}/100  {r['stars']}")
            md.append(f"- **推荐**：{'✅ 进入知识库' if r['score'] >= 90 and r['install'] == 'success' else '— 未达门槛'}")
            md.append("")

    md.append("\n---\n")
    md.append("### 各板块测试概览（基于真实落地）\n")
    for slug, info in all_results.items():
        res = info["results"]
        ok_clone = sum(1 for r in res if r["clone"])
        ok_install = sum(1 for r in res if r["install"] == "success")
        ok_run = sum(1 for r in res if r["run"] == "success")
        md.append(f"- **{info['label']}**：测试 {len(res)} / clone {ok_clone} / 安装 {ok_install} / 运行 {ok_run}")
    report = "\n".join(md)

    out = BOARDS_DIR / f"{date.isoformat()}-boards.md"
    out.write_text(report, encoding="utf-8")
    log(f"板块报告已生成：{out}")
    return out


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
def main():
    # 支持 --date YYYY-MM-DD 回填历史日期（如补跑昨日板块报告）；缺省为今天
    parser = argparse.ArgumentParser(description="AI 开源项目 11 板块测试工作流")
    parser.add_argument("--date", default=None,
                        help="目标日期 YYYY-MM-DD（缺省=今天），用于回填历史板块报告")
    args, _ = parser.parse_known_args()
    if args.date:
        try:
            date = datetime.date.fromisoformat(args.date)
        except ValueError:
            log(f"⚠️ --date 格式错误：{args.date}，回退为今天")
            date = datetime.date.today()
    else:
        date = datetime.date.today()
    log(f"=== AI 项目 11 板块测试工作流启动 {date.isoformat()} ===")
    # 先拉远端最新（多机/多自动化共用 win 分支，避免长耗时运行期间
    # 远端被其他自动化推进导致最终 push 非快进失败）
    pre_sync_pull()
    if not BOARDS:
        log("未配置任何板块，退出。")
        return None

    all_results = {}
    totals = {"boards": 0, "scanned": 0, "tested": 0, "clone_ok": 0,
              "install_ok": 0, "run_ok": 0, "recommended": 0}

    # 断点续跑：单板块耗时数分钟，11 板块全跑 30~90 分钟。若中途因网络/环境异常
    # 崩溃，重跑时从检查点恢复已完成板块，避免重复劳动（真实结果照常沿用，
    # 不是编造——检查点里存的就是本次运行真实 clone/安装/冒烟的结果）。
    ckpt = META_DIR / f".{date.isoformat()}-boards-partial.json"
    if ckpt.exists():
        try:
            saved = json.loads(ckpt.read_text(encoding="utf-8"))
            all_results = saved.get("all_results", {}) or {}
            totals = saved.get("totals", totals) or totals
            if all_results:
                log(f"检测到检查点，恢复已完成板块 {len(all_results)} 个："
                    f"{', '.join(all_results.keys())}")
        except Exception as e:  # noqa
            log(f"⚠️ 检查点读取失败，从头开始：{str(e)[:120]}")
            all_results, totals = {}, {"boards": 0, "scanned": 0, "tested": 0,
                                       "clone_ok": 0, "install_ok": 0,
                                       "run_ok": 0, "recommended": 0}

    def save_ckpt():
        try:
            ckpt.write_text(json.dumps({"all_results": all_results, "totals": totals},
                                       ensure_ascii=False), encoding="utf-8")
        except Exception as e:  # noqa
            log(f"⚠️ 检查点写入失败：{str(e)[:120]}")

    for idx, (slug, label) in enumerate(BOARDS):
        if slug in all_results:
            log(f"--- 板块：{label} ({slug}) 已在检查点中，跳过 ---")
            continue
        log(f"--- 板块：{label} ({slug}) ---")
        projects = fetch_board(slug)
        # 板间留间隔，规避未认证 Search API 的 10 次/分钟限速（最后一板无需等待）
        if idx < len(BOARDS) - 1:
            time.sleep(BOARD_API_PACE)
        totals["boards"] += 1
        totals["scanned"] += len(projects)
        top = select_top5(projects)
        results = []
        for p in top:
            totals["tested"] += 1
            log(f"  处理 {p['full']} (★{p['stars']})")
            ok, path, ct, cerr = clone_board_repo(p)
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
            totals["clone_ok"] += 1 if ok else 0
            totals["install_ok"] += 1 if istatus == "success" else 0
            totals["run_ok"] += 1 if rstatus == "success" else 0
            totals["recommended"] += 1 if (score >= 90 and istatus == "success") else 0
        all_results[slug] = {"label": label, "top": top, "results": results}
        save_ckpt()

    report = write_board_report(date, all_results, totals)
    (META_DIR / f"{date.isoformat()}-boards.json").write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")

    pushed, perr = sync_to_github(date)
    log(f"=== 完成 | 板块 {totals['boards']} / 扫描 {totals['scanned']} / 测试 {totals['tested']} "
        f"/ clone {totals['clone_ok']} / 安装 {totals['install_ok']} / 运行 {totals['run_ok']} "
        f"/ 推荐 {totals['recommended']} / 推送 {'OK' if pushed else 'FAIL'} ===")
    return report


if __name__ == "__main__":
    main()
