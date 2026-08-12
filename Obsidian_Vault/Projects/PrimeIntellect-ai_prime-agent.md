---
aliases: [Prime Agent, prime-agent, Prime Intellect Agent]
tags: [AI, Trending, TypeScript, Coding-Agent, RLM, Self-Improving, Long-Running, PrimeIntellect, Vibe-Coding]
stars: 14185
created_at: 2026-05-08
today_growth: 1138
status: 5度上榜
date_accessed: 2026-08-12
---

# Prime Agent

**项目地址**：https://github.com/PrimeIntellect-ai/prime-agent
**作者**：PrimeIntellect-ai（Prime Intellect）
**⭐ 总 Star**：13,541（13.5k）  <!-- 2026-08-11 17:5x API 实时值；08-10 为 12,346 -->
**📈 今日新增**：🔺2,642 stars（榜面值；**三天净增 +6,195（7,346→13,541，+85%），日均 ≈2,065，与榜面吻合**）
**🍴 Fork**：1,248
**💻 主要语言**：TypeScript
**📅 开源时间**：2026-05-08
**🔄 最近推送**：2026-08-08 00:24
**📜 许可证**：MIT

## 项目定位

一句话：**Prime Agent: A Self-Improving RLM Agent**。

一个面向**通用与长时任务**的开源编码 / 研究 Agent。它不是"再做一个终端里的 Claude Code"，而是围绕两个抽象重新定义了 Agent 的执行模型：

1. **RLM（Recursive Language Model）** — 把上下文当变量（*prompt-as-a-variable*），把工具和递归子代理当函数调用（*programmatic tool / sub-agent calling*），全部发生在一个**持久化 REPL** 里。
2. **Continual Harness** — 把补充提示词、记忆、技能描述、可复用子代理规格存成**耐久状态**，Agent 可以通过小步、有证据支撑的更新去精炼它。默认作用域局限于当前会话。

组合起来：**持久 Python 控制环境 + 耐久 harness 状态**，让有用的工作上下文和可复用的操作模式**活得比一个聊天窗口更久**。

## 六个核心设计

| 设计 | 说明 |
|------|------|
| **一切皆可编程** | 持久 IPython 是内置的模型工具；文件操作、shell 命令、工具调用、子代理、上下文管理**全部通过写代码完成** |
| **子代理内建** | `rlm(...)` 直接派生真实子 Agent 做并行 / 后台工作，结果以程序化方式返回 |
| **Harness 可自我改进** | `/refine` 审查当前轨迹，对补充 harness 状态施加小步、有证据的更新；**永不重写不可变的基础系统提示**，并记录快照以支持回滚 |
| **技能是可执行的** | 技能即可导入的 Python 包；内置 skill creator 能把重复工作流沉淀为项目级或个人级技能 |
| **会话后台常驻** | daemon 托底，终端断开后 Agent 继续运行，之后可 reattach |
| **Agent 直接互通** | 运行中的 Agent 之间可互相发现、交换消息、彼此编排，无需事事绕回用户 |

## 长时任务能力

- **Continual Harness**：`/refine` 把聚焦、可评审的经验持久化为补充提示 / 记忆 / 可复用技能描述 / 子代理规格，带精炼历史。官方明确它**不替代**打包与评审新的可执行技能。
- **Agent 间直连通信**：运行中的 Agent 与保留的子代理能互相发现、交换消息、引导彼此的活跃工作。
- **Daemon 连续性**：活跃会话、IPython 状态、定时任务、子代理在终端 detach 后继续存活，可再 attach。
- **心跳与调度**：`/heartbeat`、`rlm_heartbeat`、`prime-agent schedule` 可周期性或定时重新进入会话。
- **持久目标**：`/goal` 让目标及其进度跨轮次存活，直到完成 / 暂停 / 清除。
- **有界自治模式**：`/autonomous` 在配置的轮次、token、时间预算内继续推进，可运行用户定义的质量门禁。官方措辞很克制：*"A passed gate checks only what that gate verifies; reaching a limit does not imply task success."*

## 技术栈

- **语言**：TypeScript（TUI / CLI 层）+ Python（IPython 运行时、技能包）
- **控制环境**：持久化 IPython 内核
- **进程模型**：daemon / worker / kernel 三层，带持久化边界
- **TUI 底座**：构建于 [[earendil-works_pi|earendil-works/pi]] 之上（官方致谢）
- **配套项目**：[verifiers](https://github.com/PrimeIntellect-ai/verifiers)、[PRIME-RL](https://github.com/PrimeIntellect-ai/prime-rl)
- **理论基础**：[RLM 博客](https://www.primeintellect.ai/blog/rlm)、[Continual Harness 论文 arXiv:2605.09998](https://arxiv.org/abs/2605.09998)
- **许可证**：MIT

## 安装与使用

macOS / Linux：

```bash
curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh
```

安装器会下载带版本的 release、校验 SHA-256、安装 `prime-agent` 命令，并可准备 IPython 运行时。

```bash
cd /path/to/project
prime-agent                          # 在当前目录启动，首次运行 /login 选择订阅或 API-key 提供方
prime-agent agents                   # 浏览运行中 / 空闲 / 已保存的会话
prime-agent attach <agent>           # 重新接入运行中的会话
prime-agent --resume <path|id>       # 恢复已保存会话
prime-agent status                   # 检查后台服务状态
prime-agent doctor [--fix]           # 检查或修复后台服务
prime-agent update [--force]         # 更新
prime-agent shutdown [--force]       # 停止全部 Agent、worker 与后台服务
```

> [!warning] 不是安全沙箱
> Prime Agent **以你的用户权限执行模型生成的 Python 与项目命令**。其 worker 与 kernel 进程改善的是生命周期隔离与恢复能力，**不是安全沙箱**。官方建议：使用一次性 clone、干净 worktree 或可检查可恢复的检查点；只使用可信仓库、指令、技能与扩展；不可信代码请放到外部沙箱运行。

## 与同赛道项目的差异

| 维度 | Prime Agent | 主流终端编码 Agent |
|------|-------------|-------------------|
| 工具调用 | 写 Python 代码（持久 IPython 即唯一内置工具） | JSON schema tool calling |
| 子代理 | `rlm(...)` 程序化派生、结果可编程消费 | 多为固定编排或外部框架 |
| 记忆 | Continual Harness：存**工装本身**（提示/技能/子代理规格），`/refine` 小步演进 | 多为向量库存对话 |
| 自我改进边界 | 基础系统提示不可变，仅改补充层，带快照回滚 | 通常无此边界定义 |
| 长时任务 | daemon 常驻 + 目标 / 心跳 / 调度 / 有界自治 | 多依赖用户保持终端 |

## 使用场景

- 研究评测（evaluation）等**长时、需断点续跑**的工作
- 需要多 Agent 并行且彼此协调的任务分发
- 希望 Agent 把重复工作流自动沉淀为可执行技能的团队
- 需要"跑一夜"的自治任务，且要求预算上限与质量门禁

## 外部链接

- GitHub：https://github.com/PrimeIntellect-ai/prime-agent
- 文档索引：`packages/coding-agent/docs/index.md`
- Quickstart：`packages/coding-agent/docs/quickstart.md`
- RLM 编程模型：`packages/coding-agent/docs/rlm.md`
- 长时/后台 Agent：`packages/coding-agent/docs/long-running-agents.md`
- 架构总览：`packages/coding-agent/docs/architecture.md`
- 官网：https://primeintellect.ai
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-08-08|2026-08-08 日报]]（首入榜 #1，⭐6.5k / 🔺2,293，**今日最佳 🔝**）
- [[Vibe-Coding-2026-08-10|2026-08-10 日报]]（蝉联 #1，⭐12.3k / 🔺2,356，**今日最佳 🔝**）
- [[Vibe-Coding-2026-08-11|2026-08-11 日报]]（三度蝉联 #1，⭐13.5k / 🔺2,642，**今日最佳 🔝**）

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding / AI 编码 Agent 生态口径）
- 2026-05-08 开源，三个月 ⭐6.5k；**2026-08-08 首次进入 Trending 日榜即登顶 Vibe Coding #1**
- ⚠️ 昨日（08-07）未在榜面，无 API 快照基线，🔺2,293 **仅由榜面支撑，建议下期复核实测增量**
- 与 [[earendil-works_pi|pi]] 的关系：TUI 与 Agent 层构建于 pi 之上，pi 曾于 2026-07-20 上榜
- 与今日同榜项目的分层关系：它把**记忆层（Continual Harness）、控制面（goal/heartbeat/autonomous）、运行时（daemon）一并内建**，与 [[cloudflare_computer|cloudflare/computer]]（外置运行时）、[[TencentCloud_TencentDB-Agent-Memory|TencentDB Agent Memory]]（外置记忆）、[[huangruiteng_loopx|loopx]]（外置控制面）构成**「一体化」对「组件化」**的路线对照

## 反向链接
- [[Daily/Vibe-Coding-2026-08-12.md|2026-08-12 收录]]
