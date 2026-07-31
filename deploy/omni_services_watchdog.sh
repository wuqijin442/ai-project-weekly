#!/usr/bin/env bash
# omni_services_watchdog.sh — 确保 llama-omni-server + omni_bridge 始终运行。
# 用途：开机自启 + 崩溃自愈。无 sudo，靠 cron 每分钟调用一次。
#
# 设计要点：
#   - flock 保证单实例，避免 cron 重叠触发重复拉起。
#   - 先确保 omni server（8080）健康，再拉 bridge（9600）：bridge 预热 omni_init
#     依赖 server 已就绪，否则会误报 failed。
#   - 启动顺序：server -> 等健康 -> bridge -> 等预热。
set -u

OMNI_DIR="${OMNI_DIR:-$HOME/llama.cpp-omni}"
LOG="$OMNI_DIR/watchdog.log"

log(){ echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"; }

# 单实例锁
exec 9>/tmp/omni_watchdog.lock
flock -n 9 || { log "SKIP another instance holding lock"; exit 0; }

# 1) llama-omni-server（用 bin/ 前缀避免误匹配到看门狗自己的命令行）
if ! pgrep -f "bin/llama-omni-server" >/dev/null; then
  log "WARN omni server down -> launching"
  ( bash "$OMNI_DIR/run_omni_server.sh" >/dev/null 2>&1 & )
  for i in $(seq 1 30); do
    if curl -s --max-time 3 http://127.0.0.1:8080/v1/health 2>/dev/null | grep -q '"ok"'; then
      log "INFO omni server up after ~$((i*10))s"; break
    fi
    sleep 10
  done
else
  log "INFO omni server ok"
fi

# 2) omni_bridge（仅当 server 已健康才拉起，避免预热连不上）
if curl -s --max-time 3 http://127.0.0.1:8080/v1/health 2>/dev/null | grep -q '"ok"'; then
  if ! pgrep -f "python3 .*omni_bridge.py" >/dev/null; then
    log "WARN bridge down -> launching"
    ( nohup python3 "$OMNI_DIR/omni_bridge.py" > "$OMNI_DIR/bridge.log" 2>&1 < /dev/null & )
    for i in $(seq 1 90); do
      if grep -q "omni_init done" "$OMNI_DIR/bridge.log" 2>/dev/null; then
        log "INFO bridge warmup done after ~$((i*10))s"; break
      fi
      if grep -q "omni_init failed" "$OMNI_DIR/bridge.log" 2>/dev/null; then
        log "ERROR bridge warmup failed"; tail -20 "$OMNI_DIR/bridge.log" >> "$LOG"; break
      fi
      sleep 10
    done
  else
    log "INFO bridge ok"
  fi
else
  log "WARN omni server not healthy yet, skip bridge launch this tick"
fi

log "DONE tick"
