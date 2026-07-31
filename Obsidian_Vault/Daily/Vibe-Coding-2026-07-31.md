---
date: 2026-07-31
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [GitHub, Trending, Vibe-Coding, AI, Daily]
source: https://github.com/trending?since=daily
---

# GitHub AI 热门项目 · Vibe Coding 日报（2026-07-31 · 周五）

> 数据源：GitHub Trending 日榜（飙升榜，按当日新增 Star 降序）｜筛选口径：严格关键词 + Vibe Coding / AI 编码 Agent 生态扩充。
> ⚠️ 今日严格关键词（cursor / cline / copilot 等 15 个）命中 1 个（affaan-m/ECC 简介含 "Cursor"）；GitHub 日榜经 WebFetch 抓回 14 个仓库（curl 直连临时 HTTP:000，按兜底规则用 WebFetch，高新增段完整捕获、尾部低新增段被截断不影响 Top 5 选取），按 Vibe Coding / AI 编码 Agent 生态口径扩充取 Top 5（当日新增降序）。今日主线为「Agent 工作流跨工具复用 + 代码质量 / 调试下沉到 Agent」。

## 🔝 今日最佳开源项目

**#1 [[different-ai_openwork|openwork]]** — different-ai
- 链接：https://github.com/different-ai/openwork
- 总 Star：**19.1k** ｜ 今日新增：**🔺915**
- 一句话亮点：开源的 AI 工作流共享桌面应用，Claude Cowork / Codex 的开源替代；通过一个 OpenWork MCP 把 skills / MCPs / 连接服务在 Codex、Claude Code、Cursor 等工具间复用，一次创建、处处可用，今日以 +915 登顶 Vibe Coding 飙升榜（首入榜 #1）。

---

## 入选项目（按当日新增降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 简介 |
|---|------|------|-----------|------|
| 1 | [[different-ai_openwork|openwork]] | different-ai | 🔺915 | The open-source alternative to Claude Cowork (powered by opencode) — a free desktop app for sharing AI workflows; add one OpenWork MCP to Codex, Claude Code, Cursor and reuse skills/MCPs across tools. |
| 2 | [[affaan-m_ECC|ECC]] | affaan-m | 🔺804 | The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond. |
| 3 | [[mvanhorn_last30days-skill|last30days-skill]] | mvanhorn | 🔺378 | AI agent skill that researches any topic across Reddit, X, YouTube, HN, Polymarket, and the web — then synthesizes a grounded summary. |
| 4 | [[agavra_tuicr|tuicr]] | agavra | 🔺190 | A code review TUI with vim keybindings — terminal UI for AI-assisted code review. |
| 5 | [[ChromeDevTools_chrome-devtools-mcp|chrome-devtools-mcp]] | ChromeDevTools | 🔺80 | Chrome DevTools for coding agents — an MCP server bringing browser debugging (puppeteer / Chrome DevTools Protocol) to agents. |

---

## 今日趋势解读

1. **「Agent 工作流跨工具复用」登顶，能力即服务成新范式**：different-ai/openwork（+915 居 #1，首入榜）把"共享 AI 工作流"做成开源桌面应用，通过一个 OpenWork MCP 让 Codex / Claude Code / Cursor / ChatGPT 等共用同一套 skills、MCP 连接、Google Workspace / Microsoft 365 能力——"一次创建、处处可用"。标志 Vibe Coding 从"单 Agent 写代码"跃迁到"跨工具、跨团队、跨机器复用工作流"。
2. **「Agent harness 作为操作系统」稳居 #2**：affaan-m/ECC（236.5k，+804 居 #2，四度上榜）自述"the agent harness performance optimization system"，把 Skills + instincts + memory + security + research-first 打包为统一 harness，多语言文档含繁体中文——仍是今日体量最大的编码 Agent 底座之一，与 openwork 形成"底座优化 + 工作流分发"互补。
3. **「Agent 技能生态」补位研究侧**：mvanhorn/last30days-skill（55.8k，+378 居 #3，三度上榜）跨 Reddit / X / YouTube / HN / Polymarket / Web 研究并综合成有依据摘要，是 Agent Skills 规范在"实时研究 / 竞品情报"侧的标杆——印证 Skills 从"能力封装"走向"知识工作流封装"。
4. **「代码质量 / 调试下沉到 Agent」双线升温**：agavra/tuicr（2.0k，+190 居 #4，首入榜）用 Rust 写带 vim 键位的 code review TUI，把 AI 辅助审查搬进终端；ChromeDevTools/chrome-devtools-mcp（48.2k，+80 居 #5，首入榜）把 Chrome DevTools 浏览器调试通过 MCP 带给 coding agents——两者共同把"审查"与"调试"两大工程环节直接接入 Agent 闭环。
5. **边界排除**：huggingface/speech-to-speech（+628 本地语音 Agent）、pascalorg/editor（+625 3D 建筑编辑器）、paperswithbacktest/awesome-systematic-trading（+621 量化交易清单）、microsoft/AI-For-Beginners（+155 AI 课程）、microsoft/PowerToys（+70 Windows 工具）、WhiskeySockets/Baileys（+19 WhatsApp API）、jenkinsci/jenkins（+25 CI）、ansible/ansible（+29 IT 自动化）、dotnet/aspnetcore（+7 Web 框架）等非编码 Agent 项目均不纳入；sponsors/* 伪条目已剔除。

## 严格关键词命中说明

- **严格关键词**（项目名或简介含 cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev）：本日 **1 个**命中 —— affaan-m/ECC（简介含 "Cursor"）。
- 命中不足 5 个，按 **Vibe Coding / AI 编码 Agent 生态**（Claude Code / Codex / Cursor / MCP / 编码 Agent / 技能 / Agent 工程底座）口径扩充，取当日新增 Star 降序：
  - `different-ai/openwork`（开源 AI 工作流共享桌面应用，OpenWork MCP 跨 Codex/Claude Code/Cursor 复用 skills/MCPs）— **生态扩充（今日登顶 #1）**
  - `affaan-m/ECC`（agent harness 性能优化系统：Skills/instincts/memory/security，面向 Claude Code/Codex/Opencode/Cursor，236.5k 体量）— **严格命中（四度上榜 #2）**
  - `mvanhorn/last30days-skill`（跨社媒/Web 的 AI Agent 研究技能，Agent Skills 规范）— **生态扩充（三度上榜 #3）**
  - `agavra/tuicr`（Rust 编写、带 vim 键位的 code review TUI）— **生态扩充（首入榜 #4）**
  - `ChromeDevTools/chrome-devtools-mcp`（面向 coding agents 的 Chrome DevTools MCP 服务器）— **生态扩充（首入榜 #5）**
- 边界排除：huggingface/speech-to-speech（+628）、pascalorg/editor（+625）、paperswithbacktest/awesome-systematic-trading（+621）、microsoft/AI-For-Beginners（+155）、microsoft/PowerToys（+70）、WhiskeySockets/Baileys（+19）、jenkinsci/jenkins（+25）、ansible/ansible（+29）、dotnet/aspnetcore（+7）等非编码 Agent；sponsors/* 伪条目已剔除。
