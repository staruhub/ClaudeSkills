# Geek Skills

[English](#english) | [中文](#中文)

A curated collection of Claude Code skills for daily work efficiency — built on Skills 2.0 format.

## Installation

### Quick Install

```bash
# Install all skills at once
npx skills add staruhub/ClaudeSkills
```

### Manual Install

1. Download the `.skill` file you need from this repository
2. Import it into Claude Code via `/skill install <path-to-file>`

## Available Skills

Skills are organized into five categories:

### 🔧 Development & Architecture

#### Geek-skills-pair-programming

Pair programming partner with automatic code review for quality, security, and best practices.

```
Help me implement a user authentication module with JWT tokens.
```

#### Geek-skills-security-audit

Comprehensive code security audit covering SAST, DAST, and SCA analysis.

```
Audit this project for security vulnerabilities and provide a remediation plan.
```

#### Geek-skills-solution-architect

Solution architect for system design, technology selection, and architecture review.

#### Geek-skills-threejs-performance

Three.js performance optimization expert — WebGPU, draw calls, memory management, and more.

### ✍️ Product & Content

#### Geek-skills-product-manager

Senior product manager assistant for PRD writing, product strategy, and requirement analysis. Features a 5-step creation workflow with IPO function description pattern.

```
Write a PRD for a mobile payment feature supporting WeChat Pay and Alipay.
```

#### Geek-skills-wechat-article-writer

WeChat Official Account article writer with 4 writing style modes — Official Copy, Tech Blog, Tutorial, and Storytelling.

```
Convert this blog post into a WeChat article with Tech Blog style.
```

#### Geek-skills-ppt-designer

Professional PowerPoint designer — layout, color schemes, visual hierarchy, and OOXML generation.

### 🛠️ Tools & Utilities

#### Geek-skills-a-share-analyst

A-share stock analyst — technical analysis, fundamental analysis, and stock screening strategies.

#### Geek-skills-c-drive-cleaner

Windows C: drive cleanup and disk space management utility.

#### Geek-skills-mineru-pdf-parser

PDF parser that converts documents into LLM-friendly Markdown/JSON format.

#### Geek-skills-seedream-imagegen

Seedream 4.0 AI image generation with 2K/4K resolution support.

```
Generate a tech-style cover image for an article about AI agents.
```

### 📚 Education & Research

#### Geek-skills-gaokao-expert

Gaokao (Chinese college entrance exam) question design expert.

#### Geek-skills-university-exam-prep

University exam preparation assistant using Socratic learning methodology.

#### Geek-skills-weather-forecast-report

Weather element research report generator for meteorological analysis.

### ⚙️ Workflow (OpenSpec)

A structured workflow system for managing changes through exploration, proposal, implementation, and archival.

| Skill | Description |
|-------|-------------|
| `Geek-skills-openspec-explore` | Explore mode — thinking partner for ideas and requirements |
| `Geek-skills-openspec-propose` | Propose changes with design, specs, and task breakdown |
| `Geek-skills-openspec-apply-change` | Implement tasks from a proposed change |
| `Geek-skills-openspec-archive-change` | Archive completed changes |

## Skill Format

Each `.skill` file is a ZIP archive with the following structure:

```
skill-name/
├── SKILL.md          # Required — core skill file with YAML frontmatter
├── scripts/          # Optional — executable scripts
├── references/       # Optional — reference documents
└── assets/           # Optional — templates and resources
```

YAML frontmatter fields: `name` (Geek-skills-xxx format), `description`, `version`.

## License

MIT

---

<a id="中文"></a>

# Geek Skills（中文）

基于 Claude Code Skills 2.0 格式构建的高质量技能集合，提升日常工作效率。

## 安装

```bash
# 一键安装所有技能
npx skills add staruhub/ClaudeSkills
```

或手动下载 `.skill` 文件后通过 `/skill install <文件路径>` 导入 Claude Code。

## 技能列表

| 分类 | 技能 | 说明 |
|------|------|------|
| 🔧 开发 | `pair-programming` | 结对编程搭档，自动审查代码质量与安全性 |
| 🔧 开发 | `security-audit` | 全面代码安全审计（SAST/DAST/SCA） |
| 🔧 开发 | `solution-architect` | 解决方案架构师，系统设计与技术选型 |
| 🔧 开发 | `threejs-performance` | Three.js 性能优化专家 |
| ✍️ 内容 | `product-manager` | 资深产品经理，PRD 文档创作与评审 |
| ✍️ 内容 | `wechat-article-writer` | 微信公众号文章创作，4 种写作风格 |
| ✍️ 内容 | `ppt-designer` | 专业 PPT 设计与制作 |
| 🛠️ 工具 | `a-share-analyst` | A 股分析师，技术面/基本面分析 |
| 🛠️ 工具 | `c-drive-cleaner` | Windows C 盘清理与空间管理 |
| 🛠️ 工具 | `mineru-pdf-parser` | PDF 转 Markdown/JSON |
| 🛠️ 工具 | `seedream-imagegen` | Seedream 4.0 AI 图像生成 |
| 📚 教育 | `gaokao-expert` | 高考命题专家 |
| 📚 教育 | `university-exam-prep` | 大学备考苏格拉底式学习助手 |
| 📚 教育 | `weather-forecast-report` | 天气要素研究报告生成器 |
| ⚙️ 工作流 | `openspec-explore` | 探索模式，思考伙伴 |
| ⚙️ 工作流 | `openspec-propose` | 提出变更提案 |
| ⚙️ 工作流 | `openspec-apply-change` | 实施变更任务 |
| ⚙️ 工作流 | `openspec-archive-change` | 归档已完成变更 |

所有技能文件名均以 `Geek-skills-` 为前缀，后缀为 `.skill`。
