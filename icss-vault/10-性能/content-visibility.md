---
title: content-visibility 跳过屏幕外渲染
type: technique
tags:
  - icss/性能/渲染优化
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[contain-包含上下文]]"
  - "[[will-change]]"
  - "[[transform-硬件加速]]"
---

# content-visibility 跳过屏幕外渲染

## 问题/场景
长列表（千行数据、表格、卡片瀑布流）滚动时严重卡顿。原因是浏览器把所有屏幕外的元素都渲染了，但这些用户根本看不到。我们希望浏览器只渲染可视区域内的内容，离开视口的元素直接跳过渲染。

## 核心原理
`content-visibility: auto` 告诉浏览器：「这个元素的内容如果不在视口内，就跳过它的渲染（layout、paint、style 都跳过）」。浏览器只对进入视口的元素执行渲染工作。

但跳过渲染有个副作用：浏览器不知道元素多大，会把它当作 0 高度处理，导致滚动条计算错误、页面跳动。解决方法是 `contain-intrinsic-size` 给一个预估占位尺寸，让浏览器在屏幕外也能预留空间。

## 实现方案

```css
:root {
  --card-height: 200px;
  --card-width: 100%;
}

/* 长列表的每个卡片项 */
.list-item {
  content-visibility: auto;
  /* 元素在屏幕外时，浏览器按这个尺寸占位 */
  contain-intrinsic-size: var(--card-width) var(--card-height);
  
  /* 配合 contain 进一步隔离 */
  contain: layout style paint;
}

/* 长列表容器 */
.long-list {
  /* 滚动容器 */
  overflow-y: auto;
  /* 启用惰性渲染的子项数量无关，关键是每项都设了 content-visibility */
}

/* 进阶：不同内容用不同预估尺寸 */
.list-item--small  { contain-intrinsic-size: 100% 80px; }
.list-item--medium { contain-intrinsic-size: 100% 200px; }
.list-item--large  { contain-intrinsic-size: 100% 400px; }
```

## 执行步骤
1. **找出长列表**：页面中超过 50 项的列表/表格/卡片
2. **给每个项加 `content-visibility: auto`**：浏览器自动跳过屏幕外项
3. **预估项的高度**：用 `contain-intrinsic-size` 给一个真实高度（防止滚动条跳动）
4. **滚动测试**：观察是否还有滚动条长度变化（如果跳动，调整预估高度）

## 兼容性
- Chrome: 85+
- Firefox: 125+（实验性更早）
- Safari: 17+

## 降级方案
```css
@supports not (content-visibility: auto) {
  .list-item {
    /* 老浏览器：让浏览器自然渲染，不优化但保证功能 */
    contain: layout style;
  }
}

/* 极端长列表场景（万级数据），降级到虚拟列表方案 */
@supports not (content-visibility: auto) {
  /* 需 JS 实现：仅渲染可视区域 DOM，配合 IntersectionObserver */
}
```

## 性能对比
- 1000 项列表首次渲染：未优化 ~3000ms，加 `content-visibility: auto` 后 ~80ms
- 滚动 FPS：未优化 ~30fps，优化后稳定 60fps

## 相关链接
- [[contain-包含上下文]]
- [[will-change]]
- [[transform-硬件加速]]
- [[00-MOC-性能]]
