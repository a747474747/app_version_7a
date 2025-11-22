"""
QA API router.

This module provides endpoints for quality assurance and testing.
"""

from fastapi import APIRouter, Depends
from ..auth import get_current_user, ClerkUser

router = APIRouter()


@router.post("/run-golden-suite")
async def run_golden_suite(
    user: ClerkUser = Depends(get_current_user)
):
    """
    Run golden test suite.

    Executes the complete suite of golden tests for calculation accuracy.
    """
    # TODO: Implement golden test suite
    return {"message": "Golden test suite not yet implemented"}


@router.post("/run-calculation")
async def run_calculation_test(
    request: dict,  # TODO: Add proper Pydantic schema
    user: ClerkUser = Depends(get_current_user)
):
    """
    Run specific calculation test.

    Tests a specific CAL-* calculation with provided inputs.
    """
    # TODO: Implement calculation testing
    return {"message": "Calculation testing not yet implemented"}
