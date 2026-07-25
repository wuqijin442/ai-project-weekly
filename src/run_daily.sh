#!/usr/bin/env bash
# ============================================================================
# 每日自动化编排（Linux / macOS / WSL 通用）
#   步骤1：多类别 GitHub 热门日报   -> python src/main.py
#   步骤2：11 板块 AI 项目深潜测试  -> python src/board_workflow.py
# 两步骤每日都跑；脚本路径无关（按本文件位置推导仓库根）。
#
# 用法：
#   bash src/run_daily.sh
#   GITHUB_TOKEN=xxx bash src/run_daily.sh        # headless 服务器必须带 token
# 也可被 crontab / systemd timer 调用（建议用绝对路径）。
# ============================================================================
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT" || exit 1

# 解析 python 解释器：Linux 多为 python3，macOS/Windows 多为 python
PY="$(command -v python3 || command -v python)"
if [ -z "$PY" ]; then
  echo "ERROR: 未找到 python3 / python，无法运行"
  exit 1
fi

# ---- 可调环境变量（不传则用脚本内默认值）----
export INSTALL_TIMEOUT="${INSTALL_TIMEOUT:-300}"
export RUN_TIMEOUT="${RUN_TIMEOUT:-45}"
export BOARD_INSTALL_TIMEOUT="${BOARD_INSTALL_TIMEOUT:-150}"
export BOARD_RUN_TIMEOUT="${BOARD_RUN_TIMEOUT:-40}"
export BOARD_API_PACE="${BOARD_API_PACE:-7}"
export CLONE_DEPTH="${CLONE_DEPTH:-1}"

# GITHUB_TOKEN 必须在环境中（headless Linux 推送靠它）；未设置给出警告但不阻断
if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "WARN: 未设置 GITHUB_TOKEN，GitHub 推送可能失败（headless 服务器需 HTTPS token）"
fi

LOG_DIR="$REPO_ROOT/Logs"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y-%m-%d)"
LOG="$LOG_DIR/cron-$STAMP.log"

echo "=== $(date '+%F %T') 启动每日自动化 @ $REPO_ROOT (python=$PY) ===" | tee -a "$LOG"

echo ">>> [步骤1] 多类别日报" | tee -a "$LOG"
"$PY" src/main.py >>"$LOG" 2>&1
RC1=$?
echo "<<< 步骤1 退出码=$RC1" | tee -a "$LOG"

echo ">>> [步骤2] 11 板块深潜" | tee -a "$LOG"
"$PY" src/board_workflow.py >>"$LOG" 2>&1
RC2=$?
echo "<<< 步骤2 退出码=$RC2" | tee -a "$LOG"

echo "=== $(date '+%F %T') 完成 (步骤1=$RC1 步骤2=$RC2) ===" | tee -a "$LOG"

# 任一脚本崩溃（非 0）则整体非 0，便于 cron / 监控系统告警
if [ "$RC1" -eq 0 ] && [ "$RC2" -eq 0 ]; then
  exit 0
fi
exit 1
