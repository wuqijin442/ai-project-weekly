#!/usr/bin/env bash
# ============================================================================
# Linux 服务器一键部署：把每日自动化完整跑起来
#   1) 安装系统依赖（git / python3 / python3-pip）
#   2) 以 HTTPS clone 仓库（不用 SSH，避免 key 依赖）
#   3) 配置 GITHUB_TOKEN（从环境变量或仓库内 .env 读取，不回显）
#   4) 写入 crontab，每日 07:40 自动运行 src/run_daily.sh
#
# 用法：
#   GITHUB_TOKEN=ghp_xxx  bash deploy/setup-linux.sh                 # 默认装到 ~/ai-project-weekly
#   GITHUB_TOKEN=ghp_xxx  bash deploy/setup-linux.sh /opt/aipw       # 指定目录
#   bash deploy/setup-linux.sh                                        # 仅装依赖+clone，token 后补
#   （也可把 GITHUB_TOKEN=xxx 写入仓库内 .env 后直接 bash deploy/setup-linux.sh）
# ============================================================================
set -u

REPO_URL="https://github.com/wuqijin442/ai-project-weekly.git"
TARGET="${1:-$HOME/ai-project-weekly}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

echo "==> 目标目录: $TARGET"

# ---- 1) 系统依赖 ----
echo "== 1) 安装系统依赖 (git / python3 / python3-pip) =="
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -y && sudo apt-get install -y git python3 python3-pip
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y git python3 python3-pip
elif command -v yum >/dev/null 2>&1; then
  sudo yum install -y git python3 python3-pip
elif command -v apk >/dev/null 2>&1; then
  sudo apk add --no-cache git python3 py3-pip
elif command -v pacman >/dev/null 2>&1; then
  sudo pacman -S --noconfirm git python python-pip
else
  echo "WARN: 未识别的包管理器，请手动安装 git / python3 / python3-pip"
fi

# ---- 2) Clone 仓库 (HTTPS) ----
echo "== 2) Clone 仓库 (HTTPS) =="
if [ -d "$TARGET/.git" ]; then
  echo "已存在 $TARGET，执行 git pull --ff-only"
  git -C "$TARGET" pull --ff-only || true
else
  git clone --depth 1 "$REPO_URL" "$TARGET"
fi
cd "$TARGET" || exit 1

# ---- 3) 配置 GITHUB_TOKEN ----
echo "== 3) 配置 GITHUB_TOKEN =="
if [ -z "$GITHUB_TOKEN" ] && [ -f "$TARGET/.env" ]; then
  # 从 .env 读取 GITHUB_TOKEN（不回显到终端）
  GITHUB_TOKEN="$(grep -v '^#' "$TARGET/.env" | grep '^GITHUB_TOKEN=' | head -1 | cut -d= -f2-)"
fi
if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "WARN: 未提供 GITHUB_TOKEN。推送会失败！"
  echo "      方式A: GITHUB_TOKEN=xxx bash deploy/setup-linux.sh"
  echo "      方式B: 把 'GITHUB_TOKEN=xxx' 写入 $TARGET/.env 并执行 chmod 600 $TARGET/.env"
else
  echo "OK: GITHUB_TOKEN 已就绪（已隐藏，不打印）"
  # 落盘到 .env 供 crontab 读取（权限收紧）
  grep -v '^GITHUB_TOKEN=' "$TARGET/.env" >"$TARGET/.env.tmp" 2>/dev/null || true
  echo "GITHUB_TOKEN=$GITHUB_TOKEN" >>"$TARGET/.env.tmp"
  mv "$TARGET/.env.tmp" "$TARGET/.env"
  chmod 600 "$TARGET/.env"
fi

# ---- 4) 写入 crontab ----
echo "== 4) 安装 crontab (每日 07:40) =="
CRON_LINE="40 7 * * * cd $TARGET && bash -c 'set -a; [ -f .env ] && . ./.env; set +a; bash src/run_daily.sh' >>$TARGET/Logs/cron-boot.log 2>&1"
# 去重：移除旧的 run_daily.sh 行后追加新行
( crontab -l 2>/dev/null | grep -v "run_daily.sh"; echo "$CRON_LINE" ) | crontab -
echo "已写入 crontab："
crontab -l | grep "run_daily.sh"

echo "== 完成 =="
echo "仓库:   $TARGET"
echo "手动跑: cd $TARGET && GITHUB_TOKEN=xxx bash src/run_daily.sh"
echo "日志:   $TARGET/Logs/cron-YYYY-MM-DD.log"
