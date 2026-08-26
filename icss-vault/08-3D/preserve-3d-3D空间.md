---
title: preserve-3d-3D空间
type: technique
tags:
  - icss/08-3D/基础
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[perspective-透视]]"
  - "[[3D翻转卡片]]"
  - "[[3D立方体]]"
---

# preserve-3d-3D空间

## 问题/场景
默认情况下，子元素的 3D 变换会被父元素"压平"到 2D 平面渲染，立体感丢失。要让多个嵌套元素真正处于同一 3D 空间，必须用 `transform-style: preserve-3d`。同时控制翻转卡片背面是否可见。

## 核心原理
- `transform-style: preserve-3d`：让子元素保留 3D 位置，与父元素处于同一 3D 空间
  - 默认值 `flat` 会把所有子元素压平到父元素的 2D 平面
- 嵌套场景：每一层 3D 容器都要加 `preserve-3d`，否则 3D 信息在某一层会丢失
- `backface-visibility: hidden`：元素旋转到背面时（rotateY 超过 90°）隐藏，用于翻转卡片
- 注意：`overflow: hidden` 会强制 `preserve-3d` 失效（变成 `flat`），这是常见坑

## 实现方案
```css
:root {
  --face-color: #00e5ff;
  --back-color: #64c8ff;
  --bg-color: #0f172a;
}

/* 1. preserve-3d 让子元素保持 3D 位置 */
.scene {
  perspective: 1000px;
}

.preserve-card {
  position: relative;
  width: 200px;
  height: 260px;
  transform-style: preserve-3d; /* 关键：保留子元素 3D 空间 */
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.preserve-card:hover {
  transform: rotateY(180deg);
}

.preserve-card .face {
  position: absolute;
  inset: 0;
  backface-visibility: hidden; /* 背面隐藏 */
  -webkit-backface-visibility: hidden;
  display: grid;
  place-items: center;
  border-radius: 12px;
}

.preserve-card .front {
  background: var(--face-color);
}

.preserve-card .back {
  background: var(--back-color);
  transform: rotateY(180deg); /* 背面预先旋转 180° */
}

/* 2. 多层嵌套：每一层都要 preserve-3d */
.nested-3d {
  transform-style: preserve-3d;
  transform: rotateX(30deg);
}
.nested-3d .layer {
  transform-style: preserve-3d; /* 嵌套层级也要加 */
  transform: translateZ(50px);
}
.nested-3d .layer .item {
  transform: rotateY(45deg);
}

/* 常见坑：overflow: hidden 会让 preserve-3d 失效 */
.broken-3d {
  transform-style: preserve-3d;
  overflow: hidden; /* ⚠️ 这行会让上面那行失效！ */
}

@media (prefers-color-scheme: dark) {
  :root { --face-color: #60a5fa; --back-color: #a78bfa; }
}
```

## 执行步骤
1. 在父容器加 `perspective: 1000px` 建立景深（参考 [[perspective-透视]]）
2. 在 3D 旋转的元素上加 `transform-style: preserve-3d`，让子元素保持 3D 位置
3. 翻转卡片的正反两面都加 `backface-visibility: hidden`，背面预先 `rotateY(180deg)`
4. 嵌套 3D：每一层都要重复加 `preserve-3d`，否则中间某一层会压平
5. **避坑**：不要在 `preserve-3d` 元素上加 `overflow: hidden`，会强制变 `flat`

## 兼容性
- Chrome: 36+
- Firefox: 16+
- Safari: 9+（部分场景需要 `-webkit-` 前缀）
- `backface-visibility`：建议同时写 `-webkit-backface-visibility`

## 降级方案
```css
@supports not (transform-style: preserve-3d) {
  .preserve-card .back {
    /* 不支持 3D 时降级为透明度切换 */
    backface-visibility: visible;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  .preserve-card:hover .back {
    opacity: 1;
  }
  .preserve-card:hover .front {
    opacity: 0;
  }
}
```

## 相关链接
- [[perspective-透视]] - 配合 perspective 才有立体感
- [[3D翻转卡片]] - preserve-3d 的经典应用
- [[3D立方体]] - 6 面 3D 空间
- [[00-MOC-3D]]
