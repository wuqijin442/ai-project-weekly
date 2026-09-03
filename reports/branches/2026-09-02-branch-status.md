# 远程仓库分支状态核对 — 2026-09-02

> 自动 `git fetch --prune` 后比对各分支相对 `main` 的领先/落后提交与最近提交，结论基于真实 git 元数据，无推测。

**基准分支**：`main`　**分支总数**：3　**核对时间**：2026-09-03 08:31:48

**数据来源**：api.github.com（github.com 主站 IP 阻断，本地引用不可信）


## 各分支总览

| 分支 | 领先 main | 落后 main | 最近提交 | 作者 | 日期 |
|---|---|---|---|---|---|
| `dgx` | 1 | 176 | chore: 每日学习消化+图谱 2026-09-03 [dgx] | wuqijin442 | 2026-09-02 |
| `main` | 0 | 0 | Merge pull request #61 from wuqijin442/w | Worn Quiet Joy | 2026-09-02 |
| `win` | 3 | 4 | [2026-09-02] Daily AI Project Update | wuqijin442 | 2026-09-03 |

## 领先 main 的待归集提交


### `dgx`（领先 main 1 个提交，待 20:00 归集）

- 4e7793ce5d 2026-09-02 wuqijin442 chore: 每日学习消化+图谱 2026-09-03 [dgx]

### `win`（领先 main 3 个提交，待 20:00 归集）

- 9f2c83da31 2026-09-03 wuqijin442 [2026-09-03] Daily AI Project Update
- cc70978be2 2026-09-03 wuqijin442 [2026-09-02] 删除误落期分支报告(跨零点脚本误用 09-03)，改由 --date 2026-09-02 重
- 46932c5969 2026-09-03 wuqijin442 [2026-09-02] Daily AI Project Update

---

### 说明

- 本核对仅读取 git 元数据，不克隆任何项目，耗时极短。
- ⚠️ **数据来源说明**：本次 `git fetch --prune` 因 github.com 主站 IP 层阻断失败，本地 `origin/*` 引用不可信，故领先/落后数字改由 **api.github.com** 的 `/branches` 与 `/compare` 接口实时核算（服务端权威引用），结论可靠。待主站恢复后下轮将自动回到本地 fetch 路径。
- 当前多机分支模型：`win`=Windows 端每日数据、`dgx`=dgx 端学习消化产物，二者由每日 20:00 归集任务（src/merge_branches.sh）经 GitHub PR 合并进 `main`。
- Windows 自动化 17:30 运行时，`win`/`dgx` 通常领先 `main`，属**正常的待归集状态**；若某分支长期大幅领先 main 未归集，需排查 20:00 归集任务是否异常。