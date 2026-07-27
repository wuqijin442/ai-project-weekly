---
aliases: [CubeSandbox, cube-sandbox]
tags: [AI, Trending, Rust, Sandbox, Agents, Vibe-Coding]
stars: 8915
created_at: 2026-04-10
today_growth: 564
status: 热门
date_accessed: 2026-07-09

# CubeSandbox

**项目地址**：https://github.com/TencentCloud/CubeSandbox
**作者**：TencentCloud（腾讯云）
**⭐ 总 Star**：8,915
**📈 今日新增**：564 stars
**💻 主要语言**：Rust
**当前版本**：0.3.0（PyPI）

## 项目定位

CubeSandbox 是一套**为 AI Agent 打造的高性能、开箱即用的安全沙箱服务**。基于 RustVMM 与 KVM 微虚机（microVM）技术，为代码执行、工具调用、Agent 工作流提供硬件级隔离的运行环境，是 Vibe Coding 时代 AI 编程代理安全执行不可信代码的关键基础设施。

核心理念：AI Agent 需要"能跑代码"的隔离环境，但传统容器启动慢、隔离弱。CubeSandbox 以十毫秒级冷启动、硬件级隔离、E2B 兼容 API 和高密度并发，成为 AI 原生（AI-native）运行时的代表项目，已入选 CNCF Landscape（AI 原生基础设施）。

## 核心特性

- **⚡ 极速启动**：冷启动低至十毫秒级（Tens of ms）
- **🔒 硬件级隔离**：基于 KVM / RustVMM 的微虚机（microVM），强隔离
- **🔌 E2B 兼容 API**：可无缝替换 E2B，复用现有 Agent 沙箱生态
- **📦 高密度高并发**：单节点支持高并发、高密度部署

## 技术栈

- **虚拟化底座**：RustVMM + KVM（硬件级微虚机隔离）
- **接口**：E2B 兼容 REST API
- **SDK**：Python 包 `cubesandbox`（PyPI 0.3.0）
- **生态**：CNCF Landscape（AI-native Infra → Workload Runtime）
- **许可证**：Apache 2.0

## 安装方式

```bash
pip install cubesandbox
```

## 使用场景

- AI 编程代理的**代码执行沙箱**（运行 LLM 生成的不确定代码）
- Agent 工具调用的隔离运行时
- 多 Agent 并发任务的高密度执行环境

## 外部链接

- GitHub：https://github.com/TencentCloud/CubeSandbox
- 文档（Quick Start）：https://github.com/TencentCloud/CubeSandbox
- X(Twitter)：https://x.com/CubeSandbox_AI
- 许可证：Apache 2.0

## 相关日期

- [[Vibe-Coding-2026-07-09|2026-07-09 日报]]

## 备注

- 已入选 CNCF Landscape（AI 原生基础设施 → 工作负载运行时）
- 定位对标 E2B，主打更低的启动延迟与更强的隔离保障
