# AI 开源项目日报自动化（Daily AI Project Update）

自动采集 GitHub Trending → 过滤 AI/LLM/Agent 项目 → 真实 Clone / 安装 / 冒烟运行 → 生成中文日报 → 同步到 `wuqijin442/main`。

> 所有结论均基于**真实运行结果**，不根据 README 推测。失败记录日志后继续，不中断、不编造。

## 工作流

1. `main.py` — 每日 TOP5 工作流（平日 TOP5 / 周日 TOP10）
   - 抓取 GitHub Trending（每日），按 AI 关键词过滤，排除 Awesome/Tutorial/Course/Demo/Fork
   - 对每个项目：真实 Clone → 检测构建系统 → 真实安装（pip/npm）→ 真实冒烟运行
   - 生成 `Daily-Reports/YYYY-MM-DD.md`（中文，真实数据）+ `Metadata/YYYY-MM-DD.json`
   - 本地 `git commit` 并 `_sync_to_github` 推 `main`
2. `board_workflow.py` — 11 板块 × TOP5 测试（待实现）

## 目录结构

```
main.py                每日工作流入口
Daily-Reports/         每日真实日报（Markdown）
Weekly-Reports/        周日周报
Monthly-Reports/       月末月报
Boards-Reports/        板块测试报告
Knowledge-Base/        知识库（≥90 分且安装运行成功项目）
Metadata/              每次运行的机器可读 JSON
Logs/                  运行日志
clones/                当日克隆的仓库（已 gitignore，不纳入同步）
cloned_projects/       历史落地的项目（已 gitignore）
```

## 运行

```bash
pip install -r requirements.txt   # 本脚本仅依赖 Python 标准库 + 系统 git
python main.py
```

环境变量：`GITHUB_TOKEN`（推送用）、`GITHUB_REPO`（默认 wuqijin442/ai-project-weekly）、
`INSTALL_TIMEOUT`（默认 200s）、`RUN_TIMEOUT`（默认 45s）、`CLONE_DEPTH`（默认 1）。

## 提交规范

- Commit：`[YYYY-MM-DD] Daily AI Project Update`
- 分支：`main`（不新建分支）
- 仅追加，不覆盖已有内容

## 最近一次运行（2026-07-25）

- 扫描 16 / AI 过滤 9 / Clone 成功 5 / 安装成功 2 / 运行成功 0 / 推荐 0
- 详见 [Daily-Reports/2026-07-25.md](Daily-Reports/2026-07-25.md)
- GitHub 同步状态：待仓库 `wuqijin442/ai-project-weekly` 创建并配置凭据后推送
