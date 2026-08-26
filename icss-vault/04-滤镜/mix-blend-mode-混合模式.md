---
title: mix-blend-mode 混合模式
type: technique
tags:
  - icss/滤镜/混合模式
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[filter-滤镜组合]]"
  - "[[hue-rotate-色相旋转]]"
---

# mix-blend-mode 混合模式

## 问题/场景
需要让两个重叠元素的颜色「融合」：头像与渐变背景混合成单色剪影、文字与背景图片产生反色镂空、卡片 hover 时颜色叠加变色。`mix-blend-mode` 让元素与背后内容按数学公式混合，省去 JS 取色。

## 核心原理
`mix-blend-mode` 决定元素自身像素如何与**背后的像素**（父级 stacking context 下方所有内容）混合。每种模式是一个颜色计算公式，输入是「源色（Source，元素自身）」和「目标色（Destination，背后内容）」，输出混合后的颜色。

16 种模式分四类：
- **正常**：`normal`（不混合）
- **变暗**：`darken`、`multiply`、`color-burn`、`linear-burn`（结果更暗）
- **变亮**：`lighten`、`screen`、`color-dodge`、`linear-dodge`、`difference`、`exclusion`（结果更亮）
- **对比**：`overlay`、`soft-light`、`hard-light`、`vivid-light`、`pin-light`、`hard-mix`
- **色相**：`hue`、`saturation`、`color`、`luminosity`（用源色属性替换目标色）

**与 `background-blend-mode` 区别**：
| 属性 | 混合对象 |
|------|----------|
| `mix-blend-mode` | 元素与背后**其他元素** |
| `background-blend-mode` | 同一元素的**多个 background** 之间 |

## 实现方案

```css
:root {
  --blend-color: #ff3366;
  --blend-mask: #ffffff;
}

/* 场景一：头像融合为单色剪影 */
.avatar-wrap {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--blend-color);
}
.avatar-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* multiply：图片暗部保留、亮部被背景色染上，形成单色剪影 */
  mix-blend-mode: multiply;
}

/* 场景二：文字镂空显示背景图片 */
.text-cutout {
  position: relative;
  color: var(--blend-mask);
  font-size: 96px;
  font-weight: 900;
  /* difference：与背景做差值，文字呈现反色镂空 */
  mix-blend-mode: difference;
  /* 父级需有背景图才能看到效果 */
}

.bg-image {
  position: absolute;
  inset: 0;
  background: url('bg.jpg') center/cover;
  z-index: -1;
}

/* 场景三：卡片 hover 颜色叠加 */
.card-blend {
  position: relative;
  background: var(--color-card-bg, #fff);
  transition: transform 0.3s ease;
}
.card-blend::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--blend-color), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
  mix-blend-mode: soft-light;   /* 柔光叠加，自然不突兀 */
}
.card-blend:hover::before {
  opacity: 1;
}

/* 场景四：渐变文字（mix-blend-mode 替代 background-clip） */
.gradient-text {
  background: linear-gradient(90deg, #f36, #f90, #fc3);
  color: #000;
  mix-blend-mode: screen;        /* 黑字与彩色背景 screen 提亮成渐变 */
  -webkit-background-clip: text;
  background-clip: text;
}

/* 暗黑模式：difference 在深色背景下反差更明显，无需特殊处理；
   multiply 会让结果更暗，暗黑模式可改用 lighten/screen */
@media (prefers-color-scheme: dark) {
  .avatar-wrap img {
    mix-blend-mode: screen;      /* 暗底下改用提亮模式 */
  }
}
```

## 执行步骤
1. 给容器设置纯色背景，子级图片用 `mix-blend-mode: multiply`，暗部保留亮部染色，得到单色剪影
2. 文字镂空：文字用 `mix-blend-mode: difference`，与背景图做差值运算，自动呈现反色
3. 卡片 hover 叠色用伪元素 + `mix-blend-mode: soft-light`，opacity 控制显隐，比改背景色更柔和
4. 渐变文字可配合 `background-clip: text`，`mix-blend-mode` 增强过渡
5. 暗黑模式下 `multiply` 会让画面过暗，改用 `screen`/`lighten` 提亮
6. 注意：`mix-blend-mode` 会创建新的 stacking context，配合 `z-index`/`isolation: isolate` 隔离混合范围
7. 用 `isolation: isolate` 在父级隔离混合，防止子级混合影响外部元素

## 兼容性
- Chrome: 41+
- Firefox: 32+
- Safari: 8+（前缀 `-webkit-`，现代版本无需）
- Edge: 79+
- 移动端：iOS Safari 8+、Android Chrome 41+ 全面支持
- `hard-mix`/`vivid-light`/`pin-light` 等较新模式在旧浏览器可能无效

## 降级方案
```css
/* 不支持时退回普通 opacity 叠加 */
@supports not (mix-blend-mode: multiply) {
  .avatar-wrap img {
    opacity: 0.7;                /* 退回透明度叠加 */
  }
  .card-blend::before {
    opacity: 0.15;               /* 降低不透明度模拟柔光 */
    mix-blend-mode: normal;
  }
}

/* 隔离混合范围，避免影响外部 */
.blend-scope {
  isolation: isolate;
}
```

## 相关链接
- [[filter-滤镜组合]] - filter 与 mix-blend-mode 配合做高级特效
- [[hue-rotate-色相旋转]] - hue-rotate 改变色相后再混合
- [[conic-gradient-边框]] - 渐变 + 混合模式做炫彩边框
- [[00-MOC-滤镜]]
