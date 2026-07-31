# MiniCPM-o 4.5 完整权重 — 下载与 scp 清单（给老大的手动操作手册）

> 目的：让 dgx 上的 `llama-omni-server` 加载**完整三模态**权重（LLM+视觉+音频），
> 从而让 jarvis 经 `run_jarvis_dgx.py` 跑通「对话 + 看屏幕 + 听声音」。
>
> **为什么必须手动**：WorkBuddy 盒子（与我同机）没有 HuggingFace 令牌，HF / hf-mirror / ModelScope
> 对权重内容都返回 401，我无法直接拉 ~7GB 权重。GitHub 可达，所以 **omni 源码我已拉好并 scp 到 dgx**，
> 只剩「权重」这一步需要你侧落地（你有 HF 访问权限的机器来下）。

---

## 1. 精确的权重文件清单（源码 `server-omni.cpp` 已坐实布局）

目标目录（dgx）：`~/models/MiniCPM-o-4_5-gguf/`

```
MiniCPM-o-4_5-gguf/
├── MiniCPM-o-4_5-Q4_K_M.gguf            # LLM 文本生成  ~5.0 GB   (必下)
├── vision/
│   └── MiniCPM-o-4_5-vision-F16.gguf    # VPM 视觉编码  ~1.1 GB   (必下)
└── audio/
    └── MiniCPM-o-4_5-audio-F16.gguf     # APM 音频理解  ~0.66 GB  (必下, 即"补全的 APM")
```

- 总计约 **6.8 GB**。
- `tts/MiniCPM-o-4_5-tts-F16.gguf`（语音合成）**不需要** —— jarvis 只输出文字、不播语音（VENDOR.json 明确排除 TTS）。
- ⚠️ dgx 上 Ollama 已有的 `openbmb/minicpm-o4.5` 是 Ollama blob 格式（且缺 APM），**不能直接给 omni server 用**。
  ico server 读的是上面这套**原始 gguf 目录布局**，请单独下载。

---

## 2. 在你的机器上下载（任选一种，需 HF 访问权限）

### 方式 A：huggingface_hub（Python，推荐，自动断点续传）
```bash
pip install -U huggingface_hub
# 已登录(huggingface-cli login) 或设置环境变量 HF_TOKEN=xxx
export HF_TOKEN=你的令牌
python3 - <<'PY'
from huggingface_hub import hf_hub_download
REPO="OpenBMB/MiniCPM-o_4.5-gguf"
DST="MiniCPM-o-4_5-gguf"
for f in ["MiniCPM-o-4_5-Q4_K_M.gguf",
          "vision/MiniCPM-o-4_5-vision-F16.gguf",
          "audio/MiniCPM-o-4_5-audio-F16.gguf"]:
    hf_hub_download(REPO, f, local_dir=DST)
    print("downloaded", f)
PY
```

### 方式 B：curl 直链（带令牌）
```bash
export HF_TOKEN=你的令牌
BASE="https://huggingface.co/OpenBMB/MiniCPM-o_4.5-gguf/resolve/main"
mkdir -p MiniCPM-o-4_5-gguf/vision MiniCPM-o-4_5-gguf/audio
curl -L -H "Authorization: Bearer $HF_TOKEN" -o MiniCPM-o-4_5-gguf/MiniCPM-o-4_5-Q4_K_M.gguf "$BASE/MiniCPM-o-4_5-Q4_K_M.gguf"
curl -L -H "Authorization: Bearer $HF_TOKEN" -o MiniCPM-o-4_5-gguf/vision/MiniCPM-o-4_5-vision-F16.gguf "$BASE/vision/MiniCPM-o-4_5-vision-F16.gguf"
curl -L "Authorization: Bearer $HF_TOKEN" -o MiniCPM-o-4_5-gguf/audio/MiniCPM-o-4_5-audio-F16.gguf "$BASE/audio/MiniCPM-o-4_5-audio-F16.gguf"
```
> 若 HF 主站慢，可把 `BASE` 换成 `https://hf-mirror.com/OpenBMB/MiniCPM-o_4.5-gguf/resolve/main`（镜像，同样需令牌）。

---

## 3. scp 到 dgx（保持子目录结构）

```bash
# 在你的机器上执行（能 ssh 到 dgx 的那台）
scp -r MiniCPM-o-4_5-gguf/ dgx:~/models/MiniCPM-o-4_5-gguf/
```

scp 完成后，在 dgx 上核对：
```bash
ssh dgx 'find ~/models/MiniCPM-o-4_5-gguf -type f -exec ls -lh {} \;'
# 应看到 3 个文件，分别在根 / vision/ / audio/ 下
```

---

## 4. 之后由我（WorkBuddy）在 dgx 完成的部分

权重就位后，告诉我「权重已到 `~/models/MiniCPM-o-4_5-gguf/`」，我会依次执行：

1. `bash ~/llama.cpp-omni/build_omni.sh` → 编译 `llama-omni-server`（aarch64 CPU）
2. `MODEL_DIR=~/models/MiniCPM-o-4_5-gguf bash ~/llama.cpp-omni/run_omni_server.sh` → 启动推理后端（端口 8080）
3. `python3 ~/llama.cpp-omni/omni_bridge.py` → 启动 bridge（端口 8081，收 base64 音频/图）
4. 把 `run_jarvis_dgx.py` 切到 OMNI 模式（native client 调 bridge）→ 端到端验证
   文本 / 视觉 / 音频三模态

---

## 5. 预期结果
- jarvis 文本对话：✅（已验证）
- jarvis 看屏幕：✅（截图→视觉已验证）
- jarvis 听声音：⬜ 待权重+编译后验证（omni server 路径已确认支持 `media_type=2`）
