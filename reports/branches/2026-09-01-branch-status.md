# 远程仓库分支状态核对 — 2026-09-01

> 自动 `git fetch --prune` 后比对各分支相对 `main` 的领先/落后提交与最近提交，结论基于真实 git 元数据，无推测。

**基准分支**：`main`　**分支总数**：3　**核对时间**：2026-09-02 10:54:09


## 各分支总览

| 分支 | 领先 main | 落后 main | 最近提交 | 作者 | 日期 |
|---|---|---|---|---|---|
| `dgx` | 1 | 145 | chore: 每日学习消化+图谱 2026-09-02 [dgx] | wuqijin442 | Wed Sep 2 03:03:30 2026 +0800 |
| `main` | 0 | 0 | Merge pull request #59 from wuqijin442/d | Worn Quiet Joy | Tue Sep 1 20:00:10 2026 +0800 |
| `win` | 22 | 103 | [2026-09-02] Daily AI Project Update | wuqijin442 | Wed Sep 2 10:50:09 2026 +0800 |

## 领先 main 的待归集提交


### `dgx`（领先 main 1 个提交，待 20:00 归集）

- 408a6e6 2026-09-02 wuqijin442 chore: 每日学习消化+图谱 2026-09-02 [dgx]

### `win`（领先 main 22 个提交，待 20:00 归集）

- 6ae9874 2026-09-02 wuqijin442 [2026-09-02] Daily AI Project Update
- ffb72c2 2026-09-01 wuqijin442 [2026-09-01] Daily AI Project Update
- 91134c7 2026-09-01 wuqijin442 [2026-09-01] Daily AI Project Update
- 52cbb5e 2026-09-01 wuqijin442 [2026-09-01] Daily AI Project Update
- 27bd0fd 2026-08-31 wuqijin442 [2026-08-31] rag_lib: 排除 energy 向量索引导出(.obsidian噪声) 提升 RAG 检索质量
- a70b0e3 2026-08-31 wuqijin442 [2026-08-31] fix: download_tarball 用 os.rename 替代 shutil.move 防批量删除保护杀进程 + branch-status 补 api.github.com 复核数据
- 778201e 2026-08-31 wuqijin442 [2026-08-31] Daily AI Project Update
- 2d92e9a 2026-08-31 wuqijin442 [2026-08-31] Daily AI Project Update
- 314804a 2026-08-31 wuqijin442 [2026-08-31] Add src/ask.py — RAG-based private knowledge Q&A CLI
- 0d95005 2026-08-31 wuqijin442 [2026-08-31] Daily AI Project Update
- …（其余 12 条未列出）

---

### 说明

- 本核对仅读取 git 元数据，不克隆任何项目，耗时极短。
- 当前多机分支模型：`win`=Windows 端每日数据、`dgx`=dgx 端学习消化产物，二者由每日 20:00 归集任务（src/merge_branches.sh）经 GitHub PR 合并进 `main`。
- Windows 自动化 17:30 运行时，`win`/`dgx` 通常领先 `main`，属**正常的待归集状态**；若某分支长期大幅领先 main 未归集，需排查 20:00 归集任务是否异常。