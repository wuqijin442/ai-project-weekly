---
title: 性能 MOC
type: MOC
tags:
  - moc
  - icss/性能
created: 2026-07-04
---

# 📂 性能 · MOC

> CSS 性能优化核心目标：减少重排（reflow）与重绘（repaint），让浏览器只做必要的渲染工作。性能优先使用 `transform`/`opacity` 触发 GPU 合成层，用 `contain`/`content-visibility` 隔离渲染范围，用 `will-change` 提前告知浏览器优化意图。

## 📋 笔记列表

### 渲染优化
- [[content-visibility]] - 长列表跳过屏幕外渲染，懒加载视觉内容
- [[contain-包含上下文]] - 隔离元素重排范围，限制浏览器重新计算区域
- [[will-change]] - 提示浏览器为即将发生的动画准备 GPU 层

### 硬件加速
- [[transform-硬件加速]] - 触发 GPU 合成层，让动画脱离主线程

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| 长列表卡顿 | `content-visibility: auto` + `contain-intrinsic-size` | [[content-visibility]] |
| 隔离组件重排 | `contain: layout paint` | [[contain-包含上下文]] |
| 动画前预热 | `will-change: transform`（动画后移除） | [[will-change]] |
| 动画掉帧 | `transform: translateZ(0)` 触发 GPU 层 | [[transform-硬件加速]] |
| 避免 layer explosion | 单元素只用 1 个 `will-change` 属性 | [[transform-硬件加速]] |

## 🎯 性能红线

| 红线 | 原因 | 替代方案 |
|------|------|----------|
| 动画 `width`/`height` | 触发重排 | `transform: scale()` |
| 动画 `top`/`left` | 触发重排 | `transform: translate()` |
| 滥用 `will-change` | 内存爆炸、layer explosion | 仅动画期间设置 |
| 长列表全量渲染 | 滚动卡顿 | `content-visibility: auto` |

## 🔗 关联分类
- [[00-MOC]]
- [[00-MOC-现代特性]]
- [[00-MOC-前沿特性]]
