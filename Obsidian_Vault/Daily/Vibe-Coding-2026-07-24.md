---
date: 2026-07-24
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [GitHub, Trending, Vibe-Coding, AI, Daily]
source: https://github.com/trending?since=daily
---

# GitHub AI 热门项目 · Vibe Coding 日报（2026-07-24 · 周五）

> 数据源：GitHub Trending 日榜（飙升榜，按当日新增 Star 降序）｜筛选口径：严格关键词 + Vibe Coding / AI 编码 Agent 生态扩充，取前 5。

## 🔝 今日最佳开源项目

**#1 [[diegosouzapw_OmniRoute|OmniRoute]]** — diegosouzapw
- 链接：https://github.com/diegosouzapw/OmniRoute
- 总 Star：**27.2k** ｜ 今日新增：**🔺1929**
- 一句话亮点：免费 MIT AI 网关，单一端点聚合 290+ 供应商 / 500+ 模型，专为 Claude Code / Codex / Cursor / Cline / Copilot 等编码 Agent 设计，RTK+Caveman 压缩省 15–95% token——连续三日上榜，编码 Agent 统一接入层需求持续高热。

---

## 入选项目（按当日新增降序）

| # | 项目 | 作者 | 今日新增 ⭐ | 简介 |
|---|------|------|-----------|------|
| 1 | [[diegosouzapw_OmniRoute\|OmniRoute]] | diegosouzapw | 🔺1929 | 免费 MIT AI 网关：290+ 供应商/500+ 模型一端点接入 Claude Code/Codex/Cursor/Cline/Copilot，RTK+Caveman 压缩省 15–95% token，支持 MCP/A2A |
| 2 | [[ComposioHQ_awesome-claude-skills\|awesome-claude-skills]] | ComposioHQ | 🔺636 | 1000+ 生产级 Claude Skills / 插件精选清单，覆盖 Claude.ai、Claude Code 及 Codex/Cursor/Gemini CLI 等编码 Agent |
| 3 | [[agegr_pi-web\|pi-web]] | agegr | 🔺315 | 编码 Agent「pi」的本地 Web UI：会话浏览、实时聊天、模型配置、技能管理与文件预览 |
| 4 | [[earthtojake_text-to-cad\|text-to-cad]] | earthtojake | 🔺230 | 面向 CAD / 机器人 / 硬件设计的 Agent 技能库（STEP/STL/3MF/URDF），把「技能」范式从软件编码外溢到工程制造 |
| 5 | [[alibaba_open-code-review\|open-code-review]] | alibaba | 🔺180 | 阿里孵化的 AI 代码审查 CLI：确定性流水线 + LLM Agent 生成行级评论，兼容 Claude Code/Codex/Cursor，同模型下精度更高、仅耗约 1/9 token |

---

## 今日趋势解读

1. **「网关」回归榜首，编码 Agent 接入层仍是主战场**：OmniRoute 以 +1,929 登顶 Vibe Coding #1，连续第三日上榜（07-22 #1、07-23 #2），总 Star 升破 27k；AI 网关作为编码 Agent 统一前置（多供应商路由 + token 压缩 + 自动 fallback）需求持续高热。
2. **「技能层」规模化，Claude Skills 精选成常驻**：awesome-claude-skills 以 69.4k 总 Star 居 #2（+636），印证 Claude Skills 生态已从「能力封装」走向「清单 / 社区化」；text-to-cad 把技能范式从软件编码外溢到 CAD / 硬件设计（#4，+230），技能层外延持续扩张。
3. **编码 Agent 可观测与代码审查双线并进**：pi-web（#3，+315）持续补全编码 Agent 的浏览器工作台；alibaba/open-code-review（#5，+180）以「确定性流水线 + LLM Agent」混合架构入榜，标志大厂把代码审查 Agent 化、且强调精度 / F1 与省 token。
4. **Vibe Coding 链路稳定收敛为「网关 → 技能 → Agent 工作台 / 审查」**：今日 5 项覆盖接入层（OmniRoute）、技能（awesome-claude-skills、text-to-cad）、Agent 工作台（pi-web）、代码质量（open-code-review）四节，完整链路清晰。

## 严格关键词命中说明

- **严格关键词**（项目名或简介含 cursor / cline / aider / continue / swe-agent / open-interpreter / browser-use / gpt-engineer / meta-gpt / devin / autocode / copilot / cli-agent / code-generator / llm-dev）：本日仅 **1 个**命中 → `diegosouzapw/OmniRoute`（简介与 topics 显式含 **cursor / cline / copilot**，且兼容 Claude Code / Codex）。
- 命中不足 5 个，按 **Vibe Coding / AI 编码 Agent 生态**（Claude Code / Codex / Cursor / MCP / 编码 Agent / 技能）口径扩充，取当日新增 Star 降序前 5：
  - `ComposioHQ/awesome-claude-skills`（Claude Skills 清单，claude-code / cursor / codex / mcp / agent-skills）
  - `agegr/pi-web`（pi coding agent 的 Web UI）
  - `earthtojake/text-to-cad`（面向 CAD / 机器人 / 硬件的 agent skills）
  - `alibaba/open-code-review`（LLM Agent 代码审查，兼容 Claude Code / Codex / Cursor）
- 边界排除：citrolabs/ego-lite（+247，AI 代理浏览器，属通用 Agent 基础设施非编码 Agent 生态）；block/buzz（+2,162，hive mind 通信平台）、ruvnet/RuView（+1,708，WiFi 空间智能）、koala73/worldmonitor（+3,175，全球情报看板）、shiyu-coder/Kronos（+401，金融大模型）、Automattic/harper（+624，语法检查器）、jellyfin/jellyfin（+66，媒体系统）；sponsors/* 伪条目（Pumpkin-MC / chrislgarry / likec4 及 diegosouzapw 赞助位，真实仓库 OmniRoute 已计入）已剔除。
