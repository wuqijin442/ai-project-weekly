---
title: CSS 原生嵌套语法
type: technique
tags:
  - icss/现代特性/语法
  - 难度/初级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[scope-作用域]]"
  - "[[容器查询单位]]"
---

# CSS 原生嵌套语法

## 问题/场景
写 BEM 命名的组件时，要重复写父类名：`.card { } .card__title { } .card--active .card__title { }`。代码冗长且层级关系不清晰。Sass/Less 用嵌套解决了，但需要构建工具。我们希望原生 CSS 就能嵌套。

## 核心原理
CSS Nesting Module 让原生 CSS 支持嵌套规则，子选择器自动以父选择器为前缀。`&` 显式引用父选择器，可用于复合选择器、伪类、伪元素等场景。

与 Sass 嵌套的关键差异：
- `&` 必须出现在复合选择器开头（如 `&.active`），不能写 `.active &`
- 不识别时直接报错（Sass 静默处理）
- 编译产物更精简（无构建步骤）

## 实现方案

```css
:root {
  --card-bg: #fff;
  --card-bg-hover: #f5f5f5;
  --card-padding: 16px;
}

/* ✅ 基础嵌套 */
.card {
  background: var(--card-bg);
  padding: var(--card-padding);

  /* 子元素自动以 .card 为父 */
  .title {
    font-size: 1.2rem;
    font-weight: 600;
  }

  .content {
    color: #666;
  }
}

/* ✅ 用 & 引用父选择器 */
.card {
  /* 伪类：& 引用 .card */
  &:hover {
    background: var(--card-bg-hover);
  }

  /* 复合选择器：&.active */
  &.is-active {
    border-color: #007bff;
  }

  /* 伪元素 */
  &::before {
    content: '';
    display: block;
  }

  /* 后代组合：& > .title 与 .title 等价 */
  & > .title {
    margin-bottom: 8px;
  }

  /* 兄弟组合 */
  & + .card {
    margin-top: 12px;
  }
}

/* ✅ 媒体查询嵌套 */
.card {
  font-size: 1rem;

  @media (min-width: 768px) {
    font-size: 1.2rem;
    padding: 24px;
  }
}

/* ✅ 容器查询嵌套 */
.sidebar {
  container-type: inline-size;

  .widget {
    font-size: 0.9rem;

    @container (min-width: 400px) {
      font-size: 1rem;
      display: grid;
    }
  }
}

/* ✅ 与 @scope 配合限定作用域 */
@scope (.card) to (.card-content) {
  .title { font-weight: 600; }
}
```

## 执行步骤
1. **检查目标浏览器**：Chrome 112+、Safari 16.5+、Firefox 117+ 全支持
2. **替换 Sass 嵌套**：直接复制 Sass 嵌套结构到 CSS，`&` 用法基本兼容
3. **注意 `&` 位置**：必须出现在复合选择器开头，否则语法错误
4. **生产环境加 @supports 检测**：老浏览器降级到展开写法

## 兼容性
- Chrome: 112+
- Firefox: 117+
- Safari: 16.5+

## 降级方案
```css
/* 老浏览器：展开为传统写法 */
.card { background: var(--card-bg); padding: var(--card-padding); }
.card .title { font-size: 1.2rem; font-weight: 600; }
.card .content { color: #666; }
.card:hover { background: var(--card-bg-hover); }
.card.is-active { border-color: #007bff; }

/* 现代浏览器用嵌套，配合 PostCSS 自动降级 */
@supports selector(&) {
  .card {
    &:hover { background: var(--card-bg-hover); }
    .title { font-weight: 600; }
  }
}
```

## 与 Sass 嵌套的差异
| 差异点 | Sass | 原生 CSS |
|--------|------|----------|
| `&` 位置 | 任意位置 | 必须在复合选择器开头 |
| 不识别处理 | 静默 | 报错 |
| @at-root | 支持 | 不支持 |
| 占位符选择器 % | 支持 | 不支持 |
| 构建步骤 | 需要 | 不需要 |

## 相关链接
- [[scope-作用域]]
- [[容器查询单位]]
- [[00-MOC-现代特性]]
