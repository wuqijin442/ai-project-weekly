---
title: 3D MOC
type: MOC
tags:
  - moc
  - icss/08-3D
created: 2026-07-04
---

# 📂 3D · MOC

> CSS 3D 三件套：`perspective`（景深）+ `transform-style: preserve-3d`（保持 3D 空间）+ `backface-visibility`（背面可见性）。配合 `translateZ`/`rotateX/Y` 构建立体效果。

## 📋 笔记列表

### 3D 基础
- [[perspective-透视]] - 景深属性与近大远小原理
- [[preserve-3d-3D空间]] - preserve-3d 嵌套与背面可见性

### 3D 应用
- [[3D翻转卡片]] - 经典翻转卡片与点击翻转
- [[3D立方体]] - 6 面立方体与自动旋转
- [[磨砂玻璃3D]] - 3D + backdrop-filter 景深虚化

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| 设置景深 | perspective: 1000px（父元素） | [[perspective-透视]] |
| 子元素保持 3D | transform-style: preserve-3d | [[preserve-3d-3D空间]] |
| 翻转卡片 | rotateY(180deg) + backface-visibility: hidden | [[3D翻转卡片]] |
| 立方体 | 6 面 + translateZ + rotateX/Y | [[3D立方体]] |
| 3D 毛玻璃 | backdrop-filter + translateZ | [[磨砂玻璃3D]] |

## 🔗 关联分类
- [[00-MOC-滤镜]] - backdrop-filter 基础
- [[00-MOC-动画]] - 3D 旋转动画
- [[00-MOC]]
