---
aliases: [reverse-skill, 逆向技能路由包, Cybersecurity Skills Router]
tags: [AI, Trending, PowerShell, Skills, Security, Reverse-Engineering, Vibe-Coding]
stars: 16853
created_at: 2026-05-13
today_growth: 2446
status: 今日最佳🔝（首入榜 #1，严格关键词命中）
date_accessed: 2026-08-04
---

# reverse-skill

**项目地址**：https://github.com/zhaoxuya520/reverse-skill
**作者**：zhaoxuya520
**⭐ 总 Star**：16,853（16.9k）  <!-- 18:00 复核值；10:22 首采 15,967 -->
**📈 今日新增**：🔺2,446 stars
**🍴 Fork**：2,243
**💻 主要语言**：PowerShell
**📅 开源时间**：2026-05-13
**🔄 最近推送**：2026-08-03
**📜 许可证**：MIT

## 项目定位

**Cybersecurity Skills Router · 逆向技能路由包**——把逆向工程、授权渗透测试、安全研究封装成一整套**技能路由包（Skill Router Pack）**，交给 AI 编码客户端直接调度。三大支柱：

1. **AI 自动路由**：任务进来先由 `skills/MASTER-ROUTING.md` 做快速分级（PRIMARY fast ladder），再经 `skills/routing.md` 的「任务 → 技能」矩阵派发到具体技能目录。
2. **按需自举工具链**：需要 jadx / apktool / Frida / IDA / radare2 等工具时按需引导安装，`skills/tool-index.md` 自动生成本地工具检测状态。
3. **自动进化经验库**：实战过程沉淀进 `skills/field-journal/`，形成可复用的经验积累。

关键设计：`RULES.md` 定义**全局路由规则与 scope gate**——在 ACT（实际动作）之前先过授权范围闸门，配合 `skills/ops/` 的 scope / evidence chain（证据链）/ roles / timeline 契约，把「授权渗透」的合规约束写进 Agent 工作流本身。

## 技术栈

- **语言/脚本**：PowerShell（Windows 主链）+ Bash（Linux / macOS / Kali）
- **依赖环境**：Java / JDK（jadx、apktool）、Node.js 22.12+（JS 工具链与 MCP 服务）、Python 3.x（Frida 与辅助脚本）
- **AI 客户端**：Claude Code、Kiro、**Cursor**、**Cline**、Codex CLI 等代码 AI 客户端
- **协议/集成**：MCP 服务（含 Reqable MCP 抓包）
- **许可证**：MIT

## 覆盖场景（20+ 技能域）

| 场景 | 技能入口 |
|------|---------|
| APK / Android 分析 | `skills/apk-reverse/` |
| iOS / 移动端 | `skills/mobile-reverse/` |
| 二进制逆向（exe/dll/so/elf） | `skills/ida-reverse/`、`skills/radare2/` |
| .NET / C# | `skills/dotnet-reverse/` |
| 前端 JS / 加密参数 | `skills/js-reverse/` |
| DSL VM / 自定义 JS 字节码 VM | `skills/reverse-engineering/dsl-vm-reverse/` |
| 恶意样本 / YARA | `skills/malware-analysis/` |
| 渗透测试 / 扫描 | `skills/pentest-tools/` |
| 攻击链 / 红队编排 | `skills/attack-chain/` |
| CTF 竞赛 | `CTF-Sandbox-Orchestrator/`（40+ 子技能） |
| 固件 / IoT | `skills/firmware-pentest/` |
| 补丁 diff / N-day | `skills/patch-diff-exploit/` |
| Pwn / 漏洞利用开发 | `skills/pwn-chain/` |
| EDR 绕过 | `skills/edr-bypass-re/` |
| API / GraphQL 安全 | `skills/api-security/` |
| 供应链 / SBOM | `skills/supply-chain-security/` |
| LLM / AI 安全 | `skills/llm-security/` |
| 图表 / 报告生成 | `skills/diagram-generator/`、`skills/docs-generator/` |

## 安装方式

```bash
git clone https://github.com/zhaoxuya520/reverse-skill.git

# 刷新工具索引
# Windows
powershell -File skills/scripts/refresh-tool-index.ps1
# Linux / macOS
bash skills/scripts/refresh-tool-index.sh
# Kali Linux
bash kali/scripts/refresh-tool-index.sh
```

## 关键文件

| 文件 | 用途 |
|------|------|
| `README_AI.md` | AI Agent 引导与配置入口 |
| `RULES.md` | 全局路由规则（ACT 前 scope gate） |
| `skills/MASTER-ROUTING.md` | PRIMARY 快速分级阶梯 |
| `skills/routing.md` | 任务 → 技能路由矩阵 |
| `skills/SKILL.md` | 技能总入口 |
| `skills/tool-index.md` | 本地工具状态（自动生成） |
| `skills/scripts/master-route.ps1` | 一次性 PRIMARY 分诊 |
| `skills/scripts/case-init.ps1` | 案件目录：scope / timeline / workitems |

## 使用场景

- 在 Claude Code / Cursor / Cline 中直接下达「分析这个 APK 的加密逻辑」，由路由层自动挑选技能与工具链
- 授权渗透项目的**证据链与时间线留痕**（`skills/ops/` 契约）
- CTF 竞赛的沙箱编排与 40+ 子技能调度

## 外部链接

- GitHub：https://github.com/zhaoxuya520/reverse-skill
- 平台文档：`kali/README-kali.md`、`docs/platforms/linux.md`、`docs/platforms/macos.md`
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-08-04|2026-08-04 日报]]（首入榜 #1，今日最佳🔝，严格关键词命中 Cursor / Cline）

## 备注

- 今日以 +2,446 同时登顶 **Vibe Coding 榜与 GitHub 全站日榜**
- 本日唯一严格关键词命中项（简介同时含 Cursor 与 Cline）
- 强调「**授权**渗透测试」，RULES 层做 scope gate，合规边界写进 Agent 工作流
- 本地案件目录 `work/` 已 gitignore，避免敏感数据入库
