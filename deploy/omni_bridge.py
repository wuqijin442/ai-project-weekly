#!/usr/bin/env python3
# omni_bridge.py — 跑在 dgx 上，夹在 jarvis 桥接脚本与 llama-omni-server 之间。
#
# llama.cpp-omni 协议（依据 tools/omni/test/single_test_omni.cpp 官方用法）：
#   POST /v1/stream/omni_init  {media_type:2, use_tts:false, duplex_mode:false} -> 加载模型
#   POST /v1/stream/prefill {audio_path_prefix, img_path_prefix, text, cnt}:
#       cnt=0  -> 仅做系统 prompt + ref_audio 初始化，不处理任何用户数据
#       cnt>=1 -> 用户轮次（文本/音频/图像），必须从 1 开始递增
#   POST /v1/stream/decode {stream:true} -> SSE 流式吐文
#
# 关键修复：之前把用户文本塞进 cnt=0（被忽略），导致 decode 空转 2048 token 超时。
# 现在严格分离：cnt=0 只初始化系统，用户文本走 cnt>=1 的独立 prefill。
import json, base64, os, tempfile, threading, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

OMNI_BASE = os.environ.get("OMNI_BASE", "http://127.0.0.1:8080")
BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", "9600"))
REQ_TIMEOUT = int(os.environ.get("OMNI_TIMEOUT", "1200"))

_lock = threading.Lock()
_inited = False          # omni_init（模型加载）完成
_init_err = None
_system_inited = False   # cnt=0 系统 prompt 初始化完成
_turn = 1                # 用户轮次索引（从 1 开始）


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
    """omni_init：加载 LLM+APM+VPM（CPU 上慢，仅需一次）。"""
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


def _system_prefill():
    """cnt=0：系统 prompt + ref_audio 初始化（不处理用户数据，仅需一次）。"""
    global _system_inited
    if _system_inited:
        return
    with _lock:
        if _system_inited:
            return
        _omni_post(
            "/v1/stream/prefill",
            {"audio_path_prefix": "", "img_path_prefix": "", "text": "", "cnt": 0},
            timeout=REQ_TIMEOUT,
        )
        _system_inited = True


def _decode_text(timeout=REQ_TIMEOUT):
    print("[decode] posting decode...", flush=True)
    body = _omni_post("/v1/stream/decode", {"stream": True}, timeout=timeout, stream=True)
    print(f"[decode] got {len(body)} bytes", flush=True)
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
    _system_prefill()  # cnt=0 系统初始化（首次）
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
    # 用户轮次：cnt>=1（从 1 开始递增）。空串会被 server 端守卫跳过。
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
        print(f"[warmup] omni_init (timeout={REQ_TIMEOUT}s)...")
        t0 = time.time()
        _ensure_init()
        _system_prefill()  # 预热系统 prompt，首请求更快
        print(f"[warmup] ready in {time.time()-t0:.1f}s")
    except Exception as e:
        print(f"[warmup] failed: {e}")


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
            self._send(200, {"status": "ok", "role": "omni_bridge",
                             "omni_base": OMNI_BASE,
                             "inited": _inited, "system_inited": _system_inited})
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
