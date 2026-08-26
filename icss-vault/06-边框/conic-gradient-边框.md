---
title: conic-gradient 渐变边框
type: technique
tags:
  - icss/边框/conic-gradient
  - 难度/高级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[clip-path-多边形]]"
  - "[[hue-rotate-色相旋转]]"
---

# conic-gradient 渐变边框

## 问题/场景
需要实现渐变边框（彩虹边框、四色边框、流光动画边框）。`border-color` 不支持渐变，`border-image` 兼容性与圆角冲突。最佳方案是用 `conic-gradient`/`linear-gradient` 做背景 + `mask` 抠出中空边框，实现真正的渐变边框且支持圆角。

## 核心原理
**conic-gradient（圆锥渐变）**：颜色沿圆心环绕分布，从 12 点钟方向顺时针展开。语法：
```css
background: conic-gradient(from 起始角 at 圆心, 颜色1 角度, 颜色2 角度, ...);
```

**mask 抠边框原理**：
1. 元素背景填满整个盒子（渐变色）
2. 用两层 `mask`：一层是 `content-box`（内容区，含 padding），一层是 `border-box`（整个盒子）
3. 用 `mask-composite: exclude`（差集）让两层相减，只保留边框区域
4. 结果：渐变只显示在边框环上，中间镂空

**关键属性**：
- `mask` / `-webkit-mask`：定义遮罩
- `mask-composite` / `-webkit-mask-composite`：遮罩合成方式
  - `exclude` / `xor`：差集（两层不同时存在的部分）
  - `intersect`：交集
- `padding: 2px`：边框宽度由 padding 决定

## 实现方案

```css
:root {
  --border-width: 2px;
  --color-card-bg: #ffffff;
  --rainbow: conic-gradient(
    from 0deg,
    #ff004c, #ff8a00, #ffe600, #4cff00, #00ffc8, #008cff, #6a00ff, #ff004c
  );
  --four-color: conic-gradient(
    from 45deg,
    #ff4d4f 0 25%, #1890ff 0 50%, #52c41a 0 75%, #faad14 0 100%
  );
}

/* 场景一：彩虹渐变边框（带圆角） */
.rainbow-border {
  position: relative;
  width: 240px;
  height: 120px;
  border-radius: 16px;
  background: var(--rainbow);
  padding: var(--border-width);
  /* mask 抠出中空：content-box 与 border-box 差集 */
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
}

/* 场景二：四色边框（每边一色） */
.four-color-border {
  width: 200px;
  height: 100px;
  border-radius: 12px;
  background: var(--four-color);
  padding: var(--border-width);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
}

/* 场景三：流光动画边框（hue-rotate 让彩虹转动） */
.animated-border {
  width: 240px;
  height: 120px;
  border-radius: 16px;
  background: var(--rainbow);
  padding: var(--border-width);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  animation: hue-spin 4s linear infinite;
  will-change: filter;
}

@keyframes hue-spin {
  to { filter: hue-rotate(360deg); }
}

/* 场景四：线性渐变边框（更简单） */
.linear-gradient-border {
  width: 200px;
  height: 80px;
  border-radius: 8px;
  background: linear-gradient(135deg, #1890ff, #36cfc9, #1890ff);
  padding: var(--border-width);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
}

/* 场景五：hover 边框变粗 */
.grow-border {
  width: 200px;
  height: 80px;
  border-radius: 12px;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  padding: 1px;
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  transition: padding 0.3s ease;     /* 边框宽度即 padding，可动画 */
}
.grow-border:hover {
  padding: 3px;
}

/* 场景六：暗黑模式适配 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-card-bg: #1f1f1f;
  }
  .animated-border {
    animation-duration: 6s;          /* 暗色放慢，减少刺激 */
  }
}

@media (prefers-reduced-motion: reduce) {
  .animated-border { animation: none; }
}
```

## 执行步骤
1. 用 `conic-gradient` 画圆锥渐变作为背景（彩虹色环绕分布）
2. 设置 `padding` 等于边框宽度，这是边框粗细的来源
3. 用两层 `mask`：第一层 `linear-gradient(#fff 0 0) content-box` 覆盖内容区，第二层覆盖整个盒子
4. `mask-composite: exclude`（Safari 用 `-webkit-mask-composite: xor`）让两层做差集，只留边框环
5. 渐变只在边框环显示，中间透明，露出底层内容
6. 流光动画：给元素加 `filter: hue-rotate(360deg)` 关键帧，颜色循环流转
7. hover 变粗：动画 `padding`（边框宽度），配合 `transition`
8. 暗黑模式放慢动画时长，降低视觉刺激

## 兼容性
- `conic-gradient`：Chrome 69+、Firefox 83+、Safari 12.1+
- `mask-composite`：Chrome 120+（标准）、Firefox 53+
- `-webkit-mask-composite: xor`：Safari 4+、Chrome（旧版前缀）
- 移动端：iOS Safari 12.2+、Android Chrome 69+
- `mask-composite` 标准属性较新，务必同时写 `-webkit-` 前缀保证兼容

## 降级方案
```css
/* 不支持 mask-composite 时退回双层盒子方案 */
@supports not (mask-composite: exclude) {
  .rainbow-border {
    -webkit-mask: none;
    mask: none;
    background: var(--color-card-bg);  /* 退回纯色背景 */
    border: 2px solid #1890ff;          /* 退回纯色边框 */
  }
}

/* 不支持 conic-gradient 时退回 linear-gradient */
@supports not (background: conic-gradient(red, blue)) {
  .rainbow-border {
    background: linear-gradient(135deg, #f36, #f90, #fc3, #3f6, #36f);
  }
}

/* 兼容写法：同时写前缀与标准 */
.rainbow-border {
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
}
```

## 相关链接
- [[clip-path-多边形]] - clip-path 与 conic-gradient 配合做复杂形状
- [[hue-rotate-色相旋转]] - hue-rotate 让 conic-gradient 流动
- [[border-image-边框图像]] - 另一种渐变边框方案（但有圆角限制）
- [[00-MOC-边框]]
