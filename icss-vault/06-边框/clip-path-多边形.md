---
title: clip-path 多边形
type: technique
tags:
  - icss/边框/clip-path
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[不规则边框-drop-shadow]]"
  - "[[圆角与形状]]"
---

# clip-path 多边形

## 问题/场景
需要把元素裁剪成三角形、梯形、六边形、星形等任意形状，或做形状变形动画（hover 时从矩形变箭头）。传统 `border-radius` 只能做圆角，`overflow: hidden` 只能矩形裁剪。`clip-path` 用矢量路径裁剪元素，是任意形状的终极方案。

## 核心原理
`clip-path` 用一个裁剪路径定义元素的可见区域，路径外的部分完全不渲染（透明、不可点击）。支持四种基本形状函数：

| 函数 | 语法 | 用途 |
|------|------|------|
| `polygon()` | `polygon(0 0, 100% 0, 50% 100%)` | 任意多边形（最常用） |
| `circle()` | `circle(50% at 50% 50%)` | 圆形 |
| `ellipse()` | `ellipse(50% 30% at 50% 50%)` | 椭圆 |
| `inset()` | `inset(10% round 8px)` | 矩形内缩（带圆角） |
| `path()` | `path('M0,0 L100,0...')` | SVG 路径（最灵活） |

**坐标系统**：`0 0` 是左上角，`100% 100%` 是右下角，可混用 px/%。

**与 `overflow: hidden` 区别**：
| 特性 | `overflow: hidden` | `clip-path` |
|------|---------------------|-------------|
| 形状 | 仅矩形 | 任意形状 |
| 子元素溢出 | 裁剪 | 裁剪 |
| 阴影跟随 | 矩形 | 跟随路径 |
| 动画 | 不支持 | 支持路径插值 |

**动画关键点**：`clip-path` 动画要求起止状态的**点数完全一致**，否则无法插值。用 `polygon()` 时，变形前后点数要相同。

## 实现方案

```css
:root {
  --color-primary: #1890ff;
  --color-card-bg: #ffffff;
  --color-shadow: rgba(0, 0, 0, 0.15);
}

/* 场景一：三角形 */
.triangle-up {
  width: 100px;
  height: 100px;
  background: var(--color-primary);
  clip-path: polygon(50% 0, 100% 100%, 0 100%);  /* 顶点在上中，底边在下 */
}
.triangle-right {
  clip-path: polygon(0 0, 100% 50%, 0 100%);     /* 箭头朝右 */
}

/* 场景二：梯形（带斜边） */
.trapezoid {
  width: 200px;
  height: 80px;
  background: var(--color-primary);
  clip-path: polygon(20% 0, 80% 0, 100% 100%, 0 100%);
}

/* 场景三：六边形 */
.hexagon {
  width: 120px;
  height: 138px;                 /* 高 = 宽 × √3/2 × 2 ≈ 1.155 */
  background: var(--color-primary);
  clip-path: polygon(50% 0, 100% 25%, 100% 75%, 50% 100%, 0 75%, 0 25%);
}

/* 场景四：星形 */
.star {
  width: 100px;
  height: 100px;
  background: var(--color-primary);
  clip-path: polygon(
    50% 0%, 61% 35%, 98% 35%, 68% 57%,
    79% 91%, 50% 70%, 21% 91%, 32% 57%,
    2% 35%, 39% 35%
  );
}

/* 场景五：圆形与椭圆 */
.circle-shape {
  clip-path: circle(50% at 50% 50%);
}
.ellipse-shape {
  clip-path: ellipse(60% 40% at 50% 50%);
}

/* 场景六：内缩圆角矩形（替代 overflow:hidden + border-radius） */
.inset-rounded {
  clip-path: inset(10% round 16px);
}

/* 场景七：hover 形状变形动画（矩形 → 箭头） */
.btn-arrow {
  width: 160px;
  height: 48px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  /* 起始：矩形（5 个点，与箭头点数一致） */
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 0 50%);
  transition: clip-path 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: clip-path;
}
.btn-arrow:hover {
  /* 终止：箭头（5 个点，点数一致才能插值） */
  clip-path: polygon(0 0, 80% 0, 100% 50%, 80% 100%, 0 100%);
}

/* 场景八：用 path() 做 SVG 路径裁剪 */
.svg-path-shape {
  clip-path: path('M10,10 Q50,0 90,10 T90,90 L10,90 Z');
}

/* 场景九：暗黑模式适配 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #177ddc;
    --color-card-bg: #1f1f1f;
    --color-shadow: rgba(0, 0, 0, 0.5);
  }
}

/* 尊重减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
  .btn-arrow {
    transition: none;
  }
}
```

## 执行步骤
1. 确定形状的关键顶点坐标，用 `polygon()` 按顺时针或逆时针依次列出
2. 三角形只需 3 个点，六边形 6 个点，星形 10 个点（5 角 × 2）
3. `circle(半径 at 圆心x 圆心y)` 做正圆，`ellipse(横向半径 纵向半径 at ...)` 做椭圆
4. `inset(内缩量 round 圆角)` 是矩形内缩带圆角，可替代 `overflow:hidden + border-radius`
5. 形状变形动画：起止状态用相同点数的 `polygon()`，浏览器自动插值
6. 若点数不一致，用占位点补齐（如在矩形加一个 `0 50%` 的点，与箭头的尖端对应）
7. 复杂曲线用 `path()` 传 SVG 路径字符串，但 `path()` 不支持动画插值
8. 暗黑模式仅改 CSS 变量颜色，形状不变

## 兼容性
- `clip-path` 基本形状：Chrome 55+、Firefox 54+、Safari 11+（部分需 `-webkit-`）
- `path()`：Chrome 88+、Firefox 71+、Safari 13.1+
- `clip-path` 动画：Chrome 55+、Firefox 54+、Safari 11+
- 移动端：iOS Safari 11+、Android Chrome 55+
- `path()` 动画插值兼容性较差，建议用 `polygon()` 做动画

## 降级方案
```css
/* 不支持 clip-path 时退回 overflow:hidden + border-radius */
@supports not ((clip-path: polygon(0 0)) or (-webkit-clip-path: polygon(0 0))) {
  .hexagon {
    /* 退回普通圆角矩形 */
    border-radius: 8px;
    overflow: hidden;
  }
  .btn-arrow:hover {
    /* 退回普通 hover 颜色变化 */
    background: var(--color-primary);
    opacity: 0.85;
  }
}

/* 兼容旧版 Safari */
.hexagon {
  -webkit-clip-path: polygon(50% 0, 100% 25%, 100% 75%, 50% 100%, 0 75%, 0 25%);
  clip-path: polygon(50% 0, 100% 25%, 100% 75%, 50% 100%, 0 75%, 0 25%);
}
```

## 相关链接
- [[不规则边框-drop-shadow]] - 用 drop-shadow 为 clip-path 形状加阴影
- [[圆角与形状]] - border-radius 做简单形状，clip-path 做复杂形状
- [[conic-gradient-边框]] - clip-path 与渐变边框配合
- [[00-MOC-边框]]
