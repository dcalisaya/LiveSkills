# CI/CD, Deployment & Web Server Reference — Live Developer Stack

## Pipeline Architecture

```
Code Push → GitHub Actions → Build & Test → Deploy to VM → Health Check → Notify
```

All deployments follow this flow. No manual deploys to production without CI.

---

## GitHub Actions — Standard Workflow

### Deploy on Push to Main

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

env:
  DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
  DEPLOY_USER: deploy
  DEPLOY_PATH: /opt/app

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Set up SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh-keyscan -p 2222 -H $DEPLOY_HOST >> ~/.ssh/known_hosts

      - name: Deploy
        run: |
          ssh -p 2222 ${DEPLOY_USER}@${DEPLOY_HOST} << 'ENDSSH'
            cd ${DEPLOY_PATH}
            git pull origin main
            npm ci --production
            npm run build
            pm2 restart app --update-env
          ENDSSH

      - name: Health check
        run: |
          sleep 5
          curl -sf --max-time 10 "https://${{ secrets.APP_DOMAIN }}/health" || exit 1
```

### PR Validation (Lint + Test)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main, develop]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --coverage
```

---

## Docker Deployment

### docker-compose.yml (Standard App)

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "127.0.0.1:3000:3000"
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    ports:
      - "127.0.0.1:5432:5432"

volumes:
  pgdata:
```

### Dockerfile (Node.js Production)

```dockerfile
# Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup -s /bin/sh -D appuser
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

### Docker Deploy Script

```bash
#!/usr/bin/env bash
set -euo pipefail

# Pull latest code
cd /opt/app
git pull origin main

# Build and restart (zero-downtime with health check)
docker compose build --no-cache app
docker compose up -d --remove-orphans

# Wait for health
sleep 5
docker compose exec app curl -sf http://localhost:3000/health || {
  echo "ERROR: Health check failed. Rolling back..."
  docker compose rollback
  exit 1
}

echo "Deploy complete"
docker compose ps
```

---

## Nginx Configuration

### Reverse Proxy (Standard)

```nginx
# /etc/nginx/sites-available/app.livedeveloper.com
server {
    listen 80;
    server_name app.livedeveloper.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name app.livedeveloper.com;

    # SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/app.livedeveloper.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.livedeveloper.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Proxy to app
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 90;
    }

    # Static assets with caching
    location /assets/ {
        proxy_pass http://127.0.0.1:3000;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Health check (no logging)
    location /health {
        proxy_pass http://127.0.0.1:3000;
        access_log off;
    }
}
```

### SSL Setup (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d app.livedeveloper.com --non-interactive --agree-tos -m admin@livedeveloper.com

# Auto-renewal (added automatically by certbot)
# Verify:
sudo certbot renew --dry-run
```

---

## DNS (Cloudflare)

### Standard Records

| Type | Name | Value | Proxy |
|---|---|---|---|
| A | `app` | `<server-ip>` | ✅ Proxied |
| A | `api` | `<server-ip>` | ✅ Proxied |
| CNAME | `www` | `livedeveloper.com` | ✅ Proxied |
| MX | `@` | Mail provider | ❌ DNS only |
| TXT | `@` | SPF record | ❌ DNS only |
| TXT | `_dmarc` | DMARC policy | ❌ DNS only |

### Cloudflare Settings

- SSL/TLS: **Full (Strict)** — origin has valid cert
- Always Use HTTPS: **On**
- Minimum TLS Version: **1.2**
- Auto Minify: **Off** (let build tools handle this)
- Brotli: **On**

---

## Deploy Checklist

Before any production deployment:

```
□ All tests passing on CI
□ Code reviewed and approved
□ Database migrations tested on staging
□ Environment variables set on target
□ Backup/snapshot taken
□ Rollback plan documented
□ Health check endpoint working
□ Monitoring/alerts configured
□ DNS propagated (if new domain)
□ SSL certificate valid
```

---

## Rollback Procedures

### Application Rollback

```bash
# Option 1: Git revert
cd /opt/app
git revert HEAD --no-edit
npm ci && npm run build
pm2 restart app

# Option 2: Previous Docker image
docker compose down
docker tag app:latest app:rollback
docker compose up -d --build

# Option 3: VM snapshot rollback (nuclear option)
qm rollback 110 pre-deploy
```

### Database Rollback

```bash
# Run down migration
npm run migrate:down

# Or restore from backup
pg_restore -h localhost -U app_user -d liveapp --clean --if-exists /backups/pre-deploy.dump
```
