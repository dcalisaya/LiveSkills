# Live Developer — Agent Skills Repository

**Maintainer:** Daniel Calisaya / Live Developer  
**Audience:** OPUS / Claude CLI agents operating within Live Developer's agentic infrastructure  
**Purpose:** Foundational skill directory for specialized agent workflows — audited, versioned, and production-ready.

---

## Repository Structure

```
LiveSkills/
├── MANIFEST.json                  ← Machine-readable skill registry (auto-discovery)
├── CHANGELOG.md                   ← Version history
├── README.md                      ← This file
├── LICENSE.md                     ← Proprietary license
│
├── dev-code-agent/                ← Multi-language programming + agent processes
│   ├── SKILL.md
│   └── references/
│       ├── python.md
│       ├── php-laravel.md
│       ├── typescript-node.md
│       ├── bash-shell.md
│       ├── sql-postgresql.md
│       └── agent-process-patterns.md
│
├── frontend-ui-agent/             ← Landings, dashboards, UI systems
│   ├── SKILL.md
│   └── references/
│       ├── landing-pages.md
│       ├── dashboards.md
│       ├── design-system.md
│       └── react-components.md
│
├── devops-infra-agent/            ← Servers, deploy, CI/CD, monitoring
│   ├── SKILL.md
│   └── references/
│       ├── proxmox-vms.md
│       ├── ci-cd.md
│       └── monitoring.md
│
├── content-copywriting-agent/     ← SEO, copy, email campaigns
│   ├── SKILL.md
│   └── references/
│       ├── seo.md
│       ├── copywriting.md
│       └── email-campaigns.md
│
├── qa-testing-agent/              ← Testing, code review, audits
│   ├── SKILL.md
│   └── references/
│       ├── testing-strategies.md
│       └── code-review.md
│
├── audiovisual-agent/             ← Video production, scripting, editing
│   ├── SKILL.md
│   └── references/
│       ├── pre-production.md
│       └── post-production.md
│
├── data-analysis-agent/           ← Data analysis, reporting, visualization
│   ├── SKILL.md
│   └── references/
│       ├── analysis-patterns.md
│       └── reporting.md
│
├── project-management-agent/      ← Planning, coordination, orchestration
│   ├── SKILL.md
│   └── references/
│       ├── planning.md
│       └── coordination.md
│
└── _template/                     ← Scaffold for creating new skills
    ├── README.md
    ├── SKILL.md
    └── references/
        └── example-reference.md
```

---

## Skill Index

| Skill | Domain | Triggers | Refs |
|---|---|---|---|
| `dev-code-agent` | DOM-DEV | write, build, fix, refactor, code, API, pipeline | 6 |
| `frontend-ui-agent` | DOM-DEV | landing, dashboard, UI, component, design system | 4 |
| `devops-infra-agent` | DOM-HST | deploy, server, VM, Docker, Nginx, CI/CD, SSL | 3 |
| `content-copywriting-agent` | DOM-MKT | copy, content, SEO, blog, email, newsletter | 3 |
| `qa-testing-agent` | DOM-DEV | test, review, QA, coverage, audit, lint, bug | 2 |
| `audiovisual-agent` | DOM-AV | video, storyboard, script, motion, edit, render | 2 |
| `data-analysis-agent` | DOM-DEV | analyze, report, chart, KPI, data, ETL, pandas | 2 |
| `project-management-agent` | DOM-OPS | plan, project, sprint, roadmap, estimate, coordinate | 2 |

### Domain Map

| Domain | Code | Skills |
|---|---|---|
| Development | DOM-DEV | `dev-code-agent`, `frontend-ui-agent`, `qa-testing-agent`, `data-analysis-agent` |
| Hosting & Infra | DOM-HST | `devops-infra-agent` |
| Marketing & Content | DOM-MKT | `content-copywriting-agent` |
| Audiovisual | DOM-AV | `audiovisual-agent` |
| Operations | DOM-OPS | `project-management-agent` |

---

## Skill Discovery (MANIFEST.json)

Agents can auto-select the right skill by reading `MANIFEST.json`:

```python
import json

with open("MANIFEST.json") as f:
    manifest = json.load(f)

user_input = "deploy the app to staging"

for skill in manifest["skills"]:
    if any(trigger in user_input.lower() for trigger in skill["triggers"]):
        print(f"Selected skill: {skill['id']}")
        print(f"SKILL.md path: {skill['path']}")
        break
```

Each skill entry in the manifest includes:
- **triggers** — keywords for routing
- **input/output schemas** — what the agent expects and delivers
- **references** — which files to load per task

---

## Usage in Claude CLI (OPUS)

Skills are loaded by OPUS when a task matches the skill's trigger description. To reference a skill explicitly:

```bash
claude --skill ./dev-code-agent "Create a Python FastAPI endpoint with JWT auth"
claude --skill ./frontend-ui-agent "Build a SaaS landing page for LiveApp"
claude --skill ./devops-infra-agent "Deploy to staging VM with Docker"
claude --skill ./content-copywriting-agent "Write a blog post about agency automation"
claude --skill ./qa-testing-agent "Review this PR for security issues"
claude --skill ./audiovisual-agent "Write a script for a 60s explainer video"
claude --skill ./data-analysis-agent "Analyze monthly revenue trends from the DB"
claude --skill ./project-management-agent "Create a sprint plan for the website redesign"
```

---

## Creating a New Skill

```bash
# 1. Copy the template
cp -r _template/ my-new-agent/

# 2. Edit SKILL.md — fill in all sections
# 3. Create reference files in references/
# 4. Add the skill to MANIFEST.json
# 5. Update this README's Skill Index table
# 6. Commit with: git commit -m "feat: add my-new-agent skill"
```

---

## Maintenance Guidelines

- Each `SKILL.md` has a YAML frontmatter with `name`, `description`, `version`, and `maintainer`.
- Reference files live in `references/` and are loaded selectively — only what's needed per task.
- When updating a skill: bump the `version` field, add a `# Changelog` entry at the bottom of `SKILL.md`.
- After adding or modifying a skill, update `MANIFEST.json` to keep the registry in sync.
- Audit cycle: review after every 10 production uses or quarterly, whichever comes first.
- See `CHANGELOG.md` for repository-level version history.

---

## Authorship & License

© 2025–2026 Daniel Calisaya / Live Developer — Quito, Ecuador  
Internal use. Not for public redistribution without written authorization.  
See [LICENSE.md](LICENSE.md) for details.
