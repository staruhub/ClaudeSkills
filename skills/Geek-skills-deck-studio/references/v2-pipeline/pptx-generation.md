# PPTX Generation Reference (Mode A)

## 页面类型详解

### 1. Cover Page (封面)

**布局选项:**

**非对称左右布局** — 文字集中一侧，视觉元素在另一侧
```
|  Title & Subtitle  |    Visual/Shape    |
|  Description        |                    |
```

**居中布局** — 内容居中，背景色块
```
|                                        |
|              MAIN TITLE                |
|              Subtitle                  |
|            Date / Presenter            |
```

**字号层级:** 主标题 48-72pt, 副标题 24-36pt, 元信息 14-18pt
**关键:** 标题至少是副标题的 2-3 倍大

### 2. Table of Contents (目录)

**布局选项:**

**编号竖排列表** — 3-5 节，简洁直观
```
|  TABLE OF CONTENTS            |
|  01  Section Title One         |
|  02  Section Title Two         |
|  03  Section Title Three       |
```

**双列网格** — 4-6 节，内容丰富
```
|  01  Section One   02  Section Two   |
|  03  Section Three 04  Section Four  |
```

**卡片式** — 3-4 节，现代创意
```
|  ┌─────┐  ┌─────┐  ┌─────┐  |
|  │ 01  │  │ 02  │  │ 03  │  |
|  │Title│  │Title│  │Title│  |
|  └─────┘  └─────┘  └─────┘  |
```

### 3. Section Divider (章节分隔)

- 大号章节编号 + 章节标题
- 可含一句引用或关键数据
- 背景可用 primary 色做深色调
- 起过渡和呼吸作用

### 4. Content (内容页 — 最多样化)

**必须变化布局！** 以下是可用的内容页子类型：

| 子类型 | 布局 | 适用 |
|-------|------|------|
| **大数字页** | 巨大数字居中 + 上下文说明 | 统计数据、关键指标 |
| **左右分栏** | 左文字右图形 (或反之) | 观点+图解 |
| **图标网格** | 2-4个图标+标签 | 特性列表、优势 |
| **时间轴** | 水平或垂直时间线 | 历程、步骤、发展 |
| **对比卡片** | 左右对比布局 | A vs B、前后对比 |
| **引用页** | 大引号 + 金句 + 来源 | 名人名言、用户反馈 |
| **图表页** | BAR/LINE/PIE/DOUGHNUT | 数据可视化 |
| **三栏等分** | 三列并排 | 三个并列要点 |

### 5. Summary (总结)

- 核心要点回顾 (3-5 条)
- 行动号召 (CTA)
- 联系方式 / 二维码（如需）
- 可用图标或色块标记每个要点

---

## Compile 脚本模板

```javascript
// slides/compile.js
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

// 从 design-system.md 选择的配色方案
const theme = {
  primary: "264653",    // 最深色
  secondary: "2a9d8f",  // 深辅助
  accent: "e9c46a",     // 强调
  light: "f4a261",      // 浅辅助
  bg: "f8f9fa"          // 背景 (可用纯白或极浅色)
};

const SLIDE_COUNT = 10; // 根据实际页数调整

for (let i = 1; i <= SLIDE_COUNT; i++) {
  const num = String(i).padStart(2, '0');
  const slideModule = require(`./slide-${num}.js`);
  slideModule.createSlide(pres, theme);
}

pres.writeFile({ fileName: './output/presentation.pptx' });
```

---

## 关键陷阱 (Pitfalls)

### P1: 选项对象不可复用

PptxGenJS 原地修改传入对象 (如 shadow 值被转为 EMU)。

```javascript
// ❌ 第二次调用拿到已转换的值
const shadow = { type:"outer", blur:6, offset:2, color:"000000", opacity:0.15 };
slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });
slide.addShape(pres.shapes.RECTANGLE, { shadow, ... }); // 坏了

// ✅ 用工厂函数
const makeShadow = () => ({ type:"outer", blur:6, offset:2, color:"000000", opacity:0.15 });
slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
```

### P2: createSlide 必须同步

```javascript
// ❌ compile.js 不会 await
async function createSlide(pres, theme) { ... }

// ✅ 同步
function createSlide(pres, theme) { ... }
```

### P3: 颜色不带 #

```javascript
// ❌
slide.addText("Title", { color: "#FF0000" });

// ✅
slide.addText("Title", { color: "FF0000" });
```

### P4: 正文不加粗

```javascript
// ✅
slide.addText("Main Title", { bold: true, fontSize: 36 });
slide.addText("Body text", { bold: false, fontSize: 14 });

// ❌
slide.addText("Body text", { bold: true, fontSize: 14 });
```

### P5: 只用 theme 颜色

```javascript
// ✅ 使用 theme
slide.addShape(pres.shapes.RECTANGLE, { fill: { color: theme.primary } });
slide.addText("Title", { color: theme.accent });

// ❌ 自创颜色
slide.addShape(pres.shapes.RECTANGLE, { fill: { color: "1A73E8" } });
```

### P6: ROUNDED_RECTANGLE + accent border 不兼容

不要在 ROUNDED_RECTANGLE 上叠加矩形装饰条 — 直角覆盖不住圆角。

### P7: 页码徽章位置固定

所有非 Cover 页必须在 x:9.3", y:5.1" 位置放页码。

---

## QA 流程

1. **编译测试**: `cd slides && node compile.js` — 必须无错误
2. **文本提取验证**: `python -m markitdown output/presentation.pptx` — 确认所有文字正确
3. **视觉检查**: 打开 .pptx 确认：
   - 无文字溢出
   - 颜色一致
   - 布局不单调
   - 页码正确
4. **布局多样性**: 连续两页不能使用相同子类型

---

## 子 Agent 并行生成指南

如果有子 Agent 能力，可最多 5 页并行生成:

每个子 Agent 需要知道:
1. 文件名: `slides/slide-XX.js`
2. 图片路径: `slides/imgs/`
3. 尺寸: 10" x 5.625" (LAYOUT_16x9)
4. 字体: 中文 = Microsoft YaHei, 英文 = Arial
5. 颜色: 6位hex不带# (如 `"FF0000"`)
6. 必须使用 theme 对象 (primary/secondary/accent/light/bg)
7. createSlide 必须同步
8. 导出格式: `module.exports = { createSlide, slideConfig }`

---

## 支持的图表类型

| 类型 | PptxGenJS 常量 | 适用 |
|------|---------------|------|
| 柱状图 | `BAR` | 分类对比 |
| 折线图 | `LINE` | 趋势变化 |
| 饼图 | `PIE` | 占比分布 |
| 环形图 | `DOUGHNUT` | 占比+中心数字 |
| 散点图 | `SCATTER` | 相关性 |
| 气泡图 | `BUBBLE` | 三维对比 |
| 雷达图 | `RADAR` | 多维评估 |

---

## 支持的形状

| 形状 | PptxGenJS 常量 |
|------|---------------|
| 矩形 | `RECTANGLE` |
| 圆形 | `OVAL` |
| 直线 | `LINE` |
| 圆角矩形 | `ROUNDED_RECTANGLE` |
