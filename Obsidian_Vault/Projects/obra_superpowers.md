---
aliases: [superpowers]
tags: [AI, Trending, Shell, AI, Coding, Skills, SDLC, Vibe-Coding, Subagent]
stars: 268983
created_at: 2025-10-09
today_growth: 782
status: 热门（Agentic 技能框架 + 子代理驱动开发，五度上榜 #5）
date_accessed: 2026-08-08
---

# superpowers

**项目地址**：https://github.com/obra/superpowers
**作者**：obra
**⭐ 总 Star**：268,983（269.0k）  <!-- 2026-08-08 18:05 API 实时值；当日 08:25 为 268,738，08-07 为 268,415，08-06 为 267,669 -->
**📈 今日新增**：🔺782 stars（Vibe Coding #5；榜面值，**完整 24h 实测 +568（268,415→268,983），榜面高估 38%**）
**🍴 Fork**：23,998
**👁 Watch**：1,016
**💻 主要语言**：Shell
**📅 开源时间**：2025-10-09
**🔄 最近推送**：2026-08-08 00:13
**📜 许可证**：MIT

## 项目定位

一套**完整的编码 Agent 软件开发方法论**，构建于一组可组合技能（skills）加少量初始化指令之上，确保 Agent 主动使用它们。核心行为：当 Agent 感知到你在构建东西时，它**不会立刻写代码**，而是先退一步询问你真正想做什么；从对话中梳理出规格（spec）并以小块呈现供确认；确认后生成连「品味差、无判断力、讨厌测试」的初级工程师也能遵循的实现计划，强调真正的红/绿 TDD、YAGNI 与 DRY；随后分发给子代理并行实现。

## 技术栈

- 形态：纯 Markdown 技能文件 + 初始化指令
- 运行：Shell；兼容 Claude Code、Antigravity、Codex（App/CLI）、Cursor、Factory Droid、GitHub Copilot CLI、Kimi Code、OpenCode、Pi 等
- 方法学：子代理驱动开发（subagent-driven-development）、SDLC 全流程

## 外部链接

- GitHub：https://github.com/obra/superpowers
- 作者：https://github.com/obra
- 主题标签：ai, brainstorming, coding, obra, sdlc, skills, subagent-driven-development, superpowers

## 相关日期

- [[Vibe-Coding-2026-07-11|2026-07-11 日报]]（首入榜 #4，⭐251.8k / +1,013）
- [[Vibe-Coding-2026-07-30|2026-07-30 日报]]（二度上榜 #4，⭐263.6k / +616）
- [[Vibe-Coding-2026-08-06|2026-08-06 日报]]（三度上榜 #2，⭐267.7k / 🔺931）
- [[Vibe-Coding-2026-08-07|2026-08-07 日报]]（四度上榜 #5，⭐268.4k / 🔺858）
- [[Vibe-Coding-2026-08-08|2026-08-08 日报]]（五度上榜 #5，⭐268.7k / 🔺782）

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding / AI 编码 Agent 生态口径）。2026-07-11 首入榜（+1013，251.8k，Vibe Coding #4）。
- 2026-07-30 二度上榜（+616，263.6k，Vibe Coding #4），以纯 Markdown 技能 + 子代理驱动开发（subagent-driven-development）覆盖 Claude Code / Codex / Cursor / Copilot CLI / Kimi Code / OpenCode / Pi 等 11+ 主机，核心「先 spec、后红绿 TDD、再分发给子代理」已成事实标准方法论—— Skills 从「能力封装」走向「工程纪律封装」。
- 2026-08-06 三度上榜（🔺931，⭐267.7k，Vibe Coding #2）。08-05 曾是次席生态候选（+653）未入 Top 5，次日以第二名回归。**成长曲线**：2026-07-11 ⭐251,800 → 2026-07-30 ⭐263,643 → 2026-08-06 ⭐267,669。
- 形态始终是纯 Markdown 技能文件 + 少量初始化指令——没有 SDK、没有运行时，却撑起 26 万星。**「技能」这层的边际成本几乎为零，扩散速度天然快过任何需要安装的工具**，这解释了 7 月以来 `book-to-skill` / `reverse-skill` / `compound-engineering-plugin` / `agent-skills` / `superpowers` 反复霸榜的现象。
- 与 [[huangruiteng_loopx|LoopX]] 的分野：superpowers 管**单次任务内怎么干**（spec → 红绿 TDD → 子代理分发），LoopX 管**跨天跨回合怎么接**（目标/闸门/证据/配额）。
- **格式修复（2026-08-06）**：本页 YAML frontmatter 自建档起缺失闭合 `---`，Obsidian 无法解析其属性，本次一并修复。

### 2026-08-08 更新（五度上榜 #5）

- **成长曲线**：2026-07-11 ⭐251,800 → 07-30 ⭐263,643 → 08-06 ⭐267,669 → 08-07 ⭐268,415 → 08-08 ⭐268,738。榜面日增连续三日回落：931 → 858 → 782，**总量仍在爬，动量在缓慢衰减**。
- **技能层三足格局成型**：本项目（268.7k / 🔺782）与 [[mattpocock_skills|mattpocock/skills]]（208.8k / 🔺2,152）、[[addyosmani_agent-skills|addyosmani/agent-skills]]（83.9k / 🔺1,131）**同日占据 Top 5 三席，合计 56.1 万星、当日合计 🔺4,065**。昨日还是「双 20 万星」，今天 addyosmani 挤进来变成三足。
- **三家在「自由度」轴上的刻度**：mattpocock 给零件不管你怎么装 → addyosmani 给零件外加一张质检表 → superpowers 直接给你整条产线。**三者同时高增长，说明市场尚未选出唯一答案，但已确认「技能」这层要独立于 Agent 本体存在。**
- ⚡ **大厂开始进场**：同日 [google/skills](https://github.com/google/skills)（🔺327 / ⭐16.2k，Apache-2.0）列生态第 7。技能层此前全是个人开发者，Google 官方带自家产品线下场后，竞争逻辑会分岔——社区库拼通用工程手艺，厂商库拼「我家产品只有我最懂」。
- **反向样本**：今日 #1 的 [[PrimeIntellect-ai_prime-agent|prime-agent]] 把技能做成**可导入的 Python 包**（而非纯 Markdown），且内置 skill creator 自动沉淀。这是对「技能 = 纯 Markdown、零边际成本」这一主流形态的一次正面挑战。