---
title: 文字 MOC
type: MOC
tags:
  - moc
  - icss/07-文字
created: 2026-07-04
---

# 📂 文字 · MOC

> CSS 文字特效核心：渐变、描边、打字机、溢出省略、可变字体。原则是单标签优先、CSS 变量管理、暗黑主题友好。

## 📋 笔记列表

### 文字视觉
- [[渐变文字]] - background-clip: text 实现渐变与流动动画
- [[文字描边]] - -webkit-text-stroke 与 paint-order 控制描边层级
- [[可变字体]] - font-variation-settings 单文件多字重

### 文字动效
- [[打字机效果]] - steps() 步进函数与 ch 单位实现逐字输出

### 文字布局
- [[文字溢出省略]] - 单行/多行省略与 Flex min-width: 0 坑

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| 渐变文字 | background-clip: text + text-fill-color: transparent | [[渐变文字]] |
| 描边文字 | -webkit-text-stroke + paint-order: stroke fill | [[文字描边]] |
| 打字机 | steps(n) + ch 宽度 + 光标闪烁 | [[打字机效果]] |
| 单行省略 | white-space + overflow + text-overflow | [[文字溢出省略]] |
| 多行省略 | -webkit-line-clamp + display: -webkit-box | [[文字溢出省略]] |
| 字重过渡 | font-variation-settings + transition | [[可变字体]] |

## 🔗 关联分类
- [[00-MOC-渐变]] - 渐变是文字特效的基础
- [[00-MOC-动画]] - steps() 与 keyframes 原理
- [[00-MOC]]
