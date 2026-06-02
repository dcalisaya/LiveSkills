---
name: project-management-agent
description: >
  Project management and orchestration skill for planning, tracking, and coordinating
  work across teams and agent pipelines. Use this skill whenever the user asks to plan
  a project, create a timeline, write a brief, define deliverables, estimate effort,
  coordinate between teams or agents, manage a sprint, create a roadmap, track progress,
  or any task focused on organizing and executing work systematically. Trigger on: "plan",
  "project", "timeline", "brief", "deliverable", "sprint", "roadmap", "milestone",
  "estimate", "scope", "schedule", "coordinate", "stakeholder", "status update",
  "kickoff", "retrospective", or any request about organizing work.
version: 1.0.0
maintainer: Daniel Calisaya / Live Developer
---

# Project Management Agent Skill

This skill guides OPUS through project planning, coordination, and execution — from
initial brief to final delivery. It serves as the orchestration layer that connects
other agent skills into coherent workflows. Every output must be actionable, time-bound,
and aligned with stakeholder expectations.

---

## Agent Thinking Process

Before planning or coordinating, execute this checklist:

1. **Classify the task** — Planning, tracking, reporting, or coordination?
2. **Identify stakeholders** — Who needs to know? Who decides? Who executes?
3. **Define scope** — What's included? What's explicitly OUT of scope?
4. **Assess constraints** — Budget, timeline, available resources, dependencies.
5. **Choose the framework** — Agile sprint, waterfall phase, or hybrid?
6. **Load the relevant reference** — Read the appropriate file in `references/`.

---

## Task Types

| Task | Description | Reference |
|---|---|---|
| Project brief | Define scope, goals, deliverables, timeline | `references/planning.md` |
| Sprint planning | Break work into tasks, assign, estimate | `references/planning.md` |
| Roadmap creation | Multi-month/quarter planning | `references/planning.md` |
| Status report | Progress update for stakeholders | `references/coordination.md` |
| Risk assessment | Identify and mitigate project risks | `references/planning.md` |
| Agent orchestration | Coordinate multi-agent workflows | `references/coordination.md` |
| Client communication | Updates, approvals, feedback cycles | `references/coordination.md` |
| Retrospective | Review what worked, what didn't, action items | `references/coordination.md` |

---

## Project Frameworks

### Agile/Sprint (Default for Live Developer)

```
Sprint = 2 weeks

Monday W1:    Sprint Planning → define tasks, estimate, assign
Daily:        Standup (async) → blockers, progress, plan
Friday W1:    Mid-sprint check → are we on track?
Thursday W2:  Feature freeze → testing and polish only
Friday W2:    Sprint Review → demo to stakeholders
Friday W2:    Retrospective → what to improve
```

### Milestone-Based (Client Projects)

```
Phase 1: Discovery & Brief      → 1 week
Phase 2: Design & Architecture   → 1-2 weeks
Phase 3: Development             → 2-4 weeks
Phase 4: Testing & QA            → 1 week
Phase 5: Launch & Handoff        → 3 days
```

### Kanban (Ongoing Operations)

```
Columns: Backlog → To Do → In Progress → Review → Done
WIP Limit: 3 items per person in "In Progress"
Cadence: Weekly prioritization, continuous delivery
```

---

## Input Schema

| Field | Required | Type | Description |
|---|---|---|---|
| `task_description` | ✅ | string | What needs to be planned or coordinated |
| `project_name` | ❌ | string | Name of the project |
| `deadline` | ❌ | date | Hard deadline, if any |
| `team` | ❌ | list | People or agents involved |
| `constraints` | ❌ | string | Budget, tech, or scope constraints |
| `framework` | ❌ | string | agile, waterfall, kanban |

---

## Structured Output Format

### For Project Briefs

```
## Project Brief: [Name]

### Overview
[What is this project and why are we doing it?]

### Goals
[2-4 measurable objectives]

### Scope
**In scope:** [explicit list]
**Out of scope:** [explicit list]

### Deliverables
[Numbered list with owner and deadline]

### Timeline
[Phase breakdown with dates]

### Risks
[Top 3 risks with mitigation plans]

### Success Criteria
[How do we know this project succeeded?]
```

### For Status Reports

```
## Status Report: [Project Name] — [Date]

### Summary
[One paragraph: overall health, key accomplishment, key blocker]

### Progress
| Deliverable | Status | Owner | Due | Notes |
|---|---|---|---|---|

### Blockers
[What's stuck and what's needed to unblock]

### Next Week
[Top 3 priorities]

### Risks
[New or escalated risks]
```

---

## Agent Orchestration Patterns

This skill coordinates work across other agent skills:

| Workflow | Agents Involved | Pattern |
|---|---|---|
| Website build | `frontend-ui-agent` → `dev-code-agent` → `qa-testing-agent` → `devops-infra-agent` | Sequential Chain |
| Content campaign | `content-copywriting-agent` (SEO + email) ‖ `frontend-ui-agent` (landing) | Fan-Out + Merge |
| Full product launch | All agents, phased | Milestone + HITL gates |
| Client deliverable | `dev-code-agent` → `qa-testing-agent` → HITL (client review) | Sequential + HITL |

### Delegation Format

When delegating to another agent, structure the handoff as:

```
## Task Delegation: [Agent Name]

**Objective:** [One sentence]
**Skill to use:** [skill-name]
**Input:** [Structured data for the agent]
**Constraints:** [Time, quality, scope limits]
**Expected output:** [What to deliver back]
**Deadline:** [When]
```

---

## Estimation Framework

### T-Shirt Sizing

| Size | Effort | Calendar Time | Complexity |
|---|---|---|---|
| XS | < 2 hours | Same day | Trivial change |
| S | 2-4 hours | 1 day | Simple, well-understood |
| M | 1-2 days | 2-3 days | Some unknowns, moderate scope |
| L | 3-5 days | 1 week | Significant scope, multiple components |
| XL | 1-2 weeks | 2 weeks | Complex, cross-functional, unknowns |
| XXL | 2+ weeks | **Split it** | Too large for one task |

### Estimation Rules

- Always multiply your first estimate by **1.5** (optimism bias correction).
- If you can't estimate, spend 1 hour on research, then re-estimate.
- XXL tasks must be broken into L or smaller before starting.
- Include buffer for testing, review, and deployment — not just coding.

---

## Quality Standards

- **Every project has a brief** — No work starts without a written scope.
- **Every task has an owner** — No orphan tasks. One person accountable.
- **Every deliverable has a deadline** — Open-ended = never finished.
- **Every blocker has an escalation** — Don't let things sit. Escalate within 24h.
- **Every project ends with a retro** — Learn something every time.
- **Status is visible** — Stakeholders should never have to ask "where are we?"

---

## Reference Files

Load the relevant reference before acting:

- `references/planning.md` — Briefs, roadmaps, estimation, risk management, sprint planning
- `references/coordination.md` — Status reports, stakeholder comms, agent orchestration, retros

---

# Changelog

## v1.0.0 — 2026-06
- Initial release. Foundation by Daniel Calisaya / Live Developer.
- Covers project briefs, sprint planning, status reports, agent orchestration.
- Estimation framework and delegation format established.
