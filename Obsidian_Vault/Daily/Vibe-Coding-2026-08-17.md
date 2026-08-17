---
date: 2026-08-17
mode: vibe-coding
project_count: 5
tags: [github, ai, trending, vibe-coding]
source: GitHub Trending 飙升榜(WebFetch 截断至7条) + GitHub Search API 兜底
---

# GitHub AI 项目日报 · Vibe Coding 赛道 · 2026-08-17（工作日）

> ⚠️ **数据源说明**：本日沙箱对 `github.com` 直连被 IP 层阻断（curl 返回空 body），WebFetch 代理通道可命中 GitHub，但趋势页 Markdown 提取被截断至 **7 条**（且无法稳定读出「当日新增 Star」字段）。因此：
> - **Vibe Coding Top 5** 改用 **GitHub Search API**（关键词 `cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev` 任一命中 `owner/repo` / 简介 / topics）按**当前总 Star 降序**生成，严格命中 5/5。
> - **全赛道爆款**仅取回 7 条真实 trending 数据（带真实当日新增），标注「部分」。
> - ⭐ 总 Star 为 2026-08-17 经 GitHub REST API 实时校验值；📈 当日新增因趋势页不可达统一标记为 `—`。

## 🔝 今日最佳开源项目

**github/spec-kit** — ⭐129.7k / Python / GitHub 官方
- 链接：https://github.com/github/spec-kit
- 简介：💫 Toolkit to help you get started with Spec-Driven Development（规格驱动开发）
- 入选：✅ 严格命中（topics 含 `copilot`）

## 分类速览（Vibe Coding Top 5 · 按当前总 Star 降序）

| # | 项目 | 语言 | ⭐ | 📈 新增 | 入选依据 |
|---|---|---|---|---|---|
| 1 | [[Projects/github_spec-kit|github/spec-kit]] | Python | 129.7k | — | ✅ 严格命中(copilot) |
| 2 | [[Projects/browser-use_browser-use|browser-use/browser-use]] | Python | 109.5k | — | ✅ 严格命中(browser-use) |
| 3 | [[Projects/addyosmani_agent-skills|addyosmani/agent-skills]] | JavaScript | 87.9k | — | ✅ 严格命中(cursor) |
| 4 | [[Projects/Panniantong_Agent-Reach|Panniantong/Agent-Reach]] | Python | 72.4k | — | ✅ 严格命中(cursor) |
| 5 | [[Projects/FoundationAgents_MetaGPT|FoundationAgents/MetaGPT]] | Python | 69.9k | — | ✅ 严格命中(metagpt) |

## 🌐 全赛道爆款 Top7（部分 · trending 页截断至 7 条）

> GitHub Trending 全局（不限 Vibe Coding 赛道），按**当日新增 Star** 降序。仅取回 7 条真实数据。

| # | 项目 | 语言 | ⭐ | 📈 新增 |
|---|---|---|---|---|
| 1 | [public-apis/public-apis](https://github.com/public-apis/public-apis) | Python | 462.6k | 🔺1,588 |
| 2 | [cordiverse/cordis](https://github.com/cordiverse/cordis) | TypeScript | 5.3k | 🔺720 |
| 3 | [unslothai/unsloth](https://github.com/unslothai/unsloth) | Python | 73.0k | 🔺572 |
| 4 | [ToolJet/ToolJet](https://github.com/ToolJet/ToolJet) | JavaScript | 40.3k | 🔺452 |
| 5 | [cactus-compute/needle](https://github.com/cactus-compute/needle) | Python | 6.9k | 🔺443 |
| 6 | [basecamp/omarchy](https://github.com/basecamp/omarchy) | Shell | 25.8k | 🔺270 |
| 7 | [OpenCut-app/OpenCut](https://github.com/OpenCut-app/OpenCut) | TypeScript | 84.3k | 🔺150 |

## 趋势解读

- 语言分布（Vibe Coding Top 5）：Python×4、JavaScript×1。
- 严格关键词命中 **5/5**（copilot / browser-use / cursor×2 / metagpt），本日无需生态扩充。
- 头部集中在「工程纪律 / 感知层 / 多智能体」三条线：spec-kit（规格驱动）、agent-skills（工程技能）、Agent-Reach（联网感官）、browser-use（浏览器操作）、MetaGPT（多智能体）。
- 全赛道爆款仅取回 7 条（trending 页截断），`public-apis` 以 🔺1,588 居首，量级远超其余。
- 注：机械统计由本自动化生成；深度趋势解读可由 agent 在生成后补充。

## 详细见 Obsidian 项目页

- [[Projects/github_spec-kit|github/spec-kit]]
- [[Projects/browser-use_browser-use|browser-use/browser-use]]
- [[Projects/addyosmani_agent-skills|addyosmani/agent-skills]]
- [[Projects/Panniantong_Agent-Reach|Panniantong/Agent-Reach]]
- [[Projects/FoundationAgents_MetaGPT|FoundationAgents/MetaGPT]]
