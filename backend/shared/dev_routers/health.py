"""
Health check router for development - bypasses authentication.
"""

from datetime import datetime
from fastapi import APIRouter
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
        uptime="dev server"
    )


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with component status."""
    from calculation_engine.registry import get_registered_calculations
    from services.rule_loader import rule_loader

    try:
        registered = get_registered_calculations()
        rules = rule_loader.load_rules()

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "components": {
                "calculation_engine": {
                    "status": "healthy",
                    "function_count": len(registered),
                    "functions": list(registered.keys())
                },
                "rule_loader": {
                    "status": "healthy" if rules else "error",
                    "rules_loaded": rules is not None
                },
                "debug_endpoints": "enabled",
                "authentication": "bypassed (dev mode)"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
