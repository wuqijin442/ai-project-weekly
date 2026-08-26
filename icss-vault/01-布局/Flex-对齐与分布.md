---
title: Flex 对齐与分布
type: technique
tags:
  - icss/01-布局/flex
  - 难度/初级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[Grid-二维布局]]"
  - "[[等高布局方案]]"
  - "[[圣杯布局]]"
---

# Flex 对齐与分布

## 问题/场景
日常开发最高频的布局需求：水平垂直居中、等间距分布、文本溢出省略、子项自适应伸缩。Flex 布局一维方向上几乎能解决所有排列问题，但 `min-width: 0` 文本溢出坑、`gap` 间距控制、`flex` 缩写语义混淆是常见踩点。

## 核心原理
Flex 容器有主轴（main axis）和交叉轴（cross axis）两根轴。`justify-content` 控制主轴对齐，`align-items` 控制交叉轴对齐。子项的 `flex` 缩写等价于 `flex-grow flex-shrink flex-basis`，默认 `0 1 auto`。`min-width: auto` 是默认值，会导致 flex 子项内容（如长文本/表格）撑破容器，必须显式置 `0` 才能正确触发溢出省略。

## 实现方案
```css
:root {
  --gap-sm: 8px;
  --gap-md: 16px;
  --color-text: #333;
  --color-border: #ddd;
}

/* ① 水平垂直居中：三件套 */
.c-center {
  display: flex;
  justify-content: center;   /* 主轴居中 */
  align-items: center;       /* 交叉轴居中 */
}

/* ② 等间距分布 + gap 替代 margin */
.c-space-between {
  display: flex;
  justify-content: space-between;  /* 两端对齐，等间距 */
  gap: var(--gap-md);              /* 用 gap 控制间距，避免 margin 折叠 */
}

/* ③ flex 缩写：grow shrink basis */
.c-flex-1   { flex: 1; }      /* = 1 1 0%，等分剩余空间 */
.c-flex-auto { flex: auto; }  /* = 1 1 auto，按内容大小伸缩 */
.c-flex-none { flex: none; }  /* = 0 0 auto，不伸缩 */

/* ④ 文本溢出省略：必须 min-width: 0 */
.c-ellipsis {
  display: flex;
  gap: var(--gap-sm);
}
.c-ellipsis__text {
  min-width: 0;               /* 关键：覆盖默认 min-width: auto */
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

/* ⑤ Flex 方向切换：导航栏横排 / 移动端纵排 */
.c-nav {
  display: flex;
  flex-direction: row;        /* 默认横排 */
  flex-wrap: wrap;            /* 允许换行 */
}
@media (max-width: 768px) {
  .c-nav { flex-direction: column; }
}
```

## 执行步骤
1. 容器加 `display: flex`，子项自动成为 flex item，沿主轴排列
2. 用 `justify-content` 控制主轴对齐方式（居中/两端/分散）
3. 用 `align-items` 控制交叉轴对齐（默认 `stretch` 即等高效果）
4. 用 `gap` 替代 margin 控制子项间距，避免外边距合并问题
5. 长文本子项务必加 `min-width: 0`，否则会撑破容器导致省略号失效
6. 用 `flex: 1` 让子项等分剩余空间，`flex: none` 固定大小不伸缩

## 兼容性
- Chrome: 29+
- Firefox: 28+
- Safari: 9+（`gap` 需 14.1+）
- Edge: 12+

## 降级方案
```css
/* gap 不支持时降级到 margin */
@supports not (gap: 8px) {
  .c-space-between > * + * {
    margin-left: var(--gap-md);
  }
}

/* 老版浏览器 flex 前缀 */
@supports not (display: flex) {
  .c-center {
    display: table-cell;
    text-align: center;
    vertical-align: middle;
  }
}
```

## 相关链接
- [[Grid-二维布局]] - 二维布局场景改用 Grid
- [[等高布局方案]] - Flex 默认 stretch 即天然等高
- [[圣杯布局]] - 三栏布局的现代实现
- [[00-MOC-布局]]
