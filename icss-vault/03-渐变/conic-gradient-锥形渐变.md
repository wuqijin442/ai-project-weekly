---
title: conic-gradient 锥形渐变
type: technique
tags:
  - icss/03-渐变/conic
  - 难度/高级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[linear-gradient-线性渐变]]"
  - "[[radial-gradient-径向渐变]]"
  - "[[单标签加载动画]]"
  - "[[repeating渐变条纹]]"
---

# conic-gradient 锥形渐变

## 问题/场景
饼图、加载圈、雷达扫描、渐变边框——这些「绕中心点旋转」的视觉用 `linear-gradient`/`radial-gradient` 都难以实现。`conic-gradient` 锥形渐变沿圆周方向辐射颜色，是饼图和环形进度的原生方案。

## 核心原理
`conic-gradient(从角度 at 位置, 颜色1 起始角度, 颜色2 结束角度, ...)` 从中心点向外辐射，颜色沿圆周方向（顺时针）变化。
- 起始角度：`from 0deg`（默认从顶部开始）
- 位置：`at center`（默认中心）
- 颜色范围用 `起始角度 结束角度` 表示，如 `red 0deg 90deg` 表示红色覆盖 0°-90°
- 配合 `mask: radial-gradient(...)` 可镂空中心成环形

## 实现方案
```css
:root {
  --color-primary: #5e6ad2;
  --color-secondary: #a8b1ff;
  --color-accent: #ff6b6b;
  --color-success: #1dd1a1;
  --color-warning: #feca57;
}

/* ① 基础锥形渐变 */
.c-conic {
  background: conic-gradient(
    var(--color-primary),
    var(--color-secondary),
    var(--color-accent),
    var(--color-primary)
  );
}

/* ② 饼图：硬边色块 */
.c-pie {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: conic-gradient(
    var(--color-primary) 0deg 130deg,        /* 36% */
    var(--color-secondary) 130deg 250deg,    /* 33% */
    var(--color-accent) 250deg 360deg        /* 31% */
  );
}

/* ③ 环形进度条：conic + mask 镂空 */
.c-progress-ring {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: conic-gradient(
    var(--color-primary) 0deg 270deg,        /* 75% 进度 */
    rgba(94, 106, 210, 0.2) 270deg 360deg
  );
  -webkit-mask: radial-gradient(transparent 55%, #000 56%);
          mask: radial-gradient(transparent 55%, #000 56%);
}

/* ④ 锥形渐变边框：conic + mask 双层 */
.c-conic-border {
  position: relative;
  padding: 20px;
  border-radius: 12px;
  background: var(--color-bg, #fff);
}
.c-conic-border::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 2px;
  background: conic-gradient(
    var(--color-primary),
    var(--color-accent),
    var(--color-success),
    var(--color-primary)
  );
  -webkit-mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
          mask-composite: exclude;
  pointer-events: none;
}

/* ⑤ 旋转 loading：conic + mask + animation */
.c-loading {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: conic-gradient(transparent 0deg, var(--color-primary) 360deg);
  -webkit-mask: radial-gradient(transparent calc(50% - 3px), #000 calc(50% - 2px));
          mask: radial-gradient(transparent calc(50% - 3px), #000 calc(50% - 2px));
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ⑥ 雷达扫描：conic + 透明终止 */
.c-radar {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    rgba(94, 106, 210, 0.8) 0deg,
    transparent 90deg,
    transparent 360deg
  );
  animation: spin 4s linear infinite;
}

/* ⑦ 多色轮盘：等分色块 */
.c-wheel {
  background: conic-gradient(
    var(--color-primary) 0 25%,
    var(--color-secondary) 0 50%,
    var(--color-accent) 0 75%,
    var(--color-success) 0 100%
  );
  border-radius: 50%;
}

/* ⑧ 配合 @property 动画：色相旋转 */
@property --hue {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}
.c-rainbow-spin {
  background: conic-gradient(
    hsl(var(--hue) 80% 60%),
    hsl(calc(var(--hue) + 90deg) 80% 60%),
    hsl(calc(var(--hue) + 180deg) 80% 60%),
    hsl(calc(var(--hue) + 270deg) 80% 60%),
    hsl(var(--hue) 80% 60%)
  );
  animation: hueRotate 4s linear infinite;
}
@keyframes hueRotate {
  to { --hue: 360deg; }
}
```

## 执行步骤
1. 用 `conic-gradient(颜色1, 颜色2, ...)` 创建基础锥形渐变，颜色沿圆周顺时针变化
2. 饼图：颜色后跟角度范围（`颜色 0deg 130deg`）制造硬边色块
3. 环形进度：`conic-gradient` 绘制进度 + `mask: radial-gradient` 镂空中心
4. 渐变边框：伪元素 `padding: 2px` + 双层 mask（`mask-composite: exclude`）实现边框裁剪
5. Loading 圈：`conic-gradient(transparent 0, color 360)` + mask 镂空 + spin 动画
6. 雷达扫描：conic 从有色到透明的渐变 + spin 旋转
7. 色相动画：用 `@property` 注册 `--hue` 为 `<angle>`，在 `@keyframes` 中可插值

## 兼容性
- Chrome: 69+
- Firefox: 83+
- Safari: 12.1+
- Edge: 79+
- `mask-composite`: Chrome 120+（之前需 `-webkit-mask-composite: xor`）

## 降级方案
```css
/* 不支持 conic-gradient 时降级到 SVG 或多色拼接 */
@supports not (background: conic-gradient(red, blue)) {
  .c-pie {
    /* 降级到 SVG 饼图或多个半圆叠加 */
    background: var(--color-primary);
  }
  .c-loading {
    /* 降级到 border 旋转方案 */
    background: transparent;
    border: 3px solid rgba(94, 106, 210, 0.2);
    border-top-color: var(--color-primary);
    border-radius: 50%;
    -webkit-mask: none;
            mask: none;
  }
}

/* 不支持 mask 时降级到双层 div */
@supports not (mask: radial-gradient(transparent 50%, #000 50%)) {
  @supports not (-webkit-mask: radial-gradient(transparent 50%, #000 50%)) {
    .c-progress-ring {
      /* 需改用嵌套 div：外层 conic + 内层白色圆遮盖中心 */
      background: conic-gradient(var(--color-primary) 0 75%, transparent 75%);
    }
  }
}
```

## 相关链接
- [[linear-gradient-线性渐变]] - 线性渐变基础
- [[radial-gradient-径向渐变]] - 径向渐变
- [[单标签加载动画]] - conic 实现 loading 圈
- [[repeating渐变条纹]] - repeating-conic-gradient 棋盘格
- [[00-MOC-渐变]]
