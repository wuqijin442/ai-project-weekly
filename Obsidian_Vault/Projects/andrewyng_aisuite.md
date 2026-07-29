---
aliases: [aisuite]
tags: [AI, Trending, Python, LLM, Vibe-Coding]
stars: 15786
created_at: 2024-06-30
today_growth: 62
status: 活跃（统一多 GenAI 供应商接口，Andrew Ng 出品）
date_accessed: 2026-07-29

# aisuite

**项目地址**：https://github.com/andrewyng/aisuite
**作者**：andrewyng（Andrew Ng）
**⭐ 总 Star**：15,786（15.8k）
**📈 今日新增**：62 stars（Vibe Coding #4）
**💻 主要语言**：Python
**许可证**：MIT

## 项目定位

轻量级 Python LLM 构建库，分两层：跨供应商统一的 **Chat Completions API**，以及在之上叠加 tools / toolkits 的 **Agents API**。让开发者用一套接口切换 OpenAI、Anthropic、Google 等多家模型，是编码 Agent 的 LLM 接入底座。

## 核心特性

- **统一 Chat Completions API**：一行切换供应商，降低供应商锁定风险。
- **Agents API**：在统一接口之上提供 tool / toolkit 抽象，便于构建带工具的智能体。
- **驱动 OpenWorker**：同一作者推出的桌面 AI 同事（andrewyng/openworker）即构建于 aisuite 之上——可聊天、深度研究、读文件、连 Slack/邮件、产出 PDF/文档/表格、跑定时自动化，支持自带 API key 或本地 Ollama。
- **易于安装**：PyPI 发布，pip 即可安装。

## 使用场景

- 编码 Agent / 应用统一接入多家大模型，做 A/B 与回退。
- 以 Agents API 快速搭建带工具调用的本地智能体。
- 作为上层 Agent 产品（如 OpenWorker）的模型抽象层。

## 技术栈

- **语言**：Python
- **接口层**：统一 Chat Completions API + Agents API（tools / toolkits）
- **生态**：OpenWorker（桌面 AI coworker）、多供应商 LLM 适配

## 外部链接

- GitHub：https://github.com/andrewyng/aisuite
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-07-29|2026-07-29 日报]]

## 反向链接

- [[Vibe-Coding-2026-07-29]]
