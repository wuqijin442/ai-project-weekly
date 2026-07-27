---
aliases:
  - planning-with-files
  - Planning with Files
  - 文件规划技能
tags:
  - AI
  - Trending
  - Python
  - ClaudeCode
  - ContextEngineering
  - VibeCoding
stars: 24690
created_at: 2026-01-03
daily_growth: 61
status: 待填写
date_accessed: 2026-07-06
owner: OthmanAdi
repo: planning-with-files
url: https://github.com/OthmanAdi/planning-with-files
language: Python

# OthmanAdi/planning-with-files

> 面向 AI 编程 agent 的持久化文件规划技能，灵感来自 Manus AI，通过 3 文件模式解决上下文丢失问题。

## 项目定位

planning-with-files 是一个持久化的基于文件的规划技能（Skill），专为 AI 编程 agent 设计。它将 `task_plan.md`、`findings.md` 和 `progress.md` 保存在磁盘上，使 agent 能够在**上下文丢失**、`/clear` 命令和崩溃中存活，并提供可选的完成门控（Completion Gate）确保计划真正执行完毕。

项目灵感来自 Manus AI 的上下文工程方法（Meta 以 20 亿美元收购 Manus）。核心理念：**上下文窗口 = RAM（易失、有限），文件系统 = 磁盘（持久、无限）→ 所有重要内容都写入磁盘。**

通过 SKILL.md 标准兼容 60+ agent，包括 Claude Code、Cursor、Codex、Gemini CLI、GitHub Copilot、CodeBuddy 等。基准测试通过率 96.7%（claude-sonnet-4-6）。

## 技术栈

- **主要语言**：Python（测试）/ Bash + PowerShell（脚本）
- **技能格式**：SKILL.md（agentskills.io 开放标准）
- **3 文件模式**：task_plan.md（计划）/ findings.md（发现）/ progress.md（进度）
- **Hook 系统**：PreToolUse、PostToolUse、Stop、PreCompact、SessionStart、UserPromptSubmit
- **多 IDE 适配**：18+ 平台，含 `.claude`、`.cursor`、`.codex`、`.gemini`、`.continue` 等适配器
- **安装**：`npx skills add OthmanAdi/planning-with-files --skill planning-with-files -g`
- **许可**：MIT
- **当前版本**：v3.2.0

## 核心特性

| 特性 | 说明 |
| --- | --- |
| 3 文件模式 | task_plan.md / findings.md / progress.md 持久化在磁盘 |
| 上下文恢复 | `/clear` 后自动从磁盘恢复计划和进度 |
| 完成门控 | Stop hook 验证所有阶段完成才允许停止（v3.0.0+） |
| 并行规划 | slug 模式支持多个独立计划并行运行（v2.36.0+） |
| 哈希认证 | SHA-256 锁定计划文件，防止篡改（v2.37.0+） |
| 多语言 | 支持中文（简/繁）、阿拉伯语、德语、西班牙语 |

## 外部链接

- **项目地址**：https://github.com/OthmanAdi/planning-with-files
- **作者**：Ahmad Othman Ammar Adi
- **基准测试详情**：https://github.com/OthmanAdi/planning-with-files/blob/main/docs/evals.md
- **Manus 上下文工程博客**：https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus

## 关键数据

| 指标 | 数值 |
| --- | --- |
| 总 Star | 24,690 |
| 今日新增 | +61 |
| 编程语言 | Python |
| 兼容 IDE 数 | 18+ |
| 基准通过率 | 96.7% |
| 当前版本 | v3.2.0 |
| 访问日期 | 2026-07-06 |

## 反向链接

- [[Vibe-Coding-2026-07-06|2026-07-06 Vibe Coding 日报]]
- [[_Index|全局索引]]
