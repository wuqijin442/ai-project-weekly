---
title: contain 包含上下文隔离重排
type: technique
tags:
  - icss/性能/渲染优化
  - 难度/高级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[content-visibility]]"
  - "[[will-change]]"
  - "[[transform-硬件加速]]"
---

# contain 包含上下文隔离重排

## 问题/场景
页面里某个组件内部变化（比如一个卡片内部状态更新），浏览器重新计算了整个页面的布局。我们希望组件内部变化只影响组件自身，不要扩散到外部。

## 核心原理
`contain` 属性告诉浏览器：「这个元素的某些方面独立于页面其他部分，变化时不需要重新计算外部」。浏览器会跳过对应范围的工作。

`contain` 有四个取值，对应四种隔离：
- `layout`：隔离布局，元素内部布局变化不影响外部
- `paint`：隔离绘制，元素内容不会溢出到外部（类似 `overflow: hidden`）
- `size`：元素尺寸不受内容影响（必须显式给尺寸，否则尺寸为 0）
- `style`：隔离样式（counter、quote 等）

简写：`contain: layout paint` 同时隔离布局和绘制。`contain: strict` = `size layout paint`，`contain: content` = `layout paint`。

## 实现方案

```css
:root {
  --card-padding: 16px;
}

/* ✅ 基础用法：隔离卡片的布局和绘制 */
.card {
  contain: layout paint;
  padding: var(--card-padding);
}

/* ✅ 严格隔离：尺寸也独立（必须显式给尺寸） */
.card--strict {
  contain: strict;  /* 等于 size layout paint */
  width: 300px;
  height: 200px;
}

/* ✅ 内容隔离：布局+绘制（最常用） */
.card--content {
  contain: content;  /* 等于 layout paint */
}

/* 实战：列表项隔离，内部状态变化不影响其他项 */
.list-item {
  contain: layout paint style;
  /* 内部 hover、展开、动画都只影响自身 */
}

/* 实战：第三方组件沙箱 */
.third-party-widget {
  contain: layout paint style;
  /* 第三方代码的布局变化不会影响宿主页面 */
}
```

### 严格 containment 的副作用与应对

```css
/* ⚠️ contain: size 会让元素尺寸为 0，除非显式设置 */
.bad { contain: size; }  /* 元素高度变 0，内容消失 */

.good {
  contain: size;
  height: 200px;  /* 必须显式给尺寸 */
}
```

## 执行步骤
1. **找出频繁变化的组件**：内部有 hover、展开、动画、数据更新的卡片
2. **加 `contain: layout paint`**：隔离布局和绘制，最安全
3. **需要尺寸独立时再加 `size`**：但要确保元素有显式尺寸
4. **加 `style` 隔离 counter/quote**：第三方组件建议加
5. **DevTools 验证**：Rendering 面板勾选 Paint Flashing，看变化是否只局限在组件内

## 兼容性
- Chrome: 52+（layout/paint/style），85+（size 严格模式）
- Firefox: 69+
- Safari: 15.4+

## 降级方案
```css
@supports not (contain: layout paint) {
  /* 老浏览器：用 overflow:hidden + position:relative 模拟 paint 隔离 */
  .card {
    position: relative;
    overflow: hidden;
  }
  /* layout 隔离无法完全模拟，但 overflow 能限制绘制范围 */
}

/* 渐进增强：优先用 contain，老浏览器降级 */
.card {
  position: relative;
  overflow: hidden;  /* 基础绘制隔离 */
}

@supports (contain: layout paint) {
  .card {
    contain: layout paint;
    overflow: visible;  /* contain 接管，不再需要 overflow */
  }
}
```

## 各取值适用场景
| 取值 | 隔离范围 | 适用场景 | 副作用 |
|------|----------|----------|--------|
| `layout` | 布局 | 内部布局变化的组件 | 无 |
| `paint` | 绘制 | 防止内容溢出 | 类似 overflow:hidden |
| `size` | 尺寸 | 固定尺寸容器 | 元素尺寸为 0 |
| `style` | 样式 | counter/quote 隔离 | 无 |
| `strict` | size+layout+paint | 完全独立容器 | 需显式尺寸 |
| `content` | layout+paint | 通用组件隔离 | 无 |

## 相关链接
- [[content-visibility]]
- [[will-change]]
- [[transform-硬件加速]]
- [[00-MOC-性能]]
