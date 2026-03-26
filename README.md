# Geek Skills Collection

Vibe Coding 时代社群共享技能集合 — 基于 Claude Code Skills 2.0 格式构建的高质量提示工程技能库。

所有技能统一使用 `Geek-skills-xxx` 命名规范，以 `.skill` (ZIP) 格式发布。

## Skills 列表

### 开发与架构

| 技能文件 | 说明 |
|---------|------|
| `Geek-skills-pair-programming.skill` | 结对编程搭档，代码生成后自动审查质量、安全性和最佳实践 |
| `Geek-skills-security-audit.skill` | 全面的代码安全检查和服务器安全审计（SAST/DAST/SCA） |
| `Geek-skills-solution-architect.skill` | 解决方案架构师，系统架构设计、技术选型、架构评审 |
| `Geek-skills-threejs-performance.skill` | Three.js 性能优化专家（WebGPU、绘制调用、内存管理等） |

### 产品与内容

| 技能文件 | 说明 |
|---------|------|
| `Geek-skills-product-manager.skill` | 资深产品经理助手，PRD 文档创作与评审、产品策略咨询 |
| `Geek-skills-wechat-article-writer.skill` | 微信公众号文章创作助手，多风格适配 |
| `Geek-skills-ppt-designer.skill` | 专业 PPT 设计与制作，排版、配色、视觉层次 |

### 工具与效率

| 技能文件 | 说明 |
|---------|------|
| `Geek-skills-a-share-analyst.skill` | A 股专业分析师，技术面/基本面分析、选股策略 |
| `Geek-skills-c-drive-cleaner.skill` | Windows C 盘清理和磁盘空间管理 |
| `Geek-skills-mineru-pdf-parser.skill` | PDF 解析工具，转换为 LLM 友好的 Markdown/JSON |
| `Geek-skills-seedream-imagegen.skill` | Seedream 4.0 AI 图像生成（2K/4K 分辨率） |

### 教育与研究

| 技能文件 | 说明 |
|---------|------|
| `Geek-skills-gaokao-expert.skill` | 高考命题专家，试题创作与评审 |
| `Geek-skills-university-exam-prep.skill` | 大学备考苏格拉底式学习助手 |
| `Geek-skills-weather-forecast-report.skill` | 天气要素专题研究报告生成器 |

### 工作流（OpenSpec）

| 技能文件 | 说明 |
|---------|------|
| `Geek-skills-openspec-explore.skill` | 探索模式，思考伙伴 |
| `Geek-skills-openspec-propose.skill` | 提出变更提案 |
| `Geek-skills-openspec-apply-change.skill` | 实施变更任务 |
| `Geek-skills-openspec-archive-change.skill` | 归档已完成变更 |

## 使用方式

将 `.skill` 文件导入 Claude Code 即可使用。

## 技能格式规范

每个 `.skill` 文件是一个 ZIP 压缩包，内部结构：

```
skill-name/
├── SKILL.md          # 必需 - 核心技能文件（含 YAML frontmatter）
├── scripts/          # 可选 - 可执行脚本
├── references/       # 可选 - 参考文档
└── assets/           # 可选 - 模板、资源文件
```

YAML frontmatter 必需字段：`name`（Geek-skills-xxx 格式）、`description`、`version`。
