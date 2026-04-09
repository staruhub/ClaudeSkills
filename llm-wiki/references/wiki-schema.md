# Wiki Schema Reference

## _schema.md Format

The schema file is the wiki's configuration document. It records project metadata and wiki conventions.

```markdown
---
title: Wiki Schema
updated: YYYY-MM-DD
---

# Project Metadata

| Field | Value |
|-------|-------|
| Project Name | <name> |
| Language(s) | TypeScript, Python, etc. |
| Framework(s) | Next.js, FastAPI, etc. |
| Build System | npm, cargo, gradle, etc. |
| Entry Point(s) | src/index.ts, main.py, etc. |
| Test Framework | jest, pytest, etc. |
| Package Manager | pnpm, pip, etc. |
| Monorepo | yes/no |

# Directory Overview

<annotated tree of top-level directories and their purpose>

# Wiki Conventions

## Naming
- Article filenames: kebab-case.md (e.g., `user-auth.md`, `data-flow.md`)
- Directory names: lowercase, single word when possible

## Cross-references
- Use relative markdown links: `[Module Name](../modules/module-name.md)`
- Every article must be reachable from `_index.md` within 2 clicks

## Source Citations
- Reference source files as: `src/path/file.ext:L10-L25`
- Always include the file path in article frontmatter `sources` field

## Update Protocol
- After every update, bump the `updated` field in article frontmatter
- Append a summary line to `_log.md`
```

## _index.md Format

The index is a content-oriented catalog, NOT a flat file listing.

```markdown
---
title: Wiki Index
updated: YYYY-MM-DD
---

# <Project Name> Wiki

## Architecture
- [System Overview](architecture/overview.md) — High-level architecture and component diagram
- [Data Flow](architecture/data-flow.md) — How data moves through the system
- [Directory Structure](architecture/directory-structure.md) — Annotated project tree

## Modules
- [Auth](modules/auth.md) — Authentication and authorization
- [API Gateway](modules/api-gateway.md) — Request routing and middleware
- ...

## Concepts
- [Error Handling](concepts/error-handling.md) — Error strategy and patterns
- [Configuration](concepts/configuration.md) — Config loading and env vars
- ...

## APIs
- [REST API](apis/rest.md) — HTTP endpoints
- [CLI](apis/cli.md) — Command-line interface
- ...

## Guides
- [Setup](guides/setup.md) — Dev environment setup
- [Testing](guides/testing.md) — Running and writing tests
- ...
```

## _log.md Format

Chronological, append-only log with parseable timestamps.

```markdown
---
title: Wiki Log
---

# Wiki Activity Log

## 2026-04-09

- **[INIT]** Wiki created. Scanned 245 source files across 18 directories.
- **[WRITE]** architecture/overview.md — System architecture with component diagram
- **[WRITE]** modules/auth.md — Authentication module deep dive
- **[WRITE]** modules/api.md — API layer documentation
- **[INDEX]** Updated _index.md with 12 articles
- **[LINT]** Health check passed. 0 broken links, 0 orphan pages.

## 2026-04-15

- **[UPDATE]** modules/auth.md — Added OAuth2 PKCE flow (new in commit abc123)
- **[WRITE]** concepts/rate-limiting.md — New rate limiting middleware
- **[LINT]** Fixed 2 broken links in modules/api.md
```

Log entry tags:
- `[INIT]` — First build
- `[WRITE]` — New article created
- `[UPDATE]` — Existing article modified
- `[DELETE]` — Article removed
- `[RENAME]` — Article moved/renamed
- `[INDEX]` — Index updated
- `[LINT]` — Health check run
- `[SCHEMA]` — Schema updated

## Directory Structure

```
.llm-wiki/
├── _schema.md              # Project metadata + wiki conventions
├── _index.md               # Content-oriented catalog
├── _log.md                 # Chronological activity log
├── architecture/
│   ├── overview.md         # System architecture, component diagram
│   ├── data-flow.md        # Data flow through the system
│   └── directory-structure.md  # Annotated directory tree
├── modules/
│   ├── <module-a>.md       # One per major module
│   └── <module-b>.md
├── concepts/
│   ├── <concept-a>.md      # Cross-cutting concerns
│   └── <concept-b>.md
├── apis/
│   ├── <api-group>.md      # API surface documentation
│   └── ...
└── guides/
    ├── setup.md            # Dev environment setup
    ├── testing.md          # Testing guide
    └── ...
```
