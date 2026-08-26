---
title: Liquid Glass 液态玻璃特效
type: technique
tags:
  - icss/前沿特性/视觉
  - 难度/高级
  - 兼容性/渐进
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[transform-硬件加速]]"
  - "[[CSS-Houdini]]"
---

# Liquid Glass 液态玻璃特效

## 问题/场景
苹果新 UI 风格的「液态玻璃」效果：背景内容透过玻璃时产生**扭曲折射**，而不只是模糊。普通 `backdrop-filter: blur()` 只能模糊，无法实现折射扭曲的液态感。我们希望用纯 CSS + SVG 滤镜组合实现苹果风格的液态玻璃。

## 核心原理
普通毛玻璃 = `backdrop-filter: blur()`，只对背景做高斯模糊。
液态玻璃 = 模糊 + **像素位移扭曲**，背景像透过水波纹一样变形。

实现方案对比：
| 方案 | 优点 | 缺点 |
|------|------|------|
| Shader (WebGL) | 效果最佳 | 实现复杂，需 WebGL |
| WebGPU | 性能最优 | 兼容性差 |
| CSS + SVG Filter | 实现简单 | 效果略逊 |

SVG 滤镜方案核心三个原语：
1. `feTurbulence`：生成 Perlin 噪声纹理
2. `feDisplacementMap`：用噪声对像素位移产生扭曲
3. `feGaussianBlur`：平滑边缘

通过 `backdrop-filter: blur() url(#filter)` 把 SVG 滤镜应用到 backdrop 上。

## 实现方案

### 基础液态玻璃

```html
<!-- SVG 滤镜定义（隐藏在页面中） -->
<svg style="position:absolute;width:0;height:0">
  <filter id="liquid-glass">
    <!-- 1. 生成噪声纹理 -->
    <feTurbulence
      type="fractalNoise"
      baseFrequency="0.01"
      numOctaves="2"
      seed="0"/>
    <!-- 2. 用噪声位移像素 -->
    <feDisplacementMap
      in="SourceGraphic"
      scale="30"/>
    <!-- 3. 平滑边缘 -->
    <feGaussianBlur stdDeviation="2"/>
  </filter>
</svg>

<div class="glass-element">液态玻璃内容</div>
```

```css
:root {
  --glass-bg: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
  --glass-radius: 16px;
}

.glass-element {
  /* 关键：blur + SVG 滤镜组合 */
  backdrop-filter: blur(10px) url(#liquid-glass);
  -webkit-backdrop-filter: blur(10px);  /* Safari 兼容 */

  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  padding: 24px;
}
```

### 进阶：可调参数液态玻璃

```css
/* 不同强度参数 */
.glass--subtle {
  backdrop-filter: blur(5px) url(#liquid-glass-subtle);
}
.glass--medium {
  backdrop-filter: blur(10px) url(#liquid-glass-medium);
}
.glass--strong {
  backdrop-filter: blur(20px) url(#liquid-glass-strong);
}
```

```html
<svg style="position:absolute;width:0;height:0">
  <!-- 微弱扭曲 -->
  <filter id="liquid-glass-subtle">
    <feTurbulence type="fractalNoise" baseFrequency="0.008" numOctaves="1"/>
    <feDisplacementMap in="SourceGraphic" scale="10"/>
  </filter>

  <!-- 中等扭曲 -->
  <filter id="liquid-glass-medium">
    <feTurbulence type="fractalNoise" baseFrequency="0.01" numOctaves="2"/>
    <feDisplacementMap in="SourceGraphic" scale="30"/>
  </filter>

  <!-- 强烈扭曲 -->
  <filter id="liquid-glass-strong">
    <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="3"/>
    <feDisplacementMap in="SourceGraphic" scale="50"/>
  </filter>
</svg>
```

### 动态液态玻璃（动画扭曲）

```css
@keyframes liquid-flow {
  0%   { filter: url(#liquid-1); }
  50%  { filter: url(#liquid-2); }
  100% { filter: url(#liquid-1); }
}

.animated-glass {
  backdrop-filter: blur(15px);
  /* 通过切换不同 seed 的滤镜模拟流动 */
  animation: liquid-flow 8s infinite ease-in-out;
}
```

### 边缘高光增强玻璃感

```css
.glass-element {
  backdrop-filter: blur(10px) url(#liquid-glass);
  background: var(--glass-bg);
  border-radius: var(--glass-radius);

  /* 顶部高光 */
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.4),  /* 顶部内高光 */
    inset 0 -1px 0 rgba(255, 255, 255, 0.1), /* 底部内阴影 */
    0 8px 32px rgba(0, 0, 0, 0.1);            /* 外阴影 */

  /* 边缘渐变模拟玻璃折射 */
  border: 1px solid transparent;
  background-clip: padding-box;
  background-image:
    linear-gradient(var(--glass-bg), var(--glass-bg)),
    linear-gradient(135deg,
      rgba(255,255,255,0.5) 0%,
      rgba(255,255,255,0.1) 50%,
      rgba(255,255,255,0.3) 100%);
  background-origin: padding-box, border-box;
}
```

## 执行步骤
1. **在页面放 SVG 滤镜定义**：`position: absolute; width: 0; height: 0` 隐藏
2. **配置 `feTurbulence`**：`baseFrequency` 越小噪声越平滑，`numOctaves` 越大细节越多
3. **配置 `feDisplacementMap`**：`scale` 控制扭曲强度（10-50 之间）
4. **元素应用 `backdrop-filter: blur() url(#id)`**：blur 和滤镜组合
5. **加边缘高光增强真实感**：`box-shadow: inset` 顶部高光
6. **测试性能**：SVG 滤镜有性能开销，长列表慎用

## 兼容性
- Chrome: 76+（backdrop-filter）、18+（SVG filter）
- Firefox: 103+（backdrop-filter）、35+（SVG filter）
- Safari: 9+（-webkit-backdrop-filter）、6+（SVG filter）
- `backdrop-filter: url()` 组合：Chrome 76+、Safari 9+，Firefox 部分支持

## 降级方案
```css
@supports not (backdrop-filter: blur(10px)) {
  .glass-element {
    /* 老浏览器：用半透明背景模拟 */
    background: rgba(255, 255, 255, 0.3);
  }
}

@supports not (backdrop-filter: url(#test)) {
  .glass-element {
    /* 不支持 SVG 滤镜组合：降级为普通毛玻璃 */
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }
}

/* 渐进增强：先 blur，再叠加 url() */
.glass-element {
  backdrop-filter: blur(10px);  /* 基础毛玻璃 */
}
@supports (backdrop-filter: blur(10px) url(#test)) {
  .glass-element {
    backdrop-filter: blur(10px) url(#liquid-glass);  /* 叠加液态扭曲 */
  }
}
```

## 与 backdrop-filter 对比
| 维度 | backdrop-filter: blur() | + SVG 滤镜 |
|------|-------------------------|------------|
| 效果 | 高斯模糊 | 模糊 + 扭曲折射 |
| 性能 | 高 | 中（滤镜开销） |
| 兼容 | Chrome 76+/Safari 9+ | 同上 |
| 真实感 | 中 | 高 |
| 适用 | 普通毛玻璃 UI | 苹果液态玻璃风格 |

## 参数调优
| 参数 | 作用 | 推荐范围 |
|------|------|----------|
| `baseFrequency` | 噪声密度 | 0.005-0.02 |
| `numOctaves` | 噪声层数 | 1-3 |
| `scale` | 扭曲强度 | 10-50 |
| `stdDeviation` | 模糊半径 | 1-5 |
| `seed` | 噪声种子 | 任意整数 |

## 应用场景
| 场景 | 参数建议 |
|------|----------|
| 顶部导航栏 | 微弱扭曲，scale=10 |
| 卡片悬浮 | 中等扭曲，scale=30 |
| 模态弹窗 | 强烈扭曲，scale=50 |
| 苹果风格 UI | 配合边缘高光 |

## 相关链接
- [[transform-硬件加速]]
- [[CSS-Houdini]]
- [[00-MOC-前沿特性]]
