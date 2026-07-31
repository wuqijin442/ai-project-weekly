#!/usr/bin/env bash
# run_omni_server.sh — 在 dgx 启动 llama-omni-server (MiniCPM-o 4.5 全模态推理后端)
# 权重目录布局 (由 server-omni.cpp 固定派生，务必一致):
#   $MODEL_DIR/
#     MiniCPM-o-4_5-Q4_K_M.gguf            (LLM, 文本)
#     vision/MiniCPM-o-4_5-vision-F16.gguf (VPM, 视觉)
#     audio/MiniCPM-o-4_5-audio-F16.gguf   (APM, 音频)
set -euo pipefail

OMNI_DIR="${OMNI_DIR:-$HOME/llama.cpp-omni}"
MODEL_DIR="${MODEL_DIR:-$HOME/models/MiniCPM-o-4_5-gguf}"
LLM="$MODEL_DIR/MiniCPM-o-4_5-Q4_K_M.gguf"
PORT="${PORT:-8080}"

BIN="$(find "$OMNI_DIR/build" -name llama-omni-server -type f | head -1)"
[ -x "$BIN" ] && echo "binary: $BIN" || { echo "未找到 llama-omni-server，先跑 build_omni.sh"; exit 1; }
[ -f "$LLM" ] && echo "llm   : $LLM" || { echo "未找到 LLM: $LLM (先 scp 权重)"; exit 1; }

# aarch64 CPU 推理：一条序列即可 (omni server 为单会话 1:1 duplex)
EXTRA_ARGS="${EXTRA_ARGS:-} -ngl 0 -n 2048"

echo "== 启动 llama-omni-server on 0.0.0.0:$PORT =="
nohup "$BIN" -m "$LLM" --host 0.0.0.0 --port "$PORT" $EXTRA_ARGS \
  > "$OMNI_DIR/omni_server.log" 2>&1 &
echo "launched pid $!"
echo "日志: $OMNI_DIR/omni_server.log"
echo "健康检查: curl -s http://127.0.0.1:$PORT/v1/health"
