---
date: 2026-07-18
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [GitHub, Trending, Vibe-Coding, AI, Coding-Agent]
source: GitHub Trending 日榜（https://github.com/trending?since=daily，WebFetch 兜底）
---

# GitHub AI 项目日报 · Vibe Coding 赛道（2026-07-18，周六）

> 数据口径：GitHub Trending 全局日榜按「今日新增 Star」降序；Vibe Coding 赛道 = 严格关键词命中 + 生态扩充取前 5。
> ⚠️ 环境限制：沙箱 curl 直连 github.com 被阻断（HTTP:000），本次仅经 WebFetch 抓取 Trending 页 + GitHub REST API 补全元数据；WebFetch 对 Trending 页 summarizer 硬截断于第 14 个仓库（共应 25 个），第 15–25 位尾部不可达，故 #4/#5 排名基于已获取 14 仓，可能存在尾部遗漏风险。

## 🔝 今日最佳开源项目

**[[Nutlope_hallmark|Nutlope/hallmark]]** — Anti-AI-slop 设计技能，兼容 Claude Code / Cursor / Codex
- 🔗 https://github.com/Nutlope/hallmark
- ⭐ 总 Star：**12.0k** ｜ 📈 今日新增：**🔺1,486**
- 💡 一句话亮点：把「能生成」推向「生成得好看且不像 AI」，多日连榜稳居 Vibe Coding 榜首。

## 📊 今日入榜项目（Top 5，按今日新增 Star 降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 总 Star | 语言 | 一句话简介 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 🔝 | [[Nutlope_hallmark\|Nutlope/hallmark]] | Nutlope | 🔺1,486 | 12.0k | CSS | 反 AI-slop 设计技能，兼容 Claude Code / Cursor / Codex |
| 2 | [[openinterpreter_openinterpreter\|openinterpreter/openinterpreter]] | openinterpreter | 🔺431 | 66.4k | Rust | 面向 Kimi/Qwen/DeepSeek 等开放模型的开源编码 Agent |
| 3 | [[github_copilot-sdk\|github/copilot-sdk]] | github | 🔺234 | 9.8k | Java | 把 GitHub Copilot Agent 能力 SDK 化的多平台官方 SDK |
| 4 | [[tirth8205_code-review-graph\|tirth8205/code-review-graph]] | tirth8205 | 🔺57 | 19.7k | Python | 本地优先代码智能图谱，MCP+CLI 让 AI 只读该读的代码 |
| 5 | [[anthropics_cwc-workshops\|anthropics/cwc-workshops]] | anthropics | 🔺37 | 1.6k | TypeScript | Anthropic 官方「Code with Claude」八大工作坊教材 |

## 🧭 今日趋势解读

1. **「大厂把编码 Agent 标准化」双线齐发**：`github/copilot-sdk`（#3）把 Copilot Agent 能力做成多语言 SDK；`anthropics/cwc-workshops`（#5）把「怎么用好 Claude Code」做成开源工作坊教材——能力 SDK 化 + 最佳实践教材化同步推进。
2. **「反套路化设计」成持续主线**：`Nutlope/hallmark`（#1）连续多日登顶，反映社区从「AI 能生成界面」转向「生成得好看、不像 AI slop」的审美升级需求。
3. **MCP 从连接协议演进为代码智能底座**：`code-review-graph`（#4）用 MCP+CLI 把代码库变成可查询的图谱，让编码 Agent 只读取变更影响的最小文件集（38×–528× 上下文缩减），是 MCP 实用化的标杆案例。
4. **老牌开源编码 Agent 稳健回归**：`openinterpreter`（#2）以 Rust 重构 + 开放模型（Kimi/Qwen/DeepSeek）路线稳居头部，印证「低成本模型 + 本地沙箱」路线仍具强吸引力。

## 🎯 严格关键词命中说明

- **严格关键词集**：cursor, cline, aider, continue, swe-agent, open-interpreter, browser-use, gpt-engineer, meta-gpt, devin, autocode, copilot, cli-agent, code-generator, llm-dev。
- **严格命中 3 个**：
  - `Nutlope/hallmark` — 简介含 **cursor**（兼容 Claude Code / Cursor / Codex）✓
  - `openinterpreter/openinterpreter` — 语义词匹配 **open-interpreter**（仓库名无连字符，按项目意图计入，与历史口径一致）✓
  - `github/copilot-sdk` — 项目名/简介含 **copilot** ✓
- **生态扩充 2 个**（严格不足 5，按 Vibe Coding / AI 编码 Agent 生态：Claude Code / MCP / 编码 Agent / 技能 等口径）：
  - `tirth8205/code-review-graph` — topics 含 `ai-coding / claude-code / mcp`，定位为 AI 编程工具的代码上下文底座
  - `anthropics/cwc-workshops` — anthropics 官方 Claude Code 工作坊，涵盖 Skills / MCP / Managed Agents
- **边界排除说明**：同榜 `PostHog/posthog` 简介虽提及 "MCP" 与 "agents"，但其本质为产品分析/可观测性平台，非编码 Agent 工具，依赛道口径排除；`HKUDS/DeepTutor`、`maths-cs-ai-compendium` 等为 AI 学习/辅导类，非 Vibe Coding 工具，亦排除。
- **数据完整性风险**：Trending 页应含 25 仓，WebFetch 截断致第 15–25 位不可见；若尾部存在更高新增的 Vibe Coding 项目，可能进入 #4/#5 区间，本次基于已获取 14 仓尽力排名。
