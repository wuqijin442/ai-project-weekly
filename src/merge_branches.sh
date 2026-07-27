#!/usr/bin/env bash
# ============================================================================
# merge_branches.sh — 每日 20:00 分支归集：把 win / dgx 两条机器分支归并进 main
#
# 设计（多机分支模型）：
#   - dgx 分支：dgx 端 learn_link 产物（reports/learnings/、knowledge-base/learn_links/）
#   - win 分支 ：Windows 端每日数据 + 板块 + Obsidian（data/metadata/、reports/daily/、
#                reports/boards/、Obsidian_Vault/）
#   两分支文件集合天然不相交，合并通常无冲突；仍内置按「归属」的冲突兜底。
#
# 归集方式（优先 PR，失败回退本地 merge）：
#   - 优先用 GitHub REST API（curl + GITHUB_TOKEN）为每条机器分支创建 PR 并合并进
#     main，获得真正的 GitHub PR（带评审界面 / 合并记录）。
#   - 若 API 不可用（网络抖动 / token 缺 PR 写权限 / 工具缺失），自动回退到本地
#     `git merge` + push main，保证每日归集不中断。
#
# 关键健壮性：
#   0) 清残留 rebase/merge；fetch 带重试（容忍 GitHub 抖动）。
#   1) 先切到 main 并同步远端最新，再依次处理 dgx、win。
#   2) API 路径：查重已有 PR → 创建 PR → PUT 合并（merge 方式，保留分支）。
#   3) 本地兜底路径：冲突按归属解决（learn_links/learnings -> dgx；data/reports/boards/Obsidian -> win）。
#   4) 推送 main 带重试，且**用正确退出码判定成功**（绝不管道 tail 掩盖 non-fast-forward）。
#
# 用法（crontab，建议前置 `git checkout -f main &&` 确保从 main 读取本脚本）：
#   0 20 * * * cd ~/ai-project-weekly && git checkout -f main && GITHUB_TARGET_BRANCH=main bash src/merge_branches.sh
# 依赖：仓库根 .env 提供 GITHUB_TOKEN（headless 服务器 HTTPS 推送 / API 鉴权）。
# 注：原设计用 gh CLI，但 dgx 无 sudo/apt 且 GitHub 二进制下载受 TLS 抖动影响，
#     故直接用 REST API（curl）实现等价 PR 流程，零额外依赖。
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
API_REPO="${MERGE_GH_REPO:-wuqijin442/ai-project-weekly}"
API_REPO_OWNER="${API_REPO%%/*}"

LOG_DIR="$REPO_ROOT/Logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/merge-branches-$(date +%Y-%m-%d).log"
echo "=== $(date '+%F %T') merge_branches 启动（dgx=$BR_DGX win=$BR_WIN main=$BR_MAIN api=$API_REPO）===" | tee -a "$LOG"

# 0) 清残留 rebase / merge 状态
git rebase --abort >/dev/null 2>&1
git merge --abort >/dev/null 2>&1

# 1) fetch 所有远端分支（带重试）
FETCHED=0
for i in 1 2 3 4 5 6; do
  # 显式拉取全部分支（覆盖仓库可能配置的 single-branch fetch，确保 origin/dgx、origin/win 也更新）
  if git fetch origin '+refs/heads/*:refs/remotes/origin/*' >>"$LOG" 2>&1; then FETCHED=1; break; fi
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

# ---------------------------------------------------------------------------
# API PR 路径（优先）
# ---------------------------------------------------------------------------
api_pr_merge () {
  local br="$1"
  local title body pr_num mcode
  # 已合入 main（无新提交）则跳过
  if git merge-base --is-ancestor "origin/$br" "origin/$BR_MAIN" 2>/dev/null; then
    echo "<<< $br 已合入 main（无新提交），跳过" | tee -a "$LOG"
    return 0
  fi
  title="merge: $br -> $BR_MAIN $(date +%F)"
  body="每日 20:00 自动归集：将 $br 分支归并进 $BR_MAIN。文件归属天然不相交（learn_links/learnings->dgx，data/reports/boards/Obsidian->win），冲突按归属兜底。"
  # 查找已有 open PR（head 格式 owner:branch）
  pr_num=$(curl -s --max-time 30 \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$API_REPO/pulls?head=$API_REPO_OWNER:$br&base=$BR_MAIN&state=open" \
    | grep -oE '"number"[[:space:]]*:[[:space:]]*[0-9]+' | head -1 | grep -oE '[0-9]+')
  # 没有则创建（同仓 PR，head 用分支名）
  if [ -z "$pr_num" ]; then
    pr_num=$(curl -s -X POST --max-time 30 \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      -H "Content-Type: application/json" \
      -d "{\"title\":\"$title\",\"head\":\"$br\",\"base\":\"$BR_MAIN\",\"body\":\"$body\"}" \
      "https://api.github.com/repos/$API_REPO/pulls" \
      | grep -oE '"number"[[:space:]]*:[[:space:]]*[0-9]+' | head -1 | grep -oE '[0-9]+')
  fi
  if [ -z "$pr_num" ]; then
    echo "⚠️ $br PR 创建失败，转本地合并" | tee -a "$LOG"
    return 1
  fi
  # 合并 PR（保留分支，merge 方式）
  mcode=$(curl -s -o /dev/null -w "%{http_code}" -X PUT --max-time 30 \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "Content-Type: application/json" \
    -d '{"merge_method":"merge","delete_branch":false}' \
    "https://api.github.com/repos/$API_REPO/pulls/$pr_num/merge")
  if [ "$mcode" = "200" ] || [ "$mcode" = "201" ]; then
    echo "<<< $br 已通过 PR #$pr_num 合并进 $BR_MAIN" | tee -a "$LOG"
    return 0
  fi
  echo "⚠️ $br PR #$pr_num 合并失败(http=$mcode)，转本地合并" | tee -a "$LOG"
  return 1
}

# ---------------------------------------------------------------------------
# 本地 merge 兜底（冲突按归属解决）
# ---------------------------------------------------------------------------
merge_one () {
  local br="$1"; local owner="$2"
  # 同步最新 main，避免 API 路径已推进后本地落后导致 non-fast-forward
  git pull --rebase --autostash origin "$BR_MAIN" >>"$LOG" 2>&1
  echo ">>> 合并 $br -> $BR_MAIN（本地兜底）" | tee -a "$LOG"
  if git merge "origin/$br" --no-edit -m "merge: $br -> $BR_MAIN $(date +%F)" >>"$LOG" 2>&1; then
    echo "<<< $br 合并完成（无冲突）" | tee -a "$LOG"
    return 0
  fi
  echo "⚠️ $br 合并冲突，按归属解决（知识图谱=dgx，每日数据/Obsidian=win）" | tee -a "$LOG"
  for f in $(git diff --name-only --diff-filter=U); do
    case "$f" in
      knowledge-base/learn_links/*|reports/learnings/*)
        if [ "$owner" = "dgx" ]; then git checkout --theirs "$f"; else git checkout --ours "$f"; fi ;;
      data/metadata/*|reports/daily/*|reports/boards/*|Obsidian_Vault/*)
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

# ---------------------------------------------------------------------------
# 选择路径
# ---------------------------------------------------------------------------
API_OK=0
if [ -n "${GITHUB_TOKEN:-}" ] && command -v curl >/dev/null 2>&1; then
  acode=$(curl -s -o /dev/null -w "%{http_code}" --max-time 30 \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$API_REPO/pulls?state=all&per_page=1")
  [ "$acode" = "200" ] && API_OK=1
fi

PUSHED=0
if [ "$API_OK" -eq 1 ]; then
  echo ">>> 走 API PR 路径" | tee -a "$LOG"
  api_pr_merge "$BR_DGX" || merge_one "$BR_DGX" dgx
  git fetch origin "$BR_MAIN" >>"$LOG" 2>&1   # 刷新 origin/main 供第二分支判定
  api_pr_merge "$BR_WIN" || merge_one "$BR_WIN" win
  # 远端合并后同步本地 main
  git pull --rebase --autostash origin "$BR_MAIN" >>"$LOG" 2>&1
  PUSHED=1
else
  echo ">>> 走本地 merge 路径（API 不可用）" | tee -a "$LOG"
  merge_one "$BR_DGX" dgx
  merge_one "$BR_WIN" win
  # 推送 main（带重试，正确退出码）
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    PUSH_URL="https://${GITHUB_TOKEN}@github.com/${API_REPO}.git"
  else
    PUSH_URL="origin"
  fi
  for i in 1 2 3 4 5 6 7 8; do
    if git push -u "$PUSH_URL" "$BR_MAIN" >>"$LOG" 2>&1; then
      PUSHED=1
      echo "PUSH_OK=$i" | tee -a "$LOG"
      break
    fi
    echo "push 第 $i/8 次失败，退避 $((i * 5))s" | tee -a "$LOG"
    sleep $((i * 5))
  done
fi

if [ "$PUSHED" -eq 1 ]; then
  echo "<<< 归集完成（main HEAD=$(git rev-parse --short HEAD)）" | tee -a "$LOG"
else
  echo "<<< main 推送失败（明日再试）" | tee -a "$LOG"
fi
exit 0
