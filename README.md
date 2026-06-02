# Live Developer — Agent Skills Repository

**Maintainer:** Daniel Calisaya / Live Developer  
**Audience:** OPUS / Claude CLI agents operating within Live Developer's agentic infrastructure  
**Purpose:** Foundational skill directory for specialized agent workflows — audited, versioned, and production-ready.

---

## Repository Structure

```
LiveSkills/
├── README.md                      ← This file
├── dev-code-agent/                ← Multi-language programming + agent processes
│   ├── SKILL.md
│   └── references/
│       ├── python.md
│       ├── php-laravel.md
│       ├── typescript-node.md
│       └── agent-process-patterns.md
└── frontend-ui-agent/             ← Landings, dashboards, UI systems
    ├── SKILL.md
    └── references/
        ├── landing-pages.md
        ├── dashboards.md
        └── design-system.md
```

---

## Skill Index

| Skill | Domain | Trigger |
|---|---|---|
| `dev-code-agent` | Multi-language code + agent orchestration | Code tasks, pipelines, APIs, agent workflows |
| `frontend-ui-agent` | Landings, dashboards, component systems | UI, visual interfaces, frontend builds |

---

## Usage in Claude CLI (OPUS)

Skills are loaded by OPUS when a task matches the skill's trigger description. To reference a skill explicitly:

```bash
claude --skill ./dev-code-agent "Create a Python FastAPI endpoint with JWT auth"
claude --skill ./frontend-ui-agent "Build a SaaS landing page for LiveApp"
```

---

## Maintenance Guidelines

- Each `SKILL.md` has a YAML frontmatter with `name`, `description`, `version`, and `maintainer`.
- Reference files live in `references/` and are loaded selectively — only what's needed per task.
- When updating a skill: bump the `version` field, add a `# Changelog` entry at the bottom of `SKILL.md`.
- Audit cycle: review after every 10 production uses or quarterly, whichever comes first.

---

## Authorship & License

© 2025–2026 Daniel Calisaya / Live Developer — Quito, Ecuador  
Internal use. Not for public redistribution without written authorization.
