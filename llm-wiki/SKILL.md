---
name: llm-wiki
description: Build and maintain a structured LLM-generated wiki for any codebase. Use when the user asks to analyze/understand/document a codebase, build a code wiki, create project documentation from source, or update an existing .llm-wiki. Triggers on phrases like "build wiki", "analyze this codebase", "document this project", "update wiki", "llm-wiki", or when entering an unfamiliar project that has no .llm-wiki yet.
---

# LLM Wiki for Codebases

Build a persistent, interlinked markdown wiki that captures the architecture, modules, patterns, and APIs of a codebase. The wiki lives in `.llm-wiki/` at the project root. Humans curate and direct; the LLM handles all bookkeeping.

Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): raw sources are "compiled" into a structured wiki that compounds over time.

## Mode Detection

Determine the mode based on current state:

- **No `.llm-wiki/` directory exists** -> Full Build mode
- **`.llm-wiki/` exists** -> Update mode (diff and refresh)

## Full Build Workflow

### Phase 1: Reconnaissance

1. Read top-level files: README, package.json/Cargo.toml/go.mod/pyproject.toml/build.gradle etc.
2. Run `find` or Glob to map the directory tree (ignore node_modules, .git, vendor, dist, build, __pycache__, .venv)
3. Identify: language(s), framework(s), build system, entry point(s), test framework
4. Count files per directory to gauge module boundaries
5. Read CLAUDE.md / AGENTS.md / .cursor/rules if present - they contain valuable architectural context

Record findings in `.llm-wiki/_schema.md` (see references/wiki-schema.md for format).

### Phase 2: Skeleton

Create the directory structure:

```
.llm-wiki/
  _schema.md          # Wiki conventions and project metadata
  _index.md           # Content-oriented catalog by category
  _log.md             # Chronological build/update log
  architecture/       # High-level design docs
  modules/            # Per-module deep dives
  concepts/           # Cross-cutting concepts (auth, caching, error handling...)
  apis/               # API surface docs (REST endpoints, CLI commands, exported functions)
  guides/             # How-to guides (setup, deployment, testing)
```

### Phase 3: Core Articles

Write articles in priority order. See references/article-templates.md for templates.

**Priority 1 - Architecture:**
- `architecture/overview.md` - System architecture, component diagram (ASCII), tech stack
- `architecture/data-flow.md` - How data flows through the system
- `architecture/directory-structure.md` - Annotated directory tree

**Priority 2 - Modules:**
- One `modules/<name>.md` per major module/package/directory
- Cover: purpose, key files, public interface, internal patterns, dependencies

**Priority 3 - Concepts:**
- Cross-cutting concerns that span modules (auth, logging, error handling, state management, config)
- One `concepts/<name>.md` per concept

**Priority 4 - APIs:**
- External-facing API surfaces (REST routes, CLI commands, SDK exports)
- One `apis/<name>.md` per API group

**Priority 5 - Guides:**
- `guides/setup.md` - Dev environment setup
- `guides/testing.md` - How to run and write tests
- Other guides as relevant

### Phase 4: Index and Cross-link

1. Build `_index.md` - organized by category with one-line descriptions and links
2. Ensure every article has a `## See Also` section linking to related articles
3. Add backlinks: if A references B, B should reference A

### Phase 5: Lint

Run a health check over the wiki:
- Broken internal links (references to non-existent `.md` files)
- Orphan pages (not linked from `_index.md` or any other page)
- Missing coverage (directories/modules with no corresponding article)
- Stale references (mentions of files/functions that don't exist in codebase)
- Inconsistent terminology

Fix issues found. Log the lint run in `_log.md`.

## Update Workflow

When `.llm-wiki/` already exists:

1. **Read `_schema.md`** to understand project metadata and conventions
2. **Read `_log.md`** to see last update timestamp
3. **Detect changes** since last wiki build:
   - `git log --since="<last_update>" --name-status` if git available
   - Otherwise, compare directory tree against `architecture/directory-structure.md`
4. **Triage changes:**
   - New files/directories -> create new articles or update existing ones
   - Modified files -> re-read and update affected articles
   - Deleted files -> remove references, mark articles for cleanup
   - Renamed/moved files -> update paths in all referencing articles
5. **Update affected articles** - re-read source, rewrite sections as needed
6. **Update `_index.md`** if new articles added or old ones removed
7. **Run lint** (same as Phase 5 above)
8. **Append to `_log.md`** with timestamp, summary of changes

## Writing Guidelines

- **Be factual**: describe what the code does, not what it should do. Cite file paths and line ranges.
- **Use code snippets**: short inline examples from actual source, not invented ones.
- **Link aggressively**: every mention of another module/concept should be a markdown link to its article.
- **Keep articles focused**: one topic per article, 100-500 lines. Split if longer.
- **Frontmatter**: every article starts with a YAML frontmatter block:
  ```yaml
  ---
  title: Module Name
  updated: 2026-04-09
  sources:
    - src/module/index.ts
    - src/module/utils.ts
  ---
  ```
- **ASCII diagrams** over external images - they live in version control and render anywhere.
- **Language**: match the project's primary language. If the codebase comments are in English, write in English. If Chinese, write in Chinese.

## Agent Coordination

For large codebases (>500 source files), consider dispatching parallel agents:
- Agent per top-level module to write module articles concurrently
- One agent for architecture overview after modules are documented
- One agent for cross-linking and lint

## Gitignore

Add `.llm-wiki/` to `.gitignore` only if the user prefers it. By default, the wiki is intended to be committed alongside the code so the team benefits.

## Key Principles (from Karpathy)

1. **The wiki is the LLM's domain** - humans rarely edit it directly
2. **Knowledge compounds** - each query and exploration enriches the wiki
3. **Index files are critical** - `_index.md` enables the LLM to navigate efficiently
4. **Lint regularly** - catch rot before it spreads
5. **Log everything** - `_log.md` provides temporal context for future updates
