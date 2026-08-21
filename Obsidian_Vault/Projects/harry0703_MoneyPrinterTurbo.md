---
aliases: ["harry0703/MoneyPrinterTurbo"]
tags: [github, ai, vibe-coding, project]
stars: 110569
today_growth: 2304
created_at: 2024-03-11
status: 3度上榜 · 已本地全量测试(2026-08-20)
date_accessed: 2026-08-20
---

# harry0703/MoneyPrinterTurbo

## 定位
利用 AI 大模型和自动化工作流，根据主题或关键词一键生成高清短视频。Generate HD short videos from a topic or keyword with an automated AI workflow.

## 技术栈
- 主语言：Python
- Topics：ai-video-generator, content-creation, ffmpeg, instagram-reels, llm, python, short-video, subtitles, text-to-speech, tiktok, video-automation, video-workflow, workflow-automation, youtube-shorts
- License：MIT

## 外部链接
- GitHub：https://github.com/harry0703/MoneyPrinterTurbo
- Stars：⭐108.5k（今日 🔺2,304）

## 反向链接
- [[Daily/Vibe-Coding-2026-08-19.md|2026-08-19 收录]]

## 本地测试记录（2026-08-20）
- Clone：`clones/MoneyPrinterTurbo`（浅克隆 189 文件 / 335MB，main 分支，含 resource/ 素材 198MB）
- 依赖：venv `mpt`（Python 3.13.12 全 wheel 兼容，含 faster-whisper/ctranslate2/streamlit/moviepy），pip install 2.5min
- 官方测试套件（pytest）：**591 passed / 7 failed / 10 skipped**（4374 子测试，通过率 98.8%）；7 个失败全部环境性——Windows 环境变量 32767 字符上限（elevenlabs 测试）+ 套件顺序/资源竞争（单跑通过），非产品 bug
- API 验证（端口改 8890，因 8080 被本机其他服务占用）：/docs 200，12 条路由全挂载（videos/scripts/audio/subtitle/tasks/musics/video_materials/terms/social-metadata 等）
- WebUI 验证（streamlit :8891）：HTTP 200 + _stcore/health 200
- CLI 验证：`cli.py --help` 30+ 参数完整（subject/script/source/materials/aspect/concat/transition/voice/bgm/stop-at）
- 端到端生成需自备 LLM/素材 API key（Kimi/OpenAI/DeepSeek + Pexels/Pixabay），Edge TTS 免费无需 key
- 结论：可部署可用；注意默认端口 8080 与本机其他服务冲突，需改 config.toml

