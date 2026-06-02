# Proxmox VMs Reference — Live Developer Stack

## Environment

- **Proxmox VE 8.x** running on Mac Studio M4 Max (local dev/staging) and dedicated servers (production).
- Guest OS: **Ubuntu 24.04 LTS** (server, minimal install).
- Network: bridged (`vmbr0`) for public-facing, internal network (`vmbr1`) for inter-VM communication.
- Storage: local-lvm (SSDs) for VM disks, NFS or local directory for backups and ISOs.

---

## VM Provisioning Checklist

Every new VM follows this sequence:

```
1. Create VM from template (or fresh install)
2. Set resources (CPU, RAM, disk)
3. Configure networking (static IP or DHCP reservation)
4. Initial SSH setup (key auth, disable password)
5. System hardening (firewall, fail2ban, updates)
6. Install application dependencies
7. Verify connectivity and health
8. Document in infrastructure registry
```

---

## VM Creation via CLI

### From Template (Preferred)

```bash
# Clone VM from template (ID 9000 = Ubuntu 24.04 base template)
qm clone 9000 110 --name liveapp-staging --full true --storage local-lvm

# Set resources
qm set 110 --cores 4 --memory 8192 --balloon 4096

# Set network
qm set 110 --net0 virtio,bridge=vmbr0

# Set cloud-init (if template supports it)
qm set 110 --ciuser deploy --cipassword "" --sshkeys /root/.ssh/authorized_keys.pub
qm set 110 --ipconfig0 ip=10.0.1.110/24,gw=10.0.1.1

# Start VM
qm start 110
```

### From ISO (Fresh Install)

```bash
# Create VM
qm create 111 --name new-service --cores 2 --memory 4096 \
  --net0 virtio,bridge=vmbr0 \
  --scsi0 local-lvm:32 \
  --cdrom local:iso/ubuntu-24.04-live-server-amd64.iso \
  --boot order=scsi0 \
  --ostype l26

qm start 111
```

---

## Template Creation

Create a reusable base template from a configured VM:

```bash
# On the configured VM (SSH in first):
sudo apt update && sudo apt upgrade -y
sudo apt install -y qemu-guest-agent cloud-init
sudo apt autoremove -y
sudo cloud-init clean
sudo truncate -s 0 /etc/machine-id
sudo poweroff

# On Proxmox host:
qm template 9000
```

### What the Base Template Should Include

- Ubuntu 24.04 minimal server
- `qemu-guest-agent` installed and enabled
- `cloud-init` configured
- SSH server running, password auth disabled
- UFW installed (not yet enabled — enable per-VM)
- Basic tools: `curl`, `wget`, `git`, `htop`, `tmux`, `jq`
- Timezone set to UTC
- Locale set to `en_US.UTF-8`
- Swap configured (2GB)

---

## Initial VM Hardening

Run this on every new VM after first boot:

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- SSH hardening ---
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# --- Firewall ---
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp comment "SSH"
sudo ufw allow 80/tcp comment "HTTP"
sudo ufw allow 443/tcp comment "HTTPS"
sudo ufw --force enable

# --- fail2ban ---
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# --- Automatic security updates ---
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# --- System updates ---
sudo apt update && sudo apt upgrade -y
```

---

## Networking Patterns

### Static IP Assignment

```bash
# /etc/netplan/00-installer-config.yaml
network:
  version: 2
  ethernets:
    ens18:
      dhcp4: false
      addresses:
        - 10.0.1.110/24
      routes:
        - to: default
          via: 10.0.1.1
      nameservers:
        addresses:
          - 1.1.1.1
          - 8.8.8.8

# Apply
sudo netplan apply
```

### Internal Network (VM-to-VM)

```
vmbr0 (public bridge)  → Internet-facing services
vmbr1 (internal bridge) → Database, cache, internal APIs

# VM with both networks:
qm set 110 --net0 virtio,bridge=vmbr0 --net1 virtio,bridge=vmbr1
```

---

## Backup Strategy

### Automated Proxmox Backups

```bash
# In Proxmox UI: Datacenter → Backup → Add
# Or via CLI:
vzdump 110 --storage local --compress zstd --mode snapshot --mailto admin@livedeveloper.com

# Scheduled backup (all VMs, nightly at 1 AM)
# Add to /etc/cron.d/vzdump:
0 1 * * * root vzdump --all --storage local --compress zstd --mode snapshot --mailnotification always
```

### Retention Policy

| Environment | Retention | Schedule |
|---|---|---|
| Production | 7 daily + 4 weekly + 3 monthly | Daily at 1 AM |
| Staging | 3 daily | Daily at 2 AM |
| Development | 1 daily | Daily at 3 AM |

### Application-Level Backups (PostgreSQL)

```bash
# Database dump (use alongside VM snapshots)
pg_dump -Fc -h localhost -U app_user -d liveapp \
  > "/backups/db/liveapp_$(date +%Y%m%d_%H%M%S).dump"

# Sync backups off-site
rsync -avz /backups/ backup-server:/remote-backups/proxmox-host/
```

---

## Resource Allocation Guide

| Workload Type | CPU Cores | RAM | Disk | Example |
|---|---|---|---|---|
| Small web service | 1-2 | 2 GB | 20 GB | Static site, small API |
| Application server | 2-4 | 4-8 GB | 40 GB | LiveApp backend |
| Database server | 2-4 | 8-16 GB | 100+ GB | PostgreSQL primary |
| Build/CI runner | 4-8 | 8-16 GB | 60 GB | GitHub Actions runner |
| AI/ML workload | 4-8 | 16-32 GB | 100+ GB | Ollama, model inference |

---

## Common Proxmox Commands

```bash
# List all VMs
qm list

# VM status
qm status 110

# Start/stop/restart
qm start 110
qm stop 110
qm reboot 110

# Snapshot
qm snapshot 110 pre-deploy --description "Before v2.1 deployment"

# Rollback to snapshot
qm rollback 110 pre-deploy

# Delete snapshot
qm delsnapshot 110 pre-deploy

# Resize disk
qm resize 110 scsi0 +20G

# Console access
qm terminal 110
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| VM won't start | Insufficient resources | Check `qm config 110`, reduce RAM/CPU |
| Network unreachable | Netplan misconfigured | Check `/etc/netplan/*.yaml`, run `netplan apply` |
| Disk full | Logs or unmanaged files | `df -h`, `du -sh /var/log/*`, rotate logs |
| High CPU (host) | VM resource contention | `htop` on host, check balloon driver, add cores |
| Backup failed | Storage full | Check `pvesm status`, clean old backups |
| SSH refused | Firewall or SSH config | Check `ufw status`, verify SSH port, check `sshd_config` |
