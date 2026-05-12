# 📘 RUNBOOK — Task Management API

> Operational runbook for the Task Management API service.
> This document provides procedures for deployment, monitoring, debugging, and incident response.

---

## 1. Service Overview

| Field           | Value                              |
|----------------|------------------------------------|
| **Service Name** | Task Management API              |
| **Technology**   | Python 3.11 + FastAPI             |
| **Database**     | PostgreSQL (Neon)                 |
| **Hosting**      | Render                           |
| **CI/CD**        | GitHub Actions                   |
| **Monitoring**   | UptimeRobot                      |
| **Repository**   | github.com/AbhiShaw67890/ZERO-TO-DEPLOY |

### Key URLs

| Resource           | URL                                            |
|-------------------|-------------------------------------------------|
| Production API     | `https://<your-app>.onrender.com`              |
| Health Check       | `https://<your-app>.onrender.com/health`       |
| API Documentation  | `https://<your-app>.onrender.com/docs`         |
| Metrics            | `https://<your-app>.onrender.com/metrics`      |
| Render Dashboard   | `https://dashboard.render.com`                 |
| GitHub Actions     | `https://github.com/AbhiShaw67890/ZERO-TO-DEPLOY/actions` |
| UptimeRobot        | `https://uptimerobot.com/dashboard`            |
| Neon Console       | `https://console.neon.tech`                    |

---

## 2. Architecture Overview

```
┌──────────┐     ┌────────────────┐     ┌──────────┐     ┌─────────────┐
│Developer │────▶│ GitHub Actions │────▶│  Render  │────▶│ FastAPI App │
│          │push │ (CI/CD)        │hook │          │     │             │
└──────────┘     └────────────────┘     └──────────┘     └──────┬──────┘
                                                                │
                                                                ▼
                                                        ┌──────────────┐
                                                        │    Neon      │
                                                        │ PostgreSQL   │
                                                        └──────────────┘
                                                                ▲
                                                                │
                                                        ┌──────────────┐
                                                        │ UptimeRobot  │
                                                        │ (monitoring) │
                                                        └──────────────┘
```

### Components

- **FastAPI Application** — Handles HTTP requests, CRUD operations
- **PostgreSQL (Neon)** — Persistent data storage with connection pooling
- **Render** — Cloud hosting with auto-deploy
- **GitHub Actions** — Automated testing, linting, Docker build, deployment
- **UptimeRobot** — External health monitoring and alerting

---

## 3. Deployment Process

### Automatic Deployment (Standard)

1. Developer pushes code to `main` branch
2. GitHub Actions pipeline triggers:
   - **Lint** — `flake8` checks code quality
   - **Test** — `pytest` runs all test suites
   - **Build** — Docker image builds successfully
   - **Deploy** — Render deploy hook is triggered
3. Render pulls latest code and rebuilds
4. New version goes live automatically

### Manual Deployment

If automatic deployment fails:

```bash
# Option 1: Trigger via Render Dashboard
# Go to Render Dashboard → Select Service → Click "Manual Deploy" → "Deploy latest commit"

# Option 2: Trigger via deploy hook
curl -X POST "https://api.render.com/deploy/YOUR_DEPLOY_HOOK_URL"
```

### Deployment Verification

```bash
# 1. Check health endpoint
curl https://your-app.onrender.com/health

# Expected response:
# {"status": "ok", "timestamp": "...", "version": "1.0.0", "environment": "production", "database": "connected"}

# 2. Check version
curl https://your-app.onrender.com/ | jq .version

# 3. Check metrics
curl https://your-app.onrender.com/metrics
```

---

## 4. Rollback Instructions

### Via Render Dashboard

1. Go to **Render Dashboard** → Select your service
2. Click **Events** tab
3. Find the last working deployment
4. Click **"Rollback to this deploy"**

### Via Git

```bash
# Find the last working commit
git log --oneline -10

# Revert to a specific commit
git revert <bad-commit-hash>
git push origin main
# This triggers a new deployment with the fix
```

### Emergency: Disable Service

If the service is causing harm:

1. Go to **Render Dashboard** → Select service
2. Click **Settings** → **Suspend Service**
3. Investigate the issue
4. Resume when fixed

---

## 5. Common Failure Scenarios

### 5.1 Database Connection Failure

**Symptoms**: `/health` returns `{"status": "degraded", "database": "disconnected"}`

**Causes**:
- Neon database is sleeping (free tier auto-suspends)
- `DATABASE_URL` is incorrect or expired
- Neon service outage

**Resolution**:
1. Check Neon Console — is the database active?
2. Verify `DATABASE_URL` environment variable on Render
3. Try accessing the database directly: `psql $DATABASE_URL`
4. If Neon is down, check [Neon Status Page](https://neonstatus.com)

### 5.2 CI/CD Pipeline Failure

**Symptoms**: GitHub Actions shows red ❌

**Common Causes**:
- Lint errors → Fix code style issues
- Test failures → Debug failing tests
- Docker build failure → Check Dockerfile and dependencies
- Deploy hook failure → Verify `RENDER_DEPLOY_HOOK_URL` secret

**Resolution**:
1. Check the GitHub Actions log for the specific failure
2. Fix the issue locally
3. Push the fix

### 5.3 Application Crash on Startup

**Symptoms**: Render shows "Deploy failed" or service restarts repeatedly

**Causes**:
- Missing environment variables
- Database migration failure
- Import errors in code

**Resolution**:
1. Check Render logs: Dashboard → Service → Logs
2. Verify all environment variables are set
3. Test locally: `uvicorn app.main:app --reload`

### 5.4 Slow Response Times

**Symptoms**: API responses taking > 2 seconds

**Causes**:
- Neon cold start (free tier)
- Database queries without indexes
- Too many concurrent connections

**Resolution**:
1. Check `/metrics` for task counts
2. Review database query performance
3. Consider connection pooling adjustments

---

## 6. Debugging Checklist

When something goes wrong, follow this checklist:

- [ ] **Check health**: `curl https://your-app.onrender.com/health`
- [ ] **Check Render logs**: Dashboard → Service → Logs
- [ ] **Check GitHub Actions**: Recent workflow runs
- [ ] **Check UptimeRobot**: Alert history and response times
- [ ] **Check Neon Console**: Database status and connections
- [ ] **Check environment variables**: All required vars set on Render?
- [ ] **Reproduce locally**: Can you reproduce the issue locally?
- [ ] **Check recent changes**: `git log --oneline -5` — what changed?

---

## 7. Health Verification Steps

### Quick Health Check

```bash
curl -s https://your-app.onrender.com/health | python -m json.tool
```

### Expected Healthy Response

```json
{
    "status": "ok",
    "timestamp": "2025-01-01T00:00:00.000000+00:00",
    "version": "1.0.0",
    "environment": "production",
    "database": "connected"
}
```

### Full System Verification

```bash
# 1. Health check
curl -s https://your-app.onrender.com/health

# 2. Create a test task
curl -s -X POST https://your-app.onrender.com/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Health verification test"}'

# 3. List tasks (should include the test task)
curl -s https://your-app.onrender.com/tasks

# 4. Delete the test task
curl -s -X DELETE https://your-app.onrender.com/tasks/<id>

# 5. Check metrics
curl -s https://your-app.onrender.com/metrics
```

---

## 8. Environment Variable Setup

### Required Variables

| Variable       | Where to Set  | Example                                   |
|---------------|---------------|-------------------------------------------|
| `DATABASE_URL` | Render + GitHub | `postgresql://user:pass@host:5432/db`    |
| `SECRET_KEY`   | Render        | `a-long-random-string-here`              |
| `ENVIRONMENT`  | Render        | `production`                              |
| `DEBUG`        | Render        | `False`                                   |

### GitHub Secrets (for CI/CD)

| Secret                    | Purpose                    |
|--------------------------|----------------------------|
| `RENDER_DEPLOY_HOOK_URL` | Auto-deploy trigger URL    |

### How to Set on Render

1. Go to Render Dashboard → Select Service → **Environment**
2. Click **Add Environment Variable**
3. Enter key and value
4. Click **Save Changes** (triggers redeploy)

---

## 9. Incident Response Steps

### Severity Levels

| Level    | Description                           | Response Time |
|----------|---------------------------------------|---------------|
| **P1**   | Service completely down               | Immediately   |
| **P2**   | Service degraded (slow/partial)       | Within 1 hour |
| **P3**   | Non-critical issue (cosmetic/minor)   | Within 24 hours |

### P1 Response Procedure

1. **Acknowledge** — Note the time and symptoms
2. **Assess** — Check health endpoint, Render logs, Neon status
3. **Mitigate** — Rollback if a recent deploy caused it
4. **Communicate** — Update status page / notify stakeholders
5. **Fix** — Identify root cause and apply fix
6. **Verify** — Confirm health endpoint returns OK
7. **Post-mortem** — Document what happened and how to prevent it

### P2 Response Procedure

1. **Monitor** — Check if the issue is transient
2. **Investigate** — Review logs and metrics
3. **Fix** — Apply targeted fix
4. **Verify** — Confirm resolution

---

## 10. Production Troubleshooting

### View Application Logs

```bash
# Via Render Dashboard
# Dashboard → Service → Logs (real-time streaming)
```

### Connect to Database

```bash
# Via psql (if installed locally)
psql "postgresql://user:pass@host:5432/dbname?sslmode=require"

# Check table contents
SELECT COUNT(*) FROM tasks;
SELECT * FROM tasks ORDER BY created_at DESC LIMIT 10;
```

### Common Fixes

| Problem                          | Fix                                        |
|----------------------------------|--------------------------------------------|
| 502 Bad Gateway                  | Check Render logs; likely app crash         |
| Database connection refused      | Verify DATABASE_URL; check Neon status     |
| Slow cold start                  | Normal for Render free tier (~30s)         |
| CI/CD not deploying              | Check RENDER_DEPLOY_HOOK_URL secret        |
| Tests passing locally, fail in CI| Check Python version match (3.11)          |
| Import errors after deploy       | Check requirements.txt is complete         |

### Useful Commands

```bash
# Test locally before pushing
pytest tests/ -v
flake8 app/ tests/ --max-line-length=120

# Build Docker image locally
docker build -t task-api .
docker run -p 8000:8000 -e DATABASE_URL=sqlite:///./test.db task-api

# View recent git changes
git log --oneline -10
git diff HEAD~1
```

---

> **Last Updated**: 2025-01-01
> **Maintained By**: DevOps Team
