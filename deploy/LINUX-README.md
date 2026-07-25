# 在 Linux 服务器上完整运行每日自动化

本仓库的自动化（`src/main.py` 多类别日报 + `src/board_workflow.py` 11 板块深潜）已做到**跨平台**：
路径用 `pathlib`、命令用列表式 `subprocess`、解释器自动探测 `python`/`python3`、推送优先用
`GITHUB_TOKEN` 注入的 HTTPS（不依赖 SSH key）。因此同一套脚本既能在本机跑，也能在 headless Linux 服务器上跑。

下面两种方式任选其一。

---

## 方式一：用 WorkBuddy 自动化（推荐，如果你在 Linux 上也用 WorkBuddy）

1. 在 Linux 服务器上安装并登录 WorkBuddy，克隆本仓库到某目录（例如 `/opt/aipw`）。
2. 在该目录里 `export GITHUB_TOKEN=ghp_xxx`（或在 WorkBuddy 的环境/凭据里配置）。
3. 把现有自动化 `automation-1784940038188` 的 **cwd** 改为 Linux 上的仓库绝对路径
   （如 `/opt/aipw`），调度时间保持 `FREQ=DAILY;BYHOUR=7;BYMINUTE=40`。
4. 自动化提示词已改写为「步骤1 + 步骤2 每日都跑」，并显式使用 `python3` / `GITHUB_TOKEN` / HTTPS 推送。

> 脚本本身是 **cwd 无关** 的（靠 `Path(__file__).resolve()` 定位仓库根），所以自动化把 cwd 指到仓库根即可。

---

## 方式二：纯 crontab（不需要 WorkBuddy，最稳）

### 1. 一键部署

```bash
# 在 Linux 服务器上
git clone --depth 1 https://github.com/wuqijin442/ai-project-weekly.git ~/ai-project-weekly
cd ~/ai-project-weekly
GITHUB_TOKEN=ghp_你的token  bash deploy/setup-linux.sh
```

`setup-linux.sh` 会：
- 安装 `git` / `python3` / `python3-pip`（按 apt/dnf/yum/apk/pacman 自动选）
- 以 **HTTPS** clone 仓库（避免 SSH key 问题）
- 把 `GITHUB_TOKEN` 写入仓库内 `.env`（权限 `600`，不回显）
- 写入 crontab：**每天 07:40** 自动运行 `src/run_daily.sh`

### 2. 手动验证（先跑一次确认环境 OK）

```bash
cd ~/ai-project-weekly
GITHUB_TOKEN=ghp_你的token  bash src/run_daily.sh
# 或分开跑：
python3 src/main.py
python3 src/board_workflow.py
```

### 3. 日志与排查

- 每日日志：`~/ai-project-weekly/Logs/cron-YYYY-MM-DD.log`
- cron 启动日志：`~/ai-project-weekly/Logs/cron-boot.log`
- 推送失败先看日志里 `⚠️ push 失败` —— 99% 是 `GITHUB_TOKEN` 没设或只读权限。
  token 必须是**有 `repo` 写权限**的 fine-grained 或 classic token（本仓库的 `wuqijin442` 账号）。

---

## 环境变量速查（可选覆盖默认值）

| 变量 | 默认 | 说明 |
|------|------|------|
| `GITHUB_TOKEN` | 空 | **必填**（headless 推送）。有 `repo` 写权限 |
| `INSTALL_TIMEOUT` | 300 | 单项目安装超时（秒） |
| `RUN_TIMEOUT` | 45 | 单项目冒烟超时（秒） |
| `BOARD_INSTALL_TIMEOUT` | 150 | 板块项目安装超时（秒） |
| `BOARD_RUN_TIMEOUT` | 40 | 板块项目冒烟超时（秒） |
| `BOARD_API_PACE` | 7 | 板块间间隔（秒），规避未认证 Search API 10次/分钟限速 |
| `CLONE_DEPTH` | 1 | clone 深度 |

---

## 注意事项

- **耗时**：步骤2（11 板块 × 5 = 55 项目）整体较长，受网络/安装速度影响，可能 30~90 分钟。
  步骤1（5~10 个项目）通常 10~20 分钟。两步骤串行，总计请预留 1~2 小时窗口。
- **磁盘**：clone 落 `clones/`（已被 .gitignore 忽略，但会占本地磁盘）；长期运行建议定期清理 `clones/`。
- **真实运行铁律**：所有结论基于真实 clone/安装/运行，失败如实记录，绝不编造数据。
- **网络**：服务器需能访问 `github.com`（HTTPS 443）。若走代理，在 cron 环境里也要 `export https_proxy=...`。
- **Python 包**：`python3 -m pip` 需要 `python3-pip`；若某些项目安装失败会被记为 failed 并继续，不影响整体。
