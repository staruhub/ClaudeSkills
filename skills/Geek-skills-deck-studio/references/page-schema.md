# Page Schema：页面结构定义

PPT 不是每页临场发挥，是套着页面语法在出。每一页都必须能被下面的结构完整描述，从而同时支持模式 B（内容稿/PptxGenJS）和模式 C（image 出图）。

## 页面类型清单（12 种）

| 类型 | type 值 | 用途 | 特殊要求 |
|------|---------|------|---------|
| 封面页 | `cover` | 定调 | 主标题 ≤12 字；副标题一句；无正文 |
| 目录页 | `toc` | 导航 | 章节数 3-6；超出则分组 |
| 问题定义页 | `problem` | 痛点/现状 | key_message 必须是"问题陈述"不是话题 |
| 方法论页 | `framework` | 模型/框架 | 视觉结构优先图解，文字为辅 |
| 对比页 | `compare` | 方案/前后对比 | 恰好 2-3 列；维度 ≤5 行 |
| 流程页 | `flow` | 步骤/pipeline | 步骤 3-6 个；超出拆页 |
| 时间线页 | `timeline` | 里程碑/规划 | 节点 3-7 个 |
| 数据页 | `data` | 图表证据 | 一页一个核心数据洞察；图表占 ≥60% 面积 |
| 案例页 | `case` | 实例佐证 | 结构固定：背景→动作→结果（含数字） |
| 引言过渡页 | `divider` | 章节转场 | 只有章节标题±一句引言 |
| 总结行动页 | `action` | 结论+CTA | 行动项 ≤3 条，每条有主语 |
| 封底页 | `ending` | 收尾 | 联系方式/QA/致谢，三选一为主 |

## 每页字段定义

```jsonc
{
  "page_no": 1,                    // 必填
  "page_type": "cover",           // 必填，取上表 type 值
  "title": "页面标题",             // 必填，≤16 字
  "key_message": "这页只讲这一件事", // 必填，一句话核心结论——写不出来说明这页不该存在
  "visual_structure": "left-text-right-visual",  // 必填，版式代号见下
  "content_blocks": [              // 必填，1-5 个
    {"kind": "bullets|paragraph|quote|number|chart|image", "content": "..."}
  ],
  "image_need": "none",           // 必填：none | decorative | chart | hero
  "speaker_notes": "1-3 句"        // 建议填；模式 C 必填（防"好看但不好讲"）
}
```

## 版式代号（visual_structure）

`full-visual`（全图+蒙版+大字）/ `left-text-right-visual` / `top-title-bottom-grid` /
`center-statement`（超大单句）/ `two-column-compare` / `horizontal-flow` /
`big-number`（超大数字+小注）/ `card-grid`（2×2 或 3×2 卡片）

## 密度规则（硬约束，超限即拆页）

- 每页要点 3-5 个；content_blocks ≤5
- 文字层级 ≤3 级；标题:正文字号比 ≥2:1
- 数据页一页只讲一个洞察；对比页维度 ≤5
- 正文单块 ≤60 字（模式 C 出图时 ≤30 字，长文本走"留位后叠"策略）

## 标题与正文层级

- 一级：页面标题（每页唯一）
- 二级：模块小标题（card-grid / compare 的列头）
- 三级：正文/注释
- 标题写结论不写话题："Q3 成本下降 23%" ✅，"成本分析" ❌
