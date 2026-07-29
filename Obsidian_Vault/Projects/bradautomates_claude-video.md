---
aliases: [claude-video, watch]
tags: [AI, Trending, Python, Claude, Multimodal, Vibe-Coding]
stars: 12453
created_at: 2026-04-24
today_growth: 988
status: 活跃（Claude 看视频技能，四度上榜）
date_accessed: 2026-07-29

# claude-video (/watch)

**项目地址**：https://github.com/bradautomates/claude-video
**作者**：bradautomates（Brad Bonanno）
**⭐ 总 Star**：12,453（12.5k）
**📈 今日新增**：988 stars（Vibe Coding #1）
**💻 主要语言**：Python
**当前版本**：0.2.0

## 项目定位

赋予 Claude 观看任何视频的能力。当用户粘贴视频 URL 或本地路径时，Claude 可以获取字幕、提取关键帧、转录音频，并基于看到的画面和听到的内容来回答问题。

## 核心功能

### 工作流程

1. 获取字幕（优先使用原生字幕，免费即时）
2. 下载所需内容（通过 yt-dlp）
3. 提取帧（场景感知或快速关键帧，通过 ffmpeg）
4. 拉取带时间戳的文字记录（无字幕时用 Whisper API 作为后备）
5. 将每一帧作为图像进行 Read（Claude 多模态能力）
6. 基于画面和音频回答用户问题

### 帧预算管理

| 视频时长 | 默认帧预算 |
|---------|----------|
| ≤30 秒 | ~30 帧 |
| 30秒-1分钟 | ~40 帧 |
| 1-3分钟 | ~60 帧 |
| 3-10分钟 | ~80 帧 |
| >10分钟 | 100 帧（稀疏扫描） |

### 四种详细模式

| 模式 | 帧数上限 | 提取时间 | 图像 tokens |
|------|---------|---------|-------------|
| `transcript` | 0 | ~4.5 秒 | 0（仅文本） |
| `efficient` | 50 | ~0.5 秒 | ~9.8k |
| `balanced`（默认） | 100 | ~20.9 秒 | ~19.7k |
| `token-burner` | 无上限 | ~21.0 秒 | ~22.8k |

## 使用场景

- **分析他人内容**：分析病毒视频的开场钩子、广告创意、竞争对手发布会
- **从视频诊断 Bug**：`/watch bug-repro.mov what's going wrong?`
- **总结视频**：快速拉取结构、关键时刻
- **将播放列表转为笔记**：把频道或课程变成可搜索的笔记集合

## 安装方式

```bash
# Claude Code（推荐）
/plugin marketplace add bradautomates/claude-video
/plugin install watch@claude-video

# 其他 50+ Agent Skills 主机
npx skills add bradautomates/claude-video -g
```

## 技术栈

- **视频下载**：yt-dlp（支持 YouTube、Loom、TikTok、X、Instagram 等）
- **帧提取**：ffmpeg
- **转录后端**：Groq Whisper（首选）、OpenAI Whisper（后备）
- **多模态读取**：Claude 的 Read 工具（图像直接在其上下文中渲染）
- **去重算法**：纯标准库 Python（16×16 灰度缩略图，平均绝对差值）

## 自带密钥

| 能力 | 所需条件 | 成本 |
|------|---------|------|
| 下载 + 原生字幕 | yt-dlp + ffmpeg | 免费 |
| Whisper 后备（首选） | Groq API key | 便宜、快速 |
| Whisper 后备（备选） | OpenAI API key | 标准定价 |

## 外部链接

- GitHub：https://github.com/bradautomates/claude-video
- 作者 YouTube：https://www.youtube.com/@bradbonanno
- Solaris Automation：https://www.solarisautomation.io/
- 许可证：MIT

## 相关日期

- [[Vibe-Coding-2026-07-08|2026-07-08 日报]]
- [[Vibe-Coding-2026-07-09|2026-07-09 日报]]
- [[Vibe-Coding-2026-07-28|2026-07-28 日报]]
- [[Vibe-Coding-2026-07-29|2026-07-29 日报]]

## 备注

- 测试：37/37 测试通过
- 支持 50+ Agent Skills 主机
- 协作者包括 Claude Opus 4.7 / 4.8（共同署名）
