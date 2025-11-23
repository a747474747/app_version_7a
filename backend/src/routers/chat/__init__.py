"""
Chat API router.

This module provides endpoints for conversational AI interactions.
"""

from fastapi import APIRouter, Depends
from auth import get_current_user, ClerkUser

router = APIRouter()


@router.post("/process")
async def process_chat(
    request: dict,  # TODO: Add proper Pydantic schema
    user: ClerkUser = Depends(get_current_user)
):
    """
    Process chat message.

    Handles conversational interactions with the LLM Orchestrator.
    """
    # TODO: Implement chat processing
    return {"message": "Chat processing not yet implemented"}
