---
title: @scope 作用域规则
type: technique
tags:
  - icss/现代特性/作用域
  - 难度/中级
  - 兼容性/渐进
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[CSS嵌套]]"
  - "[[容器查询单位]]"
  - "[[scope-作用域]]"
---

# @scope 作用域规则

## 问题/场景
BEM 命名（`.card__title`）是为了避免样式污染，但写起来啰嗦。`:where()`/`:is()` 能降低优先级但不能限定作用范围。我们希望样式只在某个 DOM 子树内生效，超出范围不污染。

## 核心原理
`@scope` 规则定义样式的「作用范围」：从某个根元素开始，到某个边界元素结束（不含边界内的子树）。语法：

```css
@scope (根选择器) to (边界选择器) {
  /* 这里的样式只作用于根到边界之间 */
  .title { ... }
}
```

- 不写 `to` 时，作用域从根一直到所有后代
- 写 `to` 时，边界元素及其后代不应用样式
- `:scope` 引用当前作用域根元素

与 BEM 的区别：BEM 靠命名约定，`@scope` 靠浏览器原生作用域。与 `:where()` 配合可控制优先级。

## 实现方案

### 基础：限定卡片样式作用域

```css
:root {
  --card-accent: #007bff;
}

/* 限定 .card 内的 .title 样式，不影响其他 .title */
@scope (.card) {
  .title {
    color: var(--card-accent);
    font-weight: 600;
  }

  .content {
    color: #666;
  }

  /* :scope 引用 .card 自身 */
  :scope {
    padding: 16px;
    border: 1px solid #eee;
  }
}
```

### 带边界：避免污染嵌套组件

```css
/* .media 内的样式不影响 .media 内嵌套的 .card */
@scope (.media) to (.card) {
  .title {
    font-size: 1.5rem;
    /* 这个样式不会应用到 .card 内的 .title */
  }

  img {
    width: 100%;
  }
}
```

### 与 :where() 配合控制优先级

```css
/* 用 :where() 让作用域内样式零优先级，便于覆盖 */
@scope (.card) {
  :where(.title) {
    color: #333;  /* 优先级 0,0,1,0，容易被覆盖 */
  }
}

/* 默认样式优先级低，主题样式可覆盖 */
.theme-dark .card .title {
  color: #fff;  /* 优先级 0,0,2,1，覆盖 :where() 版本 */
}
```

### 替代 BEM 的写法

```css
/* 传统 BEM */
.card { ... }
.card__title { ... }
.card__content { ... }
.card--active .card__title { ... }

/* @scope 等价写法 */
@scope (.card) {
  :scope { ... }                                   /* .card */
  .title { ... }                                   /* .card__title */
  .content { ... }                                 /* .card__content */
  :scope.is-active .title { ... }                  /* .card--active .card__title */
}
```

### 多根作用域

```css
/* 多个根选择器，用逗号分隔 */
@scope (.card, .panel, .modal) {
  .title {
    font-weight: 600;
  }
}
```

## 执行步骤
1. **找出需要限定范围的样式**：通常是组件级样式
2. **用 `@scope (根) { ... }` 包裹**：根通常是组件容器选择器
3. **嵌套组件加 `to (边界)`**：避免污染第三方组件
4. **配合 `:where()` 降优先级**：让样式易于覆盖
5. **渐进增强**：老浏览器降级到 BEM

## 兼容性
- Chrome: 118+
- Firefox: 实验性（128+ 部分支持）
- Safari: 17.4+

## 降级方案
```css
/* 老浏览器：用 BEM 命名约定 */
.card { padding: 16px; border: 1px solid #eee; }
.card .title { color: var(--card-accent); font-weight: 600; }
.card .content { color: #666; }

/* 现代浏览器用 @scope，更精确 */
@supports selector(@scope (.test)) {
  @scope (.card) {
    .title { color: var(--card-accent); font-weight: 600; }
  }
}
```

## 与其他作用域方案对比
| 方案 | 作用范围 | 优先级 | 浏览器 |
|------|----------|--------|--------|
| BEM 命名 | 全局但命名隔离 | 普通选择器 | 全部 |
| Shadow DOM | 真正隔离 | 隔离 | 现代浏览器 |
| `@scope` | DOM 子树 | 普通选择器 | Chrome 118+/Safari 17.4+ |
| `:where()` | 全局 | 零优先级 | 现代浏览器 |

## 应用场景
| 场景 | 用法 |
|------|------|
| 组件样式隔离 | `@scope (.card) { ... }` |
| 避免污染第三方 | `@scope (.page) to (.ad) { ... }` |
| 替代 BEM | `:scope` + `.title` 等价 `.card__title` |
| 主题切换 | 配合 `:where()` 易覆盖 |
| 内容区域限定 | `@scope (.article) to (.no-style)` |

## 相关链接
- [[CSS嵌套]]
- [[容器查询单位]]
- [[00-MOC-现代特性]]
