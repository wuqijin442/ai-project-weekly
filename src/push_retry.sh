#!/usr/bin/env bash
# ============================================================================
# push_retry.sh — 幂等、健壮的同步推送（被 run_daily.sh 步骤4 与重试 cron 共用）
#
# 分支感知：默认推 main；多机分支模型下由 GITHUB_TARGET_BRANCH 指定目标分支
# （dgx 端推 dgx 分支，Windows 端推 win 分支）。本脚本仅负责「把当前分支的
# 新增提交到远端对应分支」，具体归属由调用方（crontab / 自动化）通过环境变量决定。
#
# 设计目标：覆盖 headless 服务器（dgx）→ GitHub 凌晨偶发不可达（GnuTLS 中断 /
# 连接 134s 超时）的多小时窗口，避免「学习消化报告」因一次推送失败就丢失。
#
# 关键健壮性：
#   0) 推前先 abort 任何残留的 rebase/merge —— 这是上次失败 pull 留下
#      .git/rebase-merge 导致后续所有 git 操作卡死的根因，必须先清。
#   1) pull 用 --rebase --autostash，最多 6 次重试 + 退避（每次先 abort 残留）。
#   2) commit 仅在确有改动时执行（避免空提交失败）。
#   3) push 最多 8 次重试 + 退避，且**用正确退出码判定成功**（绝不用管道 tail 掩盖失败）。
#   4) 全程失败不致命：本次退出，下个 cron 周期（*/20 2-8）再试。
# ============================================================================
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT" || exit 1

# 从仓库根 .env 载入机密（若存在）；token 不进 git、不进 crontab。
if [ -f "$REPO_ROOT/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$REPO_ROOT/.env"
  set +a
fi

# 分支感知：默认 main；GITHUB_TARGET_BRANCH 指定实际目标分支（win/dgx）。
TARGET_BRANCH="${GITHUB_TARGET_BRANCH:-main}"

LOG_DIR="$REPO_ROOT/Logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/push-retry-$(date +%Y-%m-%d).log"
echo "=== $(date '+%F %T') push_retry 启动 @ $REPO_ROOT (branch=$TARGET_BRANCH) ===" | tee -a "$LOG"

# 0) 清理任何残留的 rebase / merge 状态（防止卡死）
git rebase --abort >/dev/null 2>&1
git merge --abort >/dev/null 2>&1

# 0.5) 确保停留在目标分支（仅当工作树干净时才切换，避免误丢未提交改动）
CURRENT="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
if [ "$CURRENT" != "$TARGET_BRANCH" ]; then
  if git diff --quiet && git diff --cached --quiet; then
    git checkout "$TARGET_BRANCH" >>"$LOG" 2>&1 \
      || git checkout -b "$TARGET_BRANCH" "origin/$TARGET_BRANCH" >>"$LOG" 2>&1 \
      || git checkout -b "$TARGET_BRANCH" >>"$LOG" 2>&1
    echo "（已切换到目标分支 $TARGET_BRANCH）" | tee -a "$LOG"
  else
    echo "⚠️ 当前分支 $CURRENT 有未提交改动且非目标分支 $TARGET_BRANCH，放弃切换以免丢失" | tee -a "$LOG"
  fi
fi

# 1) 拉取远端最新（容忍 TLS 抖动，最多 6 次，每次先 abort 残留）
PULLED=0
for i in 1 2 3 4 5 6; do
  git rebase --abort >/dev/null 2>&1
  if git pull --rebase --autostash origin "$TARGET_BRANCH" >>"$LOG" 2>&1; then
    PULLED=1
    break
  fi
  echo "pull 第 $i/6 次失败，退避 $((i * 5))s" | tee -a "$LOG"
  [ "$i" -lt 6 ] && sleep $((i * 5))
done
if [ "$PULLED" -ne 1 ]; then
  echo "pull 持续失败，本次放弃（下个 cron 周期再试）" | tee -a "$LOG"
  exit 0
fi

# 2) 提交本日新增（学习产物 / 数据 / 报告 / 图谱）
git add -A >>"$LOG" 2>&1
if git diff --cached --quiet; then
  echo "（无新增改动，无需提交）" | tee -a "$LOG"
else
  git commit -m "chore: 每日学习消化+图谱 $(date +%Y-%m-%d) [$TARGET_BRANCH]" >>"$LOG" 2>&1
fi

# 3) 推送（容忍 TLS 抖动，最多 8 次，**用 rc=$? 判定成功**）
if [ -n "${GITHUB_TOKEN:-}" ]; then
  PUSH_URL="https://${GITHUB_TOKEN}@github.com/wuqijin442/ai-project-weekly.git"
else
  PUSH_URL="origin"
fi
PUSHED=0
for i in 1 2 3 4 5 6 7 8; do
  if git push -u "$PUSH_URL" "$TARGET_BRANCH" >>"$LOG" 2>&1; then
    PUSHED=1
    echo "PUSH_OK=$i" | tee -a "$LOG"
    break
  fi
  echo "push 第 $i/8 次失败，退避 $((i * 5))s" | tee -a "$LOG"
  [ "$i" -lt 8 ] && sleep $((i * 5))
done

if [ "$PUSHED" -eq 1 ]; then
  echo "<<< 推送成功（HEAD=$(git rev-parse --short HEAD) -> $TARGET_BRANCH）" | tee -a "$LOG"
else
  echo "<<< 推送仍未成功（下个 cron 周期再试）" | tee -a "$LOG"
fi
exit 0
