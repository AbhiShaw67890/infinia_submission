# Case 5: Zero-to-Deploy — Task Management API

**Live demo:** https://zero-to-deploy.onrender.com
**Repo:** https://github.com/AbhiShaw67890/ZERO-TO-DEPLOY

---

## What this is

This project is a production-ready Task Management REST API built with FastAPI and PostgreSQL, designed to demonstrate deployment automation, operational reliability, and DevOps best practices.

The system includes Docker containerization, automated CI/CD pipelines, structured logging, health monitoring, and cloud deployment with automatic redeployments on every Git push.

---

## Core Features

* Task CRUD REST API
* PostgreSQL persistence using Neon DB
* Dockerized production setup
* GitHub Actions CI/CD pipeline
* Automatic deployment to Render
* Structured application logging
* Health and metrics endpoints
* Uptime monitoring with UptimeRobot
* Production-ready environment variable handling
* Automated testing with pytest

---

## Live Architecture

```text
Developer
   ↓ git push
GitHub Actions
   ↓
Lint → Test → Docker Build
   ↓
Render Deployment
   ↓
Live FastAPI Service
   ↓
Neon PostgreSQL

UptimeRobot monitors /health endpoint
```

---

## API Endpoints

### Health & Monitoring

| Method | Endpoint   | Description                          |
| ------ | ---------- | ------------------------------------ |
| GET    | `/`        | Service information                  |
| GET    | `/health`  | Health check + database connectivity |
| GET    | `/metrics` | Application metrics                  |

### Tasks CRUD

| Method | Endpoint      | Description   |
| ------ | ------------- | ------------- |
| GET    | `/tasks`      | List tasks    |
| POST   | `/tasks`      | Create task   |
| GET    | `/tasks/{id}` | Retrieve task |
| PUT    | `/tasks/{id}` | Update task   |
| DELETE | `/tasks/{id}` | Delete task   |

---

## How to run locally

### 1. Clone the repository

```bash
git clone https://github.com/AbhiShaw67890/ZERO-TO-DEPLOY.git
cd ZERO-TO-DEPLOY
```

### 2. Create virtual environment

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env`

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ENVIRONMENT=development
DEBUG=True
```

### 5. Start development server

```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Open API documentation

```text
http://localhost:8000/docs
```

---

## Docker Setup

### Start full stack

```bash
docker-compose up -d
```

### View logs

```bash
docker-compose logs -f app
```

### Stop containers

```bash
docker-compose down
```

---

## Stack

| Layer            | Technology        | Why it was chosen                            |
| ---------------- | ----------------- | -------------------------------------------- |
| Backend          | FastAPI           | Lightweight, fast, async-ready API framework |
| Database         | PostgreSQL (Neon) | Reliable cloud-hosted relational database    |
| ORM              | SQLAlchemy        | Flexible and production-ready ORM            |
| Deployment       | Render            | Easy CI/CD integration with GitHub           |
| Containerization | Docker            | Reproducible production environments         |
| Monitoring       | UptimeRobot       | Simple uptime and health monitoring          |
| CI/CD            | GitHub Actions    | Automated testing and deployment             |
| Logging          | Python logging    | Structured operational logging               |

---

## Project Structure

```text
project/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── logging_config.py
│   ├── routes/
│   │   ├── health.py
│   │   └── tasks.py
│   └── services/
│       └── task_service.py
│
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   └── test_tasks.py
│
├── alembic/
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── render.yaml
├── requirements.txt
├── .env.example
├── README.md
└── RUNBOOK.md
```

---

## CI/CD Pipeline

The CI/CD workflow automatically runs on every push to GitHub.

Pipeline steps:

1. Install dependencies
2. Run linting
3. Run pytest test suite
4. Build Docker image
5. Trigger automatic Render deployment

This enables seamless deployment:

```text
git push → CI pipeline → Render deploy → live update
```

---

## Monitoring & Health Checks

The application exposes:

```text
GET /health
```

This endpoint checks:

* API availability
* database connectivity
* response health

UptimeRobot continuously monitors this endpoint and alerts on downtime.

---

## Deployment

The application is deployed using:

* Render → application hosting
* Neon → PostgreSQL database
* GitHub Actions → CI/CD automation
* UptimeRobot → health monitoring

### Render Configuration

#### Build Command

```bash
pip install -r requirements.txt
```

#### Start Command

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

---

## Environment Variables

```env
DATABASE_URL=postgresql://...
SECRET_KEY=...
ENVIRONMENT=production
DEBUG=False
```

---

## Testing

### Run all tests

```bash
pytest tests/ -v
```

### Run specific test file

```bash
pytest tests/test_tasks.py -v
```

---

## What's NOT done

* Authentication and authorization
* Rate limiting
* Distributed tracing
* Kubernetes deployment
* Horizontal autoscaling
* Advanced metrics dashboards

These were intentionally excluded to focus on a clean and production-aware MVP within the project time constraints.

---

## In production, I would also add

* JWT authentication
* API rate limiting
* Prometheus + Grafana monitoring
* Centralized log aggregation
* Blue/green deployment strategy
* Redis caching
* OpenTelemetry tracing
* Load testing and autoscaling

---

## Key Engineering Decisions

* Chose FastAPI for lightweight high-performance APIs
* Used Docker to ensure reproducible deployments
* Used GitHub Actions for automated CI/CD
* Used Render to simplify deployment infrastructure
* Used Neon PostgreSQL for managed cloud database hosting
* Added health monitoring to simulate production operational practices
* Prioritized operational maturity over application complexity

---

## Additional Documentation

* `RUNBOOK.md` — operational troubleshooting and deployment procedures

---

## Author

Built for the “Zero-to-Deploy — Ship a Service Like You Mean It” DevOps case study challenge.
