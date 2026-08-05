---
date: 2026-08-05
mode: 工作日（Vibe Coding 赛道）
project_count: 5
tags: [AI, Trending, Vibe-Coding, Daily, GitHub]
source: GitHub Trending 全局日榜（飙升榜，按当日新增 Star 降序）
---

# Vibe Coding 每日榜 · 2026-08-05（周三）

> 数据源：GitHub Trending 全局日榜（`/trending?since=daily`，18 仓库解析）+ GitHub REST API 实时补全
> 赛道口径：Vibe Coding / AI 编码 Agent。**严格关键词命中 3 个**（reverse-skill、video-use、compound-engineering-plugin），按生态扩充 2 个补足 Top 5。

## 今日最佳开源项目 🔝

> [!tip] **[[zhaoxuya520_reverse-skill|zhaoxuya520/reverse-skill]]** — 🔺2,297 / ⭐18.7k
> **逆向 · 渗透 · 安全研究的「技能路由包」，二度登顶。**
> AI 自动路由 + 按需自举工具链 + 自动进化经验库，明确支持 Claude Code / Kiro / **Cursor** / **Cline** 等编码 AI 客户端。今日以 +2,297 蝉联 Vibe Coding 榜首，同时位居 GitHub 全站日榜第 2；一天之内 ⭐16.9k → ⭐18.7k，说明「**把专业领域打包成 Agent 可调度的技能路由**」这条路线正在被市场快速验证。

## Top 5 榜单

| # | 项目 | 简介 | 语言 | ⭐ Star | 📈 今日新增 | 入选依据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [[zhaoxuya520_reverse-skill\|zhaoxuya520/reverse-skill]] 🔝 | 逆向/渗透/安全技能路由包，AI 自动路由 + 工具链自举 + 经验库自进化 | PowerShell | 18.7k | 🔺2297 | 严格命中 `cursor` `cline` |
| 2 | [[TencentCloud_TencentDB-Agent-Memory\|TencentCloud/TencentDB-Agent-Memory]] | 团队级 Agent 记忆中枢，对话/文档/代码 → 四类可治理记忆资产 | TypeScript | 14.5k | 🔺1111 | 生态扩充 |
| 3 | [[esengine_DeepSeek-Reasonix\|esengine/DeepSeek-Reasonix]] | DeepSeek 原生终端编码 Agent，围绕 prefix-cache 稳定性做工程 | Go | 31.1k | 🔺922 | 生态扩充 |
| 4 | [[browser-use_video-use\|browser-use/video-use]] | 用编码 Agent 剪视频：素材丢进文件夹，对话产出 final.mp4 | Python | 19.6k | 🔺320 | 严格命中 `browser-use` |
| 5 | [[EveryInc_compound-engineering-plugin\|EveryInc/compound-engineering-plugin]] | Compound Engineering 官方插件，覆盖 Claude Code / Codex / Cursor | TypeScript | 24.0k | 🔺40 | 严格命中 `cursor` |

## 趋势解读

### 1. 「领域知识 → 技能路由包」成为最强主线
[[zhaoxuya520_reverse-skill|reverse-skill]] 二度登顶（+2,297，全站日榜 #2）。它的价值不在某个逆向工具，而在 `MASTER-ROUTING.md` → `routing.md` 的**两级路由层**：任务进来先分级、再派发到 20+ 技能域，需要 jadx / Frida / IDA 时按需自举工具链。这与 7 月以来的 `book-to-skill`（技术书→技能）、`reverse-skill`（安全领域→技能）构成同一条曲线——**Agent Skills 从「能力封装」升级为「领域知识资产的调度层」**。

### 2. Agent 记忆从「个人」走向「团队治理」
[[TencentCloud_TencentDB-Agent-Memory|TencentDB Agent Memory]] 三度上榜（07-09 首入 ⭐7.6k → 08-04 ⭐12.6k → 今日 ⭐14.5k，不到一个月 +91%）。官方描述已从「本地长期记忆」改写为「**团队级记忆中枢**」，四类资产 Chat Memory / Skill / LLM-Wiki / **Code-Graph** 中，Code-Graph 直接切进编码 Agent 的代码理解底座。记忆层正在从工具变成基础设施。

### 3. 终端编码 Agent 的竞争点是「成本与稳定性」
[[esengine_DeepSeek-Reasonix|DeepSeek-Reasonix]] 二度上榜（⭐31.1k / +922），主张只有一句：*Engineered around prefix-cache stability — leave it running.* 与 07-30 的 `jcode`（最省 RAM 的 harness）呼应——能力堆叠阶段已过，**长会话下 prompt cache 不失效、进程能一直挂着**才是新的差异点。

### 4. 编码 Agent 越界到非编码工作流
[[browser-use_video-use|video-use]] 把 Claude Code 变成视频剪辑师：自动剪填充词、色彩分级、30ms 音频淡入淡出防爆音、并行子代理生成动画覆盖层、渲染后自评每个剪辑点、`project.md` 持久化会话记忆。**"coding agent" 里的 coding 正在褪色，剩下的是 agent + shell + skill 这套通用底座。**

### 5. 方法论层：Compound Engineering 与 superpowers 的分野
[[EveryInc_compound-engineering-plugin|compound-engineering-plugin]] 首入榜（⭐24.0k，Every 出品），口号是 *AI skills that make each unit of engineering work easier than the last*——把工程复利做成跨 Claude Code / Codex / Cursor 的官方插件。与之相邻的 [[obra_superpowers|obra/superpowers]] 今日 +653、⭐266.9k（本日次席生态候选，未入 Top 5 因严格命中优先），二者同属「**agentic 方法论产品化**」赛道。

### 边界排除说明
今日日榜前列的高增长项目中，以下判定为**非编码 Agent**，未纳入 Vibe Coding 赛道：
`firecrawl/pdf-inspector`(+2540，PDF 解析库)、`lyogavin/airllm`(+1711，单卡推理)、`microsoft/generative-ai-for-beginners`(+783，教程)、`usekaneo/kaneo`(+559，项目管理)、`livekit/agents`(+432，实时语音 Agent)、`uber/ADR`(+148，Agent 安全观测)、以及 `tailwindcss`/`deno`/`angular`/`cypress`/`webpack`/`spdlog` 等传统 OSS。`sponsors/*` 推广位伪条目已剔除。

## 相关链接

- [[_Index|全局索引]]
- 上一期：[[Vibe-Coding-2026-08-04|2026-08-04 日报]]
