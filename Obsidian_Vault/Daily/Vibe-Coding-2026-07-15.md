---
date: 2026-07-15
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [AI, Trending, Vibe-Coding, 飙升榜, Claude-Code, Cursor, Codex, Skill, Agent-Safety]
source: GitHub Trending 日榜（github.com/trending?since=daily，curl 直连 HTTP:200）+ GitHub REST API（curl 直连 HTTP:200）
---

# GitHub AI 项目 · Vibe Coding 日报（2026-07-15）

> 数据口径：**GitHub Trending 日榜「飙升榜」**（按当日新增 Star 降序）＋ 严格关键词 + Vibe Coding / AI 编码 Agent 生态扩充。
> 抓取时间：2026-07-15 08:20 (GMT+8)。主数据源 GitHub Trending 日榜（curl 直连 HTTP:200，获取 638KB 页面，解析 16 个仓库）；GitHub REST API（curl 直连 HTTP:200）补全 created_at / stars / 语言 / topics。**本日网络连通性恢复**（沙箱此前对 github.com 直连 HTTP:000 的阻断已解除），raw.githubusercontent.com 仍不可达（HTTP:000），README 提炼改以 API description + topics 为主。

## 🔝 今日最佳开源项目

**Graphify-Labs/graphify** — [仓库链接](https://github.com/Graphify-Labs/graphify)
⭐ **86.3k** ｜ 今日 **+1,851⭐**
💡 一句话亮点：把任意代码库（代码 / SQL schema / R 脚本 / 文档 / 论文 / 图片 / 视频）变成**可查询知识图谱**的 AI 编码助手技能，原生兼容 Claude Code / Cursor / Codex / Gemini CLI 等主流编码 Agent——连续两日稳居 Vibe Coding 榜首。

---

## 📊 今日入选项目（按当日新增 Star 降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 简介 |
| - | ---- | ---- | --------- | ---- |
| 1 | [[Graphify-Labs_graphify\|Graphify-Labs/graphify]] | Graphify-Labs | 🔺1,851 | AI 编码助手技能，将代码/SQL/R/文档/图片/视频转成可查询知识图谱（Claude Code、Cursor、Codex、Gemini CLI 等通用） |
| 2 | [[mattpocock_skills\|mattpocock/skills]] | mattpocock | 🔺1,679 | 为「真实工程师」服务的 AI Agent 技能集（.claude 目录沉淀），小而可组合、跨模型通用 |
| 3 | [[HKUDS_Vibe-Trading\|HKUDS/Vibe-Trading]] | HKUDS | 🔺1,256 | 个人交易 Agent——LLM 多智能体量化交易系统（MCP + backtesting + fintech） |
| 4 | [[Nutlope_hallmark\|Nutlope/hallmark]] | Nutlope | 🔺1,015 | 面向 Claude Code / Cursor / Codex 的「反 AI-slop」设计技能，拒绝生成千篇一律的模板页 |
| 5 | [[Dicklesworthstone_destructive_command_guard\|Dicklesworthstone/destructive_command_guard]] | Dicklesworthstone | 🔺473 | 面向 AI 编程代理的高性能钩子，拦截 `git reset --hard`/`rm -rf` 等破坏性命令（Rust，亚毫秒级） |

---

## 🧭 今日趋势解读

**「技能层 + 代理安全」双线并进，Vibe 范式向金融外溢。**

今日 5 个入选项目中，3 个属于「技能（Skill）」——

- **知识图谱技能**（graphify，🔺1,851，两连冠）：让 Agent 把整库代码 + 数据库 schema + 基础设施建成一张图，检索与推理更省 token；
- **工程技能集**（mattpocock/skills，🔺1,679，17 万 Star）：主张「为真实工程师服务，而非 vibe coding」，技能小而可组合、跨模型通用；
- **反 AI-slop 设计技能**（hallmark，🔺1,015，三连榜）：把 Vibe Coding 战场从「能生成」推向「生成得好看且不像 AI」。

**代理安全**（dcg，🔺473）持续在榜——Rust 钩子拦截代理破坏性命令，是 Vibe Coding 走向生产可用的一道护栏，已是本周第二次入榜。

**新变量**：**Vibe-Trading**（🔺1,256）代表 "Vibe" 范式从「写代码」向「金融决策」外溢——LLM 多智能体 + MCP 驱动的量化交易，由 HKUDS 学术团队出品。技能层（graphify / skills / hallmark）+ 安全护栏（dcg）+ 范式外溢（Vibe-Trading），勾勒出 Vibe Coding 生态从「生成」到「可控生成」再到「跨界智能体」的演进路径。

---

## 🔎 严格关键词命中说明

- **严格关键词**（项目名/简介含 cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev）：
  - ✅ `Graphify-Labs/graphify` — 简介含 **Cursor**
  - ✅ `Nutlope/hallmark` — 简介含 **Cursor**
  - （共 **2** 个严格命中）
- **Vibe Coding / AI 编码 Agent 生态扩充**（Claude Code / Codex / Cursor / MCP / 编码 Agent / 技能）：因严格命中 < 5，按口径扩充至 Top 5（当日新增降序）：
  - `mattpocock/skills` — Claude Code 技能集（.claude 目录）
  - `HKUDS/Vibe-Trading` — Vibe 范式 + 多智能体 Agent（MCP）生态，今日新增居第 3
  - `Dicklesworthstone/destructive_command_guard` — AI 编码代理安全护栏
- **环境说明**：本日 GitHub Trending 日榜与 REST API 均经 curl 直连成功（HTTP:200），16 个仓库全量解析、5 个项目 created_at / stars / 语言 / topics 完整补全；raw.githubusercontent.com 仍不可达（HTTP:000），README 提炼以 API 元数据为主，不影响归档完整性。

---

## 📎 相关链接

- 全局索引：[[_Index|GitHub AI 项目归档索引]]
- 昨日（2026-07-14）：[[Vibe-Coding-2026-07-14]]
