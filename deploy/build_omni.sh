#!/usr/bin/env bash
# build_omni.sh — 在 dgx (aarch64 / GB10, 无 CUDA) 编译 llama.cpp-omni 的 omni HTTP server
# 源码已由 WorkBuddy 盒子 scp 到 ~/llama.cpp-omni (commit b9d15b83, sha256-verified)
set -euo pipefail

OMNI_DIR="${OMNI_DIR:-$HOME/llama.cpp-omni}"
cd "$OMNI_DIR"

echo "== [1/3] 环境检查 =="
for t in cmake gcc g++ make; do
  command -v "$t" >/dev/null 2>&1 || { echo "缺少工具: $t"; exit 1; }
done
echo "cmake: $(cmake --version | head -1)"
echo "gcc  : $(gcc --version | head -1)"
echo "arch : $(uname -m)  nproc: $(nproc)"

echo "== [2/3] cmake 配置 (LLAMA_BUILD_SERVER=ON, GGML_NATIVE=ON, 无 CUDA) =="
rm -rf build && mkdir -p build && cd build
cmake -DLLAMA_BUILD_SERVER=ON \
      -DGGML_NATIVE=ON \
      -DLLAMA_CURL=ON \
      -DLLAMA_OPENSSL=ON \
      .. || { echo "cmake 失败 (如 LLAMA_OPENSSL 缺 openssl-dev，可去掉该开关重试)"; exit 1; }

echo "== [3/3] 编译 llama-omni-server ($(nproc) 并行) =="
make -j"$(nproc)" llama-omni-server

BIN="$(find "$PWD" -name llama-omni-server -type f | head -1)"
if [ -z "$BIN" ]; then echo "未找到二进制"; exit 1; fi
echo "BUILD OK -> $BIN"
echo "可运行: bash run_omni_server.sh"
