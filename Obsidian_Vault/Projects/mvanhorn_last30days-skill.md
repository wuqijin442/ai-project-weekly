---
aliases: [last30days, last30days-skill]
tags: [AI, Trending, Python, Agent-Skill, Research, Vibe-Coding]
stars: 55816
created_at: 2026-01-23
today_growth: 378
status: 活跃（AI Agent 研究/搜索技能，三度上榜 #3）
date_accessed: 2026-07-31

# /last30days

**项目地址**：https://github.com/mvanhorn/last30days-skill
**作者**：mvanhorn（Mike Van Horn）
**⭐ 总 Star**：55,816（55.8k）
**📈 今日新增**：378 stars（Vibe Coding #3）
**💻 主要语言**：Python
**形态**：Agent Skills（SKILL.md 规范）

## 项目定位

`/last30days` 是一个**由 AI Agent 主导的搜索引擎**——它按"点赞、喜欢、真实金钱（如预测市场赔率）"打分，而不是由编辑排序。它会并行检索 Reddit、X、YouTube、Hacker News、Polymarket 与整个网络上的任意主题，再由一个 AI Agent "裁判"综合提炼出有依据的总结。

核心理念：Google 聚合的是"编辑视角"，而 `/last30days` 搜索的是"真实的人"——每天有数百万人用注意力和钱包投票。它把这些分散在各平台围墙花园里的信号（Reddit 评论、X 帖子、YouTube 字幕、TikTok 互动、Polymarket 真实资金）并行拉取、按真实参与度打分、再综合成一份简报。

## 核心能力

- **跨平台并行检索**：Reddit、X、YouTube、Hacker News、Polymarket、TikTok、arXiv、Techmeme、GitHub 等
- **真实信号打分**：按点赞/喜欢/真实金钱（预测市场）加权，而非编辑权重
- **AI 裁判综合**：Agent 将多源信息提炼为一份有依据的简报
- **零配置启动**：Reddit / HN / Polymarket / GitHub 开箱即用；X、YouTube、TikTok、arXiv 等由设置向导 30 秒解锁

## 技术栈

- **语言**：Python
- **形态**：Agent Skills 规范（运行时以 `skills/last30days/SKILL.md` 为事实来源）
- **分发**：Claude Code（推荐，marketplace 自动更新）、Codex、Cursor、Copilot、Gemini CLI 等 50+ Agent Skills 主机
- **集成**：各平台 API（需自备 key），当前为 v3 管线

## 安装方式

```bash
# Claude Code（推荐）
/plugin marketplace add mvanhorn/last30days-skill
/plugin install last30days

# 其他 50+ Agent Skills 主机
npx skills add mvanhorn/last30days-skill -g
```

## 使用场景

- AI 编程代理的**实时研究/竞品情报**（"过去 30 天大家怎么评价 X"）
- 选题与趋势发现（Reddit/HN/Polymarket 信号聚合）
- 替代"编辑排序"搜索，获取真实人群观点

## 外部链接

- GitHub：https://github.com/mvanhorn/last30days-skill
- 许可证：详见仓库 LICENSE 文件

## 相关日期

- [[Vibe-Coding-2026-07-09|2026-07-09 日报]]
- [[Vibe-Coding-2026-07-28|2026-07-28 日报]]
- [[Vibe-Coding-2026-07-31|2026-07-31 日报]]

## 备注

- 曾登上 GitHub Trending "Repository of the Day" #1
- 强调"搜索人，而非编辑"——填补各 AI 平台因平台围墙而无法跨源检索的空白
