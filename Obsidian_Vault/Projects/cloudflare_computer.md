---
aliases: [Cloudflare Computer, computer, "@cloudflare/computer"]
tags: [AI, Trending, TypeScript, Agent-Runtime, Sandbox, Cloudflare, DurableObject, Vibe-Coding]
stars: 4171
created_at: 2026-06-05
today_growth: 891
status: 新星（首入榜 #3，PREVIEW ONLY）
date_accessed: 2026-08-06
---

# Cloudflare Computer

**项目地址**：https://github.com/cloudflare/computer
**作者**：cloudflare
**⭐ 总 Star**：4,171（4.2k）  <!-- 2026-08-06 18:00 实时值 -->
**📈 今日新增**：🔺891 stars
**🍴 Fork**：199
**💻 主要语言**：TypeScript
**📅 开源时间**：2026-06-05
**🔄 最近推送**：2026-08-05
**📜 许可证**：MIT

## 项目定位

一句话：**Give your agent a computer 👾**。

Cloudflare Computer 是一个**活在 Durable Object 里的虚拟文件系统**。Durable Object 用 SQLite 持有权威状态（authoritative state），并通过 `workspace.runtime` 暴露**唯一一个可插拔的执行面**。

它解决的是编码 Agent 的一个长期矛盾：给 Agent 真容器则贵、慢、状态难持久；给纯内存沙箱则跑不了真命令。Computer 的做法是**把「状态权威」与「在哪儿执行」彻底解耦**——文件系统是唯一真相源，执行后端是配置项。

> [!warning] PREVIEW ONLY
> 官方明确标注：仅供反馈用的预览版，API 不稳定、设计可能变更。适合实验、探索与原型，**当前不适合生产**。`docs/` 下的规范是前瞻性的，读它是为了理解意图，而非描述当前代码。

## 三种执行后端

| 后端 | 形态 | 特点 |
|------|------|------|
| **Container** | 沙箱容器 + 真实 FUSE 挂载 | 把 SQLite 状态投射进容器，沙箱侧守护进程 `computerd` 挂载为文件系统，通过 capnweb RPC 回同步。完整 Linux 用户态、真二进制、真网络 |
| **Isolate shell** | Dynamic Worker 跑 [just-bash](https://github.com/vercel-labs/just-bash) | 经 Workers RPC 直连权威 Workspace，**没有第二份存储、没有同步往返** |
| **Isolate JavaScript** | Dynamic Worker 跑 ESM 模块 | 结构化输入/输出、可持久化的相对导入、可配置库、Workspace 支撑的 `node:fs/promises`，以及受信的 `ws:git`、`ws:artifacts` 模块 |

一个 Workspace 可以在稳定 ID 下注册多个后端；`workspace.runtime.exec(source, { backend })` 是唯一执行入口，选中的后端决定 `source` 是 shell 命令还是 ESM 模块。后端在首次使用时惰性连接。Workspace 也可以**完全不带后端**构造，只当文件系统用。

## 技术栈

- **语言**：TypeScript
- **底座**：Cloudflare Durable Object + SQLite（权威状态）
- **同步协议**：capnweb RPC（容器侧 `computerd` ↔ DO）
- **执行**：Cloudflare Dynamic Worker（`env.LOADER`）、容器沙箱
- **仓库形态**：小型 monorepo，各 package 独立 README
- **许可证**：MIT

## 仓库结构

- `packages/dofs`（`@cloudflare/dofs`）— Durable Object SQLite 虚拟文件系统、同步协议构件
- `packages/computer`（`@cloudflare/computer`）— 对外主包，安装与入口映射见其 README
- `examples/` — 可运行的公共接口消费者，每个都是独立 Worker workspace

## 示例目录（examples/）

| 示例 | 说明 |
|------|------|
| `container` | 容器内跑 `computerd`，挂载 workspace，经 capnweb 与 DO 通信；提供 write/read/exec HTTP 接口 |
| `worker-shell` | 同样的 HTTP 接口，但 shell 是 Dynamic Worker 里的 just-bash，**无容器** |
| `worker-javascript` | 同上，`exec` 改为在 Dynamic Worker 中求值 ESM 模块 |
| `think` | `@cloudflare/think` 聊天 Agent，以 workspace 为工作目录，可从终端连入 |
| `think-compare-runtimes` | Web UI，把同一个 Agent 任务同时跑在容器与 Worker 两种运行时上对比 |
| `tutorial` | 分步搭建：一个端点、一个 Agent，在宿主写 Markdown 食谱卡，再在容器里跑 `pandoc` 生成 PDF |
| `artifacts` | 在 workspace 里生成 Worker 项目并发布到 Cloudflare Artifacts，成为可 clone 的仓库 |
| `assets` | Workers AI 把 prompt 变成图片写入 workspace，经 `@cloudflare/computer/assets` 返回可分享链接 |

## 使用场景

- 给编码 Agent 一个**状态持久、执行可替换**的工作目录
- 需要在"真容器"与"轻量 isolate"之间按成本/能力切换的 Agent 产品
- Agent 生成完整项目并直接发布为可 clone 仓库（见 `examples/artifacts`）
- 同一任务跨运行时做 A/B 对比（见 `examples/think-compare-runtimes`）

## 外部链接

- GitHub：https://github.com/cloudflare/computer
- 主包 README：`packages/computer/README.md`
- 规范文档：`docs/`（前瞻性，非当前实现描述）
- 贡献指南：`CONTRIBUTING.md` / `COLLABORATORS.md`
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-08-06|2026-08-06 日报]]（首入榜 #3，⭐4.2k / 🔺891）

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding / AI 编码 Agent 生态口径）
- 2026-06-05 开源，两个月内 ⭐4.2k，单日 +891 —— 大厂官方下场做 Agent 运行时的信号
- 与同日上榜的 [[TencentCloud_TencentDB-Agent-Memory|TencentDB Agent Memory]]（记忆层）、[[huangruiteng_loopx|loopx]]（控制面）构成互补：Computer 是"在哪儿干"的那一层
- 参照物：[[TencentCloud_CubeSandbox|TencentCloud/CubeSandbox]] 同属 Agent 沙箱赛道，但 Computer 的差异点在于**文件系统即权威状态**而非"沙箱即环境"
