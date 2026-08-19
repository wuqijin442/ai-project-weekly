---
aliases: [video-use, browser-use/video-use]
tags: [AI, Trending, Python, Coding-Agent, Video, Skills, Vibe-Coding]
stars: 19595
created_at: 2026-04-12
today_growth: 320
status: 热门（二度上榜 #4，严格关键词命中 browser-use）
date_accessed: 2026-08-05
---

# video-use

**项目地址**：https://github.com/browser-use/video-use
**作者**：browser-use
**⭐ 总 Star**：19,595（19.6k）
**📈 今日新增**：🔺320 stars
**🍴 Fork**：2,423
**💻 主要语言**：Python
**📅 开源时间**：2026-04-12
**🔄 最近推送**：2026-07-01
**📜 许可证**：MIT

## 项目定位

**用编码 Agent 剪视频。100% 开源。**

把原始素材丢进一个文件夹，和 Claude Code 对话，拿回 `final.mp4`。没有预设、没有菜单——适用于口播、混剪、教程、旅拍、访谈等任意内容形态。

这是 browser-use 团队从「Agent 操作浏览器」延伸到「Agent 操作剪辑流水线」的一步：**能力载体仍是 shell + skill，只是把动作域从 DOM 换成了 ffmpeg**。

## 核心能力

| 能力 | 说明 |
|------|------|
| **去填充词** | 自动剪掉 `umm` / `uh` / 卡壳重来与镜头间死时间 |
| **自动调色** | 每段素材自动色彩分级（暖色电影感、中性锐利，或自定义 ffmpeg 链） |
| **音频防爆音** | 每个剪辑点加 30ms 淡入淡出 |
| **字幕烧录** | 默认 2 词大写分块，样式完全可定制 |
| **动画覆盖层** | 通过 HyperFrames / Remotion / Manim / PIL 生成，**每个动画一个并行子代理** |
| **渲染自评** | 在每个剪辑边界自评渲染结果，确认后才呈现给用户 |
| **会话记忆** | `project.md` 持久化，下周接着上次的进度继续 |

## 技术栈

- **语言**：Python
- **媒体处理**：ffmpeg
- **动画生成**：[HyperFrames](https://github.com/heygen-com/hyperframes)、[Remotion](https://www.remotion.dev/)、[Manim](https://www.manim.community/)、PIL
- **语音**：ElevenLabs API（需自备 key）
- **宿主 Agent**：Claude Code / Codex / Hermes / OpenClaw 等任意具备 shell 访问能力的 Agent
- **许可证**：MIT

## 安装方式

以「安装提示词」形式交给 Agent 自己完成（clone、依赖、ffmpeg、技能注册、API key）：

```text
Set up https://github.com/browser-use/video-use for me.

Read install.md first to install this repo, wire up ffmpeg, register the skill with
whichever agent you're running under, and set up the ElevenLabs API key — ask me to
paste it when you need it. Then read SKILL.md for daily usage, and always read
helpers/ because that's where the editing scripts live.
```

然后把 Agent 指向素材目录：

```bash
cd /path/to/your/videos
claude    # 或 codex / hermes
```

会话内一句 `edit these into a launch video`，它会盘点素材、提出剪辑策略、等你确认，最后在素材旁产出 `edit/final.mp4`。

## 使用场景

- 口播 / 教程 / 混剪的批量粗剪自动化，省掉时间线拖拽
- 需要动画覆盖层但不想手写 Remotion / Manim 的创作者
- 通过 Browser Use Box 在 VPS 或 Telegram 上做「常驻剪辑」

## 外部链接

- GitHub：https://github.com/browser-use/video-use
- Browser Use Cloud：https://cloud.browser-use.com/v4
- 许可证：MIT

## 相关日期

- [[AI-Weekly-2026-07-05|2026-07-05 周报]]（首次收录，⭐14.7k / 周增 4,174）
- [[Vibe-Coding-2026-08-05|2026-08-05 日报]]（二度上榜 #4，严格关键词命中 `browser-use`）

## 备注

- **成长曲线**：2026-07-05 ⭐14,685 → 2026-08-05 ⭐19,595（31 天 +33%）
- 最近推送停留在 2026-07-01，项目已趋于稳定，今日 +320 更多来自 Agent 生态外溢关注
- 「渲染后自评」与「并行子代理生成动画」是两个值得借鉴的 Agent 工程模式
