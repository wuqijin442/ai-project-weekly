---
title: 现代特性 MOC
type: MOC
tags:
  - moc
  - icss/现代特性
created: 2026-07-04
---

# 📂 现代特性 · MOC

> 现代 CSS 已有的、主流浏览器全支持或大部分支持的特性。这些特性大多已稳定 2-3 年，可在生产环境使用，但需要带降级方案兜底老浏览器。核心原则：能用 CSS 原生解决的不引入预处理工具或 JS。

## 📋 笔记列表

### 语法增强
- [[CSS嵌套]] - 原生嵌套语法、`&` 父选择器引用，告别 Sass
- [[scope-作用域]] - `@scope` 规则替代 BEM，限定样式作用边界

### 计算能力
- [[CSS三角函数]] - `sin()`/`cos()`/`tan()`，圆周运动无需 JS
- [[容器查询单位]] - `cqw`/`cqh` 等基于容器尺寸的单位

### 布局增强
- [[subgrid-子网格]] - 子网格继承父网格轨道，解决嵌套对齐难题

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| 父子选择器嵌套 | `& > .child` | [[CSS嵌套]] |
| 限定样式作用域 | `@scope (.card) to (.card-content)` | [[scope-作用域]] |
| 圆周运动动画 | `transform: rotate() translate() ` + `cos()`/`sin()` | [[CSS三角函数]] |
| 容器响应式字号 | `font-size: clamp(1rem, 5cqi, 3rem)` | [[容器查询单位]] |
| 嵌套网格对齐 | `grid-template-columns: subgrid` | [[subgrid-子网格]] |

## 🔗 关联分类
- [[00-MOC]]
- [[00-MOC-性能]]
- [[00-MOC-前沿特性]]
