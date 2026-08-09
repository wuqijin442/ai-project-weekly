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

# 1) 拉取远端最新
#    区分两类失败：①网络抖动（可重试） ②内容冲突（重试无意义，必须告警）
#    2026-08-09 教训：07-30 日报 add/add 冲突让 pull 连败 6 轮，退出前又不清场，
#    仓库停在 detached HEAD + .git/rebase-merge 残留，且 exit 0 吞掉失败 ->
#    dgx 分支连续 4 天零提交且零告警。三点根治：清场 / 识别冲突 / 非零退出。
STUCK_FLAG="$LOG_DIR/PUSH_STUCK.flag"
PULLED=0
CONFLICT=0
for i in 1 2 3 4 5 6; do
  git rebase --abort >/dev/null 2>&1
  git merge --abort >/dev/null 2>&1
  PULL_ERR="$(git pull --rebase --autostash origin "$TARGET_BRANCH" 2>&1)"
  PULL_RC=$?
  printf '%s\n' "$PULL_ERR" >>"$LOG"
  if [ "$PULL_RC" -eq 0 ]; then
    PULLED=1
    break
  fi
  if printf '%s' "$PULL_ERR" | grep -qE "CONFLICT|could not apply|Resolve all conflicts|冲突|不能应用"; then
    CONFLICT=1
    echo "pull 遇内容冲突（非网络问题），重试无意义，立即停止" | tee -a "$LOG"
    break
  fi
  echo "pull 第 $i/6 次失败（疑似网络），退避 $((i * 5))s" | tee -a "$LOG"
  [ "$i" -lt 6 ] && sleep $((i * 5))
done
if [ "$PULLED" -ne 1 ]; then
  # 关键：退出前必须清场，否则残留状态会让后续所有 git 操作卡死
  git rebase --abort >/dev/null 2>&1
  git merge --abort >/dev/null 2>&1
  if [ "$CONFLICT" -eq 1 ]; then
    REASON="内容冲突（需人工介入，或 git merge -s ours origin/$TARGET_BRANCH 合流）"
  else
    REASON="网络持续不可达"
  fi
  {
    echo "date=$(date '+%F %T')"
    echo "branch=$TARGET_BRANCH"
    echo "reason=$REASON"
    echo "log=$LOG"
  } > "$STUCK_FLAG"
  echo "[ALERT] pull 持续失败：$REASON" | tee -a "$LOG"
  echo "[ALERT] 已写告警标记 $STUCK_FLAG（该文件存在 = 需人工介入）" | tee -a "$LOG"
  exit 2
fi
rm -f "$STUCK_FLAG" 2>/dev/null

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
  rm -f "$STUCK_FLAG" 2>/dev/null
  echo "<<< 推送成功（HEAD=$(git rev-parse --short HEAD) -> $TARGET_BRANCH）" | tee -a "$LOG"
else
  {
    echo "date=$(date '+%F %T')"
    echo "branch=$TARGET_BRANCH"
    echo "reason=push 连续 8 次失败"
    echo "log=$LOG"
  } > "$STUCK_FLAG"
  echo "[ALERT] 推送仍未成功，已写告警标记 $STUCK_FLAG" | tee -a "$LOG"
  exit 3
fi
exit 0
