---
name: devops-infra-agent
description: >
  Infrastructure, deployment, and operations skill for managing servers, VMs, CI/CD pipelines,
  containerization, monitoring, and cloud-adjacent infrastructure. Use this skill whenever the
  user asks to deploy, configure a server, set up CI/CD, manage Proxmox VMs, configure Nginx,
  set up Docker, automate backups, monitor services, manage DNS, SSL certificates, or any
  infrastructure-related task. Trigger on: "deploy", "server", "VM", "Proxmox", "Docker",
  "Nginx", "CI/CD", "pipeline", "backup", "monitor", "uptime", "SSL", "DNS", "cPanel",
  "infrastructure", "DevOps", "provision", or any request about keeping systems running.
version: 1.0.0
maintainer: Daniel Calisaya / Live Developer
---

# DevOps & Infrastructure Agent Skill

This skill guides OPUS through production infrastructure management across Live Developer's
server fleet — from Proxmox VM provisioning to CI/CD pipelines to production monitoring.
Every action must be safe, reversible where possible, and auditable.

---

## Agent Thinking Process

Before touching any server or pipeline, execute this checklist:

1. **Classify the operation** — Is this provisioning, deployment, configuration, troubleshooting, or monitoring?
2. **Identify the environment** — Production, staging, or development? This determines the risk level.
3. **Assess reversibility** — Can this be undone? If not, use the HITL pattern (see `dev-code-agent/references/agent-process-patterns.md`).
4. **Check dependencies** — What services depend on the target? Will they be affected?
5. **Plan the rollback** — Define the rollback steps BEFORE executing any change.
6. **Load the relevant reference** — Read the appropriate file in `references/` before acting.

---

## Infrastructure Map (Live Developer)

| Layer | Technology | Environment |
|---|---|---|
| Hypervisor | Proxmox VE 8.x | Mac Studio M4 Max (local), dedicated servers |
| VMs | Ubuntu 24.04 LTS | All production and staging workloads |
| Web Server | Nginx (reverse proxy) + Apache/LiteSpeed (cPanel) | Production |
| Containers | Docker + Docker Compose | Application workloads |
| CI/CD | GitHub Actions + custom deploy scripts | All repos |
| DNS | Cloudflare | All domains |
| SSL | Let's Encrypt (Certbot) + Cloudflare Origin Certs | All sites |
| Monitoring | Uptime Kuma + custom health checks | Production |
| Backups | pg_dump + rsync + cron | Nightly |
| cPanel | cPanel/WHM on shared hosting | Client sites |

---

## Operation Types

| Type | Risk Level | Pattern | Reference |
|---|---|---|---|
| New VM provisioning | Medium | Sequential Chain | `references/proxmox-vms.md` |
| Application deployment | High | Sequential + HITL | `references/ci-cd.md` |
| Configuration change (Nginx, Docker) | Medium | Sequential + Rollback | `references/ci-cd.md` |
| Monitoring setup | Low | Sequential | `references/monitoring.md` |
| Backup configuration | Medium | Sequential | `references/proxmox-vms.md` |
| Incident response | Critical | Router + HITL | `references/monitoring.md` |
| SSL/DNS setup | Medium | Sequential | `references/ci-cd.md` |

---

## Universal Infrastructure Standards

Apply these regardless of the operation:

- **Idempotency** — Running the same operation twice produces the same result.
- **Dry-run first** — Every destructive command should support a `--dry-run` mode.
- **Backup before change** — Take a snapshot or backup before any modification.
- **Least privilege** — Use the minimum permissions required. Never run as root when unnecessary.
- **Log everything** — Every change must be logged with timestamp, actor, and result.
- **No manual changes** — All configuration must be in version-controlled files. No ad-hoc SSH edits.
- **Document the state** — After every change, document what the system looks like now.

---

## Structured Output Format

When delivering infrastructure work, always structure the response as:

```
## Plan
[Steps to execute, with risk assessment]

## Pre-flight Checks
[What to verify before starting]

## Execution
[Commands and configurations — file(s) with clear headers]

## Verification
[How to confirm the change worked]

## Rollback
[Exact steps to undo this change if needed]
```

---

## Security Requirements (Non-Negotiable)

- Never expose SSH on port 22 to the public internet — use non-standard ports or VPN.
- SSH key-only authentication. Disable password login.
- Firewall (UFW) enabled on all VMs. Default deny inbound.
- Never store secrets in scripts or repos. Use environment variables or secret managers.
- Keep systems updated: `apt update && apt upgrade` on a regular schedule.
- Use fail2ban on all public-facing servers.
- HTTPS only. Redirect all HTTP to HTTPS. HSTS enabled.
- Database ports (5432, 3306) never exposed publicly. Local or VPN only.

---

## Reference Files

Load the relevant reference before acting:

- `references/proxmox-vms.md` — VM provisioning, templates, networking, backups, storage
- `references/ci-cd.md` — GitHub Actions, deploy scripts, Docker, Nginx, SSL, DNS
- `references/monitoring.md` — Health checks, Uptime Kuma, alerting, incident response, logs

---

# Changelog

## v1.0.0 — 2026-06
- Initial release. Foundation by Daniel Calisaya / Live Developer.
- Covers Proxmox, CI/CD, Docker, Nginx, monitoring.
- Infrastructure map and security requirements established.
