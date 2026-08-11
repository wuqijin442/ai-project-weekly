---
aliases: [agent-skills, addyosmani/agent-skills]
tags: [AI, Trending, JavaScript, Claude-Code, Cursor, Codex, Agent, Skills, Vibe-Coding]
stars: 85991
created_at: 2026-02-15
today_growth: 659
status: 热门（技能层，三度上榜，2026-08-11 Vibe Coding #4 · 严格命中 cursor）
date_accessed: 2026-08-11
---

# agent-skills

**项目地址**：https://github.com/addyosmani/agent-skills
**作者**：addyosmani（Addy Osmani，Google 工程师）
**⭐ 总 Star**：85,991（86.0k）  <!-- 2026-08-11 17:5x API 实时值；08-10 为 85,426 -->
**📈 今日新增**：🔺659 stars（榜面值；**48h 净增 +1,854（84,137→85,991），日均 ≈+927，与榜面吻合**）
**🎯 严格命中**：`cursor`（topics）—— 2026-08-08 起严格命中判定范围扩展至 GitHub topics，本项目由生态扩充升为严格命中
**🍴 Fork**：9,188
**💻 主要语言**：JavaScript
**📅 开源时间**：2026-02-15
**🔄 最近推送**：2026-08-06 22:45
**🌐 官网**：https://skills.addy.ie
**🏷 Topics**：agent-skills, antigravity, claude-code, codex, cursor, skills
**📜 许可证**：MIT

## 项目定位

一组为 AI 编程代理设计的**生产级工程技能**框架。将资深工程师在构建软件时使用的工作流程、质量门禁和最佳实践编码化，使 AI 代理在开发的每个阶段都能一致地遵循。

核心理念：AI 编程代理默认走最短路径，往往会跳过规格说明、测试、安全审查等使软件可靠的实践。agent-skills 为代理提供结构化工作流，强制执行与资深工程师对生产代码相同的要求。

## 核心组成

### 8 个 Slash 命令（开发生命周期）

| 阶段 | 命令 | 核心原则 |
|------|------|----------|
| 定义需求 | `/spec` | 先写规格再写代码 |
| 规划方案 | `/plan` | 小而原子化的任务 |
| 增量构建 | `/build` | 一次一个切片 |
| 验证测试 | `/test` | 测试即证据 |
| 代码审查 | `/review` | 提升代码健康度 |
| 性能审计 | `/webperf` | 先测量再优化 |
| 代码简化 | `/code-simplify` | 清晰优于聪明 |
| 部署上线 | `/ship` | 越快越安全 |

### 24 个技能（按阶段分类）

- **Define（定义）**：`interview-me`、`idea-refine`、`spec-driven-development`
- **Plan（规划）**：`planning-and-task-breakdown`
- **Build（构建）**：`incremental-implementation`、`test-driven-development`、`context-engineering`、`source-driven-development` 等 7 个
- **Verify（验证）**：`browser-testing-with-devtools`、`debugging-and-error-recovery`
- **Review（审查）**：`code-review-and-quality`、`code-simplification`、`security-and-hardening`、`performance-optimization`
- **Ship（部署）**：`git-workflow-and-versioning`、`ci-cd-and-automation` 等 6 个

### 4 个专家代理角色

| 角色 | 职位 |
|------|------|
| `code-reviewer` | Senior Staff Engineer |
| `test-engineer` | QA Specialist |
| `security-auditor` | Security Engineer |
| `web-performance-auditor` | Web Performance Engineer |

## 兼容平台（70+）

Claude Code、Cursor、Codex、Copilot、Cline、Gemini CLI、Windsurf、OpenCode、Antigravity CLI、Kiro IDE 等。

## 安装方式

```bash
# 安装全部 24 个技能
npx skills add addyosmani/agent-skills

# Claude Code 通过 Plugin Marketplace
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

## 技术栈

- 内容格式：纯 Markdown（SKILL.md 文件）
- 评估脚本：零依赖 JavaScript
- CI/CD：GitHub Actions
- 许可证：MIT

## 评估基线

- 120 项检查通过
- 72 个正向提示中 85% 触发 rank-1 率
- 零目录冲突

## 外部链接

- GitHub：https://github.com/addyosmani/agent-skills
- 作者：https://github.com/addyosmani
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-07-14|2026-07-14 日报]]
- [[Vibe-Coding-2026-07-11|2026-07-11 日报]]
- [[Vibe-Coding-2026-07-08|2026-07-08 日报]]
- [[Vibe-Coding-2026-07-09|2026-07-09 日报]]
- [[Vibe-Coding-2026-07-10|2026-07-10 日报]]
- [[Vibe-Coding-2026-08-08|2026-08-08 日报]]（#3，⭐83.9k / 🔺1,131）
- [[Vibe-Coding-2026-08-10|2026-08-10 日报]]（#3，⭐85.4k / 🔺680，严格命中 cursor）
- [[Vibe-Coding-2026-08-11|2026-08-11 日报]]（#4，⭐86.0k / 🔺659，严格命中 cursor，三度上榜）

## 三条核心主张（2026-08-08 复核 README）

| 主张 | 原文 | 含义 |
|------|------|------|
| **Process, not prose.** | — | 技能是**工作流**，不是参考文档 |
| **Anti-rationalization.** | — | 每个技能自带借口反驳表，专治「我稍后补测试」 |
| **Verification is non-negotiable.** | — | 技能结尾必须有证据要求（测试通过等） |

> *"AI coding agents default to the shortest path… Agent Skills gives agents structured workflows that enforce the same discipline senior engineers bring."*

补充：`/build auto` 支持一次性审批后自主实现；已接入 Command Code / Antigravity / Kiro 等较新宿主；单技能安装的便携性缺口由 [#361](https://github.com/addyosmani/agent-skills/issues/361) 跟踪。

## 备注

- 融入了 Google 工程文化的最佳实践（包括《Software Engineering at Google》中的概念）
- 技能为流程导向（非散文式），包含反合理化机制和验证要求
- 渐进式披露设计，最小化 token 使用
- 2026-07-14 更新：总 Star 由 76,816 升至 77,927；今日精确新增因 GitHub Trending 日榜 WebFetch 截断未能直读，frontmatter 曾记 `weekly_growth: 7300`（findarepo 镜像近 7 日动量，约 +7.3k），该仓库已确认位于今日日榜尾段。
- **格式修复（2026-08-08）**：本页 YAML frontmatter 自建档起缺失闭合 `---`，Obsidian 无法解析属性，本次修复；`weekly_growth` 字段改为 `today_growth`，与其余项目页对齐。
- **成长曲线**：2026-07-14 ⭐77,927 → 2026-08-07 ⭐83,351（🔺593，赛道内落榜，列近失名单） → 2026-08-08 ⭐83,891（🔺1,131，Vibe Coding #3）。**榜面日增从 593 翻到 1,131，一天翻倍后重回榜单。**
- ⚠️ **口径备注（连续两期）**：本仓库 topics 含 `cursor` `codex` `claude-code`，若 Vibe Coding 严格关键词判定扩展到 topics 字段，则构成**严格命中**（`cursor`）。本归档历史口径仅匹配 `owner/repo` + 简介，故 08-07、08-08 两期均计为「生态扩充」。该分歧建议评估是否调整口径。
- 2026-08-08 日报（#3）：与 [[mattpocock_skills|mattpocock/skills]]、[[obra_superpowers|obra/superpowers]] 同日占 Top 5 三席。三者定位差异：本项目 = 零件 + 质检表（24 技能 + 8 斜杠命令 + 质量门禁），mattpocock = 只给零件，superpowers = 整条产线。
