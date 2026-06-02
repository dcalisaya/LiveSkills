# Changelog

All notable changes to the LiveSkills repository are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).  
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-06-02

### Full audit and expansion of the LiveSkills agent skill directory.

### Added

**Phase 1 — Repository Hygiene**
- `.gitignore` — macOS, env, dependencies, builds, IDE files
- `LICENSE.md` — proprietary license (internal use only)
- Fixed README repo name from `live-developer-skills/` to `LiveSkills/`
- Normalized CSS design tokens across `landing-pages.md` and `dashboards.md` to match `design-system.md` canonical naming (`--color-*` → `--bg-*`, `--text-*`, `--border-*`, `--accent`)
- Removed `.DS_Store` files from repository

**Phase 2 — Missing References for Existing Skills**
- `dev-code-agent/references/bash-shell.md` — strict headers, logging, deploy scripts, argument parsing, security
- `dev-code-agent/references/sql-postgresql.md` — schema conventions, query patterns, migrations, indexing, performance
- `frontend-ui-agent/references/react-components.md` — React Query, React Hook Form + Zod, Zustand, routing, API client

**Phase 3 — New Critical Skills**
- `devops-infra-agent/` — servers, VMs, CI/CD, Docker, Nginx, monitoring
  - `references/proxmox-vms.md` — VM creation, templates, hardening, networking, backups
  - `references/ci-cd.md` — GitHub Actions, Docker deploy, Nginx, SSL, DNS, rollbacks
  - `references/monitoring.md` — health endpoints, Uptime Kuma, log management, incident response
- `content-copywriting-agent/` — SEO, copywriting, email campaigns
  - `references/seo.md` — keyword research, on-page SEO, content templates, technical SEO, schema markup
  - `references/copywriting.md` — headline formulas, persuasion frameworks (PAS/AIDA/BAB), CTA writing, microcopy
  - `references/email-campaigns.md` — sequences, subject lines, segmentation, deliverability (SPF/DKIM/DMARC)
- `qa-testing-agent/` — testing, code review, security audits
  - `references/testing-strategies.md` — patterns per language (pytest, Vitest, Pest), mocking, coverage strategy
  - `references/code-review.md` — review checklist, comment format, severity system, PR size guidelines

**Phase 4 — Discovery Infrastructure**
- `MANIFEST.json` — machine-readable skill registry with triggers, I/O schemas, routing logic
- `_template/` — scaffold for creating new skills (SKILL.md + reference templates)
- Updated `dev-code-agent/SKILL.md` — added bash-shell.md and sql-postgresql.md to reference section
- Updated `frontend-ui-agent/SKILL.md` — added react-components.md to reference section
- Complete README rewrite with expanded tree, skill index, domain map, and discovery docs

**Phase 5 — Secondary Skills**
- `audiovisual-agent/` — video production pipeline (DOM-AV)
  - `references/pre-production.md` — brief parsing, script writing (two-column format), storyboards, shot lists, creative direction
  - `references/post-production.md` — editing workflow, color grading, audio mix (LUFS), motion graphics, export specs per platform
- `data-analysis-agent/` — data analysis and reporting (DOM-DEV)
  - `references/analysis-patterns.md` — EDA workflow, time series, cohort analysis, funnels, RFM, A/B testing, ETL
  - `references/reporting.md` — report templates, Chart.js/matplotlib code, dashboard design, Excel output
- `project-management-agent/` — planning and coordination (DOM-OPS)
  - `references/planning.md` — project briefs, sprint planning, roadmaps, risk management, estimation
  - `references/coordination.md` — status reports, client comms, agent orchestration, RACI matrix
- `CHANGELOG.md` — this file

### Repository Stats (v1.0.0)

| Metric | Value |
|---|---|
| Total skills | 8 |
| Total reference files | 24 |
| Total files (md + json) | 38 |
| Domains covered | 5 (DOM-DEV, DOM-HST, DOM-MKT, DOM-AV, DOM-OPS) |
| Template included | Yes |
| Machine-readable manifest | Yes |

---

## [0.0.0] — 2025-06

### Added
- Initial creation by Daniel Calisaya / Live Developer.
- `dev-code-agent/` with 4 references (python, php-laravel, typescript-node, agent-process-patterns).
- `frontend-ui-agent/` with 3 references (landing-pages, dashboards, design-system).
- `README.md` with basic structure and skill index.
