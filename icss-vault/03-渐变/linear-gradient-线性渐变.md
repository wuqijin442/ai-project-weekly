---
title: linear-gradient 线性渐变
type: technique
tags:
  - icss/03-渐变/linear
  - 难度/初级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[radial-gradient-径向渐变]]"
  - "[[repeating渐变条纹]]"
  - "[[background-clip-文字渐变]]"
---

# linear-gradient 线性渐变

## 问题/场景
按钮背景、卡片强调、分割线渐变、进度条填充——线性渐变是最高频的视觉装饰。掌握角度方向、多色渐变、透明度、`repeating-linear-gradient` 条纹，能覆盖大部分渐变需求。

## 核心原理
`linear-gradient(方向, 颜色1 位置1, 颜色2 位置2, ...)` 沿一条直线渐变。方向可用角度（`0deg` 向上、`90deg` 向右、`180deg` 向下）或关键字（`to right`/`to bottom right`）。位置用百分比或长度，相邻颜色位置相同可制造硬边。透明度用 `rgba()` 或 `#RRGGBBAA` 八位 hex。

## 实现方案
```css
:root {
  --color-primary: #5e6ad2;
  --color-secondary: #a8b1ff;
  --color-accent: #ff6b6b;
  --color-transparent: transparent;
}

/* ① 基础方向渐变 */
.c-gradient-down {
  background: linear-gradient(to bottom, var(--color-primary), var(--color-secondary));
}
.c-gradient-right {
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
}
.c-gradient-diagonal {
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
}

/* ② 多色渐变 */
.c-multi {
  background: linear-gradient(
    90deg,
    var(--color-primary) 0%,
    var(--color-secondary) 50%,
    var(--color-accent) 100%
  );
}

/* ③ 透明度渐变：fade 效果 */
.c-fade {
  background: linear-gradient(
    to bottom,
    rgba(94, 106, 210, 1) 0%,
    rgba(94, 106, 210, 0.5) 50%,
    rgba(94, 106, 210, 0) 100%
  );
}

/* ④ 硬边渐变：制造色块分割 */
.c-hard-line {
  background: linear-gradient(
    to right,
    var(--color-primary) 0% 50%,        /* 50% 处硬切换 */
    var(--color-secondary) 50% 100%
  );
}

/* ⑤ repeating-linear-gradient：条纹背景 */
.c-stripes {
  background: repeating-linear-gradient(
    45deg,
    var(--color-primary) 0,
    var(--color-primary) 10px,
    var(--color-secondary) 10px,
    var(--color-secondary) 20px
  );
}

/* ⑥ 按钮高光：双层渐变叠加 */
.c-btn-shine {
  background:
    linear-gradient(
      to bottom,
      rgba(255, 255, 255, 0.3) 0%,
      rgba(255, 255, 255, 0) 50%
    ),
    linear-gradient(var(--color-primary), var(--color-secondary));
}

/* ⑦ 渐变边框：border-image */
.c-gradient-border {
  border: 2px solid;
  border-image: linear-gradient(135deg, var(--color-primary), var(--color-accent)) 1;
}

/* ⑧ 渐变进度条：background-size 控制 */
.c-progress {
  background: linear-gradient(
    to right,
    var(--color-primary),
    var(--color-secondary)
  ) no-repeat;
  background-size: 50% 100%;              /* JS 控制宽度 */
  transition: background-size 0.3s var(--ease-out, ease-out);
}
```

## 执行步骤
1. 用 `linear-gradient(方向, 起始色, 结束色)` 创建基础渐变
2. 方向用角度（`90deg`）或关键字（`to right`），`135deg` 是常用对角方向
3. 多色渐变用逗号分隔多个 `颜色 位置` 节点
4. 透明度用 `rgba()` 或八位 hex（`#5e6ad2ff`/`#5e6ad200`）
5. 硬边色块：相邻颜色位置相同（`颜色1 50%, 颜色2 50%`）
6. 条纹用 `repeating-linear-gradient`，颜色位置循环
7. 多层渐变用逗号叠加，先写的在上层
8. 渐变边框用 `border-image: linear-gradient(...) 1`

## 兼容性
- Chrome: 26+
- Firefox: 16+
- Safari: 6.1+（部分需 `-webkit-`）
- Edge: 12+

## 降级方案
```css
/* 不支持渐变时降级到纯色 */
@supports not (background: linear-gradient(red, blue)) {
  .c-gradient-down {
    background: var(--color-primary);
  }
}

/* 八位 hex 不支持时降级到 rgba */
@supports not (background: #5e6ad200) {
  .c-fade {
    background: linear-gradient(
      to bottom,
      rgba(94, 106, 210, 1) 0%,
      rgba(94, 106, 210, 0) 100%
    );
  }
}

/* 老版浏览器前缀 */
@supports (-webkit-linear-gradient(red, blue)) and (not (linear-gradient(red, blue))) {
  .c-gradient-down {
    background: -webkit-linear-gradient(top, var(--color-primary), var(--color-secondary));
  }
}
```

## 相关链接
- [[radial-gradient-径向渐变]] - 圆形渐变
- [[conic-gradient-锥形渐变]] - 锥形渐变
- [[repeating渐变条纹]] - 条纹背景详解
- [[background-clip-文字渐变]] - 渐变文字
- [[00-MOC-渐变]]
