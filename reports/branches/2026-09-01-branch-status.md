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

### 【09-02 更新】根因已定位并修复 ✅

- **根因**：08-31 09:22/09:23 同一份 RAG 提交（Add src/ask.py）被双推 win(314804a) 与 main侧(b6ac214) → src/ask.py/rag_index.py/rag_lib.py/rag_query.py 形成 add/add 冲突（内容同仅文件模式 100755vs100644；rag_lib 有 13 行 exclude 增强漂移）→ PR#55(win→main, 08-28 起 open) 每日被 GitHub 拒自动合 → 现役 main 版 merge_branches.sh 的 api_pr_merge 失败后转本地兜底合并，但兜底前不 rebase（同轮 dgx 已走 API 合入致本地 main 过期）→ 推送必非快进失败，日复一日静默。
- **处置（09-02 15:13）**：本地 merge main→win 逐文件裁决（merge_branches/push_retry 取 main 现役 PR 版；main.py 取 win 的 os.rename 版；rag_lib 保留 win 的 exclude 增强并补回 100755）→ 提交 28601f6 推送 win → PR#55 经 API 合并成功（merge commit c160ecf），win 已归集进 main，领先归零。
- **防复发**：① DGX 侧 RAG 代码只推 dgx 分支，禁止双推 win；② merge_branches.sh 兜底路径应补 pull --rebase（待下轮由 dgx 侧合入 main）。

---

### 说明

- ✅ 已与 api.github.com（/branches + /compare 接口）交叉复核，ahead/behind 与最近提交数字一致。
- ⚠️ **win 分支自 08-27（PR #53）起已连续 5 天未归集进 main**（08-28 起每日 20:00 仅合并了 dgx：PR #54~#59 全为 `dgx -> main`），领先 main 达 22 个提交，需排查 dgx 侧 20:00 归集任务中 win 合并腿是否失败。
- 本核对仅读取 git 元数据，不克隆任何项目，耗时极短。
- 当前多机分支模型：`win`=Windows 端每日数据、`dgx`=dgx 端学习消化产物，二者由每日 20:00 归集任务（src/merge_branches.sh）经 GitHub PR 合并进 `main`。
- Windows 自动化 17:30 运行时，`win`/`dgx` 通常领先 `main`，属**正常的待归集状态**；若某分支长期大幅领先 main 未归集，需排查 20:00 归集任务是否异常。