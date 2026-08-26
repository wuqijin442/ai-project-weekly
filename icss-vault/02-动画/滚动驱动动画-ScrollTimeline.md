---
title: 滚动驱动动画 ScrollTimeline
type: technique
tags:
  - icss/02-动画/滚动驱动
  - 难度/高级
  - 兼容性/实验
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[animation-动画属性]]"
  - "[[keyframes-关键帧]]"
  - "[[00-MOC-前沿特性]]"
---

# 滚动驱动动画 ScrollTimeline

## 问题/场景
传统滚动动画需要 JS 监听 `scroll` 事件 + `getBoundingClientRect()` 计算进度，性能差且代码繁琐。Chrome 115+ 原生支持 `animation-timeline`，让 CSS 动画直接由滚动进度驱动，无需 JS。

## 核心原理
`animation-timeline` 让动画的进度与滚动位置或元素可见性绑定：
- `scroll()`：基于滚动容器的滚动条进度（0% 顶部 → 100% 底部）
- `view()`：基于元素自身进入/离开视口的进度

`animation-range` 定义动画在时间轴上的触发范围，如 `entry 0%` 到 `exit 100%`。配合普通 `@keyframes`，浏览器自动用滚动进度替换时间进度。

## 实现方案
```css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --color-primary: #5e6ad2;
}

/* ① scroll()：滚动条驱动整页动画 */
@keyframes parallax {
  from { transform: translateY(0); }
  to   { transform: translateY(-200px); }
}
.c-parallax {
  animation: parallax linear both;
  animation-timeline: scroll();           /* 整页滚动进度驱动 */
}

/* ② scroll() 指定方向和容器 */
.c-progress-bar {
  animation: progress linear;
  animation-timeline: scroll(root block); /* root 视口、block 垂直方向 */
  transform-origin: 0 0;
}
@keyframes progress {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

/* ③ view()：元素进入视口时触发 */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(50px); }
  to   { opacity: 1; transform: translateY(0); }
}
.c-reveal {
  animation: fadeInUp var(--ease-out) both;
  animation-timeline: view();             /* 元素进入视口时驱动 */
  animation-range: entry 0% entry 100%;   /* 进入视口 0%→100% 期间 */
}

/* ④ view() 配合 range：滚动全程控制 */
.c-card-scroll {
  animation: cardTransform linear both;
  animation-timeline: view();
  animation-range: cover 0% cover 100%;   /* 从进入前到离开后全程 */
}
@keyframes cardTransform {
  0%   { opacity: 0; transform: scale(0.8) translateY(100px); }
  50%  { opacity: 1; transform: scale(1) translateY(0); }
  100% { opacity: 0; transform: scale(0.8) translateY(-100px); }
}

/* ⑤ 阅读进度条：顶部进度指示 */
.c-reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--color-primary);
  transform-origin: 0 0;
  animation: readingProgress linear;
  animation-timeline: scroll();
}
@keyframes readingProgress {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

/* ⑥ 滚动驱动旋转：3D 立体旋转跟随滚动 */
.c-3d-spin {
  animation: spin3d linear both;
  animation-timeline: scroll();
}
@keyframes spin3d {
  from { transform: rotateY(0deg); }
  to   { transform: rotateY(360deg); }
}
```

## 执行步骤
1. 写普通的 `@keyframes` 定义动画起止状态
2. 元素加 `animation: 名称 缓动 both`（**不要写 duration**，由滚动驱动）
3. 加 `animation-timeline: scroll()` 让整页滚动驱动动画进度
4. 或加 `animation-timeline: view()` 让元素进入视口驱动
5. 用 `animation-range: entry 0% entry 100%` 精确控制触发范围
6. `scroll()` 参数：`scroll(<container> <axis>)`，如 `scroll(root block)` 表示根视口垂直方向
7. `view()` 范围关键字：`cover`（含进入前/离开后）/`contain`（完全可见期间）/`entry`（进入）/`exit`（离开）

## 兼容性
- Chrome: 115+
- Edge: 115+
- Firefox: 仍实验性（需 flag）
- Safari: 不支持
- 降级方案：JS `IntersectionObserver` + `scroll` 监听

## 降级方案
```css
/* 不支持 animation-timeline 时降级到普通时间动画 */
@supports not (animation-timeline: scroll()) {
  .c-reveal {
    animation: fadeInUp 0.6s var(--ease-out) both;
    /* 失去滚动驱动，改为加载时一次性播放 */
  }
  .c-progress-bar {
    /* 进度条降级到固定 100% 或 JS 计算 */
    transform: scaleX(1);
  }
}

/* 配合 JS 降级方案（仅在 @supports 失败时执行） */
@supports not (animation-timeline: scroll()) {
  .c-reveal {
    opacity: 0;
    transform: translateY(50px);
    transition: opacity 0.6s var(--ease-out), transform 0.6s var(--ease-out);
  }
  .c-reveal.is-visible {
    opacity: 1;
    transform: translateY(0);
  }
  /* JS: const io = new IntersectionObserver(...) → 添加 .is-visible */
}
```

## 相关链接
- [[animation-动画属性]] - animation 子属性基础
- [[keyframes-关键帧]] - @keyframes 定义
- [[00-MOC-动画]]
- [[00-MOC-前沿特性]] - 路径动画 × 滚动驱动
