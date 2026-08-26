---
title: transition 过渡技巧
type: technique
tags:
  - icss/02-动画/transition
  - 难度/初级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[动画核心原则]]"
  - "[[keyframes-关键帧]]"
  - "[[CSS变量复用动画函数]]"
---

# transition 过渡技巧

## 问题/场景
hover、focus、状态切换时需要平滑过渡而非生硬跳变。`transition` 是 CSS 最简单的动画能力，但 `transitionend` 事件监听、hover 暂停动画、复用 CSS 变量等进阶技巧常被忽略。

## 核心原理
`transition` 定义属性从状态 A 到状态 B 的过渡。完整属性：`property duration timing-function delay`。仅当属性值变化时触发，结束后触发 `transitionend` 事件。**关键限制**：仅对可中间值属性生效（`display` 无法过渡，需用 `visibility` 或 `opacity` 替代）。

## 实现方案
```css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-base: 0.3s;
  --color-primary: #5e6ad2;
  --color-hover: #4a55b8;
}

/* ① 基础 hover 过渡 */
.c-btn {
  background: var(--color-primary);
  transition: background var(--duration-base) var(--ease-out),
              transform var(--duration-base) var(--ease-out);
}
.c-btn:hover {
  background: var(--color-hover);
  transform: translateY(-2px);
}

/* ② 全属性过渡（慎用，性能差） */
.c-all {
  transition: all var(--duration-base) var(--ease-out);  /* ❌ 会过渡非必要属性 */
}

/* ③ transitionend 事件配合：链式动画 */
.c-accordion {
  max-height: 0;
  overflow: hidden;
  transition: max-height var(--duration-base) var(--ease-out);
}
.c-accordion.is-open {
  max-height: 500px;
}
/* JS:
   el.addEventListener('transitionend', (e) => {
     if (e.propertyName === 'max-height') { ... }
   });
*/

/* ④ hover 暂停动画：暂停正在运行的 animation */
.c-loading {
  animation: spin 1s infinite linear;
}
.c-loading:hover {
  animation-play-state: paused;          /* hover 时暂停 */
}

/* ⑤ CSS 变量复用：统一管理 */
.c-card {
  --hover-translate: -4px;
  transition: transform var(--duration-base) var(--ease-out);
}
.c-card:hover {
  transform: translateY(var(--hover-translate));
}
.c-card--large {
  --hover-translate: -8px;               /* 覆盖变量即可改变位移量 */
}

/* ⑥ display 切换过渡：用 visibility + opacity */
.c-modal {
  visibility: hidden;
  opacity: 0;
  transition: visibility 0s var(--duration-base),
              opacity var(--duration-base) var(--ease-out);
}
.c-modal.is-visible {
  visibility: visible;
  opacity: 1;
  transition: visibility 0s,
              opacity var(--duration-base) var(--ease-out);
}

/* ⑦ 延迟过渡：hover 后稍等再触发 */
.c-tooltip {
  opacity: 0;
  transition: opacity var(--duration-base) var(--ease-out) 0.5s;  /* delay 0.5s */
}
.c-trigger:hover .c-tooltip {
  opacity: 1;
}
```

## 执行步骤
1. 在元素的**基础状态**（非 hover）上加 `transition`，定义要过渡的属性、时长、缓动
2. 在 `:hover`/`.is-active` 等状态类中改变属性值，自动触发过渡
3. 仅过渡 `transform`/`opacity`/`background`/`color` 等性能友好属性，避免 `width`/`top`
4. 链式动画用 JS 监听 `transitionend`，通过 `e.propertyName` 判断哪条过渡结束
5. 用 CSS 变量统一管理时长/缓动/位移量，组件变体只需覆盖变量
6. `display: none` 无法过渡，改用 `visibility: hidden` + `opacity: 0` 组合
7. `visibility` 延迟设为 `0s 0.3s`（隐藏时延迟），显示时设为 `0s`（立即），实现「淡入立即、淡出延迟」

## 兼容性
- Chrome: 26+
- Firefox: 16+
- Safari: 6.1+（部分属性需 `-webkit-` 前缀）
- Edge: 12+

## 降级方案
```css
/* 不支持 transition 时降级到无动画直接跳变 */
@supports not (transition: opacity 0.3s) {
  .c-btn { transition: none; }
}

/* max-height 过渡的优雅降级（无法精确内容高度） */
@supports not (interpolate-size: allow-keywords) {
  .c-accordion {
    /* 旧方案：估算 max-height */
    max-height: 500px;
  }
}

/* 现代方案（Chrome 129+）：原生支持 height auto 过渡 */
@supports (interpolate-size: allow-keywords) {
  .c-accordion {
    interpolate-size: allow-keywords;
    max-height: auto;                    /* 原生 auto 过渡 */
  }
}
```

## 相关链接
- [[动画核心原则]] - 性能原则：仅 transform/opacity
- [[keyframes-关键帧]] - 复杂动画用 @keyframes
- [[CSS变量复用动画函数]] - 变量统一管理动画参数
- [[hover-暂停最后一帧]] - hover 暂停动画详解
- [[00-MOC-动画]]
