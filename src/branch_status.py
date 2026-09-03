#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程仓库各分支状态核对与总结（轻量，无真实克隆）

与 main.py / board_workflow.py 同源：所有结论基于真实 git 元数据，不做推测。

用途：
- 多机分支模型下，main 由每日 20:00 归集任务（src/merge_branches.sh 经 PR）合并 win 与 dgx；
  Windows 本机自动化 17:30 运行时，win/dgx 通常领先 main（待归集）。本脚本用于每日核对
  "各分支领先/落后 main 多少提交、最近提交了什么、哪些待归集"。
- 仅做 git 元数据层面的核对（fetch + 比对 + 最近提交），不克隆任何项目，耗时极短，
  适合作为每日自动化的追加步骤（步骤3）。

产出：
- reports/branches/YYYY-MM-DD-branch-status.md（中文总结）
- data/metadata/YYYY-MM-DD-branch-status.json
- 通过 GITHUB_TARGET_BRANCH 推送到 win 分支（默认 win；多机分支模型下与每日数据同属 Windows 端产物）。
"""
import os
import sys
import json
import re
import datetime
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# 复用 main.py 的真实运行/同步函数（main.py 有 __main__ 守卫，import 不触发其主流程）
sys.path.insert(0, str(Path(__file__).resolve().parent))
from main import log, run_cmd, pre_sync_pull, sync_to_github, run_git_retry  # noqa

ROOT = Path(__file__).resolve().parent.parent          # src/branch_status.py -> 仓库根
BRANCH_DIR = ROOT / "reports" / "branches"
BRANCH_DIR.mkdir(parents=True, exist_ok=True)
META_DIR = ROOT / "data" / "metadata"
META_DIR.mkdir(exist_ok=True)


def fetch_all():
    """拉取所有远端分支引用（--prune 清理已删除远端分支的本地跟踪引用）。
    fetch 走 run_git_retry：18:1x–19:0x 窗口 GitHub 连接重置时自动退避重试。
    返回 True 表示取得可信远端引用；False 表示主站被 IP 阻断，须改走 api.github.com 复核。"""
    rc, _, err = run_git_retry(
        ["git", "fetch", "origin", "--prune"], cwd=ROOT, timeout=120,
        max_attempts=4, op_label="fetch --prune")
    if rc != 0:
        log(f"⚠️ git fetch --prune 失败：{err[:200]}（主站疑似 IP 层阻断）")
        return False
    log("✅ 已 fetch --prune 更新全部远端分支引用")
    return True


def _api_get(url, token=None):
    """访问 api.github.com，返回 dict；失败抛异常。"""
    headers = {"User-Agent": "branch-status-script",
               "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_repo_slug():
    """从 origin remote URL 解析 owner/repo。"""
    rc, out, _ = run_cmd(["git", "remote", "get-url", "origin"], cwd=ROOT, timeout=20)
    if rc == 0:
        m = re.search(r"github\.com[:/]([^/]+)/(.+?)(?:\.git)?$", out.strip())
        if m:
            return f"{m.group(1)}/{m.group(2)}"
    return None


def api_branch_rows(repo_slug, base="main"):
    """回退路径：主站被 IP 阻断、git fetch 失败时，经 api.github.com 取可信分支元数据。
    返回 rows 列表（结构与 git 路径一致），失败返回 None。"""
    try:
        branches = _api_get(
            f"https://api.github.com/repos/{repo_slug}/branches?per_page=100")
    except Exception as e:  # noqa
        log(f"⚠️ api.github.com /branches 请求失败：{e}")
        return None
    rows = []
    for b in branches:
        name = b["name"]
        head_sha = b["commit"]["sha"]
        last = None
        try:
            c = _api_get(f"https://api.github.com/repos/{repo_slug}/commits/{head_sha}")
            cm = c.get("commit", {})
            last = {
                "hash": head_sha[:10],
                "author": cm.get("author", {}).get("name", "")
                          or c.get("author", {}).get("login", ""),
                "date": (cm.get("author", {}).get("date") or "")[:10],
                "subject": cm.get("message", "").split("\n")[0][:80],
            }
        except Exception:  # noqa
            last = {"hash": head_sha[:10], "author": "", "date": "", "subject": ""}
        if name == base:
            rows.append({"branch": name, "last": last, "behind_main": 0,
                         "ahead_main": 0, "unique_commits": []})
            continue
        try:
            cmp = _api_get(
                f"https://api.github.com/repos/{repo_slug}/compare/{base}...{name}")
            ahead = cmp.get("ahead_by", 0)
            behind = cmp.get("behind_by", 0)
        except Exception:  # noqa
            ahead, behind = 0, 0
        uniq = []
        for c in cmp.get("commits", [])[:10]:
            cm = c.get("commit", {})
            uniq.append(
                f"{c.get('sha', '')[:10]} {(cm.get('author', {}).get('date') or '')[:10]} "
                f"{cm.get('author', {}).get('name', '')} {cm.get('message', '').split(chr(10))[0][:60]}")
        rows.append({"branch": name, "last": last, "behind_main": behind,
                     "ahead_main": ahead, "unique_commits": uniq})
    return rows


def list_remote_branches():
    rc, out, _ = run_cmd(["git", "branch", "-r"], cwd=ROOT, timeout=30)
    branches = []
    for line in out.splitlines():
        b = line.strip()
        if not b:
            continue
        # 跳过符号引用行（形如 origin/HEAD -> origin/main）
        if " -> " in b:
            continue
        if b.startswith("origin/"):
            name = b[len("origin/"):]
            if name and name != "HEAD":
                branches.append(name)
    return branches


def branch_last_commit(branch):
    rc, out, _ = run_cmd(
        ["git", "log", "-1", "--format=%H|%an|%ad|%s", f"origin/{branch}"],
        cwd=ROOT, timeout=30)
    if rc != 0 or not out.strip():
        return None
    parts = (out.strip().split("|", 3) + ["", "", "", ""])[:4]
    return {"hash": parts[0][:10], "author": parts[1], "date": parts[2], "subject": parts[3]}


def ahead_behind(branch, base="main"):
    # 左 = base 独有（branch 落后数），右 = branch 独有（branch 领先数）
    rc, out, _ = run_cmd(
        ["git", "rev-list", "--left-right", "--count",
         f"origin/{base}...origin/{branch}"],
        cwd=ROOT, timeout=30)
    if rc != 0 or not out.strip():
        return (0, 0)
    left, right = out.strip().split()
    return (int(left), int(right))  # (behind, ahead)


def unique_commits(branch, base="main", limit=10):
    rc, out, _ = run_cmd(
        ["git", "log", "--format=%h %ad %an %s", "--date=short",
         f"origin/{base}..origin/{branch}"],
        cwd=ROOT, timeout=30)
    if rc != 0:
        return []
    return [l for l in out.splitlines() if l.strip()][:limit]


def main():
    parser = argparse.ArgumentParser(description="远程仓库各分支状态核对")
    parser.add_argument("--date", default=None,
                        help="目标日期 YYYY-MM-DD（缺省=今天），用于回填历史分支状态报告")
    args = parser.parse_args()
    if args.date:
        try:
            date = datetime.date.fromisoformat(args.date)
        except ValueError:
            log(f"⚠️ --date 格式错误：{args.date}，回退为今天")
            date = datetime.date.today()
    else:
        date = datetime.date.today()
    log(f"=== 远程仓库各分支状态核对 {date.isoformat()} ===")
    # 先拉远端最新，保证本地 win 与远端一致，且 main 引用为最新
    pre_sync_pull()
    fetch_ok = fetch_all()

    rows = None
    data_source = "本地 git fetch"
    force_api = os.environ.get("GH_BRANCH_API") == "1"
    if force_api:
        log("🔧 GH_BRANCH_API=1：强制走 api.github.com 权威接口核算（忽略本地 fetch）")
        fetch_ok = False
    if not fetch_ok:
        # 主站被 IP 阻断 → 改走 api.github.com 取可信数据（working-memory 约定）
        slug = get_repo_slug()
        if slug:
            log(f"🔄 主站不可达，改走 api.github.com 复核分支元数据（repo={slug}）")
            rows = api_branch_rows(slug, base="main")
            if rows is not None:
                data_source = f"api.github.com（github.com 主站 IP 阻断，本地引用不可信）"
                branches = [r["branch"] for r in rows]
                base = "main" if any(r["branch"] == "main" for r in rows) else branches[0]
                log(f"基准分支：{base}；检测到分支：{', '.join(branches)}（数据源：{data_source}）")
    if rows is None:
        branches = list_remote_branches()
        base = "main"
        if base not in branches:
            base = branches[0] if branches else "main"
        log(f"基准分支：{base}；检测到分支：{', '.join(branches)}")
        rows = []
        for b in branches:
            last = branch_last_commit(b)
            if b == base:
                behind, ahead = 0, 0
                uniq = []
            else:
                behind, ahead = ahead_behind(b, base)
                uniq = unique_commits(b, base) if ahead > 0 else []
            rows.append({
                "branch": b, "last": last, "behind_main": behind,
                "ahead_main": ahead, "unique_commits": uniq,
            })

    # ---- 生成报告 ----
    md = []
    md.append(f"# 远程仓库分支状态核对 — {date.isoformat()}\n")
    md.append("> 自动 `git fetch --prune` 后比对各分支相对 `main` 的领先/落后提交与最近提交，"
              "结论基于真实 git 元数据，无推测。\n")
    md.append(f"**基准分支**：`{base}`　**分支总数**：{len(branches)}　"
              f"**核对时间**：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md.append(f"**数据来源**：{data_source}\n")

    md.append("\n## 各分支总览\n")
    md.append("| 分支 | 领先 main | 落后 main | 最近提交 | 作者 | 日期 |")
    md.append("|---|---|---|---|---|---|")
    for r in rows:
        last = r["last"] or {}
        md.append(
            f"| `{r['branch']}` | {r['ahead_main']} | {r['behind_main']} | "
            f"{last.get('subject', '')[:40]} | {last.get('author', '')} | {last.get('date', '')} |")

    md.append("\n## 领先 main 的待归集提交\n")
    any_ahead = False
    for r in rows:
        if r["branch"] != base and r["ahead_main"] > 0:
            any_ahead = True
            md.append(f"\n### `{r['branch']}`（领先 main {r['ahead_main']} 个提交，待 20:00 归集）\n")
            if r["unique_commits"]:
                for c in r["unique_commits"]:
                    md.append(f"- {c}")
                if r["ahead_main"] > len(r["unique_commits"]):
                    md.append(f"- …（其余 {r['ahead_main'] - len(r['unique_commits'])} 条未列出）")
            else:
                md.append("- （无明细）")
    if not any_ahead:
        md.append("\n- 所有分支均已归集进 `main`，无待合并提交。\n")

    md.append("\n---\n")
    md.append("### 说明\n")
    md.append("- 本核对仅读取 git 元数据，不克隆任何项目，耗时极短。")
    if data_source.startswith("api.github.com"):
        md.append("- ⚠️ **数据来源说明**：本次 `git fetch --prune` 因 github.com 主站 IP 层阻断失败，"
                  "本地 `origin/*` 引用不可信，故领先/落后数字改由 **api.github.com** 的 `/branches` 与 `/compare` "
                  "接口实时核算（服务端权威引用），结论可靠。待主站恢复后下轮将自动回到本地 fetch 路径。")
    md.append("- 当前多机分支模型：`win`=Windows 端每日数据、`dgx`=dgx 端学习消化产物，"
              "二者由每日 20:00 归集任务（src/merge_branches.sh）经 GitHub PR 合并进 `main`。")
    md.append("- Windows 自动化 17:30 运行时，`win`/`dgx` 通常领先 `main`，属**正常的待归集状态**；"
              "若某分支长期大幅领先 main 未归集，需排查 20:00 归集任务是否异常。")
    report = "\n".join(md)

    out = BRANCH_DIR / f"{date.isoformat()}-branch-status.md"
    out.write_text(report, encoding="utf-8")
    log(f"分支状态报告已生成：{out}")
    (META_DIR / f"{date.isoformat()}-branch-status.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    pushed, perr = sync_to_github(date)
    log(f"=== 完成 | 分支 {len(branches)} / 推送 {'OK' if pushed else 'FAIL'} ===")
    return report


if __name__ == "__main__":
    main()
