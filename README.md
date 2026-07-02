# Geek Skills

[![validate](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml/badge.svg)](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml)

[English](#english) | [中文](#中文)

A curated repository of unpacked Claude Code skills. This repo keeps normalized in-house skills under `skills/` and preserves selected upstream imports when they are synced in their original layout.

## ✳️ Fable 5 Refactor — Self-Audit Report (Skill Quality Standard v1.0), 2026-07-02

Every curated skill in this repo was audited and rebuilt by **Claude Fable 5** against a single **Skill Quality Standard v1.0**. This is a *self-audit* (not a third-party certification): what the standard guarantees, and what changed to meet it. Reproduce the gate with `python3 scripts/validate.py` and `python3 scripts/run_routing_evals.py` — both should print `L1 PASS`.

**What every skill now guarantees**

- **Trigger accuracy** — `description` says *when to use* (not *what it is*) and lists explicit negatives so the skill stays out of the way when another one fits.
- **Checkable acceptance criteria** — a self-check list the agent can answer yes/no before claiming done.
- **Boundaries** — an explicit "不做什么 / when NOT to use", with hand-offs to sibling skills.
- **Pitfall tables** — concrete failure modes + fixes, drawn from real traps, not generic advice.
- **No stale hardcoding** — CVE numbers, years, and platform paths (`/mnt/...`, `/home/claude`) replaced with live-search instructions or relative paths.
- **Routing evals** — `evals/routing-evals.json` cases proving each skill triggers when it should and defers when it shouldn't.

**What changed in this refactor**

| Area | Change |
|------|--------|
| Merge | `notion-infographic` + `ppt-designer` → **`deck-studio`** (v3): a full PPT-production agent (scene → style library of 13 styles → outline → page schema → deck or per-page visuals). Old dirs removed; v2 assets kept under `references/v2-pipeline/`. |
| Refactor | All 19 curated skills (plus the upstream-synced `llm-wiki`) converged on Quality Standard v1.0 (三件套: acceptance criteria / boundaries / pitfalls). `deep-research` 8.0 → 8.1.1. |
| Script fixes | Behavior aligned with documented safety promises — `c-drive-cleaner` system-dir protection; `a-share-analyst` de-directivized output + ST filtering; `security-audit` secret redaction, CVE-table baseline disclaimer, and reduced-coverage declaration. |
| Tooling | New `scripts/validate.py` (structural L1 assertions) and `scripts/run_routing_evals.py` (routing eval schema + consistency). Both must print `L1 PASS`. |

Full record: **[CHANGELOG.md](CHANGELOG.md)**.

## ⭐ Featured Skills

Four flagship skills, each an end-to-end workflow rather than a single prompt:

| Skill | What it does | Reach for it when |
|-------|--------------|-------------------|
| 🔬 **[deep-research](skills/Geek-skills-deep-research/SKILL.md)** (v8.1) | Evidence-based research pipeline: scoped plan → parallel investigation → verified citations → decision brief. Single-agent by default, fans out only when it pays off; ships with evals and a degraded mode. | You need a cited memo, literature review, market/tech landscape, or a decision brief — not a quick lookup. |
| 🎞️ **[deck-studio](skills/Geek-skills-deck-studio/SKILL.md)** (v3) | PPT production agent: scene → recommend from a 13-style library → outline → page schema → deck content **or** per-page visual images. Iron rule: outline first, visuals second. | Making a report, pitch, course, or proposal deck — or turning an outline/article into slides or infographics. |
| 📋 **[product-manager](skills/Geek-skills-product-manager/SKILL.md)** | Senior PM: PRD authoring & review, retention/growth diagnosis, competitive research, feature prioritization — framework-driven, with "dev can start from this" acceptance bars. | Writing/reviewing a PRD, diagnosing low retention, or prioritizing features. |
| ✍️ **[wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md)** | Multi-style WeChat article writing with a built-in anti-translationese (反翻译腔) pass so Chinese long-form reads natively, not machine-translated. | Turning material into a publishable Chinese article (tech blog, product intro, event recap). |

## Repository Status

- Curated skills live in `skills/Geek-skills-xxx/`.
- Each skill is kept as an unpacked directory with `SKILL.md` as the required entrypoint.
- Supporting material is split into `references/`, `assets/`, `scripts/`, and optional `evals/`.
- The README skill tables use short display names. Per Claude Code's rules, the slash command comes from the **installed directory name**, not the frontmatter `name` (which is only the display label shown in skill listings; the plugin-root `SKILL.md` is the sole exception).
- Last download-folder sync: 2026-04-21, covering existing matching skills only.
- 2026-07-02: Fable 5 refactor (see the section above and [CHANGELOG.md](CHANGELOG.md)).

## Install in Claude Code

Claude Code skills are directory-based: each skill needs a `SKILL.md` entrypoint and can include supporting files such as references, templates, examples, and scripts. The official guidance is to keep `SKILL.md` focused, reference supporting files from it, and move large details out of the entrypoint.

**Quickest — the installer (recommended):** it copies the skill under a clean command name (prefix stripped), so `/deep-research` just works.

```bash
python3 scripts/install_skill.py --list            # see installable names
python3 scripts/install_skill.py deep-research      # -> ~/.claude/skills/deep-research  (command: /deep-research)
python3 scripts/install_skill.py deep-research --project   # -> ./.claude/skills/deep-research
```

**Manual:** the installed directory name *is* the slash command, so copy-and-rename.

1. Pick a skill directory (e.g. `skills/Geek-skills-deep-research`).
2. `cp -r skills/Geek-skills-deep-research ~/.claude/skills/deep-research` (Personal) or `.claude/skills/deep-research` (Project).
3. Keep `SKILL.md` and its supporting files together in that directory.
4. Invoke by the target directory name, e.g. `/deep-research`. (Copy without renaming → the command is `/Geek-skills-deep-research`.) Claude also auto-loads a skill when its `description` matches — `/command` is just the explicit way to invoke it.

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
| `pair-programming` | [skills/Geek-skills-pair-programming](skills/Geek-skills-pair-programming/SKILL.md) | Pair-programming partner: delivers code with a structured self-review, focused on AI-specific defects |
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

## ✳️ Fable 5 重构 — 自审报告（Skill 质量标准 v1.0），2026-07-02

本仓库全部自维护 skill 由 **Claude Fable 5** 按统一的 **Skill 质量标准 v1.0** 逐个审计并重构。这是一次*自审*（非第三方认证），说明两件事：标准保证了什么，以及为达标改了什么。可用 `python3 scripts/validate.py` 与 `python3 scripts/run_routing_evals.py` 复现校验，两者都应打印 `L1 PASS`。

**每个 skill 现在保证**

- **触发准确**——`description` 写"何时用"而非"是什么"，并列出负触发，别的 skill 更合适时主动让路。
- **可判定验收标准**——一份 agent 能自答是/否的自查清单，答完才算完成。
- **能力边界**——明确的"不做什么"，并给出移交给兄弟 skill 的指引。
- **陷阱表**——来自真实踩坑的失败模式 + 应对，而非泛泛而谈。
- **无过时硬编码**——写死的 CVE 编号、年份、平台路径（`/mnt/...`、`/home/claude`）改为实时搜索指令或相对路径。
- **路由 evals**——`evals/routing-evals.json` 用例证明该触发时触发、不该触发时让路。

**本次重构改了什么**

| 方面 | 改动 |
|------|------|
| 合并 | `notion-infographic` + `ppt-designer` → **`deck-studio`**（v3）：完整的 PPT 生产 Agent（场景 → 13 个风格库 → 大纲 → 页面语法 → 内容稿或逐页视觉图）。旧目录移除，v2 资产保留在 `references/v2-pipeline/`。 |
| 重构 | 19 个自维护 skill（外加上游同步的 `llm-wiki`）统一到质量标准 v1.0（三件套：验收标准 / 边界 / 陷阱）。`deep-research` 8.0 → 8.1.1。 |
| 脚本修复 | 让代码行为兑现文档承诺——`c-drive-cleaner` 系统目录保护；`a-share-analyst` 去指令化 + ST 过滤；`security-audit` 密钥脱敏、CVE 表基线声明、覆盖范围缩窄声明。 |
| 工具链 | 新增 `scripts/validate.py`（结构断言）与 `scripts/run_routing_evals.py`（路由 eval 校验）。两者都必须打印 `L1 PASS`。 |

完整记录见 **[CHANGELOG.md](CHANGELOG.md)**。

## ⭐ 核心推荐

四个旗舰 skill，每个都是端到端的工作流，而不是单条 prompt：

| Skill | 做什么 | 什么时候用 |
|-------|--------|-----------|
| 🔬 **[deep-research](skills/Geek-skills-deep-research/SKILL.md)**（v8.1） | 循证研究流水线：定范围 → 并行调查 → 校验引用 → 决策简报。默认单 Agent，值得时才并行；内置 evals 与降级模式。 | 需要带引用的备忘、综述、市场/技术全景或决策简报——而不是快速查一下。 |
| 🎞️ **[deck-studio](skills/Geek-skills-deck-studio/SKILL.md)**（v3） | PPT 生产 Agent：识别场景 → 从 13 个风格库推荐 → 先出大纲 → 定义页面 → 输出内容稿**或**逐页视觉图。铁律：先大纲后视觉。 | 做汇报/路演/课件/提案的 PPT，或把大纲、文章做成 slides、信息图。 |
| 📋 **[product-manager](skills/Geek-skills-product-manager/SKILL.md)** | 资深 PM：PRD 创作与评审、留存/增长诊断、竞品研究、功能优先级——框架驱动，验收标准做到"开发照着就能动手"。 | 写/评审 PRD、诊断留存低、给功能排优先级。 |
| ✍️ **[wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md)** | 多风格公众号文章创作，内置反翻译腔精修，让中文长文读起来是"人写的"而非机翻。 | 把素材写成可发布的中文长文（技术博客、产品介绍、活动回顾）。 |

## 仓库状态

- 自维护技能统一放在 `skills/Geek-skills-xxx/`。
- 每个 skill 都以解包目录形式保存，`SKILL.md` 是必需入口。
- 支持资料按用途拆到 `references/`、`assets/`、`scripts/` 和可选的 `evals/`。
- README 表格里的技能名是短展示名。按 Claude Code 官方规则，slash command 来自**安装后的目录名**，而非 frontmatter 的 `name`（`name` 只是技能列表里的显示标签；唯一例外是 plugin 根目录的 `SKILL.md`）。
- 最近一次按下载目录同步：2026-04-21，只更新仓库中已有的匹配技能。
- 2026-07-02：Fable 5 重构（见上方板块与 [CHANGELOG.md](CHANGELOG.md)）。

## 在 Claude Code 中安装

Claude Code 的 skill 以目录为单位组织：每个 skill 至少包含一个 `SKILL.md` 入口文件，并可按需附带参考资料、模板、示例或脚本。官方建议让 `SKILL.md` 保持聚焦，从入口文件引用 supporting files，并把大块细节拆到单独文件。

**最快——用安装脚本（推荐）：** 它会以干净的命令名（去掉前缀）复制 skill，`/deep-research` 直接可用。

```bash
python3 scripts/install_skill.py --list            # 查看可安装的名字
python3 scripts/install_skill.py deep-research      # -> ~/.claude/skills/deep-research（命令：/deep-research）
python3 scripts/install_skill.py deep-research --project   # -> ./.claude/skills/deep-research
```

**手动：** 安装后的目录名就是 slash command，所以复制时改名。

1. 选一个 skill 目录（例如 `skills/Geek-skills-deep-research`）。
2. `cp -r skills/Geek-skills-deep-research ~/.claude/skills/deep-research`（个人级）或 `.claude/skills/deep-research`（项目级）。
3. 保持 `SKILL.md` 与 supporting files 在同一目录内。
4. 用目标目录名调用，例如 `/deep-research`。（不改名直接复制 → 命令是 `/Geek-skills-deep-research`。）Claude 也会在 `description` 匹配时自动加载，`/命令` 只是显式调用方式之一。

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
| `pair-programming` | [skills/Geek-skills-pair-programming](skills/Geek-skills-pair-programming/SKILL.md) | 结对编程搭档，交付代码附带结构化自审，重点盯 AI 生成代码特有缺陷 |
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
