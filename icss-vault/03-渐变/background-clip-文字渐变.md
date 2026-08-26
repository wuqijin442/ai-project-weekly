---
title: background-clip 文字渐变
type: technique
tags:
  - icss/03-渐变/文字
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[linear-gradient-线性渐变]]"
  - "[[conic-gradient-锥形渐变]]"
  - "[[CSS变量复用动画函数]]"
---

# background-clip 文字渐变

## 问题/场景
标题渐变、品牌文字流光、渐变描边——`color` 只能设纯色，无法直接给文字应用渐变。`background-clip: text` 让背景被文字字形裁切，配合 `transparent` 文字色实现渐变文字。这是品牌设计高频需求。

## 核心原理
- `background-clip: text`：背景被文字字形作为 mask 裁切，仅文字内部显示背景
- `-webkit-text-fill-color: transparent`：让文字本身的填充色透明，露出背景（兼容 Safari 必需）
- `color: transparent`：兜底方案，老版本浏览器用此让文字透明

**关键**：必须同时设置 `background-clip: text` 和 `-webkit-text-fill-color: transparent`，否则 Safari 不生效。`-webkit-background-clip: text` 是 Safari 必需前缀。

## 实现方案
```css
:root {
  --color-primary: #5e6ad2;
  --color-secondary: #a8b1ff;
  --color-accent: #ff6b6b;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}

/* ① 基础渐变文字 */
.c-gradient-text {
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  -webkit-background-clip: text;
          background-clip: text;
  -webkit-text-fill-color: transparent;
          color: transparent;             /* 兜底 */
}

/* ② 多色渐变文字 */
.c-multi-text {
  background: linear-gradient(
    90deg,
    var(--color-primary) 0%,
    var(--color-secondary) 50%,
    var(--color-accent) 100%
  );
  -webkit-background-clip: text;
          background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ③ 流光动画：背景位置移动 */
.c-shine {
  background: linear-gradient(
    90deg,
    var(--color-primary) 0%,
    var(--color-secondary) 25%,
    var(--color-accent) 50%,
    var(--color-secondary) 75%,
    var(--color-primary) 100%
  );
  background-size: 200% 100%;
  -webkit-background-clip: text;
          background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s linear infinite;
}
@keyframes shine {
  to { background-position: 200% 0; }
}

/* ④ 雷达扫描文字：conic-gradient + 旋转 */
.c-radar-text {
  background: conic-gradient(
    from 0deg,
    var(--color-primary),
    var(--color-secondary),
    var(--color-accent),
    var(--color-primary)
  );
  -webkit-background-clip: text;
          background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: spin 4s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }       /* 注意：会旋转整个元素 */
}

/* ⑤ 渐变描边：text-stroke + 渐变 */
.c-stroke-text {
  -webkit-text-stroke: 2px transparent;
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  -webkit-background-clip: text;
          background-clip: text;
  /* 仅描边显示渐变，文字内部透明 */
  color: var(--color-bg, #fff);
}

/* ⑥ 文字闪烁：透明度动画 */
.c-blink-text {
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
  -webkit-background-clip: text;
          background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: blink 2s ease-in-out infinite;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50%      { opacity: 0.4; }
}

/* ⑦ 暗黑模式适配 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #8b95ff;
    --color-secondary: #c5ccff;
  }
}

/* ⑧ 渐变链接 hover：变色 */
.c-link {
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
  background-size: 0% 100%;
  background-repeat: no-repeat;
  -webkit-background-clip: text;
          background-clip: text;
  -webkit-text-fill-color: transparent;
  transition: background-size 0.3s var(--ease-out);
}
.c-link:hover {
  background-size: 100% 100%;
}
```

## 执行步骤
1. 元素加 `background: linear-gradient(...)` 设置渐变背景
2. 加 `-webkit-background-clip: text` 和 `background-clip: text`（双重声明，兼容 Safari）
3. 加 `-webkit-text-fill-color: transparent` 让文字填充透明，露出背景
4. 兜底加 `color: transparent`，兼容老版本
5. 流光动画：`background-size: 200% 100%` + `background-position` 移动
6. 描边文字：`-webkit-text-stroke: 2px transparent` + 内部填充非透明色
7. 链接 hover：`background-size` 从 0% 到 100% 实现「渐变填充」效果
8. 颜色用 CSS 变量，暗黑模式只改变量值

## 兼容性
- Chrome: 49+（需 `-webkit-` 前缀到 49+）
- Firefox: 49+（无需前缀）
- Safari: 14+（之前需 `-webkit-` 前缀，现在仍推荐加）
- Edge: 79+
- 注意：`background-clip: text` 在某些老旧浏览器显示为纯色，需测试

## 降级方案
```css
/* 不支持 background-clip: text 时降级到纯色 */
@supports not ((-webkit-background-clip: text) or (background-clip: text)) {
  .c-gradient-text {
    background: none;
    color: var(--color-primary);
    -webkit-text-fill-color: currentColor;
  }
}

/* 同时检测前缀和标准属性 */
@supports not (background-clip: text) {
  @supports (-webkit-background-clip: text) {
    /* Safari 老版仅支持前缀，无需降级 */
  }
  @supports not (-webkit-background-clip: text) {
    .c-gradient-text {
      background: none;
      color: var(--color-primary);
    }
  }
}

/* prefers-reduced-motion：禁用流光动画 */
@media (prefers-reduced-motion: reduce) {
  .c-shine,
  .c-radar-text {
    animation: none;
  }
}
```

## 相关链接
- [[linear-gradient-线性渐变]] - 渐变背景基础
- [[conic-gradient-锥形渐变]] - 雷达扫描文字
- [[CSS变量复用动画函数]] - 动画参数统一管理
- [[00-MOC-渐变]]
- [[00-MOC-文字]] - 文字特效分类
