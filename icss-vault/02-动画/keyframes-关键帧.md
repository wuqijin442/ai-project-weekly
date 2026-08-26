---
title: keyframes 关键帧
type: technique
tags:
  - icss/02-动画/keyframes
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[animation-动画属性]]"
  - "[[transition-过渡技巧]]"
  - "[[动画核心原则]]"
---

# keyframes 关键帧

## 问题/场景
`transition` 只能从 A 到 B 两点过渡，复杂动画（旋转一周、多阶段变色、循环播放）需要 `@keyframes` 定义多个关键帧。配合 `animation` 属性实现循环、方向、保持终态等行为。

## 核心原理
`@keyframes` 用百分比（`0%`/`50%`/`100%`）或关键字（`from`/`to`）定义动画在各时间点的状态，浏览器自动在关键帧之间插值。`animation` 属性组合 `name duration timing-function delay iteration-count direction fill-mode play-state` 七个子属性。

- `alternate`：正反交替播放，适合来回运动
- `forwards`：保持终态，避免动画结束跳回初始
- `infinite`：无限循环

## 实现方案
```css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-spin: 1s;
  --color-primary: #5e6ad2;
}

/* ① 基础旋转：from/to 关键字 */
@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
.c-loading {
  animation: spin var(--duration-spin) infinite linear;
  /* name | duration | iteration-count | timing-function */
}

/* ② 多关键帧：弹跳效果 */
@keyframes bounce {
  0%   { transform: translateY(0); }
  50%  { transform: translateY(-30px); }
  100% { transform: translateY(0); }
}
.c-bounce {
  animation: bounce 0.6s var(--ease-out) infinite;
}

/* ③ alternate 方向：来回运动 */
@keyframes moveX {
  from { transform: translateX(0); }
  to   { transform: translateX(200px); }
}
.c-pendulum {
  animation: moveX 1s var(--ease-out) infinite alternate;
  /* alternate: 0→200 → 200→0 → 0→200 循环 */
}

/* ④ reverse 方向：反向播放 */
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
.c-fade-out {
  animation: fadeIn 0.3s var(--ease-out) reverse;  /* 1→0 淡出 */
}

/* ⑤ forwards 保持终态：单次播放后停在终态 */
@keyframes slideIn {
  from { transform: translateX(-100%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}
.c-once {
  animation: slideIn 0.5s var(--ease-out) forwards;  /* 停在终态 */
}

/* ⑥ 组合：多属性动画 */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
}
.c-pulse {
  animation: pulse 1.5s var(--ease-out) infinite;
}

/* ⑦ 颜色循环：多色关键帧 */
@keyframes rainbow {
  0%   { background: #ff6b6b; }
  25%  { background: #feca57; }
  50%  { background: #48dbfb; }
  75%  { background: #1dd1a1; }
  100% { background: #ff6b6b; }
}
.c-rainbow {
  animation: rainbow 4s infinite linear;
}

/* ⑧ 多动画并存：逗号分隔 */
.c-multi {
  animation:
    spin 2s infinite linear,
    pulse 1.5s infinite ease-in-out;
}
```

## 执行步骤
1. 用 `@keyframes 名称 {}` 定义动画序列，名称全局可用
2. 内部用 `0%`/`50%`/`100%` 或 `from`/`to` 定义关键帧状态
3. 元素加 `animation: 名称 时长 缓动 次数 方向 填充模式` 简写
4. 来回运动加 `alternate`，反向播放用 `reverse`，停在终态加 `forwards`
5. 仅动画 `transform`/`opacity`，避免重排
6. 多个动画并存用逗号分隔：`animation: a 1s, b 2s`
7. 性能优化：动画元素加 `will-change: transform`，结束后移除

## 兼容性
- Chrome: 43+
- Firefox: 16+
- Safari: 9+（部分需 `-webkit-` 前缀）
- Edge: 12+

## 降级方案
```css
/* 不支持 animation 时降级到静态状态 */
@supports not (animation: name) {
  .c-loading {
    /* 静态显示，无旋转 */
  }
}

/* prefers-reduced-motion：尊重用户偏好 */
@media (prefers-reduced-motion: reduce) {
  .c-loading,
  .c-bounce,
  .c-pulse {
    animation: none;
  }
}

/* 老版 Safari 前缀 */
@supports (-webkit-animation: name) and (not (animation: name)) {
  .c-loading {
    -webkit-animation: spin 1s infinite linear;
  }
}
```

## 相关链接
- [[animation-动画属性]] - animation 子属性详解
- [[transition-过渡技巧]] - 简单两点过渡用 transition
- [[动画核心原则]] - 性能原则
- [[hover-暂停最后一帧]] - forwards 单次播放
- [[00-MOC-动画]]
