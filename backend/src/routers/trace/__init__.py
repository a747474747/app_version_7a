"""
Trace API router.

This module provides endpoints for audit trail and calculation traceability.
"""

from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user, ClerkUser

router = APIRouter()


@router.get("/{scenario_id}")
async def get_scenario_trace(
    scenario_id: str,
    user: ClerkUser = Depends(get_current_user)
):
    """
    Get scenario audit trail.

    Returns the complete trace log for a scenario's calculations and decisions.
    """
    # TODO: Implement trace retrieval
    return {"message": f"Trace retrieval for scenario {scenario_id} not yet implemented"}
