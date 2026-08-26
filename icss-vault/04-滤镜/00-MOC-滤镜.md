---
title: 滤镜 MOC
type: MOC
tags:
  - moc
  - icss/滤镜
created: 2026-07-04
---

# 📂 滤镜 · MOC

> CSS 滤镜是视觉特效的核心能力，涵盖 `filter`、`backdrop-filter`、混合模式与 SVG 滤镜。
> 核心原则：滤镜会触发 GPU 合成层，合理使用可加速，滥用则拖垮性能；动画仅用 `transform`/`opacity`，滤镜属性变化谨慎做动画。

## 📋 笔记列表

### 基础滤镜
- [[filter-滤镜组合]] - filter 多重滤镜组合与性能影响
- [[backdrop-filter-毛玻璃]] - 毛玻璃语法、与 filter 区别、暗色主题适配
- [[hue-rotate-色相旋转]] - 色相旋转动画、彩虹效果、暗黑模式适配

### 混合模式
- [[mix-blend-mode-混合模式]] - 16 种混合模式、头像融合、文字与图片融合

### SVG 滤镜
- [[SVG滤镜]] - feTurbulence 噪声、feDisplacementMap 位移、Liquid Glass 简版

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| 毛玻璃/磨砂效果 | `backdrop-filter: blur()` | [[backdrop-filter-毛玻璃]] |
| 图片去色变灰 | `filter: grayscale(1)` | [[filter-滤镜组合]] |
| 头像与背景融合 | `mix-blend-mode: multiply` | [[mix-blend-mode-混合模式]] |
| 彩虹流光动画 | `hue-rotate` + `conic-gradient` | [[hue-rotate-色相旋转]] |
| 液态玻璃扭曲 | SVG `feDisplacementMap` | [[SVG滤镜]] |
| 给不规则形状加阴影 | `filter: drop-shadow()` | [[不规则边框-drop-shadow]] |
| hover 图片增强 | `filter: brightness() contrast()` | [[filter-滤镜组合]] |

## ⚡ 性能红线

1. `filter`/`backdrop-filter` 会创建合成层，长列表慎用
2. 滤镜动画代价高，优先用 `transform` 替代
3. `backdrop-filter` 在低端机易掉帧，配合 `will-change` 谨慎使用
4. SVG 滤镜 `feTurbulence` 计算量大，避免大面积应用

## 🔗 关联分类
- [[00-MOC-边框]] - drop-shadow 与 clip-path 配合
- [[00-MOC-选择器]] - :has() 控制滤镜触发
- [[00-MOC]]
