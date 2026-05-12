"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


# ── Task Schemas ──────────────────────────────────────────────

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=255, examples=["Buy groceries"])
    description: Optional[str] = Field(
        None, max_length=1000, examples=["Milk, eggs, bread"]
    )
    completed: bool = False


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Schema for task API responses."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Health Schemas ────────────────────────────────────────────

class HealthResponse(BaseModel):
    """Schema for the /health endpoint."""
    status: str
    timestamp: datetime
    version: str
    environment: str
