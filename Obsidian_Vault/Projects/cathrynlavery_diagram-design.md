---
aliases: ["cathrynlavery/diagram-design"]
tags: [github, ai, vibe-coding, project]
stars: 22437
today_growth: 1607
created_at: 2026-04-16
status: 5度上榜 · 已本地全量测试(2026-08-19)
date_accessed: 2026-08-19
---

# cathrynlavery/diagram-design

## 定位
29 editorial diagram types for Claude Code. Self-contained HTML + SVG. No shadows, no Mermaid-slop.

## 技术栈
- 主语言：HTML
- Topics：—
- License：MIT

## 外部链接
- GitHub：https://github.com/cathrynlavery/diagram-design
- Stars：⭐14.4k（今日 🔺2,855）

## 反向链接
- [[Daily/Vibe-Coding-2026-08-13.md|2026-08-13 收录]]
- [[Daily/Vibe-Coding-2026-08-14.md|2026-08-14 收录]]
- [[Daily/Vibe-Coding-2026-08-15.md|2026-08-15 收录]]
- [[Daily/AI-Weekly-2026-08-16.md|2026-08-16 收录]]

## 本地测试记录（2026-08-19）
- Clone：`clones/diagram-design`（浅克隆，335 文件 / 12MB，main 分支）
- 结构：Claude Code 插件（`.claude-plugin`）+ Codex 插件（`.codex-plugin`）+ 标准 `skills/diagram-design/`（SKILL.md v2.4 + 110 个 HTML + 41 references + 3 脚本）
- 资产：28+ 类型 × 3 变体（默认 light / `-dark` / `-full` 编辑级），命名 `example-{type}.html`；另有 template 系列（含 motion/terminal）、icons、画廊 index.html
- 全量自检：`scripts/self_check.py` 跑全部 110 个 HTML → **108 通过**；2 个「失败」为导航页（index.html 画廊 / icons.html 图标引用页），非图表生成物，预期内
- 单文件自包含：内联 CSS 变量 token（paper/ink/muted/accent + 三套字体栈）+ 内联 SVG；唯一外链为 Google Fonts（官方唯一获批资源）；无 JS（静态变体）、无外部图片
- 使用验证：本地 http.server:8899 画廊预览正常（HTTP 200）
- 结论：图表模板全部可离线使用，无构建步骤，浏览器直接打开即可；品牌化靠 style-guide.md token 或 onboard 从网站抽取
