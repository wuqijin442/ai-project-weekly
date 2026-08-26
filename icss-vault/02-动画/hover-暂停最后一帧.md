---
title: hover 暂停最后一帧
type: technique
tags:
  - icss/02-动画/暂停
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[animation-动画属性]]"
  - "[[keyframes-关键帧]]"
  - "[[transition-过渡技巧]]"
---

# hover 暂停最后一帧

## 问题/场景
动画播放一次后保持终态、hover 时暂停在当前位置、点击触发单次播放——这些「动画控制」需求常被误解为必须用 JS。其实 `animation-play-state` + `animation-fill-mode: forwards` 组合即可纯 CSS 实现。

## 核心原理
- `animation-play-state: paused`：暂停动画，元素停留在当前帧
- `animation-play-state: running`：恢复播放
- `animation-fill-mode: forwards`：动画结束后保持终态样式
- `animation-iteration-count: 1`：仅播放一次（非无限循环）

**关键技巧**：`forwards` 让动画播放完毕后保留 `to {}` 状态；`paused` 可在任意帧冻结，配合 hover 实现交互暂停。

## 实现方案
```css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --duration: 0.5s;
  --color-primary: #5e6ad2;
}

/* ① 单次播放保持终态：forwards */
@keyframes slideIn {
  from { transform: translateX(-100%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}
.c-once {
  animation: slideIn var(--duration) var(--ease-out) forwards;
  /* 播放一次后停在 to 状态，不跳回 from */
}

/* ② hover 暂停：正在循环的动画 hover 时暂停 */
@keyframes spin {
  to { transform: rotate(360deg); }
}
.c-hover-pause {
  animation: spin 2s linear infinite;
  animation-play-state: running;
}
.c-hover-pause:hover {
  animation-play-state: paused;           /* hover 时冻结当前帧 */
}

/* ③ hover 启动：默认暂停，hover 时播放一次 */
.c-hover-start {
  animation: slideIn var(--duration) var(--ease-out) forwards;
  animation-play-state: paused;           /* 默认暂停 */
}
.c-hover-start:hover {
  animation-play-state: running;          /* hover 启动播放 */
}

/* ④ 切换类名触发播放：JS 配合 */
.c-trigger {
  opacity: 0;
  transform: translateY(20px);
}
.c-trigger.is-active {
  animation: slideIn var(--duration) var(--ease-out) forwards;
  /* JS: el.classList.add('is-active') 触发动画 */
}

/* ⑤ 列表项依次进入：负 delay 错开 + forwards */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.c-list > * {
  opacity: 0;                              /* 初始隐藏 */
  animation: fadeInUp var(--duration) var(--ease-out) forwards;
}
.c-list > *:nth-child(1) { animation-delay: 0s; }
.c-list > *:nth-child(2) { animation-delay: 0.1s; }
.c-list > *:nth-child(3) { animation-delay: 0.2s; }
.c-list > *:nth-child(4) { animation-delay: 0.3s; }
.c-list > *:nth-child(5) { animation-delay: 0.4s; }

/* ⑥ 视口进入时播放：配合 IntersectionObserver */
.c-reveal {
  opacity: 0;
  transform: translateY(40px);
  animation: fadeInUp var(--duration) var(--ease-out) forwards;
  animation-play-state: paused;           /* 默认暂停 */
}
.c-reveal.is-visible {
  animation-play-state: running;          /* 进入视口时播放 */
}
```

## 执行步骤
1. 动画声明末尾加 `forwards`，确保播放完毕保留 `to {}` 终态样式
2. 仅播放一次设置 `iteration-count: 1`（简写中可省略，默认为 1）
3. hover 暂停用 `:hover { animation-play-state: paused; }`
4. hover 启动：基础类设 `animation-play-state: paused`，`:hover` 改为 `running`
5. 列表项错开进入：`opacity: 0` 初始隐藏 + `forwards` + 递增 `animation-delay`
6. 视口触发：默认 `paused`，JS `IntersectionObserver` 添加类名后改 `running`

## 兼容性
- Chrome: 43+
- Firefox: 16+
- Safari: 9+
- Edge: 12+

## 降级方案
```css
/* 不支持 animation 时降级到 transition + 类名切换 */
@supports not (animation: name) {
  .c-once {
    transform: translateX(-100%);
    opacity: 0;
    transition: transform var(--duration) var(--ease-out),
                opacity var(--duration) var(--ease-out);
  }
  .c-once.is-shown {
    transform: translateX(0);
    opacity: 1;
  }
  /* JS: el.classList.add('is-shown') */
}

/* prefers-reduced-motion：禁用动画但保留终态 */
@media (prefers-reduced-motion: reduce) {
  .c-once,
  .c-list > *,
  .c-reveal {
    animation: none;
    opacity: 1;
    transform: none;
  }
}

/* 不支持 forwards 时降级：JS 监听 animationend 添加终态类 */
@supports not (animation-fill-mode: forwards) {
  .c-once.is-done {
    transform: translateX(0);
    opacity: 1;
  }
  /* JS: el.addEventListener('animationend', () => el.classList.add('is-done')) */
}
```

## 相关链接
- [[animation-动画属性]] - play-state/fill-mode 详解
- [[keyframes-关键帧]] - @keyframes 定义
- [[transition-过渡技巧]] - 简单过渡替代方案
- [[00-MOC-动画]]
