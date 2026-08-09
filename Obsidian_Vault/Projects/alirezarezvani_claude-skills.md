---
aliases: [claude-skills, Claude Skills, Agent Skills]
tags: [AI, Trending, Python, Vibe-Coding, Claude-Code, Skills, Multi-tool]
stars: 21132
created_at: 2025-10-19
daily_growth: 611
status: 待填写
date_accessed: 2026-07-07
---

# claude-skills

> 收录自：[[Daily/Vibe-Coding-2026-07-07|Vibe-Coding 日报 2026-07-07]]

## 项目定位

一站式开源 AI 编程技能与插件库，提供 355 个 Claude Code 技能、Agent 技能与插件，兼容 13 种 AI 编程工具（Cursor、Aider、Windsurf 等）。

## 基本信息

- **作者**：[alirezarezvani](https://github.com/alirezarezvani)
- **仓库**：[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
- **⭐ 总 Star**：21,132（截至 2026-07-07）
- **📈 今日新增**：+611
- **编程语言**：Python 98.1%（CLI 工具仅用标准库，零 pip 依赖）
- **许可证**：MIT
- **活跃度**：1,213 Commits / 51 Contributors / 最新发布 v2.9.0（2026-05-28）

## 规模数据

| 类别 | 数量 |
|------|------|
| Skills（技能） | 355 |
| Agents（代理） | 97 |
| Personas（角色） | 7 |
| Commands（命令） | 103 |
| Python CLI 工具 | 602 |
| 参考文档/模板 | 711 |

## 18 个覆盖领域

| 领域 | 技能数 | 代表技能 |
|------|--------|----------|
| 🔧 工程核心 | 52 | 架构、前端、后端、QA、DevOps、SecOps、AI/ML |
| ⚡ 工程进阶 | 81 | RAG 架构师、CI/CD 构建器、MCP 构建器、零幻觉编码器 |
| 🎯 产品 | 17 | 产品经理、UX 研究、UI 设计、SaaS 脚手架 |
| 📣 营销 | 48 | SEO+AEO（LLM 引用优化）、CRO、增长 |
| 💼 C 级顾问 | 68 | CEO/CTO/CFO/CMO/CRO 等全套 C 套件 |
| 🔬 学术研究 | 9 | 文献综述、专利、NIH 基金、深度研究 |
| 🏥 合规与质量 | 19 | ISO 13505、MDR、FDA、GDPR、SOC 2 |
| 🤝 商务 | 8 | 定价策略、交易台、合作伙伴架构 |
| 💰 金融 | 4 | 财务分析、SaaS 指标教练、投资顾问 |

## 兼容的 13 种 AI 编程工具

| 工具 | 支持格式 |
|------|----------|
| Claude Code | 原生插件 |
| OpenAI Codex | 原生 agent skills |
| Gemini CLI | 原生 skills |
| **Cursor** | `.mdc` 规则文件 ✅ |
| **Aider** | `CONVENTIONS.md` ✅ |
| **Windsurf** | `.windsurf/skills/` |
| Kilo Code | `.kilocode/rules/` |
| OpenCode | `.opencode/skills/` |
| Augment | `.augment/rules/` |
| Antigravity | `~/.gemini/antigravity/skills/` |
| Hermes Agent | `~/.hermes/skills/` |
| Mistral Vibe | `~/.vibe/skills/` |
| OpenClaw | 原生安装脚本 |

## 安装使用

### Claude Code（推荐）
```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install engineering-skills@claude-code-skills
```

### Cursor / Aider / Windsurf 等
```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
./scripts/convert.sh --tool all   # 一键转换所有技能为 9 种工具格式
./scripts/install.sh --tool cursor --target /path/to/project
```

### Python 工具示例
```bash
# SaaS 健康检查
python3 finance/saas-metrics-coach/scripts/metrics_calculator.py --mrr 80000 --customers 200

# 安全审计技能
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/
```

## Vibe Coding 相关性

✅ **直接命中关键词**：简介含 "Claude Code, Codex, Gemini CLI, **Cursor**, and 8 more coding agents"
- 与 Vibe Coding 赛道高度相关，是目前**最全面的多工具技能兼容库**
- 支持 Cursor、Aider、Windsurf 等主流 Vibe Coding 工具
- 355 个技能覆盖从编码到产品、营销、合规的全流程，堪称"AI 编程助手技能商店"
- MIT 许可证，可自由使用和修改

## 编排协议（Orchestration）

四种跨域协作模式：
1. **Solo Sprint** — 项目阶段间切换角色
2. **Domain Deep-Dive** — 单角色 + 多技能叠加
3. **Multi-Agent Handoff** — 角色互相评审产出
4. **Skill Chain** — 顺序技能链，无需角色

## 外部链接

- 仓库：https://github.com/alirezarezvani/claude-skills
- 作者 Twitter：@alirezarezvani
- 网站：https://claudeskills.com（如有）

## 备注

- 所有 Python CLI 工具仅用标准库，零外部依赖
- 内置 `skill-security-auditor` 可在安装前扫描恶意代码
- 项目在 Vibe Coding 生态中扮演"技能基础设施"角色
