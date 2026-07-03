# Repository Guidelines

## Project Structure & Module Organization
Skills are stored as unpacked directories under `skills/`:

```
skills/
├── Geek-skills-xxx/
│   ├── SKILL.md        # Core skill definition (source of truth)
│   ├── scripts/        # Optional executable scripts
│   ├── references/     # Optional reference documents
│   └── assets/         # Optional templates and resources
├── Geek-skills-yyy/
│   └── ...
```

Other top-level files:
- `README.md`: project overview and skill index
- `AGENTS.md`: repository guidelines (this file)

Prefer iterating on existing skills instead of introducing new parallel variants.

## Build, Test, and Development Commands
Most changes are content edits to skill files. Two canonical checks exist:

- `python3 scripts/validate.py` — structural L1 assertions for every curated skill (frontmatter, line caps, 三件套 sections, orphan files, platform-path/CVE hardcoding). Run before publishing any skill change.
- `python3 scripts/run_routing_evals.py` — validates all `evals/routing-evals.json` files (schema, global id uniqueness, route_to targets, cross-skill prompt conflicts). Add `--emit-prompts` to produce an agent-based L2 routing test bundle. Run after changing any skill `description`.
- `python3 scripts/install_skill.py <name>` — install a skill under a clean command name (`--list`, `--project`, `--force`, `--dry-run`).

CI (`.github/workflows/validate.yml`) runs the two L1 gates plus a script compile-check on every push and PR.

## Syncing Downloaded `.skill` Packages

1. Unpack the candidate package into a temporary directory.
2. Match it only to an existing repository skill unless intentionally adding a new one.
3. Preserve repo naming conventions: `skills/Geek-skills-xxx/`, `references/`, `assets/`, `scripts/`, and `evals/`.
4. Keep useful upstream updates, but avoid reverting normalized frontmatter unless the slash command is intentionally changing. (Per Claude Code's rules, the slash command comes from the **installed directory name**, not the frontmatter `name`, which is only a display label.)
5. Update the README whenever the visible skill list, layout rules, or notable sync status changes. Last download-folder sync: 2026-04-21, covering existing matching skills only.

## Coding Style & Naming Conventions
- Prefer ASCII in `SKILL.md` files unless non-ASCII is required by the skill content.
- Skill directories use `Geek-skills-xxx` naming convention (lowercase kebab-case after prefix).
- Keep artifacts small and focused; avoid single files growing beyond ~200-300 lines without refactoring.
- Avoid duplication: update existing skills instead of copying large sections across files.

## Testing Guidelines
No full unit/integration test suite is present yet. Two pre-publish validation scripts act as **L1 quality gates** (see Build, Test, and Development Commands above): `scripts/validate.py` and `scripts/run_routing_evals.py`; both should print `L1 PASS`. If you add deeper tests:
- State the framework and how to run it (one command).
- Use consistent naming (for example `*.test.*`).
- Define any coverage expectations and what counts as "done".

## Commit & Pull Request Guidelines
This repository uses Git. Existing history uses short, imperative commit messages (for example `Add repository guidelines`).

Guidelines:
- Commits: imperative, minimal scope, no drive-by reformatting.
- PRs: include purpose, list affected files/skills, and note any validation performed. Add screenshots only when an artifact has a visual output.

## Security & Configuration Tips
Do not commit secrets or private data. If a skill requires credentials, document environment variable placeholders (for example `API_KEY`) rather than real values.
