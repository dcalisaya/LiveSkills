---
name: qa-testing-agent
description: >
  Quality assurance, testing, and code review skill for ensuring production-grade software
  quality. Use this skill whenever the user asks to write tests, review code, set up a
  testing strategy, audit code quality, create test plans, debug failing tests, improve
  test coverage, perform a security audit, or any task focused on validating that code
  works correctly, performs well, and meets quality standards. Trigger on: "test", "review",
  "QA", "quality", "coverage", "lint", "audit", "code review", "bug", "regression",
  "integration test", "unit test", "e2e", "performance test", "security audit", or any
  request to verify that something works as expected.
version: 1.0.0
maintainer: Daniel Calisaya / Live Developer
---

# QA & Testing Agent Skill

This skill guides OPUS through comprehensive quality assurance — from writing unit tests to
conducting code reviews to establishing testing strategies. The goal is zero surprises in
production: every bug caught in testing is a production incident prevented.

---

## Agent Thinking Process

Before writing a test or starting a review, execute this checklist:

1. **Classify the task** — Is this writing tests, reviewing code, debugging, auditing, or strategy?
2. **Identify the scope** — Unit, integration, end-to-end, or performance?
3. **Understand the contract** — What are the expected inputs, outputs, and side effects?
4. **Identify edge cases** — What happens with null, empty, boundary values, concurrent access?
5. **Check existing coverage** — What's already tested? Where are the gaps?
6. **Load the relevant reference** — Read the appropriate file in `references/` before acting.

---

## Task Types

| Task | Description | Reference |
|---|---|---|
| Write unit tests | Isolated function/class tests, mocking dependencies | `references/testing-strategies.md` |
| Write integration tests | Tests spanning multiple components/services | `references/testing-strategies.md` |
| Write E2E tests | Full-stack browser or API flow tests | `references/testing-strategies.md` |
| Code review | Evaluate code for quality, security, and correctness | `references/code-review.md` |
| Test strategy | Design a testing plan for a project or feature | `references/testing-strategies.md` |
| Debug failing tests | Diagnose and fix test failures | `references/testing-strategies.md` |
| Security audit | Check for vulnerabilities, injection, auth issues | `references/code-review.md` |
| Performance review | Identify bottlenecks, N+1 queries, memory leaks | `references/code-review.md` |

---

## Testing Pyramid

```
          ╱╲
         ╱  ╲          E2E Tests (few, slow, high confidence)
        ╱ E2E╲         Browser flows, API chains, deploy smoke tests
       ╱──────╲
      ╱        ╲       Integration Tests (moderate count)
     ╱Integration╲    API routes, DB queries, service interactions
    ╱──────────────╲
   ╱                ╲   Unit Tests (many, fast, focused)
  ╱   Unit Tests     ╲  Pure functions, business logic, transformations
 ╱────────────────────╲
```

| Level | Count | Speed | Mocking | When to Use |
|---|---|---|---|---|
| Unit | Many (70%+) | < 10ms each | Heavy | Pure logic, calculations, transformations |
| Integration | Moderate (20%) | < 1s each | Partial | API endpoints, DB operations, service calls |
| E2E | Few (10%) | 5-30s each | None | Critical user flows, smoke tests |

---

## Quality Standards (Non-Negotiable)

### For Tests

- **Test behavior, not implementation** — Tests should survive refactoring.
- **One assertion focus per test** — A test name should describe one scenario.
- **Arrange-Act-Assert** — Every test follows this structure clearly.
- **No test interdependence** — Tests must run in isolation and in any order.
- **Deterministic** — No flaky tests. No reliance on time, randomness, or network.
- **Readable test names** — `should_return_404_when_project_not_found` not `test3`.
- **Test the sad paths** — Error cases, edge cases, boundary values matter most.

### For Code Reviews

- **Security first** — Check for injection, auth bypass, data exposure.
- **Logic correctness** — Does it actually do what it claims?
- **Error handling** — Are all failure paths covered? No silent failures.
- **Performance** — N+1 queries, unbounded lists, missing pagination.
- **Readability** — Can someone else understand this in 6 months?
- **Consistency** — Does it follow the project's established patterns?

---

## Structured Output Format

### For Test Writing

```
## Test Plan
[What's being tested, what's the scope, what's the strategy]

## Tests
[Implementation — complete, runnable test files]

## Coverage Notes
[What's covered, what's NOT covered, and why]
```

### For Code Reviews

```
## Summary
[One paragraph: overall assessment — ship, fix then ship, or redesign]

## Critical Issues (Must Fix)
[Security vulnerabilities, logic errors, data loss risks]

## Improvements (Should Fix)
[Performance, readability, maintainability issues]

## Suggestions (Nice to Have)
[Style, naming, minor optimizations]

## What's Done Well
[Acknowledge good patterns — positive reinforcement matters]
```

---

## Severity Classification (Code Review)

| Severity | Label | Action | Examples |
|---|---|---|---|
| 🔴 Critical | `MUST FIX` | Block merge | SQL injection, auth bypass, data loss, crash |
| 🟡 Important | `SHOULD FIX` | Fix before or soon after merge | N+1 query, missing validation, poor error handling |
| 🔵 Suggestion | `CONSIDER` | Optional improvement | Naming, readability, minor refactor |
| ✅ Positive | `NICE` | Acknowledge | Clean pattern, good test, clear naming |

---

## Reference Files

Load the relevant reference before acting:

- `references/testing-strategies.md` — Testing patterns per language, mocking, fixtures, coverage
- `references/code-review.md` — Review checklist, security audit patterns, performance checks

---

# Changelog

## v1.0.0 — 2026-06
- Initial release. Foundation by Daniel Calisaya / Live Developer.
- Testing pyramid, quality standards, and review severity system established.
- Covers unit/integration/E2E testing and code review workflows.
