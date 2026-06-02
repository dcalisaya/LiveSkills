# Agent Process Patterns — Live Developer

This reference defines the canonical agent process patterns used across Live Developer's
agentic infrastructure (mcp-foundation, LiveApp orchestration, DOM-DEV/DOM-AV pipelines).

---

## Pattern Catalog

### 1. Sequential Chain

**When to use:** Linear transformation where each step depends on the previous output.
Ideal for: data ETL, content generation pipelines, document processing chains.

```
Input → StepA → StepB → StepC → Output
```

**Python template:**

```python
from typing import TypeVar, Callable, Awaitable

T = TypeVar("T")

async def sequential_chain(input_data: T, steps: list[Callable]) -> T:
    result = input_data
    for step in steps:
        result = await step(result)
    return result

# Usage
output = await sequential_chain(
    raw_brief,
    [extract_requirements, generate_outline, write_draft, review_draft]
)
```

**TypeScript template:**

```typescript
async function sequentialChain<T>(
  input: T,
  steps: Array<(input: unknown) => Promise<unknown>>
): Promise<unknown> {
  let current: unknown = input
  for (const step of steps) {
    current = await step(current)
  }
  return current
}
```

---

### 2. Router / Classifier

**When to use:** Input must be dispatched to a specialist agent based on type/intent.
Ideal for: triage systems, multi-domain queries, task routing, support bots.

```
Input → Classifier → Route Decision → [AgentA | AgentB | AgentC] → Output
```

**Python template:**

```python
from enum import StrEnum
from dataclasses import dataclass

class TaskType(StrEnum):
    CODE_REVIEW = "code_review"
    CONTENT_WRITE = "content_write"
    DATA_ANALYSIS = "data_analysis"
    UNKNOWN = "unknown"

@dataclass
class RoutedTask:
    task_type: TaskType
    payload: dict

async def classify(input_text: str) -> RoutedTask:
    # Call LLM or rule-based classifier
    task_type = await llm_classify(input_text)
    return RoutedTask(task_type=task_type, payload={"text": input_text})

AGENT_MAP = {
    TaskType.CODE_REVIEW: code_review_agent,
    TaskType.CONTENT_WRITE: content_agent,
    TaskType.DATA_ANALYSIS: analysis_agent,
}

async def router_pipeline(input_text: str) -> dict:
    routed = await classify(input_text)
    agent_fn = AGENT_MAP.get(routed.task_type, fallback_agent)
    return await agent_fn(routed.payload)
```

---

### 3. Parallel Fan-Out + Merge

**When to use:** Multiple independent analyses needed before synthesis.
Ideal for: research pipelines, multi-perspective reviews, parallel content generation.

```
Input → [AgentA ‖ AgentB ‖ AgentC] → MergeAgent → Output
```

**Python template (asyncio.gather):**

```python
import asyncio
from dataclasses import dataclass

@dataclass
class FanOutResult:
    source: str
    data: dict
    error: str | None = None

async def safe_agent(name: str, fn, payload: dict) -> FanOutResult:
    try:
        result = await fn(payload)
        return FanOutResult(source=name, data=result)
    except Exception as e:
        return FanOutResult(source=name, data={}, error=str(e))

async def fan_out_pipeline(payload: dict) -> dict:
    results = await asyncio.gather(
        safe_agent("seo_agent", seo_analysis, payload),
        safe_agent("ux_agent", ux_review, payload),
        safe_agent("perf_agent", performance_check, payload),
    )
    successful = [r for r in results if r.error is None]
    return await merge_agent(successful)
```

**TypeScript template (Promise.allSettled):**

```typescript
const results = await Promise.allSettled([
  seoAgent(payload),
  uxAgent(payload),
  perfAgent(payload),
])

const fulfilled = results
  .filter((r): r is PromiseFulfilledResult<unknown> => r.status === 'fulfilled')
  .map(r => r.value)

const merged = await mergeAgent(fulfilled)
```

---

### 4. Human-in-the-Loop (HITL)

**When to use:** High-stakes or irreversible actions that require human approval.
Ideal for: publishing workflows, financial operations, deployments, client deliverables.

This is the canonical HITL implementation per ADR-012.

```
Input → Agent Proposes → Present to Human → [Approve | Reject] → Execute | Revise
```

**Python template (CLI HITL):**

```python
from enum import StrEnum

class HITLDecision(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
    REVISE = "revise"

async def hitl_gate(proposal: dict, context: str) -> HITLDecision:
    """Present proposal to human and collect decision."""
    print(f"\n{'='*60}")
    print(f"AGENT PROPOSAL — {context}")
    print(f"{'='*60}")
    print(proposal.get("summary", "No summary provided."))
    print(f"{'='*60}")
    choice = input("Decision [approve/reject/revise]: ").strip().lower()
    return HITLDecision(choice) if choice in HITLDecision._value2member_map_ else HITLDecision.REJECT

async def hitl_pipeline(input_data: dict) -> dict:
    proposal = await agent_propose(input_data)
    decision = await hitl_gate(proposal, context="Content Publication")
    
    match decision:
        case HITLDecision.APPROVE:
            return await agent_execute(proposal)
        case HITLDecision.REVISE:
            revised_input = {**input_data, "feedback": proposal.get("revision_notes", "")}
            return await hitl_pipeline(revised_input)  # recursive revision
        case HITLDecision.REJECT:
            return {"status": "rejected", "reason": "Human rejected proposal"}
```

**Web-based HITL (LiveApp context):**

For LiveApp, HITL gates are implemented as approval states in the Deliverable model:
- Status: `draft → pending_review → approved | revision_requested`
- Human interaction via the Client Contact Portal review UI.
- Agent resumes after status change via a queued job listener.

---

### 5. Audit Log Pattern

**When to use:** Any agent action with side effects (writes, sends, publishes).
Always combine with other patterns. Required for mcp-foundation operations.

```python
import sqlite3
import json
from datetime import datetime, UTC

def audit_log(
    db_path: str,
    agent_name: str,
    action: str,
    payload: dict,
    result: dict,
    status: str,
) -> None:
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("""
        INSERT INTO audit_log (agent, action, payload, result, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        agent_name,
        action,
        json.dumps(payload),
        json.dumps(result),
        status,
        datetime.now(UTC).isoformat(),
    ))
    con.commit()
    con.close()
```

---

## Pattern Selection Guide

| Scenario | Pattern |
|---|---|
| Multi-step data transformation | Sequential Chain |
| Multi-domain input dispatch | Router / Classifier |
| Independent parallel analyses | Fan-Out + Merge |
| Any write/publish/deploy action | HITL |
| All agent operations (default) | + Audit Log |
| Complex workflows | Compose multiple patterns |

---

## Domain Agent Registry (Live Developer)

Reference for available agents per domain:

| Domain | Agents |
|---|---|
| DOM-DEV | ArquitectoSoftware, ResearchScout, TechLeadFullStack, CodeAuditor, QAVerifier |
| DOM-AV | BriefParser, ScriptWriter, StoryboardAgent, ProductionCoordinator, QAReviewer |
| DOM-MKT | CampaignStrategist, CopyWriter, SEOAnalyst |
| DOM-HST | InfraArchitect, DeployAgent, MonitorAgent |

Full registry in `live-ops-core` knowledge base.
