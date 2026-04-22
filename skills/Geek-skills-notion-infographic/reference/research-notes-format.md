# 研究笔记格式规范

所有子 Agent 的研究产出必须遵循此格式。
Lead Agent 只通过读取笔记文件获取信息，永远不直接看搜索结果。

## 笔记文件结构

```
workspace/
└── research-notes/
    ├── task-a.md    ← Expert A 写入
    ├── task-b.md    ← Expert B 写入
    ├── task-c.md    ← Expert C 写入
    └── synthesis.md ← Lead Agent 汇总（P2阶段产出）
```

## 笔记文件模板

```markdown
---
task_id: task-a
role: 行业分析师
topic: AI编程工具市场趋势
status: complete
sources_found: 4
---

## Sources

[1] GitHub Copilot 用户数据报告 | https://... | 权威性: 9/10 | 2025-03
[2] Stack Overflow 2025 开发者调查 | https://... | 权威性: 8/10 | 2025-06
[3] Gartner AI 编程工具魔力象限 | https://... | 权威性: 9/10 | 2025-04
[4] 某创业公司CTO的博客 | https://... | 权威性: 5/10 | 2025-05

## Findings

- GitHub Copilot 月活用户突破 1500 万，同比增长 180%. [1]
- 72% 的开发者表示已在工作中使用 AI 辅助编码. [2]
- Cursor 在 2025 年独立开发者群体中满意度排名第一. [2]
- AI 编程工具市场规模预计 2026 年达 150 亿美元. [3]
- 使用 AI 编程工具后，代码 review 时间平均减少 35%. [1]
- 初级开发者使用 AI 工具的生产力提升 (56%) 高于高级开发者 (26%). [2]

## Infographic Material

### 数字冲击
- 1500万月活: Copilot 的用户规模已相当于一个中型国家人口 [1]
- 72%: 近四分之三开发者已拥抱 AI 编码 [2]
- 150亿美元: 2026年市场规模预测 [3]

### 对比素材
- 初级 (56%提升) vs 高级 (26%提升): AI对不同水平开发者的增益差异 [2]
- 有AI vs 无AI: review时间减少35% [1]

### 金句
- "AI won't replace programmers, but programmers who use AI will replace those who don't." — GitHub CEO, Thomas Dohmke [1]

### 流程/时间线
- 2021: Copilot预览版 → 2023: ChatGPT引爆 → 2024: Cursor崛起 → 2025: Agent编码时代 [综合]

## Leads Discovered

- Devin AI: 号称第一个AI软件工程师 — 可能有独立使用数据 — "Devin AI developer agent performance"
- Windsurf: 新兴AI编辑器 — 增长很快 — "Windsurf AI editor market share"

## Gaps

- 缺少中国市场的 AI 编程工具使用数据
- 未找到 AI 编程工具对代码质量影响的长期研究

## END
```

## Lead Agent 汇总格式 (synthesis.md)

P2 阶段 Lead Agent 读取所有笔记后产出：

```markdown
# Research Synthesis — {主题}

## 核心观点 (按信息图顺序)

### 观点 1: {标题}
**一句话:** {核心信息}
**支撑数据:** {来自哪个任务笔记的哪个发现}
**可视化建议:** {适合什么类型的图}

### 观点 2: {标题}
...

## 信息图规划

| 序号 | 类型 | 核心观点 | 关键数据 | 视觉元素 |
|-----|------|---------|---------|---------|
| 1 | 封面 | {主题} | — | {场景描述} |
| 2 | 数据图 | {观点1} | {数据} | {图表类型} |
| 3 | 对比图 | {观点2} | {A vs B} | {对比布局} |
| ... | ... | ... | ... | ... |
| N | 总结 | {行动号召} | — | {收束场景} |

## 未使用的素材 (备用)

- {有价值但本次未纳入的发现}
```

## 质量检查

Lead Agent 在读取笔记时检查：

1. ✅ 每条 finding 都有来源编号
2. ✅ 来源编号在 Sources 列表中存在
3. ✅ 数据类素材标注了年份/机构
4. ✅ 金句标注了说话人和身份
5. ⚠️ 权威性 < 6 的来源需谨慎使用
6. ❌ 没有来源的数据标记 [待验证]
