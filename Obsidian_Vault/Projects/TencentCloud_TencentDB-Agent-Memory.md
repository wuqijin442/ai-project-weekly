---
aliases: [TencentDB-Agent-Memory, agent-memory]
tags: [AI, Trending, TypeScript, Memory, Agent, Vibe-Coding]
stars: 18478
created_at: 2026-04-07
weekly_growth: 8046
status: 热门（全赛道周榜 #2，本周 🔺8,046）
date_accessed: 2026-08-09
---

# TencentDB Agent Memory

**项目地址**：https://github.com/TencentCloud/TencentDB-Agent-Memory
**作者**：TencentCloud（腾讯云）
**⭐ 总 Star**：18,478（18.5k）  <!-- 2026-08-09 实时值；08-07 为 17,093 -->
**📈 本周新增**：🔺8,046 stars（全赛道周榜 #2）
**🍴 Fork**：1,533
**👁 Watch**：63
**💻 主要语言**：TypeScript
**📅 开源时间**：2026-04-07
**🔄 最近推送**：2026-08-06
**运行环境**：Node.js ≥ 22.16

## 项目定位

TencentDB Agent Memory 为 AI Agent 提供**完全本地化、零外部 API 依赖的长期记忆**能力，采用 4 级渐进式（4-tier progressive）记忆管线。它将"符号化短期记忆 + 分层长期记忆"结合，解决 Agent 在长程任务中上下文累积、token 爆炸、记忆扁平化的问题。

核心理念：拒绝扁平向量堆存储，拥抱"分层 + 符号化"。符号化短期记忆把繁重的工具调用日志压缩为紧凑的 Mermaid 符号，显著降低 token 消耗；分层长期记忆把碎片化对话提炼为结构化"人格（persona）"与"场景（scene）"。

**2026-08 定位升级**：官方描述已改写为「**团队级（team-level）AI Agent 记忆中枢**」——把对话、文档与代码转化为四类可治理、可共享、可跨 Agent/框架装配的记忆资产：

| 记忆资产 | 说明 |
|---------|------|
| **Chat Memory** | 会话记忆（短期符号化 + 长期人格/场景） |
| **Skill** | 可复用技能沉淀 |
| **LLM-Wiki** | 文档/知识结构化沉淀 |
| **Code-Graph** | **代码图谱**，直接切入编码 Agent 的代码理解底座 |

## 核心能力

- **符号化短期记忆**：工具日志 → 紧凑符号，降低 token 使用
- **分层长期记忆**：对话 → 结构化人格/场景，而非扁平向量堆
- **4 级渐进式管线**：渐进式蒸馏，上下文随任务推进持续优化
- **四类记忆资产治理**：Chat Memory / Skill / LLM-Wiki / Code-Graph 跨 Agent 共享与装配

## 基准表现（与 OpenClaw 集成）

| 记忆能力 | 基准 | OpenClaw | 接入插件 | 相对提升 |
|---------|------|---------|---------|---------|
| 短期 | WideSearch | 33% | 50% | +51.52% |
| 短期 | SWE-bench | 58.4% | 64.2% | +9.93% |
| 长期 | PersonaMem | 48% | 76% | +59% |

> 集成 OpenClaw 后：token 使用最高降低 **61.38%**，任务通过率相对提升 **51.52%**，PersonaMem 准确率从 48% 升至 76%。

## 技术栈

- **语言/运行时**：TypeScript / Node.js（≥ 22.16）
- **npm 包**：`@tencentdb-agent-memory/memory-tencentdb`
- **集成**：OpenClaw 插件、Hermes Gateway
- **核心能力**：Embedding、向量检索（vector-search）、本地优先（local-first）
- **许可证**：MIT

## 安装方式

```bash
npm install @tencentdb-agent-memory/memory-tencentdb
```

## 使用场景

- 为 AI 编程 Agent 提供跨会话的**长期记忆**，避免重复上下文
- 长程编码任务中的工具调用日志压缩与回忆
- 多 Agent 协作时的"人格/场景"一致性维护

## 外部链接

- GitHub：https://github.com/TencentCloud/TencentDB-Agent-Memory
- 文档：https://github.com/TencentCloud/TencentDB-Agent-Memory
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-07-09|2026-07-09 日报]]（首入榜，⭐7.6k / +318）
- [[Vibe-Coding-2026-08-04|2026-08-04 日报]]（二度上榜 #2，⭐12.6k / 🔺1,090）
- [[Vibe-Coding-2026-08-05|2026-08-05 日报]]（三度上榜 #2，⭐14.5k / 🔺1,111）
- [[Vibe-Coding-2026-08-06|2026-08-06 日报]]（四度上榜 #1，⭐15.6k / 🔺1,892，**今日最佳 🔝**）
- [[AI-Weekly-2026-08-09|2026-08-09 全赛道周报]]（周榜 #2，🔺8,046 / ⭐18.5k）

## 备注

- 本地优先（local-first），零外部 API 依赖，数据可控
- 已适配 OpenClaw 生态（OpenClaw ≥ 2026.3.13），并接入 Hermes Gateway
- **成长曲线**：2026-07-09 ⭐7,620 → 2026-08-04 ⭐12,622 → 2026-08-05 ⭐14,527 → 2026-08-06 ⭐15,566 → 2026-08-09 ⭐18,478（+8,046 本周，34 天 +142%，Fork 1,404 → 1,533）
- **日增在放大**：+1,090（08-04）→ +1,111（08-05）→ **+1,892（08-06）**。连续三日在榜且增速不降反升，08-05 判断的「扩散尚未见顶」得到证实；定位从「本地长期记忆插件」改写为「团队级记忆中枢」后，受众从个人开发者换成工程团队，是量级差异的来源
- 2026-08-06 首次登顶 GitHub 全站日榜第 1
- topics：`agent`、`ai-agent`、`embedding`、`llm`、`local-first`、`long-term-memory`、`memory`、`openclaw-plugin`、`vector-search`
