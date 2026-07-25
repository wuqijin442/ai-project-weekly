# GitHub AI 热门项目 · Vibe Coding 日报（2026-07-22）

> 数据来源：GitHub Trending 日榜 `?since=daily`（飙升榜，按当日新增 Star 降序）
> 模式：工作日 · Vibe Coding 赛道（严格关键词命中 1 个 + 生态扩充 4 个，取前 5）
> 归档时间：2026-07-22（周三）

## 🔝 今日最佳开源项目

**#1 OmniRoute** — diegosouzapw（今日 +2,034 ⭐，总 23.6k）
免费 MIT AI 网关，把 268+ 供应商 / 500+ 模型收口到「一个端点」，直接对接 Claude Code / Codex / Cursor / Cline / Copilot，RTK+Caveman 压缩省 15–95% token，由 500+ 贡献者共建。

---

## 一、分类总结（按赛道归类）

今日 5 个项目可归入 4 条 Vibe Coding 赛道，反映「编码 Agent 基建」正从模型能力向「接入层 → 上下文底座 → 技能层 → Agent 基座」逐层下沉：

| 赛道 | 项目 | 一句话归类 |
| --- | --- | --- |
| ① 接入层 / AI 网关 | OmniRoute | 统一接入多家模型厂 + token 成本压缩的编码 Agent 前置网关 |
| ② 代码上下文底座 | code-review-graph、wigolo | 给 Agent 喂最精准、最省 token 的上下文（图谱 / 联网检索） |
| ③ 技能层 / 输出风格 | i-have-adhd | 把 Agent 输出可读性封装成可安装技能 |
| ④ 编码 Agent 基座 | jcode | 终端 / Rust 打造的编码 Agent Harness |

**赛道解读**
- **接入层（新主线）**：OmniRoute 登顶标志竞争上移到「统一接入 + 成本压缩」——编码 Agent 不再各自对接模型厂，而是经网关统一路由、自动 fallback 与压缩。
- **代码上下文底座（固化双雄）**：code-review-graph（本地优先代码智能图谱）+ wigolo（本地优先联网检索）连续多日同榜，是 Agent 跑得准、跑得省的底层设施。
- **技能层（走向风格封装）**：i-have-adhd 首入榜，把「先给结论、步骤编号、不寒暄」的输出风格做成 Claude Code / Codex 插件，技能从「能力封装」延伸到「交互风格封装」。
- **编码 Agent 基座（稳健）**：jcode（Rust harness）三度上榜，跨平台、多会话、低开销定位延续。

---

## 二、上榜项目总览（按当日新增 Star 降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 总 Star | 语言 | 一句话 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | OmniRoute | diegosouzapw | 🔺2,034 | 23.6k | TypeScript | 免费 AI 网关，统一接入 268+ 供应商/500+ 模型，省 15–95% token |
| 2 | code-review-graph | tirth8205 | 🔺1,925 | 24.5k | Python | 本地优先代码智能图谱，Tree-sitter+MCP 只读取「爆炸半径」内文件 |
| 3 | i-have-adhd | ayghri | 🔺1,866 | 6.8k | —（Skill） | 编码 Agent 输出风格插件，先给结论、步骤编号、不寒暄 |
| 4 | jcode | 1jehuang | 🔺843 | 10.3k | Rust | 新一代 Coding Agent Harness，面向多会话工作流、无限可定制 |
| 5 | wigolo | KnockOutEZ | 🔺642 | 3.1k | TypeScript | 本地优先 AI 编码 Agent 联网检索，无 key、零查询成本、MCP 接入 |

---

## 三、项目详情

### 1. OmniRoute（接入层 / AI 网关）
- **地址**：https://github.com/diegosouzapw/OmniRoute ｜ **作者**：diegosouzapw
- **⭐ 总 Star**：23,568（23.6k）｜ **今日新增**：2,034 ｜ **语言**：TypeScript ｜ **开源时间**：2026-02-13
- **定位**：免费（MIT）AI 网关 / LLM Router。把 268+ 供应商（50+ 免费）的 500+ 模型收口到「一个端点」，让 Claude Code / Codex / Cursor / OpenCode / Cline / Copilot 统一接入；配额感知的自动 fallback，RTK + Caveman 堆叠压缩省 15–95% token（均值约 89%），支持 MCP / A2A 与 Desktop / PWA。
- **技术栈**：TypeScript；聚合 39 个供应商池 / 460+ 模型免费层（约 1.4B 免费 token/月）；MCP / A2A；18 种路由策略；RTK+Caveman 压缩。
- **严格命中**：简介与 topics 显式含 cursor / cline / copilot。

### 2. code-review-graph（代码上下文底座）
- **地址**：https://github.com/tirth8205/code-review-graph ｜ **作者**：tirth8205
- **⭐ 总 Star**：24,527（24.5k）｜ **今日新增**：1,925 ｜ **语言**：Python ｜ **开源时间**：2026-02-26
- **定位**：本地优先代码智能图谱，用 Tree-sitter 为代码库构建结构化持久化映射（函数、类、调用/继承等关系边），经 MCP / CLI 让 AI 编码工具只读取受变更影响的「最小文件集合」（爆炸半径分析）。基准测试实现 38×–528× 上下文缩减。
- **技术栈**：Tree-sitter（AST，30+ 语言）；本地 SQLite 图谱；Leiden 社区检测 / Betweenness 中心性 / 爆炸半径分析；可选向量嵌入 + FTS5；MCP（30 工具 + 5 Prompt）、CLI、GitHub Action。
- **备注**：四度上榜，今日被 OmniRoute 挤下榜首但仍居 #2。

### 3. i-have-adhd（技能层 / 输出风格）
- **地址**：https://github.com/ayghri/i-have-adhd ｜ **作者**：ayghri
- **⭐ 总 Star**：6,828（6.8k）｜ **今日新增**：1,866 ｜ **语言**：—（Claude Code / Codex 插件 / Skill 仓库）｜ **开源时间**：2026-05-13
- **定位**：面向编码 Agent 的输出风格 Skill / 插件。把助手「埋答案」的啰嗦输出改造成「先给结论（Action first）、步骤编号、不寒暄」的 ADHD 友好格式。支持 Claude Code 与 Codex 插件市场一行命令安装，无需本地 clone。
- **技术栈**：Claude Code Plugin / Codex Plugin（Skill 定义）；`claude plugin marketplace add ayghri/i-have-adhd`；`codex plugin marketplace add ayghri/i-have-adhd`。
- **备注**：首入榜即居 #3，标志技能层从能力封装走向输出风格封装。

### 4. jcode（编码 Agent 基座）
- **地址**：https://github.com/1jehuang/jcode ｜ **作者**：1jehuang
- **⭐ 总 Star**：10,300（10.3k）｜ **今日新增**：843 ｜ **语言**：Rust ｜ **开源时间**：2026-01-05
- **定位**：新一代 Coding Agent Harness（编码代理基座），定位「抬升技能上限」。面向多会话工作流、无限可定制与高性能，跨 Linux / macOS / Windows，内置记忆系统，强调 RAM 与启动速度优化。
- **技术栈**：Rust（编译型跨平台二进制 + TUI）；终端编码 Agent / Harness，多会话并行；Claude / OpenAI 接入；MCP。
- **备注**：三度上榜，今日新增较昨日（568）明显放大。

### 5. wigolo（代码上下文底座）
- **地址**：https://github.com/KnockOutEZ/wigolo ｜ **作者**：KnockOutEZ
- **⭐ 总 Star**：3,136（3.1k）｜ **今日新增**：642 ｜ **语言**：TypeScript ｜ **开源时间**：2026-04-12
- **定位**：本地优先的 AI 编码 Agent 联网研究与检索工具。经 MCP 提供 search / fetch / crawl / research 能力，无云端 API、零查询成本。原生对接 Claude Code · Cursor · Codex · Gemini CLI · VS Code · Windsurf · Zed · Antigravity。
- **技术栈**：TypeScript / Node.js（metasearch）；MCP server；web-search / web-scraping / RAG；local-first、privacy 优先。
- **备注**：三度上榜，与 code-review-graph 共筑上下文工程双底座。

---

## 四、今日趋势解读

1. **「AI 网关 / 路由」接管编码 Agent 接入层**：OmniRoute 以 +2,034 登顶，把 268+ 供应商 / 500+ 模型收口到「一个端点」，RTK+Caveman 压缩省 15–95% token——编码 Agent 竞争上移到「统一接入 + 成本压缩」层。
2. **「代码上下文底座」双雄依旧**：code-review-graph（+1,925）+ wigolo（+642）再同榜，code-review-graph 由 #1 降至 #2 但新增几近持平，wigolo 三度上榜，持续领跑上下文工程基础设施。
3. **「Agent 输出风格 / 技能层」新面孔**：i-have-adhd（+1,866，#3）首入榜，把 Agent 输出可读性做成可安装技能，技能层从能力封装走向交互风格封装。
4. **Rust / CLI 编码 Agent 基座稳健**：jcode（Rust harness，+843）三度上榜，跨平台、多会话、低开销定位延续。

---

## 五、严格关键词命中说明与边界

- **严格关键词**（cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev）：**本日 1 命中** → OmniRoute（cursor / cline / copilot）。
- **生态扩充口径**：命中不足 5 时按 Vibe Coding / AI 编码 Agent 生态（Claude Code / Codex / Cursor / MCP / 编码 Agent / 技能）扩充，补足至前 5：code-review-graph、i-have-adhd、jcode、wigolo。
- **边界排除**：bojieli/ai-agent-book（+4,624，当日总榜 #2）为 AI Agent 工程教材（教育内容，非编码工具，按口径排除）；agegr/pi-web（+298，pi coding agent UI）、tradesdontlie/tradingview-mcp（+114，Claude Code 交易 MCP）为更低新增的生态候选，未进 Top 5。

---

## 六、关联归档

- Obsidian 知识库：Daily/Vibe-Coding-2026-07-22.md（日报）+ Projects/{owner}_{repo}.md（5 个项目详情页）
- 自动化执行日志：logs/task_2026-07-22.log
