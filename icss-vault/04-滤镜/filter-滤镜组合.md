---
title: filter 滤镜组合
type: technique
tags:
  - icss/滤镜/基础
  - 难度/初级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[backdrop-filter-毛玻璃]]"
  - "[[hue-rotate-色相旋转]]"
  - "[[不规则边框-drop-shadow]]"
---

# filter 滤镜组合

## 问题/场景
需要对图片或元素做视觉增强：hover 时提亮增对比、禁用态变灰、卡片悬浮加投影。`filter` 提供一组图形滤镜函数，可链式组合，是低成本视觉特效首选。

## 核心原理
`filter` 属性对一个元素的**自身渲染内容**（含文本、图片、子元素）应用图形滤镜。多个函数按书写顺序依次执行，前一个的输出是后一个的输入。所有滤镜函数都接收一个值，作用于像素的 RGBA 通道或位置。

常用函数：
- `blur(px)` 高斯模糊
- `brightness(0~1+)` 亮度（1 为原图）
- `contrast(0~1+)` 对比度
- `drop-shadow(x y blur color)` 跟随 alpha 通道的投影
- `grayscale(0~1)` 去色
- `hue-rotate(deg)` 色相旋转
- `sepia(0~1)` 棕褐色
- `saturate(0~1+)` 饱和度
- `invert(0~1)` 反色
- `opacity(0~1)` 透明度

**性能要点**：`filter` 会创建合成层（compositing layer），触发 GPU 加速；但 `blur`/`drop-shadow` 计算量大，长列表大面积使用会掉帧。优先用 `transform` 做动画，`filter` 仅做状态切换。

## 实现方案

```css
:root {
  --color-card-bg: #ffffff;
  --color-shadow: rgba(0, 0, 0, 0.15);
  --color-disabled: #9a9a9a;
  --filter-hover: brightness(1.08) contrast(1.1) saturate(1.15);
  --filter-disabled: grayscale(1) opacity(0.6);
}

/* 场景一：图片 hover 增强视觉 */
.card-img {
  width: 100%;
  aspect-ratio: 16 / 9;          /* 预留渲染空间，避免布局抖动 */
  object-fit: cover;
  transition: filter 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: filter;           /* 动画前声明，结束后移除 */
}
.card-img:hover {
  filter: var(--filter-hover);
}

/* 场景二：禁用态变灰 */
.btn-disabled {
  cursor: not-allowed;
  filter: var(--filter-disabled);
}

/* 场景三：卡片悬浮投影（drop-shadow 跟随透明轮廓） */
.badge {
  filter: drop-shadow(0 4px 8px var(--color-shadow));
  transition: filter 0.3s ease;
}
.badge:hover {
  filter: drop-shadow(0 8px 16px var(--color-shadow));
}

/* 场景四：复古棕褐色照片 */
.photo-vintage {
  filter: sepia(0.6) contrast(1.1) brightness(0.95);
}

/* 场景五：暗黑模式降饱和，避免刺眼 */
@media (prefers-color-scheme: dark) {
  :root {
    --filter-hover: brightness(1.05) contrast(1.05);
  }
  .photo-vintage {
    filter: sepia(0.4) contrast(1.05) brightness(0.85);
  }
}
```

## 执行步骤
1. 在 `:root` 用 CSS 变量定义常用滤镜组合，便于主题切换与复用
2. 给图片设置 `aspect-ratio` 预留空间，防止图片加载导致布局抖动
3. hover 时应用 `brightness`+`contrast`+`saturate` 组合，让图片更鲜活
4. 禁用态用 `grayscale`+`opacity`，语义清晰且无侵入
5. 不规则形状（如 PNG 透明图）用 `drop-shadow` 而非 `box-shadow`，阴影才跟随轮廓
6. 暗黑模式下降低 `brightness` 与 `sepia` 强度，避免过曝刺眼
7. 滤镜动画务必声明 `will-change: filter`，动画结束移除以释放内存

## 兼容性
- Chrome: 53+
- Firefox: 35+
- Safari: 9.1+（需 `-webkit-` 前缀，现代版本已无需）
- Edge: 79+
- 移动端：iOS Safari 9.3+、Android Chrome 53+ 全面支持

## 降级方案
```css
/* 不支持 filter 的浏览器退回普通 hover */
@supports not (filter: blur(1px)) {
  .card-img:hover {
    opacity: 0.9;                /* 退回透明度变化 */
  }
  .btn-disabled {
    opacity: 0.5;
  }
}

/* 兼容旧版 Safari */
.card-img {
  -webkit-filter: var(--filter-hover);
  filter: var(--filter-hover);
}
```

## 相关链接
- [[backdrop-filter-毛玻璃]] - 模糊背景而非元素本身
- [[hue-rotate-色相旋转]] - 用 hue-rotate 制作彩虹动画
- [[不规则边框-drop-shadow]] - drop-shadow 为 clip-path 形状加阴影
- [[00-MOC-滤镜]]
