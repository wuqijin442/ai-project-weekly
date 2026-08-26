---
title: CSS Houdini
type: technique
tags:
  - icss/前沿特性/扩展
  - 难度/高级
  - 兼容性/渐进
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[CSS三角函数]]"
  - "[[Liquid-Glass-液态玻璃]]"
  - "[[transform-硬件加速]]"
---

# CSS Houdini

## 问题/场景
CSS 内置属性和函数有限，复杂效果（自定义背景图案、自定义布局、可动画的自定义属性）要么靠 hack，要么靠 JS 操纵 DOM。我们希望直接扩展 CSS 引擎能力，让开发者写「真正的 CSS」实现复杂效果。

## 核心原理
CSS Houdini 是一组底层 API，让 JS 能直接介入浏览器的样式/布局/绘制流程：

| API | 作用 | 状态 |
|-----|------|------|
| **Paint API** | 用 JS Canvas 绘制 CSS 背景/边框 | Chrome 65+/Safari 16.4+ ✅ |
| **Layout API** | 用 JS 自定义布局算法 | 实验性 ⚠️ |
| **Worklet** | 在主线程外运行的轻量 JS | 配合上述 API |
| **@property** | 注册自定义属性，支持类型/动画 | Chrome 85+/Safari 16.4+ ✅ |
| **Typed OM** | 类型化的 CSS 对象模型 | Chrome 66+/Safari 16.4+ ✅ |
| **Properties & Values API** | 注册全局 CSS 变量 | 部分 ✅ |

最常用的是 **Paint API** 和 **@property**。

## 实现方案

### @property 注册可动画属性

```css
/* ① 注册自定义属性，声明类型 */
@property --angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

@property --color-hue {
  syntax: '<number>';
  inherits: false;
  initial-value: 180;
}

/* ② 注册后可参与动画（普通 CSS 变量不可动画） */
.spinner {
  --angle: 0deg;
  transform: rotate(var(--angle));
  animation: spin 2s linear infinite;
}

@keyframes spin {
  to { --angle: 360deg; }
}

/* 颜色平滑过渡（不用 @property 时颜色突变） */
.color-shift {
  --color-hue: 180;
  background: hsl(var(--color-hue), 70%, 50%);
  animation: hue 3s linear infinite;
}

@keyframes hue {
  to { --color-hue: 540; }  /* 平滑过渡 180 → 540 */
}
```

### Paint API 自定义绘制

```javascript
// 1. 定义 Paint Worklet（单独 JS 文件，如 ripple-paint.js）
class RipplePainter {
  static get inputProperties() {
    return ['--ripple-color', '--ripple-size'];
  }

  paint(ctx, size, props) {
    const color = props.get('--ripple-color').toString() || '#007bff';
    const radius = parseFloat(props.get('--ripple-size')) || 50;

    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(size.width / 2, size.height / 2, radius, 0, Math.PI * 2);
    ctx.fill();
  }
}

registerPaint('ripple', RipplePainter);
```

```javascript
// 2. 主线程注册 Worklet
if ('paintWorklet' in CSS) {
  CSS.paintWorklet.addModule('/ripple-paint.js');
}
```

```css
/* 3. CSS 中使用 */
.ripple-bg {
  --ripple-color: #007bff;
  --ripple-size: 50;
  background: paint(ripple);
  width: 200px;
  height: 200px;
}
```

### Paint API 实战：渐变边框

```javascript
// gradient-border.js
class GradientBorderPainter {
  static get inputProperties() {
    return ['--border-width', '--gradient-angle'];
  }

  paint(ctx, size, props) {
    const borderWidth = parseFloat(props.get('--border-width')) || 2;
    const angle = props.get('--gradient-angle').value || 0;

    const gradient = ctx.createLinearGradient(0, 0, size.width, size.height);
    gradient.addColorStop(0, '#007bff');
    gradient.addColorStop(0.5, '#00e5ff');
    gradient.addColorStop(1, '#007bff');

    ctx.lineWidth = borderWidth;
    ctx.strokeStyle = gradient;
    ctx.strokeRect(
      borderWidth / 2,
      borderWidth / 2,
      size.width - borderWidth,
      size.height - borderWidth
    );
  }
}
registerPaint('gradient-border', GradientBorderPainter);
```

```css
.gradient-border-box {
  --border-width: 3;
  background: paint(gradient-border);
  border-radius: 8px;
  padding: 16px;
}
```

### Typed OM 类型化操作

```javascript
// 传统 CSSOM（字符串操作，易错）
element.style.opacity = '0.5';

// Typed OM（类型化，性能更好）
const opacity = element.attributeStyleMap.get('opacity');  // CSSUnitValue
element.attributeStyleMap.set('opacity', CSS.number(0.5));

// 计算值
const computed = element.computedStyleMap().get('width');  // CSSUnitValue {value: 200, unit: 'px'}
console.log(computed.value, computed.unit);  // 200 'px'
```

### Properties & Values API 注册全局变量

```javascript
// 注册全局 CSS 变量，带类型和默认值
if ('registerProperty' in CSS) {
  CSS.registerProperty({
    name: '--theme-primary',
    syntax: '<color>',
    inherits: true,
    initialValue: '#007bff'
  });
}
```

```css
/* 注册后变量有类型，可参与动画和计算 */
.button {
  background: var(--theme-primary);
  transition: --theme-primary 0.3s;  /* 颜色可平滑过渡 */
}
.button:hover {
  --theme-primary: #00e5ff;
}
```

## 执行步骤
1. **@property 注册自定义属性**：声明 `syntax` 类型，让变量可动画
2. **Paint API 写 Worklet 类**：实现 `paint(ctx, size, props)` 方法
3. **主线程注册 Worklet**：`CSS.paintWorklet.addModule('xxx.js')`
4. **CSS 中用 `paint(name)` 调用**：传入 `inputProperties` 读取 CSS 变量
5. **检测支持并降级**：`@supports` + `if ('paintWorklet' in CSS)`

## 兼容性
| API | Chrome | Firefox | Safari |
|-----|--------|---------|--------|
| Paint API | 65+ | 不支持 | 16.4+ |
| @property | 85+ | 128+ | 16.4+ |
| Typed OM | 66+ | 不支持 | 16.4+ |
| Layout API | 实验性 | 不支持 | 不支持 |
| Properties & Values API | 85+ | 不支持 | 16.4+ |

## 降级方案
```css
/* @property 不支持时，自定义变量不可动画，降级到 @keyframes 直接动画属性 */
@supports not (background: paint(test)) {
  .ripple-bg {
    background: radial-gradient(circle, #007bff 0, transparent 70%);
  }
}

@supports not (at-rules: @property) {
  /* 颜色突变（无平滑过渡） */
  .color-shift:hover {
    background: hsl(540, 70%, 50%);
  }
}
```

```javascript
// JS 端检测 Paint API 支持
if ('paintWorklet' in CSS) {
  CSS.paintWorklet.addModule('/paint.js');
} else {
  // 降级：用 SVG 背景或图片
  document.body.classList.add('no-paint-api');
}
```

## @property syntax 类型
| 类型 | 示例 |
|------|------|
| `<angle>` | `0deg`, `45deg`, `1rad` |
| `<color>` | `#fff`, `red`, `hsl(180,50%,50%)` |
| `<length>` | `10px`, `1em`, `100%` |
| `<number>` | `1`, `1.5`, `-3.14` |
| `<percentage>` | `50%` |
| `<time>` | `0.3s`, `200ms` |
| `<url>` | `url(image.png)` |
| `<integer>` | `1`, `-3` |
| `*` | 任意值（不推荐，丢失类型） |

## 应用场景
| 场景 | API | 优势 |
|------|-----|------|
| 圆周运动 | @property + `<angle>` | 角度可动画 |
| 颜色平滑过渡 | @property + `<color>` | 颜色变量可过渡 |
| 自定义背景图案 | Paint API | 任意 Canvas 绘制 |
| 自定义边框 | Paint API | 渐变边框、波浪边框 |
| 自定义布局 | Layout API | 替代 Flex/Grid |
| 高效样式操作 | Typed OM | 类型化、高性能 |

## 相关链接
- [[CSS三角函数]]
- [[Liquid-Glass-液态玻璃]]
- [[transform-硬件加速]]
- [[00-MOC-前沿特性]]
