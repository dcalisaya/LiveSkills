---
name: dev-code-agent
description: >
  Multi-language programming skill with structured agent process patterns. Use this skill
  for any coding task — writing, reviewing, refactoring, debugging, or architecting code
  across Python, PHP/Laravel, TypeScript/Node.js, Bash, and SQL. Also activates for agent
  pipeline design, API integration, CLI tooling, background workers, data processing scripts,
  test suites, and any task where executable code is the primary deliverable. Trigger whenever
  the user says "write", "build", "fix", "refactor", "create a script", "set up a pipeline",
  "implement", or "code" — even if the request is vague or informal.
version: 1.0.0
maintainer: Daniel Calisaya / Live Developer
---

# Dev Code Agent Skill

This skill guides OPUS through production-quality code generation and agent-process design across
the Live Developer technology stack. All output must be clean, auditable, and deployment-ready.

---

## Agent Thinking Process

Before writing a single line of code, execute this internal checklist:

1. **Classify the task** — Is this new code, a fix, a refactor, an integration, or a pipeline?
2. **Identify the language and runtime** — See Language Selection below.
3. **Identify the context** — Solo script, API endpoint, background job, agent step, or library?
4. **Define the contract** — What are the inputs, outputs, side effects, and failure modes?
5. **Load the relevant reference** — Read the appropriate file in `references/` before coding.
6. **Select the agent process pattern** — See Agent Process Patterns below.

---

## Language Selection

| Trigger | Language | Reference |
|---|---|---|
| Django, FastAPI, data pipeline, ML, scripting | Python 3.11+ | `references/python.md` |
| Laravel, WordPress, cPanel, legacy web, API backends | PHP 8.2+ / Laravel | `references/php-laravel.md` |
| React, Next.js, Node services, CLI tools, APIs | TypeScript / Node.js | `references/typescript-node.md` |
| Infrastructure, deploy scripts, CI hooks | Bash / Shell | `references/bash-shell.md` |
| Migrations, queries, reports | SQL (PostgreSQL 16+) | `references/sql-postgresql.md` |

If the task is ambiguous, ask one clarifying question before proceeding.

---

## Universal Code Quality Standards

Apply these regardless of language:

- **Single Responsibility** — Every function/class does one thing.
- **Explicit over implicit** — Name variables, parameters, and return types clearly.
- **Error handling first** — Handle every failure path. No silent exceptions.
- **No magic values** — Extract constants, use enums or config.
- **Comments for WHY, not WHAT** — Code explains itself; comments explain intent.
- **Security by default** — Validate inputs, sanitize outputs, never hardcode secrets.
- **Testability** — Write code that can be unit-tested without a full stack.

---

## Agent Process Patterns

Read `references/agent-process-patterns.md` for the full pattern library.
The four core patterns are:

### 1. Sequential Chain
One agent feeds output directly into the next. Use for linear transformations.
```
Input → AgentA → AgentB → AgentC → Output
```

### 2. Router / Classifier
A lead agent classifies the input and dispatches to the appropriate specialist.
```
Input → Classifier → [AgentA | AgentB | AgentC] → Output
```

### 3. Parallel Fan-Out + Merge
Multiple agents process simultaneously; a merge agent assembles the results.
```
Input → [AgentA ‖ AgentB ‖ AgentC] → MergeAgent → Output
```

### 4. Human-in-the-Loop (HITL)
Agent proposes, human approves/rejects, agent proceeds or revises.
```
Input → Agent → HITL Gate → [Approve → Execute | Reject → Revise]
```

Always declare which pattern you're using at the top of your implementation plan.

---

## Structured Output Format

When delivering code, always structure the response as:

```
## Plan
[2–4 bullet points describing the approach]

## Code
[The implementation — file(s) with clear headers]

## Usage
[Minimal example showing how to run/call this code]

## Notes
[Any gotchas, environment requirements, or follow-up tasks]
```

---

## File and Naming Conventions (Live Developer Stack)

- **Python**: `snake_case` files and functions, `PascalCase` classes. Prefer `pathlib` over `os.path`.
- **PHP/Laravel**: PSR-12. Controllers in `app/Http/Controllers`, services in `app/Services`.
- **TypeScript**: `camelCase` functions/vars, `PascalCase` types/interfaces/components. Strict mode always.
- **Bash**: Executable scripts named `verb-noun.sh`. Always `set -euo pipefail` at the top.
- **SQL**: UPPERCASE keywords. Table names `snake_case` plural. Index names `idx_table_column`.

---

## Security Requirements (Non-Negotiable)

- Never output real secrets, tokens, or credentials — use `<YOUR_SECRET_HERE>` placeholders.
- Environment variables via `.env` + a `.env.example` file. Never hardcode.
- Validate and sanitize all external inputs (HTTP requests, file reads, CLI args).
- Use parameterized queries. Never interpolate user input into SQL.
- Log errors to stderr or a logger; never expose stack traces to end users.

---

## Reference Files

Read the relevant reference file before coding:

- `references/python.md` — Python conventions, packages, async patterns, testing
- `references/php-laravel.md` — Laravel architecture, Eloquent, queues, API resources
- `references/typescript-node.md` — TypeScript config, ESM, Express/Fastify, testing
- `references/bash-shell.md` — Strict headers, logging, deploy scripts, argument parsing
- `references/sql-postgresql.md` — Schema conventions, query patterns, migrations, indexing
- `references/agent-process-patterns.md` — Full pattern catalog with code templates

---

# Changelog

## v1.0.0 — 2025-06
- Initial release. Foundation by Daniel Calisaya / Live Developer.
- Four agent process patterns established.
- Language reference structure defined.
