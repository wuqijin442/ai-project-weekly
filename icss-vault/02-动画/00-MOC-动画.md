---
title: 动画 MOC
type: MOC
tags:
  - moc
  - icss/02-动画
created: 2026-07-04
---

# 📂 动画 · MOC

> 收集 CSS 动画核心技巧。核心原则：**仅对 transform/opacity 做动画**，避免重排重绘；动画时长 0.2s-0.5s，优先 `cubic-bezier` 缓动；用 CSS 变量统一管理动画参数。

## 📋 笔记列表

### 基础原则
- [[动画核心原则]] - 性能优先、will-change 使用、cubic-bezier 缓动
- [[CSS变量复用动画函数]] - 变量统一管理 duration/easing，配合 @property

### 过渡与关键帧
- [[transition-过渡技巧]] - transitionend 事件、hover 暂停、复用变量
- [[keyframes-关键帧]] - @keyframes 语法、alternate/reverse、forwards 终态
- [[animation-动画属性]] - 简写、delay 负值、steps() 步进、play-state 暂停

### 进阶技巧
- [[滚动驱动动画-ScrollTimeline]] - animation-timeline: scroll()/view()
- [[单标签加载动画]] - 单标签 loading、box-shadow 多边框、conic-gradient
- [[hover-暂停最后一帧]] - play-state 切换 + forwards 单次播放

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| hover 过渡 | `transition: transform 0.3s cubic-bezier(0.4,0,0.2,1)` | [[transition-过渡技巧]] |
| 循环动画 | `animation: spin 1s infinite linear` | [[keyframes-关键帧]] |
| 步进动画 | `animation-timing-function: steps(8)` | [[animation-动画属性]] |
| 滚动驱动 | `animation-timeline: scroll()` | [[滚动驱动动画-ScrollTimeline]] |
| 单次播放保持终态 | `animation-fill-mode: forwards` | [[hover-暂停最后一帧]] |
| 性能优化 | `will-change: transform` + 仅 transform 动画 | [[动画核心原则]] |
| loading 圈 | 单标签 + `conic-gradient` + `mask` | [[单标签加载动画]] |
| 统一缓动 | `--ease: cubic-bezier(0.4,0,0.2,1)` 全局复用 | [[CSS变量复用动画函数]] |

## 🔗 关联分类
- [[00-MOC]]
- [[00-MOC-布局]] - 布局过渡动画
- [[00-MOC-渐变]] - 渐变动画、conic-gradient loading
- [[00-MOC-性能]] - will-change、contain、content-visibility
- [[00-MOC-前沿特性]] - animation-composition 多动画合成
