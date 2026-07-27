---
aliases: [text-to-cad]
tags: [AI, Trending, JavaScript, Agent-Skills, CAD, Robotics, Hardware-Design, Vibe-Coding]
stars: 9970
created_at: 2026-04-22
today_growth: 230
status: 新兴（技能外溢至工程制造）
date_accessed: 2026-07-24

# text-to-cad

**项目地址**：https://github.com/earthtojake/text-to-cad
**作者**：earthtojake
**⭐ 总 Star**：9,970（10.0k）
**📈 今日新增**：230 stars（Vibe Coding #4）
**💻 主要语言**：JavaScript
**🗓 开源时间**：2026-04-22

## 项目定位

面向 **CAD / 机器人 / 硬件设计** 的 **Agent 技能库**。把生成、检查、寻源、切片及交接 CAD 与机器人描述文件（STEP / STL / 3MF / URDF / SDF / SRDF 等）封装为聚焦的技能工作流，让 AI Agent 直接从本地项目文件产出可制造的工程工件。一句话：把「技能（Skill）」范式从软件编码外溢到机械 / 硬件设计，让 Agent 既能写代码也能造零件。

## 技术栈

- **形态**：Agent Skills 库（每个技能以 `SKILL.md` 组织，含 requirements.txt / 依赖）
- **覆盖工件**：CAD（STEP/STL/3MF/DXF）、机器人描述（URDF/SRDF）、仿真（SDF）、格式转换与本地审查
- **底层引擎**：build123d / OpenCASCADE（几何内核）
- **运行依赖**：Python 3.11+（技能侧）；仓库主语言 JavaScript（上层封装 / 站点）
- **Topics**：agents, ai-agents, cad, robotics, build123d, opencascade, mechanical-engineering
- **许可**：MIT｜官网：https://www.cadskills.xyz｜文档：https://www.cadskills.xyz

## 外部链接

- GitHub：https://github.com/earthtojake/text-to-cad
- 作者：https://github.com/earthtojake
- 官网 / 文档：https://www.cadskills.xyz
- 在线 Demo：https://demo.cadskills.xyz

## 相关日期

- [[Vibe-Coding-2026-07-24|2026-07-24 日报]]

## 备注

- 由 GitHub Trending 日榜自动归档（Vibe Coding 生态扩充命中：以「agent skills」范式服务 CAD / 机器人 / 硬件设计，属「技能层」外延）。2026-07-24 首入 Vibe Coding 榜单居 #4（+230，10.0k），标志「技能」从软件编码向工程制造外溢——与 awesome-claude-skills（软件技能清单）形成技能层上下游呼应。
