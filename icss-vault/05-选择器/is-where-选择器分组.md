---
title: ":is()/:where() 选择器分组"
type: technique
tags:
  - icss/选择器/is-where
  - 难度/初级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[has-父选择器]]"
  - "[[layer-层级管控]]"
---

# :is() / :where() 选择器分组

## 问题/场景
传统写法中，给多个不同父级下的同一元素加相同样式，要写一长串重复选择器：`header h1, main h1, footer h1, aside h1 { ... }`。冗长难维护，且特异性计算复杂。`:is()` 和 `:where()` 让选择器分组变得简洁，且 `:where()` 提供零特异性，是写 reset 样式的利器。

## 核心原理
两者都接收一个选择器列表，匹配其中任意一个选中的元素。

**语法**：
```css
:is(选择器1, 选择器2, ...) { /* 公共样式 */ }
:where(选择器1, 选择器2, ...) { /* 公共样式 */ }
```

**唯一区别——特异性**：
| 函数 | 特异性 | 用途 |
|------|--------|------|
| `:is()` | 取参数中**最高**特异性 | 简化选择器，保持原有优先级 |
| `:where()` | **永远为 0** | 写 reset/默认样式，方便后续覆盖 |

**`:is()` 特异性举例**：
- `:is(#nav, .list) a` → 特异性为 `#nav a` 的最高值（1,0,1）
- `:where(#nav, .list) a` → 特异性始终为 `(0,0,1)`，仅 `a` 自身

**容错性**：两者都忽略参数中无效的选择器（不像传统逗号分组会整条失效）。

## 实现方案

```css
:root {
  --color-link: #1890ff;
  --color-link-hover: #40a9ff;
  --color-heading: #1a1a1a;
}

/* 场景一：用 :is() 简化冗长选择器 */
/* 传统写法：header h1, header h2, main h1, main h2, footer h1, footer h2 { } */
:is(header, main, footer) :is(h1, h2) {
  color: var(--color-heading);
  font-weight: 700;
}

/* 场景二：用 :where() 写零特异性 reset */
:where(h1, h2, h3, h4, h5, h6) {
  margin: 0;                     /* 特异性 0，任意 .title 都能覆盖 */
  font-size: inherit;
}
:where(ul, ol) {
  list-style: none;
  padding: 0;
  margin: 0;
}
:where(a) {
  color: inherit;
  text-decoration: none;
}

/* 业务样式可轻松覆盖 reset（因 reset 是 0 特异性） */
.title { font-size: 32px; }      /* 覆盖 :where(h1) 的 font-size:inherit */
.nav-link { color: var(--color-link); }  /* 覆盖 :where(a) 的 color:inherit */

/* 场景三：配合 :has() 进一步简化 */
.card:has(.card-img) :is(.card-title, .card-desc) {
  padding-inline: 16px;
}

/* 场景四：容错性——忽略无效选择器 */
/* :is(:unknown-pseudo, .valid) 不会整条失效，.valid 仍生效 */
:is(.btn, :unknown-pseudo) {
  cursor: pointer;
}

/* 场景五：暗黑模式主题色 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-heading: #f0f0f0;
    --color-link: #40a9ff;
    --color-link-hover: #69b1ff;
  }
}
```

## 执行步骤
1. 用 `:is()` 把多个父级或多个子元素合并：`:is(header, main, footer) :is(h1, h2)` 比传统逗号写法短得多
2. 写 reset 样式时用 `:where()`，确保特异性为 0，业务样式能轻松覆盖
3. 理解 `:is()` 取最高特异性：`:is(#nav, .list)` 的特异性等同 `#nav`，可能比预期高
4. 利用容错性：`:is()` 内有无效选择器不会让整条规则失效，比传统逗号分组更健壮
5. 配合 `:has()` 用：`:has()` 内部可放 `:is()` 进一步简化
6. 嵌套深度控制：`:is()` 可拍平多层嵌套，保持选择器不超 3 层

## 兼容性
- Chrome: 88+（`:is()`）/ 88+（`:where()`）
- Firefox: 78+ / 78+
- Safari: 14+ / 14+
- Edge: 88+ / 88+
- 移动端：iOS Safari 14+、Android Chrome 88+
- 全球支持率超 95%

## 降级方案
```css
/* 不支持 :is()/:where() 时退回传统逗号分组 */
@supports not selector(:is(*)) {
  header h1, header h2,
  main h1, main h2,
  footer h1, footer h2 {
    color: var(--color-heading);
    font-weight: 700;
  }
}

@supports not selector(:where(*)) {
  h1, h2, h3, h4, h5, h6 {
    margin: 0;
    font-size: inherit;
  }
}
```

## 相关链接
- [[has-父选择器]] - :has() 内部配合 :is() 简化选择器
- [[layer-层级管控]] - :where() 在 @layer reset 中的应用
- [[nth-child-奇技淫巧]] - :is() 配合 :nth-child 简化
- [[00-MOC-选择器]]
