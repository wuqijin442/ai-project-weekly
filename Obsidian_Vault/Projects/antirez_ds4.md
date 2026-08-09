---
aliases: [ds4, DwarfStar, antirez/ds4]
tags: [AI, Trending, C, Inference-Engine, DeepSeek, Local-LLM, Metal, CUDA, ROCm]
stars: 21010
weekly_growth: 1254
created_at: 2026-05-06
status: 活跃（首入周榜 #9，Redis 作者 antirez 新作）
date_accessed: 2026-08-09
---

# antirez/ds4 · DwarfStar

**项目地址**：https://github.com/antirez/ds4
**作者**：antirez（Salvatore Sanfilippo，Redis 作者）
**⭐ 总 Star**：21,010（21.0k）
**📈 本周新增**：🔺1,254（全赛道周榜 #9）
**🍴 Fork**：1,884
**👁 Watch**：166
**💻 主要语言**：C
**📅 开源时间**：2026-05-06
**🔄 最近推送**：2026-08-05
**许可证**：MIT

## 项目定位

**DwarfStar** 是一个**小而原生的本地推理引擎**，首要优化目标是 **DeepSeek V4 Flash**，同时支持 **GLM 5.2**，在超大内存机器上还能跑 **DeepSeek V4 PRO**。

它把自己的边界划得很清楚：**这不是一个通用 GGUF runner**。模型加载、prompt 渲染、工具调用、KV 状态、HTTP 服务器、编码 Agent —— 这几块是**一起构建、一起测试**的，宁可窄也要稳。仓库里还附带 GGUF、imatrix、质量与速度评测的工具和数据。

模型支持策略是**刻意机会主义**的：只跟随「在有用的本地机器规模上最好的开放权重」，尤其是 128GB 笔记本与 512GB 工作站；**有更好的替代品出现时，旧模型会被移除**。

## 支持的后端

| 后端 | 目标硬件 | 说明 |
| --- | --- | --- |
| **Metal**（主要目标） | 96GB+ 的 Mac | 内存较小的机器可走 SSD 流式加载 |
| **NVIDIA CUDA** | 多 GPU 系统、**DGX Spark** | 支持多卡 |
| **ROCm** | Strix Halo（如 Framework Desktop） | AMD 路径 |

## 典型用法

- **消费级硬件跑大模型**：MacBook / DGX Spark / Strix Halo；内存不够时用 SSD 流式加载仍能保持可用速度
- **老卡复活成公司级 LLM 服务器**：CUDA 多 GPU + `ds4-server` 的解码/生成微批处理，可把已被 vLLM 放弃支持的 Ada Lovelace 架构老卡组成多用户服务。实测 **8×L40S**：聚合生成 **120 t/s**、prefill **2000 t/s**
- **双机张量并行**：两台 MacBook M5 Max / M3 Ultra 走 RDMA，跑 4bit DeepSeek Flash 或 GLM 5.2
- **流水线并行**：多台机器内存相加，跑更大的模型

## 技术栈

- **语言**：C（自包含，无重依赖）
- **基础**：站在 llama.cpp / GGML 的肩膀上（README 致谢章节明确说明）
- **形态**：推理引擎 + `ds4-server` HTTP 服务 + 内置编码 Agent

## 与 airllm 的分工

同期上榜的 [[lyogavin_airllm|airllm]]（#4）解决的是「**显存不够也要跑**」——分层推理 + 稀疏 MoE 专家流式加载；
ds4 解决的是「**高内存机器上跑得又快又稳**」——窄而深的原生引擎，全链路协同优化。
两者共同前提：开放权重模型已经装得进个人硬件。

## 外部链接

- GitHub：https://github.com/antirez/ds4

## 相关日期

- [[AI-Weekly-2026-08-09|2026-08-09 全赛道周报]]

## 备注

- 📌 **与本地基建直接相关**：README 明确点名 **DGX Spark** 属于 CUDA 后端支持范围，是手上有 DGX Spark 时值得优先实测的本地推理方案。
- antirez 时隔多年从 Redis 转向 LLM 推理引擎，本身即是信号：**本地推理正在从「能跑」进入「工程化打磨」阶段**。
