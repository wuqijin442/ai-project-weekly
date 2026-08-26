---
title: 不规则边框 drop-shadow
type: technique
tags:
  - icss/边框/drop-shadow
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[clip-path-多边形]]"
  - "[[filter-滤镜组合]]"
---

# 不规则边框 drop-shadow

## 问题/场景
用 `clip-path` 裁出的三角形、六边形、PNG 透明图等不规则形状，`box-shadow` 的阴影仍是矩形，与形状轮廓不匹配，看起来很违和。需要阴影跟随形状的真实轮廓（alpha 通道），这就必须用 `filter: drop-shadow()`。

## 核心原理
`drop-shadow()` 是 `filter` 的一个函数，它根据元素的 **alpha 通道**（透明度）计算阴影轮廓。透明区域不产生阴影，不透明区域的边缘生成阴影。

**与 `box-shadow` 的核心区别**：
| 特性 | `box-shadow` | `drop-shadow` |
|------|--------------|---------------|
| 阴影轮廓 | 元素的**盒模型矩形** | 元素的**真实可见形状**（alpha 通道） |
| 跟随圆角 | 部分跟随 `border-radius` | 完全跟随 |
| 跟随 clip-path | ❌ 不跟随 | ✅ 跟随 |
| 跟随 PNG 透明 | ❌ 矩形阴影 | ✅ 跟随图形轮廓 |
| 性能 | 高（GPU 友好） | 较低（需计算 alpha） |
| 多重阴影 | 支持多个 | 支持多个（链式） |
| inset 内阴影 | 支持 | ❌ 不支持 |

**语法**：
```css
filter: drop-shadow(x偏移 y偏移 模糊半径 [扩展半径] 颜色);
```
注意：`drop-shadow` 没有 `inset`（内阴影），也没有 `spread`（扩展半径，部分浏览器支持但非标准）。

## 实现方案

```css
:root {
  --color-shadow: rgba(0, 0, 0, 0.25);
  --color-primary: #1890ff;
}

/* 场景一：为 clip-path 裁剪的箭头加阴影 */
.arrow-btn {
  width: 120px;
  height: 48px;
  background: var(--color-primary);
  clip-path: polygon(0 0, 80% 0, 100% 50%, 80% 100%, 0 100%);
  /* box-shadow 会是矩形阴影，错误！改用 drop-shadow 跟随箭头轮廓 */
  filter: drop-shadow(0 4px 6px var(--color-shadow));
  transition: filter 0.3s ease;
}
.arrow-btn:hover {
  filter: drop-shadow(0 8px 12px var(--color-shadow));
}

/* 场景二：为 PNG 透明图加阴影（图标/logo） */
.icon-img {
  width: 64px;
  height: 64px;
  /* 图标 PNG 有透明背景，drop-shadow 只沿图标形状投射 */
  filter: drop-shadow(0 2px 4px var(--color-shadow));
}

/* 场景三：为带圆角的不规则卡片加阴影 */
.card-rounded {
  border-radius: 16px;
  /* box-shadow 也能跟随 border-radius，但 drop-shadow 更精确 */
  filter: drop-shadow(0 8px 16px var(--color-shadow));
}

/* 场景四：多重 drop-shadow 做彩色光晕 */
.glow-icon {
  filter:
    drop-shadow(0 0 4px rgba(24, 144, 255, 0.6))
    drop-shadow(0 0 8px rgba(24, 144, 255, 0.4));
}

/* 场景五：为文字加描边阴影（替代 text-shadow 的局限） */
.text-stroke-shadow {
  font-size: 48px;
  font-weight: 900;
  color: var(--color-primary);
  /* drop-shadow 跟随文字 alpha，比 text-shadow 更柔和 */
  filter: drop-shadow(0 2px 2px var(--color-shadow));
}

/* 场景六：气泡对话框尖角阴影 */
.bubble {
  position: relative;
  background: var(--color-card-bg, #fff);
  border-radius: 12px;
  padding: 16px;
  /* 用伪元素做尖角，整体加 drop-shadow */
  filter: drop-shadow(0 4px 8px var(--color-shadow));
}
.bubble::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 24px;
  width: 0;
  height: 0;
  border: 8px solid transparent;
  border-top-color: var(--color-card-bg, #fff);
  /* 注意：伪元素的 border 三角也需 drop-shadow 跟随 */
}

/* 场景七：暗黑模式阴影加深 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-shadow: rgba(0, 0, 0, 0.6);
    --color-primary: #177ddc;
  }
  .glow-icon {
    filter:
      drop-shadow(0 0 4px rgba(24, 144, 255, 0.8))
      drop-shadow(0 0 12px rgba(24, 144, 255, 0.5));
  }
}
```

## 执行步骤
1. 不规则形状（clip-path 裁剪、PNG 透明图）用 `drop-shadow` 而非 `box-shadow`，阴影才跟随轮廓
2. `drop-shadow` 写在 `filter` 属性中，语法 `drop-shadow(x y 模糊 颜色)`，无 inset
3. 多重阴影用链式：`filter: drop-shadow(...) drop-shadow(...)`，可叠加彩色光晕
4. 气泡对话框：伪元素做尖角 + 父级 `drop-shadow`，尖角阴影自动跟随
5. hover 时增大模糊半径和偏移，做「浮起」效果，配合 `transition: filter`
6. 暗黑模式阴影颜色加深（透明度提高），光晕效果增强以突出
7. 性能注意：`drop-shadow` 比 `box-shadow` 耗能，长列表大面积慎用，必要时改用 `box-shadow`

## 兼容性
- `drop-shadow`：Chrome 53+、Firefox 35+、Safari 9.1+（需 `-webkit-`）、Edge 79+
- 移动端：iOS Safari 9.1+、Android Chrome 53+ 全面支持
- 多重 `drop-shadow`：所有支持 `filter` 的浏览器均支持链式
- 性能：`drop-shadow` 需实时计算 alpha 通道，在低端机或大元素上可能掉帧

## 降级方案
```css
/* 不支持 filter/drop-shadow 时退回 box-shadow */
@supports not (filter: drop-shadow(0 0 1px black)) {
  .arrow-btn {
    /* box-shadow 不跟随形状，但至少有阴影 */
    box-shadow: 0 4px 6px var(--color-shadow);
  }
  .icon-img {
    box-shadow: 0 2px 4px var(--color-shadow);
  }
}

/* 兼容旧版 Safari */
.arrow-btn {
  -webkit-filter: drop-shadow(0 4px 6px var(--color-shadow));
  filter: drop-shadow(0 4px 6px var(--color-shadow));
}

/* 性能降级：低端机改用 box-shadow */
@media (prefers-reduced-data: reduce) {
  .arrow-btn {
    filter: none;
    box-shadow: 0 4px 6px var(--color-shadow);
  }
}
```

## 相关链接
- [[clip-path-多边形]] - clip-path 裁剪后用 drop-shadow 加阴影
- [[filter-滤镜组合]] - drop-shadow 是 filter 家族成员
- [[圆角与形状]] - 不规则圆角形状的阴影
- [[00-MOC-边框]]
