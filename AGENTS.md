# Repository Guidelines

## Project Structure & Module Organization
This repository is a collection of standalone skill artifacts stored at the repository root. You will primarily work with:
- `*.skill`: individual skill documents (source of truth)
- `*.zip`: packaged assets that accompany a skill (name should match the skill)
- `README.md`, `AGENTS.md`: minimal repository docs

There is no nested source tree and no dedicated tests directory at the moment. Prefer iterating on existing skills instead of introducing new parallel variants.

## Build, Test, and Development Commands
There are currently no standard build/test/dev-server commands. Most changes are content edits to skill files.

If automation is introduced later, document the canonical commands here (examples):
- `make validate`: validate formatting/structure
- `npm test`: run any added unit tests

## Coding Style & Naming Conventions
- Prefer ASCII in `.skill` files unless non-ASCII is required by the skill content.
- Use clear Title Case filenames and the `.skill` suffix, for example `New Feature Skill.skill`.
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
