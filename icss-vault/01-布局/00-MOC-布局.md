---
title: 布局 MOC
type: MOC
tags:
  - moc
  - icss/01-布局
created: 2026-07-04
---

# 📂 布局 · MOC

> 收集 CSS 布局核心技巧，从经典 Flex/Grid 到现代容器查询、锚点定位。核心原则：原生优先、用 gap 替代 margin、Flex 文本溢出必加 `min-width: 0`。

## 📋 笔记列表

### Flex 布局
- [[Flex-对齐与分布]] - justify-content/align-items/gap/min-width:0 文本溢出
- [[等高布局方案]] - Flex/Grid 天然等高、table-cell、padding+margin 负值 hack

### Grid 布局
- [[Grid-二维布局]] - grid-template/repeat/auto-fit/minmax/subgrid
- [[圣杯布局]] - 经典圣杯/双飞翼/现代 Grid 实现

### 定位与粘性
- [[Sticky-粘性定位]] - position: sticky 原理、吸顶导航
- [[锚点定位-Anchor-Positioning]] - 跨容器定位（简版，详细在 12-前沿特性）

### 响应式与移动端
- [[容器查询-@container]] - 组件级响应式、cqi/cqw 单位
- [[1px-边框问题]] - 移动端 1px、transform: scale(0.5) 方案

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| 水平垂直居中 | Flex `justify-content:center; align-items:center` | [[Flex-对齐与分布]] |
| 等分多列 | Grid `repeat(auto-fit, minmax(200px, 1fr))` | [[Grid-二维布局]] |
| 吸顶导航 | `position: sticky; top: 0` | [[Sticky-粘性定位]] |
| 组件响应式 | `@container` + `cqw/cqi` 单位 | [[容器查询-@container]] |
| 移动端 1px | `transform: scale(0.5)` + 伪元素 | [[1px-边框问题]] |
| 三栏自适应 | Grid `grid-template-columns: auto 1fr auto` | [[圣杯布局]] |
| 等高列 | Flex 天然等高（默认 `align-items: stretch`） | [[等高布局方案]] |
| Tooltip 跨容器定位 | `anchor-name` + `anchor()` | [[锚点定位-Anchor-Positioning]] |

## 🔗 关联分类
- [[00-MOC]]
- [[00-MOC-动画]] - 布局过渡动画
- [[00-MOC-现代特性]] - 容器查询单位、subgrid
- [[00-MOC-前沿特性]] - Anchor Positioning 详细实现
