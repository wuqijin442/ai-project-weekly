#!/usr/bin/env python3
# 仅重下 VPM + APM 两个权重（LLM 已在 hf-mirror 下好）。改用 HF 官方源，规避 hf-mirror SSL 断连。
import os, time, urllib.request, ssl

BASE = "https://huggingface.co/openbmb/MiniCPM-o-4_5-gguf/resolve/main"
ROOT = os.path.join(os.environ.get("HOME", "/tmp"), "omni_weights", "MiniCPM-o-4_5-gguf")
FILES = [
    "vision/MiniCPM-o-4_5-vision-F16.gguf",
    "audio/MiniCPM-o-4_5-audio-F16.gguf",
]
UA = {"User-Agent": "Mozilla/5.0"}
CHUNK = 256 * 1024


def download(rel):
    out = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    url = BASE + "/" + rel
    # 宽松 SSL：部分镜像 TLS 握手不稳
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    for attempt in range(20):
        start = os.path.getsize(out) if os.path.exists(out) else 0
        req = urllib.request.Request(url, headers=UA)
        if start > 0:
            req.add_header("Range", "bytes=%d-" % start)
        try:
            with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
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
                        if got % (100 * CHUNK) < CHUNK:
                            print("    %s +%dMB total=%dMB" % (rel, got // CHUNK, (start + got) // CHUNK), flush=True)
            size = os.path.getsize(out)
            print("  DONE %s size=%d (%.2f GB)" % (rel, size, size / 1e9), flush=True)
            return True
        except Exception as e:
            print("  attempt %d failed %s: %r" % (attempt, rel, e), flush=True)
            time.sleep(2)
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
