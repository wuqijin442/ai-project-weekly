---
date: 2026-07-16
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [AI, Trending, Vibe-Coding, 飙升榜, Claude-Code, Cursor, Codex, Skills, Agent-Safety, MCP]
source: GitHub Trending 日榜（github.com/trending?since=daily，curl 直连 HTTP:200）+ GitHub REST API（curl 直连 HTTP:200）

# GitHub AI 项目 · Vibe Coding 日报（2026-07-16）

> 数据口径：**GitHub Trending 日榜「飙升榜」**（按当日新增 Star 降序）＋ 严格关键词 + Vibe Coding / AI 编码 Agent 生态扩充。
> 抓取时间：2026-07-16 08:20 (GMT+8)。主数据源 GitHub Trending 日榜（curl 直连 HTTP:200，获取 608KB 页面，解析 13 个仓库）；GitHub REST API（curl 直连 HTTP:200，Bearer Token）补全 created_at / stars / 语言 / topics；README 经 API `/readme` 端点获取并提炼定位与技术栈。

## 🔝 今日最佳开源项目

**mattpocock/skills** — [仓库链接](https://github.com/mattpocock/skills)
⭐ **172.2k** ｜ 今日 **+2,130⭐**
💡 一句话亮点：Matt Pocock（Total TypeScript）日常真实工程使用的 **AI Agent 技能集**，主张「为真实工程师服务，而非 vibe coding」，小巧可组合、跨模型通用——今日以 **+2,130** 新增登顶 Vibe Coding 榜首（总 Star 172.2k）。

---

## 📊 今日入选项目（按当日新增 Star 降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 简介 |
| - | ---- | ---- | --------- | ---- |
| 1 | [[mattpocock_skills|mattpocock/skills]] | mattpocock | 🔺2,130 | 日常真实工程使用的 AI Agent 技能集（.claude 目录沉淀），小而可组合、跨模型通用，今日新增登顶 |
| 2 | [[Nutlope_hallmark|Nutlope/hallmark]] | Nutlope | 🔺1,277 | 面向 Claude Code / Cursor / Codex 的「反 AI-slop」设计技能（Together AI），57 道 slop-test 门禁拒绝套路化生成 |
| 3 | [[HKUDS_Vibe-Trading|HKUDS/Vibe-Trading]] | HKUDS | 🔺915 | 个人交易 Agent——LLM 多智能体 + MCP 量化交易系统（backtesting + fintech） |
| 4 | [[Dicklesworthstone_destructive_command_guard|Dicklesworthstone/destructive_command_guard]] | Dicklesworthstone | 🔺471 | 面向 AI 编码代理的高性能 Rust 钩子，拦截 git reset --hard / rm -rf 等破坏性命令 |
| 5 | [[openinterpreter_openinterpreter|openinterpreter/openinterpreter]] | openinterpreter | 🔺299 | 知名开源编码 Agent，专为低成本模型优化，让模型直接运行代码完成多步任务 |

---

## 🧭 今日趋势解读

**「技能层」三连击登顶，「代理安全」与「Vibe 范式跨界」并行。**

今日 5 个入选项目中，**mattpocock/skills** 以 🔺2,130 登顶——Matt Pocock（Total TypeScript）把日常 `.claude` 目录里的工程技能公开，主张「为真实工程师服务，而非 vibe coding」，技能小而可组合、跨模型通用。

- **反 AI-slop 设计技能**（hallmark，🔺1,277，多日连榜）：Together AI 出品，57 道 slop-test 门禁 + 发射前自批判，把 Vibe Coding 从「能生成」推向「生成得好看且不像 AI」；
- **Vibe 范式向金融外溢**（Vibe-Trading，🔺915）：HKUDS 出品的 LLM 多智能体 + MCP 量化交易 Agent，延续「写代码」向「金融决策」的跨界主线；
- **代理安全护栏**（dcg，🔺471）：Rust 钩子拦截代理破坏性命令，兼容 Claude Code / Codex CLI / Gemini CLI / Copilot CLI / Cursor，本周多次入榜；
- **老牌编码 Agent 回归**（openinterpreter，🔺299）：严格关键词（open-interpreter）语义匹配，专为低成本模型优化的开源编码 Agent。

**数据看点**：严格关键词仅命中 hallmark（Cursor）+ openinterpreter（语义匹配 open-interpreter），其余按 Vibe Coding / AI 编码 Agent 生态扩充；skills 单日 +2,130、总 Star 17.2 万，稳居「技能即工程纪律」赛道头部。

---

## 🔎 严格关键词命中说明

- **严格关键词**（项目名/简介含 cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev）：
  - ✅ `Nutlope/hallmark` — 简介含 **Cursor**
  - ✅ `openinterpreter/openinterpreter` — 语义匹配 **open-interpreter** 关键词（仓库名无连字符，按项目意图计入；今日 +299 回归）
  - （共 **2** 个严格命中；其中 openinterpreter 为语义匹配，已标注）
- **Vibe Coding / AI 编码 Agent 生态扩充**（Claude Code / Codex / Cursor / MCP / 编码 Agent / 技能）：因严格命中 < 5，按口径扩充至 Top 5（当日新增降序）：
  - `mattpocock/skills` — Claude Code 技能集（.claude 目录），今日 +2,130 居首
  - `HKUDS/Vibe-Trading` — Vibe 范式 + 多智能体 Agent（MCP），今日 +915
  - `Dicklesworthstone/destructive_command_guard` — AI 编码代理安全护栏，今日 +471
- **落选说明**：`coreyhaines31/marketingskills`（Claude Code 营销技能，+340）与 `Shubhamsaboo/awesome-llm-apps`（AI Agent 应用合集，+1,236）因名额与赛道纯度未入选——后者为通用 AI 应用清单，非 Vibe Coding 编码工具。
- **环境说明**：本日 GitHub Trending 日榜与 REST API 均经 curl 直连成功（HTTP:200），13 个仓库全量解析、5 个项目 created_at / stars / 语言 / topics 完整补全；README 经 API `/readme` 端点获取，提炼定位与技术栈。

---

## 📎 相关链接

- 全局索引：[[_Index|GitHub AI 项目归档索引]]
- 昨日（2026-07-15）：[[Vibe-Coding-2026-07-15]]
