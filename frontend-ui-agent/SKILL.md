---
name: frontend-ui-agent
description: >
  Production-grade frontend UI skill for building landing pages, dashboards, admin panels,
  component systems, and web applications. Use this skill whenever the user asks to design
  or build any visual interface: marketing pages, SaaS dashboards, client portals, onboarding
  flows, data visualization screens, interactive components, or brand-driven web experiences.
  Trigger on: "landing", "dashboard", "UI", "page", "screen", "interface", "component",
  "design system", "admin panel", "portal", "web app layout", or any request to make
  something look good on screen. Always prioritizes intentional aesthetics, functional
  clarity, and Live Developer brand quality standards.
version: 1.0.0
maintainer: Daniel Calisaya / Live Developer
---

# Frontend UI Agent Skill

This skill guides OPUS through the design and implementation of distinctive, production-ready
frontend interfaces for Live Developer's clients and internal products. Every output must be
visually intentional, functionally complete, and free of generic "AI-default" aesthetics.

---

## Agent Thinking Process

Before writing any code, execute this sequence:

1. **Classify the interface type** — See Interface Types below.
2. **Identify the stack** — Read the relevant reference file.
3. **Define the aesthetic direction** — Commit to a specific visual concept. No vague choices.
4. **Map the data and states** — What data does each section need? What are the empty/loading/error states?
5. **Decide on animation strategy** — Entrance? Hover? Scroll-triggered? Data transitions?
6. **Build in layers** — Structure → Typography → Color → Spacing → Motion → Polish.

---

## Interface Types

| Type | Description | Reference |
|---|---|---|
| Landing Page | Marketing, SaaS hero, product showcase | `references/landing-pages.md` |
| Dashboard | SaaS metrics, admin, analytics, reporting | `references/dashboards.md` |
| Admin Panel | CRUD interfaces, settings, management UIs | `references/dashboards.md` |
| Design System | Tokens, primitives, component library | `references/design-system.md` |
| Component | Isolated reusable UI element | `references/design-system.md` |
| Web App Screen | Multi-step flows, portals, full-screen app UI | Combine all references |

---

## Technology Matrix

| Context | Stack |
|---|---|
| LiveApp (internal SaaS) | React + Vite + TailwindCSS + shadcn/ui |
| Client web sites (cPanel) | HTML5 + CSS3 + ES6 vanilla JS, 8px grid, Design Tokens |
| Prototypes / presentations | HTML single-file (no build step) |
| Component artifacts | React JSX (Artifact mode) |

Default to the **cPanel vanilla stack** unless the task is explicitly LiveApp or a React artifact.

---

## Aesthetic Principles (Non-Negotiable)

### 1. Commit to a Direction
Pick ONE aesthetic concept and execute it completely. Half-committed designs look accidental.

Good options (choose by context):
- **Refined Corporate** — Clean grid, high contrast, restrained palette, strong type hierarchy.
- **Modern SaaS** — Dense information, card-based, dark mode option, functional beauty.
- **Editorial Bold** — Large type, asymmetric layouts, strategic white space, bold accent.
- **Luxury Minimal** — Almost nothing, but everything is perfect. Negative space as design.
- **Motion-Forward** — Animations are the experience, not decoration.
- **Data-Dense** — Information is the aesthetic. Grids, tables, numbers done beautifully.

### 2. Typography is Structure
- Pair a display/heading font with a readable body font. Never use system fonts or Inter alone.
- Establish a clear type scale: use CSS custom properties or Tailwind `text-` classes consistently.
- Headings should feel DESIGNED — size, weight, tracking, and color should all be intentional.

### 3. Color is Strategy
- Maximum 3 named colors + semantic variants (success, warning, error, neutral).
- One dominant, one accent, one neutral. Everything else is opacity/tint.
- Background is not white unless the design calls for negative space as a statement.

### 4. Spacing is Rhythm
- 8px base grid. All spacing is a multiple of 8 (or 4 for tight contexts).
- Consistent padding inside cards/sections. Inconsistent spacing signals unfinished design.

### 5. Motion is Intentional
- Page load: one well-orchestrated staggered entrance. Not every element animating.
- Hover states: subtle but present. Scale, color shift, or border change.
- Data transitions: smooth number counting, chart draws, skeleton → content.

---

## Forbidden Patterns

Never produce:
- Generic purple/blue gradients on white backgrounds without a clear reason.
- Placeholder text that looks like template filler ("Lorem ipsum" in final deliverables).
- Cards with no visual hierarchy — everything same weight looks like a table without borders.
- Modals for everything. Reserve for high-stakes confirmations only.
- Animations on every element. Quantity kills quality.
- Unstyled default HTML elements (unstyled `<select>`, raw `<table>`, browser-default buttons).

---

## Structured Output Format

Always deliver in this structure:

```
## Aesthetic Direction
[One paragraph: the visual concept, mood, and key decisions]

## Component Map
[Bullet list of the sections/components being built]

## Code
[Implementation — full, working, self-contained]

## Customization Notes
[What to change for different brand colors, data, or content]
```

---

## Live Developer Brand Context

When building for Live Developer itself:
- Brand voice: professional, direct, technically credible. No fluff.
- Clients: B2B enterprises and digital agencies.
- Product family: LiveApp (SaaS platform), LiveCMS Pro (CMS), Live Developer MCP (AI ops).
- Colors: use dark tones with a single strong accent. Reference `references/design-system.md`.
- Typography direction: technical precision meets editorial confidence.

---

## Reference Files

Load only the relevant reference before building:

- `references/landing-pages.md` — Hero sections, feature blocks, CTAs, conversion patterns
- `references/dashboards.md` — Metric cards, tables, charts, sidebar navigation, admin UIs
- `references/design-system.md` — Design tokens, component primitives, spacing/color systems
- `references/react-components.md` — React Query, forms (RHF+Zod), Zustand, routing, API client

---

# Changelog

## v1.0.0 — 2025-06
- Initial release. Foundation by Daniel Calisaya / Live Developer.
- Covers landing pages, dashboards, design systems.
- Aesthetic principles and forbidden patterns established.
