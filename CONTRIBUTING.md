# Contributing | 贡献指南

Thanks for wanting to make these skills better. Two ways in:

## Report / suggest — 反馈与建议

[Open an issue](https://github.com/staruhub/ClaudeSkills/issues) for bugs, unclear docs, or ideas. If a skill misfired (triggered when it shouldn't, or produced a bad result), paste the prompt you used — misfire reports directly become new routing-eval cases.

发现 bug、文档不清、或有想法，直接[提 issue](https://github.com/staruhub/ClaudeSkills/issues)。如果某个 skill 误触发或产出质量差，请附上你当时的 prompt——误触发报告会直接变成新的路由 eval 用例。

## Contribute a skill — 投稿 skill

1. **Open an issue first** describing the job-to-be-done and why existing skills don't cover it. This avoids wasted work — we prefer iterating on existing skills over adding parallel variants.
2. **New skills land in [`lab/`](lab/)**, using the same directory layout (`Geek-skills-<name>/SKILL.md` + optional `scripts/`, `references/`, `assets/`, `evals/`).
3. **Graduation into the curated `skills/`** requires the Skill Quality Standard: the "三件套" (checkable acceptance criteria, explicit boundaries with hand-offs, a pitfall table from real failures), `SKILL.md` ≤ 500 lines, routing evals, and passing both gates:

   ```bash
   python3 scripts/validate.py && python3 scripts/run_routing_evals.py   # both must print L1 PASS
   ```

先开 issue 说清这个 skill 解决什么活、为什么现有的覆盖不了（我们优先迭代现有 skill，不加平行变体）。新 skill 先进 `lab/`，目录结构与 `skills/` 相同。毕业进精选集需满足质量标准：三件套（可判定验收标准 / 明确边界与移交 / 真实踩坑的陷阱表）、`SKILL.md` 不超过 500 行、配路由 evals、两个门禁全绿。

Repository conventions (naming, layout, sync rules) live in [AGENTS.md](AGENTS.md). Per-skill capability disclosure lives in [SECURITY.md](SECURITY.md) — if your skill ships code, its row in the matrix is part of the PR.

目录与命名约定见 [AGENTS.md](AGENTS.md)；逐 skill 能力披露见 [SECURITY.md](SECURITY.md)——如果你的 skill 带代码，矩阵里的对应行也是 PR 的一部分。
