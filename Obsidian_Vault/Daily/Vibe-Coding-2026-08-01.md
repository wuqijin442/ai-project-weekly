---
date: 2026-08-01
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [GitHub, Trending, Vibe-Coding, AI, Daily]
source: https://github.com/trending?since=daily
---

# GitHub AI 热门项目 · Vibe Coding 日报（2026-08-01（周六））

> 数据源：GitHub Trending 日榜（飙升榜，按当日新增 Star 降序）｜筛选口径：严格关键词 + Vibe Coding / AI 编码 Agent 生态扩充。
> ⚠️ 今日严格关键词（cursor / cline / copilot 等 15 个）命中 0 个；GitHub 日榜经 curl 直连 HTTP:200 解析 12 个仓库，按 Vibe Coding / AI 编码 Agent 生态口径扩充取 Top 5（当日新增降序）。**数据质量提示**：今日 trending 快照的「今日新增」数值与 2026-07-29 高度重叠（book-to-skill 423/423、aisuite 62/62、agent-governance-toolkit 46/46），疑似沙箱侧命中 GitHub Trending 缓存快照；总 Star 以 GitHub REST API 实时值（权威）记录，今日新增沿用 trending 页面解析值并如实标注。今日主线为「Claude Code 技能生态双线 + Agent harness 底座 + LLM 接入标准化 + 生产治理补齐」。

## 🔝 今日最佳开源项目

**#1 [[bradautomates_claude-video|claude-video]]** — bradautomates
- 链接：https://github.com/bradautomates/claude-video
- 总 Star：**13.2k** ｜ 今日新增：**🔺988**
- 一句话亮点：赋予 Claude 观看任何视频的能力（/watch 下载、提取帧、转录、把画面与音频交给 Claude 理解）；Claude Code / Codex / Cursor / Copilot / Gemini CLI 等 50+ Agent Skills 主机通用，今日以 +988 登顶 Vibe Coding 飙升榜（五度上榜🔝）。

---

## 入选项目（按当日新增降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 简介 |
|---|------|------|-----------|------|
| 1 | [[bradautomates_claude-video|claude-video]] | bradautomates | 🔺988 | Give Claude the ability to watch any video. /watch downloads, extracts frames, transcribes, hands it all to Claude. |
| 2 | [[affaan-m_ECC|ECC]] | affaan-m | 🔺636 | The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond. |
| 3 | [[virgiliojr94_book-to-skill|book-to-skill]] | virgiliojr94 | 🔺423 | Turn any technical book PDF into a Claude Code skill — ready to study, reference, and use while you work. |
| 4 | [[andrewyng_aisuite|aisuite]] | andrewyng | 🔺62 | Simple, unified interface to multiple Generative AI providers  |
| 5 | [[microsoft_agent-governance-toolkit|agent-governance-toolkit]] | microsoft | 🔺46 | AI Agent Governance Toolkit — Policy enforcement, zero-trust identity, execution sandboxing, and reliability engineering for autonomous AI agents. Covers 10/10 OWASP Agentic Top 10. |

---

## 今日趋势解读

1. **「Claude Code 技能生态」双线统治 Vibe Coding 榜**：bradautomates/claude-video（+988 居 #1，五度上榜）把"看视频"封装为 Claude 技能——抓字幕、下帧、转写、逐帧 Read，让 Agent 真正"看见"并听懂视频；virgiliojr94/book-to-skill（+423 居 #3，三度上榜）把任意技术书/文档文件夹转成符合 Agent Skills Open Standard 的可复用技能包。两者共同印证 Skills 正从"能力封装"走向"多模态理解"与"知识资产沉淀"。
2. **「Agent harness 作为操作系统」稳居前列**：affaan-m/ECC（236.7k，+636 居 #2，连续 4 日上榜）自述"the agent harness performance optimization system"，把 Skills + instincts + memory + security + research-first 整合为面向 Claude Code / Codex / Opencode / Cursor 的底座，多语言文档含简繁中文——仍是今日体量最大的编码 Agent 底座候选。
3. **「LLM 接入层标准化」补位**：andrewyng/aisuite（+62 居 #4，二度上榜，⭐15.9k) 提供跨供应商统一的 Chat Completions API + 上层 Agents API（tools / toolkits），是编码 Agent 切换 OpenAI / Anthropic / Google 模型的抽象底座；其上还驱动桌面 AI 同事 OpenWorker。
4. **「Agent 生产化治理」补齐最后一块**：microsoft/agent-governance-toolkit（+46 居 #5，二度上榜，⭐5.5k) 提供策略引擎 + 零信任身份 + 执行沙箱 + 可靠性工程，官方宣称覆盖 10/10 OWASP Agentic Top 10，PyPI / npm / NuGet 三栖分发——标志 Agent 从"能写代码"走向"敢上生产"。
5. **边界排除**：moeru-ai/airi（+797 Grok 伴侣机器人）、yorukot/superfile（+662 终端文件管理器）、opengeos/GeoLibre（+607 云原生 GIS）、pascalorg/editor（+341 3D 建筑编辑器）、paperswithbacktest/awesome-systematic-trading（+309 量化交易清单）、huggingface/speech-to-speech（+227 本地语音 Agent）、jenkinsci/jenkins（+180 CI 服务器）等非编码 Agent 项目均不纳入；sponsors/* 伪条目已剔除。

## 严格关键词命中说明

- **严格关键词**（项目名或简介含 cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev）：本日 **0 个**命中。
- 命中不足 5 个，按 **Vibe Coding / AI 编码 Agent 生态**（Claude Code / Codex / Cursor / MCP / 编码 Agent / 技能 / Agent 工程底座）口径扩充，取当日新增 Star 降序：
  - `bradautomates/claude-video`（Claude 看视频技能，50+ Agent Skills 主机通用）— **生态扩充（五度上榜登顶 #1）**
  - `affaan-m/ECC`（agent harness 性能优化系统：Skills/instincts/memory/security，面向 Claude Code/Codex/Opencode/Cursor，236.7k 体量）— **生态扩充（连续 4 日上榜 #2）**
  - `virgiliojr94/book-to-skill`（技术书/文档 → 符合 Agent Skills Open Standard 的技能包）— **生态扩充（三度上榜 #3）**
  - `andrewyng/aisuite`（跨供应商统一 Chat Completions + Agents API，Andrew Ng 出品）— **生态扩充（二度上榜 #4）**
  - `microsoft/agent-governance-toolkit`（策略引擎 + 零信任 + 沙箱，覆盖 OWASP Agentic Top 10）— **生态扩充（二度上榜 #5）**
- 边界排除：moeru-ai/airi（+797）、yorukot/superfile（+662）、opengeos/GeoLibre（+607）、pascalorg/editor（+341）、paperswithbacktest/awesome-systematic-trading（+309）、huggingface/speech-to-speech（+227）、jenkinsci/jenkins（+180）等非编码 Agent；sponsors/* 伪条目已剔除。
