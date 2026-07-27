---
date: 2026-07-14
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [AI, Trending, Vibe-Coding, 飙升榜, Claude-Code, Cursor, Codex]
source: GitHub Trending 日榜（github.com/trending?since=daily）+ GitHub REST API（WebFetch 兜底）
---

# GitHub AI 项目 · Vibe Coding 日报（2026-07-14）

> 数据口径：**GitHub Trending 日榜「飙升榜」**（按当日新增 Star 降序）＋ 严格关键词 + Vibe Coding / AI 编码 Agent 生态扩充。
> 抓取时间：2026-07-14 08:20 (GMT+8)。主数据源 GitHub Trending 日榜；curl 直连被沙箱阻断（HTTP:000），改用 WebFetch 抓取 + GitHub REST API（WebFetch 可达）补全 created_at / stars。

## 🔝 今日最佳开源项目

**Graphify-Labs/graphify** — [仓库链接](https://github.com/Graphify-Labs/graphify)
⭐ **84.7k** ｜ 今日 **+1,028⭐**
💡 一句话亮点：把任意代码库（代码 / SQL schema / R 脚本 / 文档 / 论文 / 图片 / 视频）变成**可查询知识图谱**的 AI 编码助手技能，原生兼容 Claude Code / Cursor / Codex / Gemini CLI 等主流编码 Agent。

---

## 📊 今日入选项目（按当日新增 Star 降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 简介 |
| - | ---- | ---- | --------- | ---- |
| 1 | [[Graphify-Labs_graphify\|Graphify-Labs/graphify]] | Graphify-Labs | 🔺1,028 | AI 编码助手技能，将代码/SQL/R/文档/图片/视频转成可查询知识图谱（Claude Code、Cursor、Codex、Gemini CLI 等通用） |
| 2 | [[Nutlope_hallmark\|Nutlope/hallmark]] | Nutlope | 🔺802 | 面向 Claude Code / Cursor / Codex 的「反 AI-slop」设计技能，拒绝生成千篇一律的模板页 |
| 3 | [[github_spec-kit\|github/spec-kit]] | github | 🔺508 | GitHub 官方出品的 Spec-Driven Development（规格驱动开发）上手工具包，深度对接 Copilot |
| 4 | [[coreyhaines31_marketingskills\|coreyhaines31/marketingskills]] | coreyhaines31 | 🔺260 | 面向 Claude Code 与 AI Agent 的营销技能集（CRO、文案、SEO、分析与增长工程） |
| 5 | [[addyosmani_agent-skills\|addyosmani/agent-skills]] | addyosmani | 🔺(近7日 +7.3k)* | 生产级工程技能框架，为 AI 编程 Agent 提供覆盖全生命周期的结构化工作流（兼容 70+ 工具） |

> \* agent-skills 今日「精确新增」因 GitHub Trending 日榜 WebFetch 被截断至前 11 位未能直接读取，采用 findarepo 镜像的近 7 日动量（+7.3k）作为代理；该仓库已确认位于今日日榜尾段。详见「严格关键词命中说明」。

---

## 🧭 今日趋势解读

**「技能（Skills）」成为 Vibe Coding 绝对主线。** 今日 5 个入选项目全部属于「技能 / 工程纪律」类，且清一色面向 Claude Code / Cursor / Codex 生态：

- **知识图谱技能**（graphify）：让 Agent 把整库代码 + 数据库 schema + 基础设施建成一张图，检索与推理更省 token；
- **反 AI-slop 设计技能**（hallmark）：把 Vibe Coding 的战场从「能生成」推向「生成得好看且不像 AI」；
- **规格驱动开发**（github/spec-kit）：GitHub 官方亲自下场推 SDD，信号意义极强——先写 spec/PRD 再写代码正成为主流工作流；
- **垂直技能外延**（marketingskills）：技能正从纯工程向营销/增长等职能扩散；
- **生产级工程技能**（agent-skills）：将 Google 工程文化编码为 24 个可复用技能，定义行业质量基准。

**结论**：Claude Code / Cursor / Codex 的「技能层」已成型，竞争焦点从模型能力转向**技能质量与工程纪律**。GitHub 官方的 spec-kit 入榜，标志大厂正式把 SDD 推向标准实践。

---

## 🔎 严格关键词命中说明

- **严格关键词**（项目名/简介含 cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev）：
  - ✅ `Graphify-Labs/graphify` — 简介含 **Cursor**
  - ✅ `Nutlope/hallmark` — 简介含 **Cursor**
  - （共 **2** 个严格命中）
- **Vibe Coding / AI 编码 Agent 生态扩充**（Claude Code / Codex / Cursor / MCP / 编码 Agent / 技能）：因严格命中 < 5，按口径扩充至 Top 5（当日新增降序）：
  - `github/spec-kit` — Copilot 主题 + 规格驱动开发（AI 编码生态）
  - `coreyhaines31/marketingskills` — Claude Code 技能
  - `addyosmani/agent-skills` — AI coding agents 技能（主题亦含 cursor）
- **环境限制**：GitHub Trending 日榜经 WebFetch 仅稳定返回前 11 个仓库（沙箱对 github.com 直连 HTTP:000，WebFetch 服务存在分页截断），第 12–25 位未能直接解析；`agent-skills` 经 findarepo（GitHub 日榜镜像）确认为今日在榜，其「今日新增」以近 7 日动量 +7.3k 作代理并标注。其余 4 项「今日新增」均来自 GitHub Trending 日榜页面原始数值。

---

## 📎 相关链接

- 全局索引：[[_Index|GitHub AI 项目归档索引]]
- 昨日（2026-07-13）：[[Vibe-Coding-2026-07-13]]
