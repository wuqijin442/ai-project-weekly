---
title: Anchor Positioning 锚点定位
type: technique
tags:
  - icss/前沿特性/定位
  - 难度/高级
  - 兼容性/实验
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[position-try-智能边界]]"
  - "[[View-Transitions-API]]"
  - "[[scope-作用域]]"
---

# Anchor Positioning 锚点定位

## 问题/场景
传统绝对定位只能基于最近的 `position: relative` 父元素，无法跨容器定位。Tooltip/Popover 跟随触发按钮，通常需要 JS `getBoundingClientRect()` 计算坐标 + 监听 resize/scroll 修正。我们希望纯 CSS 实现「让一个元素相对另一个任意元素定位」。

## 核心原理
Anchor Positioning 让 CSS 原生具备「改变定位基准元素」的能力，替代 popper.js 的核心功能。

三个核心 API：
1. `anchor-name: --xxx`：给元素打上「锚点标签」
2. `position-anchor: --xxx`：让目标元素引用某个锚点
3. `anchor(--xxx bottom)`：在 `top`/`left` 中动态读取锚点的方位坐标
4. `anchor-size(width)`：继承锚点尺寸

定位逻辑：目标元素的 `top/left` 不再相对于父元素，而是相对锚点元素的方位。

## 实现方案

### 基础：Tooltip 跟随按钮

```css
:root {
  --tooltip-bg: #333;
  --tooltip-fg: #fff;
  --tooltip-gap: 5px;
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
}

/* ① 触发按钮：声明为锚点 */
.trigger-btn {
  anchor-name: --menu-anchor;
}

/* ② Tooltip：绑定锚点并定位 */
.tooltip {
  position: fixed;                      /* 必须 fixed/absolute */
  position-anchor: --menu-anchor;       /* 引用锚点 */
  top: anchor(--menu-anchor bottom);    /* 顶部对齐锚点底部 */
  left: anchor(--menu-anchor center);   /* 水平对齐锚点中心 */
  transform: translate(-50%, var(--tooltip-gap));  /* 居中 + 留间隙 */

  background: var(--tooltip-bg);
  color: var(--tooltip-fg);
  padding: 8px 12px;
  border-radius: 4px;
  transition: opacity 0.2s var(--ease-standard),
              transform 0.2s var(--ease-standard);
}
```

### 多按钮共享一个 Tooltip

```css
/* 两个按钮各声明锚点 */
.btn-a { anchor-name: --btn-a; }
.btn-b { anchor-name: --btn-b; }

/* hover A 时，Tooltip 绑定 A 锚点 */
.btn-a:hover ~ .tooltip {
  position-anchor: --btn-a;
  left: anchor(--btn-a center);
  top: anchor(--btn-a bottom);
}

/* hover B 时，Tooltip 绑定 B 锚点 */
.btn-b:hover ~ .tooltip {
  position-anchor: --btn-b;
  left: anchor(--btn-b center);
  top: anchor(--btn-b bottom);
}

.tooltip {
  position: fixed;
  transform: translate(-50%, var(--tooltip-gap));
  transition: all 0.2s var(--ease-standard);
}
```

### 尺寸继承：Popover 宽度跟随按钮

```css
.popover {
  position: absolute;
  position-anchor: --trigger;
  top: anchor(--trigger bottom);
  left: anchor(--trigger left);
  width: anchor-size(width);              /* 宽度 = 锚点宽度 */
  min-height: calc(anchor-size(height) * 1.5);  /* 最小高度 = 锚点 1.5 倍 */
}
```

### Popover API 配合

```css
/* 配合原生 Popover API：点击触发，自动管理显隐 */
.btn { anchor-name: --pop-trigger; }

.popover {
  position-anchor: --pop-trigger;
  top: anchor(--pop-trigger bottom);
  left: anchor(--pop-trigger center);
  transform: translate(-50%, 8px);
  /* popover 属性由 HTML 设置：popover="auto" */
}
```

## 方位参数速查

| 方向 | 参数 |
|------|------|
| 垂直 | `top` / `center` / `bottom` |
| 水平 | `left` / `center` / `right` |
| 组合 | `top-left` / `bottom-right` 等 |

## 执行步骤
1. **触发元素加 `anchor-name: --xxx`**：自定义名字，必须以 `--` 开头
2. **目标元素加 `position-anchor: --xxx`**：绑定锚点
3. **目标 `top`/`left` 用 `anchor()` 函数定位**：如 `top: anchor(--xxx bottom)`
4. **需要尺寸继承用 `anchor-size()`**：`width: anchor-size(width)`
5. **加 `@supports` 降级**：Firefox/Safari 不支持

## 兼容性
- Chrome: 125+
- Edge: 125+
- Firefox: 实验性（flag）
- Safari: 实验性

## 降级方案
```css
@supports not (anchor-name: --test) {
  /* 降级方案 1：固定父容器相对定位 */
  .trigger-wrapper { position: relative; }
  .tooltip {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translate(-50%, 5px);
  }
}

/* 降级方案 2：JS 计算坐标（popper.js / floating-ui） */
@supports not (anchor-name: --test) {
  /* 由 JS 接管定位逻辑 */
}
```

## 与传统方案对比
| 方案 | 是否需 JS | 跨容器 | 边界翻转 | 兼容性 |
|------|-----------|--------|----------|--------|
| 传统 absolute | 否 | 否 | 需 JS | 全部 |
| popper.js | 是 | 是 | 内置 | 全部 |
| floating-ui | 是 | 是 | 内置 | 全部 |
| Anchor Positioning | 否 | 是 | 配合 @position-try | Chrome 125+ |

## 应用场景
| 场景 | 锚点选择 | 定位方式 |
|------|----------|----------|
| Tooltip | 触发按钮 | `bottom` + `center` |
| 下拉菜单 | 触发按钮 | `bottom` + `left` |
| Popover | 触发元素 | `bottom` + `center` |
| 上下文菜单 | 鼠标位置 | 配合 JS 设锚点 |
| 表单错误提示 | 输入框 | `right` + `center` |

## 相关链接
- [[position-try-智能边界]]
- [[View-Transitions-API]]
- [[scope-作用域]]
- [[00-MOC-前沿特性]]
