---
title: View Transitions API
type: technique
tags:
  - icss/前沿特性/过渡
  - 难度/高级
  - 兼容性/实验
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[Anchor-Positioning-锚点定位]]"
  - "[[路径动画×滚动驱动]]"
  - "[[animation-composition-动画合成]]"
---

# View Transitions API

## 问题/场景
SPA 切换页面/状态时，元素位置变化没有过渡动画，体验生硬。传统做法用 FLIP 技术（First-Last-Invert-Play）+ JS 计算位置差，代码复杂。跨页面（MPA）跳转更无法过渡。我们希望原生 CSS 提供状态过渡能力。

## 核心原理
View Transitions API 让浏览器在两个 DOM 状态间自动生成过渡动画：
1. JS 调用 `document.startViewTransition(callback)`
2. 浏览器截图当前状态（旧快照）
3. 执行 callback 更新 DOM（新状态）
4. 浏览器截图新状态
5. 用 `::view-transition-*` 伪元素在两个快照间做动画

CSS 端核心：
- `view-transition-name: xxx`：给元素命名，让浏览器知道新旧状态是同一元素
- `::view-transition-old(xxx)` / `::view-transition-new(xxx)`：旧/新快照伪元素
- `::view-transition-group(xxx)`：包含新旧快照的容器
- `::view-transition-root`：根容器

跨文档（MPA）过渡：Chrome 115+ 支持同源跨页面过渡，配合 `@view-transition` 规则。

## 实现方案

### 基础：SPA 状态过渡

```css
:root {
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --duration-standard: 0.3s;
}

/* ① 给需要过渡的元素命名 */
.card-image {
  view-transition-name: card-image;
}

.card-title {
  view-transition-name: card-title;
}

/* ② 默认过渡动画（可选，浏览器有默认） */
::view-transition-old(card-image) {
  animation: fade-out var(--duration-standard) var(--ease-standard);
}

::view-transition-new(card-image) {
  animation: fade-in var(--duration-standard) var(--ease-standard);
}

@keyframes fade-out {
  to { opacity: 0; }
}
@keyframes fade-in {
  from { opacity: 0; }
}
```

```javascript
// ③ JS 触发过渡
function updateCard(newData) {
  // 不支持时直接更新（降级）
  if (!document.startViewTransition) {
    renderCard(newData);
    return;
  }
  // 支持时：包裹在过渡中
  document.startViewTransition(() => {
    renderCard(newData);
  });
}
```

### 列表项展开/收起过渡

```css
.list-item {
  view-transition-name: var(--vt-name);  /* 动态命名 */
}

/* 展开时给当前项命名 */
.list-item.is-expanded {
  view-transition-name: expanded-item;
}

/* 过渡：旧位置 → 新位置平滑移动 */
::view-transition-group(expanded-item) {
  animation-duration: 0.4s;
  animation-timing-function: var(--ease-standard);
}
```

```javascript
function expandItem(item) {
  document.startViewTransition(() => {
    // 移除其他项的展开状态
    document.querySelectorAll('.list-item.is-expanded')
      .forEach(el => el.classList.remove('is-expanded'));
    // 展开当前项
    item.classList.add('is-expanded');
  });
}
```

### 共享元素过渡（列表 → 详情）

```css
/* 列表中的图片 */
.list-card .thumb {
  view-transition-name: thumb--list;
}

/* 详情页图片（同名，浏览器自动过渡） */
.detail .thumb {
  view-transition-name: thumb--list;
}

/* 浏览器自动计算两个位置的 transform/size 差异并动画 */
```

### 跨页面过渡（MPA）

```css
/* 在所有页面声明启用跨文档过渡 */
@view-transition {
  navigation: auto;  /* 启用同源跨页面过渡 */
}

/* 给跨页面共享元素命名 */
.site-header {
  view-transition-name: site-header;
}

.site-logo {
  view-transition-name: site-logo;
}
```

### 自定义过渡方向

```css
/* 旧元素向左滑出，新元素从右滑入 */
::view-transition-old(slide) {
  animation: slide-out-left var(--duration-standard) var(--ease-standard);
}
::view-transition-new(slide) {
  animation: slide-in-right var(--duration-standard) var(--ease-standard);
}

@keyframes slide-out-left {
  to { transform: translateX(-100%); opacity: 0; }
}
@keyframes slide-in-right {
  from { transform: translateX(100%); opacity: 0; }
}
```

### 排除元素过渡

```css
/* 不参与过渡的元素 */
.background-deco {
  view-transition-name: none;  /* 默认就是 none */
}

/* 整个根过渡禁用 */
::view-transition-root {
  display: none;
}
```

## 执行步骤
1. **给需要过渡的元素加 `view-transition-name: xxx`**：名字必须唯一
2. **JS 用 `document.startViewTransition(callback)` 包裹状态更新**：callback 内修改 DOM
3. **可选：自定义 `::view-transition-old/new` 动画**：默认是淡入淡出
4. **跨页面过渡加 `@view-transition { navigation: auto; }`**：MPA 场景
5. **检测 `document.startViewTransition` 是否存在**：降级直接更新 DOM

## 兼容性
- SPA 状态过渡：Chrome 111+/Edge 111+/Safari 18+/Firefox 不支持
- 跨文档过渡（MPA）：Chrome 115+/Edge 115+/Safari 18+/Firefox 不支持

## 降级方案
```javascript
// JS 端：检测并降级
function safeUpdate(updateFn) {
  if (!document.startViewTransition) {
    // 老浏览器：直接更新，无过渡
    updateFn();
    return;
  }
  document.startViewTransition(updateFn);
}
```

```css
/* CSS 端：降级过渡用 transition 模拟 */
@supports not (view-transition-name: test) {
  .card-image {
    transition: transform 0.3s, opacity 0.3s;
  }
  /* 老浏览器：用传统 transition，无法精确过渡位置变化 */
}
```

## ::view-transition-* 伪元素层级
```
::view-transition-root
  └─ ::view-transition-group(name)        # 位置/尺寸变化容器
       ├─ ::view-transition-image-pair(name)
       │    ├─ ::view-transition-old(name)  # 旧快照
       │    └─ ::view-transition-new(name)  # 新快照
```

## 应用场景
| 场景 | 命名策略 | 动画类型 |
|------|----------|----------|
| 列表→详情 | 共享元素同名 | 位置/尺寸过渡 |
| 卡片展开 | 动态命名 | 高度过渡 |
| 主题切换 | 全局过渡 | 淡入淡出 |
| 拖拽排序 | 列表项命名 | 位置交换 |
| 跨页面跳转 | 共享 header/logo | MPA 过渡 |

## 关键技巧
| 技巧 | 用法 |
|------|------|
| 唯一命名 | 同一时刻只能有一个元素用某名字 |
| 动态命名 | 用 CSS 变量 `view-transition-name: var(--vt-name)` |
| 共享过渡 | 新旧位置同 name，浏览器自动算 transform |
| 自定义动画 | 覆盖 `::view-transition-old/new` |
| 禁用过渡 | `view-transition-name: none` |

## 相关链接
- [[Anchor-Positioning-锚点定位]]
- [[路径动画×滚动驱动]]
- [[animation-composition-动画合成]]
- [[00-MOC-前沿特性]]
