---
title: Sticky 粘性定位
type: technique
tags:
  - icss/01-布局/sticky
  - 难度/初级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[锚点定位-Anchor-Positioning]]"
  - "[[Flex-对齐与分布]]"
---

# Sticky 粘性定位

## 问题/场景
长页面滚动时，导航栏/分类标题/表头需要「滚动到顶部后吸住」继续固定显示。`position: fixed` 会脱离文档流导致内容跳跃，`position: sticky` 能在滚动到阈值前保持正常流式定位，到达阈值后转为固定，是最自然的吸顶方案。

## 核心原理
`position: sticky` 是 `relative` 和 `fixed` 的混合体。元素默认按 `relative` 流式排版，当滚动使其相对容器边距达到 `top`/`bottom`/`left`/`right` 阈值时，自动转为 `fixed` 行为固定在阈值位置。**关键限制**：sticky 元素只能在**最近的滚动容器**内活动，若父元素 `overflow: hidden` 或高度不够会失效。

## 实现方案
```css
:root {
  --header-h: 60px;
  --color-bg: #fff;
  --color-border: #eee;
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
  --duration: 0.2s;
}

/* ① 吸顶导航：滚动到 top:0 时吸住 */
.c-header {
  position: sticky;
  top: 0;                                /* 滚动到距视口顶部 0 时固定 */
  z-index: 100;
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
  transition: box-shadow var(--duration) var(--ease);  /* 仅动画 box-shadow */
}
.c-header.is-stuck {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* ② 表头吸顶：表格头滚动时保持可见 */
.c-table thead th {
  position: sticky;
  top: var(--header-h);                  /* 让位于吸顶导航下方 */
  background: var(--color-bg);
  z-index: 10;
}

/* ③ 多级吸顶：分类标题依次吸顶 */
.c-section__title--h1 { position: sticky; top: 0;       z-index: 30; }
.c-section__title--h2 { position: sticky; top: 40px;    z-index: 20; }
.c-section__title--h3 { position: sticky; top: 80px;    z-index: 10; }

/* ④ 底部吸底：滑动到底部时吸住 */
.c-footer-bar {
  position: sticky;
  bottom: 0;                             /* 滚动到底部时吸住 */
  z-index: 50;
}

/* ⑤ 横向吸左：侧边栏滚动时吸住左边 */
.c-sidebar {
  position: sticky;
  left: 0;
  top: var(--header-h);
  height: calc(100vh - var(--header-h));
  overflow-y: auto;
}
```

## 执行步骤
1. 元素加 `position: sticky`，并指定至少一个阈值（`top`/`bottom`/`left`/`right`）
2. 检查所有祖先元素，确保没有 `overflow: hidden/auto/scroll` 阻断（否则 sticky 仅在祖先内生效）
3. sticky 元素的父容器必须有足够高度（否则没有滚动空间，sticky 不触发）
4. 用 `z-index` 确保吸顶时层级高于后续内容
5. 多级吸顶时，下级 `top` 值要大于上级高度，避免重叠遮挡
6. 配合 `transition` 仅动画 `box-shadow`/`opacity`，避免触发布局重排

## 兼容性
- Chrome: 56+
- Firefox: 32+
- Safari: 13+（之前需 `-webkit-` 前缀）
- Edge: 16+

## 降级方案
```css
/* 不支持 sticky 时降级到 relative（无吸顶效果，但布局不乱） */
@supports not (position: sticky) {
  .c-header { position: relative; }
  /* 进阶降级需 JS 监听 scroll 切换 fixed */
}

/* Safari 老版前缀 */
@supports (-webkit-sticky: initial) and (not (position: sticky)) {
  .c-header { position: -webkit-sticky; }
}
```

## 相关链接
- [[锚点定位-Anchor-Positioning]] - 跨容器定位的进阶方案
- [[Flex-对齐与分布]] - 吸顶导航内部常用 Flex 布局
- [[00-MOC-布局]]
