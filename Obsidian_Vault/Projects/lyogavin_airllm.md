---
aliases: [airllm, AirLLM, lyogavin/airllm]
tags: [AI, Trending, Python, Inference, Local-LLM, MoE, Memory-Optimization]
stars: 30244
weekly_growth: 5711
created_at: 2023-06-12
status: 活跃（全赛道周榜 #4，2023 年老项目本周复活）
date_accessed: 2026-08-09
---

# lyogavin/airllm

**项目地址**：https://github.com/lyogavin/airllm
**作者**：lyogavin（Gavin Li）
**⭐ 总 Star**：30,244（30.2k）
**📈 本周新增**：🔺5,711（全赛道周榜 #4）
**🍴 Fork**：3,215
**👁 Watch**：271
**💻 主要语言**：Jupyter Notebook / Python
**📅 开源时间**：2023-06-12
**🔄 最近推送**：2026-08-09
**许可证**：Apache-2.0

## 项目定位

**AirLLM 大幅降低推理显存占用，让 70B 大模型跑在单张 4GB 显卡上——不量化、不蒸馏、不剪枝。**

核心手段是**分层推理**（layered inference）：不把整个模型压进显存，而是按层调度，用时间换空间。因此模型精度不受损失，代价是吞吐降低。

## 极限案例

| 模型 | 参数量 | 所需显存 |
| --- | --- | --- |
| Llama 系 70B | 70B | **4GB** |
| Llama 3.1 | 405B | **8GB** |
| DeepSeek-V3 | 671B | **~12GB** |
| **Kimi K3**（目前最大开源模型） | **2.8T** | **< 4GB** |

Kimi K3 这一条尤其值得注意：它之所以能压到 4GB 以下，是因为**稀疏 MoE 模型可以一次只流式加载一个专家**，而不是加载整层。也就是说——**MoE 的稀疏性本身就是显存优化的杠杆**，模型越稀疏，分层推理的收益越大。

## 技术要点

- **分层推理**：逐层加载/释放，避免全模型驻留
- **MoE 专家流式加载**：稀疏模型按专家而非按层调度
- **无损**：不依赖量化 / 蒸馏 / 剪枝，输出与原模型一致
- **多平台**：支持 CUDA，亦有 MacOS 路径
- **分发**：PyPI 包 `airllm`，配有示例 Notebook

## 使用场景

- 单卡消费级 GPU（4GB / 8GB）上验证或推理超大开放权重模型
- 无法负担多卡集群时的**离线批处理**场景
- 教学 / 研究中需要跑原始精度大模型做对照实验

## 权衡说明

分层推理是**空间换时间**，吞吐显著低于全量驻留的推理引擎。它解决的是「**能不能跑**」，不是「**跑得快不快**」——追求速度应看同期上榜的 [[antirez_ds4|antirez/ds4]]（#9）。

## 外部链接

- GitHub：https://github.com/lyogavin/airllm
- PyPI：https://pypi.org/project/airllm/
- 作者博客：https://gavinliblog.com

## 相关日期

- [[AI-Weekly-2026-08-09|2026-08-09 全赛道周报]]

## 备注

- 2023-06 开源的老项目，本周 🔺5,711 冲进全赛道第 4。推测与 Kimi K3（2.8T）这类超大 MoE 模型发布后「普通人怎么跑」的需求集中爆发有关——最近推送日期就是 2026-08-09，作者在持续跟进新模型。
