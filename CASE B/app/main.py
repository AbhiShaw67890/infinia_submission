"""
FastAPI application entry point.
Configures middleware, routes, logging, and lifecycle events.
"""

import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import APP_NAME, APP_VERSION, DEBUG, ENVIRONMENT
from app.logging_config import setup_logging
from app.database import Base, engine
from app.routes import health, tasks

# ── Initialize Logging ───────────────────────────────────────
setup_logging()
logger = logging.getLogger(__name__)


# ── Application Lifespan ─────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    logger.info(
        "service_starting app=%s version=%s env=%s",
        APP_NAME, APP_VERSION, ENVIRONMENT,
    )
    Base.metadata.create_all(bind=engine)
    logger.info("database_ready tables_verified=true")
    yield
    # Shutdown
    logger.info("service_stopping app=%s", APP_NAME)


# ── Create Application ───────────────────────────────────────
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="A production-ready task management API with CI/CD and monitoring.",
    debug=DEBUG,
    lifespan=lifespan,
)

# ── CORS Middleware ───────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request Logging Middleware ────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every incoming request with method, path, status, and duration."""
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(
        "request method=%s path=%s status=%d duration=%.3fs",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )
    return response


# ── Register Routes ──────────────────────────────────────────
app.include_router(health.router)
app.include_router(tasks.router)


# ── Root Endpoint ────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    """Root endpoint — returns service info."""
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "docs": "/docs",
    }
