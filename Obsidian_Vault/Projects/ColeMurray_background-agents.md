---
aliases: [background-agents, Open-Inspect]
tags: [AI, Trending, TypeScript, Agent, Background, Coding, Vibe-Coding]
stars: 2251
created_at: 2026-01-25
today_growth: 9
status: 待填写
date_accessed: 2026-07-13
---

# background-agents (Open-Inspect)

**项目地址**：https://github.com/ColeMurray/background-agents
**作者**：ColeMurray
**⭐ 总 Star**：2,251
**📈 今日新增**：9 stars
**💻 主要语言**：TypeScript

## 项目定位

一个**开源的"后台代理（background agents）"编码系统**，受 Ramp 公司的 Inspect 工具启发。它提供托管式后台编程代理，可在用户专注其他事务时自主完成任务。安全模型明确为**单租户（Single-Tenant Only）**：所有用户为同一组织内的可信成员，共享 GitHub App 凭证，无多租户隔离——把"代理在旁自主干活"的范式向前推了一步。

## 技术栈

- 前端：React / Next.js（web 包）、Tailwind
- 控制面：TypeScript + Cloudflare Workers + D1 / SQLite
- 沙箱运行：Python（`modal-infra` / `sandbox-runtime`）、Bun（代理服务）、Terraform（基础设施）
- 集成：GitHub App、Slack、Linear、Webhook

## 外部链接

- GitHub：https://github.com/ColeMurray/background-agents
- 作者：https://github.com/ColeMurray
- 会话产品域：https://open-inspect-prod.vercel.app
- 主题标签：agents, background, coding, claude, codex, vibe-coding

## 相关日期

- [[Vibe-Coding-2026-07-13|2026-07-13 日报]]

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding / AI 编码 Agent 生态口径）。
- 关键特性：后台任务执行（完整 dev 环境：Node.js、Python、git、浏览器自动化、VS Code）；多入口触发（Web UI / Slack / GitHub PR / Linear issue / webhook）；实时多人协作；并行子任务（独立沙箱）；灵活模型（Anthropic Claude、OpenAI Codex、OpenCode Zen）与 cron / Sentry 告警 / webhook 调度。
