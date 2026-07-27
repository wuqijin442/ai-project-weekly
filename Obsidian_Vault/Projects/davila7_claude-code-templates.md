---
aliases: [claude-code-templates, aitmpl]
tags: [AI, Trending, Python, Claude-Code, CLI, MCP, Vibe-Coding, Templates]
stars: 29228
created_at: 2025-07-04
today_growth: 274
status: 待填写
date_accessed: 2026-07-13

# claude-code-templates (aitmpl.com)

**项目地址**：https://github.com/davila7/claude-code-templates
**作者**：davila7
**⭐ 总 Star**：29,228
**📈 今日新增**：274 stars
**💻 主要语言**：Python

## 项目定位

为 Anthropic 的 **Claude Code 提供即用型配置（aitmpl.com）**——一个全面的 AI agents、自定义命令、设置、钩子、外部集成（MCP）与项目模板集合，用于增强开发工作流。配套 CLI（`npx claude-code-templates@latest`）可一键安装组件，并辅以分析、监控与插件仪表板，把编码代理从"零散提示词"带向"可治理的组件市场"。

## 技术栈

- CLI 工具：Node.js（`cli-tool`）、Rust 移植版（`cli-rust`，二进制 `cct`）
- 前端 / 文档站：Astro（部署于 Cloudflare Pages）
- 后端 / API：Cloudflare Workers（含 cron、newsletter）、Neon PostgreSQL（`database/migrations`）
- 分发：npm、Homebrew、cargo-binstall
- 监控：Sentry；自动化：GitHub Actions、Dependabot

## 外部链接

- GitHub：https://github.com/davila7/claude-code-templates
- 作者：https://github.com/davila7
- 项目主页：https://aitmpl.com
- 文档站：https://docs.aitmpl.com
- 仪表板（Beta）：https://www.aitmpl.com
- 主题标签：cli, claude-code, agents, mcp, templates, vibe-coding

## 相关日期

- [[Vibe-Coding-2026-07-13|2026-07-13 日报]]

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding / AI 编码 Agent 生态口径）。
- 关键特性：100+ Agents / Commands / Settings / Hooks / MCPs / Skills（如安全审计、测试生成、GitHub 集成）一键安装；Claude Code Analytics（`--analytics`）、对话监控（`--chats`）、健康检查（`--health-check`）、插件仪表板（`--plugins`）；Beta Dashboard 浏览/管理/追踪安装；多源聚合（K-Dense-AI 科学技能、Anthropic 官方技能、社区技能）并保留原许可证与署名。
