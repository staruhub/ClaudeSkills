# Security & Trust

[English](#english) | [中文](#中文)

<a id="english"></a>

Installing a Claude Code skill means dropping instructions — and sometimes executable scripts — into your `~/.claude/skills/`. You should know exactly what each one can touch **before** you install it. This page is the honest, per-skill answer.

## How to read this

Every capability below is derived from the **bundled code** each skill actually ships, verified by grepping the scripts (network calls, file writes, deletions, subprocess, credentials) — not from marketing claims. Reproduce it yourself:

```bash
# what executable code a skill ships
find skills/Geek-skills-<name>/scripts -name '*.py' -o -name '*.sh'

# does it reach the network / write / delete / shell out?
grep -rE 'requests|urllib|http|socket'      skills/Geek-skills-<name>/scripts/
grep -rE 'open\([^)]*[wa]|write_text|to_csv' skills/Geek-skills-<name>/scripts/
grep -rE 'os\.remove|unlink|rmtree|shutil'   skills/Geek-skills-<name>/scripts/
grep -rE 'subprocess|os\.system|exec\('       skills/Geek-skills-<name>/scripts/
```

**Two kinds of risk, kept separate:**

1. **Bundled-script risk** — what the skill's own `scripts/*.py` do when run. This is the supply-chain surface and the focus of the matrix below.
2. **Agent-behavior risk** — a prompt-only skill can still *instruct Claude* to search the web or write a file, but those actions go through **Claude Code's own permission prompts**, which you approve case by case. A prompt-only skill ships **no code of its own**.

## Risk tiers

| Tier | Meaning | Skills |
|:---:|---|---|
| 🟢 **T0 — Prompt only** | No bundled executable code. Pure instructions; all actions gated by Claude Code's permission system. | `ai-sales-champion` · `deck-studio`¹ · `keqian-method` · `pair-programming` · `product-manager` · `solution-architect` · `threejs-performance` · `weather-forecast-report` · `wechat-article-writer` · `xuefeng-method` · `llm-wiki` |
| 🟡 **T1 — Local compute** | Ships scripts that read input and write output **on your machine only**. No network, no deletion, no credentials. | `gaokao-expert` · `university-exam-prep` |
| 🟠 **T2 — Network / API** | Scripts reach the network. Some need API credentials (which you supply via env vars). | `a-share-analyst` · `deep-research` · `mineru-pdf-parser` · `podcast-generator` · `seedream-imagegen` |
| 🔴 **T3 — Shells out / can delete** | Runs external tools via `subprocess`, or deletes/moves files. Read the notes before running. | `security-audit` · `c-drive-cleaner` |

¹ `deck-studio` ships no Python. Its **render pipeline is opt-in** and, when you choose to run it, invokes Node.js + headless Chrome locally to screenshot HTML — no network, no data leaves your machine.

## Per-skill capability matrix

Legend: ● = yes · ○ = no · — = n/a (no bundled code)

| Skill | Ships code | Reads files | Writes files | Network | Shells out | Needs creds | Can delete |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `ai-sales-champion` | ○ | — | — | — | — | — | — |
| `deck-studio` | ○¹ | — | — | ○ | ○¹ | ○ | ○ |
| `keqian-method` | ○ | — | — | — | — | — | — |
| `pair-programming` | ○ | — | — | — | — | — | — |
| `product-manager` | ○ | — | — | — | — | — | — |
| `solution-architect` | ○ | — | — | — | — | — | — |
| `threejs-performance` | ○ | — | — | — | — | — | — |
| `weather-forecast-report` | ○ | — | — | — | — | — | — |
| `wechat-article-writer` | ○ | — | — | — | — | — | — |
| `xuefeng-method` | ○ | — | — | — | — | — | — |
| `llm-wiki` | ○ | — | — | — | — | — | — |
| `gaokao-expert` | ● | ● | ● | ○ | ○ | ○ | ○ |
| `university-exam-prep` | ● | ● | ● | ○ | ○ | ○ | ○ |
| `a-share-analyst` | ● | ○ | ● | ● | ○ | ○² | ○ |
| `deep-research` | ● | ● | ● | ● | ● | ○ | ○ |
| `mineru-pdf-parser` | ● | ● | ● | ●³ | ○ | ○ | ○ |
| `podcast-generator` | ● | ○ | ● | ● | ○ | ● | ○ |
| `seedream-imagegen` | ● | ○ | ● | ● | ○ | ● | ○ |
| `security-audit` | ● | ● | ● | ○⁴ | ● | ○ | ○ |
| `c-drive-cleaner` | ● | ● | ○ | ○ | ○ | ○ | ●⁵ |

## Notes on the higher-risk skills

- **`c-drive-cleaner` (🔴 T3)** — the only skill that deletes files. Mitigations baked in: `safe_remove()` **defaults to `dry_run=True`** (simulates, deletes nothing) — you must pass `dry_run=False` explicitly to actually remove; and a hardcoded **protection list** (System32, WinSxS, Program Files, …) blocks system-critical directories. Windows-only; targets temp / recycle-bin / browser-cache paths.
- **`security-audit` (🔴 T3)** — reads your codebase to scan it and shells out (`subprocess`) to invoke external scanners (e.g. `pip-audit`); if a scanner isn't installed it declares reduced coverage rather than silently passing. Secrets found in your code are **redacted in the report** (first/last chars + length only), never echoed in plaintext. Its offline CVE table is labeled a stale baseline, not a live feed.
- **`deep-research` (🟠 T2)** — fetches URLs to verify citations and shells out for its run pipeline; writes run summaries to your working dir. No credentials required.
- **`podcast-generator` / `seedream-imagegen` (🟠 T2)** — call third-party APIs (Volcano Engine / image-gen) and **require credentials you provide via environment variables** (e.g. `API_KEY`, `APP_ID`). Documented as placeholders — the repo ships **no real keys**. Your inputs are sent to those APIs; treat them as you would any cloud service.
- **`a-share-analyst` (🟠 T2)** — pulls live market data via the `akshare` library (no key needed). Output is de-directivized (strength descriptions, not "buy/sell" instructions) and is **not investment advice**.
- **`mineru-pdf-parser` (🟠 T2)** — parses PDFs with the local `mineru` library; first run may download models over the network.

## What this repo does and doesn't guarantee

- ✅ **No secrets committed** — no real API keys, tokens, or private data live in the repo; credential needs are documented as env-var placeholders.
- ✅ **Reproducible audit** — the grep commands above and `python3 scripts/validate.py` let you re-derive every claim here yourself.
- ✅ **Deletion is opt-in and guarded** — the one destructive skill defaults to dry-run and protects system dirs.
- ⚠️ **This is a self-audit, not a third-party certification.** Skills are reviewed by the maintainer (with Claude); there is no external security attestation.
- ⚠️ **Third-party libraries are trusted as-is.** Where a skill imports `akshare`, `mineru`, an API SDK, or an external scanner, that dependency's own supply chain is out of scope here — pin and vet them per your own policy.
- ⚠️ **Claude Code's permission system is your backstop.** Even a T0 skill runs under Claude Code; keep file-write and command-execution prompts on if you want a per-action gate.

## Reporting a concern

Found something that doesn't match this page — a script that reaches the network where the matrix says it shouldn't, or a hardcoded secret? Open an issue on the repository. Please **do not** paste real credentials into the issue.

---

<a id="中文"></a>

# 安全与信任

装一个 Claude Code skill,等于把指令——有时还有可执行脚本——放进你的 `~/.claude/skills/`。你有权在**安装之前**就知道每个 skill 能碰什么。这一页给出诚实的、逐 skill 的答案。

## 怎么读这张表

下面每一项能力都来自每个 skill **实际打包的代码**,通过 grep 脚本(网络调用、文件写入、删除、subprocess、凭证)核实得出——不是宣传口径。你可以自己复现:

```bash
# 这个 skill 打包了哪些可执行代码
find skills/Geek-skills-<name>/scripts -name '*.py' -o -name '*.sh'

# 它会联网 / 写文件 / 删文件 / 调外部命令吗?
grep -rE 'requests|urllib|http|socket'      skills/Geek-skills-<name>/scripts/
grep -rE 'open\([^)]*[wa]|write_text|to_csv' skills/Geek-skills-<name>/scripts/
grep -rE 'os\.remove|unlink|rmtree|shutil'   skills/Geek-skills-<name>/scripts/
grep -rE 'subprocess|os\.system|exec\('       skills/Geek-skills-<name>/scripts/
```

**两种风险,分开看:**

1. **打包脚本风险**——skill 自己的 `scripts/*.py` 运行时干了什么。这是供应链风险面,也是下面矩阵的重点。
2. **Agent 行为风险**——纯 prompt skill 仍可能*指示 Claude* 去联网搜索或写文件,但这些动作都走 **Claude Code 自己的权限弹窗**,由你逐次批准。纯 prompt skill **本身不带任何代码**。

## 风险分级

| 级别 | 含义 | Skills |
|:---:|---|---|
| 🟢 **T0 — 纯 prompt** | 不带任何可执行代码。纯指令,所有动作由 Claude Code 权限系统把关。 | `ai-sales-champion` · `deck-studio`¹ · `keqian-method` · `pair-programming` · `product-manager` · `solution-architect` · `threejs-performance` · `weather-forecast-report` · `wechat-article-writer` · `xuefeng-method` · `llm-wiki` |
| 🟡 **T1 — 本地计算** | 带脚本,只在**你本机**读输入、写输出。不联网、不删除、不需凭证。 | `gaokao-expert` · `university-exam-prep` |
| 🟠 **T2 — 网络 / API** | 脚本会联网。部分需要 API 凭证(由你通过环境变量提供)。 | `a-share-analyst` · `deep-research` · `mineru-pdf-parser` · `podcast-generator` · `seedream-imagegen` |
| 🔴 **T3 — 调外部命令 / 可删文件** | 通过 `subprocess` 调外部工具,或删除/移动文件。运行前先看注释。 | `security-audit` · `c-drive-cleaner` |

¹ `deck-studio` 不带 Python。它的**渲染管线是可选的**,你选择运行时才在本地调 Node.js + headless Chrome 给 HTML 截图——不联网,数据不出本机。

## 逐 skill 能力矩阵

图例:● = 是 · ○ = 否 · — = 不适用(无打包代码)

| Skill | 带代码 | 读文件 | 写文件 | 联网 | 调外部命令 | 需凭证 | 可删文件 |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `ai-sales-champion` | ○ | — | — | — | — | — | — |
| `deck-studio` | ○¹ | — | — | ○ | ○¹ | ○ | ○ |
| `keqian-method` | ○ | — | — | — | — | — | — |
| `pair-programming` | ○ | — | — | — | — | — | — |
| `product-manager` | ○ | — | — | — | — | — | — |
| `solution-architect` | ○ | — | — | — | — | — | — |
| `threejs-performance` | ○ | — | — | — | — | — | — |
| `weather-forecast-report` | ○ | — | — | — | — | — | — |
| `wechat-article-writer` | ○ | — | — | — | — | — | — |
| `xuefeng-method` | ○ | — | — | — | — | — | — |
| `llm-wiki` | ○ | — | — | — | — | — | — |
| `gaokao-expert` | ● | ● | ● | ○ | ○ | ○ | ○ |
| `university-exam-prep` | ● | ● | ● | ○ | ○ | ○ | ○ |
| `a-share-analyst` | ● | ○ | ● | ● | ○ | ○² | ○ |
| `deep-research` | ● | ● | ● | ● | ● | ○ | ○ |
| `mineru-pdf-parser` | ● | ● | ● | ●³ | ○ | ○ | ○ |
| `podcast-generator` | ● | ○ | ● | ● | ○ | ● | ○ |
| `seedream-imagegen` | ● | ○ | ● | ● | ○ | ● | ○ |
| `security-audit` | ● | ● | ● | ○⁴ | ● | ○ | ○ |
| `c-drive-cleaner` | ● | ● | ○ | ○ | ○ | ○ | ●⁵ |

## 高风险 skill 注释

- **`c-drive-cleaner`(🔴 T3)**——唯一会删文件的 skill。内置缓解:`safe_remove()` **默认 `dry_run=True`**(只模拟,不删任何东西),必须显式传 `dry_run=False` 才真删;并带硬编码**保护清单**(System32、WinSxS、Program Files……)拦住系统关键目录。仅 Windows;针对 temp / 回收站 / 浏览器缓存路径。
- **`security-audit`(🔴 T3)**——读你的代码库做扫描,并用 `subprocess` 调外部扫描器(如 `pip-audit`);扫描器没装时会声明覆盖缩窄而非静默放行。代码里扫到的密钥在报告里**脱敏**(只留首尾字符+长度),绝不回显明文。离线 CVE 表标注为过时基线,不是实时源。
- **`deep-research`(🟠 T2)**——抓取 URL 校验引用,并为运行管线调外部命令;把 run summary 写到你的工作目录。无需凭证。
- **`podcast-generator` / `seedream-imagegen`(🟠 T2)**——调第三方 API(火山引擎 / 图像生成),**需要你通过环境变量提供凭证**(如 `API_KEY`、`APP_ID`)。文档里是占位符,仓库**不含任何真实密钥**。你的输入会发送给这些 API,请按对待任何云服务的方式处理。
- **`a-share-analyst`(🟠 T2)**——通过 `akshare` 库拉实时行情(不需 key)。输出已去指令化(强弱描述,而非"买/卖"指令),**不构成投资建议**。
- **`mineru-pdf-parser`(🟠 T2)**——用本地 `mineru` 库解析 PDF;首次运行可能联网下载模型。

## 本仓库保证什么、不保证什么

- ✅ **不含任何密钥**——仓库里没有真实 API key、token 或私有数据;凭证需求都以环境变量占位符记录。
- ✅ **审计可复现**——上面的 grep 命令和 `python3 scripts/validate.py` 让你自己复算此页每一条结论。
- ✅ **删除是可选且有护栏的**——唯一破坏性 skill 默认 dry-run 并保护系统目录。
- ⚠️ **这是自审,不是第三方认证。** skill 由维护者(借助 Claude)审阅,没有外部安全背书。
- ⚠️ **第三方库按原样信任。** skill 引入 `akshare`、`mineru`、API SDK 或外部扫描器时,这些依赖自身的供应链不在本页范围内——请按你自己的策略 pin 与审查。
- ⚠️ **Claude Code 的权限系统是你的兜底。** 即使 T0 skill 也在 Claude Code 下运行;想要逐动作把关,就保持文件写入与命令执行的弹窗开启。

## 反馈问题

发现与本页不符的地方——矩阵说不联网的脚本却联网了,或藏着硬编码密钥?请在仓库开 issue。请**不要**把真实凭证粘进 issue。

---

脚注:¹ 渲染管线可选,调本地 Node + Chrome · ² `akshare` 免费无需 key · ³ 首次运行可能下载模型 · ⁴ `requests` 等匹配为包名/正则字符串,非真实网络调用 · ⁵ 默认 dry-run,带系统目录保护清单
