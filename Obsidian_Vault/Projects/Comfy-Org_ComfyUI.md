---
aliases: [ComfyUI, Comfy-Org/ComfyUI, comfyanonymous/ComfyUI]
tags: [AI, Trending, Python, Diffusion, Image-Generation, Video-Generation, Node-Graph, Local-First]
stars: 125052
weekly_growth: 1778
created_at: 2023-01-17
status: 存量大盘（周榜 #8，生成式媒体基础设施）
date_accessed: 2026-08-09
---

# Comfy-Org/ComfyUI

**项目地址**：https://github.com/Comfy-Org/ComfyUI
**作者**：Comfy-Org（原 comfyanonymous 个人仓库，已转入组织）
**⭐ 总 Star**：125,052（125.1k）
**📈 本周新增**：🔺1,778（全赛道周榜 #8）
**🍴 Fork**：14,814
**👁 Watch**：770
**💻 主要语言**：Python
**📅 开源时间**：2023-01-17
**🔄 最近推送**：2026-08-09
**许可证**：GPL-3.0

## 项目定位

**最强大、最模块化的扩散模型 GUI / API / 后端**，核心是一张**可视化节点图**——不写代码就能搭建并复用图像、视频、音频、3D、文本工作流。

它早已不只是「Stable Diffusion 的界面」，而是**生成式媒体的本地工作流引擎**。

## 核心特性

- **节点图工作流**：可复用子图（subgraph）、工作流模板、App Mode、本地 API（便于嵌入自有应用）
- **高效本地执行**：异步队列、**局部图重执行**（只跑改动部分）、智能 VRAM/RAM 管理、模型卸载、量化模型支持
- **完全离线**：核心不主动下载任何东西；`--disable-api-nodes` 可关闭可选的付费 Comfy API 节点，强制全离线
- **工作流可移植**：存取为 JSON，甚至能**从生成的媒体文件里还原完整工作流与随机种子**
- **可扩展**：自定义节点生态 + `extra_model_paths.yaml` 配置额外模型目录

## 原生模型支持（节选）

| 类别 | 代表模型 |
| --- | --- |
| 图像生成 | SD 1.5 / SDXL / SD3.5、Flux.1 / Flux.2、Qwen Image、Z-Image、Hunyuan Image 2.1、HiDream、Lumina Image 2.0、Ideogram 4、Kandinsky 5 |
| 图像编辑 | Flux Kontext、Flux.2 Klein、Qwen Image Edit、HiDream E1.1/O1、OmniGen2 |
| 视频生成 | Wan 2.1/2.2、LTX-Video 2/2.3、HunyuanVideo 1.5、Kandinsky 5 Video、CogVideoX、Cosmos Predict2、Mochi |
| 音频 | ACE-Step 1.5、Stable Audio 3；音视频 MiniMax H3、LTX-AV |
| 3D 与视觉 | Hunyuan3D 2.1、TripoSplat、SeedVR2、SUPIR、Depth Anything 3、SAM 3/3.1、BiRefNet |
| 文本生成 | Gemma 3/4、Qwen3 / Qwen3.5 / Qwen3-VL（含多模态输入） |

同时支持加载完整 checkpoint 或分离的 diffusion model、VAE、text encoder、LoRA、ControlNet、adapter、upscaler。

## 内置工具

inpainting、outpainting、参考图条件控制、遮罩与合成、模型融合、超分、插帧、分割、深度估计、媒体处理。

## 安装方式

- Windows / Mac 桌面版
- Windows Portable 便携包
- `comfy-cli` 命令行
- Linux / Windows 手动安装
- ComfyUI-Manager（节点包管理）

## 外部链接

- GitHub：https://github.com/Comfy-Org/ComfyUI
- 官网：https://www.comfy.org/
- 工作流库：https://comfy.org/workflows/
- 文档：https://docs.comfy.org/

## 相关日期

- [[AI-Weekly-2026-08-09|2026-08-09 全赛道周报]]

## 备注

- 🔺1,778 对 12.5 万存量而言属正常波动，**不构成趋势信号**，本期作为生成式媒体基础设施的在场记录收录。
- 值得注意的产品判断：它把「完全离线」当作默认承诺（付费 API 节点可一键关闭），这在多数工具都在往云端靠的当下是个明确的差异化选择——对**素材不能出内网**的商用视频生产场景尤其重要。
