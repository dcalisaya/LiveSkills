---
name: <skill-name>
description: >
  <One paragraph describing what this skill does, when to use it, and what triggers it.
  Be specific about trigger words and task types. This description is used for agent routing.>
version: 0.1.0
maintainer: Daniel Calisaya / Live Developer
---

# <Skill Display Name>

<One paragraph describing this skill's purpose and what it guides the agent to do.>

---

## Agent Thinking Process

Before acting, execute this checklist:

1. **Classify the task** — <What categories exist?>
2. **Identify the context** — <What variables matter?>
3. **Define the contract** — <What are inputs, outputs, side effects?>
4. **Check preconditions** — <What must be true before starting?>
5. **Load the relevant reference** — Read the appropriate file in `references/`.

---

## Task Types

| Type | Description | Reference |
|---|---|---|
| <task_type_1> | <description> | `references/<reference>.md` |
| <task_type_2> | <description> | `references/<reference>.md` |

---

## Input Schema

| Field | Required | Type | Description |
|---|---|---|---|
| `task_description` | ✅ | string | What the user wants to accomplish |
| `<field_2>` | ❌ | string | <description> |

---

## Output Schema

The agent must deliver structured output in this format:

```
## <Section 1>
[<description>]

## <Section 2>
[<description>]

## <Section 3>
[<description>]
```

---

## Quality Standards (Non-Negotiable)

- <standard_1>
- <standard_2>
- <standard_3>

---

## Reference Files

Load the relevant reference before acting:

- `references/<topic>.md` — <description>

---

# Changelog

## v0.1.0 — YYYY-MM
- Initial scaffold. Fill in before first use.
