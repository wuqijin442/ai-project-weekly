---
title: 纯CSS下拉菜单
type: technique
tags:
  - icss/09-交互/下拉菜单
  - 难度/初级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[纯CSS弹窗]]"
  - "[[00-MOC-选择器]]"
---

# 纯CSS下拉菜单

## 问题/场景
不写 JS 实现下拉菜单的展开/收起。`hover` 在移动端失效，`focus-within` 更友好（支持键盘 Tab 切换），`details/summary` 是 HTML5 原生方案。

## 核心原理
- `:hover`：鼠标悬停展开，移动端无效，且点击菜单项后会失去焦点而收起
- `:focus-within`：元素或其子元素获得焦点时触发，支持键盘，鼠标点击菜单项时焦点仍在容器内不会收起
- `<details>`/`<summary>`：HTML5 原生折叠组件，`open` 属性控制状态，无需任何 CSS 即可工作
- 多级菜单：嵌套 `details` 或嵌套 `:focus-within` 容器

## 实现方案
```css
:root {
  --menu-bg: #ffffff;
  --menu-hover: #f1f5f9;
  --text-color: #0f172a;
  --border-color: #e2e8f0;
}

/* === 方案 1：:focus-within（推荐） === */
.dropdown {
  position: relative;
  display: inline-block;
}
.dropdown-trigger {
  padding: 8px 16px;
  background: var(--menu-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  cursor: pointer;
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 160px;
  background: var(--menu-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  margin-top: 4px;
  padding: 4px;
  list-style: none;
  /* 默认隐藏：用 opacity + visibility 避免动画后仍可点击 */
  opacity: 0;
  visibility: hidden;
  transform: translateY(-8px);
  transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s ease;
}
.dropdown:focus-within .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
.dropdown-menu a {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  color: var(--text-color);
  text-decoration: none;
  border-radius: 4px;
  /* 触摸目标最小 44×44，padding 8 12 配合行高约达标 */
  min-height: 44px;
}
.dropdown-menu a:hover,
.dropdown-menu a:focus {
  background: var(--menu-hover);
  outline: none;
}

/* === 方案 2：details/summary 原生方案 === */
details.dropdown-native {
  position: relative;
  display: inline-block;
}
details.dropdown-native summary {
  padding: 8px 16px;
  background: var(--menu-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  cursor: pointer;
  list-style: none; /* 移除默认三角 */
  display: inline-block;
}
details.dropdown-native summary::-webkit-details-marker {
  display: none; /* Safari 移除三角 */
}
details.dropdown-native[open] .dropdown-menu {
  /* 用动画增强体验 */
  animation: slideDown 0.2s ease forwards;
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* === 方案 3：多级菜单（嵌套 :focus-within） === */
.dropdown-multi .sub {
  position: relative;
}
.dropdown-multi .sub-menu {
  position: absolute;
  left: 100%;
  top: 0;
  opacity: 0;
  visibility: hidden;
  transform: translateX(8px);
  transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s ease;
}
.dropdown-multi .sub:focus-within .sub-menu {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}

@media (prefers-color-scheme: dark) {
  :root {
    --menu-bg: #1e293b;
    --menu-hover: #334155;
    --text-color: #f8fafc;
    --border-color: #334155;
  }
}
```

## 执行步骤
1. **选方案**：现代浏览器用 `:focus-within`（键盘友好），原生组件用 `<details>`
2. `:focus-within` 方案：容器内放触发器与菜单，菜单默认 `opacity: 0; visibility: hidden`
3. 容器 `:focus-within .menu` 时显示，触发器用 `<a>` 或 `<button>` 保证可 Tab 聚焦
4. `details` 方案：`<summary>` 是触发器，`[open]` 属性控制状态，无需 JS
5. 多级菜单：嵌套子容器 + `:focus-within`，子菜单 `left: 100%` 从右侧展开
6. 暗黑模式只切换菜单背景与文字变量

## 兼容性
- `:focus-within`：Chrome 60+、Firefox 52+、Safari 10.1+
- `<details>`：全浏览器支持（IE 除外）
- 多级 `:focus-within`：同上

## 降级方案
```css
@supports not (selector(:focus-within)) {
  /* 不支持 focus-within 时降级为 :hover */
  .dropdown:hover .dropdown-menu {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
}
```

## 相关链接
- [[纯CSS弹窗]] - 同类状态切换
- [[00-MOC-选择器]] - :focus-within 原理
- [[00-MOC-交互]]
