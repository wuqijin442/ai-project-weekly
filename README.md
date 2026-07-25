# AI 开源项目日报自动化（Daily AI Project Update）

自动采集 GitHub Trending → 按多维度类别（AI/LLM/Agent、前端/Web、后端/DevOps、数据库、开发工具、安全、移动、数据/ML）过滤 → 真实 Clone / 安装 / 冒烟运行 → 生成中文日报 → 同步到 `wuqijin442/main`。

> 所有结论均基于**真实运行结果**，不根据 README 推测。失败记录日志后继续，不中断、不编造。

## 工作流

1. `src/main.py` — 每日 TOP5 工作流（平日 TOP5 / 周日 TOP10）
   - 抓取 GitHub Trending（每日），按 8 大类别多维过滤（AI/LLM/Agent、前端/Web、后端/DevOps、数据库、开发工具、安全、移动、数据/ML），排除 Awesome/Tutorial/Course/Demo/Fork，按类别轮询选 TOP5 保证多样性
   - 对每个项目：真实 Clone → 检测构建系统 → 真实安装（pip/npm）→ 真实冒烟运行
   - 生成 `reports/daily/YYYY-MM-DD.md`（中文，真实数据）+ `data/metadata/YYYY-MM-DD.json`
   - 本地 `git commit` 并 `_sync_to_github` 推 `main`
2. `src/board_workflow.py` — 11 板块 × TOP5 测试（已实现）
   - 11 个板块（GitHub topic）：大语言模型 / AI / RAG / 扩散模型 / 计算机视觉 / 语音识别 / 机器人 / MLOps / 向量数据库 / 提示工程 / 微调
   - 通过 GitHub Search API（无需 token，按 star 降序）真实抓取每板块 TOP5
   - 对每个项目：真实 Clone → 检测构建 → 真实安装 → 真实冒烟（复用 main.py 的同款真实运行函数）
   - 生成 `reports/boards/YYYY-MM-DD-boards.md` + `data/metadata/YYYY-MM-DD-boards.json`
   - 注意：11×5=55 个项目，整体耗时较长；已做未认证 Search API 限速规避（板间间隔 + 403 退避重试）

## 目录结构（已按职能重组）

```
src/
  main.py              每日工作流入口（仅标准库 + 系统 git）
  board_workflow.py    11 板块 × TOP5 测试入口（复用 main.py 真实运行函数）
  run_daily.sh         每日编排：先跑 main 再跑 board_workflow（cron / systemd 友好）
deploy/
  setup-linux.sh       Linux 一键部署（装依赖 + HTTPS clone + 配置 token + 写 crontab）
  LINUX-README.md      Linux 服务器运行完整说明
reports/
  daily/               每日真实日报（Markdown）
  weekly/              周日周报
  monthly/             月末月报
  boards/              板块测试报告
knowledge-base/
  projects/            知识库（≥90 分且安装运行成功项目）
  awesome/             Awesome 清单类整理
analysis/
  reviews/             项目评测
  benchmarks/          基准对比
  architecture/       架构分析
data/
  metadata/            每次运行的机器可读 JSON
  screenshots/         截图 / 运行证据
logs/                  运行日志
clones/                当日克隆的仓库（gitignore，不纳入同步）
cloned_projects/       历史落地的项目（gitignore）
```

## 运行

```bash
pip install -r requirements.txt   # 本脚本仅依赖 Python 标准库 + 系统 git
python src/main.py                 # 每日 TOP5 工作流（Linux 上用 python3）
python src/board_workflow.py       # 11 板块 × TOP5 测试（耗时较长）
bash src/run_daily.sh              # 一键跑完上面两步（推荐用于 crontab / 自动化）
```

环境变量：`GITHUB_TOKEN`（**推送必填**，有 `repo` 写权限的 token，优先用其注入 HTTPS 推送）、`GITHUB_REPO`（默认 wuqijin442/ai-project-weekly）、
`INSTALL_TIMEOUT`（默认 200s）、`RUN_TIMEOUT`（默认 45s）、`CLONE_DEPTH`（默认 1）、
`BOARD_INSTALL_TIMEOUT`（默认 120s）、`BOARD_RUN_TIMEOUT`（默认 40s）、`BOARD_API_PACE`（默认 7s，板间间隔）、`BOARD_MIN_STARS`（默认 50）。

> 脚本自动探测 `python` / `python3`，Windows / Linux / macOS 通用；推送优先走 `GITHUB_TOKEN` 注入的 HTTPS，**不依赖 SSH key**。

## Linux 服务器部署

在 headless Linux 服务器上完整跑每日自动化（两步骤每日都跑），推荐直接用 crontab：

```bash
git clone --depth 1 https://github.com/wuqijin442/ai-project-weekly.git ~/ai-project-weekly
cd ~/ai-project-weekly
GITHUB_TOKEN=ghp_你的token  bash deploy/setup-linux.sh   # 装依赖 + HTTPS clone + 写 .env + 每日 07:40 crontab
```

详见 [`deploy/LINUX-README.md`](deploy/LINUX-README.md)。前提：服务器可访问 `github.com`（HTTPS 443），且 `GITHUB_TOKEN` 有本仓库写权限。

## 提交规范

- Commit：`[YYYY-MM-DD] Daily AI Project Update`
- 分支：`main`（不新建分支）
- 仅追加，不覆盖已有内容

## 最近一次验证（2026-07-25 多类别改造）

- 多类别 dry-run：扫描 16 / 多类别过滤 11（覆盖 6 类：AI/LLM/Agent、Frontend/Web、Backend/DevOps 等）/ TOP5 跨类别多样
- 分类逻辑已从「纯 AI 关键词」扩展为「8 大类别多维过滤」，覆盖更广的 GitHub 每日热门
- 完整每日真实运行（Clone/安装/冒烟）由自动化任务执行，输出见 `reports/daily/YYYY-MM-DD.md`
- GitHub 同步状态：✅ 推送到 [`wuqijin442/ai-project-weekly`](https://github.com/wuqijin442/ai-project-weekly) 的 `main` 分支（HTTPS + GITHUB_TOKEN 认证）
