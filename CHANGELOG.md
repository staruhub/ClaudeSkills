# Changelog

本仓库遵循语义化的变更记录。日期为 `YYYY-MM-DD`（本地时区）。

## [Fable 5 重构版] — 2026-07-02

由 Claude Fable 5 主导的一次全仓库质量重构。目标：把 20 个自维护 skill 从
"能用但松散"提升到统一的可验证质量标准，并沉淀可回归的校验基建。

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

- **20 个 skill 全部达标**：description 从"它是什么"改为"何时触发"并补负触发；
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
  消除与"不维护 CVE 清单"的文档矛盾；去除 SKILL.md 中 `--break-system-packages` 危险安装命令。
- `deep-research`：`verify_citations.py` 的 URL 归一化重写（保留合法查询串语法）；
  `subagent-prompt.md` 修正 `reference/` → `references/` 路径。

### 移除

- `Geek-skills-notion-infographic/` 与 `Geek-skills-ppt-designer/` 目录（合并入 deck-studio；
  v2 资产保留在 `deck-studio/references/v2-pipeline/`，无内容丢失）。

### 已知遗留（非阻塞）

- name 前缀大小写统一（18 skill 用 `Geek-skills-` 大写前缀）属破坏性变更，待治理决策。
- ClawTime/WorkBuddy 风格色值为初稿，待品牌资产校准。
- deck-studio 后续批次：风格推荐 evals、image 分支实测、风格库扩至 24+。
