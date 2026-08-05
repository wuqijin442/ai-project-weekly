---
aliases: [compound-engineering-plugin, Compound Engineering, CE]
tags: [AI, Trending, TypeScript, Skills, Plugin, Methodology, Vibe-Coding]
stars: 23975
created_at: 2025-10-09
today_growth: 40
status: 新上榜（首入榜 #5，严格关键词命中 Cursor）
date_accessed: 2026-08-05
---

# compound-engineering-plugin

**项目地址**：https://github.com/EveryInc/compound-engineering-plugin
**作者**：EveryInc（Every 媒体/工作室）
**⭐ 总 Star**：23,975（24.0k）
**📈 今日新增**：🔺40 stars
**🍴 Fork**：1,960
**💻 主要语言**：TypeScript
**📅 开源时间**：2025-10-09
**🔄 最近推送**：2026-08-05
**🌐 官网**：https://every.to/guides/compound-engineering
**📜 许可证**：MIT

## 项目定位

**Compound Engineering（复利工程）官方插件**。一句话主张：

> *AI skills that make each unit of engineering work easier than the last.*
> 让每一单位工程工作，都比上一单位更省力。

这是一套**方法论 + 可执行技能包**的组合体：不是又一个编码 Agent，而是架在既有 Agent（Claude Code / Codex / Cursor）之上的**工作方式插件**——把 review、research、规划等重复性工程动作沉淀为技能，使团队的工程效率随使用次数产生复利，而非线性消耗。

## 跨客户端安装（覆盖主流编码 Agent）

| 客户端 | 安装方式 |
|--------|---------|
| **Claude Code** | `/plugin marketplace add EveryInc/compound-engineering-plugin` → `/plugin install compound-engineering` |
| **Cursor** | Agent chat 内 `/add-plugin compound-engineering`，或插件市场搜索 "compound engineering" |
| **Codex App** | 侧栏 Plugins → Add marketplace → Source 填 `EveryInc/compound-engineering-plugin`、Git ref `main` → 安装后重启 |
| **Codex CLI** | `codex plugin marketplace add EveryInc/compound-engineering-plugin` → `codex plugin add compound-engineering@compound-engineering-plugin` |

> ⚠️ **老用户升级注意**：项目已迁移为 root-native 布局，必须**先刷新 marketplace 再更新**，仅执行 `/plugin update` 会停留在旧版本。

## 技术要点

- **自包含设计**：专家审查者（specialist reviewer）与研究行为以**本地 prompt 资产**形式内置在 skills 中，无需额外安装 custom-agent
- **多 profile 支持**：非默认 Codex profile 需对所有 Codex 步骤统一 `CODEX_HOME`（如 `CODEX_HOME="$HOME/.codex/profiles/work"`）
- **topics**：`compound`、`engineering`
- **许可证**：MIT

## 使用场景

- 团队希望把 code review / 研究 / 规划的最佳实践固化成可复用技能，而非散落在个人 prompt 里
- 同时使用 Claude Code、Codex、Cursor 的多客户端团队，需要一份统一的工程技能基线
- 追求「工程复利」而非单次提效的长期项目

## 外部链接

- GitHub：https://github.com/EveryInc/compound-engineering-plugin
- 方法论指南：https://every.to/guides/compound-engineering
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-08-05|2026-08-05 日报]]（首入榜 #5，严格关键词命中 `cursor`）

## 备注

- 今日新增仅 +40，入选源于**严格关键词命中优先**规则（简介含 Cursor），而非飙升幅度；其 24.0k 存量说明这是一个已完成早期扩散、进入稳定使用期的项目
- 与同日 +653 的 [[obra_superpowers|obra/superpowers]] 同属「agentic 方法论产品化」赛道，两者路径不同：superpowers 走技能框架 + 子代理驱动开发，CE 走跨客户端官方插件分发
