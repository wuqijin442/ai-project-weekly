#!/usr/bin/env bash
# 用 curl + shell `>` 重定向直接下到最终目录（绕过 Git Bash 下 curl -o 长路径写文件 bug）。
# 不用 -w（会混入文件体），下载后 stat 校验大小。
set -u
BASE="https://hf-mirror.com/openbmb/MiniCPM-o-4_5-gguf/resolve/main"
OUT="$HOME/omni_weights/MiniCPM-o-4_5-gguf"
mkdir -p "$OUT/vision" "$OUT/audio"
declare -A SZ=( [vision/MiniCPM-o-4_5-vision-F16.gguf]=1095113184 [audio/MiniCPM-o-4_5-audio-F16.gguf]=660167904 )
for rel in "${!SZ[@]}"; do
  out="$OUT/$rel"
  echo ">>> [$(date +%H:%M:%S)] $rel"
  curl -L -A "Mozilla/5.0" --retry 40 --retry-delay 3 --retry-all-errors \
       --connect-timeout 20 --max-time 1800 "$BASE/$rel" > "$out" 2>/dev/null
  rc=$?
  act=$(stat -c%s "$out" 2>/dev/null || echo 0)
  echo "    curl rc=$rc actual=$act expected=${SZ[$rel]}"
  if [ "$act" != "${SZ[$rel]}" ]; then echo "    !! SIZE MISMATCH on $rel"; fi
done
echo ALL_DOWNLOADS_FINISHED
