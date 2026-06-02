# Monitoring & Incident Response Reference — Live Developer Stack

## Monitoring Architecture

```
Application → Health Endpoints → Uptime Kuma → Alerts (Telegram/Email)
     ↓
  Logs → journald / Docker logs → Log rotation
     ↓
  Metrics → Custom health scripts → Cron checks
```

---

## Health Check Endpoints

Every service must expose a `/health` endpoint:

### Basic Health (HTTP 200 = OK)

```typescript
// Node.js / Fastify
app.get('/health', async (_req, reply) => {
  return reply.status(200).send({ status: 'ok', timestamp: new Date().toISOString() })
})
```

### Deep Health (Check Dependencies)

```typescript
app.get('/health/deep', async (_req, reply) => {
  const checks: Record<string, string> = {}

  // Database
  try {
    await db.execute(sql`SELECT 1`)
    checks.database = 'ok'
  } catch {
    checks.database = 'error'
  }

  // Redis
  try {
    await redis.ping()
    checks.redis = 'ok'
  } catch {
    checks.redis = 'error'
  }

  const allOk = Object.values(checks).every(v => v === 'ok')

  return reply.status(allOk ? 200 : 503).send({
    status: allOk ? 'healthy' : 'degraded',
    checks,
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  })
})
```

### Python (FastAPI)

```python
@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now(UTC).isoformat()}

@app.get("/health/deep")
async def health_deep():
    checks = {}
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"

    all_ok = all(v == "ok" for v in checks.values())
    status_code = 200 if all_ok else 503
    return JSONResponse(
        status_code=status_code,
        content={"status": "healthy" if all_ok else "degraded", "checks": checks},
    )
```

---

## Uptime Kuma Setup

### Installation (Docker)

```bash
docker run -d \
  --name uptime-kuma \
  --restart unless-stopped \
  -p 127.0.0.1:3001:3001 \
  -v uptime-kuma-data:/app/data \
  louislam/uptime-kuma:1
```

### Monitor Configuration

| Service | Type | URL/Target | Interval | Retries |
|---|---|---|---|---|
| LiveApp API | HTTP(s) | `https://app.livedeveloper.com/health` | 60s | 3 |
| LiveApp Deep | HTTP(s) | `https://app.livedeveloper.com/health/deep` | 300s | 2 |
| PostgreSQL | TCP Port | `db-server:5432` | 60s | 3 |
| Nginx | HTTP(s) | `https://livedeveloper.com` | 60s | 3 |
| SSH | TCP Port | `server:2222` | 120s | 2 |
| Client Site | HTTP(s) | `https://client-domain.com` | 300s | 3 |

### Alert Channels

- **Telegram Bot** — Primary. Instant notification for Critical and Warning.
- **Email** — Secondary. Summary for all events.
- Configure in Uptime Kuma: Settings → Notifications.

---

## Log Management

### Application Logs (Docker)

```bash
# View logs (last 100 lines, follow)
docker compose logs -f --tail 100 app

# Filter by time
docker compose logs --since "2026-06-01T00:00:00" app

# Save logs to file
docker compose logs app > /var/log/app/$(date +%Y%m%d).log
```

### System Logs (journald)

```bash
# Service logs
journalctl -u nginx -f --no-pager -n 50

# Logs since last boot
journalctl -b

# Filter by priority (err and above)
journalctl -p err --since "1 hour ago"
```

### Log Rotation

```bash
# /etc/logrotate.d/app
/var/log/app/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 appuser appgroup
    postrotate
        docker compose -f /opt/app/docker-compose.yml restart app > /dev/null 2>&1 || true
    endscript
}
```

---

## Custom Health Check Scripts

### Server Resource Check

```bash
#!/usr/bin/env bash
set -euo pipefail

# check-server-health.sh — Run via cron every 5 minutes

ALERT_THRESHOLD_CPU=85
ALERT_THRESHOLD_MEM=90
ALERT_THRESHOLD_DISK=85

# CPU usage (1-minute load average vs cores)
cpu_cores=$(nproc)
load_avg=$(awk '{print $1}' /proc/loadavg)
cpu_pct=$(echo "$load_avg $cpu_cores" | awk '{printf "%.0f", ($1/$2)*100}')

# Memory usage
mem_pct=$(free | awk '/Mem:/ {printf "%.0f", $3/$2*100}')

# Disk usage (root partition)
disk_pct=$(df / | awk 'NR==2 {print $5}' | tr -d '%')

# Alert if thresholds exceeded
alerts=""
[[ $cpu_pct -gt $ALERT_THRESHOLD_CPU ]] && alerts+="CPU: ${cpu_pct}% "
[[ $mem_pct -gt $ALERT_THRESHOLD_MEM ]] && alerts+="MEM: ${mem_pct}% "
[[ $disk_pct -gt $ALERT_THRESHOLD_DISK ]] && alerts+="DISK: ${disk_pct}% "

if [[ -n "$alerts" ]]; then
  echo "[ALERT] $(hostname): $alerts" | tee -a /var/log/health-alerts.log
  # Send to Telegram or email here
fi
```

### Database Connection Check

```bash
#!/usr/bin/env bash
set -euo pipefail

# check-db-health.sh
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-app_user}"
DB_NAME="${DB_NAME:-liveapp}"

if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; then
  echo "[OK] PostgreSQL is ready"
else
  echo "[CRITICAL] PostgreSQL is NOT responding on ${DB_HOST}:${DB_PORT}"
  exit 1
fi

# Check active connections
active=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -tAc \
  "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'")
echo "[INFO] Active connections: $active"

if [[ $active -gt 80 ]]; then
  echo "[WARN] High connection count: $active"
fi
```

---

## Incident Response Playbook

### Severity Levels

| Level | Definition | Response Time | Escalation |
|---|---|---|---|
| **P1 — Critical** | Service completely down, data loss risk | < 15 min | Immediate — all hands |
| **P2 — Major** | Degraded performance, partial outage | < 1 hour | Notify team lead |
| **P3 — Minor** | Non-critical feature broken, workaround exists | < 4 hours | Ticket + schedule |
| **P4 — Low** | Cosmetic, non-functional, enhancement | Next sprint | Ticket only |

### Incident Response Steps

```
1. DETECT   — Alert fires or user reports issue
2. ASSESS   — Determine severity (P1-P4), impact, scope
3. MITIGATE — Apply immediate fix (restart, rollback, scale)
4. DIAGNOSE — Find root cause (logs, metrics, traces)
5. RESOLVE  — Deploy permanent fix
6. REVIEW   — Post-mortem: timeline, root cause, prevention
```

### Quick Mitigation Commands

```bash
# Restart application
docker compose restart app
# or
pm2 restart app

# Rollback to last known good
cd /opt/app && git checkout HEAD~1 && npm ci && npm run build && pm2 restart app

# Restart Nginx
sudo systemctl restart nginx

# Kill runaway process
sudo kill -9 $(pgrep -f "stuck-process")

# Free disk space (emergency)
sudo journalctl --vacuum-size=100M
docker system prune -f
sudo apt autoremove -y

# Check what's using a port
sudo lsof -i :3000
sudo ss -tlnp | grep 3000
```

### Post-Mortem Template

```markdown
# Incident Post-Mortem — [TITLE]

**Date:** YYYY-MM-DD
**Duration:** HH:MM
**Severity:** P1/P2/P3
**Impact:** [What users experienced]

## Timeline
- HH:MM — Alert fired
- HH:MM — Engineer acknowledged
- HH:MM — Root cause identified
- HH:MM — Mitigation applied
- HH:MM — Service fully restored

## Root Cause
[What actually broke and why]

## Resolution
[What was done to fix it]

## Prevention
- [ ] Action item 1
- [ ] Action item 2

## Lessons Learned
[What we'll do differently]
```

---

## Cron Schedule (Standard)

```bash
# /etc/cron.d/livedeveloper
# Health checks
*/5 * * * * root /opt/scripts/check-server-health.sh >> /var/log/health.log 2>&1
*/5 * * * * root /opt/scripts/check-db-health.sh >> /var/log/health.log 2>&1

# Database backup
0 2 * * * root /opt/scripts/backup-db.sh >> /var/log/backup.log 2>&1

# Log rotation check
0 0 * * * root logrotate /etc/logrotate.conf

# SSL certificate renewal
0 3 * * 1 root certbot renew --quiet >> /var/log/certbot.log 2>&1

# Docker cleanup (weekly)
0 4 * * 0 root docker system prune -f >> /var/log/docker-cleanup.log 2>&1
```
