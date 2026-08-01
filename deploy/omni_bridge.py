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
# 关键事实（踩坑总结）：
#   1) omni server 是「单会话 1:1 duplex」——全局只维护一个会话，且 cnt 是全局轮次。
#      并发请求或 cnt 不连续都会让它空转/返回垃圾。因此所有对 server 的调用必须串行。
#   2) 不要依赖 server 的全局 cnt 历史：bridge 每次对话都从 cnt=0(系统)+cnt=1(用户)
#      重新开始，等价于「独立单轮会话」，bridge 重启/并发都安全，不与会话 cnt 不同步。
#   3) server 在 content 里偶发把单引号转义成 \'（非法 JSON 转义），decode 解析时
#      必须 tolerant 地跳过坏行，不能让整次请求崩溃。
import json, base64, os, tempfile, threading, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

OMNI_BASE = os.environ.get("OMNI_BASE", "http://127.0.0.1:8080")
BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", "9600"))
REQ_TIMEOUT = int(os.environ.get("OMNI_TIMEOUT", "300"))

# server 单会话 1:1：所有对 server 的调用（init/prefill/decode）必须串行，
# 否则并发会破坏唯一会话，导致空转或返回非法数据。
_lock = threading.Lock()
_inited = False  # omni_init（模型加载）是否已完成（全局仅一次）


def _omni_post(path, payload, timeout=REQ_TIMEOUT, stream=False):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        OMNI_BASE + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _ensure_init():
    """omni_init：加载 LLM+APM+VPM（CPU 上慢，全局仅一次）。"""
    global _inited
    with _lock:
        if _inited:
            return
        try:
            _omni_post(
                "/v1/stream/omni_init",
                {"media_type": 2, "use_tts": False, "duplex_mode": False},
                timeout=REQ_TIMEOUT,
            )
        except Exception as e:
            # server 已经初始化（重复 omni_init 返回 500 / already-initialized）时，
            # 视为就绪，可直接复用，不必重载模型、也不应永久阻塞。
            msg = str(e)
            if "500" in msg or "already" in msg.lower() or "init" in msg.lower():
                pass
            else:
                raise
        _inited = True


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
            # server 偶发非法 JSON 转义（如 content 里的 \'），跳过该行而非崩溃
            continue
        if ev.get("is_listen"):
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
    # 每次对话 = 独立单轮会话：omni_init(全局一次) + cnt=0(系统初始化) + cnt=1(用户)
    # 不维护全局递增 cnt，彻底避免与 server 单会话的全局 cnt 不同步。
    with _lock:
        _ensure_init()
        print("[pf] init ok", flush=True)
        # cnt=0 系统初始化：把 server 会话重置为干净的系统上下文（幂等，可重复）
        _omni_post(
            "/v1/stream/prefill",
            {"audio_path_prefix": "", "img_path_prefix": "", "text": "", "cnt": 0},
            timeout=REQ_TIMEOUT,
        )
        print("[pf] sys prefill ok", flush=True)
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
        # cnt=1 用户轮次（与 server 约定从 1 开始）
        _omni_post(
            "/v1/stream/prefill",
            {"audio_path_prefix": audio_path, "img_path_prefix": img_path,
             "text": text or "", "cnt": 1},
            timeout=REQ_TIMEOUT,
        )
        print("[pf] user prefill ok", flush=True)
        return _decode_text(timeout=REQ_TIMEOUT)


def _warmup():
    try:
        _ensure_init()
        print("[warmup] ready", flush=True)
    except Exception as e:
        print(f"[warmup] failed: {e}", flush=True)


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
                             "omni_base": OMNI_BASE, "inited": _inited})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/bridge/omni":
            self._send(404, {"error": "only /bridge/omni supported"})
            return
        try:
            print("[post] start", flush=True)
            length = int(self.headers.get("Content-Length", 0))
            print(f"[post] len={length}", flush=True)
            raw = self.rfile.read(length)
            print(f"[post] raw={raw[:60]!r}", flush=True)
            data = json.loads(raw)
            print("[post] json ok", flush=True)
            text = data.get("text", "")
            image_b64 = data.get("image_b64") or data.get("image")
            audio_b64 = data.get("audio_b64") or data.get("audio")
            t0 = time.time()
            reply = _prefill(text, image_b64, audio_b64)
            print(f"[request] processed in {time.time()-t0:.1f}s, reply_len={len(reply)}", flush=True)
            self._send(200, {"text": reply})
        except urllib.error.URLError as e:
            self._send(502, {"error": f"omni server unreachable: {e}"})
        except Exception as e:
            self._send(500, {"error": str(e)})

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}", flush=True)


if __name__ == "__main__":
    print(f"omni_bridge listening on 0.0.0.0:{BRIDGE_PORT} -> omni {OMNI_BASE}", flush=True)
    threading.Thread(target=_warmup, daemon=True).start()
    ThreadingHTTPServer(("0.0.0.0", BRIDGE_PORT), Handler).serve_forever()
