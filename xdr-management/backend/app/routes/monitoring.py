from fastapi import APIRouter, Depends
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any

from ..core.logging import metrics
from ..core.security import require_admin

router = APIRouter(prefix="/api/monitoring", tags=["Monitoring"])


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    uptime_seconds: float


class MetricsResponse(BaseModel):
    requests_total: int
    requests_by_endpoint: Dict[str, int]
    requests_by_status: Dict[str, int]
    avg_response_time_ms: float
    errors_total: int
    websocket_connections: int


# Track startup time
_startup_time = datetime.utcnow()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = (datetime.utcnow() - _startup_time).total_seconds()

    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        version="1.0.0",
        uptime_seconds=round(uptime, 2)
    )


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(current_user: dict = Depends(require_admin)):
    """Get application metrics (admin only)"""
    return MetricsResponse(**metrics.get_metrics())


@router.post("/metrics/reset")
async def reset_metrics(current_user: dict = Depends(require_admin)):
    """Reset application metrics (admin only)"""
    metrics.reset()
    return {"message": "Metrics reset successfully"}


@router.get("/ready")
async def readiness_check():
    """Readiness probe for Kubernetes"""
    # Add any readiness checks here (e.g., database connection)
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """Liveness probe for Kubernetes"""
    return {"status": "alive"}
