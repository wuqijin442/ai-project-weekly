---
aliases: [ai-memory, akitaonrails/ai-memory]
tags: [AI, Trending, Rust, Claude-Code, Codex, Agent, Memory, Vibe-Coding]
stars: 3000
created_at: 2026-05-21
today_growth: 648
status: 3度上榜
date_accessed: 2026-08-19
---

# ai-memory

**项目地址**：https://github.com/akitaonrails/ai-memory
**作者**：akitaonrails（Fabio Akita）
**⭐ 总 Star**：2,395（2.4k）  <!-- 2026-08-18 GitHub REST API 实时值 -->
**📈 今日新增**：🔺207（2026-08-18 GitHub Trending 飙升榜真实值）
**🎯 生态命中**：agent coding CLIs / AI coding agents 记忆层（描述与 README 明确面向编码 Agent）
**🍴 Fork**：212
**💻 主要语言**：Rust
**📅 开源时间**：2026-05-21
**🔄 最近推送**：2026-08-18 01:24（今日活跃）
**🌐 官网**：（无）
**🏷 Topics**：（空，未在 trending/API 暴露）
**📜 许可证**：MIT

## 项目定位

为 **AI 编码 Agent** 提供长期记忆（Long-term Memory）的解决方案。核心理念：在 Claude Code 中途退出任务后，切换到 OpenAI Codex 在同一目录继续工作，**无需重新解释架构、失败过的尝试路径与遗留的未决问题**——通过跨 Agent 厂商的记忆交接（handoff），保留上下文。

> *"Long-term memory for AI coding agents. Quit Claude Code mid-task, start OpenAI Codex in the same directory, continue without re-explaining the architecture, the failed approaches, or the open questions."*

## 核心能力

- **跨厂商记忆交接**：在不同编码 Agent（Claude Code / Codex / 其他）之间保留任务上下文，避免重复解释。
- **多平台支持矩阵**：
  - Linux（主推 Docker/server + CI，含 amd64/arm64 镜像）
  - macOS（Apple Silicon 原生二进制优先）
  - Windows via WSL2（推荐路径）
  - 原生 Windows（实验性，提供 `ai-memory.exe`）
- **Claude Code 集成**：MCP 配置 + 生命周期 hooks；`install-mcp --session-aware` 可开启按会话自动隔离（本地 stdio bridge）；`--capture-assistant` 可在 `Stop` 时捕获助手最后一回合（双 opt-in，默认关）。

## 技术栈

- 语言：Rust（rust-toolchain 1.95+）
- 分发：Docker 镜像 / 原生二进制（macOS aarch64/x86_64、Windows x86_64 zip）/ Arch AUR 包（含 systemd units）
- 集成协议：MCP（Model Context Protocol）

## 外部链接

- GitHub：https://github.com/akitaonrails/ai-memory
- 作者：https://github.com/akitaonrails

## 相关日期

- [[Daily/Vibe-Coding-2026-08-18|2026-08-18 日报]]（Vibe Coding #1，⭐2.4k / 🔺207，生态命中 agent coding CLIs）

## 备注

- 2026-08-18：作为今日 Vibe Coding 赛道「今日最佳🔝」入选。总 Star 2,395、今日新增 🔺207，且当日仍有活跃推送（01:24Z），属新兴编码 Agent 配套工具中势头最猛者。
- 赛道定位：编码 Agent「记忆层」，与 08-17 的 spec-kit / agent-skills（工程纪律 / 技能层）形成互补——从「怎样写更好」走向「记住写过了什么」。

## 反向链接
- [[Daily/Vibe-Coding-2026-08-18.md|2026-08-18 收录]]
- [[Daily/Vibe-Coding-2026-08-19.md|2026-08-19 收录]]
