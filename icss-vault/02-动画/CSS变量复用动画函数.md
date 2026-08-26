---
title: CSS 变量复用动画函数
type: technique
tags:
  - icss/02-动画/变量
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[动画核心原则]]"
  - "[[animation-动画属性]]"
  - "[[transition-过渡技巧]]"
---

# CSS 变量复用动画函数

## 问题/场景
项目里多个组件用不同缓动函数、不同时长，散落在各处难以统一管理。改一次设计稿要从几十个文件里搜索替换。用 CSS 变量统一管理 `--ease`/`--duration`，配合 `@property` 注册类型化变量，可实现全局一致性。

## 核心原理
- **CSS 变量**：`--ease: cubic-bezier(0.4,0,0.2,1)` 全局定义，各组件 `var(--ease)` 引用
- **`@property` 注册**：声明变量的语法、初始值、是否继承，让浏览器知道这是 `<time>`/`<easing-function>` 类型，可在动画中插值
- **`@property` 关键意义**：未注册的变量默认是字符串，无法在 `@keyframes` 中插值；注册为 `<length>`/`<color>` 后，可在关键帧间平滑过渡

## 实现方案
```css
:root {
  /* ① 统一管理缓动函数 */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* ② 统一管理时长 */
  --duration-fast: 0.2s;
  --duration-base: 0.3s;
  --duration-slow: 0.5s;

  /* ③ 颜色变量 */
  --color-primary: #5e6ad2;
  --color-hover: #4a55b8;
}

/* ④ @property 注册类型化变量（关键） */
@property --angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}
@property --hue {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}
@property --glow {
  syntax: "<length>";
  initial-value: 0px;
  inherits: false;
}

/* ⑤ 组件复用变量 */
.c-btn {
  background: var(--color-primary);
  transition: transform var(--duration-base) var(--ease-out),
              background var(--duration-base) var(--ease-out);
}
.c-btn:hover {
  background: var(--color-hover);
  transform: translateY(-2px);
}
.c-btn--bounce {
  transition: transform var(--duration-base) var(--ease-bounce);  /* 复用回弹缓动 */
}

/* ⑥ @property 让变量可动画：旋转角度 */
.c-conic-spin {
  background: conic-gradient(
    hsl(var(--hue) 80% 60%),
    hsl(calc(var(--hue) + 120deg) 80% 60%),
    hsl(calc(var(--hue) + 240deg) 80% 60%),
    hsl(var(--hue) 80% 60%)
  );
  animation: hueRotate 4s linear infinite;
}
@keyframes hueRotate {
  to { --hue: 360deg; }                   /* 可插值，因为 @property 注册了 <angle> */
}

/* ⑦ @property 让 glow 可动画 */
.c-glow-card {
  --glow: 0px;
  box-shadow: 0 0 var(--glow) var(--color-primary);
  transition: --glow var(--duration-base) var(--ease-out);
}
.c-glow-card:hover {
  --glow: 20px;                           /* 平滑过渡，因为注册为 <length> */
}

/* ⑧ 组件级覆盖：变体只需覆盖变量 */
.c-card { transition: transform var(--duration-base) var(--ease-out); }
.c-card--slow { --duration-base: 0.8s; }  /* 覆盖时长 */
.c-card--bounce { --ease-out: var(--ease-bounce); }  /* 覆盖缓动 */

/* ⑨ 主题切换：暗黑模式只需改变量 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #8b95ff;
    --color-hover: #a8b1ff;
  }
}
```

## 执行步骤
1. 在 `:root` 定义 `--ease-*`/`--duration-*`/`--color-*` 系列变量
2. 所有 `transition`/`animation` 引用变量，禁止硬编码 `0.3s`/`ease`
3. 需要在 `@keyframes` 内插值的变量，用 `@property` 注册为类型化变量
4. `@property` 声明 `syntax`（如 `<angle>`/`<length>`/`<color>`）、`initial-value`、`inherits`
5. 组件变体只需覆盖局部变量：`.c-card--slow { --duration-base: 0.8s; }`
6. 暗黑模式/主题切换只需改变量值，所有引用处自动更新
7. `@property` 注册的变量可在 `@keyframes` 中作为可动画属性使用

## 兼容性
- CSS 变量：Chrome 49+, Firefox 31+, Safari 9.1+
- `@property`: Chrome 85+, Edge 85+, Safari 16.4+, Firefox 128+

## 降级方案
```css
/* 不支持 @property 时降级到 transform/opacity 动画 */
@supports not (background: paint(test)) {
  @supports not (@property: --test) {
    .c-conic-spin {
      animation: hueRotateFallback 4s linear infinite;
    }
    @keyframes hueRotateFallback {
      from { filter: hue-rotate(0deg); }
      to   { filter: hue-rotate(360deg); }  /* 用 filter 替代变量动画 */
    }
    .c-glow-card {
      transition: box-shadow var(--duration-base) var(--ease-out);  /* 退回 box-shadow 动画 */
    }
  }
}

/* 不支持 CSS 变量时降级到硬编码 */
@supports not (--a: 0) {
  .c-btn {
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }
}
```

## 相关链接
- [[动画核心原则]] - 性能原则与 will-change
- [[animation-动画属性]] - animation 简写
- [[transition-过渡技巧]] - transition 复用变量
- [[00-MOC-动画]]
- [[00-MOC-现代特性]] - @property/Houdini 详解
