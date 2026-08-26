---
title: 渐变 MOC
type: MOC
tags:
  - moc
  - icss/03-渐变
created: 2026-07-04
---

# 📂 渐变 · MOC

> 收集 CSS 渐变核心技巧。核心原则：颜色统一用 CSS 变量管理，渐变文字必带 `-webkit-` 前缀，多层渐变叠加实现复杂背景图案。

## 📋 笔记列表

### 三大基础渐变
- [[linear-gradient-线性渐变]] - 角度/方向、多色、透明度、条纹
- [[radial-gradient-径向渐变]] - 圆形/椭圆、位置控制、光晕高光
- [[conic-gradient-锥形渐变]] - 饼图、锥形边框、配合 mask

### 重复渐变与图案
- [[repeating渐变条纹]] - 条纹背景、棋盘格、repeating 三兄弟
- [[渐变实现复杂背景]] - 多层叠加、网格、噪点、几何图案

### 文字渐变
- [[background-clip-文字渐变]] - background-clip: text、渐变文字、配合动画

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| 渐变文字 | `background-clip: text` + `-webkit-text-fill-color: transparent` | [[background-clip-文字渐变]] |
| 饼图 | `conic-gradient(var(--c1) 0 30%, var(--c2) 0 70%, var(--c3) 0)` | [[conic-gradient-锥形渐变]] |
| 条纹背景 | `repeating-linear-gradient(45deg, ...)` | [[repeating渐变条纹]] |
| 按钮高光 | `radial-gradient` 椭圆高光叠加 | [[radial-gradient-径向渐变]] |
| 网格背景 | 双层 `linear-gradient` 叠加 | [[渐变实现复杂背景]] |
| 锥形边框 | `conic-gradient` + `mask` 镂空中心 | [[conic-gradient-锥形渐变]] |
| 光晕效果 | `radial-gradient` 透明渐变 + blur | [[radial-gradient-径向渐变]] |
| 棋盘格 | 双 `repeating-conic-gradient` 错位 | [[repeating渐变条纹]] |

## 🔗 关联分类
- [[00-MOC]]
- [[00-MOC-动画]] - 渐变动画、conic-gradient loading
- [[00-MOC-边框]] - 渐变边框、border-image
- [[00-MOC-文字]] - 渐变文字、描边
