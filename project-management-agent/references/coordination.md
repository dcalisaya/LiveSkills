# Coordination Reference — Live Developer Stack

## Status Reporting

### Daily Standup (Async)

Keep it to 3 questions, text-only, under 100 words:

```
## Standup — [Name] — [Date]

**Yesterday:** Completed [task]. Reviewed [PR/deliverable].
**Today:** Working on [task]. Meeting with [person] at [time].
**Blockers:** [None / Waiting on X from Y]
```

### Weekly Status Report

```markdown
# Weekly Status — [Project Name] — [Date]

## Health: 🟢 On Track / 🟡 At Risk / 🔴 Off Track

## Summary
[2-3 sentences: what happened, what's next, any concerns]

## Completed This Week
- ✅ [Task 1]
- ✅ [Task 2]

## In Progress
- 🔄 [Task 3] — [% complete, ETA]
- 🔄 [Task 4] — [% complete, ETA]

## Blocked
- 🚫 [Task 5] — blocked by [what], need [action] from [who]

## Next Week
1. [Priority 1]
2. [Priority 2]

## Risks
- [New risk or update on existing risk]

## Decisions Needed
- [Decision 1] — needed by [date]
```

---

## Client Communication Templates

### Project Kickoff Email

```
Subject: [Project Name] — Kickoff Summary & Next Steps

Hi [Client Name],

Thank you for the kickoff meeting today. Here's a summary of what we aligned on:

**Project:** [Name]
**Timeline:** [Start] → [End]
**Key deliverables:** [List 3-5]
**Your main contact:** [Name, email]

**Next steps:**
1. We'll send the detailed project brief by [date]
2. Design phase starts [date]
3. Your first review checkpoint is [date]

If anything looks off, just reply to this email.

Best,
[Name]
Live Developer
```

### Deliverable Review Request

```
Subject: [Project Name] — [Deliverable] Ready for Review

Hi [Client Name],

[Deliverable name] is ready for your review:

🔗 [Link to deliverable / portal]

**What to review:**
- [Specific thing 1]
- [Specific thing 2]

**Deadline for feedback:** [Date]

If we don't receive feedback by [date], we'll proceed with the current version
for the next phase.

Please note: for this round, we're focusing on [content/layout/functionality].
Visual polish comes in the next iteration.

Best,
[Name]
```

### Scope Change Request

```
Subject: [Project Name] — Scope Change Request #[Number]

Hi [Client Name],

You've requested [describe the change]. Here's the impact:

**Change:** [What's being added/modified]

**Impact:**
- Timeline: +[X days/weeks]
- Budget: +$[amount] or [included in current scope]
- Affected deliverables: [list]

**Options:**
A. Add this and extend the timeline by [X]
B. Add this and remove [lower-priority item] to stay on schedule
C. Defer to Phase 2

Please confirm your preferred option by [date] so we can adjust the plan.

Best,
[Name]
```

---

## Meeting Templates

### Kickoff Meeting Agenda

```
## Kickoff — [Project Name] — [Duration: 60 min]

1. Introductions (5 min)
2. Project overview & goals (10 min)
3. Scope walkthrough (15 min)
4. Timeline & milestones (10 min)
5. Roles & communication plan (10 min)
6. Q&A (10 min)

### Pre-read (send 24h before):
- Project brief
- Timeline draft

### Outputs:
- Confirmed scope
- Agreed timeline
- Communication cadence established
```

### Sprint Retrospective

```
## Retrospective — Sprint [Number] — [Date]

### What went well ✅
- [Item]
- [Item]

### What didn't go well ❌
- [Item]
- [Item]

### Action items for next sprint 🎯
| Action | Owner | Due |
|---|---|---|
| [Action] | [Name] | [Date] |
| [Action] | [Name] | [Date] |

### Team mood: [1-5 scale or emoji]
```

---

## Agent Orchestration

### Multi-Agent Workflow Template

When coordinating work across multiple agent skills:

```markdown
## Workflow: [Name]

### Objective
[What's the end-to-end goal?]

### Pipeline

| Step | Agent | Input | Output | Dependencies |
|---|---|---|---|---|
| 1 | `project-management-agent` | Client brief | Project plan | None |
| 2 | `content-copywriting-agent` | Project plan | Landing page copy | Step 1 |
| 3 | `frontend-ui-agent` | Copy + design direction | Landing page code | Step 2 |
| 4 | `qa-testing-agent` | Landing page code | Test report | Step 3 |
| 5 | `devops-infra-agent` | Code + test report | Deployed site | Step 4 |

### Quality Gates (HITL)
- After Step 2: Client reviews copy before design starts
- After Step 4: Client reviews staging site before launch

### Fallback
If any step fails, escalate to [person/process].
```

### Handoff Format Between Agents

```
## Agent Handoff: [From Agent] → [To Agent]

**Context:** [What was done before this step]
**Objective:** [What this agent needs to accomplish]
**Input:**
  - [File, data, or artifact from previous step]
  - [Constraints or requirements]
**Expected output:**
  - [Deliverable format]
  - [Quality criteria]
**Deadline:** [When]
**Escalation:** [Who to contact if blocked]
```

---

## RACI Matrix Template

For complex projects with multiple stakeholders:

```
| Activity | Daniel | Client | Tech Lead | Designer |
|---|---|---|---|---|
| Define scope | A | C | R | I |
| Approve design | C | A | I | R |
| Write code | I | I | A/R | I |
| Review deliverable | R | A | C | I |
| Deploy to production | I | I | A/R | I |

R = Responsible (does the work)
A = Accountable (makes the decision)
C = Consulted (gives input)
I = Informed (needs to know)
```

### Rules
- Every row has exactly **one A** (Accountable).
- **R without A** = nobody can make decisions.
- **Everyone is R** = nobody owns it.
- Keep it simple — if more than 5 columns, the project is too complex for one RACI.

---

## Communication Cadence

| Stakeholder | Channel | Frequency | Content |
|---|---|---|---|
| Internal team | Slack/async | Daily | Standup, quick questions |
| Client (active project) | Email | Weekly | Status report |
| Client (review cycle) | Portal + email | Per deliverable | Review request |
| Leadership | Email/meeting | Biweekly/monthly | Portfolio status |
| All stakeholders | Meeting | Per milestone | Demo, review, decision |
