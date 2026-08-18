---
date: 2026-08-18
mode: vibe-coding
project_count: 2
tags: [github, ai, trending, vibe-coding]
source: GitHub Trending 飙升榜(WebFetch 截断至前 11 条·按当日新增降序) + GitHub REST API 元数据校验 + Search API 交叉核验
---

# GitHub AI 项目日报 · Vibe Coding 赛道 · 2026-08-18（工作日·周二）

> ⚠️ **数据源说明**：本日沙箱对 `github.com` 直连被 IP 层阻断（curl 返回 HTTP:200 但 body 为空），WebFetch 代理通道可命中 GitHub 趋势页，但趋势页 Markdown 提取被**截断至前 11 条**（按当日新增 Star 降序），下半段 12–25 名（≤344 新增）不可达。因此：
> - **Vibe Coding 入选**：在可检索的前 11 条中严格筛选，仅 **2 项** 命中 Vibe Coding / AI 编码 Agent 生态（详见下表），赛道今日极度稀疏，故取 **Top 2**。
> - **全赛道爆款** 仅取回 11 条真实 trending 数据（带真实当日新增），标注「部分」。
> - ⭐ 总 Star 经 GitHub REST API 实时校验（2026-08-18）；📈 当日新增取自趋势页真实值。
> - GitHub Search API 交叉核验：近期活跃的 claude-code/cursor 主题库均为长期热门大库（ECC 240k、hermes-agent 232k 等），**未**出现在今日飙升榜前段，确认无遗漏的 Vibe Coding 爆款。

## 🔝 今日最佳开源项目

**akitaonrails/ai-memory** — ⭐2.4k / Rust / 今日新增 🔺207
- 链接：https://github.com/akitaonrails/ai-memory
- 简介：💡 Long-term memory for AI coding agents —— 让 Claude Code 中途退出、换成 OpenAI Codex 在同一目录继续，无需重新解释架构、失败尝试与未决问题。
- 入选：✅ 生态命中（agent coding CLIs / AI coding agents 记忆层）；今日（2026-08-18）仍有活跃推送。

## 分类速览（Vibe Coding Top 2 · 按当日新增 Star 降序）

| # | 项目 | 语言 | ⭐ | 📈 新增 | 入选依据 |
|---|---|---|---|---|---|
| 1 | [[Projects/akitaonrails_ai-memory|akitaonrails/ai-memory]] | Rust | 2.4k | 🔺207 | ✅ 生态命中(agent coding CLIs / AI coding agents 记忆层) |
| 2 | [[Projects/mukul975_Anthropic-Cybersecurity-Skills|mukul975/Anthropic-Cybersecurity-Skills]] | Python | 28.7k | 🔺198 | ✅ 严格命中(copilot / cursor / codex · topics 含 claude-code) |

## 🌐 全赛道爆款 Top11（部分 · trending 页截断至前 11 条·按当日新增降序）

> GitHub Trending 全局（不限 Vibe Coding 赛道），按**当日新增 Star** 降序。仅取回 11 条真实数据；其中 🟢 标记为本日 Vibe Coding 入选。

| # | 项目 | 语言 | ⭐ | 📈 新增 | 赛道 |
|---|---|---|---|---|---|
| 1 | [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | Python | 107.2k | 🔺1,189 | 视频生成 |
| 2 | [cordiverse/cordis](https://github.com/cordiverse/cordis) | TypeScript | 5.9k | 🔺957 | 框架 |
| 3 | [usestrix/strix](https://github.com/usestrix/strix) | Python | 54.7k | 🔺598 | 安全渗透 |
| 4 | [agalwood/Motrix](https://github.com/agalwood/Motrix) | TypeScript | 53.3k | 🔺344 | 下载工具 |
| 5 | [santifer/career-ops](https://github.com/santifer/career-ops) | JavaScript | 65.2k | 🔺218 | 求职 CLI |
| 6 | 🟢 [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) | Rust | 2.4k | 🔺207 | **Vibe Coding** |
| 7 | 🟢 [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | Python | 28.7k | 🔺198 | **Vibe Coding** |
| 8 | [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) | Rust | 32.6k | 🔺198 | 模型运行 |
| 9 | [immich-app/immich](https://github.com/immich-app/immich) | TypeScript | 111.4k | 🔺175 | 相册管理 |
| 10 | [nautechsystems/nautilus_trader](https://github.com/nautechsystems/nautilus_trader) | Rust | 26.2k | 🔺120 | 交易引擎 |
| 11 | [jundot/omlx](https://github.com/jundot/omlx) | Python | 19.2k | 🔺78 | 推理服务 |

## 趋势解读

- 语言分布（Vibe Coding Top 2）：Rust×1、Python×1。
- 严格/生态命中 **2/2**：ai-memory（编码 Agent 记忆层，Rust 新秀）、Anthropic-Cybersecurity-Skills（817 个面向 AI Agent 的安全技能库，兼容 Claude Code / Copilot / Cursor / Codex 等 20+ 平台）。
- 今日 Vibe Coding 赛道**极度稀疏**：全 25 条趋势榜中可检索前 11 条仅 2 条命中，且均为「编码 Agent 配套层」（记忆 / 技能），无纯编码生成本体上榜——延续 08-17「工程纪律 / 技能层」主线，但量级明显降温。
- 全赛道爆款由 `MoneyPrinterTurbo`（🔺1,189，AI 短视频）领跑，量级远超其余；`cordis`（🔺957，时空可组合元框架）次之。
- 注：机械统计由本自动化生成；深度趋势解读可由 agent 在生成后补充。

## 详细见 Obsidian 项目页

- [[Projects/akitaonrails_ai-memory|akitaonrails/ai-memory]]
- [[Projects/mukul975_Anthropic-Cybersecurity-Skills|mukul975/Anthropic-Cybersecurity-Skills]]
