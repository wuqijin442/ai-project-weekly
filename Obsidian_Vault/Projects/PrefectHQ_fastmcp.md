---
aliases: [fastmcp]
tags: [AI, Trending, Python, MCP, MCP-Servers, MCP-Clients, Agents, LLMs, Vibe-Coding]
stars: 26526
today_growth: 96
created_at: 2024-11-30
status: 成熟（生产级）
date_accessed: 2026-07-21

# fastmcp

**项目地址**：https://github.com/PrefectHQ/fastmcp
**作者**：PrefectHQ（Prefect）
**⭐ 总 Star**：26,526（26.5k）
**📈 今日新增**：96 stars
**💻 主要语言**：Python
**🗓 开源时间**：2024-11-30

## 项目定位

**MCP（Model Context Protocol，模型上下文协议）的 Python 首选框架**，口号「Move fast and make things.」The Model Context Protocol 把 LLM 连接到大模型工具与数据；FastMCP 提供从原型到生产所需的一切，让你用极简、Pythonic 的方式构建 MCP server 与 client。

一句话：Vibe Coding 时代的「MCP 基建标准件」——几乎所有 Python 编码 Agent / 技能（code-review-graph、wigolo 等）都通过 MCP 接入，而 FastMCP 是搭建这些 MCP 服务端最流行的工具。

## 技术栈

- **语言/分发**：Python（PyPI 包 `fastmcp`），跨平台
- **核心抽象**：`FastMCP` 服务器、`@mcp.tool` 装饰器定义工具、`@mcp.resource` / `@mcp.prompt`
- **形态**：MCP servers（工具/资源/提示）与 MCP clients，支持 stdio / 传输层
- **生态**：gofastmcp.com 文档站、Discord 社区、PyPI 发布、CI 测试
- **Topics**：agents, fastmcp, llms, mcp, mcp-clients, mcp-servers

## 外部链接

- GitHub：https://github.com/PrefectHQ/fastmcp
- 作者/组织：https://github.com/PrefectHQ
- 官网/文档：https://gofastmcp.com
- 安装：`pip install fastmcp`

## 相关日期

- [[Vibe-Coding-2026-07-21|2026-07-21 日报]]

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding 生态扩充命中：topics 含 mcp / mcp-servers / mcp-clients / agents / llms，定位为「编码 Agent 的 MCP 连接协议底座」）。2026-07-21 首次入 Vibe Coding #5（+96，26.5k，老牌成熟项目）；作为 MCP 事实标准框架，它是今日 Top 5 中 code-review-graph / wigolo 等工具得以被编码 Agent 调用的底层基础设施。
