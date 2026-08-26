---
title: ":nth-child 奇技淫巧"
type: technique
tags:
  - icss/选择器/nth-child
  - 难度/中级
  - 兼容性/现代
created: 2026-07-04
source: https://github.com/chokcoco/iCSS
related:
  - "[[is-where-选择器分组]]"
  - "[[has-父选择器]]"
---

# :nth-child 奇技淫巧

## 问题/场景
列表/表格场景需要精准定位元素：斑马纹（奇偶行）、首末元素特殊处理、选中第 N 到第 M 个、每隔 3 个变色、倒数第 2 个去掉边框。`:nth-child` 系列伪类用 `an+b` 公式精准定位，是列表美化的核心武器。

## 核心原理
`:nth-child(an+b)` 按公式匹配兄弟元素中第几个。`a` 是步长，`b` 是起始偏移，`n` 从 0 开始递增。

**公式速查**：
| 公式 | 匹配元素 | 场景 |
|------|----------|------|
| `odd` / `2n+1` | 第 1、3、5… | 斑马纹奇数行 |
| `even` / `2n` | 第 2、4、6… | 斑马纹偶数行 |
| `first-child` | 第 1 个 | 首元素 |
| `last-child` | 最后 1 个 | 末元素 |
| `n+4` | 第 4、5、6…（含第 4 起） | 跳过前 3 个 |
| `-n+3` | 第 1、2、3（前 3 个） | 只选前 3 个 |
| `3n` | 第 3、6、9… | 每 3 个一组 |
| `3n+1` | 第 1、4、7… | 每组第 1 个 |

**组合技巧**：两个 `:nth-child` 用 `:is()` 或直接串联，可选中区间。
- `:nth-child(n+2):nth-child(-n+5)` → 第 2 到第 5 个（两个条件同时满足）

**相关伪类**：
- `:nth-of-type(an+b)`：在同类型兄弟中计数（只算同标签）
- `:nth-last-child(an+b)`：从后往前数
- `:nth-last-of-type(an+b)`：从后往前数且按类型

## 实现方案

```css
:root {
  --color-stripe: rgba(0, 0, 0, 0.03);
  --color-divider: rgba(0, 0, 0, 0.08);
  --color-accent: #1890ff;
}

/* 场景一：表格斑马纹（偶数行变色） */
.table-row:nth-child(even) {
  background: var(--color-stripe);
}

/* 场景二：首末元素特殊处理 */
.list-item:first-child {
  border-top: none;              /* 首项去掉顶部分割线 */
}
.list-item:last-child {
  border-bottom: none;           /* 末项去掉底部分割线 */
}

/* 场景三：选中第 2 到第 5 个 */
.list-item:nth-child(n+2):nth-child(-n+5) {
  color: var(--color-accent);
}

/* 场景四：每 3 个一组，每组的第 1 个加左边框 */
.grid-item:nth-child(3n+1) {
  border-left: 2px solid var(--color-accent);
}
/* 每组最后一个去掉右边距（3 列网格） */
.grid-item:nth-child(3n) {
  margin-right: 0;
}

/* 场景五：倒数第 2 个特殊处理 */
.card:nth-last-child(2) {
  opacity: 0.6;                  /* 倒数第二个变淡，引导滚动 */
}

/* 场景六：:nth-of-type 按类型计数 */
/* 同一容器内混排 h2 和 p，只给第 2 个 p 加强调 */
.article p:nth-of-type(2) {
  font-weight: 600;
  color: var(--color-accent);
}
/* 第 1 个 h2 加顶部间距 */
.article h2:nth-of-type(1) {
  margin-top: 32px;
}

/* 场景七：前 N 个用动画延迟错开入场 */
.list-item {
  opacity: 0;
  transform: translateY(20px);
  animation: fade-in 0.4s ease forwards;
}
.list-item:nth-child(1) { animation-delay: 0.05s; }
.list-item:nth-child(2) { animation-delay: 0.10s; }
.list-item:nth-child(3) { animation-delay: 0.15s; }
.list-item:nth-child(4) { animation-delay: 0.20s; }
.list-item:nth-child(5) { animation-delay: 0.25s; }

@keyframes fade-in {
  to { opacity: 1; transform: translateY(0); }
}

/* 场景八：暗黑模式调整分割线 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-stripe: rgba(255, 255, 255, 0.04);
    --color-divider: rgba(255, 255, 255, 0.1);
  }
}
```

## 执行步骤
1. 斑马纹用 `:nth-child(even)` 给偶数行加浅色背景，提升可读性
2. 首末元素用 `:first-child`/`:last-child` 去掉多余分割线，避免视觉断层
3. 区间选择：`:nth-child(n+2):nth-child(-n+5)` 同时满足「第 2 起」和「前 5 内」，得第 2~5 个
4. 网格分组：`:nth-child(3n)` 每 3 个一组的最后一个，去掉 margin 防换行错位
5. 倒数定位用 `:nth-last-child()`，避免依赖列表总长度
6. 混排场景用 `:nth-of-type()` 按标签类型计数，不被其他标签干扰
7. 动画延迟：用 `:nth-child(N)` 给前几个元素设置递增 `animation-delay`，做错开入场

## 兼容性
- `:nth-child`：Chrome 1+、Firefox 3.5+、Safari 3.1+、IE9+ 全面支持
- `:nth-of-type`：同上，全面支持
- `:nth-last-child`：IE9+ 支持
- 移动端：所有现代浏览器全面支持，无兼容顾虑

## 降级方案
```css
/* :nth-child 支持极广，几乎无需降级；仅 IE8 及以下不支持 */
/* 老旧浏览器用 :first-child + 类名兜底 */
.list-item {
  border-top: 1px solid var(--color-divider);
}
.list-item.first {
  border-top: none;
}
/* JS 给首末元素加 class */
```

```html
<script>
  // IE8 兜底：给首末元素加 class
  var items = document.querySelectorAll('.list-item');
  if (items.length && !('nth-child' in document.documentElement.style)) {
    items[0].classList.add('first');
    items[items.length - 1].classList.add('last');
  }
</script>
```

## 相关链接
- [[is-where-选择器分组]] - :is() 配合 :nth-child 简化多组选择
- [[has-父选择器]] - :has() + :nth-child 实现复杂联动
- [[layer-层级管控]] - :nth-child 在 @layer 中的优先级
- [[00-MOC-选择器]]
