---
title: 纯CSS弹窗
type: technique
tags:
  - icss/09-交互/弹窗
  - 难度/中级
  - 兼容性/渐进
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[纯CSS下拉菜单]]"
  - "[[00-MOC-前沿特性]]"
---

# 纯CSS弹窗

## 问题/场景
不写 JS 实现弹窗（Modal）的打开/关闭。三种方案各有适用：`:target` 适合 URL 锚点跳转；`:checked + label` 适合状态切换；`popover` 属性（Chrome 114+）是现代标准方案，自带 ESC 关闭与点击遮罩关闭。

## 核心原理
- **方案 1：`:target`**：URL hash 变化时，匹配 ID 的元素被 `:target` 选中。点击 `<a href="#modal">` 打开，`<a href="#">` 关闭
- **方案 2：`:checked + label`**：隐藏 `<input type="checkbox">`，用 `<label>` 关联切换。`:checked ~ .modal` 控制显示
- **方案 3：`popover` 属性**（推荐）：元素加 `popover` 属性，调用 `.showPopover()` 或 `<button popovertarget>` 即可显示，浏览器自动管理焦点、ESC 关闭、点击外关闭

## 实现方案
```css
:root {
  --overlay-bg: rgba(0, 0, 0, 0.5);
  --modal-bg: #ffffff;
  --text-color: #0f172a;
  --accent: #00e5ff;
}

/* === 方案 1：:target 弹窗 === */
.modal-target {
  position: fixed;
  inset: 0;
  display: grid;
  place-items: center;
  background: var(--overlay-bg);
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
  z-index: 100;
}
.modal-target:target {
  opacity: 1;
  visibility: visible;
}

/* === 方案 2：:checked + label 弹窗 === */
.modal-toggle {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}
.modal-checked {
  position: fixed;
  inset: 0;
  display: grid;
  place-items: center;
  background: var(--overlay-bg);
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
  z-index: 100;
}
.modal-toggle:checked ~ .modal-checked {
  opacity: 1;
  visibility: visible;
}

/* === 方案 3：popover 属性（现代标准） === */
.modal-popover {
  /* popover 属性自动设置定位与层级 */
  background: var(--modal-bg);
  color: var(--text-color);
  border: none;
  border-radius: 12px;
  padding: 24px;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  /* popover 默认 margin: auto 居中 */
}

/* popover 显示/隐藏动画：用 @starting-style 或 transition */
.modal-popover::backdrop {
  background: var(--overlay-bg);
}

@media (prefers-color-scheme: dark) {
  :root { --modal-bg: #1e293b; --text-color: #f8fafc; }
}
```

HTML 结构对照：
```html
<!-- 方案 1：:target -->
<a href="#modal1">打开</a>
<div id="modal1" class="modal-target">
  <div>内容 <a href="#">关闭</a></div>
</div>

<!-- 方案 2：:checked -->
<input type="checkbox" id="t1" class="modal-toggle">
<label for="t1">打开</label>
<div class="modal-checked">
  <div>内容 <label for="t1">关闭</label></div>
</div>

<!-- 方案 3：popover（推荐） -->
<button popovertarget="modal3">打开</button>
<div id="modal3" class="modal-popover" popover>
  内容
  <button popovertarget="modal3" popovertargetaction="hide">关闭</button>
</div>
```

## 执行步骤
1. **选方案**：现代浏览器优先 `popover` 属性，兼容旧浏览器用 `:checked`，需要 URL 直链打开用 `:target`
2. **:target 实现**：弹窗加 `id`，链接 `href="#id"` 打开，关闭链接 `href="#"`
3. **:checked 实现**：隐藏 checkbox，`<label for>` 切换，`:checked ~ .modal` 控制显示
4. **popover 实现**：元素加 `popover` 属性，按钮 `popovertarget="id"` 触发，浏览器自动管理 ESC 与点击外关闭
5. 显示/隐藏用 `opacity + visibility` 双属性过渡（避免动画结束仍可点击）
6. 暗黑模式切换弹窗背景变量

## 兼容性
- `:target`：全浏览器支持
- `:checked`：全浏览器支持
- `popover` 属性：Chrome 114+、Edge 114+、Safari 17+、Firefox 125+
- 配合 `Anchor Positioning`（Chrome 125+）可精准定位

## 降级方案
```css
@supports not (popover: auto) {
  /* 不支持 popover 时降级为 :checked 方案 */
  .modal-popover {
    position: fixed;
    inset: 0;
    display: grid;
    place-items: center;
    background: var(--modal-bg);
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.3s ease, visibility 0.3s ease;
  }
  /* 需配合 checkbox + label 控制 */
}
```

## 相关链接
- [[纯CSS下拉菜单]] - 同类状态切换思路
- [[00-MOC-前沿特性]] - popover 与 Anchor Positioning
- [[00-MOC-交互]]
