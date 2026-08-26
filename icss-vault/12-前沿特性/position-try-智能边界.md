---
title: @position-try 智能边界
type: technique
tags:
  - icss/前沿特性/定位
  - 难度/高级
  - 兼容性/实验
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[Anchor-Positioning-锚点定位]]"
  - "[[scope-作用域]]"
---

# @position-try 智能边界

## 问题/场景
下拉菜单/Popover 在视口边缘时会被截断。floating-ui 等库提供「智能避让」：检测溢出后自动翻转方向。我们希望纯 CSS 实现这个能力，无需 JS 监听。

## 核心原理
`@position-try` 定义命名的「候补定位策略」。`position-try-fallbacks` 让目标元素按顺序尝试候补策略：先用默认定位，若溢出视口则按列表依次尝试，第一个不溢出的策略生效。

执行流程：
1. 浏览器应用默认定位（如锚点下方）
2. 检测元素是否溢出视口
3. 若溢出，按 `position-try-fallbacks` 列表尝试候补
4. 第一个不溢出的策略被采用
5. 全部溢出则回退默认定位

候补策略独立作用域，只覆盖指定属性，不影响元素其他样式。

## 实现方案

### 基础：上下翻转

```css
:root {
  --popover-gap: 8px;
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
}

/* 触发按钮 */
.btn { anchor-name: --trigger; }

/* ① 定义候补策略：翻转到上方 */
@position-try --position-top {
  top: anchor(--trigger top);          /* 改为锚点顶部 */
  bottom: unset;                        /* 清除原 bottom */
  margin-bottom: var(--popover-gap);
  margin-top: 0;
}

/* ② 默认在锚点下方，溢出时翻转到上方 */
.popover {
  position: absolute;
  position-anchor: --trigger;
  left: anchor(--trigger center);
  top: anchor(--trigger bottom);       /* 默认：锚点下方 */
  margin-top: var(--popover-gap);
  transform: translateX(-50%);
  position-try-fallbacks: --position-top;  /* 溢出时尝试上方 */

  transition: all 0.2s var(--ease-standard);
}
```

### 四方向翻转

```css
/* 四个方向的候补策略 */
@position-try --flip-top {
  top: anchor(--trigger top);
  bottom: anchor(--trigger bottom);
  margin: 0 0 var(--popover-gap) 0;
}
@position-try --flip-bottom {
  top: anchor(--trigger bottom);
  bottom: anchor(--trigger top);
  margin: var(--popover-gap) 0 0 0;
}
@position-try --flip-left {
  left: anchor(--trigger left);
  right: anchor(--trigger right);
  margin: 0 var(--popover-gap) 0 0;
}
@position-try --flip-right {
  left: anchor(--trigger right);
  right: anchor(--trigger left);
  margin: 0 0 0 var(--popover-gap);
}

/* 默认下方，依次尝试上方、左方、右方 */
.popover {
  position: absolute;
  position-anchor: --trigger;
  top: anchor(--trigger bottom);
  left: anchor(--trigger center);
  transform: translateX(-50%);
  margin-top: var(--popover-gap);

  position-try-fallbacks: --flip-top, --flip-left, --flip-right;
}
```

### 内置关键字

```css
/* CSS 提供内置翻转关键字 */
.popover {
  position: absolute;
  position-anchor: --trigger;
  top: anchor(--trigger bottom);
  left: anchor(--trigger center);

  /* flip-block: 上下翻转
     flip-inline: 左右翻转
     flip-start: 翻转到起点 */
  position-try-fallbacks: flip-block, flip-inline, flip-start;
}
```

### 配合 position-try-options 控制行为

```css
.popover {
  position: absolute;
  position-anchor: --trigger;
  top: anchor(--trigger bottom);
  position-try-fallbacks: --flip-top;

  /* always-try: 即使默认不溢出也尝试候补（用于动画切换） */
  position-try-order: most-height;  /* 优先选择空间最大的方向 */
}
```

## 执行步骤
1. **触发元素加 `anchor-name`**：参考 [[Anchor-Positioning-锚点定位]]
2. **目标元素默认定位**：如 `top: anchor(--trigger bottom)`
3. **用 `@position-try --name {}` 定义候补策略**：覆盖需要变化的属性
4. **目标元素加 `position-try-fallbacks: --name1, --name2`**：按顺序尝试
5. **测试边界**：把触发按钮放到视口各边缘，验证翻转

## 兼容性
- Chrome: 125+
- Edge: 125+
- Firefox: 不支持
- Safari: 不支持

## 降级方案
```css
@supports not (position-try-fallbacks: --test) {
  /* 降级方案 1：使用 floating-ui / popper.js JS 库 */
  /* JS 检测溢出并切换 class */

  /* 降级方案 2：用 :has() + 滚动检测，简单场景 */
  .popover {
    /* 固定在锚点下方，超出部分用 max-height + 滚动 */
    max-height: 50vh;
    overflow-y: auto;
  }
}

/* 渐进增强 */
@supports (position-try-fallbacks: --test) {
  .popover {
    position-try-fallbacks: --flip-top;
  }
}
```

## 与 floating-ui 对比
| 方案 | 实现方式 | 性能 | 兼容性 | 灵活性 |
|------|----------|------|--------|--------|
| floating-ui | JS 监听 resize/scroll | 中 | 全部 | 极高 |
| @position-try | 纯 CSS | 高（浏览器原生） | Chrome 125+ | 中 |
| 传统 fixed | CSS 固定 | 高 | 全部 | 低 |

## 关键技巧
| 技巧 | 用法 |
|------|------|
| 清除原属性 | 候补策略中用 `unset` 清除默认值 |
| 多策略顺序 | `--a, --b, --c` 依次尝试 |
| 内置关键字 | `flip-block`/`flip-inline` 简化常用翻转 |
| 选择空间最大 | `position-try-order: most-height` |
| 候补独立作用域 | 不影响元素其他样式 |

## 相关链接
- [[Anchor-Positioning-锚点定位]]
- [[scope-作用域]]
- [[00-MOC-前沿特性]]
