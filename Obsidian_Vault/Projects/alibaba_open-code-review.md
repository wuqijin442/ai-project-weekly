---
aliases: [open-code-review]
tags: [AI, Trending, Go, Vibe-Coding, Coding-Agent, Code-Review]
stars: 13784
created_at: 2026-05-18
today_growth: 832
status: 活跃（大厂代码审查 Agent 化，二度上榜）
date_accessed: 2026-07-27

# open-code-review

**项目地址**：https://github.com/alibaba/open-code-review
**作者**：alibaba
**⭐ 总 Star**：13,784（13.8k）
**📈 今日新增**：832 stars（Vibe Coding #2）
**💻 主要语言**：Go
**🗓 开源时间**：2026-05-18

## 项目定位

阿里巴巴内部孵化的 **AI 代码审查 CLI**。源自阿里集团官方 AI 代码审查助手，两年间服务数万开发者、识别数百万代码缺陷，经大规模验证后开源。读取 Git diff，经「带工具调用的 LLM Agent」生成行级精准审查评论；Agent 可读取完整文件、搜索代码库、检视其他变更文件以产出深度审查。另含 `ocr scan` 审查整个文件用于审计陌生代码库。一句话：把「代码审查」做成确定性流水线 + LLM Agent 的混合架构，兼容 Claude Code / Codex / Cursor。

## 技术栈

- **形态**：AI 代码审查 CLI（开源免费，Apache-2.0）
- **架构**：确定性流水线（静态规则）+ LLM Agent（工具调用）混合；内置微调规则集（NPE、线程安全、XSS、SQL 注入）
- **能力**：行级精准评论、跨文件上下文、整文件 `ocr scan` 审计
- **兼容 Agent**：Claude Code / Codex / Cursor；支持 OpenAI & Anthropic
- **分发**：npm 包 `@alibaba-group/open-code-review`；跨平台（Windows / macOS / Linux）；Go 编写
- **Topics**：agent, agent-skills, code-review, harness, repository-level-context
- **官网**：https://open-codereview.ai

## 外部链接

- GitHub：https://github.com/alibaba/open-code-review
- 作者组织：https://github.com/alibaba

## 相关日期

- [[Vibe-Coding-2026-07-27|2026-07-27 日报]]

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding 生态扩充命中：以 LLM Agent 做代码审查、兼容 Claude Code / Codex / Cursor，属「编码 Agent / 代码质量」细分）。2026-07-24 首入榜 #5（+180，11.5k）；2026-07-27 二度上榜跃居 #2（+832，13.8k），标志大厂把「代码审查」Agent 化持续走热、且强调精度 / F1 与省 token。
