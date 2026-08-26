---
title: subgrid 子网格
type: technique
tags:
  - icss/现代特性/布局
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[容器查询单位]]"
  - "[[scope-作用域]]"
  - "[[CSS嵌套]]"
---

# subgrid 子网格

## 问题/场景
嵌套网格中，子网格的列宽无法与父网格对齐。比如一个表单：外层 grid 定义了「标签列 + 输入框列」，里面再嵌套一个 grid 时，子 grid 的列宽和父对不齐，视觉错位。传统做法是子网格用相同的列宽定义，但响应式时容易脱节。

## 核心原理
`grid-template-columns: subgrid`（或 `grid-template-rows: subgrid`）让子网格**直接继承父网格的轨道定义**，包括列宽、行高、gap。子网格的列就是父网格的列，无论父怎么调整，子自动对齐。

注意：subgrid 继承的是父的**轨道尺寸**，不是父的全部网格属性。子网格仍可以独立设置 `align-items`/`justify-items`。

## 实现方案

### 嵌套网格列对齐

```css
:root {
  --label-width: 120px;
  --gap: 16px;
}

/* ① 父网格定义列宽 */
.form {
  display: grid;
  grid-template-columns: var(--label-width) 1fr;
  gap: var(--gap);
}

/* ② 子网格继承父列宽 */
.form-row {
  display: grid;
  grid-template-columns: subgrid;  /* 继承父的 120px 1fr */
  grid-column: 1 / -1;             /* 跨父网格全部列 */
  gap: var(--gap);                 /* 可继承也可重写 */
}

/* ③ 三层嵌套也能对齐 */
.form-row .nested-group {
  display: grid;
  grid-template-columns: subgrid;
  grid-column: 2 / -1;             /* 只占父的第二列 */
}
```

### 卡片列表跨行跨列对齐

```css
/* 父网格：4 列卡片栅格 */
.gallery {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

/* 某个卡片跨 2 列，内部再分 2 列与父对齐 */
.gallery .featured {
  grid-column: span 2;
  display: grid;
  grid-template-columns: subgrid;
  /* 子网格的 2 列就是父网格的 2 列，宽度完全一致 */
}

.gallery .featured .sub-card {
  /* 自动对齐父网格的列 */
}
```

### 跨行对齐标题区

```css
/* 父网格：行结构 */
.layout {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 24px;
  min-height: 100vh;
}

/* 子网格继承父行高 */
.layout .main {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: 2 / -1;
}
```

## 执行步骤
1. **父网格定义清晰轨道**：`grid-template-columns: 120px 1fr`
2. **子项设置 `grid-column: 1 / -1`**：占满父网格全部列（或需要的范围）
3. **子项加 `grid-template-columns: subgrid`**：继承父轨道
4. **gap 自动继承**：子网格默认继承父 gap，也可显式覆盖
5. **多层嵌套逐级 subgrid**：每层都继承上一层

## 兼容性
- Chrome: 117+
- Firefox: 71+
- Safari: 16+

## 降级方案
```css
/* 老浏览器：手动复制父列宽定义 */
.form-row {
  display: grid;
  grid-template-columns: var(--label-width) 1fr;  /* 与父一致 */
  gap: var(--gap);
}

@supports (grid-template-columns: subgrid) {
  .form-row {
    grid-template-columns: subgrid;  /* 用 subgrid，自动对齐 */
  }
}

/* 缺点：父列宽改变时，子必须同步更新（用 CSS 变量缓解） */
```

## 应用场景
| 场景 | 用法 |
|------|------|
| 表单标签对齐 | 标签列宽度一致跨多行 |
| 卡片网格跨列 | 跨列卡片内部对齐父列 |
| 表格分组 | 分组行对齐表头列 |
| 仪表盘布局 | 嵌套模块对齐外部网格 |
| 时间轴 | 嵌套时间块对齐时间列 |

## 与传统方案对比
| 方案 | 优点 | 缺点 |
|------|------|------|
| subgrid | 自动对齐父轨道 | 兼容性 2023+ |
| 复制列宽 | 全兼容 | 父变要同步子 |
| Flex 等宽 | 简单 | 无法精确对齐 |
| CSS 变量传递 | 部分缓解 | 仍需手动同步 |

## 相关链接
- [[容器查询单位]]
- [[scope-作用域]]
- [[CSS嵌套]]
- [[00-MOC-现代特性]]
