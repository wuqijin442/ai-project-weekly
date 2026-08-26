---
title: 交互 MOC
type: MOC
tags:
  - moc
  - icss/09-交互
created: 2026-07-04
---

# 📂 交互 · MOC

> 纯 CSS 实现交互：用 `:target`、`:checked`、`:focus-within`、`:valid/:invalid` 等伪类驱动状态切换，配合 `popover`、`details` 等原生元素减少 JS 依赖。鼠标跟随等场景用最小 JS 改 CSS 变量。

## 📋 笔记列表

### 状态切换
- [[纯CSS弹窗]] - :target/:checked/popover 实现弹窗
- [[纯CSS下拉菜单]] - :hover/:focus-within + details/summary
- [[纯CSS表单验证]] - :valid/:invalid + pattern + :placeholder-shown

### 鼠标与拖拽
- [[鼠标跟随效果]] - CSS 变量 + 最小 JS 实现光晕跟随
- [[拖拽交互]] - HTML5 drag API 视觉反馈 + input range 美化

## 🎯 核心速查

| 场景 | 方案 | 笔记 |
|------|------|------|
| 弹窗 | popover 属性（Chrome 114+） | [[纯CSS弹窗]] |
| URL 弹窗 | :target 选择器 | [[纯CSS弹窗]] |
| 复选框弹窗 | :checked + label | [[纯CSS弹窗]] |
| 下拉菜单 | :focus-within 或 details | [[纯CSS下拉菜单]] |
| 表单校验 | :invalid + pattern | [[纯CSS表单验证]] |
| 鼠标光晕 | --x/--y 变量 + JS 监听 | [[鼠标跟随效果]] |
| 滑块 | input range + appearance: none | [[拖拽交互]] |

## 🔗 关联分类
- [[00-MOC-选择器]] - 伪类驱动交互的核心
- [[00-MOC-动画]] - 交互动效
- [[00-MOC]]
