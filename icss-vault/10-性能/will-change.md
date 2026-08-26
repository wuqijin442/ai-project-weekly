---
title: will-change 提示浏览器优化
type: technique
tags:
  - icss/性能/硬件加速
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[transform-硬件加速]]"
  - "[[content-visibility]]"
  - "[[contain-包含上下文]]"
---

# will-change 提示浏览器优化

## 问题/场景
动画刚开始的几帧会卡顿（掉帧、抖动）。原因是浏览器没提前准备，第一帧才开始创建图层、分配 GPU 内存，开销最大。我们希望动画一开始就丝滑。

## 核心原理
`will-change` 是个「提前告知」属性，告诉浏览器：「这个元素接下来要变化这几个属性，请你提前做好优化准备（创建合成层、预分配内存、准备 GPU 路径）」。这样动画真正开始时，浏览器已经准备好了，第一帧就丝滑。

但 `will-change` 不能常驻：每个 `will-change` 都会创建一个独立的合成层（layer），常驻会消耗大量内存，导致 **layer explosion（图层爆炸）**。

正确做法：动画即将开始前设置 `will-change`，动画结束后立即移除。

## 实现方案

```css
:root {
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --duration-standard: 0.3s;
}

/* ❌ 错误：常驻 will-change，会导致 layer explosion */
.bad-example {
  will-change: transform, opacity;  /* 永远占用 GPU 资源 */
}

/* ✅ 正确：只在 hover 时启用 will-change */
.card {
  transition: transform var(--duration-standard) var(--ease-standard),
              opacity var(--duration-standard) var(--ease-standard);
}

/* 鼠标移入时提前预热（鼠标进入 → 点击/移动有几毫秒延迟，刚好预热） */
.card:hover {
  will-change: transform;
}

/* 动画结束后通过 JS 移除 will-change，或用 :not(:hover) 自动移除 */
.card:not(:hover) {
  will-change: auto;
}
```

```javascript
// 进阶：动画结束后立即移除 will-change
const el = document.querySelector('.animated');
el.addEventListener('mouseenter', () => {
  el.style.willChange = 'transform, opacity';
});
el.addEventListener('transitionend', () => {
  el.style.willChange = 'auto';
});
```

## 执行步骤
1. **识别即将开始的动画**：通常是 hover、focus、scroll 触发
2. **在动画前的状态设置 `will-change`**：如 `:hover` 时设置，给浏览器几十毫秒预热
3. **动画结束后立即移除**：用 `:not(:hover)` 或 JS `transitionend` 事件移除
4. **不要常驻**：常驻等于每个元素都建图层，内存爆炸

## 兼容性
- Chrome: 36+
- Firefox: 36+
- Safari: 9.1+

## 降级方案
```css
/* 老浏览器不识别 will-change，用 transform: translateZ(0) 强制创建图层 */
@supports not (will-change: transform) {
  .card:hover {
    transform: translateZ(0);  /* hack：触发 GPU 层 */
  }
}

/* 现代浏览器用 will-change，老浏览器用 translateZ(0) */
```

## 使用建议
| 场景 | 推荐做法 |
|------|----------|
| 频繁触发的 hover 动画 | `:hover` 时设 `will-change` |
| 一次性入场动画 | 入场前 100ms 用 JS 设置，结束后移除 |
| 滚动视差 | 进入滚动区域前设置，离开后移除 |
| 大量元素同时动画 | 不要每个都设，只设最关键的几个 |

## 相关链接
- [[transform-硬件加速]]
- [[content-visibility]]
- [[contain-包含上下文]]
- [[00-MOC-性能]]
