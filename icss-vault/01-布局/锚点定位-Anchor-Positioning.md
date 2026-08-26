---
title: 锚点定位 Anchor Positioning（简版）
type: technique
tags:
  - icss/01-布局/锚点定位
  - 难度/高级
  - 兼容性/实验
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[Sticky-粘性定位]]"
  - "[[00-MOC-前沿特性]]"
---

# 锚点定位 Anchor Positioning（简版）

> 本笔记仅介绍布局意义与基础语法，**详细 API、@position-try 边界处理、完整 Popover 实现请见** [[Anchor-Positioning-锚点定位]]（12-前沿特性分类）。

## 问题/场景
传统绝对定位只能基于最近的 `position: relative` 父元素，无法跨容器定位。Tooltip/Popover 跟随触发元素需要 JS `getBoundingClientRect()` 计算。Anchor Positioning 让 CSS 原生具备「改变定位基准元素」的能力，是布局领域的重要突破。

## 核心原理
`anchor-name` 给元素打上「锚点标签」，`position-anchor` 让目标元素引用该锚点，`anchor()` 函数在 `top`/`left` 中动态读取锚点方位坐标。目标元素无需是锚点的子元素，可跨任意层级定位。

## 实现方案
```css
:root {
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
  --duration: 0.2s;
}

/* ① 声明锚点：触发按钮 */
.c-trigger {
  anchor-name: --menu-anchor;            /* 给按钮打锚点标签 */
}

/* ② 绑定锚点：弹出层基于锚点定位 */
.c-popover {
  position: fixed;                       /* 必须 fixed/absolute */
  position-anchor: --menu-anchor;        /* 引用锚点 */
  top: anchor(--menu-anchor bottom);     /* 锚点底部对齐 */
  left: anchor(--menu-anchor center);    /* 锚点水平居中 */
  transform: translate(-50%, 5px);
  transition: transform var(--duration) var(--ease), opacity var(--duration) var(--ease);
}

/* ③ 尺寸继承：宽度跟随锚点 */
.c-popover--match {
  width: anchor-size(width);             /* 宽度等于锚点宽度 */
}
```

## 执行步骤
1. 在触发元素上加 `anchor-name: --xxx`，命名锚点（双横线开头）
2. 在弹出元素上加 `position-anchor: --xxx`，绑定锚点
3. 用 `top/ left: anchor(--xxx 方位)` 动态读取锚点位置坐标
4. 用 `anchor-size(width/height)` 让弹出层尺寸跟随锚点
5. 配合 `transition` 仅动画 `transform`/`opacity`，弹出收起丝滑
6. 边界翻转、候补位置等进阶用法见 [[00-MOC-前沿特性]]

## 兼容性
- Chrome: 125+
- Firefox: 实验性（需 flag）
- Safari: 实验性
- 降级方案：JS 计算定位 / floating-ui 库

## 降级方案
```css
@supports not (anchor-name: --test) {
  /* 降级到普通绝对定位，丢失跨容器能力 */
  .c-popover {
    position: absolute;
    top: 100%;
    left: 0;
    transform: none;
  }
}
```

## 相关链接
- [[Sticky-粘性定位]] - 同属定位家族，sticky 用于吸顶
- [[00-MOC-布局]]
- [[00-MOC-前沿特性]] - Anchor 完整 API、@position-try 智能边界
