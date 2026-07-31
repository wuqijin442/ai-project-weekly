#!/usr/bin/env bash
# 用 curl 从 hf-mirror 重下 VPM+APM（urllib 在 hf-mirror 上 SSL 断，curl 正常）。
# 策略：先续传到 /tmp（curl -o 在 /tmp 可写），完成后 cp 到无空格的 omni_weights 目录。
set -u
BASE="https://hf-mirror.com/openbmb/MiniCPM-o-4_5-gguf/resolve/main"
OUT="$HOME/omni_weights/MiniCPM-o-4_5-gguf"
FILES=("vision/MiniCPM-o-4_5-vision-F16.gguf" "audio/MiniCPM-o-4_5-audio-F16.gguf")

for rel in "${FILES[@]}"; do
  base=$(basename "$rel")
  tmp="/tmp/omni_$base"
  echo ">>> [$(date +%H:%M:%S)] downloading $rel -> /tmp then cp"
  curl -L -A "Mozilla/5.0" --retry 40 --retry-delay 3 --retry-all-errors \
       --connect-timeout 20 --max-time 1800 -C - -o "$tmp" "$BASE/$rel" \
       -w "    curl done $rel HTTP %{http_code} size=%{size_download}\n"
  rc=$?
  if [ $rc -ne 0 ]; then echo "    !! curl exit $rc on $rel"; continue; fi
  mkdir -p "$OUT/$(dirname "$rel")"
  cp "$tmp" "$OUT/$rel" && echo "    cp -> $OUT/$rel ($(stat -c%s "$OUT/$rel") bytes)"
  rm -f "$tmp"
done
echo "ALL_DOWNLOADS_FINISHED"
