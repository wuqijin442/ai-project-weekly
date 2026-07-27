#!/usr/bin/env bash
# ============================================================================
# 每日自动化编排（Linux / macOS / WSL 通用）
#   步骤1：多类别 GitHub 热门日报   -> python src/main.py    （内含 git 推送）
#   步骤2：11 板块 AI 项目深潜测试  -> python src/board_workflow.py
#   步骤3：Ollama DeepSeek 学习+链接 -> python src/learn_link.py（best-effort）
#   步骤4：委托 src/push_retry.sh 同步推送（幂等健壮；同脚本被重试 cron 复用）
# 四步骤每日都跑；脚本路径无关（按本文件位置推导仓库根）。
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

# 从仓库根 .env 载入机密（若存在）。.env 必须 chmod 600 且已被 .gitignore 排除。
# 这样 token 不进 crontab、不进 git；headless 服务器靠它做 HTTPS 推送。
if [ -f "$REPO_ROOT/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$REPO_ROOT/.env"
  set +a
fi

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

echo ">>> [步骤3] Ollama DeepSeek 学习+链接（best-effort，失败不阻断）" | tee -a "$LOG"
"$PY" src/learn_link.py >>"$LOG" 2>&1
RC3=$?
echo "<<< 步骤3 退出码=$RC3" | tee -a "$LOG"

# ---- 步骤4：把「学习+链接」产物（及本日任何新增）同步推送 ----
# 委托 src/push_retry.sh：幂等、健壮（先 abort 残留 rebase，再 pull 重试→commit→push 重试）。
# 该脚本同时被重试 cron（*/20 2-8）调用，覆盖 GitHub 凌晨偶发不可达的多小时窗口。
echo ">>> [步骤4] 同步推送（委托 push_retry.sh）" | tee -a "$LOG"
bash "$SCRIPT_DIR/push_retry.sh" >>"$LOG" 2>&1
RC4=$?
echo "<<< 步骤4 退出码=$RC4" | tee -a "$LOG"

echo "=== $(date '+%F %T') 完成 (步骤1=$RC1 步骤2=$RC2 步骤3=$RC3 步骤4=$RC4) ===" | tee -a "$LOG"

# 步骤1/2 是主流程，必须成功；步骤3/4 为增强与同步（best-effort），
# 即使 Ollama/DeepSeek 不可用或推送失败，也不影响当日数据采集。
if [ "$RC1" -eq 0 ] && [ "$RC2" -eq 0 ]; then
  exit 0
fi
exit 1
