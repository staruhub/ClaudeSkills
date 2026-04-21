# Geek Skills

[English](#english) | [中文](#中文)

A curated repository of unpacked Claude Code skills. This repo keeps normalized in-house skills under `skills/` and preserves selected upstream imports when they are synced in their original layout.

## Recent Updates

- Updated original skills from the latest matching download packages on 2026-04-21.
- Synced `deep-research` to V8.0 and added its latest `evals/`, observability references, and run-summary helper.
- Updated `product-manager` with the latest PRD anti-translation guidance and refreshed `wechat-article-writer` with stronger Chinese polish checks plus new linguistic reference material.

## Install in Claude Code

Claude Code skills are directory-based: each skill needs a `SKILL.md` entrypoint and can include supporting files such as references, templates, examples, and scripts.

1. Pick a skill directory from this repository.
2. Copy the whole directory into one of these locations:
   - Personal: `~/.claude/skills/<skill-name>/`
   - Project: `.claude/skills/<skill-name>/`
3. Keep `SKILL.md` and its supporting files in the same directory.

## Repository Layout

```text
.
├── skills/                         # Curated, normalized Geek skills
│   └── Geek-skills-xxx/
│       ├── SKILL.md
│       ├── references/
│       ├── assets/
│       ├── scripts/
│       └── evals/                  # Optional, when a skill ships evaluation assets
├── llm-wiki/                       # Upstream-synced skill kept in original layout
│   ├── SKILL.md
│   └── references/
├── README.md
└── AGENTS.md
```

### Layout Rules

- Add new curated skills under `skills/Geek-skills-xxx/`.
- Keep `SKILL.md` focused on activation, workflow, and navigation.
- Move large reference material into `references/` or `assets/`.
- Put executable helpers in `scripts/`.
- Keep evaluation fixtures in `evals/` when the skill includes repeatable routing or quality checks.
- Preserve upstream structure only when syncing external skills with minimal changes.

## Curated Skills

### Development & Architecture

| Skill | Path | Description |
|-------|------|-------------|
| `pair-programming` | [skills/Geek-skills-pair-programming](skills/Geek-skills-pair-programming/SKILL.md) | Pair programming partner with automatic code review |
| `security-audit` | [skills/Geek-skills-security-audit](skills/Geek-skills-security-audit/SKILL.md) | Comprehensive code security audit |
| `solution-architect` | [skills/Geek-skills-solution-architect](skills/Geek-skills-solution-architect/SKILL.md) | System design, tech selection, and architecture review |
| `threejs-performance` | [skills/Geek-skills-threejs-performance](skills/Geek-skills-threejs-performance/SKILL.md) | Three.js performance optimization |

### Product & Content

| Skill | Path | Description |
|-------|------|-------------|
| `product-manager` | [skills/Geek-skills-product-manager](skills/Geek-skills-product-manager/SKILL.md) | PRD writing, requirement analysis, and product strategy |
| `wechat-article-writer` | [skills/Geek-skills-wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md) | Multi-style WeChat article writing |
| `ppt-designer` | [skills/Geek-skills-ppt-designer](skills/Geek-skills-ppt-designer/SKILL.md) | PPT structure, layout, and visual hierarchy |

### Tools & Utilities

| Skill | Path | Description |
|-------|------|-------------|
| `a-share-analyst` | [skills/Geek-skills-a-share-analyst](skills/Geek-skills-a-share-analyst/SKILL.md) | A-share technical and fundamental analysis |
| `c-drive-cleaner` | [skills/Geek-skills-c-drive-cleaner](skills/Geek-skills-c-drive-cleaner/SKILL.md) | Windows C drive cleanup and disk space management |
| `mineru-pdf-parser` | [skills/Geek-skills-mineru-pdf-parser](skills/Geek-skills-mineru-pdf-parser/SKILL.md) | PDF to Markdown or JSON for LLM workflows |
| `seedream-imagegen` | [skills/Geek-skills-seedream-imagegen](skills/Geek-skills-seedream-imagegen/SKILL.md) | Seedream 4.0 image generation |

### Education & Research

| Skill | Path | Description |
|-------|------|-------------|
| `deep-research` | [skills/Geek-skills-deep-research](skills/Geek-skills-deep-research/SKILL.md) | Evidence-based research workflow with observability, evals, and decision briefs |
| `gaokao-expert` | [skills/Geek-skills-gaokao-expert](skills/Geek-skills-gaokao-expert/SKILL.md) | Gaokao question design expert |
| `university-exam-prep` | [skills/Geek-skills-university-exam-prep](skills/Geek-skills-university-exam-prep/SKILL.md) | University exam prep with Socratic learning |
| `weather-forecast-report` | [skills/Geek-skills-weather-forecast-report](skills/Geek-skills-weather-forecast-report/SKILL.md) | Weather element research report generator |

## Upstream-Synced Skills

| Skill | Path | Notes |
|-------|------|-------|
| `llm-wiki` | [llm-wiki](llm-wiki/SKILL.md) | Preserved in original upstream layout at repo root |

## License

MIT

---

<a id="中文"></a>

# Geek Skills（中文）

这是一个以“解包目录”形式维护的 Claude Code skills 仓库。仓库会把自维护技能统一放在 `skills/` 下，同时在必要时保留少量上游技能的原始目录结构。

## 最近更新

- 已按 2026-04-21 下载目录中的最新匹配包更新原有 skills。
- 已将 `deep-research` 升级到 V8.0，并补齐最新的 `evals/`、可观测性参考材料和 run-summary 脚本。
- 已更新 `product-manager` 的 PRD 反翻译腔写作规范，以及 `wechat-article-writer` 的中文润色检查和语言学参考资料。

## 在 Claude Code 中安装

Claude Code 的 skill 以目录为单位组织：每个 skill 至少包含一个 `SKILL.md` 入口文件，并可按需附带参考资料、模板、示例或脚本。

1. 从本仓库选择一个 skill 目录。
2. 将整个目录复制到以下任一位置：
   - 个人级：`~/.claude/skills/<skill-name>/`
   - 项目级：`.claude/skills/<skill-name>/`
3. 保持 `SKILL.md` 与 supporting files 在同一个目录内。

## 仓库结构

```text
.
├── skills/                         # 规范化维护的 Geek 技能
│   └── Geek-skills-xxx/
│       ├── SKILL.md
│       ├── references/
│       ├── assets/
│       ├── scripts/
│       └── evals/                  # 可选，用于路由或质量评估资产
├── llm-wiki/                       # 按上游结构保留的同步技能
│   ├── SKILL.md
│   └── references/
├── README.md
└── AGENTS.md
```

### 维护约定

- 新增自维护技能时，优先放在 `skills/Geek-skills-xxx/`。
- `SKILL.md` 只保留触发条件、主流程和导航信息。
- 大块参考资料优先拆到 `references/` 或 `assets/`。
- 可执行辅助脚本放到 `scripts/`。
- 需要重复验证的路由或质量检查资源，放到 `evals/`。
- 同步外部技能时，只有在低风险情况下才做结构规范化；否则保留上游原始布局。

## 自维护技能

### 开发与架构

| 技能 | 路径 | 说明 |
|------|------|------|
| `pair-programming` | [skills/Geek-skills-pair-programming](skills/Geek-skills-pair-programming/SKILL.md) | 结对编程搭档，自动审查代码质量 |
| `security-audit` | [skills/Geek-skills-security-audit](skills/Geek-skills-security-audit/SKILL.md) | 全面代码安全审计 |
| `solution-architect` | [skills/Geek-skills-solution-architect](skills/Geek-skills-solution-architect/SKILL.md) | 系统设计与技术选型 |
| `threejs-performance` | [skills/Geek-skills-threejs-performance](skills/Geek-skills-threejs-performance/SKILL.md) | Three.js 性能优化 |

### 产品与内容

| 技能 | 路径 | 说明 |
|------|------|------|
| `product-manager` | [skills/Geek-skills-product-manager](skills/Geek-skills-product-manager/SKILL.md) | PRD 创作、需求分析与产品策略 |
| `wechat-article-writer` | [skills/Geek-skills-wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md) | 多风格微信公众号文章创作 |
| `ppt-designer` | [skills/Geek-skills-ppt-designer](skills/Geek-skills-ppt-designer/SKILL.md) | PPT 结构设计、排版与视觉层次 |

### 工具与效率

| 技能 | 路径 | 说明 |
|------|------|------|
| `a-share-analyst` | [skills/Geek-skills-a-share-analyst](skills/Geek-skills-a-share-analyst/SKILL.md) | A 股技术面与基本面分析 |
| `c-drive-cleaner` | [skills/Geek-skills-c-drive-cleaner](skills/Geek-skills-c-drive-cleaner/SKILL.md) | Windows C 盘清理与空间管理 |
| `mineru-pdf-parser` | [skills/Geek-skills-mineru-pdf-parser](skills/Geek-skills-mineru-pdf-parser/SKILL.md) | 面向 LLM 工作流的 PDF 解析 |
| `seedream-imagegen` | [skills/Geek-skills-seedream-imagegen](skills/Geek-skills-seedream-imagegen/SKILL.md) | Seedream 4.0 图像生成 |

### 教育与研究

| 技能 | 路径 | 说明 |
|------|------|------|
| `deep-research` | [skills/Geek-skills-deep-research](skills/Geek-skills-deep-research/SKILL.md) | 带可观测性、评估资产和决策简报能力的深度研究流水线 |
| `gaokao-expert` | [skills/Geek-skills-gaokao-expert](skills/Geek-skills-gaokao-expert/SKILL.md) | 高考命题专家 |
| `university-exam-prep` | [skills/Geek-skills-university-exam-prep](skills/Geek-skills-university-exam-prep/SKILL.md) | 大学备考苏格拉底式学习助手 |
| `weather-forecast-report` | [skills/Geek-skills-weather-forecast-report](skills/Geek-skills-weather-forecast-report/SKILL.md) | 天气要素研究报告生成器 |

## 上游同步技能

| 技能 | 路径 | 备注 |
|------|------|------|
| `llm-wiki` | [llm-wiki](llm-wiki/SKILL.md) | 当前保留上游原始目录结构，位于仓库根目录 |
