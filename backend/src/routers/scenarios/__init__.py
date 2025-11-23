"""
Scenarios API router.

This module provides endpoints for managing financial scenarios.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from auth import get_current_user, ClerkUser
from services.scenario_service import get_scenario_service
from config import get_db

router = APIRouter()


@router.post("/")
async def create_scenario(
    request: dict,  # TODO: Add proper Pydantic schema
    user: ClerkUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new scenario.

    This endpoint creates a new financial scenario for the authenticated user.
    """
    service = get_scenario_service(db)

    # Find user profile
    # TODO: Implement user profile lookup
    user_profile_id = 1  # Placeholder

    scenario = service.create_scenario(
        user_profile_id=user_profile_id,
        name=request.get("name", "New Scenario"),
        description=request.get("description"),
        created_by_clerk_id=user.clerk_id
    )

    return {
        "scenario_id": scenario.scenario_id,
        "name": scenario.name,
        "description": scenario.description,
        "status": scenario.status,
        "created_at": scenario.created_at.isoformat()
    }


@router.get("/")
async def list_scenarios(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None,
    user: ClerkUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List user's scenarios.

    Returns a paginated list of scenarios belonging to the authenticated user.
    """
    service = get_scenario_service(db)

    # Find user profile
    # TODO: Implement user profile lookup
    user_profile_id = 1  # Placeholder

    scenarios = service.get_scenarios_by_user(
        user_profile_id=user_profile_id,
        status=status,
        limit=limit,
        offset=offset
    )

    return {
        "scenarios": [
            {
                "scenario_id": s.scenario_id,
                "name": s.name,
                "description": s.description,
                "status": s.status,
                "updated_at": s.updated_at.isoformat()
            }
            for s in scenarios
        ],
        "total": service.get_scenario_count(user_profile_id, status),
        "limit": limit,
        "offset": offset
    }


@router.get("/{scenario_id}")
async def get_scenario(
    scenario_id: str,
    user: ClerkUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get scenario details.

    Returns complete information about a specific scenario.
    """
    service = get_scenario_service(db)
    scenario = service.get_scenario_by_id(scenario_id)

    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # TODO: Check ownership permissions

    return {
        "scenario_id": scenario.scenario_id,
        "name": scenario.name,
        "description": scenario.description,
        "status": scenario.status,
        "version": scenario.version,
        "mode": scenario.mode,
        "calculation_state": scenario.calculation_state,
        "projection_output": scenario.projection_output,
        "last_calculated_at": scenario.last_calculated_at,
        "tags": scenario.tags or [],
        "created_at": scenario.created_at.isoformat(),
        "updated_at": scenario.updated_at.isoformat()
    }


@router.put("/{scenario_id}")
async def update_scenario(
    scenario_id: str,
    updates: dict,  # TODO: Add proper Pydantic schema
    user: ClerkUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update scenario.

    Updates scenario properties and metadata.
    """
    service = get_scenario_service(db)
    scenario = service.update_scenario(
        scenario_id=scenario_id,
        updates=updates,
        updated_by_clerk_id=user.clerk_id
    )

    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return {
        "scenario_id": scenario.scenario_id,
        "name": scenario.name,
        "description": scenario.description,
        "status": scenario.status,
        "updated_at": scenario.updated_at.isoformat()
    }


@router.delete("/{scenario_id}")
async def delete_scenario(
    scenario_id: str,
    user: ClerkUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete scenario.

    Soft deletes a scenario (marks as deleted).
    """
    service = get_scenario_service(db)
    deleted = service.delete_scenario(
        scenario_id=scenario_id,
        deleted_by_clerk_id=user.clerk_id
    )

    if not deleted:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return {"message": "Scenario deleted successfully"}


@router.post("/{scenario_id}/run")
async def run_scenario(
    scenario_id: str,
    user: ClerkUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Run scenario calculations.

    Executes the calculation engine on the scenario and stores results.
    """
    # TODO: Implement scenario execution
    return {"message": "Scenario execution not yet implemented"}


@router.get("/{scenario_id}/results")
async def get_scenario_results(
    scenario_id: str,
    user: ClerkUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get scenario calculation results.

    Returns the projection output and calculation results.
    """
    service = get_scenario_service(db)
    scenario = service.get_scenario_by_id(scenario_id)

    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return {
        "scenario_id": scenario.scenario_id,
        "projection_output": scenario.projection_output,
        "last_calculated_at": scenario.last_calculated_at
    }
