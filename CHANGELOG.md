# Changelog

本仓库遵循语义化的变更记录。日期为 `YYYY-MM-DD`（本地时区）。

## [P1 产品化] — 2026-07-03

把发布/安装链路从"看 README 手动复制"升级为可自动化、可一键安装。

### 新增

- **CI**：`.github/workflows/validate.yml` 在每次 push / PR 上跑两个 L1 gate（`validate.py`、
  `run_routing_evals.py`）+ 全量脚本编译检查 + AppleDouble 追踪检查。README 顶部加 CI badge。
- **一键安装脚本**：`scripts/install_skill.py <name>` 以**干净命令名**（去 `Geek-skills-` 前缀）
  把 skill 装到 `~/.claude/skills/<name>/` 或（`--project`）`./.claude/skills/<name>/`，`/deep-research`
  直接可用；支持 `--list / --force / --dry-run`，自动忽略 `__pycache__`。相比 `dist/` 方案，
  不产生重复入库的中间产物。README 安装章节改为"脚本安装（推荐）+ 手动"两条路径。

## [外部评审修复 P0] — 2026-07-03

针对一次外部评审的 P0 反馈，修正安装/调用链路的事实性错误（均已用 Claude Code 官方文档核验）。

### 修复

- **命令名说明纠错**：官方规则是 slash command 来自**安装后的目录名**，而非 frontmatter `name`。
  README 双语安装章节改为"复制并重命名到目标命令名"，并说明 `name` 只是显示标签、Claude 也会按
  `description` 自动加载。
- **frontmatter `name` 统一为短名**：此前 18 个写 `Geek-skills-xxx`、1 个写短名，自相矛盾；
  全部统一为短名（`deck-studio`、`product-manager` 等）。`name` 是显示标签、不决定命令名，
  故此改动非破坏性。
- **计数口径修正**：README/CHANGELOG 多处"20 个自维护 skill" → "19 个自维护 + 1 个上游 `llm-wiki`"。
- **security-audit OWASP 去年份**："OWASP Top 10 2024" → "以官方当前版本为准（现行 2025），
  离线清单标注可能过时"，消除与"时效性硬编码清零"的自相矛盾。
- **AGENTS.md 消除矛盾**："No automated tests are present" 改为承认两个 L1 quality gate 脚本存在。
- **措辞降调**："Fable 5 重构认证 / Certified" → "自审报告 / Self-Audit Report"，避免被误读为第三方背书，
  并给出可复现的校验命令。

## [Fable 5 重构版] — 2026-07-02

由 Claude Fable 5 主导的一次全仓库质量重构。目标：把 19 个自维护 skill
（外加上游同步的 `llm-wiki`）从"能用但松散"提升到统一的可验证质量标准，
并沉淀可回归的校验基建。

### 新增

- **Skill Quality Standard v1.0**：D0 门槛（一票否决）+ D1–D8 计 100 分的评估框架；
  行数以 300 行为满分线、500 行为硬顶；每个 skill 必备"三件套"——验收标准 / 不做什么 / 已知陷阱。
- **`scripts/validate.py`**：全部 skill 的结构断言（frontmatter、行数、三件套、孤儿文件、
  平台路径/CVE 硬编码），一条命令跑出 `L1 PASS`。
- **`scripts/run_routing_evals.py`**：路由 evals 的 L1 校验 + `--emit-prompts` 生成 L2 测试包；
  校验 schema、全局 id 唯一性、`route_to` 目标存在性、跨 skill prompt 冲突。
- **Routing evals 规范 v1.0**：`evals/routing-evals.json` 与 skill 同目录，字段
  `id/prompt/should_trigger/reason` + 可选 `boundary/route_to/expected_mode`；互斥对镜像双写。
  已覆盖 7 个高价值 skill 共 64 条用例。
- **`Geek-skills-deck-studio`（v3.0）**：由 `notion-infographic` + `ppt-designer` 合并而成的
  "PPT 生产 Agent"。四层架构（内容规划 / 风格系统 / 页面语法 / 渲染策略）、13 个风格模板
  （六大类，含 ChaoGeek/ClawTime/WorkBuddy 定制品牌风格）、三条铁律（先大纲后视觉、
  每页先 brief 后 prompt、全套单一风格）、10 条路由 evals。
- 各 skill 的 `evals/` 与 `references/` 补充：deep-research 补 evals 模式断言与 handoff 引用；
  university-exam-prep 下沉对话示例；ppt/solution-architect 的理论下沉到 references。
- `CHANGELOG.md`（本文件）。

### 变更

- **19 个自维护 skill 全部达标**：description 从"它是什么"改为"何时触发"并补负触发；
  统一补齐可判定的验收标准、"不做什么"、带具体表现的陷阱表。
- **deep-research（8.0 → 8.1.1）**：收敛 description（移除会诱导跳过正文的 "Success=" 总结句），
  修复负触发措辞使"简短但需证据"的请求正确命中 brief 模式（经 L2 回归确认）。
- 平台路径硬编码全仓清零（`/mnt/skills`、`/mnt/user-data`、`/home/claude` → 相对路径或宿主环境说明）。
- 时效性硬编码清零：写死的 CVE 编号、"2025 年趋势"、年份改为"实时搜索"指令或标注"记录时点、会过时"。
- README 双语索引同步；AGENTS.md 补充两条 canonical 校验命令。

### 修复（脚本层，行为与文档对齐）

- **c-drive-cleaner**：`clean_temp.py` 补系统关键目录保护清单（System32/WinSxS/Program Files 等），
  纯字符串归一化实现，兑现 SKILL.md "跳过系统关键目录"的承诺（原为虚假承诺）。
- **a-share-analyst**：`generate_report.py`/`technical_analysis.py` 的"建议买入/强烈买入/逢低布局"
  等指令式表述改为中性强弱描述（合规边界）；补 ST/退市/停牌过滤；SKILL.md 脚本清单诚实化
  （原声称 6 个策略脚本，实际仅 4 个）。
- **security-audit**：`secrets_scan.py` 新增脱敏，命中的密钥、上下文、JWT payload 只保留首尾+长度
  （兑现"不回显明文"）；`dependency_check.py` 的硬编码 CVE 表标注为"离线基线、会过时、需实时确认"，
  消除与"不维护 CVE 清单"的文档矛盾；去除 SKILL.md 中 `--break-system-packages` 危险安装命令；
  `full_scan.py` 记录缺失的扫描器并在报告中声明覆盖范围缩窄（兑现"零发现≠安全"），
  报告结构声明对齐脚本实际输出。
- `deep-research`：`verify_citations.py` 的 URL 归一化重写（保留合法查询串语法）；
  `subagent-prompt.md` 修正 `reference/` → `references/` 路径。

### 移除

- `Geek-skills-notion-infographic/` 与 `Geek-skills-ppt-designer/` 目录（合并入 deck-studio；
  v2 资产保留在 `deck-studio/references/v2-pipeline/`，无内容丢失）。

### 已知遗留（非阻塞，需外部输入或决策）

- ~~name 前缀大小写统一~~ → 已在 2026-07-03 批次解决（见下）。
- ClawTime/WorkBuddy 风格色值为初稿，待品牌资产校准后锁定。
- deck-studio 后续批次：风格推荐 evals、image 分支实测、风格库扩至 24+（新范围，待明确启动）。
