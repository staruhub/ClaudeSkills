---
name: Geek-skills-deck-studio
version: 3.0.0
description: PPT 生产 Agent：理解场景 → 推荐风格 → 先出大纲 → 定义页面 → 双通路交付（PPT 内容稿 / 逐页视觉图 / 信息图组图）。当用户要做汇报、路演、培训课件、提案、咨询报告的演示文稿，或要把大纲/文章做成 slides、deck、PPT、信息图、小红书图文、可视化传播图时使用。支持指定风格或从风格库推荐，支持 image 模型逐页出视觉稿。前身为 notion-infographic（v2）并吸收 ppt-designer 的设计原则。不用于：pptx 文件的纯技术操作（拆分/合并/提取，用宿主 pptx skill）、演讲稿或文章本体的写作（用 wechat-article-writer）、需要先做研究的内容调研（先走 deep-research 再回来）、单张海报或 logo 设计。
---

# Deck Studio：PPT 生产 Agent

不是"帮你排版润色"，而是一条从场景理解到成品交付的生产线。
核心信条（承自 ppt-designer）：**PPT 的本质是信息传达，设计是为内容服务的。**

## 铁律（不是建议）

1. **先 outline，后一切**。视觉图模式（模式 C）必须在大纲经用户确认后才启动；image 模型只负责"把已定义的页画出来"，永远不决定 deck 讲什么。用户要求"跳过大纲直接画"时，解释原因并先给大纲。
2. **每页先有 page brief，再有 image prompt**，禁止跳级。
3. **一套 deck 一个风格**。风格参数从 style brief 统一注入每页，不允许逐页漂移。

## 验收标准（交付前逐条自查）

- [ ] outline 在任何页面产出之前存在且经用户确认（模式 A 除外，它本身就是终点）
- [ ] 每页符合 page schema 必填字段，密度合规（要点 3-5 / 层级 ≤3 / 字号比 ≥2:1）
- [ ] 全套使用同一 style brief，任取两页字体、色板、版式代号一致
- [ ] 模式 C 的每页 prompt 包含风格名、构图、标题文案、正文文案、禁止项
- [ ] 交付物包含 speaker notes（用户明确不要时除外）
- [ ] 没有 emoji 充当功能图标；配色来自所选风格色板而非临场发挥

## 不做什么

- pptx 文件技术操作（拆分/合并/页数统计）→ 宿主环境 pptx skill
- 演讲稿、文章正文的深度写作 → `wechat-article-writer`
- 内容需要多源调研时 → 先移交 `deep-research`，拿到结论再回本流程
- 单张海报、logo、纯装饰图 → 图像生成类 skill 直接处理
- 用户只要"随便几页能用就行"时，压缩为：快速 outline → 模式 B 简化输出，不走完整六步

## 工作流程（六步）

### Step 1 识别任务类型
汇报 / 路演 / 培训 / 提案 / 复盘 / 咨询报告 / 招聘介绍 / 自媒体分享。
判断规则见 `references/scene-routing.md`。识别不确定时直接问，不猜。

### Step 2 补齐关键上下文（最多问 5 项，已知的不重复问）
① 给谁看 ② 目标是什么 ③ 期望页数 ④ 偏内容清晰还是视觉冲击 ⑤ 有无指定风格/品牌色

### Step 3 选择风格
用户指定 → 锁定。未指定 → 按 `references/scene-routing.md` 的"场景×风格"矩阵推荐 3 个并给一句话理由。
用户有品牌资产（ChaoGeek / ClawTime / WorkBuddy）→ 直接用 `style-library/custom/` 定制风格。

### Step 4 出 outline（模式 A 到此为止）
按 `templates/outline-template.md`：主题 / 受众 / 目标 / 页数建议 / 每页标题 + 一句话摘要。
**停，等用户确认后再继续。**

### Step 5 页级结构
逐页填 page schema（`references/page-schema.md`）：页面类型、核心结论、视觉结构、内容模块、图像需求。

### Step 6 按模式交付

| 模式 | 适用 | 输出 |
|------|------|------|
| **A. Outline** | 用户还没想清楚内容 | 大纲（Step 4 产物） |
| **B. 内容稿** | 交给 PPT 生成器/前端引擎，或用 PptxGenJS 直接产 pptx | slide schema JSON + 可读 Markdown + 风格参数；PptxGenJS 路线见 `references/v2-pipeline/pptx-generation.md` |
| **C. 视觉图** | 逐页出图（image 模型），或信息图组图 | 每页 page brief → image prompt → 出图；流程与引擎适配见 `references/image-branch.md` |

## 风格库（style-library/，当前 13 个，持续扩充）

| 类别 | 风格 | 一句话 |
|------|------|--------|
| 通用商务 | `business/moshiro-consulting.md` 墨白咨询 | 黑白灰+单强调色，咨询报告的克制感 |
| 通用商务 | `business/heibai-ledger.md` 黑白账本 | 表格与数字为主角的数据汇报风（默认模式 B） |
| 品牌创意 | `creative/yinghuang-studio.md` 英黄工作室 | 黑+暖黄，高端提案感，大字留白 |
| 品牌创意 | `creative/tanghe-frame.md` 糖盒彩框 | 奶油底+彩色块边框，新潮杂志感 |
| 教育培训 | `education/qingfeng-classroom.md` 清风讲堂 | 水蓝清爽，低压迫感课件 |
| 教育培训 | `education/academic-bluegray.md` 学术蓝灰 | 论文答辩与学术报告（默认模式 B） |
| 科技未来 | `tech/polar-night.md` 极夜科技 | 深底霓虹，AI/数据产品发布 |
| 科技未来 | `tech/platinum-future.md` 铂灰未来 | 浅色金属质感，投影友好的科技感 |
| 内容传播 | `media/hot-card.md` 热帖卡片 | 小红书式高对比卡片组图 |
| 内容传播 | `media/notion-handdrawn.md` Notion 手绘 | v2 招牌：手绘线条+便签质感知识图解 |
| 定制品牌 | `custom/chaogeek-pixel.md` ChaoGeek 像素半调 | 霓虹绿/龙虾红/深底 DNA，派生自 chaogeek 视觉系统 |
| 定制品牌 | `custom/clawtime-industrial.md` ClawTime 黑红工业 | 碳黑+机械红，工业咬合感（初稿待品牌校准） |
| 定制品牌 | `custom/workbuddy-modern.md` WorkBuddy 绿色现代 | 生产力绿，效率工具官网感（初稿待品牌校准） |

选择规则：先按类别匹配场景，再看风格文件里的"不适用场景"排除。每个风格文件含 10 字段（色板/字体气质/版式/图像策略/密度/style brief 等）。

## 已知陷阱

| 陷阱 | 具体表现 | 应对 |
|------|---------|------|
| 跳过大纲直接出页 | 用户催"直接画"，整套 deck 逻辑散架 | 铁律 1：解释后先给 outline，大纲确认成本远低于返工 |
| 逐页风格漂移 | 第 8 页突然换了配色和字体 | 每页 prompt 从同一 style brief 注入，抽查任意两页 |
| image 模型中文排版翻车 | 文字重叠、字压图、乱码伪汉字 | prompt 必带中文排版禁止项；长文本改为"图留文位、文字后期叠加"策略，见 image-branch.md |
| 好看但不好讲 | 视觉冲击页密度过低，一页讲 3 分钟没内容 | page schema 的 key_message 必填；speaker notes 同步产出 |
| 单页信息超载 | 要点 6+，图表 3 张挤一页 | 密度规则硬约束：拆页 |
| 风格推荐同质化 | 推荐的 3 个风格看不出差别 | 3 个推荐必须来自 ≥2 个类别 |

## 参考文档（按需加载）

| 文件 | 何时读 |
|------|--------|
| `references/page-schema.md` | Step 5 逐页定义时 |
| `references/scene-routing.md` | Step 1 识别与 Step 3 推荐时 |
| `references/image-branch.md` | 模式 C 启动时；引擎适配（gpt-image / seedream / skywork）与中文排版禁止项 |
| `references/layout-rules.md` | 排版细节拿不准时；CRAP/层级/配色/图片完整理论（承自 ppt-designer） |
| `references/quick-reference.md` | 制作中随时查数值规范（字号/间距/色值） |
| `references/case-examples.md` | 需要整套风格方案参考时；商务/创意/学术三案例 |
| `templates/outline-template.md` | Step 4 |
| `templates/page-brief-template.md` | Step 5 |
| `templates/image-prompt-template.md` | 模式 C 逐页出 prompt 时 |

### v2 遗产（references/v2-pipeline/，模式 B/C 实现细节，按需取用）

- `pptx-generation.md` — PptxGenJS 编程生成完整方案（模式 B 直出 pptx 的实现）
- `design-system.md` — v2 设计系统（token/组件，模式 B 的默认视觉参数）
- `style-guide.md` — Notion 手绘风等 v2 风格定义（待改造为 style-library 格式）
- `aesthetic-design.md` — 审美设计笔记
- `research-notes-format.md` / `subagent-prompt.md` — 子代理并行研究协议（大纲需要资料抓取时）
- `v2-prompt-template.md` — v2 信息图 prompt 模板（新模板未覆盖的手绘风参数可从此取）
- `v2-skill-archive.md` — notion-infographic v2 的原始 SKILL.md 存档

## 回归

- `evals/routing-evals.json` — 触发/模式路由用例，改 description 后用仓库根 `scripts/run_routing_evals.py` 校验
