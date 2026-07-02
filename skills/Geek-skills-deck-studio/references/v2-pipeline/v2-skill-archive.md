---
name: Geek-skills-notion-infographic
version: 2.0.0
description: >
  基于大纲自动研究并生成高质量可视化内容的 Agent Pipeline。
  支持两种输出模式：(A) PPTX 演示文稿（PptxGenJS 编程生成，含完整设计系统）；
  (B) 信息图提示词组图（Notion 手绘风 / 多风格可选，可直接用于 imageGen / DALL·E）。
  用户只需提供主题大纲或关键词，skill 自动启动专家子 Agent 并行抓取信息，
  主 Agent 负责规划、设计决策和验收，最终输出风格统一的高质量视觉内容。
  触发场景："帮我做一组信息图"、"生成 Notion 风格图片"、"做个PPT"、"做个演示文稿"、
  "把这个大纲做成图"、"infographic"、"信息图"、"手绘信息图"、"图解"、
  "把这篇文章可视化"、"做成社交媒体传播图"、"小红书图文"、"slides"、
  "presentation"、"deck"、"pptx"、"演示文稿"、"汇报PPT"。
  即使用户没有明确说"信息图"或"PPT"，但在提供大纲/要点并要求可视化传播时也应触发。
  当用户上传文章/文稿并要求"做成图"、"可视化"、"做成演示"时，同样触发此 skill。
compatibility: >
  Requires web_search and web_fetch. Optimal with subagent dispatch
  (Claude Code, Cowork). Degrades gracefully to single-thread on Claude.ai.
  Mode A (PPTX): Requires Node.js + pptxgenjs.
  Mode B (Infographic): Requires imageGen tool or manual use of prompts.
---

# Notion Infographic & Presentation Generator — Agent Pipeline V2

用户给大纲，Agent 去研究 + 设计，你只管 Plan 和验收。

## Architecture

```
User Outline / Topic
       ↓
P0: 环境检测 + 输入解析 + 输出模式决策
       ↓
Lead Agent (你 — 永远不搜索)
  │
  P1: 研究任务板 (拆解大纲为研究任务)
  │
  Dispatch ──→ Expert A ──→ writes task-a.md ──┐
           ──→ Expert B ──→ writes task-b.md ──┤ (parallel)
           ──→ Expert C ──→ writes task-c.md ──┘
  │                                             │
  │     workspace/research-notes/  <────────────┘
  │
  P2: Read notes → 提炼核心观点
  P3: 设计决策 (风格选择 + 配色 + 版式规划)
  P4: 生成输出
  │   ├─ Mode A: PptxGenJS → .pptx 文件
  │   └─ Mode B: 信息图提示词 → imageGen / 文本输出
  P5: QA 验收 + 输出
```

---

## P0: 环境检测 + 输出模式决策

```
1. 检测子 Agent 能力:
   - Claude Code / Cowork: YES → 并行派遣
   - Claude.ai: NO → 降级模式 (Lead 自己串行执行研究)

2. 可用工具检测:
   - web_search / web_fetch → 研究能力
   - Node.js + pptxgenjs → Mode A 可用
   - imageGen → Mode B 可直接出图
   - 均无 → Mode B 输出提示词文本

3. 输出模式决策 (优先级: 用户指定 > 场景推断):
   - 用户说 "PPT/演示文稿/slides/deck" → Mode A
   - 用户说 "信息图/图解/小红书/社交媒体" → Mode B
   - 未指定 → 推断：汇报/培训/商务 → A；传播/科普/内容营销 → B

4. 解析用户输入:
   - 纯主题/关键词 → 需要全面研究
   - 大纲/要点列表 → 按要点研究
   - 完整文稿 → 提炼观点后补充研究
   - 用户指定张数/页数? → 记录，优先级最高
```

---

## P1: 研究任务板

Lead Agent 将用户大纲拆解为 3-6 个研究任务。每个任务分配一个专家角色。

**Read `references/subagent-prompt.md` for the prompt template.**

### 任务板格式

```
# Research Task Board
Topic: {用户主题}
Output Mode: {A: PPTX / B: Infographic}
Outline Points: {大纲要点列表}

## Group A (parallel — 核心观点研究)
Task A: [行业分析师] — 研究 {观点1} 的数据支撑和案例
Task B: [技术专家] — 研究 {观点2} 的技术细节和趋势
Task C: [用户研究员] — 研究 {观点3} 的用户痛点和故事

## Group B (parallel — 补充素材)
Task D: [数据挖掘师] — 搜集相关统计数据和图表素材
Task E: [案例猎手] — 搜集经典案例和金句
```

### 任务分配原则

- 每个大纲要点至少分配 1 个研究任务
- 优先研究"需要数据/案例支撑"的观点
- 纯观点类（不需要外部信息）可跳过研究
- 总任务数控制在 3-6 个

### 环境适配派遣

**Claude Code / Cowork (有子Agent):**
```bash
for task in a b c; do
  claude -p "$(cat workspace/prompts/task-${task}.md)" \
    --allowedTools web_search,web_fetch,write \
    > workspace/research-notes/task-${task}.md &
done
wait
```

**Claude.ai (降级):**
Lead Agent 自己串行执行每个任务:
1. 按任务板顺序，依次执行 web_search + web_fetch
2. 每完成一个任务，将发现写入笔记块
3. 完成所有研究后进入 P2

---

## P2: 提炼核心观点

Lead Agent 阅读所有研究笔记，执行:

1. **信息聚合** — 把分散的发现按大纲要点归类
2. **观点提炼** — 每个要点提炼 1 个可视化核心观点
3. **数据筛选** — 为每个观点挑选最有冲击力的数据/案例
4. **可视化评估** — 判断每个观点适合什么呈现形式

### 观点提炼规则

- 每张图/每页 slide 只承载 1 个核心观点
- 观点不足时不强行凑数
- 观点过多时合并相近内容
- 硬上限：不超过 12 张/页

---

## P3: 设计决策

**Read `references/design-system.md` for the complete design system.**

这是 V2 的核心升级点 — 把美学决策系统化而不是凭感觉。

### 3.1 选择配色方案

**Read `references/design-system.md` → Color Palette Reference**

根据主题和受众选择配色：

| 场景 | 推荐色板 |
|------|---------|
| 商务/年报/财务 | Business & Authority (#2b2d42 系) |
| 科技/产品发布 | Vibrant & Tech (#023047 系) 或 Tech & Night (#000814 系) |
| 教育/数据报告 | Education & Charts (#264653 系) |
| 健康/咨询 | Modern & Wellness (#006d77 系) |
| 创意/时尚/生活 | Soft & Creative (#cdb4db 系) 或 Elegant & Fashion (#edafb8 系) |
| 自然/环保/ESG | Nature & Outdoors (#606c38 系) 或 Forest & Eco (#dad7cd 系) |

### 3.2 选择设计风格

| 风格 | 特征 | 适用 |
|------|------|------|
| **Sharp** | 直角、实线、高对比 | 商务、科技、金融 |
| **Soft** | 微圆角(4-8px)、柔和阴影 | 教育、咨询、通用 |
| **Rounded** | 大圆角(12-20px)、友好感 | 消费、社交、年轻受众 |
| **Pill** | 全圆角胶囊形、现代感 | 创意、科技产品、SaaS |
| **Notion手绘** | 马克笔线稿、涂鸦感、大留白 | 信息图、社媒传播、科普 |

### 3.3 版式规划 (Mode A: PPTX)

**分类每一页为五种页面类型之一:**

| 类型 | 用途 | 内容 |
|------|------|------|
| **Cover** | 开场定调 | 大标题+副标题+日期+视觉元素 |
| **TOC** | 导航预期 | 章节列表(3-5节) |
| **Section Divider** | 章节过渡 | 章节标题+引用/数据 |
| **Content** | 核心内容 | 观点+数据+图表+视觉 |
| **Summary** | 总结收束 | 核心要点回顾+CTA |

**关键：布局多样性！**
- **严禁**连续使用相同布局
- 主动使用：左右分栏、大数字突出、时间轴、对比图、引用卡片、图标网格
- 内容类型匹配版式：关键数据→大数字页，对比→左右分栏，流程→时间轴

### 3.4 组图规划 (Mode B: 信息图)

| 内容长度 | 通常观点数 | 参考张数 |
|---------|-----------|---------|
| 短内容 (<500字) | 2-4 | 3-5 张 |
| 中等 (500-1500字) | 4-7 | 5-8 张 |
| 长内容 (>1500字) | 6-10 | 8-12 张 |

组图结构:
```
第 1 张: 标题封面图 — 主题 + 核心价值主张
第 2~N-1 张: 内容图 — 每张一个核心观点 + 研究数据支撑
第 N 张: 总结/行动号召图
```

---

## P4: 生成输出

### Mode A: PPTX (PptxGenJS)

**Read `references/pptx-generation.md` for complete PptxGenJS guidance.**

执行时只保留这 4 条入口约束：
1. 每页一个 `slide-XX.js`，导出同步 `createSlide(pres, theme)`。
2. `theme` 只能使用 `primary/secondary/accent/light/bg`。
3. Cover 外每页必须有固定页码徽章。
4. 生成后运行 `cd slides && node compile.js`，输出 `slides/output/presentation.pptx`。

### Mode B: 信息图提示词

**Read `references/style-guide.md` for style specifications.**

每张图的提示词 = 风格前缀 + 内容描述 + 风格后缀

内容描述是唯一的变量区域，需要:
- 描述画面场景（简洁、视觉化）
- 融入研究数据（转化为图表/数字元素）
- 指定中文标注文字
- 保持大量留白和呼吸感

---

## P5: QA 验收

### Mode A 验收清单

- [ ] 每页分类为五种类型之一
- [ ] 连续页无相同布局
- [ ] Theme 对象 key 正确 (primary/secondary/accent/light/bg)
- [ ] 所有颜色来自 theme，无自创颜色
- [ ] 正文不加粗，bold 仅用于标题
- [ ] Cover 外每页有页码徽章
- [ ] `node compile.js` 成功运行
- [ ] 生成的 .pptx 可正常打开

### Mode B 验收清单

- [ ] 每张图的风格前缀和后缀完整无缺
- [ ] 内容描述融入了研究数据（不是空泛描述）
- [ ] 中文标注文字精简（每张不超过 30 字标注）
- [ ] 组图逻辑连贯（封面→内容→总结）
- [ ] 总张数在合理范围内

### 通用验收

- [ ] 所有数据来自研究笔记，无编造
- [ ] 统计数据标注年份和机构
- [ ] 金句/引用标注来源
- [ ] 研究笔记中没有的数据标注 [待验证]

---

## 美学设计原则

设计决策阶段阅读 `references/aesthetic-design.md`。入口文件只保留执行流程；长参考规则集中放入 references。

---

## Anti-Hallucination Rules

1. Lead Agent 不编造数据 — 所有数据必须来自研究笔记
2. 研究笔记中没有的数据标注 [待验证]
3. 子 Agent 只使用搜索结果中的真实信息
4. 金句/引用必须标注来源
5. 统计数据必须标注年份和机构

## Progress Reporting

```
[P0] 环境: {claude.ai/code}. 输出模式: {A/B}. 输入类型: {大纲/文稿/关键词}.
[P1] 任务板: {N} 个研究任务, {M} 组并行. 派遣中...
[P1 task-X done] {N} 条发现, {M} 个数据点.
[P1 all done] 研究完成. {总发现数} 条发现, {总源数} 个来源.
[P2] 提炼 {N} 个核心观点.
[P3] 设计决策: 配色={色板名}, 风格={风格名}, 版式={N}页规划.
[P4] 生成中... {已完成}/{总数}
[P5] QA {通过/失败}. 输出完成.
```

## Dependencies

| 工具 | 用途 | 安装 |
|------|------|------|
| markitdown | 读取已有 PPTX | `pip install "markitdown[pptx]"` |
| pptxgenjs | 从零创建 PPTX (Mode A) | `npm install -g pptxgenjs` |
| react-icons | SVG 图标 (可选) | `npm install -g react-icons react react-dom sharp` |
