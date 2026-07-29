---
date: 2026-07-29
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [GitHub, Trending, Vibe-Coding, AI, Daily]
source: https://github.com/trending?since=daily
---

# GitHub AI 热门项目 · Vibe Coding 日报（2026-07-29 · 周三）

> 数据源：GitHub Trending 日榜（飙升榜，按当日新增 Star 降序）｜筛选口径：严格关键词 + Vibe Coding / AI 编码 Agent 生态扩充。
> ⚠️ 今日严格关键词（cursor / cline / copilot 等 15 个）命中 0 个；GitHub 日榜仅返回 12 个仓库（/trending/ai 补充校验为空），按 Vibe Coding / AI 编码 Agent 生态口径扩充取 Top 5（当日新增降序）。今日 Vibe Coding 信号偏稀疏，#4/#5 为 Agent 工程基础设施（LLM 接入层 + 治理）。

## 🔝 今日最佳开源项目

**#1 [[bradautomates_claude-video|claude-video]]** — bradautomates
- 链接：https://github.com/bradautomates/claude-video
- 总 Star：**12.5k** ｜ 今日新增：**🔺988**
- 一句话亮点：让 Claude「看懂视频」的 /watch 技能——下载、抽帧、转写、把每一帧作为图像读入上下文；支持 50+ Agent Skills 主机（Claude Code / Codex / Cursor / Copilot / Gemini CLI），今日以 +988 领跑 Vibe Coding 飙升榜。

---

## 入选项目（按当日新增降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 简介 |
|---|------|------|-----------|------|
| 1 | [[bradautomates_claude-video|claude-video]] | bradautomates | 🔺988 | Give Claude the ability to watch any video. /watch downloads, extracts frames, transcribes, hands it all to Claude. |
| 2 | [[affaan-m_ECC|ECC]] | affaan-m | 🔺636 | The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond. |
| 3 | [[virgiliojr94_book-to-skill|book-to-skill]] | virgiliojr94 | 🔺423 | Turn any technical book PDF into a Claude Code skill — ready to study, reference, and use while you work. |
| 4 | [[andrewyng_aisuite|aisuite]] | andrewyng | 🔺62 | Simple, unified interface to multiple Generative AI providers (Chat Completions + Agents API). |
| 5 | [[microsoft_agent-governance-toolkit|agent-governance-toolkit]] | microsoft | 🔺46 | AI Agent Governance Toolkit — Policy enforcement, zero-trust identity, execution sandboxing, reliability engineering; covers 10/10 OWASP Agentic Top 10. |

---

## 今日趋势解读

1. **「Claude 技能生态」三箭齐发，今日 Vibe Coding 榜被 Claude Code 生态垄断**：claude-video（看视频技能，+988 登顶）、book-to-skill（技术书→Claude Code 技能，+423）、ECC（agent harness 操作系统，+636 居 #2）——三者均围绕 Claude Code 的 Skills / 记忆 / harness 工程化，标志「把能力封装成可安装 Skill」已成 Vibe Coding 主流范式。
2. **「Agent harness 作为操作系统」范式成熟**：affaan-m/ECC 以 **235.2k** 总星、35.8k Fork 居全 GitHub 日榜前列（日榜 #4），自述「the agent harness operating system」，面向 Claude Code / Codex / Opencode / Cursor，把 Skills + instincts + memory + security + research-first 打包为统一 harness；多语言文档含繁体中文，是今日体量最大的编码 Agent 底座。
3. **「编码 Agent 接入层 → 治理」走向生产化**：andrewyng/aisuite（15.8k，Andrew Ng 出品，统一多 GenAI 供应商接口 + Agents API，驱动 OpenWorker 桌面 AI 同事）补齐 LLM 接入底座；microsoft/agent-governance-toolkit（5.4k，零信任身份 + 执行沙箱 + 策略引擎，覆盖 10/10 OWASP Agentic Top 10，提供 PyPI/npm/NuGet 多语言包）补齐治理与合规——从「能跑」走向「可控、可治理」。
4. **边界排除**：moeru-ai/airi（+797 Grok 伴侣，AI 伴侣非编码 Agent）、yorukot/superfile（+662 终端文件管理器）、opengeos/GeoLibre（+607 云原生 GIS）、pascalorg/editor（+341 3D 建筑编辑器）、paperswithbacktest/awesome-systematic-trading（+309 量化交易清单）、huggingface/speech-to-speech（+227 本地语音 Agent）、jenkinsci/jenkins（+180 CI 服务器）等非编码 Agent 项目均不纳入；sponsors/* 伪条目已剔除。

## 严格关键词命中说明

- **严格关键词**（项目名或简介含 cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev）：本日 **0 个**命中。
- 命中不足 5 个，按 **Vibe Coding / AI 编码 Agent 生态**（Claude Code / Codex / Cursor / MCP / 编码 Agent / 技能 / Agent 工程底座）口径扩充，取当日新增 Star 降序：
  - `bradautomates/claude-video`（Claude 看视频技能，Claude Code 生态，50+ Agent Skills 主机）— **生态扩充（今日登顶 #1）**
  - `affaan-m/ECC`（agent harness OS：Skills/instincts/memory/security，面向 Claude Code/Codex/Opencode/Cursor）— **生态扩充（235k 体量，日榜 #4）**
  - `virgiliojr94/book-to-skill`（技术书/文档→Claude Code 技能，Agent Skills Open Standard）— **生态扩充**
  - `andrewyng/aisuite`（统一多 GenAI 供应商接口 + Agents API，编码 Agent LLM 接入底座）— **生态扩充（基础设施）**
  - `microsoft/agent-governance-toolkit`（Agent 治理/零信任/沙箱/OWASP Agentic Top 10）— **生态扩充（基础设施）**
- 边界排除：moeru-ai/airi（+797）、yorukot/superfile（+662）、opengeos/GeoLibre（+607）、pascalorg/editor（+341）、paperswithbacktest/awesome-systematic-trading（+309）、huggingface/speech-to-speech（+227）、jenkinsci/jenkins（+180）等非编码 Agent；sponsors/* 伪条目已剔除。
