---
title: hue-rotate 色相旋转
type: technique
tags:
  - icss/滤镜/色相
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[filter-滤镜组合]]"
  - "[[conic-gradient-边框]]"
---

# hue-rotate 色相旋转

## 问题/场景
需要实现彩虹流光边框、彩色文字呼吸、加载动画的色相循环。手动写多个关键帧颜色太繁琐，`hue-rotate` 滤镜可让一个基础色相沿色环旋转 360°，配合动画实现自动变色。

## 核心原理
`hue-rotate(deg)` 是 `filter` 的一个函数，将元素所有像素的色相（HSL 中的 H）按指定角度沿色环旋转。0deg 不变，360deg 回到原色，180deg 取补色。

**色环旋转规律**：
- 红色（0°）旋转 120° → 绿色
- 红色（0°）旋转 240° → 蓝色
- 旋转 360° 回到红色

**关键技巧**：只需定义一个基础彩色（如 `conic-gradient` 的红→黄→绿→蓝），用 `hue-rotate` 动画从 0deg 到 360deg，就能让整个渐变循环流转，无需写多帧颜色。配合 `conic-gradient`（圆锥渐变）可做彩虹圆环。

**性能提示**：`hue-rotate` 计算量中等，单元素动画可接受；避免大面积应用。动画时声明 `will-change: filter`。

## 实现方案

```css
:root {
  --rainbow-gradient: conic-gradient(
    from 0deg,
    #ff004c, #ff8a00, #ffe600, #4cff00, #00ffc8, #008cff, #6a00ff, #ff004c
  );
  --anim-duration: 4s;
}

/* 场景一：彩虹流光边框（conic-gradient + mask） */
.rainbow-border {
  position: relative;
  width: 240px;
  height: 120px;
  border-radius: 16px;
  background: var(--rainbow-gradient);
  /* 用 mask 抠出中间，只留边框 */
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  padding: 2px;
  animation: hue-spin var(--anim-duration) linear infinite;
  will-change: filter;
}

@keyframes hue-spin {
  to { filter: hue-rotate(360deg); }
}

/* 场景二：彩虹文字 */
.rainbow-text {
  background: linear-gradient(90deg, #f36, #f90, #fc3, #3f6, #36f, #93f, #f36);
  background-size: 200% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: hue-spin 6s linear infinite, bg-pan 4s linear infinite;
}

@keyframes bg-pan {
  to { background-position: 200% 0; }
}

/* 场景三：加载圆环（单色环 + hue-rotate 变色） */
.spinner {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 4px solid transparent;
  border-top-color: #00e5ff;
  border-right-color: #00e5ff;
  animation: spin 1s linear infinite, hue-spin 3s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 场景四：暗黑模式彩虹降饱和，避免刺眼 */
@media (prefers-color-scheme: dark) {
  :root {
    --anim-duration: 6s;          /* 暗色放慢，减少视觉刺激 */
  }
  .rainbow-border,
  .rainbow-text {
    filter: saturate(0.7) brightness(0.85);
  }
  /* 注意：hue-rotate 动画会覆盖静态 filter，需合并到关键帧 */
  .rainbow-border {
    animation: hue-spin-dark var(--anim-duration) linear infinite;
  }
}

@keyframes hue-spin-dark {
  0%   { filter: hue-rotate(0deg) saturate(0.7) brightness(0.85); }
  100% { filter: hue-rotate(360deg) saturate(0.7) brightness(0.85); }
}

/* 尊重用户的减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
  .rainbow-border,
  .rainbow-text,
  .spinner {
    animation: none;
  }
}
```

## 执行步骤
1. 用 `conic-gradient` 画一个圆锥渐变作为彩虹基底（红橙黄绿青蓝紫循环）
2. 用 `mask` + `mask-composite: exclude` 把渐变抠成中空边框，只保留外圈
3. 给元素加 `animation: hue-spin` 关键帧，`filter: hue-rotate` 从 0 到 360 度循环
4. 彩虹文字用 `linear-gradient` + `background-clip: text`，叠加 `hue-rotate` 让色彩流动
5. 加载圆环用单色 `border-top-color`，配合 `transform: rotate` 旋转 + `hue-rotate` 变色双动画
6. 暗黑模式下放慢动画时长、降低 `saturate` 和 `brightness`，避免刺眼
7. 注意：`filter` 动画会覆盖静态 filter，需把 `saturate`/`brightness` 合并进关键帧
8. 用 `prefers-reduced-motion` 为敏感用户关闭动画

## 兼容性
- `filter: hue-rotate`：Chrome 53+、Firefox 35+、Safari 9.1+、Edge 79+ 全面支持
- `conic-gradient`：Chrome 69+、Firefox 83+、Safari 12.1+
- `mask-composite`：Chrome 120+（标准）、Safari 需 `-webkit-mask-composite: xor`
- 移动端：iOS Safari 12.2+、Android Chrome 69+

## 降级方案
```css
/* 不支持 conic-gradient 时退回线性渐变边框 */
@supports not (background: conic-gradient(red, blue)) {
  .rainbow-border {
    background: linear-gradient(90deg, #f36, #f90, #fc3, #3f6, #36f, #93f);
    /* 退回普通渐变，无流光 */
    animation: none;
  }
}

/* 不支持 mask-composite 时退回双层盒子 */
@supports not (mask-composite: exclude) {
  .rainbow-border {
    -webkit-mask: none;
    mask: none;
    /* 用伪元素覆盖中心实现中空 */
  }
  .rainbow-border::after {
    content: '';
    position: absolute;
    inset: 2px;
    background: var(--color-card-bg, #fff);
    border-radius: 14px;
  }
}
```

## 相关链接
- [[filter-滤镜组合]] - hue-rotate 是 filter 家族成员
- [[conic-gradient-边框]] - conic-gradient 配合 hue-rotate 做彩虹边框
- [[mix-blend-mode-混合模式]] - 色相旋转后混合产生迷幻效果
- [[00-MOC-滤镜]]
