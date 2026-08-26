---
title: "@layer 层级管控"
type: technique
tags:
  - icss/选择器/layer
  - 难度/高级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[is-where-选择器分组]]"
  - "[[has-父选择器]]"
---

# @layer 层级管控

## 问题/场景
引入第三方 UI 库（Element UI、Ant Design）时，其样式优先级难以控制：用 `!important` 污染全局、用高特异性选择器越写越长、reset 样式被业务覆盖。`@layer` 提供「层级（cascade layer）」机制，让样式按层分组，层间优先级清晰可控。

## 核心原理
`@layer` 声明命名层级，CSS 规则归入不同层。**层间优先级由声明顺序决定：后声明的层优先级更高**（与直觉相反）。未分层的样式优先级高于所有层。

**层级优先级排序**（从低到高）：
1. `@layer` 第一声明的层（最低）
2. `@layer` 后声明的层
3. …
4. `@layer` 最后声明的层
5. **未分层的样式（最高）**

**`!important` 在 @layer 中反转**：
- 普通规则：后层 > 前层 > 未分层
- `!important` 规则：**前层 > 后层 > 未分层**（优先级反转，先声明的层 `!important` 最强）

这个反转设计保证：框架层用 `!important` 时，业务层（后声明）的普通规则仍能覆盖框架的普通规则，但框架的 `!important` 仍可被业务的 `!important` 覆盖。

## 实现方案

```css
/* ① 声明层级顺序：先声明的优先级低 */
@layer reset, framework, components, utilities;

/* ② reset 层：最低优先级，用 :where() 配合零特异性 */
@layer reset {
  :where(h1, h2, h3, p, ul, ol) {
    margin: 0;
    padding: 0;
  }
  :where(a) {
    color: inherit;
    text-decoration: none;
  }
  :where(img) {
    max-width: 100%;
    display: block;
  }
}

/* ③ framework 层：第三方库样式归入此层 */
@layer framework {
  /* 假装是 Ant Design 的样式 */
  .ant-btn {
    padding: 8px 16px;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    background: #fff;
  }
}

/* ④ components 层：业务组件样式 */
@layer components {
  .btn-primary {
    background: var(--color-primary, #1890ff);
    color: #fff;
    border-color: var(--color-primary, #1890ff);
  }
  /* 因为 components 层在 framework 之后，优先级更高，可覆盖 ant-btn */
  .ant-btn.is-custom {
    border-radius: 8px;
  }
}

/* ⑤ utilities 层：工具类，最高层，可覆盖一切 */
@layer utilities {
  .u-text-center { text-align: center; }
  .u-mt-16 { margin-top: 16px; }
  .u-hidden { display: none; }
}

/* ⑥ 未分层样式：优先级最高，用于紧急覆盖 */
.btn-emergency {
  background: #ff4d4f !important;
}

/* ⑦ 暗黑模式：仅改 CSS 变量，层结构不变 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #177ddc;
  }
  @layer framework {
    .ant-btn {
      background: #1f1f1f;
      border-color: #434343;
      color: rgba(255, 255, 255, 0.85);
    }
  }
}
```

**第三方样式归入层**（用 `@import` 的 `layer` 参数）：
```css
/* 把第三方 CSS 整体归入 framework 层 */
@import url('antd.css') layer(framework);
@import url('normalize.css') layer(reset);
```

## 执行步骤
1. 在文件开头用 `@layer reset, framework, components, utilities;` 声明层级顺序（仅声明，不写规则）
2. 顺序至关重要：先声明的优先级低，后声明的优先级高，与书写顺序一致
3. 把 reset 样式放入 `reset` 层，配合 `:where()` 双重保证零特异性，绝不干扰业务
4. 用 `@import url('xxx.css') layer(framework);` 把第三方库整体归入 framework 层
5. 业务组件样式放入 `components` 层，因层序在后，可干净覆盖 framework
6. 工具类放 `utilities` 层（最高层），确保 `.u-hidden` 等总能生效
7. 紧急覆盖用未分层样式（优先级最高），或 `!important`（注意层内反转规则）
8. 暗黑模式只需在各层内用 `@media` 改 CSS 变量，层结构保持不变

## 兼容性
- Chrome: 99+
- Firefox: 97+
- Safari: 15.4+
- Edge: 99+
- 移动端：iOS Safari 15.4+、Android Chrome 99+
- 全球支持率约 95%

## 降级方案
```css
/* 不支持 @layer 时，浏览器忽略 @layer 声明，规则按普通顺序生效 */
/* 此时需保证书写顺序：reset → framework → components → utilities */
@supports not (at-rule: "@layer") {
  /* 退回传统特异性管理：用 :where() 控制 reset 特异性，
     用选择器精度控制业务覆盖，避免 !important 污染 */
}

/* 实际降级策略：@layer 被忽略后，CSS 仍按源码顺序生效，
   只要书写顺序合理，多数情况能正常工作。
   仅当依赖「层序覆盖高特异性选择器」时会失效，
   此时退回用 :where() 降低第三方样式特异性。 */
@layer framework {
  /* 若浏览器不支持，这块等价于普通 .ant-btn 规则 */
  .ant-btn { /* ... */ }
}
```

## 相关链接
- [[is-where-选择器分组]] - :where() 在 @layer reset 中的零特异性配合
- [[has-父选择器]] - :has() 在 @layer 内的优先级
- [[nth-child-奇技淫巧]] - :nth-child 归入层的优先级
- [[00-MOC-选择器]]
