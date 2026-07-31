#!/usr/bin/env python3
# omni_bridge.py — 跑在 dgx 上，夹在 jarvis 桥接脚本与 llama-omni-server 之间。
#
# 重要：llama.cpp-omni 的 /v1/stream/omni_init 每次都会重新加载 audio+vision+LLM，
# 在 CPU 上耗时 5-7 分钟。因此本 bridge 启动时会后台完成一次 omni_init，并把
# 状态缓存到 _inited；后续请求直接走 prefill/decode，不再触发重载。
#
# llama.cpp-omni 协议：
#   POST /v1/stream/omni_init  {media_type:2, use_tts:false, duplex_mode:false} -> 加载模型
#   POST /v1/stream/prefill    {audio_path_prefix, img_path_prefix, text, cnt}  -> 灌 KV(返回{success})
#   POST /v1/stream/decode     {stream:true}                                   -> SSE 流式吐文
import json, base64, os, tempfile, threading, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

OMNI_BASE = os.environ.get("OMNI_BASE", "http://127.0.0.1:8080")
BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", "9600"))
# CPU 全量加载 6.8GB + 推理需要足够时间
REQ_TIMEOUT = int(os.environ.get("OMNI_TIMEOUT", "1200"))

_lock = threading.Lock()
_inited = False
_turn = 0  # prefill 的 index 计数器
_init_err = None


def _omni_post(path, payload, timeout=REQ_TIMEOUT, stream=False):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        OMNI_BASE + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        if stream:
            return r.read().decode("utf-8", "replace")
        return r.read().decode("utf-8", "replace")


def _ensure_init():
    global _inited, _init_err
    if _inited:
        return
    with _lock:
        if _inited:
            return
        if _init_err:
            raise RuntimeError(f"previous omni_init failed: {_init_err}")
        try:
            _omni_post(
                "/v1/stream/omni_init",
                {"media_type": 2, "use_tts": False, "duplex_mode": False},
                timeout=REQ_TIMEOUT,
            )
            _inited = True
        except Exception as e:
            _init_err = str(e)
            raise


def _decode_text(timeout=REQ_TIMEOUT):
    body = _omni_post("/v1/stream/decode", {"stream": True}, timeout=timeout, stream=True)
    parts = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        payload = line[len("data:"):].strip()
        if payload in ("", "[DONE]"):
            continue
        try:
            ev = json.loads(payload)
        except Exception:
            continue
        if ev.get("is_listen") or ev.get("end_of_turn") and not ev.get("content"):
            if ev.get("stop"):
                break
            continue
        c = ev.get("content")
        if c:
            parts.append(c)
        if ev.get("stop"):
            break
    return "".join(parts).strip()


def _prefill(text, image_b64, audio_b64):
    global _turn
    _ensure_init()
    tmp = tempfile.mkdtemp(prefix="jarvis_omni_")
    audio_path = img_path = ""
    if audio_b64:
        audio_path = os.path.join(tmp, "audio.wav")
        with open(audio_path, "wb") as f:
            f.write(base64.b64decode(audio_b64))
    if image_b64:
        img_path = os.path.join(tmp, "img.png")
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(image_b64))
    payload = {
        "audio_path_prefix": audio_path,
        "img_path_prefix": img_path,
        "text": text or "",
        "cnt": _turn,
    }
    _omni_post("/v1/stream/prefill", payload, timeout=REQ_TIMEOUT)
    _turn += 1
    return _decode_text(timeout=REQ_TIMEOUT)


def _warmup():
    try:
        print(f"[warmup] calling omni_init (timeout={REQ_TIMEOUT}s)...")
        t0 = time.time()
        _ensure_init()
        print(f"[warmup] omni_init done in {time.time()-t0:.1f}s")
    except Exception as e:
        print(f"[warmup] omni_init failed: {e}")


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/health", "/v1/health"):
            self._send(200, {"status": "ok", "role": "omni_bridge", "omni_base": OMNI_BASE, "inited": _inited})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/bridge/omni":
            self._send(404, {"error": "only /bridge/omni supported"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            data = json.loads(raw)
            text = data.get("text", "")
            image_b64 = data.get("image_b64") or data.get("image")
            audio_b64 = data.get("audio_b64") or data.get("audio")
            t0 = time.time()
            reply = _prefill(text, image_b64, audio_b64)
            print(f"[request] processed in {time.time()-t0:.1f}s, reply_len={len(reply)}")
            self._send(200, {"text": reply})
        except urllib.error.URLError as e:
            self._send(502, {"error": f"omni server unreachable: {e}"})
        except Exception as e:
            self._send(500, {"error": str(e)})

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


if __name__ == "__main__":
    print(f"omni_bridge listening on 0.0.0.0:{BRIDGE_PORT} -> omni {OMNI_BASE}")
    threading.Thread(target=_warmup, daemon=True).start()
    ThreadingHTTPServer(("0.0.0.0", BRIDGE_PORT), Handler).serve_forever()
