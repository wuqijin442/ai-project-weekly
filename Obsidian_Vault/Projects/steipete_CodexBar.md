---
aliases: [CodexBar, codexbar]
tags: [AI, Trending, Swift, Claude, Cursor, Codex, Copilot, Vibe-Coding]
stars: 17021
created_at: 2025-11-16
today_growth: 377
status: 待分析
date_accessed: 2026-07-08
---

# CodexBar

**项目地址**：https://github.com/steipete/CodexBar
**作者**：steipete（Peter Steinberger）
**⭐ 总 Star**：17,021
**📈 今日新增**：377 stars
**💻 主要语言**：Swift
**当前版本**：0.41.0
**提交历史**：3,317 次提交

## 项目定位

macOS 14+ 菜单栏应用，用于实时显示 50+ 个 AI 编码服务提供商的使用量统计和配额限制。口号："Every AI coding limit, in your menu bar."（每个 AI 编码限制，尽在菜单栏）

## 核心功能

| 功能类别 | 详细说明 |
|---------|---------|
| 多提供商菜单栏 | 每个提供商独立状态项，支持逐个开关 |
| 使用量计量器 | 提供商专属的使用量计量器，带重置倒计时 |
| 花费/使用量图表 | OpenAI、Claude Admin API、OpenRouter、LiteLLM 等的内联图表 |
| 成本使用扫描 | Codex + Claude 可配置的成本使用扫描 |
| 提供商状态轮询 | 事故徽章 + 图标叠加指示器 |
| CLI 工具 | `codexbar` 命令行工具，支持脚本和 CI 使用 |
| WidgetKit 小组件 | 支持部分提供商的桌面小组件 |
| 多语言本地化 | 21 种语言 |

## 支持的 AI 编码服务商（50+）

Codex、OpenAI、Claude、Cursor、Gemini、Copilot、Grok、GroqCloud、ElevenLabs、Deepgram、z.ai、MiniMax、Kiro、Zed、Vertex AI、Augment、OpenRouter、LiteLLM、LLM Proxy、Codebuff、Command Code、AWS Bedrock 等。

## 为什么需要 CodexBar

- **围绕重置做规划**：每个提供商的会话、周窗口和月窗口及重置倒计时
- **余额、花费和成本扫描**：信用余额、Admin API 花费面板、提供商账单摘要
- **实时状态**：提供商状态轮询，在菜单中显示事故徽章
- **隐私优先**：复用已有提供商会话（OAuth、设备流、API 密钥、浏览器 Cookie），不存储密码

## 安装方式

```bash
# Homebrew（推荐）
brew install --cask codexbar

# 或从 GitHub Releases 下载
# https://github.com/steipete/CodexBar/releases
```

CLI 工具安装：
```bash
# macOS/Linux tarball
# 下载后解压，运行安装脚本
./bin/install-codexbar-cli.sh
```

## 技术栈

- **平台**：macOS 14+ (Sonoma)、Linux (CLI)
- **编程语言**：Swift 6.2+
- **构建系统**：Swift Package Manager
- **代码规范**：SwiftFormat、SwiftLint（严格并发）
- **更新机制**：Sparkle 自动更新
- **桌面小组件**：WidgetKit
- **密钥管理**：macOS Keychain
- **Linux 桌面集成**：Waybar、GNOME Shell、KDE Plasma、Quickshell

## 配置

配置文件路径：
- 新安装：`~/.config/codexbar/config.json`
- 已有安装：`~/.codexbar/config.json`

通过 CLI 设置 API 密钥：
```bash
codexbar config enable --provider grok
printf '%s' "$GROQ_API_KEY" | codexbar config set-api-key --provider groq --stdin
```

## 外部链接

- GitHub：https://github.com/steipete/CodexBar
- 作者 Twitter：https://twitter.com/steipete
- 相关项目：
  - Win-CodexBar（Windows 版本）：https://github.com/Finesssee/Win-CodexBar
  - codexbar-waybar（Wayland）：https://github.com/Marouan-chak/codexbar-waybar
  - KodexBar（KDE Plasma）：https://github.com/tylxr59/KodexBar
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-07-08|2026-07-08 日报]]

## 备注

- 作者其他项目：Trimmy（多行 shell 片段扁平化）、MCPorter（MCP 服务器 TypeScript 工具包）、Oracle（GPT-5 Pro 上下文调用工具）
- 灵感来源：ccusage (MIT)
- 不请求屏幕录制、无障碍权限（后台）
- 可选启用完全磁盘访问（仅用于读取 Safari Cookie/本地存储）
