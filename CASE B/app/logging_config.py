"""
Structured logging configuration.
Outputs JSON-formatted logs for production and human-readable logs for development.
"""

import logging
import sys
from pythonjsonlogger import jsonlogger
from app.config import ENVIRONMENT


def setup_logging() -> None:
    """Configure structured logging for the application."""
    log_level = logging.DEBUG if ENVIRONMENT == "development" else logging.INFO

    # Create formatter
    if ENVIRONMENT == "production":
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Stream handler (stdout)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Suppress noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
