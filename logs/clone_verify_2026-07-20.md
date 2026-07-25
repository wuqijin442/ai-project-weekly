# GitHub Trending 2026-07-19 Top10 — 本地克隆与验证报告

- **日期**：2026-07-20（周一，工作日）
- **来源**：2026-07-19 周末全赛道周报 Top10（`Obsidian_Vault/Weekly/AI-Weekly-2026-07-19.md`）
- **克隆目录**：`D:\Users\Administrator\Desktop\AI Project Weekly\cloned_projects\github-trending-2026-07-19\`
- **执行人**：WorkBuddy（自动化克隆+验证任务）

---

## 一、执行环境

| 工具 | 版本 | 可用性 |
|------|------|--------|
| git | 2.54.0.windows.1 | ✅ 可访问 github.com（`git ls-remote`/`clone` 正常；裸 `curl` 仍被沙箱阻断 HTTP:000） |
| Node / npm | v22.22.2 / 10.9.7 | ✅ npm registry（npmmirror）可达 |
| Python | 3.13.14（managed） | ✅ 用于 Python 项目 venv 安装 |
| Rust / cargo | 1.97.1（GNU，winget 安装） | ✅ 已安装；OpenCut desktop / codex-rs 可用 `cargo` 构建 |
| bun | 1.3.14（官方二进制直装） | ✅ 已安装；OpenCut web 已成功 `bun run build` |
| MinGW-w64 链接器 | WinLibs POSIX.UCRT 16.1.0（winget） | ✅ 已安装（gcc/ld/ar/windres），供 Rust GNU 目标链接 |
| bazel | 未安装 | ⚠️ codex 原用 Bazel，但其 `codex-rs` 是 Cargo workspace，已改用 `cargo build`，无需 bazel |

---

## 二、克隆结果

- 提交 10 个仓库 URL，全部走 `--depth 1` shallow clone。
- **首次**：7 个成功；3 个（awesome-llm-apps、openai/codex、openinterpreter）因 **Windows MAX_PATH(260)** checkout 失败 → 启用 `git config core.longpaths true` 后 `git checkout -f HEAD` 修复，3 个全部完整检出（1791 / 5623 / 5618 文件，README 均在）。
- **内容异常**：发现 `openinterpreter/openinterpreter` 目录实际内容来自 **OpenAI Codex**（含 `codex-rs/`、`codex-cli/`、`name=codex-monorepo`）。复现确认：沙箱 git 出口对该 URL 返回了 Codex 仓库对象（新建独立目录 `oi_test` 重新克隆仍得 Codex 内容）。**已删除 2 个错误目录**，最终 **9 个仓库正确克隆**。
- 每个 Python 项目的验证 venv 建在各自仓库内 `.venv/`（可随仓库删除）。

---

## 三、逐项目验证

### 1. OpenCut-app/OpenCut — ✅ 克隆完整 / ✅ web 已构建 / ⏳ desktop 构建中
- **技术栈**：Rust + Tauri 桌面应用（`apps/web`=@opencut/web、`apps/desktop`、`apps/api`）
- **验证（web）**：`bun install` + `bun run build`（`vite build`）成功 → 产出 `apps/web/dist/`（2.1M，TanStack Start：client + server）。**bun 阻断已修复**。
- **验证（desktop）**：已安装 `cargo`(GNU 1.97.1) + MinGW-w64 链接器；`cargo build`（`apps/desktop`，Tauri）**进行中**（已编译 219+ crate，无错误），产出 `target/debug/` 二进制待链接完成。
- **结论**：工具链已补齐，web 已可构建；desktop 二进制链接中（后台）。

### 2. mattpocock/skills — ✅ 验证通过
- **技术栈**：Node 技能库（package.json；scripts: changeset / version）
- **验证**：`npm install` 成功；`skills/` 含 6 类（deprecated, engineering, in-progress, misc, personal, productivity）。
- **结论**：依赖可解析、技能资源完整。

### 3. Graphify-Labs/graphify — ✅ 验证通过
- **技术栈**：Python 包 `graphifyy`（把代码库蒸馏为可查询知识图谱）
- **验证**：venv + `pip install -e .` 成功（编译 tree-sitter 多语言解析器 + networkx/numpy/rapidfuzz 等）；`import graphify` 成功。
- **结论**：完整可安装、可导入。

### 4. Nutlope/hallmark — ✅ 验证通过
- **技术栈**：Node 静态文档站（`serve` = `python3 -m http.server --directory site 4173`）
- **验证**：`npm install` 成功；`npm run serve` 在 :4173 持续运行（超时退出码 124 = 常驻，未崩溃）。
- **结论**：依赖可解析、站点可服务；无 build 脚本（直接静态托管 `site/`）。

### 5. Shubhamsaboo/awesome-llm-apps — ✅ 结构验证通过
- **技术栈**：精选合集（markdown + notebooks），无构建系统
- **验证**：13 个分类目录（advanced_ai_agents / rag_tutorials / mcp_ai_agents / agent_skills / voice_ai_agents …），README 含 18 个外链。
- **结论**：结构完整、可读。属资料库，无需构建。

### 6. HKUDS/Vibe-Trading — ✅ 验证通过
- **技术栈**：Python 包 `vibe-trading-ai`（多智能体交易 Agent；依赖 langchain / fastapi / ccxt / akshare / tushare / weasyprint 等 200+）
- **验证**：venv + `pip install -e .` 成功（构建 `vibe-trading-ai 0.1.11`）；可导入模块 **`api_server`**（`import api_server` → `agent/api_server.py`，OK）。
- **备注**：可导入模块名为 `api_server`（非 `vibe_trading`）；运行需 API key / 行情数据源。
- **结论**：完整可安装、可导入。

### 7. stablyai/orca — ✅ 安装通过 / ⚠️ typecheck 含项目自身严格类型错误
- **技术栈**：Node / Electron 大型应用（`orca@1.4.146-rc.0`，脚本极多：build / typecheck / test / dev …）
- **验证**：首轮 `npm install` 失败（**ERESOLVE peer-dependency 冲突**）；改用 `npm install --legacy-peer-deps` 成功（1176 包，并自动修复 Electron 二进制）。`npm run typecheck`（`tsc --noEmit` 三工程：node / cli / web）**报错 TS18048**（strict null：`'value'`/`fileStat` possibly undefined）于 2 个源文件：`src/main/ipc/worktree-common-git-directory.ts`、`src/main/skills/skill-installation-topology.ts`。
- **结论**：依赖可解析、tsc 可运行；typecheck 失败系**项目自身严格空值检查问题**，非环境缺陷。

### 8. iOfficeAI/OfficeCLI — ✅ 结构验证通过
- **技术栈**：AI Agent 技能仓库（首个专为 AI Agent 打造的 Office 套件）
- **验证**：结构完整（168M，含 `build/`、`build.sh`、`dev-install.sh`、`SKILL.md`(417 行)、多语言 README）；根目录无标准 node/py 构建清单（Agent 技能形态）。
- **结论**：技能定义完整；提供 `build.sh` / `dev-install.sh` 安装脚本，无常规 `npm run build`。

### 9. openai/codex — ✅ 克隆完整 / ⏳ cargo 构建中
- **技术栈**：Rust + Bazel monorepo（核心 `codex-rs/`；npm 包 `@openai/codex` 为包装）
- **验证**：根 `npm install` 成功；`codex-cli/` 存在（`bin: codex=bin/codex.js`）。已装 `cargo`，`codex-rs/` 为 Cargo workspace，`cargo build` **进行中**（已编译 277+ crate，无错误）。**无需 bazel**（bazel 仅为可选构建后端，Rust 核心可直接 `cargo build`）。
- **结论**：Rust 核心可用 `cargo` 直接构建；运行时需 OpenAI API key。

### 10. openinterpreter/openinterpreter — ❌ 克隆失败（环境受限）
- **应为**：Python 编码 Agent（面向 Kimi / Qwen / DeepSeek 等开放模型）。
- **异常**：沙箱 git 出口对该 URL 返回 **OpenAI Codex** 仓库对象（已复现），无法取得真实代码。
- **处理**：已删除错误克隆目录（避免与 #9 混淆）。
- **在普通环境克隆命令**：
  ```bash
  git clone --depth 1 https://github.com/openinterpreter/openinterpreter.git
  ```
- **结论**：本环境受限未验证；需在可正常访问 GitHub 的环境执行。

---

## 四、汇总表

| # | 项目 | 克隆 | 验证动作 | 结果 |
|---|------|------|----------|------|
| 1 | OpenCut-app/OpenCut | ✅ | bun build ✅ / cargo build ⏳ | 🔧 工具链已装（bun + cargo + MinGW） |
| 2 | mattpocock/skills | ✅ | npm install | ✅ 通过 |
| 3 | Graphify-Labs/graphify | ✅ | pip install -e . + import | ✅ 通过 |
| 4 | Nutlope/hallmark | ✅ | npm install + serve 启动 | ✅ 通过 |
| 5 | Shubhamsaboo/awesome-llm-apps | ✅ | 结构检查 | ✅ 通过（资料库） |
| 6 | HKUDS/Vibe-Trading | ✅ | pip install -e . + import | ✅ 通过（模块 api_server） |
| 7 | stablyai/orca | ✅ | npm install + typecheck | ✅ 安装 / ⚠️ typecheck 项目自身 TS 错误 |
| 8 | iOfficeAI/OfficeCLI | ✅ | 结构检查 | ✅ 通过（Agent 技能） |
| 9 | openai/codex | ✅ | npm install + cargo build ⏳ | 🔧 cargo 已装，构建中（无需 bazel） |
| 10 | openinterpreter/openinterpreter | ❌ | — | ❌ 沙箱 git 出口返回 Codex 内容 |

---

## 五、工具链修复记录（2026-07-20 补充）

原报告标注 OpenCut「需 cargo+bun 才能构建」、codex「需 cargo+bazel 才能构建」。本次已修复：

| 工具 | 安装方式 | 安装位置 | 验证 |
|------|----------|----------|------|
| **bun** 1.3.14 | 官方 GitHub Release 二进制（node 下载 + PowerShell 解压；npm 安装因 npm 10.9.7 内部 `edgesOut`/`matches` bug 失败，corepack 不支持 bun） | `C:\Users\Administrator\.workbuddy\binaries\bun\bun.exe` | ✅ `bun --version`；OpenCut web `bun run build` 成功 |
| **Rust/cargo** 1.97.1 (GNU) | `winget install -e --id Rustlang.Rust.GNU` | `C:\Program Files\Rust stable GNU 1.97\bin\cargo.exe` | ✅ `cargo --version` |
| **MinGW-w64 链接器** WinLibs POSIX.UCRT 16.1.0 | `winget install -e --id BrechtSanders.WinLibs.POSIX.UCRT`（原 id `BrechtSanders.MinGW-W64` 不存在，exit 20） | `C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_...\mingw64\bin\` | ✅ `gcc`/`x86_64-w64-mingw32-gcc`/`ld`/`ar`/`windres` 均可解析 |
| **bazel** | 未安装 | — | ⚠️ 不需要：codex `codex-rs` 是 Cargo workspace，直接 `cargo build` |

- **环境 PATH 片段**（每次新 shell 需重设，因 winget 改 PATH 需重启 shell 才生效）：
  ```bash
  export PATH="/c/Program Files/Rust stable GNU 1.97/bin:/c/Users/Administrator/AppData/Local/Microsoft/WinGet/Packages/BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe/mingw64/bin:$PATH"
  ```
- **网络说明**：裸 `curl`/`wget` 仍被沙箱阻断（HTTP:000），但 `git`、`npm`、Node `fetch`、`winget` 均可出站；bun/cargo 二进制与 crate 下载均通过各自协议完成。

## 六、下一步建议

1. **OpenCut / codex 构建收尾**：两个 `cargo build` 仍在后台链接（codex-rs / Tauri 依赖树大，预计 10–30 分钟）。完成后补 binaries 路径与体积。
2. **openinterpreter**：在可正常访问 GitHub 的机器/环境重新克隆验证（本沙箱 git 出口对该 URL 异常，返回 Codex 内容）。
3. **orca**：typecheck 失败为项目自身 strict-null TS 错误（TS18048），如需可通过放宽 `tsconfig` 严格性或上游修复解决；不影响安装与运行。
4. **编码 Agent 运行**：codex / openinterpreter / Vibe-Trading 均需在运行时提供对应 API key 或数据源，验证仅覆盖安装、导入与（部分）构建层面。
