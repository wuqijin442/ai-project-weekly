#!/usr/bin/env bash
# 下载 jarvis 锁定版 MiniCPM-o 4.5 全量权重 (LLM+VPM+APM) 到本地暂存，随后 scp 到 dgx。
# 修正点1：仓库名 openbmb/MiniCPM-o-4_5-gguf (下划线 4_5)，公开免令牌。
# 修正点2：输出路径不含空格（$HOME 下），避免 Git Bash 下 curl 写文件失败 (exit 23)。
set -u
BASE="https://hf-mirror.com/openbmb/MiniCPM-o-4_5-gguf/resolve/main"
ROOT="$HOME/omni_weights"
OUT="$ROOT/MiniCPM-o-4_5-gguf"
mkdir -p "$OUT/vision" "$OUT/audio"

FILES=(
  "MiniCPM-o-4_5-Q4_K_M.gguf"
  "vision/MiniCPM-o-4_5-vision-F16.gguf"
  "audio/MiniCPM-o-4_5-audio-F16.gguf"
)

for rel in "${FILES[@]}"; do
  out="$OUT/$rel"
  echo ">>> [$(date +%H:%M:%S)] downloading $rel"
  curl -L -C - --retry 8 --retry-delay 3 --connect-timeout 20 --max-time 900 \
       -A "Mozilla/5.0" -o "$out" "$BASE/$rel" \
       -w "    done $rel -> HTTP %{http_code} size=%{size_download} time=%{time_total}s\n"
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "    !! curl exit $rc on $rel (rerun with -C - to resume)"
  fi
done
echo "ALL_DOWNLOADS_FINISHED"
echo "STAGED_AT=$OUT"
