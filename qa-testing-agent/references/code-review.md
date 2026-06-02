# Code Review Reference — Live Developer Stack

## Review Philosophy

A code review is not a gatekeeping ritual. It is:

- **A quality conversation** between professionals.
- **A knowledge transfer mechanism** — reviewer learns the code, author learns the patterns.
- **A safety net** — catch bugs, security issues, and design problems before users do.

### Reviewer Mindset

1. **Assume positive intent.** The author did their best with the information they had.
2. **Ask, don't tell.** "What happens if this is null?" > "This will crash on null."
3. **Praise what's good.** Reinforcement works better than correction alone.
4. **Focus on the important stuff.** Don't bikeshed naming when there's a security hole.
5. **Approve with suggestions.** Don't block on style preferences.

---

## Review Checklist

### 🔴 Security (Always Check First)

```
□ No hardcoded secrets, tokens, or credentials
□ All user input is validated and sanitized
□ SQL queries use parameterized statements (no string interpolation)
□ Authentication/authorization checks on every endpoint
□ Sensitive data not logged or exposed in errors
□ File uploads validated (type, size, content)
□ CORS configured properly (not wildcard in production)
□ Rate limiting on public endpoints
□ No eval(), exec(), or dynamic code execution with user input
□ Dependencies checked for known vulnerabilities
```

### 🟡 Logic & Correctness

```
□ Does the code actually do what the PR description says?
□ Are all edge cases handled? (null, empty, boundary values)
□ Error handling is complete — no silent failures
□ Off-by-one errors checked (loops, pagination, array indexing)
□ Race conditions considered (concurrent access, shared state)
□ Transaction boundaries correct (database operations)
□ Idempotency — can this be safely retried?
□ Backwards compatibility maintained (API contracts, DB schema)
```

### 🔵 Performance

```
□ No N+1 queries (eager load or batch where needed)
□ Database queries have appropriate indexes
□ Lists are paginated (no unbounded SELECT *)
□ Heavy operations are async or queued
□ Caching used where appropriate (but not prematurely)
□ Memory usage is bounded (no accumulating arrays in loops)
□ File I/O uses streaming for large files
□ API responses are reasonably sized
```

### ⚪ Code Quality

```
□ Single Responsibility — each function/class does one thing
□ Naming is clear and descriptive (no x, tmp, data, result)
□ No dead code (unused imports, commented-out blocks, unreachable paths)
□ No duplicated logic (DRY where it makes sense)
□ Functions are small (< 30 lines is a good target)
□ Nesting depth is shallow (< 3 levels)
□ Type annotations are present and correct
□ Comments explain WHY, not WHAT
□ Follows project conventions and patterns
□ Tests are included (or existing tests updated)
```

---

## Review Comment Format

### Structure

```
[SEVERITY] [CATEGORY] — [Message]

[Explanation or question, if needed]
[Suggested fix, if helpful]
```

### Examples

```
🔴 MUST FIX [Security] — User input passed directly to SQL query.
Use parameterized queries: `WHERE id = $1` instead of string interpolation.

🟡 SHOULD FIX [Performance] — This fetches all deliverables then filters in memory.
Move the filter to the SQL query to avoid loading unused data.
Consider: `WHERE status = 'active' AND project_id = $1`

🔵 CONSIDER [Readability] — This function is 80+ lines with 4 levels of nesting.
Consider extracting the validation logic into a separate function.

✅ NICE — Clean use of the Repository pattern here.
The separation between business logic and data access is exactly right.

❓ QUESTION — What happens if `dueAt` is null here?
I see it's accessed without a null check on line 45.
```

---

## Review by Change Type

### New Feature

Focus on:
- Does it match the spec/requirements?
- Is the architecture appropriate?
- Are tests comprehensive?
- Will it scale?

### Bug Fix

Focus on:
- Does the fix actually address the root cause (not just symptoms)?
- Is there a regression test that would have caught this?
- Are there similar bugs elsewhere in the codebase?

### Refactor

Focus on:
- Does behavior remain identical? (tests should prove this)
- Is the new structure actually better?
- Is this the right scope? (too large = risky, too small = why bother)

### Dependency Update

Focus on:
- Are there breaking changes in the changelog?
- Do all tests still pass?
- Is the new version stable (not a .0 release)?
- Are there security advisories for the old version?

---

## Security Audit Patterns

### Input Validation Audit

```python
# CHECK: Is every external input validated?

# ❌ Bad — raw user input used directly
@app.post("/search")
async def search(request: Request):
    body = await request.json()
    query = body["query"]  # No validation
    results = await db.execute(f"SELECT * FROM items WHERE name = '{query}'")  # SQL injection

# ✅ Good — validated with Pydantic, parameterized query
class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=100)

@app.post("/search")
async def search(body: SearchRequest):
    results = await db.execute(
        select(Item).where(Item.name == body.query)
    )
```

### Authentication Audit

```
For every endpoint, verify:
1. Is authentication required? (middleware/decorator present)
2. Is authorization checked? (user can access THIS resource)
3. Are tokens validated properly? (expiry, signature, scope)
4. Is session management secure? (httpOnly, secure, sameSite cookies)
```

### Data Exposure Audit

```
For every API response, verify:
1. Only necessary fields are returned (no password hashes, internal IDs)
2. Error messages don't expose internals (stack traces, SQL, file paths)
3. Pagination prevents full data dump
4. Sensitive data is masked in logs
```

---

## Performance Review Patterns

### N+1 Query Detection

```python
# ❌ N+1 — one query per deliverable
projects = await db.execute(select(Project))
for project in projects:
    deliverables = await db.execute(
        select(Deliverable).where(Deliverable.project_id == project.id)
    )

# ✅ Eager load — one query with join
projects = await db.execute(
    select(Project).options(selectinload(Project.deliverables))
)
```

### Unbounded Query Detection

```python
# ❌ Bad — fetches ALL rows
results = await db.execute(select(Deliverable))

# ✅ Good — paginated
results = await db.execute(
    select(Deliverable)
    .order_by(Deliverable.created_at.desc())
    .limit(50)
    .offset(0)
)
```

### Memory Leak Detection

```typescript
// ❌ Bad — accumulates in memory forever
const cache: Map<string, unknown> = new Map()
app.get('/data/:id', async (req, reply) => {
  const data = await fetchData(req.params.id)
  cache.set(req.params.id, data)  // Never evicted
  return data
})

// ✅ Good — LRU cache with max size
import { LRUCache } from 'lru-cache'
const cache = new LRUCache({ max: 1000, ttl: 1000 * 60 * 5 })
```

---

## PR Size Guidelines

| Size | Lines Changed | Review Time | Risk |
|---|---|---|---|
| Small | < 100 | 15 min | Low |
| Medium | 100-400 | 30-60 min | Medium |
| Large | 400-1000 | 1-2 hours | High |
| Too Large | 1000+ | **Split it** | Very High |

### Rules

- **PRs over 400 lines should be split** unless they're generated code or migrations.
- **One concern per PR.** Don't mix feature + refactor + dependency update.
- **Self-review before requesting.** Re-read your own diff. You'll catch 30% of issues yourself.

---

## Review Turnaround

| Priority | Target Response Time |
|---|---|
| Hotfix / P1 | < 1 hour |
| Feature PR | < 4 hours (same day) |
| Refactor | < 1 business day |
| Documentation | < 2 business days |

If you can't review in time, say so. "I can't review this until tomorrow, if someone else can take it, please do."
