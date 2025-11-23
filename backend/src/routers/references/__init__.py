"""
References API router.

This module provides endpoints for regulatory reference materials and documentation.
"""

from fastapi import APIRouter, Depends
from auth import get_current_user, ClerkUser

router = APIRouter()


@router.get("/search")
async def search_references(
    query: str,
    user: ClerkUser = Depends(get_current_user)
):
    """
    Search reference materials.

    Searches regulatory documents, guidelines, and reference materials.
    """
    # TODO: Implement reference search
    return {"message": "Reference search not yet implemented", "query": query}
