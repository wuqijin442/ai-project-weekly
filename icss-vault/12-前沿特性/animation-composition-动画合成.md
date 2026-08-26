---
title: animation-composition 动画合成
type: technique
tags:
  - icss/前沿特性/动画
  - 难度/高级
  - 兼容性/实验
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[CSS三角函数]]"
  - "[[路径动画×滚动驱动]]"
  - "[[transform-硬件加速]]"
---

# animation-composition 动画合成

## 问题/场景
多个动画同时操作 `transform` 时，后定义的会**覆盖**前者。例如 X、Y 两个方向位移动画并存，只有一个生效。传统做法是把元素包多层 div，每层只动一个 transform。我们希望一个元素同时承载多个 transform 动画。

## 核心原理
`animation-composition` 控制多个动画对**同一属性**的合成方式：

| 取值 | 含义 | 场景 |
|------|------|------|
| `replace`（默认） | 后动画替换前动画 | 普通覆盖 |
| `add` | 动画值追加 | 复合变换叠加（矩阵相乘） |
| `accumulate` | 动画值累加 | 多方向位移合成 |

执行流程：浏览器分别计算每个动画当前帧的值，再按合成模式合并。

`add` 与 `accumulate` 的细微差异：
- `add`：矩阵相乘，考虑旋转/缩放的复合影响
- `accumulate`：值直接相加，更适合纯位移合成

## 实现方案

### 碰撞反弹动画（X+Y 双方向合成）

```css
:root {
  --ball-size: 100px;
  --ball-color: #00e5ff;
}

.ball {
  position: absolute;
  width: var(--ball-size);
  height: var(--ball-size);
  border-radius: 50%;
  background: var(--ball-color);

  /* 两个动画同时驱动 transform */
  animation:
    horizontal 2.6s infinite linear alternate,
    vertical 1.9s infinite linear alternate;

  /* 关键：累加合成，让两个 translate 都生效 */
  animation-composition: accumulate;
}

/* X 方向位移：从左到右 */
@keyframes horizontal {
  from { transform: translateX(0); }
  to   { transform: translateX(calc(100vw - 100%)); }
}

/* Y 方向位移：从上到下 */
@keyframes vertical {
  from { transform: translateY(0); }
  to   { transform: translateY(calc(100vh - 100%)); }
}
```

### 配合颜色跳变模拟碰撞

```css
.ball {
  animation:
    horizontal 2.6s infinite linear alternate,
    vertical 1.9s infinite linear alternate,
    color-shift 26s infinite step-start;  /* 26s = 2.6s × 10 */
  animation-composition: accumulate;
}

/* 每 2.6s 跳变一次色相，模拟碰撞变色 */
@keyframes color-shift {
  0%   { filter: hue-rotate(0deg); }
  10%  { filter: hue-rotate(36deg); }
  20%  { filter: hue-rotate(72deg); }
  30%  { filter: hue-rotate(108deg); }
  40%  { filter: hue-rotate(144deg); }
  50%  { filter: hue-rotate(180deg); }
  60%  { filter: hue-rotate(216deg); }
  70%  { filter: hue-rotate(252deg); }
  80%  { filter: hue-rotate(288deg); }
  90%  { filter: hue-rotate(324deg); }
  100% { filter: hue-rotate(360deg); }
}
```

### 三种合成模式对比

```css
/* replace（默认）：后动画覆盖前动画，只剩 vertical */
.demo-replace {
  animation: x 2s, y 2s;
  animation-composition: replace;  /* 只看到 Y 方向移动 */
}

/* add：矩阵相乘，旋转+缩放会相互影响 */
.demo-add {
  animation: rotate 2s, scale 2s;
  animation-composition: add;  /* 旋转和缩放复合 */
}

/* accumulate：值累加，纯位移最直观 */
.demo-accumulate {
  animation: x 2s, y 2s;
  animation-composition: accumulate;  /* X+Y 都生效 */
}
```

### 多动画分别设置合成模式

```css
.complex {
  animation:
    moveX 2s infinite alternate,
    moveY 1.5s infinite alternate,
    spin 3s infinite linear;
  /* 分别设置：前两个累加，第三个替换 */
  animation-composition: accumulate, accumulate, replace;
}
```

## 执行步骤
1. **写多个 @keyframes**：每个动画只动一个 transform 维度（X/Y/旋转/缩放）
2. **元素 `animation` 列出所有动画**：用逗号分隔
3. **设置 `animation-composition: accumulate`**：让 transform 值累加
4. **时长不一致制造随机感**：X 用 2.6s、Y 用 1.9s，循环后伪随机
5. **`alternate` 实现反弹**：到达终点自动回弹

## 兼容性
- Chrome: 112+
- Edge: 112+
- Firefox: 不支持
- Safari: 不支持

## 降级方案
```css
@supports not (animation-composition: accumulate) {
  /* 降级方案 1：多层 div 嵌套，每层一个 transform 动画 */
  .ball-wrapper {
    animation: horizontal 2.6s infinite linear alternate;
  }
  .ball-wrapper .ball {
    animation: vertical 1.9s infinite linear alternate;
  }

  /* 降级方案 2：JS 用 requestAnimationFrame 驱动 */
}
```

## 关键技巧
| 技巧 | 用法 | 效果 |
|------|------|------|
| 时长互质 | X=2.6s, Y=1.9s | 伪随机运动轨迹 |
| `alternate` 反弹 | `animation-direction: alternate` | 到达边界自动回弹 |
| `100%` 代替硬编码 | `translateX(100%)` | 通用性更强（`%` 是元素自身尺寸） |
| `step-start` 跳变 | 颜色动画用步进 | 突变效果，模拟碰撞 |
| 三个动画合成 | X+Y+color | 复杂运动+变色 |

## 应用场景
| 场景 | 动画组合 | 合成模式 |
|------|----------|----------|
| 弹球碰撞 | X+Y 位移 | accumulate |
| 行星轨道 | 旋转+缩放 | add |
| 摇摆飘落 | 旋转+位移 | accumulate |
| 心跳脉冲 | 缩放+颜色 | replace |
| 复合变换 | 多 transform | accumulate |

## 相关链接
- [[CSS三角函数]]
- [[路径动画×滚动驱动]]
- [[transform-硬件加速]]
- [[00-MOC-前沿特性]]
