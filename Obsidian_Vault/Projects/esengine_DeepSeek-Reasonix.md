---
aliases: [DeepSeek-Reasonix, Reasonix, reasonix]
tags: [AI, Trending, Go, Coding-Agent, CLI, TUI, DeepSeek, Vibe-Coding]
stars: 33297
created_at: 2026-04-21
weekly_growth: 4704
status: 热门（全赛道周榜 #5，本周 🔺4,704）
date_accessed: 2026-08-09
---

# DeepSeek-Reasonix

**项目地址**：https://github.com/esengine/DeepSeek-Reasonix
**作者**：esengine
**⭐ 总 Star**：33,297（33.3k）  <!-- 2026-08-09 实时值；08-07 为 32,749 -->
**📈 本周新增**：🔺4,704 stars（全赛道周榜 #5）
**🍴 Fork**：2,114
**👁 Watch**：91
**💻 主要语言**：Go
**📅 开源时间**：2026-04-21
**🔄 最近推送**：2026-08-07
**🌐 官网**：http://reasonix.io/
**📜 许可证**：MIT

## 项目定位

**DeepSeek 原生的终端 AI 编码 Agent**。核心工程主张只有一句：*Engineered around prefix-cache stability — leave it running.*（围绕**前缀缓存稳定性**做工程设计，可长时间常驻运行）。

这是编码 Agent 竞争进入「成本与稳定性工程」阶段的直接信号：不再比拼能力堆叠，而是比拼**长会话下 prompt cache 不失效、token 成本可控、进程能一直挂着**。

## 分发路径（四条）

| 路径 | 形态 | 安装 |
|------|------|------|
| A | CLI / TUI | `npm i -g reasonix`（全平台预编译原生二进制）／`brew install esengine/reasonix/reasonix`（macOS） |
| B | 桌面应用 | 官网下载页；macOS 通用 `.dmg`、Windows `.exe`/便携 `.zip`（x64 / ARM64，SignPath 代码签名）、Linux `.deb`/`.tar.gz` |
| C | VS Code 扩展 | `SivanLiu.reasonix-agent`（Marketplace / Open VSX），启动本地 `reasonix acp` 后端 |
| D | 源码构建 | `make build` → `bin/reasonix`；`make cross` → `dist/`（darwin\|linux\|windows × amd64\|arm64） |

## 核心能力

- **Context Engine v2**：会话记忆与检索
- **子代理 profile（Subagent Profiles）**：多角色分工
- **Checkpoints & rewind**：检查点与回滚
- **ACP 编辑器集成**：统一的编辑器接入协议（VS Code / VSCodium / Eclipse Theia）
- **能力诊断（Capability Diagnostics）** 与 **恢复/更新（Recovery）**
- **任务契约与暂停策略（Task Contract）**、**工具契约（Tool Contract）**

## 技术栈

- **语言**：Go（核心引擎）+ TypeScript / Ink（TUI）
- **模型**：DeepSeek 原生（R1 系列），支持 prompt caching
- **topics**：`agent`、`agent-framework`、`ai-agent`、`ai-coding`、`cli`、`coding-agent`、`deepseek`、`developer-tools`、`ink`、`llm`、`prompt-caching`、`r1`、`terminal`、`tool-use`、`tui`
- **许可证**：MIT

## 快速上手

```sh
npm i -g reasonix
reasonix setup                       # 配置 provider 与模型
reasonix                             # 交互式会话
reasonix run "implement the TODOs in main.go"
# 会话内执行 /init 让 Reasonix 生成项目说明
```

## 使用场景

- 终端常驻的编码 Agent，长任务不重启、缓存不失效
- 需要 DeepSeek 系列模型（成本敏感）的团队
- 通过 ACP 在 VS Code / VSCodium 中获得原生对话、编辑器上下文、工具调用审批

## 外部链接

- GitHub：https://github.com/esengine/DeepSeek-Reasonix
- 官网：http://reasonix.io/
- 文档：`docs/GUIDE.md`、`docs/CLI.md`、`docs/ACP.md`、`docs/SPEC.md`
- npm：`reasonix`
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-08-04|2026-08-04 日报]]（首入榜 #4）
- [[Vibe-Coding-2026-08-05|2026-08-05 日报]]（二度上榜 #3，⭐31.1k / 🔺922）
- [[Vibe-Coding-2026-08-06|2026-08-06 日报]]（三度上榜 #4，⭐32.0k / 🔺747）
- [[AI-Weekly-2026-08-09|2026-08-09 全赛道周报]]（周榜 #5，🔺4,704 / ⭐33.3k）

## 备注

- **成长曲线**：2026-08-04 ⭐30,398（+883）→ 2026-08-05 ⭐31,139（+922）→ 2026-08-06 ⭐32,010（+747）→ 2026-08-09 ⭐33,297（+4,704 本周）。⭐ 突破 3.3 万，但日增在 08-08 实测仅 +144（-84%），本周第 5 名次主要来自周窗口前半段存量

- 与 07-30 上榜的 1jehuang/jcode（「最省 RAM 的 harness」）同属「终端编码 Agent 工程化」主线，二者分别主打**缓存稳定**与**内存占用**
- Windows 安装包由 SignPath Foundation 提供免费证书完成代码签名
