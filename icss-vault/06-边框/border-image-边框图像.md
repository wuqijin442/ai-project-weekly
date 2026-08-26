---
title: border-image 边框图像
type: technique
tags:
  - icss/边框/border-image
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[conic-gradient-边框]]"
  - "[[圆角与形状]]"
---

# border-image 边框图像

## 问题/场景
需要用一张图片作为边框（如手绘边框、相框装饰、九宫格按钮背景）。传统 `border-color` 只能用纯色，`border-image` 把一张图按九宫格切片贴到边框上，四角固定、四边拉伸或重复，适合做装饰性边框。

## 核心原理
`border-image` 把源图像切成 **3×3 九宫格**：
- **四角**（1、3、7、9）：固定不缩放，放在边框四角
- **四边**（2、4、6、8）：按 `border-image-repeat` 规则处理（拉伸/重复/圆角）
- **中心**（5）：默认丢弃，`border-image-slice: fill` 时填充

**核心属性**：
| 属性 | 作用 | 示例 |
|------|------|------|
| `border-image-source` | 图源 URL | `url('border.png')` |
| `border-image-slice` | 切片尺寸（上 右 下 左，不带单位） | `27 27 27 27` |
| `border-image-width` | 边框宽度 | `20px` 或 `1`（倍数） |
| `border-image-repeat` | 边重复方式 | `stretch` / `repeat` / `round` / `space` |
| `border-image-outset` | 边框外扩 | `10px` |

**简写**：
```css
border-image: source slice / width / outset repeat;
```

**repeat 模式区别**：
- `stretch`：拉伸填满（默认，平滑但可能变形）
- `repeat`：平铺重复（不变形，但可能截断）
- `round`：平铺并整体缩放，完整显示（推荐）
- `space`：平铺，多余空间留白

**重要限制**：`border-image` 会覆盖 `border-radius`，圆角失效。需圆角时配合 `clip-path` 或改用 `conic-gradient + mask` 方案。

## 实现方案

```css
:root {
  --border-img-width: 20px;
  --color-card-bg: #ffffff;
}

/* 场景一：基础九宫格图片边框 */
.frame-img {
  width: 300px;
  height: 200px;
  border-style: solid;            /* 必须，否则 border-image 不生效 */
  border-width: var(--border-img-width);
  border-image-source: url('frame.png');
  border-image-slice: 27;          /* 每边切 27px（图片四角各 27×27） */
  border-image-repeat: round;      /* 推荐用 round，完整平铺 */
  /* 简写：border-image: url('frame.png') 27 / 20px round; */
}

/* 场景二：渐变作为 border-image（无需图片文件） */
.gradient-border-img {
  width: 240px;
  height: 120px;
  border-style: solid;
  border-width: 2px;
  /* 用 linear-gradient 作为图源，slice 1 表示整张图四角各 1 */
  border-image: linear-gradient(135deg, #1890ff, #722ed1) 1;
  /* 注意：此方案无圆角，需圆角用 conic-gradient+mask */
}

/* 场景三：手绘风格不规则边框 */
.hand-drawn {
  width: 200px;
  padding: 16px;
  border-style: solid;
  border-width: 12px;
  border-image-source: url('hand-drawn.png');
  border-image-slice: 12 12 12 12 fill;  /* fill 填充中心 */
  border-image-repeat: stretch;
}

/* 场景四：圆点虚线边框（repeat 平铺） */
.dot-border {
  width: 240px;
  height: 60px;
  border-style: solid;
  border-width: 8px;
  border-image-source: url('dot.png');   /* 单个圆点图 */
  border-image-slice: 4;
  border-image-repeat: round;
}

/* 场景五：响应式按钮背景（九宫格保证四角不变形） */
.btn-nine {
  display: inline-block;
  padding: 10px 24px;
  border-style: solid;
  border-width: 10px;
  border-image-source: url('btn-bg.png');
  border-image-slice: 10 14 10 14 fill;  /* 左右切窄、上下切宽 */
  border-image-repeat: stretch;           /* 中间拉伸适应文字长度 */
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

/* 场景六：暗黑模式适配（换图源） */
@media (prefers-color-scheme: dark) {
  :root {
    --color-card-bg: #1f1f1f;
  }
  .frame-img {
    border-image-source: url('frame-dark.png');
  }
  .gradient-border-img {
    border-image: linear-gradient(135deg, #177ddc, #531dab) 1;
  }
}
```

## 执行步骤
1. 准备一张可切片的边框图（PNG/SVG），确保四角内容固定、四边可拉伸
2. 用 `border-style: solid` + `border-width` 设置边框占位（必须，否则 border-image 不显示）
3. `border-image-source: url(...)` 指定图源，`border-image-slice` 设置切片尺寸（不带 px 单位，是图源像素值）
4. `border-image-repeat: round` 完整平铺不截断，`stretch` 拉伸不重复
5. 渐变边框：`border-image: linear-gradient(...) 1`，slice 为 1 表示整图四角各 1px
6. 响应式按钮：左右切片窄、用 `stretch` 让中间拉伸适应文字长度，四角不变形
7. 暗黑模式换图源或换渐变色
8. 注意：`border-image` 会覆盖 `border-radius`，圆角需配合 `clip-path` 或改用 mask 方案

## 兼容性
- `border-image`：Chrome 56+、Firefox 50+、Safari 11+、Edge 79+ 全面支持
- `border-image-source` 接收 `linear-gradient`/`conic-gradient`：所有现代浏览器支持
- 移动端：iOS Safari 11+、Android Chrome 56+
- IE11 部分支持（语法不同），现代项目无需考虑

## 降级方案
```css
/* 不支持 border-image 时退回纯色边框 */
@supports not (border-image: url('x.png') 1) {
  .frame-img {
    border: 20px solid #d9b382;       /* 退回近似纯色边框 */
    border-radius: 8px;
  }
  .gradient-border-img {
    border: 2px solid #1890ff;         /* 退回纯色 */
  }
}

/* 渐变 border-image 不支持时，用 conic-gradient+mask 替代（支持圆角） */
@supports not (border-image: linear-gradient(red, blue) 1) {
  .gradient-border-img {
    border: none;
    background: linear-gradient(135deg, #1890ff, #722ed1);
    padding: 2px;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask-composite: exclude;
    border-radius: 8px;
  }
}
```

## 相关链接
- [[conic-gradient-边框]] - 渐变边框且需圆角时改用此方案
- [[圆角与形状]] - border-image 与 border-radius 的冲突处理
- [[clip-path-多边形]] - 配合 border-image 做圆角裁剪
- [[00-MOC-边框]]
