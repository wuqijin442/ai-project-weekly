---
aliases: [code-review-graph]
tags: [AI, Trending, Python, MCP, Claude-Code, Coding-Agent, Code-Review, GraphRAG, Vibe-Coding]
stars: 26396
created_at: 2026-02-26
weekly_growth: 6423
status: 新兴
date_accessed: 2026-07-26
---

# code-review-graph

**项目地址**：https://github.com/tirth8205/code-review-graph
**作者**：tirth8205
**⭐ 总 Star**：26,396（26.4k）
**📈 本周新增**：6,423 stars
**💻 主要语言**：Python
**🗓 开源时间**：2026-02-26

## 项目定位

本地优先（local-first）的**代码智能图谱**工具。用 Tree-sitter 为代码库构建结构化持久化映射（函数、类、导入及调用/继承等关系边），并借 MCP 与 CLI 让 AI 编程助手在代码审查等任务中只读取受变更影响的**最小文件集合**（爆炸半径分析），而非反复扫描整个代码库。基准测试在 6 个真实仓库中实现 **38×–528×** 的上下文缩减，大幅降低 token 消耗、提升审查效率。口号：「Stop burning tokens. Start reviewing smarter.」

## 技术栈

- **解析**：Tree-sitter（AST），支持 30+ 语言及 Jupyter 笔记，含针对性 fallback
- **存储/图谱**：本地 SQLite（`.code-review-graph/`），节点/边含调用、继承、测试覆盖
- **图算法**：Leiden 社区检测、Betweenness 中心性、BFS/DFS、爆炸半径分析
- **语义搜索**：可选向量嵌入（sentence-transformers / Gemini / MiniMax / OpenAI 兼容端点）+ FTS5 全文混合
- **集成**：MCP（30 个工具 + 5 个 Prompt 模板）、CLI、GitHub Action、`crg-daemon` 多仓守护、编辑器 Hook/Watch
- **语言/运行时**：Python 3.10+（推荐 `uv`/`uvx`），可视化用 D3.js，构建用 hatchling

## 外部链接

- GitHub：https://github.com/tirth8205/code-review-graph
- 作者：https://github.com/tirth8205
- 官网：https://code-review-graph.com

## 相关日期

- [[Vibe-Coding-2026-07-18|2026-07-18 日报]]
- [[Vibe-Coding-2026-07-20|2026-07-20 日报]]
- [[Vibe-Coding-2026-07-21|2026-07-21 日报]]
- [[Vibe-Coding-2026-07-22|2026-07-22 日报]]
- [[Vibe-Coding-2026-07-23|2026-07-23 日报]]

- [[AI-Weekly-2026-07-26|2026-07-26 周报]]

## 备注

- 2026-07-26 周报（周末全赛道 Top 10，#6）：本周 +6,423，总 Star 26.4k（26,396）。

- 由 GitHub Trending 日榜自动归档（Vibe Coding 生态扩充命中：简介与 topics 含 MCP / ai-coding / claude-code，定位为「AI 编程工具的代码上下文底座」）。2026-07-20 居 Vibe Coding #1（本周最佳🔝，+663，21.2k）；2026-07-21 再次登顶 Vibe Coding #1（🔝今日 +1,833，23.1k），三度上榜且新增翻倍，持续领跑「代码上下文底座」赛道，印证 MCP 从「连接协议」演进为「代码智能图谱」基础设施。
- 2026-07-22 居 Vibe Coding #2（+1,925，24.5k，四度上榜），新增较昨日（1,833）略升，被新面孔 OmniRoute（+2,034）挤下榜首，但仍是「代码上下文底座」双雄之一，持续领跑本地优先代码智能图谱赛道。
- 2026-07-23 居 Vibe Coding #3（+882，25.3k，五度上榜），新增较昨日（1,925）明显回落（约 -54%），被 i-have-adhd / OmniRoute 双新势挤至第三，但仍是「代码上下文底座」长期领跑者，与 OmniRoute（接入层）/ i-have-adhd（技能层）共构完整 Vibe Coding 链路。
