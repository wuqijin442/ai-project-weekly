---
title: CSS 三角函数 sin/cos/tan
type: technique
tags:
  - icss/现代特性/计算
  - 难度/高级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[容器查询单位]]"
  - "[[路径动画×滚动驱动]]"
  - "[[animation-composition-动画合成]]"
---

# CSS 三角函数 sin/cos/tan

## 问题/场景
实现圆周运动、波浪动画、振荡器等需要三角函数计算的场景。原本要靠 JS 每帧计算坐标，现在 CSS 原生支持 `sin()`/`cos()`/`tan()`，配合 `@property` 注册可动画的自定义属性，能纯 CSS 实现复杂的圆周/波动动画。

## 核心原理
CSS Values Level 4 引入三角函数：
- `sin(angle)` / `cos(angle)` / `tan(angle)`：角度转比值
- `asin(x)` / `acos(x)` / `atan(x)` / `atan2(y, x)`：比值转角度
- 常量 `pi`：圆周率
- 角度单位支持 `deg`/`rad`/`grad`/`turn`

关键技巧：用 `@property` 注册一个 `<angle>` 类型的自定义属性，让它**可参与动画**（普通 CSS 变量不可动画），然后在 `@keyframes` 中变化这个角度，再用 `sin(angle)`/`cos(angle)` 计算出 X/Y 坐标。

## 实现方案

### 圆周运动动画

```css
/* ① 注册可动画的角度变量 */
@property --angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

:root {
  --radius: 100px;
  --duration: 4s;
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
}

/* ② 圆周运动主体 */
.orbit {
  --angle: 0deg;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #00e5ff;

  /* 用 cos 算 X，用 sin 算 Y */
  transform:
    translate(
      calc(cos(var(--angle)) * var(--radius)),
      calc(sin(var(--angle)) * var(--radius))
    );

  /* 动画驱动 --angle 从 0 → 360deg */
  animation: spin var(--duration) linear infinite;
}

@keyframes spin {
  to { --angle: 360deg; }
}
```

### 波浪/振荡动画

```css
@property --phase {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

.wave-bar {
  --phase: 0deg;
  height: 50px;
  width: 8px;
  background: linear-gradient(to top, #00e5ff, #007bff);

  /* 用 sin 把高度做正弦波动 */
  transform: scaleY(calc(0.5 + sin(var(--phase)) * 0.5));
  transform-origin: bottom;
  animation: wave 1.5s ease-in-out infinite;
}

@keyframes wave {
  to { --phase: 360deg; }
}

/* 多个 bar 错开相位，形成波浪传递 */
.wave-bar:nth-child(1) { animation-delay: 0s; }
.wave-bar:nth-child(2) { animation-delay: 0.1s; }
.wave-bar:nth-child(3) { animation-delay: 0.2s; }
.wave-bar:nth-child(4) { animation-delay: 0.3s; }
.wave-bar:nth-child(5) { animation-delay: 0.4s; }
```

### 三角函数图案生成

```css
/* sin() 配合 background 生成正弦波图案 */
.wave-bg {
  background:
    radial-gradient(
      circle at calc(50% + cos(var(--t)) * 200px) calc(50% + sin(var(--t)) * 100px),
      #007bff 0,
      transparent 50px
    );
  animation: t 8s linear infinite;
}

@property --t {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

@keyframes t { to { --t: 360deg; } }
```

## 执行步骤
1. **用 @property 注册角度变量**：必须声明 `syntax: '<angle>'`，否则不可动画
2. **写 @keyframes 让角度从 0 转到 360deg**：循环驱动
3. **在 transform 中用 cos/sin 算坐标**：`cos(var(--angle)) * radius` 得 X，`sin` 得 Y
4. **波浪场景错开相位**：用 `animation-delay` 让多个元素相位不同
5. **验证 @property 支持**：Chrome 85+/Safari 16.4+/Firefox 128+ 支持

## 兼容性
- Chrome: 111+（三角函数）、85+（@property）
- Firefox: 128+
- Safari: 15.4+（三角函数）、16.4+（@property）

## 降级方案
```css
@supports not (cos(0deg)) {
  /* 老浏览器：用旋转父容器 + 反向旋转子元素实现圆周 */
  .orbit-wrapper {
    animation: spin var(--duration) linear infinite;
  }
  .orbit {
    transform: translateX(var(--radius));
  }
  /* 缺点：旋转会带动元素自身朝向改变，需要反向旋转修正 */
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
}

@supports not (background: paint(test)) {
  /* @property 不支持时，角度变化无法动画，需 JS 驱动 */
}
```

## 应用场景
| 场景 | 关键技巧 |
|------|----------|
| 圆周运动 | `cos(--angle) * r` + `sin(--angle) * r` |
| 钟摆 | `sin(--angle) * amplitude` 偏移 |
| 波浪传递 | 多元素 `animation-delay` 错开 |
| 弹簧 | `cos(--angle) * decay` 配合阻尼 |
| 角度计算 | `atan2(y, x)` 求两点连线角度 |

## 相关链接
- [[容器查询单位]]
- [[路径动画×滚动驱动]]
- [[animation-composition-动画合成]]
- [[00-MOC-现代特性]]
