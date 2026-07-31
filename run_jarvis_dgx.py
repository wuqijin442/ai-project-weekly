"""
run_jarvis_dgx.py v3 — 用 dgx 服务器上的模型驱动 pub-local-jarvis 后端。

支持两种后端模式（环境变量 JARVIS_MODE 切换）：

  [ollama] 默认。dgx Ollama 上的 openbmb/minicpm-o4.5（文本+视觉）。
           实现「对话 + 看屏幕」。Ollama 不支持音频输入，故无「听声音」。

  [omni]    dgx 上的 llama.cpp-omni server + 完整 MiniCPM-o 4.5 权重（含 APM 音频）。
           经 omni_bridge.py（端口 8081）实现「对话 + 看屏幕 + 听声音」三模态全功能。
           需要 dgx 侧已编译 llama-omni-server 并 scp 完整权重（见 deploy/WEIGHTS_MANIFEST.md）。

背景：pub-local-jarvis 原生只支持「本地 C++ worker 加载 GGUF」或「fake 替身」，没有「远程模型」
模式。但 create_app(settings, native_client=...) 允许注入自定义 NativeClient。本脚本继承
NativeClient，把 ask（对话）请求转发到 dgx 的远程推理后端，其余命令按 fake 方式回显，
从而在不改动克隆仓库源码的前提下用真实远程模型完成 jarvis 的真实对话路径。

用法：
  # ollama 模式（默认，已验证）
  <venv>/Scripts/python.exe run_jarvis_dgx.py
  # omni 模式（需 dgx 侧 omni server + 完整权重就位）
  JARVIS_MODE=omni <venv>/Scripts/python.exe run_jarvis_dgx.py

  curl -X POST http://127.0.0.1:8000/api/v1/assistant/chat -H "Content-Type: application/json" \
    -d "{\"message\":\"屏幕上都显示了什么内容？\"}"

环境变量：
  JARVIS_MODE             ollama(默认) | omni
  JARVIS_DGX_MODEL        ollama 模式模型名（默认 openbmb/minicpm-o4.5:latest）
  ENABLE_SCREEN_CAPTURE   是否抓本机截图作视觉输入（默认 1；设 0 关闭→纯对话）
  ENABLE_AUDIO_CAPTURE    omni 模式是否抓本机麦克风作音频输入（默认 0；需 sounddevice）
  DGX_OLLAMA_URL          ollama 地址（默认 http://192.168.0.121:11434/api/chat）
  DGX_OMNI_BRIDGE_URL     omni bridge 地址（默认 http://192.168.0.121:8081/bridge/omni）
  DGX_OMNI_HEALTH_URL     omni bridge 健康检查（默认 http://192.168.0.121:8081/health）
"""

from __future__ import annotations

import asyncio
import base64
import io
import json
import os
import urllib.request
from collections.abc import AsyncIterator
from typing import Any

import uvicorn

from jarvis_backend.app import create_app
from jarvis_backend.native import NativeClient
from jarvis_backend.settings import Settings

# ---- 通用配置 ----
JARVIS_MODE = os.environ.get("JARVIS_MODE", "ollama").lower()
ENABLE_SCREEN_CAPTURE = os.environ.get("ENABLE_SCREEN_CAPTURE", "1") == "1"
ENABLE_AUDIO_CAPTURE = os.environ.get("ENABLE_AUDIO_CAPTURE", "0") == "1"

# ---- ollama 模式配置 ----
OLLAMA_CHAT_URL = os.environ.get(
    "DGX_OLLAMA_URL", "http://192.168.0.121:11434/api/chat"
)
MODEL_NAME = os.environ.get("JARVIS_DGX_MODEL", "openbmb/minicpm-o4.5:latest")
REQUEST_TIMEOUT = float(os.environ.get("DGX_TIMEOUT", "120"))

# ---- omni 模式配置 ----
OMNI_BRIDGE_URL = os.environ.get(
    "DGX_OMNI_BRIDGE_URL", "http://192.168.0.121:9600/bridge/omni"
)
OMNI_HEALTH_URL = os.environ.get(
    "DGX_OMNI_HEALTH_URL", "http://192.168.0.121:9600/health"
)
OMNI_TIMEOUT = float(os.environ.get("DGX_OMNI_TIMEOUT", "300"))


# ----------------------------------------------------------------------------
# 屏幕 / 音频采集
# ----------------------------------------------------------------------------
def capture_screen() -> bytes | None:
    """抓取主屏截图，返回 PNG bytes；无显示环境或无依赖时返回 None（降级为纯对话）。"""
    try:
        import mss

        with mss.mss() as sct:
            mon = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            shot = sct.grab(mon)
            from PIL import Image

            pil = Image.frombytes("RGB", shot.size, shot.rgb)
            buf = io.BytesIO()
            pil.save(buf, format="PNG")
            return buf.getvalue()
    except Exception:
        pass
    try:
        from PIL import ImageGrab

        img = ImageGrab.grab()
        if img is None:
            return None
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        return None


def capture_audio(duration: float = 3.0, sample_rate: int = 16000) -> bytes | None:
    """抓取本机麦克风音频，返回 WAV bytes（16kHz 单声道，MiniCPM-o 要求）。
    依赖 sounddevice + numpy。无依赖/无麦克风时返回 None（降级为无音频）。"""
    try:
        import sounddevice as sd
        import numpy as np
        import wave

        rec = sd.rec(int(duration * sample_rate), samplerate=sample_rate,
                     channels=1, dtype="int16")
        sd.wait()
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(np.frombuffer(rec, dtype=np.int16).tobytes())
        return buf.getvalue()
    except Exception as e:
        print(f"[capture_audio] 跳过（{e}）")
        return None


# ----------------------------------------------------------------------------
# jarvis prompt 解析（指令文字 + 末尾 JSON → 标准多轮消息）
# ----------------------------------------------------------------------------
def parse_jarvis_prompt(text: str) -> list[dict[str, Any]]:
    start = text.find("{")
    if start != -1:
        snippet = text[start:]
        try:
            obj, _ = json.JSONDecoder().raw_decode(snippet)
            if isinstance(obj, dict) and "user_message" in obj:
                history = obj.get("recent_dialog") or []
                msgs: list[dict[str, Any]] = []
                for turn in history:
                    if not isinstance(turn, dict):
                        continue
                    u = str(turn.get("user", "")).strip()
                    a = str(turn.get("assistant", "")).strip()
                    if u:
                        msgs.append({"role": "user", "content": u})
                    if a:
                        msgs.append({"role": "assistant", "content": a})
                um = str(obj["user_message"]).strip()
                if um:
                    msgs.append({"role": "user", "content": um})
                if msgs:
                    return msgs
        except (json.JSONDecodeError, ValueError):
            pass
    return [{"role": "user", "content": text}]


# ----------------------------------------------------------------------------
# Ollama 模式客户端（文本 + 视觉，已验证）
# ----------------------------------------------------------------------------
class RemoteOllamaNativeClient(NativeClient):
    def __init__(
        self,
        base_url: str = OLLAMA_CHAT_URL,
        model: str = MODEL_NAME,
        timeout: float = REQUEST_TIMEOUT,
    ) -> None:
        self.running = False
        self._events: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    async def start(self) -> None:
        self.running = True
        await self.emit({
            "type": "worker.ready",
            "inference_provider": "remote-ollama",
            "model": self.model,
            "vision": ENABLE_SCREEN_CAPTURE,
        })

    async def stop(self) -> None:
        if self.running:
            self.running = False
            await self._events.put(None)

    async def request(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.running:
            raise RuntimeError("native worker is not running")
        if method == "ping":
            return {"ok": True, "result": "pong"}
        if method == "ask":
            text = str(payload.get("text", ""))
            reply = await self._chat(text)
            return {"ok": True, "text": reply}
        return {"ok": True, "method": method, "result": payload}

    async def _chat(self, text: str) -> str:
        messages = parse_jarvis_prompt(text)
        if ENABLE_SCREEN_CAPTURE:
            png = capture_screen()
            if png:
                b64 = base64.b64encode(png).decode("ascii")
                attached = False
                for m in reversed(messages):
                    if m.get("role") == "user":
                        m["images"] = [b64]
                        attached = True
                        break
                if not attached:
                    messages.append(
                        {"role": "user", "content": "（附上当前屏幕截图）", "images": [b64]}
                    )
        body = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "think": False,
        }

        def _post() -> dict[str, Any]:
            req = urllib.request.Request(
                self.base_url,
                data=json.dumps(body).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))

        data = await asyncio.to_thread(_post)
        return str(data.get("message", {}).get("content", "")).strip()

    async def emit(self, event: dict[str, Any]) -> None:
        await self._events.put(event)

    async def events(self) -> AsyncIterator[dict[str, Any]]:
        while True:
            event = await self._events.get()
            if event is None:
                break
            yield event


# ----------------------------------------------------------------------------
# OMNI 模式客户端（文本 + 视觉 + 音频，需 dgx omni server + 完整权重）
# 经 omni_bridge.py 转发：bridge 收 base64 音频/图 → 落盘成文件 → 调 omni server prefill
# ----------------------------------------------------------------------------
class RemoteOmniNativeClient(NativeClient):
    def __init__(
        self,
        bridge_url: str = OMNI_BRIDGE_URL,
        health_url: str = OMNI_HEALTH_URL,
        timeout: float = OMNI_TIMEOUT,
    ) -> None:
        self.running = False
        self._events: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()
        self.bridge_url = bridge_url
        self.health_url = health_url
        self.timeout = timeout

    async def start(self) -> None:
        # 预检 bridge 是否可达
        ok = await asyncio.to_thread(self._health)
        if not ok:
            print(f"[omni] 警告: bridge 不可达 {self.health_url}，请确认 dgx 上 omni_bridge.py 已启动")
        self.running = True
        await self.emit({
            "type": "worker.ready",
            "inference_provider": "remote-omni",
            "model": "minicpm-o-4.5 (full, APM included)",
            "vision": ENABLE_SCREEN_CAPTURE,
            "audio": ENABLE_AUDIO_CAPTURE,
        })

    def _health(self) -> bool:
        try:
            req = urllib.request.Request(self.health_url)
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status == 200
        except Exception:
            return False

    async def stop(self) -> None:
        if self.running:
            self.running = False
            await self._events.put(None)

    async def request(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.running:
            raise RuntimeError("native worker is not running")
        if method == "ping":
            return {"ok": True, "result": "pong"}
        if method == "ask":
            text = str(payload.get("text", ""))
            reply = await self._chat(text)
            return {"ok": True, "text": reply}
        return {"ok": True, "method": method, "result": payload}

    async def _chat(self, text: str) -> str:
        # omni bridge 直接吃纯文本（jarvis 的指令包装由 bridge→omni server 内部处理更稳），
        # 这里提取 user_message 作为主文本，附带最新一轮截图与（可选）麦克风音频。
        messages = parse_jarvis_prompt(text)
        user_text = messages[-1]["content"] if messages else text

        image_b64 = None
        if ENABLE_SCREEN_CAPTURE:
            png = capture_screen()
            if png:
                image_b64 = base64.b64encode(png).decode("ascii")

        audio_b64 = None
        if ENABLE_AUDIO_CAPTURE:
            wav = capture_audio()
            if wav:
                audio_b64 = base64.b64encode(wav).decode("ascii")

        payload = {"text": user_text}
        if image_b64:
            payload["image_b64"] = image_b64
        if audio_b64:
            payload["audio_b64"] = audio_b64

        def _post() -> str:
            req = urllib.request.Request(
                self.bridge_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return str(data.get("text", "")).strip()

        return await asyncio.to_thread(_post)

    async def emit(self, event: dict[str, Any]) -> None:
        await self._events.put(event)

    async def events(self) -> AsyncIterator[dict[str, Any]]:
        while True:
            event = await self._events.get()
            if event is None:
                break
            yield event


# ----------------------------------------------------------------------------
# 入口
# ----------------------------------------------------------------------------
def main() -> None:
    settings = Settings()
    if JARVIS_MODE == "omni":
        client: NativeClient = RemoteOmniNativeClient()
        provider = "omni (dgx llama.cpp-omni server, full MiniCPM-o 4.5)"
    else:
        client = RemoteOllamaNativeClient()
        provider = f"ollama ({MODEL_NAME} @ {OLLAMA_CHAT_URL})"

    app = create_app(settings, client)
    print(
        f"[run_jarvis_dgx] 模式={JARVIS_MODE} | 后端={provider}\n"
        f"[run_jarvis_dgx] 屏幕视觉={'开启' if ENABLE_SCREEN_CAPTURE else '关闭'} | "
        f"音频捕获={'开启' if (JARVIS_MODE=='omni' and ENABLE_AUDIO_CAPTURE) else '关闭'}\n"
        f"[run_jarvis_dgx] 监听 http://{settings.server.host}:{settings.server.port}"
    )
    uvicorn.run(
        app,
        host=settings.server.host,
        port=settings.server.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
