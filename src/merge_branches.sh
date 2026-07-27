#!/usr/bin/env bash
# ============================================================================
# merge_branches.sh — 每日 20:00 分支归集：把 win / dgx 两条机器分支合并进 main
#
# 设计（多机分支模型）：
#   - dgx 分支：dgx 端 learn_link 产物（reports/learnings/、knowledge-base/learn_links/）
#   - win 分支 ：Windows 端每日数据 + 板块 + Obsidian（data/metadata/、reports/daily/、
#                reports/boards/、Obsidian_Vault/）
#   两分支文件集合天然不相交，合并通常无冲突；本脚本仍内置按「归属」的冲突兜底，
#   确保即使某日两机都碰了同一文件也能确定性收敛（知识图谱归 dgx，每日数据/Obsidian 归 win）。
#
# 关键健壮性：
#   0) 清残留 rebase/merge；fetch 带重试（容忍 GitHub 凌晨/傍晚抖动）。
#   1) 先切到 main 并同步远端最新，再依次合并 dgx、win。
#   2) 冲突解决按归属：learn_links/learnings -> dgx；data/reports/boards/Obsidian -> win。
#   3) 推送 main 带重试，且**用正确退出码判定成功**（绝不管道 tail 掩盖 non-fast-forward）。
#
# 用法（crontab）：
#   0 20 * * * cd ~/ai-project-weekly && GITHUB_TARGET_BRANCH=main bash src/merge_branches.sh
# 依赖：仓库根 .env 提供 GITHUB_TOKEN（headless 服务器 HTTPS 推送鉴权）。
# ============================================================================
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT" || exit 1

if [ -f "$REPO_ROOT/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$REPO_ROOT/.env"
  set +a
fi

BR_DGX="${MERGE_DGX_BRANCH:-dgx}"
BR_WIN="${MERGE_WIN_BRANCH:-win}"
BR_MAIN="${MERGE_MAIN_BRANCH:-main}"

LOG_DIR="$REPO_ROOT/Logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/merge-branches-$(date +%Y-%m-%d).log"
echo "=== $(date '+%F %T') merge_branches 启动（dgx=$BR_DGX win=$BR_WIN main=$BR_MAIN）===" | tee -a "$LOG"

# 0) 清残留 rebase / merge 状态
git rebase --abort >/dev/null 2>&1
git merge --abort >/dev/null 2>&1

# 1) fetch 所有远端分支（带重试）
FETCHED=0
for i in 1 2 3 4 5 6; do
  if git fetch origin >>"$LOG" 2>&1; then FETCHED=1; break; fi
  echo "fetch 第 $i/6 次失败，退避 $((i * 5))s" | tee -a "$LOG"
  sleep $((i * 5))
done
if [ "$FETCHED" -ne 1 ]; then
  echo "fetch 持续失败，本次放弃（明日再试）" | tee -a "$LOG"
  exit 0
fi

# 2) 切到 main 并同步远端最新
git checkout "$BR_MAIN" >>"$LOG" 2>&1
git rebase --abort >/dev/null 2>&1
git pull --rebase --autostash origin "$BR_MAIN" >>"$LOG" 2>&1

# 3) 合并单条机器分支（带按归属的冲突兜底）
merge_one () {
  local br="$1"; local owner="$2"   # owner: dgx=知识图谱, win=每日数据/Obsidian
  echo ">>> 合并 $br -> $BR_MAIN" | tee -a "$LOG"
  if git merge "origin/$br" --no-edit -m "merge: $br -> $BR_MAIN $(date +%F)" >>"$LOG" 2>&1; then
    echo "<<< $br 合并完成（无冲突）" | tee -a "$LOG"
    return 0
  fi
  # 冲突：按归属解决
  echo "⚠️ $br 合并冲突，按归属解决（知识图谱=dgx，每日数据/Obsidian=win）" | tee -a "$LOG"
  for f in $(git diff --name-only --diff-filter=U); do
    case "$f" in
      knowledge-base/learn_links/*|reports/learnings/*)
        # 知识图谱类：以 dgx 为准
        if [ "$owner" = "dgx" ]; then git checkout --theirs "$f"; else git checkout --ours "$f"; fi ;;
      data/metadata/*|reports/daily/*|reports/boards/*|Obsidian_Vault/*)
        # 每日数据 / Obsidian：以 win 为准
        if [ "$owner" = "win" ]; then git checkout --theirs "$f"; else git checkout --ours "$f"; fi ;;
      *) git checkout --ours "$f" ;;
    esac
    git add "$f"
  done
  if git merge --continue --no-edit >>"$LOG" 2>&1; then
    echo "<<< $br 冲突已解决并继续" | tee -a "$LOG"
  else
    git commit --no-edit >>"$LOG" 2>&1 || true
    echo "<<< $br 冲突已解决（commit）" | tee -a "$LOG"
  fi
}
merge_one "$BR_DGX" dgx
merge_one "$BR_WIN" win

# 4) 推送 main（带重试，正确退出码）
if [ -n "${GITHUB_TOKEN:-}" ]; then
  PUSH_URL="https://${GITHUB_TOKEN}@github.com/wuqijin442/ai-project-weekly.git"
else
  PUSH_URL="origin"
fi
PUSHED=0
for i in 1 2 3 4 5 6 7 8; do
  if git push -u "$PUSH_URL" "$BR_MAIN" >>"$LOG" 2>&1; then
    PUSHED=1
    echo "PUSH_OK=$i" | tee -a "$LOG"
    break
  fi
  echo "push 第 $i/8 次失败，退避 $((i * 5))s" | tee -a "$LOG"
  sleep $((i * 5))
done

if [ "$PUSHED" -eq 1 ]; then
  echo "<<< 归集完成（main HEAD=$(git rev-parse --short HEAD)）" | tee -a "$LOG"
else
  echo "<<< main 推送失败（明日再试）" | tee -a "$LOG"
fi
exit 0
