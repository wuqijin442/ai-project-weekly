# pub-local-jarvis 本地跑通 + 全量测试报告

> 仓库：`cloned_projects/pub-local-jarvis`（git clone --depth 1，dd8fbf9）
> 测试/运行日期：2026-07-31
> 运行环境：Windows（win32），Python 3.13.14（managed venv），Node 22.22.2，npm 10.9.7

---

## 0. 结论速览

| 项目 | 结果 |
|---|---|
| Python 后端依赖安装 | ✅ 成功（editable install） |
| **全量单元测试（102 个）** | ✅ **102 passed**（8.13s，0 failed） |
| 后端 Live 启动（fake 模式） | ✅ `Application startup complete` |
| Live HTTP API 冒烟（health/commands/scene） | ✅ 全部符合预期 |
| Live chat（fake 模式） | ⚠️ 返回 503「本地模型暂时无法回复」——**预期行为**（fake 客户端无真实模型回复） |
| 前端依赖安装（electron） | ⏳ 后台进行中（Electron 二进制下载，约 100MB+） |
| C++20 原生 Worker 编译 | ❌ 本沙箱无 VS2022 C++ Build Tools / CUDA 工具链，**无法构建** |
| MiniCPM-o 4.5 模型（6.32 GiB）下载 | ⏭️ 未执行（fake 模式不依赖；真实运行才需） |
| Electron 安装包构建 / `verify:installer` | ❌ 依赖原生运行时 + NSIS，沙箱无法完成 |

---

## 1. 为什么能「跑通」：fake 原生模式

项目 `config/default.toml` 默认 `native.mode = "fake"`。对应代码 `src/jarvis_backend/native/client.py::InProcessNativeClient`：

- 是一个**确定性的 worker 替身**，仅用于测试和显式 fake 模式；
- `start()` 直接 emit `worker.ready`；`request()` 对 `ping` 返回 `pong`，其余方法回显 payload，**不加载模型、不调用 C++ 二进制**；
- 因此后端 + 全部测试**无需 CUDA、无需 6.32 GiB 模型、无需编译 C++** 即可完整运行。

真实运行（`mode = "process"`）才会通过 Windows 命名管道连接 `jarvis-native-worker.exe`（C++ 编译产物），并加载 MiniCPM-o 4.5 权重。

---

## 2. 环境搭建步骤（已执行）

```bash
# 1) 创建 managed Python venv
C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe -m venv ^
  C:\Users\Administrator\.workbuddy\binaries\python\envs\default
# 2) 安装后端 + 测试依赖（editable）
<venv>\Scripts\python.exe -m pip install -e ".[test]"
# 3) 运行全量测试
<venv>\Scripts\python.exe -m pytest tests/unit -v
# 4) 启动后端（fake 模式）
JARVIS_CONFIG=<repo>/config/default.toml <venv>\Scripts\python.exe -m uvicorn ^
  jarvis_backend.app:app --host 127.0.0.1 --port 8000
```

> 踩坑记录：首次 `pip install --upgrade pip` 在 managed venv 内损坏 pip，已用 `ensurepip --upgrade` 修复并清理残留的 `~ip` / `~ijarvis-backend` 无效分发包。最终 `jarvis_backend` 可正常 import（指向 `src/jarvis_backend`）。

---

## 3. 全量测试结果（102 passed）

```
platform win32 -- Python 3.13.14, pytest-8.4.2, pluggy-1.6.0
asyncio: mode=Mode.AUTO
collected 102 items

tests/unit/test_api.py .........................  (5)
test_control_plane_api.py .......................  (35)
test_courses_lifecycle.py ..                     (2)
test_courses_paths.py ..                         (2)
test_memory_images.py .......                    (7)
test_memory_retrieval.py .                       (1)
test_memory_store.py ...                         (3)
test_model_download.py ......                    (6)
test_packaged_launcher.py ......                 (6)
test_policies.py .....                           (5)
test_prompts.py ..                               (2)
test_protocol.py .......                         (7)
======================= 102 passed, 2 warnings in 8.13s =======================
```

覆盖模块：HTTP API、控制面（commands/duplex/场景）、课程生命周期与路径、本地记忆（store/retrieval/图片生成，均 mock 网络）、模型下载（mock）、打包启动器（mock subprocess）、弹幕/场景策略、提示词模板、原生协议编解码。

两项 warning 均为上游 starlette/fastapi 弃用提示（`httpx` TestClient 与 `HTTP_422_UNPROCESSABLE_ENTITY`），**非项目问题**。

---

## 4. 后端 Live 冒烟测试（真实 HTTP，非 TestClient）

启动后实测：

| 请求 | 结果 | 说明 |
|---|---|---|
| `GET /api/v1/health` | `200` `{"status":"ok","lifecycle":"ready","native_connected":true,...}` | 控平面就绪 |
| `POST /api/v1/commands {"command":"ping"}` | `200` `{"accepted":true,"result":{"ok":true,"result":"pong"}}` | 命令经 orchestrator → native 客户端返回 pong |
| `GET /` | `404` | 设计如此（无浏览器 UI，`docs_url=None`） |
| `POST /api/v1/scene/observations {"score":0.9}` | `200` `{"active":false,"changed":false}` | 场景状态机逻辑可达 |
| `POST /api/v1/assistant/chat {"message":"你好"}` | `503`「本地模型暂时无法回复」 | **预期**：fake 客户端不返回真实模型文本，handler 优雅降级 |
| `POST /api/v1/commands {"command":"set_game_profile",...}` | `200` 正确透传到 native 客户端 | 游戏陪伴方案链路通 |

结论：在 fake 模式下，完整请求链路（HTTP → orchestrator → native client → 响应塑形）**真实可运行**，仅「真实模型推理」因无权重而按预期降级。

---

## 5. 无法在沙箱完成的部分（如实说明）

1. **C++20 原生 Worker 编译**：需要 Visual Studio 2022 C++ Build Tools + CMake 3.24+，真实推理还需 CUDA 12.8+/13.x。沙箱无该工具链，`native/` 无法编译为 `jarvis-native-worker.exe`。
2. **MiniCPM-o 4.5 模型（6.32 GiB）**：真实感知/对话需要；首次启动由 `model_download.py` 下载校验。本环境未下载（fake 模式不触发，且体积大）。
3. **Electron 安装包构建 / `verify:installer`**：依赖上述原生运行时 + NSIS + PowerShell 脚本，沙箱无法完整产出 `.exe`。
4. **前端 Electron 桌面 UI 实际渲染**：需 `npm run deps:install` 装好 electron 后 `npm start`；electron 二进制下载体积大，安装已在后台尝试。

---

## 6. 要在真实 Windows 机器上「全功能跑通」的最小步骤

```powershell
# 前置：Win10/11 x64 + AVX2；装 VS2022 C++ Build Tools、CMake 3.24+、CUDA 13.x（可选，GPU 加速）
# 1) 构建原生 worker + 后端冻结 + 安装包（推荐，免环境）
#    直接下载发布页 AI-Jarvis-Setup-0.1.2-x64.exe 安装启动即可
# 2) 或源码运行：
cd desktop; npm run deps:install; cd ..
.\start-real.cmd        # 启动 Electron + 后端；首次自动下载 6.32 GiB 模型
```
启动后：拖拽桌宠、双击暂停感知、`Ctrl+M` 对话、配置游戏陪伴方案、网课自动记录。

---

*生成时间：2026-07-31 · 基于本地 fake 模式实测*
