---
date: 2026-07-22
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [GitHub, Trending, AI, Vibe-Coding, Daily]
source: https://github.com/trending?since=daily
---

# GitHub AI 项目日报 · Vibe Coding（2026-07-22）

> 数据源：GitHub Trending 日榜 `?since=daily`（飙升榜，按当日新增 Star 降序）
> 筛选口径：严格关键词命中 1 个（OmniRoute：cursor / cline / copilot）→ 按 Vibe Coding / AI 编码 Agent 生态扩充，取前 5

## 🔝 今日最佳开源项目

**#1 [[diegosouzapw_OmniRoute|OmniRoute]]** — diegosouzapw
- ⭐ 总 Star：**23.6k** ｜ 今日新增：**🔺2,034**
- 一句话亮点：免费 MIT AI 网关，把 268+ 供应商 / 500+ 模型收口到「一个端点」，直接对接 Claude Code / Codex / Cursor / Cline / Copilot，RTK+Caveman 压缩省 15–95% token，由 500+ 贡献者共建。

---

## 📊 今日上榜项目（按当日新增 Star 降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 总 Star | 简介 |
| --- | --- | --- | --- | --- | --- |
| 1 | [[diegosouzapw_OmniRoute\|OmniRoute]] | diegosouzapw | 🔺2,034 | 23.6k | 免费 MIT AI 网关，一个端点接入 268+ 供应商/500+ 模型，对接 Claude Code/Codex/Cursor/Cline/Copilot，省 15–95% token |
| 2 | [[tirth8205_code-review-graph\|code-review-graph]] | tirth8205 | 🔺1,925 | 24.5k | 本地优先代码智能图谱，Tree-sitter+MCP 让 AI 编码工具只读取「爆炸半径」内文件，基准 38×–528× 上下文缩减 |
| 3 | [[ayghri_i-have-adhd\|i-have-adhd]] | ayghri | 🔺1,866 | 6.8k | 编码 Agent 输出风格 Skill（Claude Code/Codex 插件），先给结论、步骤编号、不寒暄的 ADHD 友好格式 |
| 4 | [[1jehuang_jcode\|jcode]] | 1jehuang | 🔺843 | 10.3k | 新一代 Coding Agent Harness，Rust 打造，面向多会话工作流、无限可定制与高性能 |
| 5 | [[KnockOutEZ_wigolo\|wigolo]] | KnockOutEZ | 🔺642 | 3.1k | 本地优先的 AI 编码 Agent 联网检索（search/fetch/crawl），无 key、零查询成本，MCP 接入 |

---

## 🧭 今日趋势解读

1. **「AI 网关 / 路由」接管编码 Agent 接入层**：`OmniRoute` 以 +2,034 登顶，定位免费 MIT AI 网关，把 268+ 供应商 / 500+ 模型收口到「一个端点」，直接对接 Claude Code / Codex / Cursor / Cline / Copilot，并用 RTK+Caveman 压缩省 15–95% token——标志 Vibe Coding 竞争进一步上移到「统一接入 + 成本压缩」层。
2. **「代码上下文底座」双雄依旧**：`code-review-graph`（图谱，+1,925）+ `wigolo`（联网检索，+642）再同榜，`code-review-graph` 由昨日 #1 降至 #2 但新增几近持平（1,925 vs 1,833），`wigolo` 三度上榜，持续领跑「上下文工程基础设施」。
3. **「Agent 输出风格 / 技能层」新面孔**：`i-have-adhd`（+1,866，居 #3）作为 Claude Code / Codex 插件形态的输出风格 Skill 首入榜——把「Agent 输出可读性」做成可安装技能，与既往 skills / hallmark 一脉相承，技能层从「能力封装」走向「交互风格封装」。
4. **Rust / CLI 编码 Agent 基座稳健**：`jcode`（Rust harness，+843）三度上榜，跨平台、多会话、低开销定位延续，印证「终端编码 Agent」仍是头部模型厂与独立团队共同下场的赛道。

---

## 🔎 严格关键词命中说明

- **严格关键词**（cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev）：**本日 1 命中**——`diegosouzapw/OmniRoute`（简介与 topics 显式包含 cursor / cline / copilot，并兼容 Claude Code / Codex）。
- **生态扩充口径**：命中不足 5 时按 Vibe Coding / AI 编码 Agent 生态（Claude Code / Codex / Cursor / MCP / 编码 Agent / 技能 等）扩充，补足至前 5（按当日新增降序）：
  - `code-review-graph`（MCP+CLI 代码智能图谱，topics 含 ai-coding / claude-code / mcp）
  - `i-have-adhd`（编码 Agent 输出风格 Skill，topics 含 claude-skills / claude-code-plugin / coding-agent）
  - `jcode`（Coding Agent Harness，topics 含 coding-agent / ai-coding-agent / mcp / rust）
  - `wigolo`（AI coding agent 联网检索，topics 含 mcp / mcp-server / claude / ai-agent）
- **边界说明**：同榜高新增但未纳入的候选——`bojieli/ai-agent-book`（+4,624，当日总榜 #2）为 AI Agent 工程教材（教育内容，非编码 Agent 工具，按口径排除）；`agegr/pi-web`（+298，pi coding agent UI）、`tradesdontlie/tradingview-mcp`（+114，Claude Code 交易 MCP）属更低新增的生态候选，未进 Top 5。
