---
title: perspective-透视
type: technique
tags:
  - icss/08-3D/基础
  - 难度/初级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[preserve-3d-3D空间]]"
  - "[[3D翻转卡片]]"
---

# perspective-透视

## 问题/场景
让 2D 平面上的元素呈现"近大远小"的立体透视效果。没有 `perspective`，所有 `rotateX/Y`、`translateZ` 都看不出立体感，只会被压扁。常见误区：`perspective` 属性 vs `perspective()` 函数分不清。

## 核心原理
- `perspective: <length>`：作用在**父元素**上，定义观察者到 z=0 平面的距离（景深）
  - 值越小透视越强（鱼眼效果），值越大透视越弱（接近正交投影）
  - 子元素的 `translateZ` 越大显得越大，越小（负值）显得越小
- `perspective-origin: x y`：观察点位置，默认 `50% 50%`（中心）
- `perspective()` 函数：写在元素**自身**的 `transform` 里，只对该元素生效，子元素不共享同一消失点
- 区别：父级 `perspective` 让多个子元素共享同一消失点（统一立体场景）；`perspective()` 各自独立（适合单个元素快速加 3D）

## 实现方案
```css
:root {
  --depth: 1000px;
  --card-color: #00e5ff;
  --bg-color: #0f172a;
}

/* 方案 A：父级 perspective，子元素共享消失点（推荐多元素场景） */
.scene {
  perspective: var(--depth);
  perspective-origin: 50% 50%; /* 观察点居中 */
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  background: var(--bg-color);
}

.scene .card {
  width: 160px;
  height: 200px;
  background: var(--card-color);
  transform: rotateY(45deg); /* 父有 perspective，立体感生效 */
  transition: transform 0.4s ease;
}

/* 方案 B：元素自身 perspective() 函数（单元素快速 3D） */
.solo-card {
  width: 160px;
  height: 200px;
  background: var(--card-color);
  /* perspective() 写在 transform 第一个，作用于后续 3D 变换 */
  transform: perspective(800px) rotateY(45deg);
}

/* 多元素共享同一消失点对比：父级 perspective 让三张卡片像在同一空间 */
.scene .card:nth-child(1) { transform: rotateY(-30deg) translateZ(-50px); }
.scene .card:nth-child(2) { transform: rotateY(0deg); }
.scene .card:nth-child(3) { transform: rotateY(30deg) translateZ(-50px); }

@media (prefers-color-scheme: dark) {
  :root { --bg-color: #f8fafc; --card-color: #60a5fa; }
}
```

## 执行步骤
1. 在**父容器**上加 `perspective: 1000px`（典型值 800-2000px，越小越夸张）
2. 子元素用 `transform: rotateY/rotateX/translateZ` 进行 3D 变换
3. 想改变观察点（比如俯视）就调父级 `perspective-origin: 50% 0%`
4. 单个元素快速加 3D 用 `transform: perspective(800px) rotateY(45deg)`，但多元素不要用此方式（消失点不一致）
5. 暗黑模式只切换背景与卡片颜色变量

## 兼容性
- Chrome: 36+
- Firefox: 16+
- Safari: 9+
- 移动端：全面支持

## 降级方案
```css
@supports not (perspective: 1000px) {
  .scene .card {
    /* 不支持 3D 时降级为 2D 倾斜 */
    transform: skewX(-15deg);
  }
}
```

## 相关链接
- [[preserve-3d-3D空间]] - preserve-3d 才能让子元素保持 3D 位置
- [[3D翻转卡片]] - perspective 的经典应用
- [[00-MOC-3D]]
