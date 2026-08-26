---
title: transform 触发硬件加速
type: technique
tags:
  - icss/性能/硬件加速
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[will-change]]"
  - "[[content-visibility]]"
  - "[[contain-包含上下文]]"
---

# transform 触发硬件加速

## 问题/场景
动画卡顿、滚动抖动。原因是动画触发了 CPU 路径上的重排重绘，每次都让浏览器重新计算布局。我们希望动画跑在 GPU 上，脱离主线程。

## 核心原理
浏览器渲染有两条路径：
- **CPU 路径**：layout → paint → composite，每次重排重绘都走这条
- **GPU 路径**：只 composite，跳过 layout/paint

`transform` 和 `opacity` 只触发 composite，会让浏览器为元素创建独立的**合成层（composited layer）**，由 GPU 处理。其他属性（width、top、background-color）都会触发 layout 或 paint。

经典的 `translateZ(0)` hack 就是利用这个原理：给元素一个 3D 变换，强制浏览器创建合成层（即使 z 位移为 0）。

**layer explosion（图层爆炸）**：每个 transform 元素都建一层，内存占用暴涨，反而更卡。需要控制合成层数量。

## 实现方案

```css
:root {
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
}

/* ✅ 正确：用 transform 做动画，只触发 composite */
.card {
  transition: transform 0.3s var(--ease-standard),
              opacity 0.3s var(--ease-standard);
}

.card:hover {
  transform: translateY(-4px);  /* 只触发 composite，不重排 */
  opacity: 0.9;
}

/* ✅ 经典 hack：强制创建合成层（兼容老浏览器） */
.gpu-layer {
  transform: translateZ(0);       /* 3D 变换触发 GPU 层 */
  /* 或 */
  transform: translate3d(0, 0, 0);
  /* 或现代写法：will-change */
  will-change: transform;
}

/* ✅ 与 opacity 配合：fade + move 动画全 GPU 化 */
.fade-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.4s var(--ease-standard),
              transform 0.4s var(--ease-standard);
}

.fade-in.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* ❌ 错误：动画 top/left 会触发重排 */
.bad {
  position: absolute;
  top: 0;
  transition: top 0.3s;  /* 触发 layout，卡顿 */
}
.bad:hover { top: -4px; }

/* ✅ 正确：用 transform 替代 top/left */
.good {
  position: absolute;
  transition: transform 0.3s var(--ease-standard);
}
.good:hover { transform: translateY(-4px); }
```

## 执行步骤
1. **检查动画属性**：所有动画只动 `transform` 和 `opacity`
2. **替换重排属性**：`top/left` → `transform: translate()`，`width/height` → `transform: scale()`
3. **强制合成层**：老浏览器用 `translateZ(0)`，现代浏览器用 `will-change: transform`
4. **避免 layer explosion**：不要给所有元素都加 `translateZ(0)`，只给真正动画的元素加
5. **Chrome DevTools 验证**：Layers 面板看合成层数量，太多就要精简

## 兼容性
- Chrome: 全部支持
- Firefox: 全部支持
- Safari: 全部支持
- `translateZ(0)` hack 兼容到 IE9+

## 降级方案
```css
/* 老浏览器（IE8-）不支持 transform，降级到重排但保证功能 */
@supports not (transform: translateZ(0)) {
  .card {
    transition: top 0.3s, left 0.3s;  /* 重排但能跑 */
  }
  .card:hover {
    position: relative;
    top: -4px;
  }
}
```

## 性能对比
| 属性 | 触发阶段 | 性能 |
|------|----------|------|
| `width`/`height`/`margin` | layout → paint → composite | 最差 |
| `top`/`left`/`right`/`bottom` | layout → paint → composite | 差 |
| `color`/`background`/`box-shadow` | paint → composite | 中 |
| `transform`/`opacity` | composite | 最佳 |

## 相关链接
- [[will-change]]
- [[content-visibility]]
- [[contain-包含上下文]]
- [[00-MOC-性能]]
