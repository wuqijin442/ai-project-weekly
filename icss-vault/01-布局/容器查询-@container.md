---
title: 容器查询 @container
type: technique
tags:
  - icss/01-布局/容器查询
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[Grid-二维布局]]"
  - "[[Flex-对齐与分布]]"
---

# 容器查询 @container

## 问题/场景
传统 `@media` 媒体查询基于**视口宽度**响应，但同一个组件在不同位置（侧边栏 300px、主区域 800px）显示效果应不同。组件应基于**自身容器宽度**响应，而非视口。容器查询让组件真正实现「随用随适配」。

## 核心原理
父容器声明 `container-type: inline-size` 后成为查询容器，子元素用 `@container (min-width: 400px)` 查询容器宽度。容器查询单位 `cqw`（1cqw = 容器宽度 1%）、`cqi`（容器内联尺寸 1%）替代 `vw`/`vi`，让组件内字号、间距随容器变化。

## 实现方案
```css
:root {
  --gap-sm: 8px;
  --gap-md: 16px;
}

/* ① 声明查询容器 */
.c-card-container {
  container-type: inline-size;          /* 按内联尺寸（宽度）建立容器 */
  container-name: card;                 /* 命名容器（可选） */
}

/* ② 容器查询：根据容器宽度切换布局 */
@container card (min-width: 400px) {
  .c-card {
    display: grid;
    grid-template-columns: 120px 1fr;
    gap: var(--gap-md);
  }
}

@container card (max-width: 399px) {
  .c-card {
    display: flex;
    flex-direction: column;
    gap: var(--gap-sm);
  }
}

/* ③ 容器查询单位：字号随容器变化 */
.c-card__title {
  font-size: clamp(1rem, 5cqi, 2rem);   /* 5cqi = 容器宽度的 5% */
  line-height: 1.4;
}

.c-card__body {
  font-size: clamp(0.875rem, 3cqi, 1.125rem);
  padding: 2cqw;                         /* 内边距随容器变化 */
}

/* ④ style() 查询：基于容器自定义状态 */
.c-tabs {
  container-type: inline-size;
  --variant: row;                        /* 默认横向 */
}
@container style(--variant: column) {
  .c-tabs__list { flex-direction: column; }
}
```

## 执行步骤
1. 在组件**最外层容器**加 `container-type: inline-size`，声明其为查询容器
2. （可选）用 `container-name` 命名，避免多个容器查询互相干扰
3. 子元素用 `@container 名称 (条件)` 编写响应式规则，语法类似 `@media`
4. 字号/间距改用 `cqw`/`cqi` 单位，组件即随容器宽度自适应缩放
5. 用 `clamp(min, preferred, max)` 限定上下限，避免极端值
6. 同一组件可被复用在侧边栏、主区域、对话框等不同宽度场景，无需写多套样式

## 兼容性
- Chrome: 105+
- Firefox: 110+
- Safari: 16+
- Edge: 105+
- `style()` 查询：Chrome 111+ / Firefox 仍实验性

## 降级方案
```css
/* 容器查询不支持时降级到媒体查询（组件复用性受限） */
@supports not (container-type: inline-size) {
  .c-card {
    display: flex;
    flex-direction: column;
  }
  @media (min-width: 768px) {
    .c-card {
      display: grid;
      grid-template-columns: 120px 1fr;
    }
  }
  .c-card__title { font-size: 1.25rem; }
}
```

## 相关链接
- [[Grid-二维布局]] - Grid + 容器查询组合实现组件响应式
- [[Flex-对齐与分布]] - 容器内 Flex 布局切换
- [[00-MOC-布局]]
- [[00-MOC-现代特性]] - 容器查询单位详解
