"""
Application configuration.
Loads settings from environment variables using python-decouple.
"""

from decouple import config

# --- Database ---
DATABASE_URL = config("DATABASE_URL", default="sqlite:///./dev.db")

# Fix for platforms that use 'postgres://' instead of 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# --- Application ---
SECRET_KEY = config("SECRET_KEY", default="dev-secret-key-change-in-production")
ENVIRONMENT = config("ENVIRONMENT", default="development")
DEBUG = config("DEBUG", default=True, cast=bool)

# --- Metadata ---
APP_NAME = "Task Management API"
APP_VERSION = "1.0.0"
