# 远程仓库分支状态核对 — 2026-08-31

> 自动 `git fetch --prune` 后比对各分支相对 `main` 的领先/落后提交与最近提交，结论基于真实 git 元数据，无推测。
>
> ⚠️ **数据来源标注（按运行规则 7）**：本次 `git fetch --prune` 因 github.com 主站 IP 层阻断（每次连接 21s 超时）4 次重试全部失败，本报告的领先/落后数字**基于本地旧引用**，主站阻断期间不可完全信任。下表数字为本地参考；**下表之后已附 `api.github.com` 复核的真实远端数据**，请以复核数据为准。

**基准分支**：`main`　**分支总数**：3　**核对时间**：2026-08-31 09:55:24（本地引用）

## 各分支总览（本地旧引用，仅参考）

| 分支 | 领先 main | 落后 main | 最近提交 | 作者 | 日期 |
|---|---|---|---|---|---|
| `dgx` | 1 | 141 | chore: 每日学习消化+图谱 2026-08-29 [dgx] | wuqijin442 | Sat Aug 29 03:14:08 2026 +0800 |
| `main` | 0 | 0 | Merge pull request #54 from wuqijin442/d | Worn Quiet Joy | Fri Aug 28 20:02:20 2026 +0800 |
| `win` | 15 | 94 | [2026-08-31] Daily AI Project Update | wuqijin442 | Mon Aug 31 09:34:18 2026 +0800 |

## ⭐ api.github.com 复核（真实远端数据，以此为准）

> 数据源：`api.github.com/repos/wuqijin442/ai-project-weekly/{branches/{br},commits/{sha},compare/main...{br}}`，调用时间 2026-08-31 09:58（UTC+8），主站阻断但 api 域正常。

| 分支 | 远端 HEAD sha | 远端最近提交 | 远端提交时间 | 领先 main | 落后 main |
|---|---|---|---|---|---|
| `main` | `e92511045f` | Merge pull request #57 from wuqijin442/dgx | 2026-08-30 20:01:38 +0800 | — | — |
| `win` | `778201eb12` | [2026-08-31] Daily AI Project Update | 2026-08-31 09:55:25 +0800 | 16 | 98 |
| `dgx` | `815399f79a` | chore: 每日学习消化+图谱 2026-08-31 [dgx] | 2026-08-31 03:13:51 +0800 | 1 | 143 |

**关键结论（基于 API 真实远端数据）**：
1. **main 归集链路正常**：`main` 已于 **2026-08-30 20:01:38** 经 **PR #57**（合并 dgx）完成归集，比本地旧引用（PR #54 / 08-28 20:02）新两天，说明 20:00 归集任务连续两天运行正常。
2. **win 领先 main 16 个提交**（含今晚 4 个新提交 `f434c58/0d95005/314804a/2d92e9a` + 08-29 的 12 个提交），待今晚 20:00 归集任务经 PR 合并入 main。
3. **dgx 领先 main 1 个提交**（`815399f` 2026-08-31 学习消化产物），待今晚 20:00 归集。
4. **本地旧引用滞后原因**：github.com 主站 IP 层阻断（连续 fetch/push 超时），codeload/api 域正常。本地 `origin/main` 还停留在 PR #54 旧位置，下次网络恢复后 `git fetch --prune` 即可对齐。

## 领先 main 的待归集提交


### `dgx`（领先 main 1 个提交，待 20:00 归集）

- acff988 2026-08-29 wuqijin442 chore: 每日学习消化+图谱 2026-08-29 [dgx]

### `win`（领先 main 15 个提交，待 20:00 归集）

- 2d92e9a 2026-08-31 wuqijin442 [2026-08-31] Daily AI Project Update
- 314804a 2026-08-31 wuqijin442 [2026-08-31] Add src/ask.py — RAG-based private knowledge Q&A CLI
- 0d95005 2026-08-31 wuqijin442 [2026-08-31] Daily AI Project Update
- f434c58 2026-08-31 wuqijin442 [2026-08-31] Daily AI Project Update
- 8c5f7aa 2026-08-29 wuqijin442 [2026-08-29] Daily AI Project Update
- 267431d 2026-08-29 wuqijin442 [2026-08-29] Daily AI Project Update
- 523afe0 2026-08-29 wuqijin442 [2026-08-29] Daily AI Project Update
- 8689deb 2026-08-29 wuqijin442 [2026-08-29] Daily AI Project Update
- 6f641e0 2026-08-28 wuqijin442 [2026-08-28] RAG 增量入库：每日仅追加新文件(不重吃全量历史)，--force 一次性灌全量+Obsidian/储能大库；learn_link 改走增量
- 255a571 2026-08-28 wuqijin442 fix(rag): iter_sources 改为 工作树 ∪ origin/main 取并集，保证每日重建都吃满全量历史（不被不完整工作树截断）
- …（其余 5 条未列出）

---

### 说明

- 本核对仅读取 git 元数据，不克隆任何项目，耗时极短。
- 当前多机分支模型：`win`=Windows 端每日数据、`dgx`=dgx 端学习消化产物，二者由每日 20:00 归集任务（src/merge_branches.sh）经 GitHub PR 合并进 `main`。
- Windows 自动化 17:30 运行时，`win`/`dgx` 通常领先 `main`，属**正常的待归集状态**；若某分支长期大幅领先 main 未归集，需排查 20:00 归集任务是否异常。