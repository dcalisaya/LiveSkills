# Bash / Shell Reference — Live Developer Stack

## Runtime & Conventions

- **Bash 5.2+** on Ubuntu 24.04 (Proxmox VMs) and macOS (zsh-compatible).
- Every script starts with a strict header — no exceptions.
- Scripts are executable files, not sourced libraries. One script = one task.
- Naming: `verb-noun.sh` (e.g., `deploy-app.sh`, `backup-db.sh`, `check-health.sh`).

## Strict Header (Required)

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# ── Description ──────────────────────────────────────────────
# Purpose:  <one-line description>
# Author:   Daniel Calisaya / Live Developer
# Usage:    ./verb-noun.sh [options]
# ─────────────────────────────────────────────────────────────
```

### What Each Flag Does

| Flag | Behavior |
|---|---|
| `-e` | Exit immediately on any non-zero exit code |
| `-u` | Treat unset variables as errors |
| `-o pipefail` | Pipe returns the exit code of the last failing command |

---

## Environment & Configuration

```bash
# Load .env file safely
if [[ -f .env ]]; then
  set -a
  source .env
  set +a
fi

# Required env vars — fail fast if missing
: "${DATABASE_URL:?ERROR: DATABASE_URL is not set}"
: "${DEPLOY_TARGET:?ERROR: DEPLOY_TARGET is not set}"
: "${API_KEY:?ERROR: API_KEY is not set}"
```

---

## Logging Pattern

```bash
readonly LOG_FILE="/var/log/livedeveloper/$(basename "$0" .sh).log"
readonly TIMESTAMP_FMT="+%Y-%m-%d %H:%M:%S"

log_info()  { echo "[$(date "$TIMESTAMP_FMT")] [INFO]  $*" | tee -a "$LOG_FILE"; }
log_warn()  { echo "[$(date "$TIMESTAMP_FMT")] [WARN]  $*" | tee -a "$LOG_FILE" >&2; }
log_error() { echo "[$(date "$TIMESTAMP_FMT")] [ERROR] $*" | tee -a "$LOG_FILE" >&2; }
log_step()  { echo "[$(date "$TIMESTAMP_FMT")] [STEP]  ── $* ──" | tee -a "$LOG_FILE"; }

# Usage
log_step "Starting deployment"
log_info "Target: ${DEPLOY_TARGET}"
log_error "Connection refused on port 5432"
```

---

## Argument Parsing

### Simple (positional)

```bash
readonly TARGET="${1:?Usage: $0 <target> [--dry-run]}"
readonly DRY_RUN="${2:-}"

if [[ "$DRY_RUN" == "--dry-run" ]]; then
  log_info "Dry run mode — no changes will be made"
fi
```

### Robust (flags with getopts)

```bash
usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Options:
  -t, --target    TARGET    Deployment target (required)
  -e, --env       ENV       Environment: staging|production (default: staging)
  -d, --dry-run             Simulate without executing
  -h, --help                Show this help
EOF
  exit "${1:-0}"
}

TARGET=""
ENV="staging"
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--target)  TARGET="$2"; shift 2 ;;
    -e|--env)     ENV="$2"; shift 2 ;;
    -d|--dry-run) DRY_RUN=true; shift ;;
    -h|--help)    usage 0 ;;
    *)            log_error "Unknown option: $1"; usage 1 ;;
  esac
done

[[ -z "$TARGET" ]] && { log_error "--target is required"; usage 1; }
```

---

## Common Patterns

### Cleanup Trap (always runs on exit)

```bash
cleanup() {
  local exit_code=$?
  log_info "Cleaning up temporary files..."
  rm -rf "${TEMP_DIR:-}"
  if [[ $exit_code -ne 0 ]]; then
    log_error "Script failed with exit code: $exit_code"
  fi
  exit $exit_code
}
trap cleanup EXIT

TEMP_DIR="$(mktemp -d)"
```

### SSH Remote Execution

```bash
readonly REMOTE_HOST="root@${DEPLOY_TARGET}"

remote_exec() {
  ssh -o ConnectTimeout=10 \
      -o StrictHostKeyChecking=accept-new \
      "$REMOTE_HOST" "$@"
}

# Usage
remote_exec "systemctl restart nginx"
remote_exec "docker compose -f /opt/app/docker-compose.yml up -d"
```

### Health Check with Retry

```bash
wait_for_health() {
  local url="$1"
  local max_attempts="${2:-10}"
  local delay="${3:-3}"

  for ((i = 1; i <= max_attempts; i++)); do
    if curl -sf --max-time 5 "$url" > /dev/null 2>&1; then
      log_info "Health check passed (attempt $i/$max_attempts)"
      return 0
    fi
    log_warn "Health check attempt $i/$max_attempts failed. Retrying in ${delay}s..."
    sleep "$delay"
  done

  log_error "Health check failed after $max_attempts attempts: $url"
  return 1
}

# Usage
wait_for_health "https://app.livedeveloper.com/health" 15 5
```

### File Operations (safe)

```bash
# Backup before overwrite
backup_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    cp "$file" "${file}.bak.$(date +%Y%m%d%H%M%S)"
    log_info "Backed up: $file"
  fi
}

# Atomic write (write to temp, then move)
atomic_write() {
  local target="$1"
  local content="$2"
  local tmp
  tmp="$(mktemp "${target}.tmp.XXXXXX")"
  echo "$content" > "$tmp"
  mv "$tmp" "$target"
  log_info "Wrote: $target"
}
```

---

## Deploy Script Template (Full)

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# ── deploy-app.sh ────────────────────────────────────────────
# Purpose:  Deploy application to target VM
# Author:   Daniel Calisaya / Live Developer
# Usage:    ./deploy-app.sh --target <ip> --env staging
# ─────────────────────────────────────────────────────────────

# --- Config ---
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/.env" 2>/dev/null || true

# --- Parse args ---
TARGET=""
ENV="staging"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="$2"; shift 2 ;;
    --env)    ENV="$2"; shift 2 ;;
    *)        echo "Unknown: $1" >&2; exit 1 ;;
  esac
done
[[ -z "$TARGET" ]] && { echo "Error: --target required" >&2; exit 1; }

# --- Cleanup ---
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

# --- Deploy ---
echo "==> Deploying to $TARGET ($ENV)"

scp -r ./dist/ "root@${TARGET}:/opt/app/"
ssh "root@${TARGET}" "cd /opt/app && docker compose up -d --build"

echo "==> Deploy complete"
```

---

## Cron Job Conventions

```bash
# Edit crontab
crontab -e

# Format: minute hour day month weekday command
# Run backup daily at 2 AM
0 2 * * * /opt/scripts/backup-db.sh >> /var/log/livedeveloper/backup.log 2>&1

# Run health check every 5 minutes
*/5 * * * * /opt/scripts/check-health.sh >> /var/log/livedeveloper/health.log 2>&1
```

Always redirect output to a log file. Never rely on `MAILTO`.

---

## Security Checklist

- Never hardcode passwords, tokens, or keys. Use `.env` or environment variables.
- Use `"$variable"` (quoted) everywhere. Unquoted variables cause word splitting.
- Validate all user-supplied inputs before use.
- Use `readonly` for constants. Prevents accidental reassignment.
- Prefer `[[ ]]` over `[ ]` — more robust, supports regex and pattern matching.
- Never use `eval` with user input. Period.
- Set file permissions explicitly: `chmod 700` for scripts with secrets.

---

## Common Pitfalls

- Forgetting to quote `"$variable"` — causes word splitting and glob expansion.
- Using `cd` without `|| exit` — if `cd` fails, the script continues in the wrong directory.
- Piping to `while read` in a subshell — variables set inside won't persist. Use `< <(command)`.
- Using `rm -rf $DIR/` with an unset `$DIR` — expands to `rm -rf /`. Always use `"${DIR:?}"`.
- Assuming GNU tools on macOS — `sed`, `date`, `grep` differ. Use `gsed`, `gdate` if needed.
