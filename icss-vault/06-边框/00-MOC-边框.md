---
title: 边框 MOC
type: MOC
tags:
  - moc
  - icss/边框
created: 2026-07-04
---

# 📂 边框 · MOC

> CSS 边框远不止 `border: 1px solid`。现代 CSS 用 `clip-path`、`conic-gradient`、`border-image`、`border-radius` 创造任意形状与渐变边框，配合 `drop-shadow` 为不规则形状加阴影。
> 核心原则：能 CSS 实现的不用图片；渐变边框优先用 `mask`+`gradient`；不规则形状阴影用 `drop-shadow` 而非 `box-shadow`。

## 📋 笔记列表

### 形状与裁剪
- [[clip-path-多边形]] - clip-path polygon/circle/ellipse、SVG path、动画
- [[圆角与形状.md|圆角与形状]] - border-radius 复杂语法、椭圆角、模拟形状

### 边框特效
- [[不规则边框-drop-shadow]] - drop-shadow 跟随 alpha 通道、为 clip-path 加阴影
- [[conic-gradient-边框]] - conic-gradient + mask 渐变边框、四色边框、动画边框
- [[border-image-边框图像]] - border-image 九宫格切片、应用场景

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| 三角形/梯形/任意多边形 | `clip-path: polygon()` | [[clip-path-多边形]] |
| 不规则形状加阴影 | `filter: drop-shadow()` | [[不规则边框-drop-shadow]] |
| 渐变边框 | `conic-gradient` + `mask` | [[conic-gradient-边框]] |
| 四色边框 | `conic-gradient` 四段 | [[conic-gradient-边框]] |
| 图片做边框 | `border-image-slice` | [[border-image-边框图像]] |
| 椭圆/不对称圆角 | `border-radius` 多值 | [[圆角与形状]] |
| 水滴/叶子形状 | `border-radius` 百分比 | [[圆角与形状]] |
| 形状变形动画 | `clip-path` 动画 | [[clip-path-多边形]] |

## ⚡ 使用红线

1. `clip-path` 动画需起止点数一致，否则无法插值
2. `drop-shadow` 性能不如 `box-shadow`，多重阴影慎用
3. `conic-gradient` + `mask` 做边框时，`mask-composite` 需 `-webkit-` 前缀兼容
4. `border-image` 不受 `border-radius` 影响，圆角需配合 `clip-path`
5. `border-radius` 百分比基于元素尺寸，响应式下可能变形

## 🔗 关联分类
- [[00-MOC-滤镜]] - drop-shadow 是 filter 家族
- [[00-MOC-选择器]] - :has() 联动边框样式
- [[00-MOC]]
