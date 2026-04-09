# Article Templates

## Architecture Overview

```markdown
---
title: System Architecture
updated: YYYY-MM-DD
sources:
  - <entry-point files>
  - <config files>
---

# System Architecture

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | ... |
| Framework | ... |
| Database | ... |
| Cache | ... |
| Queue | ... |

## Component Diagram

<ASCII diagram showing major components and their relationships>

## Component Descriptions

### <Component A>
Purpose, responsibilities, key files.

### <Component B>
...

## See Also
- [Data Flow](data-flow.md)
- [Directory Structure](directory-structure.md)
```

## Module Article

```markdown
---
title: <Module Name>
updated: YYYY-MM-DD
sources:
  - src/module/index.ts
  - src/module/types.ts
---

# <Module Name>

<1-2 sentence summary of what this module does>

## Responsibility

What this module owns. What it does NOT own (boundary).

## Key Files

| File | Purpose |
|------|---------|
| `index.ts` | Entry point, exports public API |
| `types.ts` | Type definitions |
| `utils.ts` | Internal helpers |

## Public Interface

Key exported functions/classes with brief signatures:

- `createUser(input: CreateUserInput): Promise<User>` — Creates a new user
- `UserService` class — Manages user lifecycle

## Internal Patterns

Notable implementation patterns, design decisions, non-obvious logic.

## Dependencies

- **Depends on**: [Database](../concepts/database.md), [Auth](auth.md)
- **Depended by**: [API](../apis/rest.md), [CLI](../apis/cli.md)

## See Also
- [Related Module](related-module.md)
- [Related Concept](../concepts/related.md)
```

## Concept Article

```markdown
---
title: <Concept Name>
updated: YYYY-MM-DD
sources:
  - src/middleware/error-handler.ts
  - src/utils/errors.ts
---

# <Concept Name>

<1-2 sentence summary>

## How It Works

Explain the concept as implemented in this codebase. Include code snippets from actual source.

## Where It Appears

List modules/files where this concept is used:
- `src/api/middleware.ts:L45-L60` — Error middleware
- `src/services/user.ts:L12` — Custom error class

## Configuration

Relevant config options, env vars, defaults.

## See Also
- [Related Concept](related.md)
- [Related Module](../modules/related.md)
```

## API Article

```markdown
---
title: <API Group Name>
updated: YYYY-MM-DD
sources:
  - src/routes/users.ts
  - src/routes/auth.ts
---

# <API Group Name>

## Base URL / Entry Point

`/api/v1` or CLI command prefix, etc.

## Endpoints / Commands

### `GET /users`
- **Purpose**: List users
- **Auth**: Required (Bearer token)
- **Params**: `page`, `limit`, `search`
- **Response**: `{ users: User[], total: number }`
- **Source**: `src/routes/users.ts:L20-L45`

### `POST /users`
...

## Authentication

How auth works for this API surface.

## Error Responses

Common error shapes and codes.

## See Also
- [Auth Module](../modules/auth.md)
- [Error Handling](../concepts/error-handling.md)
```

## Guide Article

```markdown
---
title: <Guide Title>
updated: YYYY-MM-DD
---

# <Guide Title>

## Prerequisites

What you need before starting.

## Steps

### 1. <First Step>
Commands and explanation.

### 2. <Second Step>
...

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ... | ... |

## See Also
- [Related Guide](related-guide.md)
```

## Data Flow Article

```markdown
---
title: Data Flow
updated: YYYY-MM-DD
sources:
  - <relevant files>
---

# Data Flow

## Request Lifecycle

```
Client -> [API Gateway] -> [Auth Middleware] -> [Route Handler]
  -> [Service Layer] -> [Database] -> Response
```

<Describe each step with file references>

## Key Data Transformations

Where and how data changes shape as it moves through the system.

## See Also
- [System Architecture](overview.md)
```
