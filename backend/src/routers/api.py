"""
Main API router for Four-Engine System Architecture.

This module provides the main API router with version 1 endpoints,
organized by domain and functionality.
"""

from fastapi import APIRouter, Depends
from ..auth import get_current_user, ClerkUser

router = APIRouter()


@router.get("/")
async def api_root():
    """API root endpoint."""
    return {
        "message": "Four-Engine System Architecture API v1",
        "version": "1.0.0",
        "docs": "/docs"
    }


@router.get("/auth/test")
async def auth_test(user: ClerkUser = Depends(get_current_user)):
    """Test endpoint to verify authentication."""
    return {
        "message": "Authentication successful",
        "user": {
            "clerk_id": user.clerk_id,
            "email": user.email,
            "role": user.role
        }
    }


# Include domain-specific routers
from .scenarios import router as scenarios_router
from .strategies import router as strategies_router
from .advice import router as advice_router
from .modes import router as modes_router
from .chat import router as chat_router
from .trace import router as trace_router
from .references import router as references_router
from .qa import router as qa_router

router.include_router(scenarios_router, prefix="/scenarios", tags=["Scenarios"])
router.include_router(strategies_router, prefix="/strategies", tags=["Strategies"])
router.include_router(advice_router, prefix="/advice", tags=["Advice"])
router.include_router(modes_router, prefix="/modes", tags=["Modes"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])
router.include_router(trace_router, prefix="/trace", tags=["Trace"])
router.include_router(references_router, prefix="/references", tags=["References"])
router.include_router(qa_router, prefix="/qa", tags=["QA"])
