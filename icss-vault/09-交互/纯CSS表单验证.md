---
title: 纯CSS表单验证
type: technique
tags:
  - icss/09-交互/表单
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[纯CSS下拉菜单]]"
  - "[[00-MOC-选择器]]"
---

# 纯CSS表单验证

## 问题/场景
不写 JS 实现表单校验提示：邮箱格式错误显示红框、密码强度提示、必填项校验。利用 HTML5 `required`/`pattern` + CSS `:valid`/`:invalid`/`:user-invalid` 伪类。

## 核心原理
- `:valid`：表单元素通过校验时匹配
- `:invalid`：校验失败时匹配（即使未交互过）
- `:user-invalid`（现代）：用户**交互后**仍无效才匹配，比 `:invalid` 更友好（不会一进页面就报错）
- `pattern` 属性：用正则约束输入格式（如邮箱、手机号）
- `:placeholder-shown`：占位符仍显示时（即用户没输入），可反向控制"未输入时不显示错误"
- `required` 属性：必填项，空值时 `:invalid`

## 实现方案
```css
:root {
  --success-color: #10b981;
  --error-color: #ef4444;
  --input-border: #e2e8f0;
  --input-bg: #ffffff;
  --text-color: #0f172a;
}

.form-field {
  position: relative;
  margin-bottom: 20px;
}

.form-field input {
  width: 100%;
  padding: 12px 40px 12px 16px; /* 右侧留出图标空间 */
  border: 2px solid var(--input-border);
  border-radius: 8px;
  background: var(--input-bg);
  color: var(--text-color);
  font-size: 16px;
  transition: border-color 0.2s ease;
  min-height: 44px; /* 触摸目标 */
  box-sizing: border-box;
}

/* 默认 placeholder-shown 时不显示错误（用户没输入） */
.form-field input:not(:placeholder-shown):invalid,
.form-field input:user-invalid {
  border-color: var(--error-color);
}

.form-field input:not(:placeholder-shown):valid {
  border-color: var(--success-color);
}

/* 用 :has() 让父容器根据 input 状态显示图标 */
.form-field::after {
  content: '';
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
  display: grid;
  place-items: center;
  font-size: 18px;
  font-weight: 900;
}

/* 校验通过显示 ✓ */
.form-field:has(input:not(:placeholder-shown):valid)::after {
  content: '✓';
  opacity: 1;
  color: var(--success-color);
}

/* 校验失败显示 ✗ */
.form-field:has(input:invalid:not(:placeholder-shown))::after {
  content: '✗';
  opacity: 1;
  color: var(--error-color);
}

/* 错误提示文案 */
.form-field .error-msg {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: var(--error-color);
  opacity: 0;
  transform: translateY(-4px);
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.form-field:has(input:user-invalid) .error-msg {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-color-scheme: dark) {
  :root { --input-bg: #1e293b; --text-color: #f8fafc; --input-border: #334155; }
}
```

HTML 示例：
```html
<div class="form-field">
  <input type="email" placeholder=" " required
         pattern="[^@]+@[^@]+\.[^@]+">
  <span class="error-msg">请输入有效邮箱</span>
</div>
```

## 执行步骤
1. `<input>` 加 `required`（必填）、`type="email"`（类型校验）、`pattern="正则"`（自定义格式）
2. `placeholder=" "`（注意是空格）让 `:placeholder-shown` 在没输入时为 true，避免一进页面就报红
3. `:invalid:not(:placeholder-shown)` 才显示错误：用户输入了内容且不合法
4. `:user-invalid` 更友好：只有用户交互过且仍非法才报错（Chrome 119+）
5. 用 `:has()` 让父容器根据 input 状态显示图标/文案，无需 JS 添加类名
6. 暗黑模式切换输入框背景与文字变量

## 兼容性
- `:valid`/`:invalid`：全浏览器支持
- `:user-invalid`：Chrome 119+、Firefox 117+、Safari 17.4+（较新）
- `:placeholder-shown`：Chrome 47+、Firefox 51+、Safari 9+
- `:has()`：Chrome 105+、Firefox 121+、Safari 15.4+

## 降级方案
```css
@supports not (selector(:has(*))) {
  /* 不支持 :has() 时，用相邻兄弟选择器 */
  input:not(:placeholder-shown):invalid + .error-msg {
    opacity: 1;
    transform: translateY(0);
  }
  /* 图标改用 input 自身背景图 */
  input:not(:placeholder-shown):valid {
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg">✓</svg>');
    background-position: right 12px center;
    background-repeat: no-repeat;
  }
}

@supports not (selector(:user-invalid)) {
  /* 降级为 :invalid + :focus 组合 */
  input:focus:invalid:not(:placeholder-shown) + .error-msg {
    opacity: 1;
  }
}
```

## 相关链接
- [[纯CSS下拉菜单]] - 同类伪类驱动交互
- [[00-MOC-选择器]] - :has()/:user-invalid 原理
- [[00-MOC-交互]]
