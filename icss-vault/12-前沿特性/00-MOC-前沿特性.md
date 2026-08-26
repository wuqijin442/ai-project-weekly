---
title: 前沿特性 MOC
type: MOC
tags:
  - moc
  - icss/前沿特性
created: 2026-07-04
---

# 📂 前沿特性 · MOC

> 仍在快速演进的 CSS 实验性/前沿特性。Chrome 已支持但 Firefox/Safari 多为实验性或不支持。生产环境必须带 `@supports` 降级方案，作为渐进增强使用。本分类是 iCSS 仓库最近 1-2 年的前沿实践精华。

## 📋 笔记列表

### 定位系统革命
- [[Anchor-Positioning-锚点定位]] - CSS 原生 Tooltip/Popover 跨容器定位（Chrome 125+）
- [[position-try-智能边界]] - 智能避让视口，替代 floating-ui（Chrome 125+）

### 动画系统增强
- [[animation-composition-动画合成]] - 多 transform 动画并存，碰撞反弹（Chrome 112+）
- [[路径动画×滚动驱动]] - offset-path 配合滚动进度驱动动画（Chrome 115+）
- [[View-Transitions-API]] - SPA 状态/跨页面过渡，原生过渡动画（Chrome 115+）

### 视觉特效
- [[Liquid-Glass-液态玻璃]] - 苹果风格毛玻璃，SVG 滤镜组合
- [[CSS-Houdini]] - Paint/Layout API、@property 注册、Typed OM

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| Tooltip 跟随按钮 | `anchor-name` + `position-anchor` + `anchor()` | [[Anchor-Positioning-锚点定位]] |
| Popover 超出视口翻转 | `@position-try` + `position-try-fallbacks` | [[position-try-智能边界]] |
| 多 transform 动画并存 | `animation-composition: accumulate` | [[animation-composition-动画合成]] |
| 滚动驱动路径动画 | `offset-path` + `animation-timeline: scroll()` | [[路径动画×滚动驱动]] |
| 页面切换过渡 | `view-transition-name` + `::view-transition-*` | [[View-Transitions-API]] |
| 苹果液态玻璃 | SVG `feTurbulence` + `feDisplacementMap` | [[Liquid-Glass-液态玻璃]] |
| 自定义绘制 | `CSS.paintWorklet.addModule()` | [[CSS-Houdini]] |

## ⚠️ 使用提示

> 前沿特性建议优先用于**渐进增强**场景：核心功能不依赖这些特性，仅作为体验升级。**必须**带 `@supports` 检测与降级方案。

```css
@supports (anchor-name: --test) {
  /* 现代浏览器：原生锚点定位 */
}
@supports not (anchor-name: --test) {
  /* 降级：JS 计算或 fixed 定位 */
}
```

## 🔗 关联分类
- [[00-MOC]]
- [[00-MOC-性能]]
- [[00-MOC-现代特性]]
