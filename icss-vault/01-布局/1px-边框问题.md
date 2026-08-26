---
title: 1px 边框问题
type: technique
tags:
  - icss/01-布局/移动端
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[Flex-对齐与分布]]"
---

# 1px 边框问题

## 问题/场景
移动端高 DPR（设备像素比 ≥ 2）屏幕上，CSS 的 `1px` 边框实际渲染为 2~3 个物理像素，看起来比设计稿粗。设计师要求的「细发丝边框」在移动端无法直接用 `border: 1px` 实现，需要特殊技巧让边框视觉上呈现真正的 1 物理像素。

## 核心原理
CSS `1px` 是逻辑像素，在 DPR=2 的屏幕上等于 2 个物理像素。解决思路：用 `transform: scale(0.5)` 把一个 2px 元素缩小到 1px 视觉宽度，或用 `box-shadow` 模拟边框，或通过 viewport 缩放让 1 物理像素等于 1 逻辑像素。**伪元素 + scale** 方案兼容性最好、最推荐。

## 实现方案
```css
:root {
  --color-border: #ddd;
  --radius-sm: 4px;
}

/* ① 伪元素 + scale(0.5)：推荐方案，支持圆角 */
.c-hairline {
  position: relative;
}
.c-hairline::after {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  width: 200%;                            /* 2 倍宽高 */
  height: 200%;
  border: 1px solid var(--color-border);
  border-radius: calc(var(--radius-sm) * 2);  /* 圆角也要 2 倍 */
  transform: scale(0.5);                  /* 缩小到 0.5 */
  transform-origin: 0 0;
  box-sizing: border-box;
  pointer-events: none;                   /* 不阻挡点击 */
}

/* ② 单边 1px：底部边框 */
.c-hairline--bottom {
  position: relative;
}
.c-hairline--bottom::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 1px;
  background: var(--color-border);
  transform: scaleY(0.5);                 /* 仅 Y 方向缩放 */
  transform-origin: 0 100%;
}

/* ③ box-shadow 模拟：简洁但无法圆角 */
.c-hairline-shadow {
  box-shadow: 0 0 0 0.5px var(--color-border);
}

/* ④ viewport 缩放方案：全局解决（写在 HTML head） */
/*
<meta name="viewport" content="width=device-width, initial-scale=0.5, maximum-scale=0.5, user-scalable=no">
*/

/* ⑤ 媒体查询适配不同 DPR */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 2dppx) {
  .c-hairline--bottom::after {
    transform: scaleY(0.5);
  }
}
@media (-webkit-min-device-pixel-ratio: 3), (min-resolution: 3dppx) {
  .c-hairline--bottom::after {
    transform: scaleY(0.333);             /* DPR=3 缩到 1/3 */
  }
}
```

## 执行步骤
1. 容器加 `position: relative`，作为伪元素定位基准
2. 用 `::after` 伪元素绘制边框，宽高设为 `200%`（覆盖整个容器 + 余量）
3. 加 `border: 1px solid` 后用 `transform: scale(0.5)` 缩小，视觉上变为 0.5px
4. 圆角场景需把 `border-radius` 也放大 2 倍再缩小，保持比例
5. 单边场景改用 `background` + 单方向 `scaleY/scaleX`，更省资源
6. 高 DPR 设备（≥3）需用媒体查询切换 `scale(0.333)`
7. `pointer-events: none` 防止伪元素阻挡点击

## 兼容性
- Chrome: 全部
- Firefox: 全部
- Safari: 全部
- `box-shadow: 0.5px` 方案：Safari 不支持小数 shadow

## 降级方案
```css
/* 不支持 transform 的极端老旧设备降级到普通 1px 边框 */
@supports not (transform: scale(0.5)) {
  .c-hairline {
    border: 1px solid var(--color-border);
  }
  .c-hairline::after { display: none; }
}

/* 不支持伪元素时降级到 box-shadow */
@supports not (::after) {
  .c-hairline {
    box-shadow: 0 0 0 0.5px var(--color-border);
  }
}
```

## 相关链接
- [[Flex-对齐与分布]] - 边框常配合 Flex 列表项使用
- [[00-MOC-布局]]
- [[00-MOC-边框]] - 更多边框技巧（圆角、虚线、渐变边框）
