import json

V = "Obsidian_Vault"

# ---------- Project pages ----------
omni = """---
aliases: [OmniRoute]
tags: [AI, Trending, TypeScript, AI-Gateway, LLM-Router, MCP, Claude-Code, Cursor, Codex, Copilot, Cline, Vibe-Coding]
stars: 23568
created_at: 2026-02-13
today_growth: 2034
status: 新兴（严格关键词命中）
date_accessed: 2026-07-22

# OmniRoute

**项目地址**：https://github.com/diegosouzapw/OmniRoute
**作者**：diegosouzapw
**⭐ 总 Star**：23,568（23.6k）
**📈 今日新增**：2,034 stars（严格关键词命中：cursor / cline / copilot）
**💻 主要语言**：TypeScript
**🗓 开源时间**：2026-02-13

## 项目定位

免费（MIT）的 **AI 网关 / LLM Router**。把 **268+ 供应商（50+ 免费）的 500+ 模型**收口到「一个端点」，让 Claude Code / Codex / Cursor / OpenCode / Cline / Copilot 等编码工具统一接入；配额感知的自动 fallback，RTK + Caveman 堆叠压缩可省 **15–95%** token（均值约 89%），并支持 MCP / A2A 协议与 Desktop / PWA。由 500+ 贡献者共建，口号「Never stop coding」。

一句话：把「多供应商接入 + 成本压缩 + 故障转移」做成编码 Agent 的统一前置网关。

## 技术栈

- **形态**：AI Gateway / LLM Router（MIT 协议，免费层聚合）
- **语言/运行时**：TypeScript；Desktop / PWA 双端
- **模型接入**：268+ 供应商 / 500+ 模型（Kimi、Claude、GPT、OpenAI、Gemini、GLM、DeepSeek、MiniMax 等），含 39 个供应商池 / 460+ 模型的免费层聚合（约 1.4B 免费 token/月）
- **协议**：MCP / A2A；18 种路由策略
- **压缩**：RTK + Caveman 堆叠压缩，省 15–95% token
- **Topics**：ai-gateway, llm-gateway, claude-code, cursor, codex, copilot, cline, mcp, a2a, token-saver, free-ai

## 外部链接

- GitHub：https://github.com/diegosouzapw/OmniRoute
- 作者：https://github.com/diegosouzapw
- 官网：https://omniroute.online

## 相关日期

- [[Vibe-Coding-2026-07-22|2026-07-22 日报]]

## 备注

- 由 GitHub Trending 日榜自动归档（**严格关键词命中**：项目简介与 topics 显式包含 cursor / cline / copilot，且兼容 Claude Code / Codex）。2026-07-22 居 Vibe Coding #1（🔝今日 +2,034，23.6k），标志 Vibe Coding 竞争上移至「统一接入 + 成本压缩」层——编码 Agent 不再各自对接模型厂，而是经网关统一路由、自动 fallback 与 token 压缩。
"""

adhd = """---
aliases: [i-have-adhd]
tags: [AI, Trending, Skill, Claude-Code, Codex, Coding-Agent, Productivity, Vibe-Coding]
stars: 6828
created_at: 2026-05-13
today_growth: 1866
status: 新兴（Public）
date_accessed: 2026-07-22

# i-have-adhd

**项目地址**：https://github.com/ayghri/i-have-adhd
**作者**：ayghri
**⭐ 总 Star**：6,828（6.8k）
**📈 今日新增**：1,866 stars
**💻 主要语言**：—（Claude Code / Codex 插件 / Skill 仓库，主要为 Markdown 提示词定义）
**🗓 开源时间**：2026-05-13

## 项目定位

面向「编码 Agent」的**输出风格 Skill / 插件**。核心诉求是把编码助手「埋答案」的啰嗦输出改造成「先给结论（Action first）、步骤编号、不寒暄（无 'Hope this helps!'）」的 ADHD 友好格式。支持 Claude Code 与 Codex 插件市场一行命令安装，无需本地 clone。

一句话：把「Agent 输出可读性」封装成可安装技能——技能层从「能力封装」延伸到「交互风格封装」。

## 技术栈

- **形态**：Claude Code Plugin / Codex Plugin（Skill 定义）
- **安装**：`claude plugin marketplace add ayghri/i-have-adhd`；`codex plugin marketplace add ayghri/i-have-adhd`
- **语言/运行时**：配置 / 提示词仓库（无编译型主语言）
- **Topics**：claude-skills, claude-code-plugin, developer-tools, productivity, adhd

## 外部链接

- GitHub：https://github.com/ayghri/i-have-adhd
- 作者：https://github.com/ayghri

## 相关日期

- [[Vibe-Coding-2026-07-22|2026-07-22 日报]]

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding 生态扩充命中：简介「A skill for your coding agent」+ topics 含 claude-skills / claude-code-plugin / coding-agent）。2026-07-22 首入榜即居 Vibe Coding #3（+1,866，6.8k），与既往 skills / hallmark 一脉相承，标志「技能层」从能力封装走向输出风格封装。
"""

# code-review-graph (UPDATE)
crg_old = open(f"{V}/Projects/tirth8205_code-review-graph.md", encoding='utf-8').read()
crg_new = crg_old
crg_new = crg_new.replace("stars: 23122", "stars: 24527")
crg_new = crg_new.replace("today_growth: 1833", "today_growth: 1925")
crg_new = crg_new.replace("date_accessed: 2026-07-21", "date_accessed: 2026-07-22")
crg_new = crg_new.replace("**⭐ 总 Star**：23,122（23.1k）", "**⭐ 总 Star**：24,527（24.5k）")
crg_new = crg_new.replace("**📈 今日新增**：1,833 stars", "**📈 今日新增**：1,925 stars")
crg_new = crg_new.replace("- [[Vibe-Coding-2026-07-21|2026-07-21 日报]]",
                          "- [[Vibe-Coding-2026-07-21|2026-07-21 日报]]\n- [[Vibe-Coding-2026-07-22|2026-07-22 日报]]")
crg_new = crg_new.rstrip() + "\n- 2026-07-22 居 Vibe Coding #2（+1,925，24.5k，四度上榜），新增较昨日（1,833）略升，被新面孔 OmniRoute（+2,034）挤下榜首，但仍是「代码上下文底座」双雄之一，持续领跑本地优先代码智能图谱赛道。\n"
open(f"{V}/Projects/tirth8205_code-review-graph.md","w",encoding='utf-8').write(crg_new)

# jcode (UPDATE)
jc_old = open(f"{V}/Projects/1jehuang_jcode.md", encoding='utf-8').read()
jc_new = jc_old
jc_new = jc_new.replace("stars: 9620","stars: 10300")
jc_new = jc_new.replace("today_growth: 568","today_growth: 843")
jc_new = jc_new.replace("date_accessed: 2026-07-21","date_accessed: 2026-07-22")
jc_new = jc_new.replace("**⭐ 总 Star**：9,620（9.6k）","**⭐ 总 Star**：10,300（10.3k）")
jc_new = jc_new.replace("**📈 今日新增**：568 stars","**📈 今日新增**：843 stars")
jc_new = jc_new.replace("- [[Vibe-Coding-2026-07-21|2026-07-21 日报]]",
                         "- [[Vibe-Coding-2026-07-21|2026-07-21 日报]]\n- [[Vibe-Coding-2026-07-22|2026-07-22 日报]]")
jc_new = jc_new.rstrip() + "\n- 2026-07-22 居 Vibe Coding #4（+843，10.3k，三度上榜），新增较昨日（568）明显放大，Rust/CLI 编码 Agent 基座赛道持续升温，跨平台、多会话、低开销定位延续。\n"
open(f"{V}/Projects/1jehuang_jcode.md","w",encoding='utf-8').write(jc_new)

# wigolo (UPDATE)
wg_old = open(f"{V}/Projects/KnockOutEZ_wigolo.md", encoding='utf-8').read()
wg_new = wg_old
wg_new = wg_new.replace("stars: 2536","stars: 3136")
wg_new = wg_new.replace("today_growth: 689","today_growth: 642")
wg_new = wg_new.replace("date_accessed: 2026-07-21","date_accessed: 2026-07-22")
wg_new = wg_new.replace("**⭐ 总 Star**：2,536（2.5k）","**⭐ 总 Star**：3,136（3.1k）")
wg_new = wg_new.replace("**📈 今日新增**：689 stars","**📈 今日新增**：642 stars")
wg_new = wg_new.replace("- [[Vibe-Coding-2026-07-21|2026-07-21 日报]]",
                         "- [[Vibe-Coding-2026-07-21|2026-07-21 日报]]\n- [[Vibe-Coding-2026-07-22|2026-07-22 日报]]")
wg_new = wg_new.rstrip() + "\n- 2026-07-22 居 Vibe Coding #5（+642，3.1k，三度上榜），新增较昨日（689）小幅回落，仍稳居「编码 Agent 联网检索」local-first 底座，与 code-review-graph 共筑上下文工程双底座。\n"
open(f"{V}/Projects/KnockOutEZ_wigolo.md","w",encoding='utf-8').write(wg_new)

# write new ones
open(f"{V}/Projects/diegosouzapw_OmniRoute.md","w",encoding='utf-8').write(omni)
open(f"{V}/Projects/ayghri_i-have-adhd.md","w",encoding='utf-8').write(adhd)
print("Project pages done.")

# ---------- Daily report ----------
daily = """---
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
| 1 | [[diegosouzapw_OmniRoute\\|OmniRoute]] | diegosouzapw | 🔺2,034 | 23.6k | 免费 MIT AI 网关，一个端点接入 268+ 供应商/500+ 模型，对接 Claude Code/Codex/Cursor/Cline/Copilot，省 15–95% token |
| 2 | [[tirth8205_code-review-graph\\|code-review-graph]] | tirth8205 | 🔺1,925 | 24.5k | 本地优先代码智能图谱，Tree-sitter+MCP 让 AI 编码工具只读取「爆炸半径」内文件，基准 38×–528× 上下文缩减 |
| 3 | [[ayghri_i-have-adhd\\|i-have-adhd]] | ayghri | 🔺1,866 | 6.8k | 编码 Agent 输出风格 Skill（Claude Code/Codex 插件），先给结论、步骤编号、不寒暄的 ADHD 友好格式 |
| 4 | [[1jehuang_jcode\\|jcode]] | 1jehuang | 🔺843 | 10.3k | 新一代 Coding Agent Harness，Rust 打造，面向多会话工作流、无限可定制与高性能 |
| 5 | [[KnockOutEZ_wigolo\\|wigolo]] | KnockOutEZ | 🔺642 | 3.1k | 本地优先的 AI 编码 Agent 联网检索（search/fetch/crawl），无 key、零查询成本，MCP 接入 |

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
"""
open(f"{V}/Daily/Vibe-Coding-2026-07-22.md","w",encoding='utf-8').write(daily)
print("Daily report done.")

# ---------- _Index.md update ----------
idx = open(f"{V}/_Index.md", encoding='utf-8').read()
idx = idx.replace("| 2026-07-21 | 工作日（Vibe Coding） | 5 | [[Vibe-Coding-2026-07-21]] |",
                  "| 2026-07-22 | 工作日（Vibe Coding） | 5 | [[Vibe-Coding-2026-07-22]] |\n| 2026-07-21 | 工作日（Vibe Coding） | 5 | [[Vibe-Coding-2026-07-21]] |")
new_proj = """| diegosouzapw/OmniRoute | [[diegosouzapw_OmniRoute|详情]] |
| ayghri/i-have-adhd | [[ayghri_i-have-adhd|详情]] |
"""
if "diegosouzapw_OmniRoute" not in idx:
    idx = idx.replace("| KnockOutEZ/wigolo | [[KnockOutEZ_wigolo|详情]] |",
                      "| KnockOutEZ/wigolo | [[KnockOutEZ_wigolo|详情]] |\n"+new_proj)
open(f"{V}/_Index.md","w",encoding='utf-8').write(idx)
print("Index updated.")
