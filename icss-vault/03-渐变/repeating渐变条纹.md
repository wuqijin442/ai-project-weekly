---
title: repeating 渐变条纹
type: technique
tags:
  - icss/03-渐变/repeating
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[linear-gradient-线性渐变]]"
  - "[[conic-gradient-锥形渐变]]"
  - "[[渐变实现复杂背景]]"
---

# repeating 渐变条纹

## 问题/场景
斑马线背景、斜条纹分隔、棋盘格、网格底纹——这些重复图案用图片资源太重，用 `background-image` 平铺有锯齿。`repeating-linear-gradient`/`repeating-radial-gradient`/`repeating-conic-gradient` 三兄弟能纯 CSS 实现任意重复图案，且矢量清晰、可缩放。

## 核心原理
- `repeating-linear-gradient`：线性方向重复条纹
- `repeating-radial-gradient`：径向同心圆重复
- `repeating-conic-gradient`：扇形重复（适合棋盘格）

**关键技巧**：颜色位置必须连续（`颜色1 0 10px, 颜色2 10px 20px`），浏览器自动按这个 pattern 重复。第一个和最后一个颜色必须相同，否则首尾衔接处会有色差。

## 实现方案
```css
:root {
  --color-primary: #5e6ad2;
  --color-secondary: #a8b1ff;
  --color-stripe-dark: #e8eaf6;
  --color-stripe-light: #f5f6ff;
  --color-bg: #fff;
}

/* ① 水平条纹：repeating-linear-gradient */
.c-stripes-h {
  background: repeating-linear-gradient(
    to bottom,
    var(--color-stripe-light) 0,
    var(--color-stripe-light) 10px,
    var(--color-stripe-dark) 10px,
    var(--color-stripe-dark) 20px
  );
}

/* ② 斜条纹：45 度 */
.c-stripes-45 {
  background: repeating-linear-gradient(
    45deg,
    var(--color-primary) 0,
    var(--color-primary) 10px,
    var(--color-secondary) 10px,
    var(--color-secondary) 20px
  );
}

/* ③ 斜条纹（更精细）：双倍周期 */
.c-stripes-fine {
  background: repeating-linear-gradient(
    45deg,
    var(--color-primary) 0 5px,
    var(--color-secondary) 5px 10px,
    var(--color-primary) 10px 15px,
    var(--color-secondary) 15px 20px
  );
}

/* ④ 同心圆条纹：repeating-radial-gradient */
.c-rings {
  background: repeating-radial-gradient(
    circle at center,
    var(--color-primary) 0,
    var(--color-primary) 10px,
    var(--color-secondary) 10px,
    var(--color-secondary) 20px
  );
}

/* ⑤ 棋盘格：双 repeating-conic-gradient 叠加 */
.c-checkerboard {
  background:
    repeating-conic-gradient(
      var(--color-stripe-dark) 0 25%,
      var(--color-stripe-light) 0 50%
    )
    0 0 / 40px 40px;
}

/* ⑥ 双色棋盘：错位叠加 */
.c-checkerboard-2 {
  background:
    repeating-conic-gradient(
      var(--color-primary) 0 25%,
      transparent 0 50%
    )
    0 0 / 40px 40px,
    repeating-conic-gradient(
      var(--color-secondary) 0 25%,
      transparent 0 50%
    )
    20px 20px / 40px 40px;
  background-color: var(--color-bg);
}

/* ⑦ 渐变条纹：颜色过渡 + 重复 */
.c-gradient-stripes {
  background: repeating-linear-gradient(
    45deg,
    var(--color-primary) 0 10px,
    var(--color-secondary) 10px 20px
  );
  background-size: 28px 28px;
}

/* ⑧ 动画条纹：背景位置移动 */
.c-animated-stripes {
  background: repeating-linear-gradient(
    45deg,
    var(--color-primary) 0 10px,
    var(--color-secondary) 10px 20px
  );
  background-size: 28px 28px;
  animation: stripesMove 1s linear infinite;
}
@keyframes stripesMove {
  to { background-position: 28px 0; }      /* 移动一个周期 */
}

/* ⑨ 暗黑模式：低对比条纹 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-stripe-dark: #2a2d4a;
    --color-stripe-light: #1a1d3a;
  }
}
```

## 执行步骤
1. 用 `repeating-linear-gradient(角度, 颜色1 0 宽度, 颜色2 宽度 双倍宽度)` 创建条纹
2. 颜色位置必须连续无间隙（`颜色1 0 10px, 颜色2 10px 20px`），否则有空白
3. 第一个和最后一个颜色保持一致，避免首尾衔接处色差
4. 棋盘格用 `repeating-conic-gradient` + `background-size` 控制 cell 大小
5. 双色棋盘：两层 conic 错位 50% 叠加
6. 动画条纹：用 `background-position` 移动一个周期长度，配合 `animation` 循环
7. 颜色统一用 CSS 变量，暗黑模式只改变量值

## 兼容性
- `repeating-linear-gradient`: Chrome 26+, Firefox 16+, Safari 6.1+
- `repeating-radial-gradient`: Chrome 26+, Firefox 16+, Safari 6.1+
- `repeating-conic-gradient`: Chrome 69+, Firefox 83+, Safari 12.1+

## 降级方案
```css
/* 不支持 repeating-conic-gradient 时降级到 linear-gradient 平铺 */
@supports not (background: repeating-conic-gradient(red, blue)) {
  .c-checkerboard {
    background:
      linear-gradient(45deg, var(--color-stripe-dark) 25%, transparent 25%) 0 0 / 20px 20px,
      linear-gradient(-45deg, var(--color-stripe-dark) 25%, transparent 25%) 0 0 / 20px 20px,
      linear-gradient(45deg, transparent 75%, var(--color-stripe-dark) 75%) 0 0 / 20px 20px,
      linear-gradient(-45deg, transparent 75%, var(--color-stripe-dark) 75%) 0 0 / 20px 20px;
    background-color: var(--color-stripe-light);
  }
}

/* 不支持渐变时降级到纯色 */
@supports not (background: repeating-linear-gradient(red, blue)) {
  .c-stripes-h {
    background: var(--color-stripe-light);
  }
}

/* prefers-reduced-motion：禁用动画条纹 */
@media (prefers-reduced-motion: reduce) {
  .c-animated-stripes {
    animation: none;
  }
}
```

## 相关链接
- [[linear-gradient-线性渐变]] - 线性渐变基础
- [[conic-gradient-锥形渐变]] - 锥形渐变（棋盘格基础）
- [[渐变实现复杂背景]] - 多层条纹叠加复杂图案
- [[00-MOC-渐变]]
