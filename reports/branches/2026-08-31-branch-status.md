# 远程仓库分支状态核对 — 2026-08-31

> 自动 `git fetch --prune` 后比对各分支相对 `main` 的领先/落后提交与最近提交，结论基于真实 git 元数据，无推测。

**基准分支**：`main`　**分支总数**：3　**核对时间**：2026-08-31 09:55:24


## 各分支总览

| 分支 | 领先 main | 落后 main | 最近提交 | 作者 | 日期 |
|---|---|---|---|---|---|
| `dgx` | 1 | 141 | chore: 每日学习消化+图谱 2026-08-29 [dgx] | wuqijin442 | Sat Aug 29 03:14:08 2026 +0800 |
| `main` | 0 | 0 | Merge pull request #54 from wuqijin442/d | Worn Quiet Joy | Fri Aug 28 20:02:20 2026 +0800 |
| `win` | 15 | 94 | [2026-08-31] Daily AI Project Update | wuqijin442 | Mon Aug 31 09:34:18 2026 +0800 |

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