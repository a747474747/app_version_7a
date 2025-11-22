"""
Strategies API router.

This module provides endpoints for strategy optimization and management.
"""

from fastapi import APIRouter, Depends, HTTPException
from ..auth import get_current_user, ClerkUser

router = APIRouter()


@router.post("/optimize")
async def optimize_strategy(
    request: dict,  # TODO: Add proper Pydantic schema
    user: ClerkUser = Depends(get_current_user)
):
    """
    Run strategy optimization.

    Uses the Strategy Engine to optimize financial strategies.
    """
    # TODO: Implement strategy optimization
    return {"message": "Strategy optimization not yet implemented"}


@router.get("/templates")
async def list_strategy_templates(
    user: ClerkUser = Depends(get_current_user)
):
    """
    List available strategy templates.

    Returns predefined strategy templates for common use cases.
    """
    # TODO: Implement strategy templates
    return {
        "templates": [
            {
                "id": "debt_reduction",
                "name": "Debt Reduction Strategy",
                "domain": "DEBT",
                "description": "Optimized approach to debt elimination"
            },
            {
                "id": "super_optimization",
                "name": "Superannuation Optimization",
                "domain": "SUPER",
                "description": "Maximize retirement savings efficiency"
            }
        ]
    }
