---
title: SVG 滤镜
type: technique
tags:
  - icss/滤镜/svg
  - 难度/高级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[backdrop-filter-毛玻璃]]"
  - "[[filter-滤镜组合]]"
---

# SVG 滤镜

## 问题/场景
CSS `filter` 函数有限，无法实现「液态玻璃扭曲」「噪声纹理」「水波纹」等复杂效果。SVG 滤镜（`<filter>`）提供像素级处理能力，可通过 `filter: url(#id)` 在 CSS 中调用，是 CSS 滤镜的进阶扩展。

## 核心原理
SVG 滤镜是一组「图元（primitive）」的流水线，每个图元接收输入图像、输出处理后的图像，串联起来形成复杂效果。常用图元：

| 图元 | 作用 |
|------|------|
| `feTurbulence` | 生成 Perlin 噪声纹理（云雾、水波、磨砂） |
| `feDisplacementMap` | 用一张图的颜色通道对另一张图做像素位移（扭曲） |
| `feGaussianBlur` | 高斯模糊 |
| `feColorMatrix` | 颜色矩阵变换（RGBA 通道运算） |
| `feComposite` | 合成两图层 |
| `feMerge` | 合并多个结果 |

**调用方式**：在 HTML 中定义 `<svg><filter id="x">...</filter></svg>`，CSS 用 `filter: url(#x)` 或 `backdrop-filter: url(#x)` 引用。

**Liquid Glass 简版原理**：`feTurbulence` 生成噪声 → `feDisplacementMap` 用噪声对原图像素位移产生扭曲 → `feGaussianBlur` 平滑边缘 → 叠加 `backdrop-filter` 让背后内容也折射。

## 实现方案

```html
<!-- 全局 SVG 滤镜定义（隐藏，0 尺寸） -->
<svg style="position:absolute;width:0;height:0" aria-hidden="true">
  <!-- 滤镜一：液态玻璃扭曲 -->
  <filter id="liquid-glass" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.008 0.008" numOctaves="2" seed="3" result="noise"/>
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="60" xChannelSelector="R" yChannelSelector="G"/>
    <feGaussianBlur stdDeviation="0.6"/>
  </filter>

  <!-- 滤镜二：磨砂噪声纹理 -->
  <filter id="grain-noise">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
    <feComponentTransfer>
      <feFuncA type="linear" slope="0.08"/>
    </feComponentTransfer>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>

  <!-- 滤镜三：水波纹（动态 baseFrequency） -->
  <filter id="ripple">
    <feTurbulence type="turbulence" baseFrequency="0.02 0.05" numOctaves="1">
      <animate attributeName="baseFrequency" dur="8s" values="0.02 0.05;0.04 0.02;0.02 0.05" repeatCount="indefinite"/>
    </feTurbulence>
    <feDisplacementMap in="SourceGraphic" scale="20"/>
  </filter>
</svg>
```

```css
:root {
  --glass-tint: rgba(255, 255, 255, 0.18);
  --glass-border: rgba(255, 255, 255, 0.35);
}

/* 场景一：液态玻璃卡片（苹果风格毛玻璃增强版） */
.liquid-card {
  position: relative;
  background: var(--glass-tint);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 32px;
  /* backdrop-filter 模糊背后 + url 调用 SVG 滤镜做扭曲 */
  -webkit-backdrop-filter: blur(8px) url(#liquid-glass);
  backdrop-filter: blur(8px) url(#liquid-glass);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5),
              0 10px 40px rgba(0, 0, 0, 0.15);
}

/* 场景二：磨砂噪点叠加（增加质感颗粒） */
.grain-overlay {
  position: relative;
}
.grain-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  filter: url(#grain-noise);
  mix-blend-mode: overlay;
  opacity: 0.5;
}

/* 场景三：水波纹文字（hover 触发） */
.ripple-text {
  font-size: 64px;
  font-weight: 900;
  filter: none;
  transition: filter 0.4s ease;
}
.ripple-text:hover {
  filter: url(#ripple);
}

/* 场景四：SVG 滤镜做发光描边（外发光） */
.glow-stroke {
  filter: url(#glow);
}

/* 暗黑模式：液态玻璃背景调暗 */
@media (prefers-color-scheme: dark) {
  :root {
    --glass-tint: rgba(20, 22, 30, 0.45);
    --glass-border: rgba(255, 255, 255, 0.1);
  }
  .liquid-card {
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08),
                0 10px 40px rgba(0, 0, 0, 0.5);
  }
}
```

## 执行步骤
1. 在页面放置一个 `width:0;height:0` 的隐藏 SVG，定义所有 `<filter>`，避免重复定义
2. `feTurbulence` 的 `baseFrequency` 控制噪声密度（0.01 大块云雾、0.9 细密颗粒），`numOctaves` 控制层次
3. `feDisplacementMap` 的 `scale` 控制扭曲强度，`xChannelSelector`/`yChannelSelector` 选噪声的哪个通道做位移
4. CSS 用 `filter: url(#id)` 或 `backdrop-filter: blur() url(#id)` 调用，可与其他滤镜函数串联
5. 液态玻璃：`backdrop-filter: blur(8px) url(#liquid-glass)`，blur 模糊 + url 扭曲背后内容
6. 噪点纹理：用 `feColorMatrix` 去色后 `feComponentTransfer` 调透明度，叠加为 `::after` 伪元素
7. 动态效果可用 SVG `<animate>` 让 `baseFrequency` 循环变化，制造水波流动
8. 暗黑模式下降低玻璃背景透明度、加深阴影，保持可读性

## 兼容性
- `filter: url()`：Chrome 8+、Firefox 35+、Safari 6+ 全面支持
- `backdrop-filter: url()`：Chrome 76+、Safari 9+（需 `-webkit-`）、Firefox 103+
- `feTurbulence`/`feDisplacementMap`：所有现代浏览器支持
- 性能：SVG 滤镜计算量大，`feTurbulence` 在大元素上易掉帧，限制使用面积
- 移动端：iOS Safari 9+ 支持，但低端机性能差，建议 `@media` 降级

## 降级方案
```css
/* 不支持 backdrop-filter url 时退回普通毛玻璃 */
@supports not (backdrop-filter: url(#x)) {
  .liquid-card {
    -webkit-backdrop-filter: blur(12px) saturate(1.8);
    backdrop-filter: blur(12px) saturate(1.8);
  }
}

/* 不支持 SVG 滤镜时退回 CSS filter */
@supports not (filter: url(#x)) {
  .ripple-text:hover {
    filter: blur(0.5px);          /* 退回轻微模糊 */
  }
  .grain-overlay::after {
    display: none;                /* 直接隐藏噪点 */
  }
}

/* 低端机降级：减少计算量 */
@media (prefers-reduced-data: reduce) {
  .liquid-card {
    -webkit-backdrop-filter: blur(8px);
    backdrop-filter: blur(8px);   /* 去掉 url 滤镜，保留 blur */
  }
}
```

## 相关链接
- [[backdrop-filter-毛玻璃]] - SVG 滤镜增强 backdrop-filter 为液态玻璃
- [[filter-滤镜组合]] - CSS filter 与 SVG filter 的衔接
- [[conic-gradient-边框]] - 渐变 + SVG 滤镜做特效边框
- [[00-MOC-滤镜]]
