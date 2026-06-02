# Planning Reference — Live Developer Stack

## Project Brief Template

### Full Brief (For New Projects)

```markdown
# Project Brief: [Project Name]

## Overview
**Client:** [Name]
**Project lead:** [Name]
**Start date:** [Date]
**Target delivery:** [Date]
**Budget:** [Amount or range]

## Problem Statement
[What problem does this project solve? Why now? 2-3 sentences.]

## Goals
1. [Measurable goal 1] — metric: [how to measure]
2. [Measurable goal 2] — metric: [how to measure]
3. [Measurable goal 3] — metric: [how to measure]

## Scope

### In Scope
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

### Out of Scope
- [What we are NOT doing — be explicit]
- [Deferred to future phase]

## Deliverables

| # | Deliverable | Owner | Due | Dependencies |
|---|---|---|---|---|
| 1 | [Name] | [Person] | [Date] | None |
| 2 | [Name] | [Person] | [Date] | Deliverable 1 |
| 3 | [Name] | [Person] | [Date] | Deliverable 2 |

## Timeline

| Phase | Dates | Key Activities |
|---|---|---|
| Discovery | Week 1 | Stakeholder interviews, data collection |
| Design | Week 2-3 | Architecture, wireframes, tech decisions |
| Build | Week 4-6 | Development, integration |
| Test | Week 7 | QA, user testing, bug fixes |
| Launch | Week 8 | Deploy, monitor, handoff |

## Risks

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| [Risk 1] | High | Medium | [What we'll do] |
| [Risk 2] | Medium | Low | [What we'll do] |

## Success Criteria
- [ ] [Criterion 1 — measurable]
- [ ] [Criterion 2 — measurable]
- [ ] [Criterion 3 — measurable]

## Stakeholders

| Name | Role | Involvement |
|---|---|---|
| [Name] | Decision maker | Approves scope, budget, deliverables |
| [Name] | Technical lead | Architecture decisions, code review |
| [Name] | End user / client | Feedback, acceptance testing |

## Assumptions
- [Assumption 1]
- [Assumption 2]
```

---

## Sprint Planning

### Sprint Backlog Template

```markdown
# Sprint [Number] — [Start Date] to [End Date]

## Sprint Goal
[One sentence: what will be true at the end of this sprint?]

## Capacity
| Team Member | Available Days | Notes |
|---|---|---|
| [Name] | 9/10 | OOO Monday |
| [Name] | 10/10 | Full capacity |

## Tasks

| ID | Task | Owner | Estimate | Priority | Status |
|---|---|---|---|---|---|
| T-01 | [Task name] | [Name] | M | P1 | To Do |
| T-02 | [Task name] | [Name] | S | P1 | To Do |
| T-03 | [Task name] | [Name] | L | P2 | To Do |
| T-04 | [Task name] | [Name] | XS | P3 | To Do |

## Definition of Done
- [ ] Code written and reviewed
- [ ] Tests passing (unit + integration)
- [ ] Deployed to staging
- [ ] Stakeholder accepted (if client-facing)
- [ ] Documentation updated

## Risks / Blockers
- [Known risk or dependency]
```

### Task Breakdown Rules

- Every task must be completable in **1 day or less**. If not, break it down further.
- Tasks must be **independently deliverable** — no "part 1 of 3" unless clearly sequential.
- Each task has **one owner**. Shared ownership = no ownership.
- Priority P1 = must complete this sprint. P2 = should. P3 = if time allows.

---

## Roadmap Template

```markdown
# Product Roadmap — [Product Name] — [Year/Quarter]

## Vision
[One sentence: where are we going?]

## Now (This Sprint/Month)
| Initiative | Status | Owner | Notes |
|---|---|---|---|
| [Feature/project] | 🟢 On track | [Name] | [Key detail] |
| [Feature/project] | 🟡 At risk | [Name] | [Why] |

## Next (Next Sprint/Month)
| Initiative | Effort | Owner | Dependencies |
|---|---|---|---|
| [Feature/project] | M | [Name] | Requires [X] |

## Later (This Quarter)
| Initiative | Effort | Owner | Notes |
|---|---|---|---|
| [Feature/project] | L | TBD | Needs research |

## Icebox (Future Consideration)
- [Idea 1]
- [Idea 2]
```

### Roadmap Rules

- **Now** = committed. These are happening.
- **Next** = planned. High confidence, dependencies identified.
- **Later** = directional. May change based on learnings.
- **Icebox** = ideas worth remembering but not committed to.
- Review and update **every 2 weeks**.

---

## Risk Management

### Risk Register

```markdown
| ID | Risk | Category | Impact | Probability | Score | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | Key developer leaves mid-project | Team | High (4) | Low (1) | 4 | Cross-train, document | PM | Open |
| R-02 | API dependency changes | Technical | Medium (3) | Medium (2) | 6 | Abstract API layer | Tech Lead | Monitoring |
| R-03 | Client scope creep | Scope | High (4) | High (3) | 12 | Written scope, change request process | PM | Active |
```

### Risk Score = Impact × Probability

| Score | Level | Action |
|---|---|---|
| 1-3 | Low | Monitor, review monthly |
| 4-8 | Medium | Active mitigation plan, review weekly |
| 9-16 | High | Escalate, immediate action required |

---

## Estimation Techniques

### Planning Poker (Team Estimation)

```
1. Present the task
2. Each person privately assigns a size (XS, S, M, L, XL)
3. Reveal simultaneously
4. If estimates differ by > 1 size: discuss, then re-estimate
5. Converge on a final size
```

### Reference Tasks (Anchor-Based)

```
Define reference tasks that the team agrees on:
  XS = "Update a config value and deploy" (~1 hour)
  S  = "Add a new API endpoint with tests" (~half day)
  M  = "Build a new CRUD feature" (~1-2 days)
  L  = "Integrate a third-party service" (~3-5 days)
  XL = "Design and build a new module" (~1-2 weeks)

Then estimate new tasks relative to these anchors.
```

### Buffer Rules

| Confidence Level | Buffer |
|---|---|
| "I've done this exact thing before" | +20% |
| "I've done something similar" | +50% |
| "I've never done this" | +100% |
| "Nobody on the team has done this" | **Spike first**, then estimate |

A **spike** = 2-4 hours of focused research to reduce uncertainty before committing.
