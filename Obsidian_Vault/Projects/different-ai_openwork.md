---
aliases: [openwork, different-ai/openwork]
tags: [AI, Trending, TypeScript, Vibe-Coding, Agent-Workflow, MCP]
stars: 21660
weekly_growth: 1834
created_at: 2026-01-14
status: 活跃（全赛道周榜 #7，本周 🔺1,834）
date_accessed: 2026-08-09
---

# different-ai/openwork

**项目地址**：https://github.com/different-ai/openwork
**作者**：different-ai
**⭐ 总 Star**：21,660（21.7k）  <!-- 2026-08-09 实时值；07-31 为 19,070 -->
**📈 本周新增**：🔺1,834 stars（全赛道周榜 #7）
**💻 主要语言**：TypeScript
**形态**：开源桌面应用 + MCP 服务器

## 项目定位

`openwork` 是一个**免费开源的 AI 工作流共享桌面应用**，是 Claude Cowork / Codex 的开源替代。它让你把 skills、MCP 连接、Google Workspace / Microsoft 365 等能力"一次创建、处处可用"——通过添加一个 OpenWork MCP，就能在 Codex、Claude Code、Cursor、ChatGPT 等任意兼容 Agent 间复用同一套技能与连接服务，跨工具、跨团队成员、跨机器共享。

核心理念：**能力即服务**——你不再为每个 Agent 重复配置，而是在统一工作区里创建能力，再分发给协作伙伴或自己。对企业，管理后台可发布能力、管理访问权限、配置共享或按用户的连接。

## 核心能力

- **跨 Agent 复用**：一个 OpenWork MCP 把已分配的 skills、插件、MCP 连接、Google Workspace、Microsoft 365 能力带入任意兼容 Agent
- **桌面工作区**：macOS / Windows / Linux 桌面应用，也支持纯 Agent 使用（无需桌面）
- **能力分发**：暴露 `search_capabilities`（发现可用能力）与 `execute_capability`（执行能力）两个工具
- **企业管理**：发布能力、管理访问、配置共享 / 按用户连接

## 技术栈

- **语言**：TypeScript
- **形态**：桌面应用 + MCP 服务器（HTTP transport：`https://api.openworklabs.com/mcp/agent`）
- **集成**：Codex / Claude Code / Cursor / ChatGPT 等；Google Workspace、Microsoft 365
- **协议**：MCP（Model Context Protocol）

## 安装方式

```bash
# Codex
codex mcp add openwork --url https://api.openworklabs.com/mcp/agent

# Claude Code
claude mcp add --transport http openwork https://api.openworklabs.com/mcp/agent
```

## 使用场景

- 团队 / 跨机器**复用同一套 AI 工作流与技能**
- 把企业内部能力（文档、日历、连接服务）作为 MCP 分发给多个 Agent
- Claude Cowork / Codex 的开源、自托管替代

## 外部链接

- GitHub：https://github.com/different-ai/openwork
- 官网：https://openworklabs.com
- 下载：https://openworklabs.com/download

## 相关日期

- [[Vibe-Coding-2026-07-31|2026-07-31 日报]]
- [[AI-Weekly-2026-08-09|2026-08-09 全赛道周报]]（周榜 #7，🔺1,834 / ⭐21.7k）

## 备注

- 今日以 +915 登顶 Vibe Coding 飙升榜（首入榜 #1），是"Agent 工作流跨工具复用"主线的代表项目。
