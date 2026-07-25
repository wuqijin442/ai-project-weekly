# AI Project Weekly — 项目长期记忆

## 目录结构约定（2026-07-25 按职能重组）
- `src/` — 工作流脚本入口（`main.py`、`board_workflow.py`）
- `reports/{daily,weekly,monthly,boards}/` — 日报 / 周报 / 月报 / 板块测试报告
- `knowledge-base/{projects,awesome}/` — ≥90 分且运行通过的项目、Awesome 清单类整理
- `analysis/{reviews,benchmarks,architecture}/` — 项目评测、基准对比、架构分析
- `data/{metadata,screenshots}/` — 机器可读 JSON 结果、运行证据截图
- `logs/` — 运行日志（目前仍同步；如含敏感消息可额外加入 `.gitignore`）
- `cloned_projects/` / `clones/` — 本地克隆仓库，已 gitignore，不纳入 GitHub 同步

## 提交与同步约定
- Commit 格式：`[YYYY-MM-DD] Daily AI Project Update`
- 分支：`main`，不新建分支
- 仅追加，不覆盖已有内容
- 提交账号：`wuqijin442`
- GitHub 远程：当前 HTTPS 可用，SSH 亦可

## 工作流运行约定
- `main.py`：每日 GitHub Trending → 分类/过滤 → 真实 Clone / 安装 / 冒烟 → 中文日报
- `board_workflow.py`：多板块 × TOP5 真实测试（耗时长，建议手动或独立自动化触发）
- 所有结论必须基于真实运行结果；失败记录日志后继续，不根据 README 推测、不编造

## GitHub 同步排除
- 已排除：`cloned_projects/`、`clones/`、`node_modules/`、`.venv/`、`__pycache__/`、`dist/`、`build/`、`target/`、`.next/`、`.cache/`、`*.log`、`.env`、`.trae/`、`.codebuddy/`、`.uploads/`、`.workbuddy/tmp/`、`.workbuddy/automations/`、`Obsidian_Vault/`、`储能知识库/`、`video-pipeline-guide/`
- `.workbuddy/memory/` 已纳入同步（用户要求上传）

## 工作流运行约定（补充）
- `learn_link.py`：Ollama `deepseek-r1:32b`（dgx 本地 GB10）对当日 `data/metadata/YYYY-MM-DD.json`「学习+链接」→ 产出 `reports/learnings/YYYY-MM-DD.md` 并**按日期幂等**追加 `knowledge-base/learn_links/INDEX.md`；Ollama 不可用时跳过且不阻断主流程。
- `run_daily.sh` 四步：① main.py 采集+推送（含 pre_sync_pull）② board_workflow ③ learn_link（best-effort）④ 当日同步推送学习产物（git pull+add+commit+push，复用 `.env` 的 GITHUB_TOKEN 内联 HTTPS，3 次重试）。

## 每日自动化（dgx 03:00 主跑 + Windows 08:40 错峰）
- dgx crontab：`0 3 * * * cd ~/ai-project-weekly && bash src/run_daily.sh`（原 07:40，2026-07-25 改）。
- 推送鉴权：headless 服务器靠仓库根 `.env` 的 `GITHUB_TOKEN`（chmod 600，gitignored）内联 HTTPS URL；main.py 与 run_daily.sh 步骤4 共用。
- 多机防冲突：`pre_sync_pull`（main.py 开头先拉后推，TLS 抖动重试 3 次）+ run_daily.sh 步骤4 先 pull 再 push。
- 输出落地：日报 `reports/daily/`、板块 `reports/boards/`、学习消化 `reports/learnings/`、累积知识库 `knowledge-base/learn_links/INDEX.md`。
