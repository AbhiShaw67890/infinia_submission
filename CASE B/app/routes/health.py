"""
Health and metrics endpoints.
Used for monitoring, uptime checks, and operational visibility.
"""

import time
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.config import APP_VERSION, ENVIRONMENT
from app.models import Task

router = APIRouter(tags=["Health"])
logger = logging.getLogger(__name__)

# Track application start time
_start_time = time.time()


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health endpoint for monitoring services (UptimeRobot, Render, etc.).
    Returns OK if the app and database are reachable.
    """
    # Verify database connectivity
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
        logger.error("health_check database_unreachable")

    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "database": db_status,
    }


@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """
    Basic application metrics.
    Provides operational visibility into the service.
    """
    try:
        total = db.query(Task).count()
        completed = db.query(Task).filter(Task.completed.is_(True)).count()
        pending = total - completed
    except Exception:
        total = completed = pending = -1

    return {
        "uptime_seconds": round(time.time() - _start_time, 2),
        "tasks": {
            "total": total,
            "completed": completed,
            "pending": pending,
        },
    }
