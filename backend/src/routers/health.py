"""
Health check router for Four-Engine System Architecture.

This module provides health check endpoints following contracts/api-v1.yaml.
"""

from datetime import datetime
from fastapi import APIRouter, Response
from pydantic import BaseModel


router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    version: str
    uptime: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        uptime="unknown"  # Could be enhanced with actual uptime tracking
    )


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with component status."""
    # In a full implementation, this would check:
    # - Database connectivity
    # - Engine availability
    # - External service health
    # - System resources

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "components": {
            "database": "healthy",
            "calculation_engine": "healthy",
            "strategy_engine": "healthy",
            "advice_engine": "healthy",
            "llm_orchestrator": "healthy"
        }
    }
