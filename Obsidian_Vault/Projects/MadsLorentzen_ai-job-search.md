---
aliases: [ai-job-search]
tags: [AI, Trending, TypeScript, Claude-Code, Vibe-Coding]
stars: 36993
created_at: 2026-03-18
today_growth: 1300
status: 4度上榜
date_accessed: 2026-08-27
---

# ai-job-search

**项目地址**：https://github.com/MadsLorentzen/ai-job-search
**作者**：MadsLorentzen
**⭐ 总 Star**：18,947
**📈 今日新增**：3,716 stars
**💻 主要语言**：TypeScript (77.5%)、Python (13.0%)、TeX (9.5%)

## 项目定位

基于 Claude Code 构建的 AI 驱动求职申请框架。用户 Fork 仓库后填写个人资料，Claude 可自动完成职位评估、简历定制、求职信撰写和面试准备。核心工作流（自我画像、匹配评估、起草-审查申请管线）为语言和国家无关设计。

## 核心功能

### 主要命令

| 命令 | 功能 |
|------|------|
| `/setup` | 填写个人资料（支持读取文档/导入简历/问答访谈三种模式） |
| `/scrape` | 搜索多个求职门户，去重并按匹配度排序 |
| `/apply <url>` | 完整申请工作流：评估匹配度→起草简历+求职信→审查代理批评→修订→最终输出 |
| `/outcome` | 记录申请结果，归档提交材料 |
| `/rank` | 批量评分职位，生成排名候选清单 |
| `/upskill` | 分析技能差距，生成学习计划 |

### `/apply` 工作流亮点

1. **PDF 验证循环**：编译并视觉检查每个 PDF，自动修复布局问题
2. **ATS 验证**：提取 PDF 文本层，验证联系方式、阅读顺序和关键词覆盖
3. **起草-审查分离**：第二个 Claude 代理研究公司并批评草稿
4. **相关性加权简历裁剪**：按相关性评分裁剪内容

## 技术栈

- **AI 工具**：Claude Code (CLI) by Anthropic
- **运行时**：Bun（TypeScript CLI 工具）、Python 3.10+
- **文档编译**：LaTeX（lualatex + xelatex）、moderncv 模板
- **可选工具**：pdftotext（poppler）用于 ATS 文本层提取

## 安装前提

- Claude Code CLI
- Python 3.10+
- Bun
- LaTeX 发行版（TeX Live 或 MiKTeX）
- poppler（可选，用于 ATS 检查）

## 外部链接

- GitHub：https://github.com/MadsLorentzen/ai-job-search
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-07-08|2026-07-08 日报]]
- [[Vibe-Coding-2026-07-10|2026-07-10 日报]]

## 备注

- 项目为独立开源项目，不隶属于 Anthropic
- 求职门户搜索技能目前针对丹麦市场构建，但设计上可替换为本地求职板
- 最新提交：2026-07-09
- 2026-07-10 以 +3,716 当日新增登顶 Vibe Coding 日榜（总 Star 升至 18.9k）

## 反向链接
- [[Daily/Vibe-Coding-2026-08-26.md|2026-08-26 收录]]
- [[Daily/Vibe-Coding-2026-08-27.md|2026-08-27 收录]]
