---
aliases: [LoopX, loopx, 循环工程]
tags: [AI, Trending, Python, Agent-Ops, Control-Plane, Loop-Engineering, Codex, Vibe-Coding]
stars: 2531
created_at: 2026-05-31
today_growth: 326
status: 新星（首入榜 #5，loop agents early）
date_accessed: 2026-08-06
---

# LoopX

**项目地址**：https://github.com/huangruiteng/loopx
**作者**：huangruiteng
**⭐ 总 Star**：2,531（2.5k）  <!-- 2026-08-06 18:00 实时值 -->
**📈 今日新增**：🔺326 stars
**🍴 Fork**：181
**💻 主要语言**：Python（3.11+）
**📅 开源时间**：2026-05-31
**🔄 最近推送**：2026-08-06
**🌐 用户手册**：https://my.feishu.cn/wiki/CaL5wMk9ui17ngkWzeUcMlAYnZg
**📜 许可证**：MIT

## 项目定位

**长时程 AI Agent 工作的本地控制面（local control plane）**，作者称之为「循环工程（loop engineering）」的状态内核。

中文口号：**把会干活的 Agent，接成可管理、可复盘、可持续改进的数字员工。**
英文注脚：*Keep the loop moving. Keep the judgment human.*

它**不替代你的 Agent 运行时**。Codex / Claude Code / Cursor / 自研 runner 照常执行一个有界回合（bounded turn），LoopX 只负责把目标、闸门、待办、范围、证据、配额这套**耐久控制状态**收在一层里。

## 要解决的问题

一个 Agent 在单次会话里做完一件事不难。难的是长时程工作：

- 目标会变
- 需要人来拍板的决策会冒出来
- 证据会过期
- Agent 之间要交接
- **调度器在已经没有有效状态转移之后，还在继续烧钱**

作者的判断很直接：*Chat memory and a timer are not enough to govern that.*（聊天记忆 + 定时器治不了这个。）

## 控制循环

```text
objective / issue / project
   │
   ▼
LoopX state: objective + gates + todos + scope + evidence + quota
   │
   ├─ 需要人类判断？ ── 是 ─▶ 提一个具体问题，然后等
   │
   ├─ 有安全回退？ ──────▶ 跑一个有界的 agent 切片
   │
   ▼
Codex / Claude Code / Cursor / shell agent 执行一个回合
   │
   ▼
写证据 + 交接 + 下一个 todo ─▶ 由 quota 决定下一拍
```

心智模型是「**面向 Agent 的长时程看板（agent-native Kanban）**」：卡片携带身份、权限、证据与续接；移动是经过校验的算子（claim / gate / monitor / writeback）；看板只是投影，LoopX state 才是真相源。

注册的 Agent 之间是**对等（peers）**关系——由 claim、租约（lease）、任务边界、能力与类型化续接决定下一个谁动手，**不需要持久的 leader 身份**。

## 核心能力

- **durable goals**：跨回合持久的目标
- **gates**：owner / safety / publication / private-data 四类闸门
- **executable todos**：可执行待办
- **evidence logs**：证据日志，交接可审查
- **quota-aware auto-wake**：配额感知的自动唤醒，避免无效空转烧钱
- **verifiable handoffs**：可验证的交接

## 长跑证据（这是它区别于同类的地方）

README 给出两条 **200+ 小时实际循环生命周期**的公开轨迹（wall-clock 项目时间，非 200 小时连续模型执行）：

| 轨迹 | 说明 |
|------|------|
| **Open-Source Issue Fix** | 作者以 [OpenViking 贡献者](https://github.com/volcengine/OpenViking/pulls?q=is%3Apr+author%3Ahuangruiteng)身份跑的 200+ 小时公开贡献弧：PR 交付与可复用修复知识同步演化。Issue-Fix 能力把滚动仓库上下文、带修订戳的修复知识、面向 reviewer 的偏好三者分开保存 |
| **Auto ML Experiment** | 200+ 小时 owner 主导的实验弧 |

**不是一次性 demo**——这是它和大量「Agent 编排框架」的核心差别。

## 适用场景

- 多日的工程 / 研究 / benchmark / 实验目标
- 必须保留 scope、证据与评审状态的 issue 与 PR 循环
- 周期性心跳或监控类工作
- 带 owner / 安全 / 发布 / 私有数据闸门的项目
- 有归属、租约与交接需求的对等 Agent 团队
- 需要让非工程背景的运营方也能看懂进度的创作 / 研究 / 运营工作流

> [!warning] 边界声明
> LoopX **不是自主生产控制器**。危险权限、发布、生产写入与最终归属，都留给人。

## 技术栈

- **语言**：Python 3.11+，**运行时无标准库以外依赖**
- **环境要求**：`curl`、`tar`，macOS 或 Linux shell（Git 仅贡献者 clone/canary 流程需要）
- **形态**：本地优先（local-first）控制面，与 Agent 循环无关（agent-loop agnostic）
- **topics**：`agent-control-plane`、`agent-ops`、`ai-agents`、`codex`、`long-running-agents`、`loop-engineering`、`loopx`、`workflow-automation`
- **许可证**：MIT

## 快速上手

免 clone 安装：

```bash
curl -fsSL https://raw.githubusercontent.com/huangruiteng/loopx/main/scripts/install-from-github.sh | bash
export PATH="$HOME/.local/bin:$PATH"
loopx doctor
```

在项目根目录接入：

```bash
cd /path/to/your-project
loopx connect
loopx status
```

若项目尚未初始化，`connect` 会提示 state 缺失，改走引导路径：

```bash
loopx start-goal --guided --project . --goal-text "Your long-running objective"
```

> LoopX 应复用既有 state 而非覆盖。记得把 `.loopx/`、`.codex/goals/`、`.local/` 加入 ignore。

## 宿主接入方式

| 宿主 | 推荐启动 | 循环驱动 |
|------|---------|---------|
| **Codex App** | 让 Agent 连接项目、跑 `loopx doctor`、保留既有 state 并汇报当前 gate 与下一个 todo；随后 `$loopx <task>` 或从 `/skills` 选 `loopx` | Codex App 心跳自动化，由 `quota should-run.scheduler_hint` 刷新 |
| **Codex App over SSH** | `loopx agent-onboard --agent-type codex-app-ssh --project .` | 返回的可见 `/goal <task_body>` |
| **Codex CLI** | 项目内启动 `codex`，让它连接并诊断 LoopX，然后 `$loopx <task>` 或 `/skills` | 可见 `/goal`；默认无隐式 headless 执行 |
| **Claude Code** | 装 opt-in 适配器，`/loopx <task>` 后接 `/loop` | 原生 `/loop`，由 LoopX 门控 |
| **OpenCode** | 装静态命令外观；周期目标需 `--with-goal-bridge` | 命令外观 + 显式 goal bridge |
| **Pi** | `loopx slash-commands --install --surface pi`，可信会话内 `/loopx <task>` | Pi goal 扩展，受 LoopX 配额门控 |
| **Cursor / shell / 自研 runner** | 装完跑 `loopx doctor`，手动接入或从 runner 调 LoopX | 你自己的 shell / 调度器 / runner |

## 外部链接

- GitHub：https://github.com/huangruiteng/loopx
- 官网：https://huangruiteng.github.io/loopx/
- 文档：https://huangruiteng.github.io/loopx/docs/
- 用户手册（飞书）：https://my.feishu.cn/wiki/CaL5wMk9ui17ngkWzeUcMlAYnZg
- 中文 README：`README.zh-CN.md`
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-08-06|2026-08-06 日报]]（首入榜 #5，⭐2.5k / 🔺326）

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding / AI 编码 Agent 生态口径）
- 状态标注 `loop agents early`，仍在早期
- 与同日上榜的 [[cloudflare_computer|cloudflare/computer]]（运行时）、[[TencentCloud_TencentDB-Agent-Memory|TencentDB Agent Memory]]（记忆层）分属不同层：LoopX 是「谁在干、干到哪、什么时候停」的控制面
- 与 [[obra_superpowers|superpowers]] 的分野：superpowers 管**单次任务内怎么干**（spec → TDD → 子代理），LoopX 管**跨天跨回合怎么接**
