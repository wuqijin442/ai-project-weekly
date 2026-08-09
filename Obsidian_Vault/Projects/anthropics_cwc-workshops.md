---
aliases: [cwc-workshops]
tags: [AI, Trending, TypeScript, Anthropic, Claude-Code, Workshops, Managed-Agents, Skills, MCP, Vibe-Coding]
stars: 1579
created_at: 2026-05-06
today_growth: 37
status: 新兴
date_accessed: 2026-07-18
---

# cwc-workshops

**项目地址**：https://github.com/anthropics/cwc-workshops
**作者**：anthropics（Anthropic 官方）
**⭐ 总 Star**：1,579（1.6k）
**📈 今日新增**：37 stars
**💻 主要语言**：TypeScript
**🗓 开源时间**：2026-05-06

## 项目定位

Anthropic 官方发布的 **「Code with Claude」工作坊**材料库（明确标注 Not maintained / 不接收贡献）。汇集 8 套围绕 **Claude Code / Claude Managed Agents** 的实战工作坊，覆盖「选模型、拆多智能体、AI 辅助产品工作流、托管智能体上线、Agent 对战、记忆机制、评测驱动开发、生产级 Agent」等主题，是官方把 Vibe Coding 方法论落到可复刻练习的权威教材。

## 技术栈

- **形态**：工作坊仓库（每个子目录一套 WORKSHOP.md + 参考实现 / solutions）
- **核心范式**：Claude Code SKILL、Skills + MCP、Claude Managed Agents API、子智能体编排、Memory Store / Dreaming Service
- **涉及栈**：Next.js、Streamlit、Vite + React、Tailwind、TypeScript；含 edgartools Skill、Linear MCP 等
- **许可**：Apache-2.0

### 八大工作坊速览
- `rightmodel` — 用 Claude Code SKILL 审计并扫描 LLM 评测套件，挑最优「性价比 / 速度」配置
- `agent-decomposition` — 把 400 行 prompt 库存 Agent 拆成 Skills + 代码执行 + callable_agents
- `how-we-claude-code` — 三阶段 AI 辅助产品流（访谈→规格、4 套静态 HTML 设计探索、Vite+React 契约组件）
- `ship-your-first-managed-agent` — Streamlit 事故看板 + 离线 SRE Agent，实现 7 个 Managed Agents API 调用
- `agent-battle` — 45 分钟配置 Claude Managed Agent 驱动本地游戏 bot，按钻石数 / token 数评分
- `agents-that-remember` — 从「金鱼」到「同事」：逐层加记忆原语与 Dreaming Service 做跨会话持久化
- `eval-driven-agent-development` — 用 10 任务评测套件 + 两层评分器迭代 PPTX 生成 Agent
- `production-ready-agent` / `research-desk` — 多智能体 M&A 研究台 / SEC 文件研究台（Managed Agents）

## 外部链接

- GitHub：https://github.com/anthropics/cwc-workshops
- 组织：https://github.com/anthropics

## 相关日期

- [[Vibe-Coding-2026-07-18|2026-07-18 日报]]

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding 生态扩充命中：anthropics 官方、Claude Code 工作坊，涵盖 Skills / MCP / Managed Agents）。今日 +37 入 Vibe Coding #5，标志大厂把「怎么用好编码 Agent」做成开源方法论教材，与 copilot-sdk 的 SDK 化形成「能力标准化 + 最佳实践」双线。
