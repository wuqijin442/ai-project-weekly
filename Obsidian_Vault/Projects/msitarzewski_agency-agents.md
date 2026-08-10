---
aliases: [msitarzewski/agency-agents, agency-agents]
tags: [AI, Trending, Shell, Vibe-Coding, Role-Agent, Multi-Agent]
stars: 141304
created_at: 2025-10-13
today_growth: 858
status: 活跃（角色/子代理层，2026-08-10 Vibe Coding #2）
date_accessed: 2026-08-10
---

# msitarzewski/agency-agents

**项目地址**：https://github.com/msitarzewski/agency-agents
**作者**：msitarzewski
**⭐ 总 Star**：141,304（141.3k）  <!-- 2026-08-10 18:1x API 实时值 -->
**📈 今日新增**：🔺858 stars（榜面值；**相对自身 36 天日均 ≈396 翻 2.2 倍，真异动非存量惯性**）
**🍴 Fork**：23,049
**👁 Watch**：1,050
**💻 主要语言**：Shell
**📅 开源时间**：2025-10-13
**🔄 最近推送**：2026-08-06
**📜 许可证**：MIT

## 项目定位

一句话：**一整间「AI 代理公司」装进你的终端**。

与「技能库」（教 Agent 怎么干活）和「执行体」（Agent 本体会干活）都不同，agency-agents 卖的是**角色 / 人格层**：它把一支虚拟 agency 的每一个职能岗做成独立的、带性格、带工作流、带交付物、带成功指标的专家型子代理（*specialized expert with personality, processes, and proven deliverables*）。从 frontend wizards 到 Reddit community ninjas，从 whimsy injectors 到 reality checkers，按**部门编制**（Engineering / Design / Marketing / Product / Security…）成一支完整花名册。

它解决的是「我有 Agent 本体，但没人告诉我该派谁去干哪一类活」这件事——是 Vibe Coding 分层图里的**角色层**。

## 安装

```bash
# 跨平台原生 App 一键安装到多家宿主
./scripts/install.sh --tool cursor
./scripts/install.sh --tool aider
./scripts/install.sh --tool copilot
# 已支持 Claude Code、Cursor、Codex、Gemini、Osaurus 等 13+ 宿主
```

## 与同榜项目的分层关系

今日 Top 5 里它是「派谁去干」那一层，与其余两层正交：

| 层 | 项目 | 封装单位 |
| --- | --- | --- |
| 执行体 | [[PrimeIntellect-ai_prime-agent\|prime-agent]] | 动手的那个（#1） |
| **角色层** | **agency-agents（#2）** | **派谁去干（人格 + 工作流 + 交付物）** |
| 技能层 | [[addyosmani_agent-skills\|agent-skills]]（#3）、[[google_skills\|google/skills]]（#4） | 用什么招（纪律 / 产品知识） |
| 控制面 | [[pingdotgg_t3code\|t3code]]（#5） | 人怎么盯 |

三者可同时装载、互不替代：一个「后端架构师」角色（本仓库）+ 一套「测试不可跳过」纪律（agent-skills）+ 一包「GKE Inference 迁移」产品知识（google/skills）。

## 规模与成长

- **141.3 万⭐** 是今日榜上最大的存量项目，2025-10 开源，靠一个 Reddit 帖子起家。
- 今日 🔺858 相对自身日均（≈396）翻 2.2 倍，为真异动。
- Fork 23,049、Watch 1,050，社区黏性极高。

## 技术栈

- 形态：按部门编制的子代理花名册 + 跨宿主安装脚本
- 主要语言：Shell（安装 / 编排逻辑）
- 支持宿主：Claude Code、Cursor、Codex、Gemini、Osaurus 等 13+
- 许可证：MIT

## 外部链接

- GitHub：https://github.com/msitarzewski/agency-agents

## 相关日期

- [[Vibe-Coding-2026-08-10|2026-08-10 日报]]（#2，⭐141.3k / 🔺858，角色层入选）

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding 生态扩充命中：角色 / 子代理层，属「编码 Agent 配套」细分；严格关键词未命中——topics 为空、简介无关键词，且现行判定不含 README，故即便 README 列出支持 cursor/aider/copilot 也不计严格命中）。
- 2026-07-05 首次归档为周报索引（当时 ⭐127,033，weekly_growth 10,976）；本期由存根升级为完整页，更新 08-10 实时 star / 今日增量 / 回链。
- 当前定位：Vibe Coding 分层图「角色层」代表，与 prime-agent（执行体）、agent-skills（技能层）、t3code（控制面）构成四层对照。
