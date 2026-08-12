---
aliases: [code-graph-rag, vitali87/code-graph-rag]
tags: [AI, Trending, Python, RAG, Code-Understanding, Claude-Code, MCP, Monorepo, Knowledge-Graph, Vibe-Coding, Developer-Tools]
stars: 3810
created_at: 2025-06-16
today_growth: 341
status: 4度上榜
date_accessed: 2026-08-12
---

# code-graph-rag

**项目地址**：https://github.com/vitali87/code-graph-rag
**作者**：vitali87
**⭐ 总 Star**：3,661（3.7k）
**📈 今日新增**：🔺682 stars（Vibe Coding #3，新建；08-10 尚在近失名单 🔺96）
**💻 主要语言**：Python
**📅 开源时间**：2025-06-16
**🌐 官网**：https://code-graph-rag.com
**🏷 Topics**：claude-code, code-understanding, codebase-search, mcp, mcp-server, monorepo, tree-sitter, ast, knowledge-graph, graph-database, memgraph, developer-tools, rag, retrieval-augmented-generation, semantic-search, multi-language
**📜 许可证**：MIT

## 项目定位

**monorepo 的终极 RAG**：用 AI + 知识图谱**查询、理解并编辑多语言代码库**。把代码解析成 AST，构建代码知识图谱（基于 Memgraph 等图数据库），让编码 Agent 能语义检索「哪里实现了 X」「改这个函数会影响谁」，而不只是向量相似度匹配。

一句话：coding agent 跑长任务时最缺的「**代码上下文**」底座——和 [[semantica-agi_semantica|semantica]]（业务上下文）正好互补。

## 核心能力

- **Codebase Search**：跨多语言代码库的语义检索
- **Code Understanding**：基于 AST + 知识图谱的代码理解
- **Edit Support**：理解后的代码编辑（README 明确「query, understand, and edit」）
- **Multi-language**：多语言支持（tree-sitter 驱动）
- **MCP Server**：提供 MCP server，可直接接 Claude Code / 其它支持 MCP 的编码 Agent

## 技术栈

- **解析**：tree-sitter（AST）、多语言
- **图谱**：知识图谱 / 图数据库（Memgraph）
- **检索**：RAG + 语义搜索（semantic-search）
- **集成**：MCP server（claude-code topic，可直接作为 coding agent 的工具）
- **分发**：PyPI（`code-graph-rag`）+ pip；Python
- **许可证**：MIT

## 与 Vibe Coding 的关系

它是 coding agent 的**代码上下文底座**：过去几期「记忆层」由 [[TencentCloud_TencentDB-Agent-Memory|TencentDB Agent Memory]] 承担（现已连续缺席），code-graph-rag 用「代码知识图谱 + MCP」填补了**理解代码库**这一更具体的缺口。配 claude-code / mcp topics，定位清晰。

## 外部链接

- GitHub：https://github.com/vitali87/code-graph-rag
- 官网：https://code-graph-rag.com
- PyPI：https://pypi.org/project/code-graph-rag/
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-08-11|2026-08-11 日报]]（#3，⭐3.7k / 🔺682，代码理解底座新晋；08-10 近失名单晋级）
- [[Vibe-Coding-2026-08-10|2026-08-10 日报]]（近失名单，🔺96 / ⭐3.3k）

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding 生态扩充命中：topics 含 `claude-code` `code-understanding` `codebase-search` `mcp` `developer-tools`）。
- 2025-06-16 开源，约 14 个月 ⭐3.7k；08-10 尚在近失名单（🔺96），今日 🔺682 翻 7 倍冲进 #3，是典型「近失→入榜」跃迁。

## 反向链接
- [[Daily/Vibe-Coding-2026-08-12.md|2026-08-12 收录]]
