#!/usr/bin/env python3
# 下载 jarvis 锁定版 MiniCPM-o 4.5 全量权重 (LLM+VPM+APM) 到本地暂存，随后 scp 到 dgx。
# 用 urllib 流式写文件（规避 Git Bash 下 curl -o 写文件失败的问题），自带断点续传。
import os, sys, time, urllib.request

BASE = "https://hf-mirror.com/openbmb/MiniCPM-o-4_5-gguf/resolve/main"
ROOT = os.path.join(os.environ.get("HOME", "/tmp"), "omni_weights", "MiniCPM-o-4_5-gguf")
FILES = [
    "MiniCPM-o-4_5-Q4_K_M.gguf",
    "vision/MiniCPM-o-4_5-vision-F16.gguf",
    "audio/MiniCPM-o-4_5-audio-F16.gguf",
]
UA = {"User-Agent": "Mozilla/5.0"}
CHUNK = 1024 * 1024


def download(rel):
    out = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    url = BASE + "/" + rel
    for attempt in range(12):
        start = os.path.getsize(out) if os.path.exists(out) else 0
        req = urllib.request.Request(url, headers=UA)
        if start > 0:
            req.add_header("Range", "bytes=%d-" % start)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                status = getattr(r, "status", 200)
                mode = "ab" if (status == 206 and start > 0) else "wb"
                with open(out, mode) as f:
                    got = 0
                    while True:
                        buf = r.read(CHUNK)
                        if not buf:
                            break
                        f.write(buf)
                        got += len(buf)
                        if got % (200 * CHUNK) < CHUNK:
                            print("    %s +%dMB total=%dMB" % (rel, got // CHUNK, (start + got) // CHUNK), flush=True)
            size = os.path.getsize(out)
            print("  DONE %s size=%d bytes (%.2f GB)" % (rel, size, size / 1e9), flush=True)
            return True
        except Exception as e:
            print("  attempt %d failed on %s: %r" % (attempt, rel, e), flush=True)
            time.sleep(3)
    print("  FAILED %s" % rel, flush=True)
    return False


if __name__ == "__main__":
    print("STAGED_AT=%s" % ROOT, flush=True)
    ok = True
    for rel in FILES:
        print(">>> downloading %s" % rel, flush=True)
        if not download(rel):
            ok = False
    print("ALL_DOWNLOADS_FINISHED" if ok else "SOME_DOWNLOADS_FAILED")
