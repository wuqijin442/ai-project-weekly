# -*- coding: utf-8 -*-
import json, os

BASE = r"D:\Users\Administrator\Desktop\AI Project Weekly\Obsidian_Vault"
TMP = r"D:\Users\Administrator\Desktop\AI Project Weekly\.workbuddy\tmp"
DATE = "2026-07-16"
meta = {e['full']: e for e in json.load(open(os.path.join(TMP, "selected_meta.json"), encoding='utf-8'))}

def compact(n):
    n = int(n)
    if n >= 1000:
        v = n / 1000.0
        return f"{v:.1f}k".replace('.0k', 'k')
    return str(n)

# ordered selection (today desc): protect strict + fill by stars
ORDER = ["mattpocock/skills", "Nutlope/hallmark", "HKUDS/Vibe-Trading",
         "Dicklesworthstone/destructive_command_guard", "openinterpreter/openinterpreter"]

# curated positioning + tech + tags + aliases + reverse-links
INFO = {
 "mattpocock/skills": dict(
    alias="skills",
    tags=["AI","Trending","Shell","Claude-Code","Skills","Vibe-Coding","Engineering"],
    pos="Matt Pocock（Total TypeScript 作者）日常在真实工程中使用的 **AI Agent 技能集**，定位「为真实工程师服务，而非 vibe coding」。强调技能**小而可组合、跨模型通用**，基于数十年工程经验沉淀；与 GSD / BMAD / Spec-Kit 等「接管流程」方案不同，这些技能保留开发者控制权，便于 hack 与改造。安装：`npx skills@latest add mattpocock/skills`。",
    tech=["形态：纯 Markdown 技能文件（SKILL.md），通过 skills.sh 分发","运行：Shell 安装脚本；兼容任意模型与 Agent（Claude Code 等）","设计哲学：可组合、易适配、工程纪律优先"],
    rlinks=["2026-07-11","2026-07-15","2026-07-16"],
    note="由 GitHub Trending 日榜自动归档（Vibe Coding / AI 编码 Agent 生态口径；Claude Code 技能层代表）。今日 +2,130 登顶 Vibe Coding 榜首，总 Star 17.2 万，稳居「技能即工程纪律」赛道头部。",
 ),
 "Nutlope/hallmark": dict(
    alias="hallmark",
    tags=["AI","Trending","CSS","Claude-Code","Cursor","Codex","Skills","Design","Anti-Slop"],
    pos="Together AI 出品的「**反 AI-slop**」设计技能，兼容 Claude Code / Cursor / Codex。为设计 brief 自动选取宏观结构、套用 20 套主题，跑 **57 道 slop-test 门禁 + 发射前自批判**，拒绝 LLM 训练出的「套路化默认值」，让两个不同 brief 生成截然不同的站点而非同款换色。",
    tech=["形态：设计技能（Skill）+ CSS 主题系统","能力：20 主题 × 4 动词，57 道 slop-test 门禁 + 自批判","兼容：Claude Code / Cursor / Codex"],
    rlinks=["2026-07-06","2026-07-07","2026-07-10","2026-07-13","2026-07-14","2026-07-15","2026-07-16"],
    note="由 GitHub Trending 日榜自动归档（严格关键词命中：简介含 Cursor）。今日 +1,277，连续多日稳居 Vibe Coding 榜单，把「能生成」推向「生成得好看且不像 AI」。",
 ),
 "HKUDS/Vibe-Trading": dict(
    alias="Vibe-Trading",
    tags=["AI","Trending","Python","MCP","Multi-Agent","Trading","Vibe-Coding","Fintech"],
    pos="港大 HKUDS 出品的「**你的私人交易 Agent**」——一条命令赋予 Agent 全面交易能力；基于 **LLM 多智能体 + MCP**，覆盖量化交易、回测、finbench 等场景，是 Vibe 范式从「写代码」向「金融决策」外溢的代表作。",
    tech=["语言：Python","架构：LLM 多智能体 + MCP 工具调用","领域：algorithmic-trading / backtesting / fintech / quantitative-finance"],
    rlinks=["2026-07-15","2026-07-16"],
    note="由 GitHub Trending 日榜自动归档（Vibe Coding / AI 编码 Agent 生态口径；MCP + 多智能体）。今日 +915，延续 Vibe 范式向金融外溢的主线。",
 ),
 "Dicklesworthstone/destructive_command_guard": dict(
    alias="dcg",
    tags=["AI","Trending","Rust","Agent-Safety","CLI","Git","Vibe-Coding"],
    pos="**dcg（Destructive Command Guard）**——面向 AI 编码代理的**高性能钩子**，在破坏性命令执行前拦截，保护代码免遭 Agent 误删；兼容 Claude Code / Codex CLI / Gemini CLI / Copilot CLI / VS Code Copilot Chat / Cursor。是 Vibe Coding 走向生产可用的一道安全护栏。",
    tech=["语言：Rust（高性能、亚毫秒级拦截）","形态：CLI hook，集成各编码 Agent 的 pre-tool 钩子","场景：拦截 git reset --hard / rm -rf 等破坏性命令"],
    rlinks=["2026-07-13","2026-07-15","2026-07-16"],
    note="由 GitHub Trending 日榜自动归档（Vibe Coding / AI 编码 Agent 生态口径；代理安全）。今日 +471，本周多次入榜，守住「代理安全」主线。",
 ),
 "openinterpreter/openinterpreter": dict(
    alias="openinterpreter",
    tags=["AI","Trending","Rust","Coding-Agent","Vibe-Coding","Multi-Model"],
    pos="知名开源 **编码 Agent**，专为**低成本模型**优化，让模型直接运行代码完成多步任务；支持 DeepSeek / Qwen / Kimi 等多模型（ACP 协议）。今日以严格关键词（open-interpreter）语义匹配回归榜单。",
    tech=["语言：Rust 核心 + 多模型适配","协议：ACP（Agent Client Protocol）","定位：coding-agent，低成本模型优先"],
    rlinks=["2026-07-02","2026-07-16"],
    note="由 GitHub Trending 日榜自动归档（严格关键词语义匹配：open-interpreter；仓库名无连字符，按项目意图计入）。今日 +299 回归，老牌开源编码 Agent 持续受关注。",
 ),
}

# ---- 1. project pages ----
for full in ORDER:
    m = meta[full]
    info = INFO[full]
    owner, repo = m['owner'], m['repo']
    fname = f"{owner}_{repo}.md"
    stars_c = compact(m['stars'])
    today_n = int(m['today'])
    rl = "\n".join(f"- [[Vibe-Coding-{d}|{d} 日报]]" for d in info['rlinks'])
    tags = info['tags']
    body = f"""---
aliases: [{info['alias']}]
tags: [{', '.join(tags)}]
stars: {m['stars']}
created_at: {m['created_at']}
today_growth: {today_n}
status: 热门
date_accessed: {DATE}

# {repo}

**项目地址**：{m['url']}
**作者**：{owner}
**⭐ 总 Star**：{m['stars']:,}（{stars_c}）
**📈 今日新增**：{today_n:,} stars
**💻 主要语言**：{m['language']}
**🗓 开源时间**：{m['created_at']}

## 项目定位

{info['pos']}

## 技术栈

{chr(10).join('- ' + t for t in info['tech'])}

## 外部链接

- GitHub：{m['url']}
- 作者：https://github.com/{owner}

## 相关日期

{rl}

## 备注

- {info['note']}
"""
    open(os.path.join(BASE, "Projects", fname), 'w', encoding='utf-8').write(body)
    print("WROTE Project:", fname)

# ---- 2. daily index ----
top = meta["mattpocock/skills"]
top_c = compact(top['stars'])
# build table rows with curated short desc
SHORT = {
 "mattpocock/skills":"日常真实工程使用的 AI Agent 技能集（.claude 目录沉淀），小而可组合、跨模型通用，今日新增登顶",
 "Nutlope/hallmark":"面向 Claude Code / Cursor / Codex 的「反 AI-slop」设计技能（Together AI），57 道 slop-test 门禁拒绝套路化生成",
 "HKUDS/Vibe-Trading":"个人交易 Agent——LLM 多智能体 + MCP 量化交易系统（backtesting + fintech）",
 "Dicklesworthstone/destructive_command_guard":"面向 AI 编码代理的高性能 Rust 钩子，拦截 git reset --hard / rm -rf 等破坏性命令",
 "openinterpreter/openinterpreter":"知名开源编码 Agent，专为低成本模型优化，让模型直接运行代码完成多步任务",
}
table_rows = []
for i, full in enumerate(ORDER, 1):
    m = meta[full]; owner, repo = m['owner'], m['repo']; today_n = int(m['today'])
    table_rows.append(f"| {i} | [[{owner}_{repo}|{owner}/{repo}]] | {owner} | 🔺{today_n:,} | {SHORT[full]} |")

daily = f"""---
date: {DATE}
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [AI, Trending, Vibe-Coding, 飙升榜, Claude-Code, Cursor, Codex, Skills, Agent-Safety, MCP]
source: GitHub Trending 日榜（github.com/trending?since=daily，curl 直连 HTTP:200）+ GitHub REST API（curl 直连 HTTP:200）

# GitHub AI 项目 · Vibe Coding 日报（{DATE}）

> 数据口径：**GitHub Trending 日榜「飙升榜」**（按当日新增 Star 降序）＋ 严格关键词 + Vibe Coding / AI 编码 Agent 生态扩充。
> 抓取时间：{DATE} 08:20 (GMT+8)。主数据源 GitHub Trending 日榜（curl 直连 HTTP:200，获取 608KB 页面，解析 13 个仓库）；GitHub REST API（curl 直连 HTTP:200，Bearer Token）补全 created_at / stars / 语言 / topics；README 经 API `/readme` 端点获取并提炼定位与技术栈。

## 🔝 今日最佳开源项目

**{top['owner']}/{top['repo']}** — [仓库链接]({top['url']})
⭐ **{top_c}** ｜ 今日 **+{int(top['today']):,}⭐**
💡 一句话亮点：Matt Pocock（Total TypeScript）日常真实工程使用的 **AI Agent 技能集**，主张「为真实工程师服务，而非 vibe coding」，小巧可组合、跨模型通用——今日以 **+{int(top['today']):,}** 新增登顶 Vibe Coding 榜首（总 Star {top_c}）。

---

## 📊 今日入选项目（按当日新增 Star 降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 简介 |
| - | ---- | ---- | --------- | ---- |
{chr(10).join(table_rows)}

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
"""
open(os.path.join(BASE, "Daily", f"Vibe-Coding-{DATE}.md"), 'w', encoding='utf-8').write(daily)
print("WROTE Daily: Vibe-Coding-%s.md" % DATE)
