# Changelog

本仓库遵循语义化的变更记录。日期为 `YYYY-MM-DD`（本地时区）。

## [README 首屏去证明化重排] — 2026-07-04

第二轮外部批评"系统级设计卡在文档级表达、缺一个现在就点进去用的理由"——外科手术式重排(非去工程化重写)。

### 变更

- **tagline 改 outcome-first**:从"带质量门禁/路由 evals/盲评分数的仓库"→"一句话进,一套
  能上台讲的 deck"。工程可信度不删,下沉为第二拍。
- **单点爆炸入口**:首屏三拍改为 输入命令 → 单张 hero 大图 → 30 秒安装,让"想试"当场可点;
  四旗舰平列菜单下沉到安装之后。
- **证据降为第二拍**「别听我说,看盲评」:2×2 分数画廊 + 轨迹 + 风格条移到安装后——先给爽点,
  再给"这不是我吹的,是盲评打的"。
- **守住锚点**(拒绝"只留一行"的 over-correction,重演 v4 全细体 3:0 落败教训):gates/evals 是
  唯一尖锐差异化(对标第一篇批评"你不够尖锐"),删了等于弃械,故保留仅重排序。中英同构。

## [SECURITY.md 信任矩阵] — 2026-07-04

回应外部诊断第四点"越能干活的 skill 越让人犹豫敢不敢装本地"——补上逐 skill 信任表。

### 新增

- **`SECURITY.md`**（双语）：19 个 skill 的能力矩阵——带代码/读文件/写文件/联网/调外部
  命令/需凭证/可删文件七列,全部由 grep 打包脚本核实(非宣传口径),附可复现命令。
- **四级风险分级**:🟢 T0 纯 prompt(11 个,零代码)/ 🟡 T1 本地计算 / 🟠 T2 网络·API /
  🔴 T3 调外部命令·可删文件。诚实标注唯一破坏性 skill `c-drive-cleaner` 默认 dry-run +
  系统目录保护清单;`security-audit` 密钥脱敏 + subprocess 调扫描器。
- 区分"打包脚本风险"与"agent 行为风险"(后者走 Claude Code 权限系统),并声明自审非
  第三方认证、第三方库按原样信任。README 差异化区挂 SECURITY.md 链接。

## [README 产品化重构] — 2026-07-04

回应外部诊断"高手能看懂的好项目,但不是普通人一眼想转发的产品":首屏从规范说明书改为 demo 展示。

### 变更

- **首屏 = 看得见的结果**:deck-studio 四套样例封面 2×2 画廊(带盲评/绝对分)、
  17 风格库 4 张种子预览条、分数轨迹 6.0→7.1——先看菜,再看后厨 SOP。
- **30 秒安装**上移到第二屏,单条命令 + 一句 `/deck-studio` 用例;其他安装方式折叠。
- **差异化章节**「这个仓库有什么不同」:质量标准三件套 / 113 条路由 evals / CI 双门禁 /
  盲评证据链,吸收原 Fable 5 自审板块(保留"自审非第三方认证"声明与复现命令)。
- 19 技能全目录折叠进 `<details>`;维护类章节(目录约定/同步流程/发布校验)下沉——
  `.skill` 包同步流程移入 AGENTS.md,README 只留维护者入口。
- 尖刀定位:deck-studio 升为旗舰表首位(有截图、有分数,是"能拍碎砖的那一掌");
  deep-research 居次,等 benchmark 弹药(第二波)。

## [构成主义模板实测：首破 7 分线] — 2026-07-03

用新内置的构成主义红模板种子走完整流程实测，验证"种子扩成完整 deck 即达标"。

### 新增

- **第四套样例** `examples/constructivist-design-constitution/`：9 页构成主义 deck，
  内容为 dogfood（讲 deck-studio 自己的设计宪法）。独立评审绝对分 **7.1/10**——四轮
  实战最高，**首次突破 7 分工作室线**。
- 分数轨迹（同一绝对标准）：极夜 6.0 → 英黄 6.6 → 构成主义 6.6 →（按评审 fix 改进）7.1。
  证明签名页模板种子扩成 9 页即达 6.6，改一轮破 7——品味冻结进模板后可复用达标。

### 过程教训（render→评→改→复审，两轮）

- 首评 6.6 抓出 p6 死区/p4 对比度低/p9 淡粉角柔弱；改进后复评 7.1，但改进动作**自身
  引入两处新伤**：p9 红楔压穿页脚、p6 淡粉叠层（违反单一强调色）——"母题赢了网格纪律输了"。
- 二次修复清零两处新伤，沉淀进样例 README 的教训清单：装饰母题不得压页脚系统、修 A 页
  别引入 B 页被批的柔弱色、tone-on-tone 对角太含蓄需实色对撞。

## [风格路线图与四套大师风格] — 2026-07-03

T6 全景普查(26 来源,MoMA/Cooper-Hewitt/NN|g/Material 官方)落地。

### 新增

- **`references/style-roadmap.md`**:公认流派/大师按五条硬标准的评级表(高/中高/否决)、
  反面清单(Corporate Memphis 等公认廉价化风格永不收)、≤14 套终态蓝图——风格库扩张
  从此有带证据的路线图。
- **四套「高」评级风格**,每套含 10 字段定义 + **已渲染验证的签名页模板种子**(HTML,
  改文案即复用):Bauhaus 几何(三原色+圆方三角)/ 构成主义红(红楔白圆+对角线+巨型
  标点)/ Neubrutalism 硬糖(3px 黑描边+8px 硬阴影 CSS 配方)/ Aicher 信息系统(功能
  分色+网格图标)。风格库 13 → 17。
- 明确否决记录:Carson/Grunge(不可模板化)、Y2K(位图依赖)、Flat/Metro(与瑞士同构)、
  Crouwel(并入墨白)、佐藤可士和(策略>版式)。

## [visual-checklist 首次实战审计与修复] — 2026-07-03

新建的视觉门禁首次用于审计自己的样例,闭合"建标准→审→改→复审"循环。

### 修复(三套样例,fable 独立审计→修复→复审)

- 独立审计按 visual-checklist 逐条判定,抓出 9 条真违例(2 high);修复 top 3 后复审:
  **六条原违例全部 resolved,零新违例**,三页评分 8/8/7,判定"真改结构非表面补丁"。
- **极夜 p3**(B3 high):卡片"头重-空腹-脚轻"复发病——图形移入中段固定高度区,
  标题/图形/正文/结论行五段填实,空腹消除。
- **英黄 p7**(B7 high):交付物整列涂黄导致强调失效——改为仅 W3/W6 两处保留黄色,
  其余米白,强调回归辨识度。
- **墨白 p5**(B2+B4):数据页只画终态19格→改为"重构前 4/21 灰 vs 重构后 19/21 蓝"
  上下同构对比行,前后叙事由图形自身承载,指标下移填补真空。
- 过程记录:墨白 p5 首次修复曾把空心格边框做太淡致对比框架不可见,渲染自检抓出并回炉。

### 意义

visual-checklist 的诊断力经独立 agent 双向验证(审出真问题 + 确认修复有效);
B3"卡片空腹"作为标注的复发病被再次抓到,证明教训条目确实在拦截回归。

## [deck-studio 版式注册表与原典校验] — 2026-07-03

第二轮 deep-research（49 来源，满配并行）落地为两个核心资产 + 第三套实证样例。

### 新增

- **`references/layout-registry.md`**：14 个注册版式（L01–L14），全部来自三套盲评/评审
  验证过的样例；每页生成前必须选版式并声明 `layout: LXX`，不从零发明构图——对标归藏
  S01–S22 与 Slidev named-layouts 的"锁定版式"范式。附正交拆维组织原则（视觉流派 ×
  版式骨架 × 主题色独立策展）。
- **`references/visual-checklist.md`**：渲染后 L2 视觉门禁——原典量化 12 条（Duarte 75词/3秒、
  Tufte Lie Factor 0.95–1.05 与 chartjunk=0、Müller-Brockmann 网格、Butterick 行长行距、
  W3C clreq 中文禁则与混排间距）+ 实战教训 10 条（重锚点、防空腹、垂直重心、母题、对位同构等，
  每条附盲评/评审出处）。
- **第三套样例** `examples/yinghuang-bootcamp-proposal/`：黑金提案系（独立评审 6.6/10，
  三轮最高），含时间线"交付物行"修复与"空腹病"自检记录。

### 研究结论（注册进 registry）

- 中文生态两条生产函数：商业产品靠模板堆量+场景分类（AiPPT 10万+），公认最好看的开源
  skill（归藏 8.8k★、frontend-slides 17.5k★）反而靠**极小策展库+强约束**——印证"约束换美学"。
- 最值得逆向的 token 范式：Quarto 的 reveal.js Sass 变量表、Slidev 主题 layouts 词汇表、
  apple-bento-grid 单文件实现（与本管线同构）。

## [deck-studio 视觉管线与实证样例] — 2026-07-03

把「美学在线」从口号变成管线 + 证据。

### 新增

- **HTML→Chrome 截图→pptx 视觉管线**：字体由渲染机锁定（根除 pptx 字体 fallback 崩坏），
  CSS 全效果 2×DPI 确定性输出；render→agent 看图自检→修 的闭环跑通。
- **两个实证样例**（examples/）：明色系 `moshiro-consulting-report`（墨白咨询，三评委盲评
  42.3 vs 29.7 击败旧实现，且对调组一致）；暗色系 `polar-night-ai-native`（极夜科技 AI Native
  方法论，独立评审绝对分 6/10 专业级，按评审四条修复迭代至 v5.1）。
- **陷阱表新增四条实战教训**：全盘细体假高级（v4 盲评 3:0 落败实证——极端对比=极细与极重共存）、
  pptx 字体 fallback、中文正文半角标点、JS 中文引号炸脚本。
- deep-research 产出《如何做好美学在线的 PPT skill》报告：核心结论"美是继承的不是生成的"，
  对标拆解归藏 guizang-ppt-skill 七层资产（成品模板/锁定版式/封闭主题/节奏规则/排印纪律/
  checklist/validator），指明下一步是把风格冻结成归藏级模板包。

## [P1 路由 evals 扩面] — 2026-07-03

routing evals 覆盖从 7 个 skill 扩到 14 个（113 条用例）。

### 新增

- 为 solution-architect / pair-programming / ai-sales-champion / seedream-imagegen /
  gaokao-expert / a-share-analyst / university-exam-prep 各补 7 条 routing evals
  （3 正 + 3 负带 route_to + 1 边界），并互相镜像相邻 skill 的移交边界。
- a-share 的负例含"预测明日涨跌/该不该满仓"用例，固化合规边界；gaokao 与
  university-exam-prep 互为镜像（出题 vs 备考）。
- 仍未覆盖的 5 个纯窄工具（c-drive-cleaner / mineru-pdf-parser / podcast-generator /
  threejs-performance / weather-forecast-report）误触发面小，暂缓。

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
