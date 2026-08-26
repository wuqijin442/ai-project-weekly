---
title: ":has() 父选择器"
type: technique
tags:
  - icss/选择器/has
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[is-where-选择器分组]]"
  - "[[filter-滤镜组合]]"
---

# :has() 父选择器

## 问题/场景
CSS 长期只能「父选子」（`.parent .child`），无法「子选父」。常见痛点：表单含必填项时给整个表单加红色边框、卡片 hover 时联动改变标题颜色、列表中含图片的项加内边距。这些以往必须靠 JS 加 class，现在 `:has()` 让 CSS 原生实现「父选择器」。

## 核心原理
`:has()` 是 CSS Selectors Level 4 引入的「关系伪类」，匹配**包含符合条件后代**的元素。它让选择器从「向下找」变成「向上回溯」。

语法：
```css
父元素:has(后代选择器) { /* 父元素样式 */ }
```

**关键特性**：
- `:has()` 参数可以是任意复杂选择器（含后代、兄弟、伪类）
- 可链式：`:has(img):has(.title)` 同时满足两个条件
- 可组合：`.card:has(.badge:hover)` 后代 badge hover 时选中 card
- **特异性**：`:has()` 自身为 0 特异性，取参数中最高特异性

**性能提示**：`:has()` 需要浏览器回溯检查 DOM，深层嵌套或长列表上慎用。Chrome 105+ 已做大量优化，但仍建议限制使用范围。

## 实现方案

```css
:root {
  --color-danger: #ff4d4f;
  --color-success: #52c41a;
  --color-card-border: #e8e8e8;
  --color-card-hover: #1890ff;
}

/* 场景一：表单必填校验高亮整个表单 */
.form:has(input:required:invalid) {
  border: 2px solid var(--color-danger);
  border-radius: 8px;
  padding: 16px;
}
/* 表单全部通过校验时变绿 */
.form:has(input:required:valid) {
  border-color: var(--color-success);
}

/* 场景二：卡片 hover 联动标题变色 */
.card {
  border: 1px solid var(--color-card-border);
  border-radius: 8px;
  padding: 16px;
  transition: border-color 0.3s ease;
}
/* 卡片 hover 时，标题颜色联动变化 */
.card:has(.card-title):hover .card-title {
  color: var(--color-card-hover);
}
/* 卡片内含图片时，整体增加内边距 */
.card:has(img) {
  padding: 24px;
}

/* 场景三：列表项根据内容自适应 */
.list-item:has(.tag-hot) {
  background: linear-gradient(90deg, rgba(255,77,79,0.08), transparent);
}
/* 含「已售罄」标记的商品变灰 */
.product:has(.sold-out) {
  filter: grayscale(0.8) opacity(0.6);
  pointer-events: none;
}

/* 场景四：根据兄弟元素状态选择 */
/* 输入框获得焦点时，前面的 label 高亮 */
input:focus ~ label,
label:has(+ input:focus) {
  color: var(--color-card-hover);
}

/* 场景五：模态框打开时禁用 body 滚动 */
body:has(.modal.is-open) {
  overflow: hidden;
}

/* 场景六：暗黑模式联动 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-card-border: #3a3a3a;
    --color-card-hover: #40a9ff;
  }
}
```

## 执行步骤
1. 表单校验：用 `:has(input:required:invalid)` 选中含未通过必填项的表单，加红边框
2. 全部通过时 `:has(input:required:valid)` 变绿，实现纯 CSS 校验反馈
3. 卡片联动：`.card:has(.card-title):hover .card-title` 实现 hover 卡片时标题变色
4. 内容自适应：`.card:has(img)` 给含图片的卡片加内边距，无需 JS 判断
5. 兄弟选择：`label:has(+ input:focus)` 选中后面紧跟聚焦 input 的 label
6. 全局联动：`body:has(.modal.is-open)` 模态打开时锁 body 滚动，替代 JS 加 class
7. 限制范围：`:has()` 不要用在数千项的长列表上，回溯检查开销大

## 兼容性
- Chrome: 105+（2022 年 8 月起）
- Edge: 105+
- Safari: 15.4+（2022 年 3 月起）
- Firefox: 121+（2023 年 12 月起全面支持）
- 移动端：iOS Safari 15.4+、Android Chrome 105+
- 全球浏览器支持率已超 90%

## 降级方案
```css
/* 不支持 :has() 时，用 JS 加 fallback class */
@supports not selector(:has(*)) {
  .form.is-invalid {
    border: 2px solid var(--color-danger);
  }
  .card.is-hovered .card-title {
    color: var(--color-card-hover);
  }
}
```

```html
<!-- JS 降级：监听 input 状态加 class -->
<script>
  if (!CSS.supports('selector(:has(*))')) {
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('input', () => {
        const valid = form.querySelector('input:required:invalid');
        form.classList.toggle('is-invalid', !!valid);
      });
    });
  }
</script>
```

## 相关链接
- [[is-where-选择器分组]] - :has() 内部可配合 :is() 简化
- [[filter-滤镜组合]] - :has() 触发 filter 状态变化
- [[layer-层级管控]] - :has() 在 @layer 中的优先级
- [[00-MOC-选择器]]
