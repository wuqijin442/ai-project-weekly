---
aliases: [superpowers]
tags: [AI, Trending, Shell, AI, Coding, Skills, SDLC, Vibe-Coding, Subagent]
stars: 268415
created_at: 2025-10-09
today_growth: 858
status: 热门（Agentic 技能框架 + 子代理驱动开发，四度上榜 #5）
date_accessed: 2026-08-07
---

# superpowers

**项目地址**：https://github.com/obra/superpowers
**作者**：obra
**⭐ 总 Star**：268,415（268.4k）  <!-- 2026-08-07 18:00 实时值；08-06 为 267,669 -->
**📈 今日新增**：🔺858 stars（Vibe Coding #5；榜面值，API 实测 24h 增量 +746）
**🍴 Fork**：23,982
**👁 Watch**：1,016
**💻 主要语言**：Shell
**📅 开源时间**：2025-10-09
**🔄 最近推送**：2026-08-07
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

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding / AI 编码 Agent 生态口径）。2026-07-11 首入榜（+1013，251.8k，Vibe Coding #4）。
- 2026-07-30 二度上榜（+616，263.6k，Vibe Coding #4），以纯 Markdown 技能 + 子代理驱动开发（subagent-driven-development）覆盖 Claude Code / Codex / Cursor / Copilot CLI / Kimi Code / OpenCode / Pi 等 11+ 主机，核心「先 spec、后红绿 TDD、再分发给子代理」已成事实标准方法论—— Skills 从「能力封装」走向「工程纪律封装」。
- 2026-08-06 三度上榜（🔺931，⭐267.7k，Vibe Coding #2）。08-05 曾是次席生态候选（+653）未入 Top 5，次日以第二名回归。**成长曲线**：2026-07-11 ⭐251,800 → 2026-07-30 ⭐263,643 → 2026-08-06 ⭐267,669。
- 形态始终是纯 Markdown 技能文件 + 少量初始化指令——没有 SDK、没有运行时，却撑起 26 万星。**「技能」这层的边际成本几乎为零，扩散速度天然快过任何需要安装的工具**，这解释了 7 月以来 `book-to-skill` / `reverse-skill` / `compound-engineering-plugin` / `agent-skills` / `superpowers` 反复霸榜的现象。
- 与 [[huangruiteng_loopx|LoopX]] 的分野：superpowers 管**单次任务内怎么干**（spec → 红绿 TDD → 子代理分发），LoopX 管**跨天跨回合怎么接**（目标/闸门/证据/配额）。
- **格式修复（2026-08-06）**：本页 YAML frontmatter 自建档起缺失闭合 `---`，Obsidian 无法解析其属性，本次一并修复。