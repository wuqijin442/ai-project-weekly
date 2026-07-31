# pub-local-jarvis 项目分析

> 仓库：https://github.com/LYiHub/pub-local-jarvis
> 本地路径：`cloned_projects/pub-local-jarvis`
> 克隆方式：git clone --depth 1（最新单提交 `dd8fbf9`，2026-07-24）
> 许可证：MIT（模型权重不随仓库分发）
> 版本：0.1.2（早期阶段）

---

## 1. 项目定位

**AI Jarvis（本地贾维斯）** 是一款面向 **64 位 Windows 10/11** 的「本地优先」桌面 AI 助手。核心卖点：

- 持续理解**屏幕画面（DXGI）** + **系统音频（WASAPI）**
- 基于本地多模态模型 **MiniCPM-o 4.5** 做全双工推理，数据默认不上云
- 以**桌宠气泡 / 游戏弹幕 / 课程笔记**等形式输出帮助
- 模型每秒接收约 1 帧画面 + 最近 1 秒音频，自主在 `LISTEN`（继续观察）与 `SPEAK`（说一句）间切换——非传统一问一答

适用场景：桌面陪伴、主动对话（Ctrl+M）、游戏陪伴（透明弹幕、点击穿透）、网课记录（自动生成 Markdown 笔记）、本地记忆（活动时间线/每日总结）、可视化日程图（可选联网）。

---

## 2. 技术架构（三层，全本机）

| 层 | 技术栈 | 职责 |
|---|---|---|
| **Electron 桌面端** `desktop/` | Node.js + Electron + Svelte/Vanilla JS + HTML/CSS | 启动入口、桌宠窗口、弹幕层、系统托盘、配置 UI、通知 |
| **Python 后端** `src/jarvis_backend/` | FastAPI + Pydantic v2 + uvicorn | 场景编排、交互策略、本地记忆、课程会话、HTTP/WS API |
| **C++20 原生 Worker** `native/` | C++20 + llama.cpp-omni/ggml | Windows 屏幕/音频采集、模型加载、多模态推理 |
| 第三方运行时 | `third_party/runtime/`（llama.cpp-omni 固定上游版本） | 提供 MiniCPM-o GGUF 本地推理能力 |

后端默认仅监听 `127.0.0.1:8000`，不对外暴露；可选 Bearer Token。

### 数据流（来自 README）
```
DXGI 屏幕画面 + WASAPI 系统音频
        |
        +-- 结构化感知上下文 -> 场景 / 游戏 / 课程 / 记忆
        |
        +-- 全双工上下文     -> LISTEN / SPEAK -> 模型回复
```
两套上下文隔离；结构化场景判断不能生成普通气泡，避免越权。

---

## 3. 代码规模与语言分布

仓库总文件 3276，但**大部分是 vendored 的 llama.cpp-omni 源码**（CUDA 内核 `.cu` / OpenCL `.cl` / WGSL / GLSL 等）。**第一方代码量约 1.55 万行**：

| 语言 | 文件数 | 行数 | 说明 |
|---|---|---|---|
| Python | 39 | **8,036** | 后端编排，模块粒度小、职责清晰 |
| JavaScript | 35 | **3,887** | Electron 主进程 + 各 UI 渲染脚本 |
| C++ (cpp+hpp) | 22 | **3,640** | 原生采集/推理 Worker |
| （vendor 内）cu/cl/comp/wgsl… | 数百 | — | 第三方 GPU 内核，未计入自研 |

> 结论：这是一个**真实可编译、工程化完整**的项目，不是 demo。三层分离清晰，有配置中心（`config/default.toml`）、测试（`tests/unit`）、打包脚本（`start-real.ps1` 51KB，NSIS 安装包、`verify:installer`）。

---

## 4. 关键模块拆解

### Python 后端 `src/jarvis_backend/`
- `app.py`：FastAPI 装配；按 `native.mode`（`fake`/`process`）选择内嵌 or 命名管道客户端——**支持无原生二进制的 fake 模式**，便于 CI/开发调试。
- `orchestrator/`：`service.py` + `lifecycle.py` + `scene.py` + `events.py`——编排核心，场景状态机（进入/退出阈值、采样数在 `default.toml` 可配）。
- `native/`：`client.py`（两种客户端）、`protocol.py`（信令协议）、`supervisor.py`（进程看护）。
- `barrage/policy.py`：游戏弹幕候选生成、去重、频率控制。
- `courses/core.py`：网课关键帧选取（清晰度/信息密度/独立复习价值）+ 知识点归纳。
- `memory/`：`store.py`（本地记忆时间线）+ `image_generation.py`（可选的日程图，仅主动生成时联网）。
- `api/`：`routes.py`（REST）+ `ws.py`（事件流）+ `schemas.py`。

### C++ 原生 `native/`
- `windows/dxgi_capture.cpp`：屏幕采集
- `windows/wasapi_capture.cpp`：系统音频采集
- `windows/named_pipe_server.cpp`：与后端通信（管道 `\\.\pipe\AIJarvis.Worker.v1`）
- `omni_runtime.cpp` / `runtime.cpp`：加载 MiniCPM-o GGUF 并推理
- `scheduler.cpp` / `worker.cpp`：调度与 worker 主循环
- `fingerprint.cpp`：场景证据指纹（用于游戏/课程判定）

### Electron 桌面 `desktop/src/`
- `main.js` / `preload.js` / `backend-manager.js`：启动与后端生命周期
- `pet-*.js`：桌宠显示、拖拽、命中测试、状态
- `barrage-overlay.js` / `scene-policy.js` / `game-profiles.js` / `privacy-mode.js`：交互层
- `ui/`：Svelte/HTML 渲染的 launcher、pet、barrage 界面

---

## 5. 运行与构建

**环境要求（源码）**：Python ≥3.12、Git、CMake ≥3.24、VS2022 C++ Build Tools、Node LTS；可选 NVIDIA 显卡 + CUDA 12.8+。
**终端用户（安装包）**：内置冻结 Python + 预编译 x64 CPU 运行时，无需工具链；CPU 需 AVX2；首次下载约 **6.32 GiB** MiniCPM-o 4.5 模型（断点续传+校验）。

启动：`cd desktop && npm run deps:install && cd .. && .\start-real.cmd`
构建安装包：`cd desktop && npm run build` → `desktop/dist/AI-Jarvis-Setup-<ver>-x64.exe`

**关键设计点**：
- 配置驱动（`config/default.toml`）：场景阈值、冷却时间、弹幕频率、记忆窗口全部可调，工程规范度高。
- `fake` 原生模式让后端可脱离庞大 C++/CUDA 编译单独跑起来，利于测试与 CI。
- 提供 `verify:installer` 隔离安装自包含校验，发布质量意识强。

---

## 6. 隐私与安全设计（可借鉴）

- 原始画面/音频**仅用于即时推理**，不长期持久化；长期记忆只存抽象活动，不存截图/音频。
- 隐私模式：双击桌宠暂停/恢复采集，暂停后清理采集对象。
- 后端默认绑定 `127.0.0.1`，可选 Bearer Token。
- 联网仅限「主动生成日程图」时提交当日回顾 + 两张参考图到用户自配图像 API；API Key 走系统安全存储。
- 游戏弹幕明确**不控制游戏**、不按游戏名硬编码分支，所有游戏共用证据/候选/去重链路——边界与可扩展性设计合理。

---

## 7. 亮点与可借鉴点

1. **本地全双工多模态**：屏幕+音频联合理解，模型自主决定何时介入，比「截图+问答」更接近「桌面智能体」。
2. **三层解耦 + fake 模式**：工程化成熟，便于分层开发与测试。
3. **配置驱动的场景状态机**：阈值/采样数/冷却可配，避免硬编码。
4. **隐私优先**：采集即弃 + 抽象记忆，符合本地优先叙事。
5. **完整发布链路**：NSIS 安装包 + 自包含校验，非玩具项目。

---

## 8. 局限与风险

- **平台绑定严重**：DXGI/WASAPI 仅 Windows；C++ 原生层无法跨平台，macOS/Linux 不可用。
- **模型权重不随仓库**：首次需下载 6.32 GiB，且 MiniCPM-o 商用需单独确认许可。
- **早期版本（0.1.2）**：能力边界明确——无语音播报/实时语音、游戏不代操作、课程总结依赖转写质量。
- **重依赖 vendored llama.cpp-omni**：上游固定，GPU 内核体积大，跟踪上游安全更新成本高。
- **构建门槛**：完整安装包需 CUDA Toolkit 13.x，纯 CPU 回退下首帧感知可能慢至数十秒~分钟。

---

## 9. 与本项目（AI Project Weekly）的关联

- 可作为「本地优先 AI 应用架构」的参考样本：Electron + Python FastAPI + C++ 原生推理的三层模板。
- `fake` 原生模式、配置驱动的场景状态机、发布自包含校验，均是可复用的工程实践。
- 纳入 `cloned_projects/` 已 gitignore，不进入 GitHub 同步。

---
*生成时间：2026-07-31 · 基于 --depth 1 克隆的最新提交分析*
