# 历史项目页 created_at（开源时间）回填报告

- 执行日期：2026-07-13
- 范围：Obsidian_Vault/Projects/ 下全部 43 个项目详情页
- 数据源：GitHub REST API（`api.github.com/repos/{owner}/{repo}`，经 WebFetch 出口）
- 字段：在 Frontmatter 的 `stars:` 行后新增 `created_at: YYYY-MM-DD`
- 结果：成功 43 / 跳过 0 / 失败 0

## 按开源时间排序（升序）

| 开源时间 | 项目（owner/repo） | 文件名 | 备注 |
| --- | --- | --- | --- |
| 2021-06-19 | logto-io/logto | logto-io_logto | |
| 2023-04-29 | AntonOsika/gpt-engineer | AntonOsika_gpt-engineer | |
| 2023-04-29 | gpt-engineer-org/gpt-engineer | gpt-engineer-org_gpt-engineer | 重定向至 AntonOsika/gpt-engineer |
| 2023-05-09 | Aider-AI/aider | Aider-AI_aider | |
| 2023-05-09 | paul-gauthier/aider | paul-gauthier_aider | 重定向至 Aider-AI/aider |
| 2023-05-24 | continuedev/continue | continuedev_continue | |
| 2023-07-14 | openinterpreter/openinterpreter | openinterpreter_openinterpreter | |
| 2023-08-16 | topoteretes/cognee | topoteretes_cognee | |
| 2024-04-02 | SWE-agent/SWE-agent | SWE-agent_SWE-agent | |
| 2024-04-02 | princeton-nlp/SWE-agent | princeton-nlp_SWE-agent | 重定向至 SWE-agent/SWE-agent |
| 2024-07-06 | cline/cline | cline_cline | |
| 2024-10-31 | browser-use/browser-use | browser-use_browser-use | |
| 2024-12-04 | wonderwhy-er/DesktopCommanderMCP | wonderwhy-er_DesktopCommanderMCP | |
| 2025-05-03 | asgeirtj/system_prompts_leaks | asgeirtj_system_prompts_leaks | |
| 2025-07-04 | davila7/claude-code-templates | davila7_claude-code-templates | |
| 2025-08-05 | usestrix/strix | usestrix_strix | |
| 2025-10-09 | obra/superpowers | obra_superpowers | |
| 2025-10-13 | msitarzewski/agency-agents | msitarzewski_agency-agents | |
| 2025-10-19 | alirezarezvani/claude-skills | alirezarezvani_claude-skills | |
| 2025-11-16 | steipete/CodexBar | steipete_CodexBar | |
| 2026-01-03 | OthmanAdi/planning-with-files | OthmanAdi_planning-with-files | |
| 2026-01-07 | Dicklesworthstone/destructive_command_guard | Dicklesworthstone_destructive_command_guard | |
| 2026-01-18 | affaan-m/ECC | affaan-m_ECC | |
| 2026-01-23 | mvanhorn/last30days-skill | mvanhorn_last30days-skill | |
| 2026-02-03 | mattpocock/skills | mattpocock_skills | |
| 2026-02-13 | diegosouzapw/OmniRoute | diegosouzapw_OmniRoute | |
| 2026-02-15 | addyosmani/agent-skills | addyosmani_agent-skills | |
| 2026-02-24 | DeusData/codebase-memory-mcp | DeusData_codebase-memory-mcp | |
| 2026-03-13 | JCodesMore/ai-website-cloner-template | JCodesMore_ai-website-cloner-template | |
| 2026-03-15 | iOfficeAI/OfficeCLI | iOfficeAI_OfficeCLI | |
| 2026-03-17 | stablyai/orca | stablyai_orca | |
| 2026-03-18 | MadsLorentzen/ai-job-search | MadsLorentzen_ai-job-search | |
| 2026-03-27 | ogulcancelik/herdr | ogulcancelik_herdr | |
| 2026-03-29 | calesthio/OpenMontage | calesthio_OpenMontage | |
| 2026-03-31 | VoltAgent/awesome-design-md | VoltAgent_awesome-design-md | |
| 2026-04-07 | TencentCloud/TencentDB-Agent-Memory | TencentCloud_TencentDB-Agent-Memory | |
| 2026-04-07 | xbtlin/ai-berkshire | xbtlin_ai-berkshire | |
| 2026-04-10 | TencentCloud/CubeSandbox | TencentCloud_CubeSandbox | |
| 2026-04-12 | browser-use/video-use | browser-use_video-use | |
| 2026-04-24 | bradautomates/claude-video | bradautomates_claude-video | |
| 2026-04-27 | Nutlope/hallmark | Nutlope_hallmark | |
| 2026-04-10 | google-labs-code/design.md | google-labs-code_design | 真实仓库名带 .md 后缀（原查 design 少后缀致 404） |

## 说明
- 3 个仓库在 GitHub 上发生重定向（旧路径 → 新路径），已按重定向目标的创建时间写入：
  `gpt-engineer-org/*→AntonOsika/*`、`paul-gauthier/aider→Aider-AI/aider`、`princeton-nlp/SWE-agent→SWE-agent/SWE-agent`。
- ~~`google-labs-code/design` 当前 API 返回 404~~ **已更正（2026-07-13）**：真实仓库名为 `google-labs-code/design.md`（带 `.md` 后缀），原查询 `google-labs-code/design` 少了后缀才 404。已核实 `created_at = 2026-04-10`（API 权威值，与腾讯云报道「2026-04-10 首发」一致），项目页字段已补正。
- 此后每日自动化运行（若 GitHub API 可达）将在第二步直接抓取 `created_at` 与 `weekly_growth`，无需再回填。
