"""
Advice API router.

This module provides endpoints for regulatory compliance checking and advice generation.
"""

from fastapi import APIRouter, Depends, HTTPException
from ..auth import get_current_user, ClerkUser

router = APIRouter()


@router.post("/evaluate")
async def evaluate_advice(
    request: dict,  # TODO: Add proper Pydantic schema
    user: ClerkUser = Depends(get_current_user)
):
    """
    Evaluate advice for compliance.

    Runs the Advice Engine to check regulatory compliance and provide advice validation.
    """
    # TODO: Implement advice evaluation
    return {"message": "Advice evaluation not yet implemented"}
