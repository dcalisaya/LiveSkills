# SQL / PostgreSQL Reference — Live Developer Stack

## Runtime & Environment

- PostgreSQL **16+** on Ubuntu 24.04 VMs (Proxmox) or managed instances.
- Always use parameterized queries. Never interpolate user input into SQL.
- Naming: `snake_case` for tables, columns, and functions. Tables are plural.
- Index names: `idx_<table>_<column>` (e.g., `idx_projects_client_id`).
- Constraint names: `<table>_<column>_<type>` (e.g., `deliverables_project_id_fkey`).

---

## Schema Conventions

### Table Creation (Standard Template)

```sql
CREATE TABLE deliverables (
    id              BIGSERIAL PRIMARY KEY,
    project_id      BIGINT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    status          VARCHAR(32) NOT NULL DEFAULT 'draft'
                    CHECK (status IN ('draft', 'pending_review', 'revision_requested', 'approved', 'live', 'archived')),
    priority        SMALLINT NOT NULL DEFAULT 0,
    metadata        JSONB DEFAULT '{}',
    due_at          TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

-- Indexes
CREATE INDEX idx_deliverables_project_id ON deliverables(project_id);
CREATE INDEX idx_deliverables_status     ON deliverables(status);
CREATE INDEX idx_deliverables_due_at     ON deliverables(due_at) WHERE deleted_at IS NULL;

-- GIN index for JSONB queries
CREATE INDEX idx_deliverables_metadata   ON deliverables USING GIN(metadata);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_deliverables_updated_at
    BEFORE UPDATE ON deliverables
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

COMMENT ON TABLE deliverables IS 'Client deliverables linked to projects. Central entity for the review cycle.';
```

### Data Types — Decision Guide

| Use Case | Type | Reason |
|---|---|---|
| Primary keys | `BIGSERIAL` | Avoids 32-bit overflow on high-volume tables |
| UUIDs (public-facing IDs) | `UUID` with `gen_random_uuid()` | Non-sequential, safe for URLs |
| Short strings (names, slugs) | `VARCHAR(n)` | Enforces max length at DB level |
| Long text (descriptions, content) | `TEXT` | No performance difference vs VARCHAR in PG |
| Dates with timezone | `TIMESTAMPTZ` | Always — never use `TIMESTAMP` without TZ |
| Money / financial | `NUMERIC(12,2)` | Exact precision, no floating-point errors |
| Status / enum-like | `VARCHAR(32) + CHECK` | More flexible than `ENUM` type for migrations |
| Structured metadata | `JSONB` | Indexable, queryable, schema-flexible |
| Booleans | `BOOLEAN` with `DEFAULT` | Always set a default, never leave nullable |
| Counters | `INTEGER DEFAULT 0` | Use `UPDATE ... SET count = count + 1` for atomicity |

---

## Query Patterns

### Filtered List with Pagination

```sql
SELECT
    d.id,
    d.title,
    d.status,
    d.due_at,
    p.name AS project_name,
    c.name AS client_name
FROM deliverables d
JOIN projects p ON p.id = d.project_id
JOIN clients c  ON c.id = p.client_id
WHERE d.deleted_at IS NULL
  AND d.status = :status
  AND d.due_at >= :from_date
ORDER BY d.due_at ASC, d.created_at DESC
LIMIT :limit
OFFSET :offset;
```

### Aggregate Stats (Dashboard)

```sql
SELECT
    d.status,
    COUNT(*)                    AS total,
    COUNT(*) FILTER (WHERE d.due_at < NOW())  AS overdue,
    AVG(EXTRACT(EPOCH FROM (d.updated_at - d.created_at))) / 3600 AS avg_hours_to_complete
FROM deliverables d
WHERE d.deleted_at IS NULL
  AND d.created_at >= DATE_TRUNC('month', NOW())
GROUP BY d.status
ORDER BY total DESC;
```

### Upsert (INSERT ... ON CONFLICT)

```sql
INSERT INTO settings (user_id, key, value, updated_at)
VALUES (:user_id, :key, :value, NOW())
ON CONFLICT (user_id, key)
DO UPDATE SET
    value = EXCLUDED.value,
    updated_at = NOW();
```

### CTE (Common Table Expression) — Multi-Step Query

```sql
WITH active_projects AS (
    SELECT id, name, client_id
    FROM projects
    WHERE status = 'active'
      AND deleted_at IS NULL
),
deliverable_counts AS (
    SELECT
        project_id,
        COUNT(*) AS total,
        COUNT(*) FILTER (WHERE status = 'approved') AS approved
    FROM deliverables
    WHERE deleted_at IS NULL
    GROUP BY project_id
)
SELECT
    ap.name AS project_name,
    c.name  AS client_name,
    COALESCE(dc.total, 0) AS total_deliverables,
    COALESCE(dc.approved, 0) AS approved_deliverables,
    ROUND(
        COALESCE(dc.approved, 0)::NUMERIC / NULLIF(dc.total, 0) * 100, 1
    ) AS completion_pct
FROM active_projects ap
JOIN clients c ON c.id = ap.client_id
LEFT JOIN deliverable_counts dc ON dc.project_id = ap.id
ORDER BY completion_pct DESC NULLS LAST;
```

### JSONB Queries

```sql
-- Query nested JSONB field
SELECT * FROM deliverables
WHERE metadata->>'category' = 'branding';

-- Query array inside JSONB
SELECT * FROM deliverables
WHERE metadata->'tags' ? 'urgent';

-- Update JSONB field (merge)
UPDATE deliverables
SET metadata = metadata || '{"reviewed_by": "daniel"}'::JSONB
WHERE id = :id;

-- Remove key from JSONB
UPDATE deliverables
SET metadata = metadata - 'temporary_flag'
WHERE id = :id;
```

---

## Migration Conventions

### File Naming

```
migrations/
├── 001_create_clients.sql
├── 002_create_projects.sql
├── 003_create_deliverables.sql
├── 004_add_priority_to_deliverables.sql
└── 005_create_audit_log.sql
```

### Migration Template

```sql
-- Migration: 004_add_priority_to_deliverables.sql
-- Author: Daniel Calisaya / Live Developer
-- Date: 2026-06-02
-- Description: Add priority column for deliverable ordering

BEGIN;

ALTER TABLE deliverables
    ADD COLUMN priority SMALLINT NOT NULL DEFAULT 0;

CREATE INDEX idx_deliverables_priority
    ON deliverables(priority DESC)
    WHERE deleted_at IS NULL;

COMMENT ON COLUMN deliverables.priority IS 'Sort priority: higher = more important. Default 0.';

COMMIT;
```

### Rollback Pattern

```sql
-- Rollback: 004_add_priority_to_deliverables.sql
BEGIN;
DROP INDEX IF EXISTS idx_deliverables_priority;
ALTER TABLE deliverables DROP COLUMN IF EXISTS priority;
COMMIT;
```

---

## Performance Patterns

### Index Strategy

```sql
-- Partial index (only active rows)
CREATE INDEX idx_deliverables_active
    ON deliverables(status, due_at)
    WHERE deleted_at IS NULL;

-- Covering index (avoids table lookup)
CREATE INDEX idx_projects_client_lookup
    ON projects(client_id)
    INCLUDE (name, status);

-- Expression index
CREATE INDEX idx_clients_email_lower
    ON clients(LOWER(email));
```

### EXPLAIN ANALYZE (Always Check Before Deploying)

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT d.*, p.name
FROM deliverables d
JOIN projects p ON p.id = d.project_id
WHERE d.status = 'pending_review'
ORDER BY d.due_at ASC
LIMIT 50;
```

Look for:
- **Seq Scan** on large tables → needs an index
- **Nested Loop** with high row counts → consider `Hash Join`
- **Buffers: shared read** → data not in cache, may be slow on cold start

### Vacuum & Maintenance

```sql
-- Check table bloat
SELECT
    schemaname, tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
    n_dead_tup AS dead_rows,
    last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 10;
```

---

## Security Checklist

- **Parameterized queries only.** Never build SQL with string concatenation.
- Use `LEAST()`, `GREATEST()` to clamp user-supplied LIMIT/OFFSET values.
- `GRANT` minimum permissions: app users get `SELECT/INSERT/UPDATE/DELETE`, never `DROP` or `CREATE`.
- Row-level security (RLS) for multi-tenant data isolation.
- Encrypt sensitive columns at the application layer, not in SQL.
- Audit all `DELETE` operations — prefer soft delete (`deleted_at`) over hard delete.

---

## Backup & Restore

```bash
# Backup (compressed, with timestamps)
pg_dump -Fc -h localhost -U app_user -d liveapp \
  > "/backups/liveapp_$(date +%Y%m%d_%H%M%S).dump"

# Restore
pg_restore -h localhost -U app_user -d liveapp \
  --clean --if-exists \
  /backups/liveapp_20260601_020000.dump

# Dump specific table
pg_dump -t deliverables -Fc -h localhost -U app_user -d liveapp \
  > /backups/deliverables_only.dump
```

---

## Common Pitfalls

- Using `TIMESTAMP` without timezone — always use `TIMESTAMPTZ`.
- Forgetting `WHERE deleted_at IS NULL` on soft-delete tables — add partial indexes.
- `SELECT *` in production queries — list columns explicitly, avoids breaking on schema changes.
- Missing `ON DELETE CASCADE` or `ON DELETE SET NULL` — orphaned rows accumulate silently.
- Ignoring `VACUUM` on high-write tables — leads to table bloat and slow queries.
- Using `OFFSET` for deep pagination — use keyset pagination (`WHERE id > :last_id`) instead.
