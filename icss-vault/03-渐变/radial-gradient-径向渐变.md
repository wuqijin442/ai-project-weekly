---
title: radial-gradient 径向渐变
type: technique
tags:
  - icss/03-渐变/radial
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[linear-gradient-线性渐变]]"
  - "[[conic-gradient-锥形渐变]]"
  - "[[渐变实现复杂背景]]"
---

# radial-gradient 径向渐变

## 问题/场景
按钮高光、卡片光晕、聚光灯效果、雷达扫描——这些「从一个点向外辐射」的视觉需要径向渐变。掌握圆形/椭圆、位置控制、`farthest-corner`/`closest-side` 关键字能实现精细光效控制。

## 核心原理
`radial-gradient(形状 大小 at 位置, 颜色1 位置1, 颜色2 位置2, ...)` 从中心向外辐射。
- **形状**：`circle`（圆形）或 `ellipse`（椭圆，默认）
- **大小**：`closest-side`/`farthest-side`/`closest-corner`/`farthest-corner`（默认）
- **位置**：`at center`/`at top left`/`at 50% 50%`

## 实现方案
```css
:root {
  --color-primary: #5e6ad2;
  --color-secondary: #a8b1ff;
  --color-accent: #ff6b6b;
}

/* ① 基础圆形渐变 */
.c-circle {
  background: radial-gradient(
    circle,
    var(--color-primary),
    var(--color-secondary)
  );
}

/* ② 椭圆渐变（默认） */
.c-ellipse {
  background: radial-gradient(
    var(--color-primary),
    var(--color-secondary)
  );
}

/* ③ 位置控制：高光在左上角 */
.c-highlight {
  background: radial-gradient(
    circle at top left,
    rgba(255, 255, 255, 0.4),
    transparent 60%
  );
}

/* ④ 大小关键字：closest-side 贴边 */
.c-closest-side {
  background: radial-gradient(
    circle closest-side at center,
    var(--color-primary),
    transparent
  );
}

/* ⑤ 按钮高光：双层渐变叠加 */
.c-btn-glow {
  background:
    radial-gradient(
      circle at 30% 30%,
      rgba(255, 255, 255, 0.5),
      transparent 50%
    ),
    var(--color-primary);
}

/* ⑥ 卡片光晕：从中心向外淡出 */
.c-card-glow {
  background: radial-gradient(
    circle at center,
    var(--color-primary) 0%,
    transparent 70%
  );
  filter: blur(20px);                      /* 模糊形成光晕 */
}

/* ⑦ 聚光灯效果：椭圆 + 偏移位置 */
.c-spotlight {
  background: radial-gradient(
    ellipse 60% 80% at 50% 30%,
    rgba(94, 106, 210, 0.4),
    transparent
  );
}

/* ⑧ 多色径向：环形效果 */
.c-rings {
  background: radial-gradient(
    circle,
    var(--color-primary) 0% 20%,
    var(--color-secondary) 20% 40%,
    var(--color-accent) 40% 60%,
    var(--color-primary) 60% 80%,
    var(--color-secondary) 80% 100%
  );
}

/* ⑨ 雷达扫描：conic + radial 配合 */
.c-radar {
  background:
    radial-gradient(circle, transparent 0% 80%, var(--color-primary) 80% 100%),
    conic-gradient(var(--color-primary) 0deg, transparent 90deg, transparent 360deg);
  border-radius: 50%;
  animation: spin 4s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ⑩ 暗黑模式光晕 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #8b95ff;
  }
  .c-card-glow {
    background: radial-gradient(
      circle at center,
      rgba(139, 149, 255, 0.3) 0%,
      transparent 70%
    );
  }
}
```

## 执行步骤
1. 用 `radial-gradient(形状 at 位置, 起始色, 结束色)` 创建径向渐变
2. 形状选 `circle`（圆形）或 `ellipse`（椭圆，默认）
3. 位置用 `at center`/`at top left`/`at 50% 30%` 精确控制
4. 大小用 `closest-side`/`farthest-corner` 控制辐射范围
5. 按钮高光：白色透明渐变叠加在纯色背景上
6. 光晕效果：径向渐变 + `filter: blur()` 模糊
7. 多色径向用相同位置（`20% 20%`）制造环形硬边
8. 颜色统一用 CSS 变量，暗黑模式只改变量值

## 兼容性
- Chrome: 26+
- Firefox: 16+
- Safari: 6.1+（部分需 `-webkit-`）
- Edge: 12+

## 降级方案
```css
/* 不支持 radial-gradient 时降级到纯色或 linear */
@supports not (background: radial-gradient(red, blue)) {
  .c-circle {
    background: var(--color-primary);
  }
  .c-highlight {
    background: linear-gradient(
      to bottom right,
      rgba(255, 255, 255, 0.4),
      transparent
    );
  }
}

/* 不支持 filter: blur 时降级到半透明阴影 */
@supports not (filter: blur(10px)) {
  .c-card-glow {
    box-shadow: 0 0 60px var(--color-primary);
  }
}

/* 老版浏览器前缀 */
@supports (-webkit-radial-gradient(red, blue)) and (not (radial-gradient(red, blue))) {
  .c-circle {
    background: -webkit-radial-gradient(circle, var(--color-primary), var(--color-secondary));
  }
}
```

## 相关链接
- [[linear-gradient-线性渐变]] - 线性渐变基础
- [[conic-gradient-锥形渐变]] - 锥形渐变（角度辐射）
- [[渐变实现复杂背景]] - 多层径向叠加
- [[00-MOC-渐变]]
