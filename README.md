# Geek Skills

[English](#english) | [中文](#中文)

A curated repository of unpacked Claude Code skills. This repo keeps normalized in-house skills under `skills/` and preserves selected upstream imports when they are synced in their original layout.

## Repository Status

- Curated skills live in `skills/Geek-skills-xxx/`.
- Each skill is kept as an unpacked directory with `SKILL.md` as the required entrypoint.
- Supporting material is split into `references/`, `assets/`, `scripts/`, and optional `evals/`.
- The README skill tables use short display names; the actual slash command comes from each `SKILL.md` frontmatter `name` field.
- Last download-folder sync: 2026-04-21, covering existing matching skills only.
- 2026-07-02: `notion-infographic` and `ppt-designer` merged into `deck-studio` (v3); old directories removed, v2 assets preserved under `references/v2-pipeline/`.

## Install in Claude Code

Claude Code skills are directory-based: each skill needs a `SKILL.md` entrypoint and can include supporting files such as references, templates, examples, and scripts. The official guidance is to keep `SKILL.md` focused, reference supporting files from it, and move large details out of the entrypoint.

1. Pick a skill directory from this repository.
2. Copy the whole directory into one of these locations:
   - Personal: `~/.claude/skills/<skill-name>/`
   - Project: `.claude/skills/<skill-name>/`
3. Keep `SKILL.md` and its supporting files in the same directory.
4. Invoke the skill by the `name` declared in `SKILL.md`, for example `/deep-research`.

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
- Keep `SKILL.md` focused on activation, workflow, and navigation. Aim to keep it under 500 lines.
- Move large reference material into `references/` or `assets/`, and link those files from `SKILL.md`.
- Put executable helpers in `scripts/`.
- Keep evaluation fixtures in `evals/` when the skill includes repeatable routing or quality checks.
- Preserve upstream structure only when syncing external skills with minimal changes.
- Do not commit macOS `._*` metadata files or one-off local package exports.

## Maintenance Workflow

Use this flow when syncing from downloaded `.skill` packages:

1. Unpack the candidate package into a temporary directory.
2. Match it only to an existing repository skill unless intentionally adding a new one.
3. Preserve repo naming conventions: `skills/Geek-skills-xxx/`, `references/`, `assets/`, `scripts/`, and `evals/`.
4. Keep useful upstream updates, but avoid reverting normalized frontmatter unless the slash command is intentionally changing.
5. Update this README whenever the visible skill list, layout rules, or notable sync status changes.

## Validation

Before publishing, run lightweight checks:

```bash
git status --short
find skills llm-wiki -name SKILL.md | sort
git ls-files | rg '(^|/)\._'
python3 scripts/validate.py            # structural assertions for every skill
python3 scripts/run_routing_evals.py   # routing eval schema + consistency
```

The `rg` command should produce no output (confirms AppleDouble files are not tracked); the two Python checks should both end with `L1 PASS`.

## Curated Skills

### Development & Architecture

| Skill | Path | Description |
|-------|------|-------------|
| `pair-programming` | [skills/Geek-skills-pair-programming](skills/Geek-skills-pair-programming/SKILL.md) | Pair programming partner with automatic code review |
| `security-audit` | [skills/Geek-skills-security-audit](skills/Geek-skills-security-audit/SKILL.md) | Comprehensive code security audit |
| `solution-architect` | [skills/Geek-skills-solution-architect](skills/Geek-skills-solution-architect/SKILL.md) | System design, tech selection, and architecture review |
| `threejs-performance` | [skills/Geek-skills-threejs-performance](skills/Geek-skills-threejs-performance/SKILL.md) | Three.js performance optimization |

### AI-Native Methodology

| Skill | Path | Description |
|-------|------|-------------|
| `keqian-method` | [skills/Geek-skills-keqian-method](skills/Geek-skills-keqian-method/SKILL.md) | Keqian's AI-Native product dev methodology: single-agent, SDD, quality gates |
| `xuefeng-method` | [skills/Geek-skills-xuefeng-method](skills/Geek-skills-xuefeng-method/SKILL.md) | Xuefeng's AI-Native methodology for open-behavior, model-driven products |
| `ai-sales-champion` | [skills/Geek-skills-ai-sales-champion](skills/Geek-skills-ai-sales-champion/SKILL.md) | AI sales/consulting dialogue helper — turn tech into business language |

### Product & Content

| Skill | Path | Description |
|-------|------|-------------|
| `product-manager` | [skills/Geek-skills-product-manager](skills/Geek-skills-product-manager/SKILL.md) | PRD writing, requirement analysis, and product strategy |
| `wechat-article-writer` | [skills/Geek-skills-wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md) | Multi-style WeChat article writing |
| `deck-studio` | [skills/Geek-skills-deck-studio](skills/Geek-skills-deck-studio/SKILL.md) | PPT production agent: scene → style library → outline → page schema → deck or per-page visuals (v3; merges `notion-infographic` + `ppt-designer`) |
| `podcast-generator` | [skills/Geek-skills-podcast-generator](skills/Geek-skills-podcast-generator/SKILL.md) | Volcano Engine dual-speaker AI podcast generator |

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

## 仓库状态

- 自维护技能统一放在 `skills/Geek-skills-xxx/`。
- 每个 skill 都以解包目录形式保存，`SKILL.md` 是必需入口。
- 支持资料按用途拆到 `references/`、`assets/`、`scripts/` 和可选的 `evals/`。
- README 表格中的技能名是短展示名；真正的 slash command 以对应 `SKILL.md` frontmatter 里的 `name` 为准。
- 最近一次按下载目录同步：2026-04-21，只更新仓库中已有的匹配技能。
- 2026-07-02：`notion-infographic` 与 `ppt-designer` 合并为 `deck-studio`（v3）；旧目录已移除，v2 资产保留在 `references/v2-pipeline/`。

## 在 Claude Code 中安装

Claude Code 的 skill 以目录为单位组织：每个 skill 至少包含一个 `SKILL.md` 入口文件，并可按需附带参考资料、模板、示例或脚本。官方建议让 `SKILL.md` 保持聚焦，从入口文件引用 supporting files，并把大块细节拆到单独文件。

1. 从本仓库选择一个 skill 目录。
2. 将整个目录复制到以下任一位置：
   - 个人级：`~/.claude/skills/<skill-name>/`
   - 项目级：`.claude/skills/<skill-name>/`
3. 保持 `SKILL.md` 与 supporting files 在同一个目录内。
4. 调用时使用 `SKILL.md` 中声明的 `name`，例如 `/deep-research`。

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
- `SKILL.md` 只保留触发条件、主流程和导航信息，尽量控制在 500 行以内。
- 大块参考资料优先拆到 `references/` 或 `assets/`，并从 `SKILL.md` 中说明何时加载。
- 可执行辅助脚本放到 `scripts/`。
- 需要重复验证的路由或质量检查资源，放到 `evals/`。
- 同步外部技能时，只有在低风险情况下才做结构规范化；否则保留上游原始布局。
- 不提交 macOS `._*` 元数据文件，也不提交一次性的本地 `.skill` 导出包。

## 维护流程

从下载目录同步 `.skill` 包时，按这个流程处理：

1. 先把候选 `.skill` 解包到临时目录。
2. 默认只匹配并更新仓库里已经存在的 skill，除非明确要新增。
3. 保留仓库目录约定：`skills/Geek-skills-xxx/`、`references/`、`assets/`、`scripts/` 和 `evals/`。
4. 合入上游有效内容，但不要无意中把已经规范化的 frontmatter 改回旧格式。
5. 如果技能列表、目录约定或重要同步状态变化，同步更新 README。

## 发布前校验

发布前至少跑这些轻量检查：

```bash
git status --short
find skills llm-wiki -name SKILL.md | sort
git ls-files | rg '(^|/)\._'
python3 scripts/validate.py            # 全部 skill 的结构断言
python3 scripts/run_routing_evals.py   # 路由 evals 格式与一致性
```

`rg` 那条应当没有输出（确认 AppleDouble 文件未被跟踪）；两条 Python 检查都应以 `L1 PASS` 结尾。

## 自维护技能

### 开发与架构

| 技能 | 路径 | 说明 |
|------|------|------|
| `pair-programming` | [skills/Geek-skills-pair-programming](skills/Geek-skills-pair-programming/SKILL.md) | 结对编程搭档，自动审查代码质量 |
| `security-audit` | [skills/Geek-skills-security-audit](skills/Geek-skills-security-audit/SKILL.md) | 全面代码安全审计 |
| `solution-architect` | [skills/Geek-skills-solution-architect](skills/Geek-skills-solution-architect/SKILL.md) | 系统设计与技术选型 |
| `threejs-performance` | [skills/Geek-skills-threejs-performance](skills/Geek-skills-threejs-performance/SKILL.md) | Three.js 性能优化 |

### AI-Native 方法论

| 技能 | 路径 | 说明 |
|------|------|------|
| `keqian-method` | [skills/Geek-skills-keqian-method](skills/Geek-skills-keqian-method/SKILL.md) | 克谦式 AI-Native 产品开发方法论：单 Agent、SDD、质量门禁 |
| `xuefeng-method` | [skills/Geek-skills-xuefeng-method](skills/Geek-skills-xuefeng-method/SKILL.md) | 雪峰式 AI-Native 方法论，面向行为开放、模型驱动的产品 |
| `ai-sales-champion` | [skills/Geek-skills-ai-sales-champion](skills/Geek-skills-ai-sales-champion/SKILL.md) | AI 销售/咨询对话助手，把技术讲成业务语言 |

### 产品与内容

| 技能 | 路径 | 说明 |
|------|------|------|
| `product-manager` | [skills/Geek-skills-product-manager](skills/Geek-skills-product-manager/SKILL.md) | PRD 创作、需求分析与产品策略 |
| `wechat-article-writer` | [skills/Geek-skills-wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md) | 多风格微信公众号文章创作 |
| `deck-studio` | [skills/Geek-skills-deck-studio](skills/Geek-skills-deck-studio/SKILL.md) | PPT 生产 Agent：场景识别 → 风格库 → 大纲 → 页面语法 → 内容稿或逐页视觉图（v3，合并自 `notion-infographic` + `ppt-designer`） |
| `podcast-generator` | [skills/Geek-skills-podcast-generator](skills/Geek-skills-podcast-generator/SKILL.md) | 火山引擎双人 AI 播客生成 |

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
