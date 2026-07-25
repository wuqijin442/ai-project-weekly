# AI 开源项目日报自动化（Daily AI Project Update）

自动采集 GitHub Trending → 过滤 AI/LLM/Agent 项目 → 真实 Clone / 安装 / 冒烟运行 → 生成中文日报 → 同步到 `wuqijin442/main`。

> 所有结论均基于**真实运行结果**，不根据 README 推测。失败记录日志后继续，不中断、不编造。

## 工作流

1. `src/main.py` — 每日 TOP5 工作流（平日 TOP5 / 周日 TOP10）
   - 抓取 GitHub Trending（每日），按 AI 关键词过滤，排除 Awesome/Tutorial/Course/Demo/Fork
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
python src/main.py                 # 每日 TOP5 工作流
python src/board_workflow.py       # 11 板块 × TOP5 测试（耗时较长）
```

环境变量：`GITHUB_TOKEN`（推送用）、`GITHUB_REPO`（默认 wuqijin442/ai-project-weekly）、
`INSTALL_TIMEOUT`（默认 200s）、`RUN_TIMEOUT`（默认 45s）、`CLONE_DEPTH`（默认 1）。

## 提交规范

- Commit：`[YYYY-MM-DD] Daily AI Project Update`
- 分支：`main`（不新建分支）
- 仅追加，不覆盖已有内容

## 最近一次运行（2026-07-25）

- 扫描 16 / AI 过滤 9 / Clone 成功 5 / 安装成功 2 / 运行成功 0 / 推荐 0
- 详见 [reports/daily/2026-07-25.md](reports/daily/2026-07-25.md)
- GitHub 同步状态：✅ 已推送到 [`wuqijin442/ai-project-weekly`](https://github.com/wuqijin442/ai-project-weekly) 的 `main` 分支（SSH 密钥认证）
