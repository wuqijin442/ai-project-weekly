# 2026-08-12 归集同步核查报告（人工核查 · 非自动化产出）

> 核查时间：2026-08-12 08:0x ~ 08:12 (GMT+8)
> 核查对象：2026-08-11 自动化收尾时列出的两条待跟进项
> **数据来源：api.github.com**（github.com 主站当时被阻断，`git fetch` 连接失败，本地引用不可信）

---

## 核查结论总览

| # | 待跟进项（08-11 提出） | 核查结果 | 处置 |
|---|---|---|---|
| ① | 自动化 `cwds` 仍登记 D 盘（主工作树已迁 E） | ❌ **确认未同步** | ✅ 已改为 E 盘，并在 prompt 顶部固化运行环境铁律 |
| ② | 20:00 归集任务疑因迁 E 而失效 | ✅ **归集正常，该担忧属误判** | 无需处置（已在 prompt 中注明归集与本机路径无关） |

---

## 一、核查前提：本地 git 数据不可信

首次核查执行 `git fetch --prune origin` 时：

```
fatal: unable to access 'https://github.com/wuqijin442/ai-project-weekly.git/':
Failed to connect to github.com:443 after 21150 ms: Could not connect to server
```

此时基于本地缓存引用得出的数字（win 领先 7 / dgx 领先 1）**全部失效**。
另外该命令中 `git fetch ... | tail -8` 使 `$?` 恒为 0，输出 `FETCH_EXIT=0` 的假成功信号——即项目已知铁律「禁止用管道判定 git 成败」的又一次现场复现。

改走 `api.github.com`（匿名访问返回 200，仓库 public），取得可信数据。

---

## 二、20:00 归集链路核查：正常

### 各分支远程真实状态（API `/branches`）

| 分支 | 最新提交 | 提交时间 (UTC) | 相对 main |
|---|---|---|---|
| `main` | `6fbcd295d` Merge pull request #23 from wuqijin442/win | 2026-08-11 12:00:16Z | 基准 |
| `win` | `e8c50eef7` [2026-08-11] Daily AI Project Update | 2026-08-11 11:55:04Z | **领先 0** / 落后 39（status=`behind`） |
| `dgx` | `716664fe0` chore: 每日学习消化+图谱 2026-08-12 [dgx] | 2026-08-11 19:01:13Z | 领先 1 / 落后 46（`diverged`） |

### 归集 PR 记录（API `/pulls`）

| PR | 方向 | 合并时间 (UTC) | 北京时间 |
|---|---|---|---|
| #23 | win → main | 2026-08-11T12:00:16Z | **08-11 20:00:16** |
| #22 | dgx → main | 2026-08-11T12:00:10Z | **08-11 20:00:10** |
| #21 | win → main | 2026-08-10T12:00:16Z | 08-10 20:00:16 |
| #20 | dgx → main | 2026-08-10T12:00:09Z | 08-10 20:00:09 |
| #19 | win → main | 2026-08-09T12:00:20Z | 08-09 20:00:20 |
| #18 | dgx → main | 2026-08-09T12:00:09Z | 08-09 20:00:09 |

### 判定

1. **win 待归集为 0**：08-11 17:30 自动化产出的全部提交已进 main，逐条确认包含
   - `44fa593a4` [2026-08-11] Fix run_cmd hang（昨日修复的假死 bug 已归集）
   - `fef957457` / `e8c50eef7` [2026-08-11] Daily AI Project Update
2. **dgx 领先 1 条属正常**：`716664fe0` 产生于 2026-08-12 03:01（北京时间），在 20:00 归集之后，等今晚 20:00 归集即可。
3. **链路稳定**：PR #18~#23 连续三日均在 20:00:0x~20:00:2x 准点合并，无延迟、无失败。
4. **dgx 推送链路健康**：巡检标志 `Logs/PUSH_STUCK.flag` 不存在（该 flag 为 08-09 根治死循环时植入的告警位）。

---

## 三、待跟进 ② 为误判：归集任务与本机盘符无关

`src/merge_branches.sh` 证据：

- 第 19 行 cron 用法：`0 20 * * * cd ~/ai-project-weekly && GITHUB_TARGET_BRANCH=main bash src/merge_branches.sh`
- 第 24-26 行：`SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"` → `REPO_ROOT="$SCRIPT_DIR/.."` → `cd "$REPO_ROOT"`

归集运行在 **dgx 的 Linux 家目录 `~/ai-project-weekly`**（dgx 侧独立 clone），且路径由脚本自解析，因此 Windows 本机 D→E 迁移对其零影响。已在自动化 prompt 中补注该事实，避免后续再次误判。

---

## 四、待跟进 ① 已修复：cwds 指向 D 盘的风险

### 风险等级上升

| 项 | 08-11 认知 | 08-12 实测 |
|---|---|---|
| D 盘可写性 | 满盘/只读，写不进去 | **又可写了**（22G 可用，`D_WRITABLE=yes`） |
| D 盘树状态 | — | win 分支停在 `42fcb04`（08-10），落后 origin/win |
| 风险性质 | 写入失败（会报错，易发现） | **静默产生两棵树并行写同一 win 分支**（提交混乱，且 clones 会再次撑满 D） |

D 盘从"写不进"变成"能写但是旧树"，风险反而更隐蔽——这是必须立即修掉的原因。

### 已执行修复

1. `cwds`：`D:\Users\Administrator\Desktop\AI Project Weekly` → `E:/Users/Administrator/Desktop/AI Project Weekly`
2. prompt 顶部新增【运行环境覆盖指令 · 最高优先级】7 条，固化历史踩坑：
   - E 盘为唯一主工作树；严禁在 D 盘残留旧树执行
   - Python 必须用 `.workbuddy/binaries/python/versions/3.13.12/python.exe`（PATH 首位 python 已损坏，且 `python -V` 不可用作验证）
   - Git Bash 无 `tee`、`timeout` 不可用
   - 禁止用管道判定 git push/fetch 成败
   - 主站阻断时改走 `api.github.com` 复核，不得沿用本地旧引用出结论
   - 长任务须同轮次反复 block
3. 调度未变：`FREQ=DAILY;BYHOUR=17;BYMINUTE=30`，下次执行 2026-08-12 17:30。
4. 一致性复核：E 盘本地 `win` = `e8c50ee` 与 API `origin/win` = `e8c50eef7` 完全一致，工作树干净（`git status --porcelain` 为空）。

---

## 五、今日运行前提示

- **github.com 主站当前不可用**（连接 21s 超时），`api.github.com` 正常。若 17:30 时仍阻断：
  - 步骤1/2 依赖 `GH_FALLBACK=1` 走 `codeload.github.com` tarball 通道（08-11 实测 Clone 55/55）
  - 步骤3 的 `git fetch` 会退化为沿用本地旧引用，报告中的领先/落后数字将不可信，须按 prompt 第 6 条改走 API 复核并标注来源
- 本次核查所用 API 脚本已保留于 `.workbuddy/tmp/check_sync.py`（该目录已 gitignore），后续主站阻断时可直接复用。
