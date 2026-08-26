---
title: backdrop-filter 毛玻璃
type: technique
tags:
  - icss/滤镜/毛玻璃
  - 难度/中级
  - 兼容性/渐进
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[filter-滤镜组合]]"
  - "[[SVG滤镜]]"
---

# backdrop-filter 毛玻璃

## 问题/场景
苹果 iOS / macOS 风格的「毛玻璃」效果：弹层背景半透明且背后内容被模糊。`filter: blur()` 只模糊元素自身内容，无法模糊「透过元素看到的背后内容」，必须用 `backdrop-filter`。

## 核心原理
`backdrop-filter` 对元素**背后的内容**（backdrop，即该元素之下的所有像素）应用滤镜。元素本身必须半透明，否则看不到背后内容被模糊的效果。

**与 `filter` 的关键区别**：
| 属性 | 作用对象 | 典型用途 |
|------|----------|----------|
| `filter` | 元素自身渲染内容 | 图片增强、文字模糊 |
| `backdrop-filter` | 元素背后内容 | 毛玻璃、磨砂玻璃 |

两者可同时使用：`filter` 模糊自身文字，`backdrop-filter` 模糊背后背景。

**渲染条件**：元素需有 `position` 脱离正常流或叠加在内容之上，且 `background` 半透明；背后要有可被模糊的内容（图片/渐变/其他元素）。

## 实现方案

```css
:root {
  --glass-bg-light: rgba(255, 255, 255, 0.65);
  --glass-bg-dark: rgba(20, 22, 28, 0.55);
  --glass-border-light: rgba(255, 255, 255, 0.4);
  --glass-border-dark: rgba(255, 255, 255, 0.12);
  --glass-blur: 16px;
  --glass-saturate: 1.8;
}

.glass-card {
  /* 半透明背景：必须，否则看不到背后模糊 */
  background: var(--glass-bg-light);
  /* 毛玻璃核心：模糊 + 提饱和（饱和度提升让颜色更通透） */
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturate));
  backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturate));
  /* 边框增强玻璃质感 */
  border: 1px solid var(--glass-border-light);
  border-radius: 16px;
  /* 内层高光模拟玻璃边缘 */
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5),
              0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

/* 顶部导航毛玻璃条 */
.glass-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--glass-bg-light);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--glass-border-light);
}

/* 暗黑模式适配：降低背景亮度、加深颜色 */
@media (prefers-color-scheme: dark) {
  :root {
    --glass-bg-light: var(--glass-bg-dark);
    --glass-border-light: var(--glass-border-dark);
  }
  .glass-card {
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08),
                0 8px 32px rgba(0, 0, 0, 0.4);
  }
}

/* 弹层背景毛玻璃（modal 遮罩） */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  -webkit-backdrop-filter: blur(4px);
  backdrop-filter: blur(4px);
}
```

## 执行步骤
1. 在 `:root` 用 CSS 变量定义亮/暗两套毛玻璃参数，方便主题切换
2. 元素设置半透明 `background`（透明度 0.5~0.7 效果最佳，全透明或全不透明都看不到效果）
3. 写 `-webkit-backdrop-filter` 兼容旧版 Safari，再写标准 `backdrop-filter`
4. 配合 `saturate()` 提升饱和度，让毛玻璃颜色更通透有质感
5. 用 `inset box-shadow` 模拟玻璃边缘高光，增强立体感
6. 暗黑模式下降低背景透明度（更暗）、减弱高光、加深阴影，避免过曝
7. 弹窗遮罩用小半径 `blur(4px)` 即可，过大半径会拖慢渲染

## 兼容性
- Chrome: 76+
- Firefox: 103+（默认开启，之前需 `layout.css.backdrop-filter.enabled`）
- Safari: 9+（必须 `-webkit-` 前缀，18+ 起标准属性也支持）
- Edge: 79+
- 移动端：iOS Safari 9+、Android Chrome 76+ 支持

## 降级方案
```css
/* 不支持 backdrop-filter 时退回纯半透明背景 */
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass-card {
    background: rgba(255, 255, 255, 0.9);   /* 提高不透明度保证可读性 */
  }
  .glass-nav {
    background: rgba(255, 255, 255, 0.95);
  }
}

@media (prefers-color-scheme: dark) {
  @supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
    .glass-card {
      background: rgba(20, 22, 28, 0.92);
    }
  }
}
```

## 相关链接
- [[filter-滤镜组合]] - filter 与 backdrop-filter 的区别与配合
- [[SVG滤镜]] - 用 feDisplacementMap 增强毛玻璃为液态玻璃
- [[00-MOC-滤镜]]
