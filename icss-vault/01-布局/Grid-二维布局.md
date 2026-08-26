---
title: Grid 二维布局
type: technique
tags:
  - icss/01-布局/grid
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[Flex-对齐与分布]]"
  - "[[圣杯布局]]"
  - "[[容器查询-@container]]"
---

# Grid 二维布局

## 问题/场景
当布局同时涉及行和列两维方向（如仪表盘卡片墙、复杂表单、二维网格），Flex 一维布局力不从心。Grid 是 CSS 真正的二维布局系统，配合 `repeat()`、`auto-fit`、`minmax()` 可实现响应式卡片墙，无需媒体查询。

## 核心原理
Grid 通过 `grid-template-columns`/`grid-template-rows` 定义网格轨道。`repeat(n, size)` 重复定义，`auto-fit` 让列数随容器宽度自动调整，`minmax(min, max)` 限定每列尺寸区间，`1fr` 表示按比例分配剩余空间。`subgrid` 让嵌套 grid 继承父网格轨道，解决嵌套对齐难题。

## 实现方案
```css
:root {
  --gap-md: 16px;
  --min-card: 240px;
}

/* ① 响应式卡片墙：无需媒体查询 */
.c-card-wall {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(var(--min-card), 1fr));
  gap: var(--gap-md);
}

/* ② 经典三栏布局：header / sidebar / main / aside / footer */
.c-holy-grail {
  display: grid;
  grid-template:
    "header header header" auto
    "sidebar main  aside"  1fr
    "footer footer footer" auto
    / 200px 1fr 200px;
  gap: var(--gap-md);
  min-height: 100vh;
}
.c-holy-grail__header { grid-area: header; }
.c-holy-grail__sidebar { grid-area: sidebar; }
.c-holy-grail__main   { grid-area: main; min-width: 0; }
.c-holy-grail__aside  { grid-area: aside; }
.c-holy-grail__footer { grid-area: footer; }

/* ③ 等分多列 */
.c-equal-cols {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--gap-md);
}

/* ④ subgrid：嵌套继承父网格轨道 */
.c-parent {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--gap-md);
}
.c-child {
  display: grid;
  grid-template-columns: subgrid;       /* 继承父列轨道 */
  grid-column: span 3;
}

/* ⑤ 自适应行列：auto-flow dense 填补空隙 */
.c-masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  grid-auto-rows: 100px;
  grid-auto-flow: dense;                /* 自动填补空隙 */
  gap: var(--gap-md);
}
.c-masonry__item--tall { grid-row: span 2; }
```

## 执行步骤
1. 容器加 `display: grid`，子项成为 grid item
2. 用 `grid-template-columns: repeat(auto-fit, minmax(min, 1fr))` 实现响应式列数（容器够宽则多列，变窄自动减列）
3. 用 `grid-template-areas` 命名区域，配合 `grid-area` 让子项归位，可读性最强
4. 用 `gap` 替代 margin 控制行列间距
5. 嵌套对齐场景用 `subgrid` 让子网格继承父轨道，避免对齐错位
6. 卡片高度不一可用 `grid-auto-flow: dense` 自动填补空隙

## 兼容性
- Chrome: 57+（subgrid 117+）
- Firefox: 52+（subgrid 71+）
- Safari: 10.1+（subgrid 16+）
- Edge: 16+

## 降级方案
```css
/* subgrid 不支持时降级到独立 grid */
@supports not (grid-template-columns: subgrid) {
  .c-child {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--gap-md);
  }
}

/* grid 不支持时降级到 flex */
@supports not (display: grid) {
  .c-card-wall {
    display: flex;
    flex-wrap: wrap;
  }
  .c-card-wall > * {
    flex: 1 1 var(--min-card);
    margin: calc(var(--gap-md) / 2);
  }
}
```

## 相关链接
- [[Flex-对齐与分布]] - 一维布局优先用 Flex
- [[圣杯布局]] - Grid 实现三栏布局
- [[容器查询-@container]] - 配合 Grid 实现组件级响应式
- [[00-MOC-布局]]
