---
aliases: [design.md, google-labs-code/design.md, DESIGN.md]
tags: [AI, Trending, TypeScript, DesignSystem, CodingAgent]
stars: 24630
created_at: 2026-04-10
weekly_growth: 6240
status: 待填写
date_accessed: 2026-07-04

# design.md (Google Labs Code)

> 面向 AI 编码代理的设计系统描述格式规范

## 🎯 项目定位

DESIGN.md 是一种格式规范，用于向编码代理描述项目的视觉标识。通过将机器可读的设计 token（YAML front matter）与人类可读的设计理念说明（Markdown 正文）结合，让 AI 代理获得对项目视觉标识的持久化、结构化理解。

**核心思想**：Token 给代理精确的值，文字告诉它们这些值存在的原因及如何应用。

**CLI 工具生态**：
- `lint` — 校验 DESIGN.md 结构正确性、WCAG 对比度
- `diff` — 检测 token 级别和文本回归
- `export` — 导出为 Tailwind v3/v4 或 W3C DTCG 格式
- `spec` — 输出格式规范（可注入代理提示词）

**当前版本**：alpha（积极开发中）

## 🛠 技术栈

- **TypeScript** — CLI 工具实现
- **YAML** — 设计 token front matter 格式
- W3C Design Token Format 互操作

## 🔗 外部链接

- GitHub: [https://github.com/google-labs-code/design.md](https://github.com/google-labs-code/design.md)

## 📅 归档索引

- [[AI-Weekly-2026-07-04]] — 本周 Top 10 第 5 名
