# GitHub AI 热门项目 · Vibe Coding 日报（2026-07-23）

> 数据源：GitHub Trending 日榜（飙升榜，按当日新增 Star 降序）｜筛选：严格关键词 + Vibe Coding / AI 编码 Agent 生态扩充，取前 5。

## 🔝 今日最佳

**ayghri/i-have-adhd** — https://github.com/ayghri/i-have-adhd
- 总 Star：**8.3k** ｜ 今日新增：**🔺1699**
- 一句话亮点：把「编码 Agent 输出可读性」封装成可一行安装的输出风格 Skill——技能层从「能力封装」走向「交互风格封装」。

---

## 四赛道速览

| 赛道 | 代表项目 |
| --- | --- |
| 技能层（Skills） | i-have-adhd、awesome-claude-skills |
| 接入层 / 网关（Gateway） | OmniRoute |
| 代码上下文底座（Context） | code-review-graph |
| 可观测 / 工作台（UI/Tooling） | pi-web |

---

## 入选项目详情（按当日新增降序）

### 1. ayghri/i-have-adhd
- 链接：https://github.com/ayghri/i-have-adhd
- Star：8.3k ｜ 今日新增：🔺1699
- 标签：Skill, Claude-Code, Codex, Coding-Agent, Productivity
- 简介：面向编码 Agent 的输出风格 Skill——Action first、步骤编号、不寒暄（ADHD 友好），支持 Claude Code / Codex 插件市场一行安装。

### 2. diegosouzapw/OmniRoute
- 链接：https://github.com/diegosouzapw/OmniRoute
- Star：25.2k ｜ 今日新增：🔺1651（严格关键词命中：cursor / cline / copilot）
- 标签：AI-Gateway, LLM-Router, MCP, Claude-Code, Cursor, Codex, Copilot, Cline
- 简介：免费 MIT AI 网关，268+ 供应商 / 500+ 模型一端点接入 Claude Code / Codex / Cursor / OpenCode / Cline / Copilot；RTK+Caveman 压缩省 15–95% token，支持 MCP / A2A 与自动 fallback。

### 3. tirth8205/code-review-graph
- 链接：https://github.com/tirth8205/code-review-graph
- Star：25.3k ｜ 今日新增：🔺882
- 标签：MCP, Claude-Code, Coding-Agent, Code-Review, GraphRAG
- 简介：本地优先代码智能图谱（MCP + CLI），用 Tree-sitter 构建代码库持久化映射，让 AI 编码工具只读取受变更影响的最小文件集，基准 38×–528× 上下文缩减。

### 4. agegr/pi-web
- 链接：https://github.com/agegr/pi-web
- Star：2.1k ｜ 今日新增：🔺314
- 标签：Coding-Agent, Web-UI, Claude-Code
- 简介：编码 Agent「pi」的本地 Web UI——会话浏览、实时聊天、模型配置、技能管理与项目文件预览，把终端编码 Agent 搬到浏览器工作台。

### 5. ComposioHQ/awesome-claude-skills
- 链接：https://github.com/ComposioHQ/awesome-claude-skills
- Star：68.8k ｜ 今日新增：🔺163
- 标签：Agent-Skills, Claude-Code, Cursor, Codex, MCP, Skill
- 简介：Claude Skills 精选清单（awesome list），汇总 claude-code / cursor / codex / mcp 生态的技能与工具，是「技能即工程纪律」范式的事实入口之一。

---

## 今日趋势解读

1. **「技能层」登顶，输出风格封装成新爆点**：i-have-adhd 以 +1,699 登顶 Vibe Coding #1，把 Agent 输出可读性做成可安装技能，标志技能从「能力封装」走向「交互风格封装」。
2. **「网关 → 上下文 → 技能」完整链路固化**：OmniRoute（接入层）+ code-review-graph（上下文底座）+ i-have-adhd（技能层）连续同榜，Vibe Coding 三件套格局稳定。
3. **编码 Agent 可观测层升温**：pi-web 首入榜（#4）把终端编码 Agent 的会话/配置搬到浏览器工作台；awesome-claude-skills 以 68.8k 总 Star 居 #5，印证 Claude Skills 生态已规模化。
4. **code-review-graph 新增回落但长跑稳健**：今日 +882（较昨日 1,925 约 -54%），五度上榜仍居 #3，是「代码上下文底座」长期领跑者。

## 严格关键词命中说明

- 严格关键词（项目名或简介含 cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev）：本日仅 **1 个**命中 → `diegosouzapw/OmniRoute`（简介显式含 cursor / cline / copilot）。
- 命中不足 5 个，按 Vibe Coding / AI 编码 Agent 生态（Claude Code / Codex / Cursor / MCP / 编码 Agent / 技能）扩充，取当日新增 Star 降序前 5：
  - ayghri/i-have-adhd（编码 Agent 技能）
  - tirth8205/code-review-graph（MCP / ai-coding / claude-code）
  - agegr/pi-web（pi coding agent 的 Web UI）
  - ComposioHQ/awesome-claude-skills（claude-code / cursor / codex / mcp 清单）
- 边界排除：worldmonitor、voicebox、RuView、dioxus、Hyprland、croc 等非编码 Agent 工具；dottxt-ai/outlines（+364，通用 LLM 结构化输出库，非编码 Agent 专用）列为近邻未入榜。

---

详细笔记见 Obsidian 知识库（Daily/Vibe-Coding-2026-07-23.md）
