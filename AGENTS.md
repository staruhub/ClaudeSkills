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
There are currently no standard build/test/dev-server commands. Most changes are content edits to skill files.

If automation is introduced later, document the canonical commands here (examples):
- `make validate`: validate formatting/structure
- `npm test`: run any added unit tests

## Coding Style & Naming Conventions
- Prefer ASCII in `SKILL.md` files unless non-ASCII is required by the skill content.
- Skill directories use `Geek-skills-xxx` naming convention (lowercase kebab-case after prefix).
- Keep artifacts small and focused; avoid single files growing beyond ~200-300 lines without refactoring.
- Avoid duplication: update existing skills instead of copying large sections across files.

## Testing Guidelines
No automated tests are present. If you add tests:
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
