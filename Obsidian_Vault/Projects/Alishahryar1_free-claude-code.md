---
aliases: [free-claude-code, FCC, Free Claude Code]
tags: [AI, Trending, Python, Proxy, Gateway, Claude-Code, Codex, Vibe-Coding]
stars: 44068
created_at: 2026-01-28
today_growth: 278
status: 热门（首入榜 #5）
date_accessed: 2026-08-04
---

# free-claude-code

**项目地址**：https://github.com/Alishahryar1/free-claude-code
**作者**：Alishahryar1
**⭐ 总 Star**：44,068（44.1k）
**📈 今日新增**：🔺278 stars
**🍴 Fork**：7,273
**💻 主要语言**：Python（3.14）
**📅 开源时间**：2026-01-28
**🔄 最近推送**：2026-08-03
**📜 许可证**：MIT

## 项目定位

通过**自建供应商代理网关（FCC）**，让 Claude Code、Codex、Pi 及其 IDE 扩展跑在免费、付费或本地模型上——终端、IDE、桌面、手机全覆盖（支持语音，类 OpenClaw 体验）。

一句话：*Run your coding agents with free, paid, or local models. Choose and validate providers from one local Admin UI.*

## 核心能力

- **一键启动**：`fcc-claude` 启 Claude Code、`fcc-codex` 启 Codex、`fcc-pi` 启 Pi
- **后台常驻**：Windows / macOS 桌面启动器后台运行 FCC
- **31 家供应商**：Admin UI 中切换云端与本地供应商，并做连通性校验
- **原生模型选择器**：各编码 Agent 自带的 `/model` 选择器直接列出 FCC 网关模型
- **分级路由**：Fable / Opus / Sonnet / Haiku 与 fallback 流量可分别路由到不同模型
- **能力保真**：跨兼容模型保留流式输出、工具调用（tool use）、推理（reasoning）与图像输入
- **Codex 兼容**：本地 FCC Responses provider 支持 Codex CLI

## 技术栈

- **语言**：Python 3.14
- **包管理**：uv
- **质量工具链**：Pytest（测试）、Ty（类型检查）、Ruff（格式化）、Loguru（日志）
- **形态**：本地代理服务 + Admin UI + 桌面启动器
- **许可证**：MIT

## 使用场景

- 降低 Claude Code / Codex 使用成本（切到免费或自建本地模型）
- 团队统一模型出入口，集中做供应商校验与流量分级
- 在手机 / 桌面 / IDE 多端复用同一套编码 Agent 配置

## 外部链接

- GitHub：https://github.com/Alishahryar1/free-claude-code
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-08-04|2026-08-04 日报]]（首入榜 #5）

## 备注

- 与 [[andrewyng_aisuite|aisuite]]（07-29/08-01）、[[diegosouzapw_OmniRoute|OmniRoute]]（07-22~07-24）同属「LLM 接入 / 网关层」稳定赛道，但本项目更偏「**编码 Agent 客户端直连代理**」而非 SDK 抽象
- Fork 数 7,273 相对 Star 比例偏高，反映大量用户自建部署
