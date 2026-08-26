---
title: animation 动画属性
type: technique
tags:
  - icss/02-动画/animation
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[keyframes-关键帧]]"
  - "[[hover-暂停最后一帧]]"
  - "[[CSS变量复用动画函数]]"
---

# animation 动画属性

## 问题/场景
`animation` 简写背后的 7 个子属性各有妙用：`animation-delay` 负值可「跳过动画开头」，`steps()` 步进函数实现逐帧精灵动画，`play-state` 控制 hover 暂停。掌握这些细节才能写出精密控制的动画。

## 核心原理
`animation` 完整子属性：
- `animation-name`：`@keyframes` 名称
- `animation-duration`：单次时长
- `animation-timing-function`：缓动函数，`steps(n)` 可步进
- `animation-delay`：延迟开始，**负值**表示从动画中段开始
- `animation-iteration-count`：次数，`infinite` 无限
- `animation-direction`：`normal`/`reverse`/`alternate`/`alternate-reverse`
- `animation-fill-mode`：`none`/`forwards`/`backwards`/`both`
- `animation-play-state`：`running`/`paused`

## 实现方案
```css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --duration: 1s;
}

/* ① 完整简写顺序 */
.c-full {
  animation:
    spin              /* name */
    var(--duration)   /* duration */
    var(--ease-out)   /* timing-function */
    0s                /* delay */
    infinite          /* iteration-count */
    normal            /* direction */
    forwards          /* fill-mode */
    running;          /* play-state */
}

/* ② animation-delay 负值：从动画中段开始 */
@keyframes spin {
  to { transform: rotate(360deg); }
}
.c-delay-negative {
  animation: spin 1s infinite linear;
  animation-delay: -0.5s;                /* 从动画 50% 位置开始 */
}
/* 应用：多个 loading 圈错开起始角度，避免同步旋转 */

/* ③ steps() 步进函数：精灵图逐帧动画 */
@keyframes sprite {
  to { background-position: -800px 0; }  /* 8 帧 × 100px */
}
.c-sprite {
  width: 100px;
  height: 100px;
  background: url('sprite.png') no-repeat;
  animation: sprite 0.8s infinite steps(8);  /* 8 步，无插值 */
}

/* ④ steps() 实现打字机效果 */
@keyframes typing {
  from { width: 0; }
  to   { width: 12ch; }
}
.c-typewriter {
  overflow: hidden;
  white-space: nowrap;
  border-right: 2px solid currentColor;
  animation:
    typing 2s steps(12),                  /* 12 字符逐个出现 */
    blink 0.6s step-end infinite;         /* 光标闪烁 */
}
@keyframes blink {
  50% { border-color: transparent; }
}

/* ⑤ play-state 暂停：hover 暂停 */
.c-running {
  animation: spin 1s infinite linear;
  animation-play-state: running;
}
.c-running:hover {
  animation-play-state: paused;           /* hover 暂停 */
}

/* ⑥ fill-mode 详解 */
.c-none     { animation: fadeIn 0.3s; animation-fill-mode: none; }      /* 结束跳回初始 */
.c-forwards { animation: fadeIn 0.3s; animation-fill-mode: forwards; }  /* 保持终态 */
.c-backwards { animation: fadeIn 0.3s 1s; animation-fill-mode: backwards; } /* delay 期间应用第一帧 */
.c-both     { animation: fadeIn 0.3s 1s; animation-fill-mode: both; }   /* 同时具备 forwards+backwards */

/* ⑦ 多动画负 delay 错开 */
.c-stagger-1 { animation: fadeIn 0.3s -0.0s both; }
.c-stagger-2 { animation: fadeIn 0.3s -0.1s both; }
.c-stagger-3 { animation: fadeIn 0.3s -0.2s both; }
.c-stagger-4 { animation: fadeIn 0.3s -0.3s both; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

## 执行步骤
1. 用简写 `animation: name duration timing delay count direction fill play-state` 一行声明
2. **delay 负值**让动画从指定位置开始播放，常用于错开多个动画的起始相位
3. **steps(n)** 让动画分 n 步跳变（无插值），用于精灵图逐帧、打字机逐字
4. **play-state: paused** 配合 hover/focus 实现交互暂停
5. **fill-mode: forwards** 让动画结束后保持终态，避免跳回初始
6. **fill-mode: backwards** 让 delay 期间就应用第一帧样式
7. 多元素错开动画用递增的负 delay，比递增正 delay 更优雅（同时启动但相位不同）

## 兼容性
- Chrome: 43+
- Firefox: 16+
- Safari: 9+
- Edge: 12+
- `animation-composition`（多 transform 合成）：Chrome 112+

## 降级方案
```css
/* 不支持 steps() 时降级到线性插值 */
@supports not (animation-timing-function: steps(1)) {
  .c-sprite {
    animation-timing-function: linear;    /* 失去逐帧效果，但动画仍运行 */
  }
}

/* 不支持 animation 时降级到静态显示 */
@supports not (animation: name) {
  .c-sprite {
    background-position: 0 0;
  }
}

/* prefers-reduced-motion：禁用动画但保留终态 */
@media (prefers-reduced-motion: reduce) {
  .c-forwards {
    animation: none;
    opacity: 1;                           /* 直接应用终态样式 */
    transform: none;
  }
}
```

## 相关链接
- [[keyframes-关键帧]] - @keyframes 定义
- [[hover-暂停最后一帧]] - play-state + forwards 单次播放
- [[CSS变量复用动画函数]] - 变量统一管理动画参数
- [[单标签加载动画]] - steps() 配合 conic-gradient
- [[00-MOC-动画]]
