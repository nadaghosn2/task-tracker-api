# Pydantic models used for API response validation and serialization.

from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response shape returned by GET /health."""
    status: str
    timestamp: datetime