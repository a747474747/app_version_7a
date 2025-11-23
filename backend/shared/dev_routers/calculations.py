"""
Calculations API router for development - bypasses authentication.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import json

from calculation_engine.registry import run_calculation, get_registered_calculations
from calculation_engine.schemas.calculation import CalculationState
from calculation_engine.schemas.orchestration import TraceEntry
from dev_routers.debug import add_trace_entry


router = APIRouter()


class CalculationRequest(BaseModel):
    """Request to run a single calculation."""
    calc_id: str = Field(..., description="Calculation ID (e.g., CAL-PIT-001)")
    entity_id: str = Field(..., description="Entity identifier")
    year_index: int = Field(default=0, description="Year index for projections")
    state_data: Dict[str, Any] = Field(..., description="CalculationState data as dictionary")


class CalculationResponse(BaseModel):
    """Response from a calculation execution."""
    calc_id: str
    entity_id: str
    year_index: int
    success: bool
    value: Optional[float] = None
    trace_entries: List[TraceEntry] = []
    error_message: Optional[str] = None
    execution_time_ms: Optional[float] = None
    timestamp: str


class BatchCalculationRequest(BaseModel):
    """Request to run multiple calculations."""
    calculations: List[CalculationRequest] = Field(..., description="List of calculations to run")
    continue_on_error: bool = Field(default=False, description="Continue processing if a calculation fails")


class BatchCalculationResponse(BaseModel):
    """Response from batch calculation execution."""
    total_calculations: int
    successful_calculations: int
    failed_calculations: int
    results: List[CalculationResponse]
    errors: List[Dict[str, Any]] = []
    total_execution_time_ms: float
    timestamp: str


class AvailableCalculationsResponse(BaseModel):
    """Response listing available calculations."""
    calculations: Dict[str, Dict[str, Any]]
    total_count: int
    domains: Dict[str, List[str]]


def dict_to_calculation_state(state_data: Dict[str, Any]) -> CalculationState:
    """
    Convert dictionary to CalculationState.
    """
    try:
        return CalculationState(
            global_context=state_data.get("global_context", {}),
            entities=state_data.get("entities", {}),
            asset_context=state_data.get("asset_context", {}),
            cashflow_context=state_data.get("cashflow_context", {}),
            intermediates={"tax_results": {}, "trace_log": []}
        )
    except Exception as e:
        raise ValueError(f"Invalid CalculationState data: {str(e)}")


@router.get("/available", response_model=AvailableCalculationsResponse)
async def get_available_calculations():
    """
    Get list of available calculations.
    """
    try:
        registered = get_registered_calculations()

        # Group by domain
        domains = {}
        calculations = {}

        for calc_id, func in registered.items():
            # Extract domain from CAL-DOMAIN-NNN format
            parts = calc_id.split('-')
            if len(parts) >= 2:
                domain = parts[1]
                if domain not in domains:
                    domains[domain] = []
                domains[domain].append(calc_id)

            # Get function metadata
            calculations[calc_id] = {
                "function_name": func.__name__,
                "module": func.__module__,
                "description": getattr(func, "__doc__", "").strip().split('\n')[0] if func.__doc__ else ""
            }

        return AvailableCalculationsResponse(
            calculations=calculations,
            total_count=len(registered),
            domains=domains
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve available calculations: {str(e)}"
        )


@router.post("/run", response_model=CalculationResponse)
async def run_single_calculation(
    request: CalculationRequest,
    background_tasks: BackgroundTasks
):
    """
    Run a single CAL-* calculation function.
    """
    start_time = datetime.utcnow()

    try:
        # Validate calc_id exists
        registered = get_registered_calculations()
        if request.calc_id not in registered:
            available_ids = list(registered.keys())
            raise HTTPException(
                status_code=400,
                detail=f"Calculation '{request.calc_id}' not found. Available: {available_ids}"
            )

        # Convert state data to CalculationState
        try:
            state = dict_to_calculation_state(request.state_data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Run the calculation
        result = run_calculation(
            request.calc_id,
            state,
            request.entity_id,
            request.year_index
        )

        execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000

        # Add trace entries to debug log in background
        if result.trace_entries:
            for trace_entry in result.trace_entries:
                background_tasks.add_task(add_trace_entry, trace_entry)

        return CalculationResponse(
            calc_id=request.calc_id,
            entity_id=request.entity_id,
            year_index=request.year_index,
            success=result.success,
            value=float(result.value) if result.value is not None else None,
            trace_entries=result.trace_entries,
            error_message=result.error_message,
            execution_time_ms=execution_time,
            timestamp=datetime.utcnow().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        return CalculationResponse(
            calc_id=request.calc_id,
            entity_id=request.entity_id,
            year_index=request.year_index,
            success=False,
            error_message=f"Unexpected error: {str(e)}",
            execution_time_ms=execution_time,
            timestamp=datetime.utcnow().isoformat()
        )


@router.post("/run-batch", response_model=BatchCalculationResponse)
async def run_batch_calculations(
    request: BatchCalculationRequest,
    background_tasks: BackgroundTasks
):
    """
    Run multiple CAL-* calculations in batch.
    """
    start_time = datetime.utcnow()
    results = []
    errors = []

    for i, calc_request in enumerate(request.calculations):
        try:
            # Reuse the single calculation logic
            single_response = await run_single_calculation(calc_request, background_tasks)

            # Convert to dict for batch response
            result_dict = single_response.dict()
            results.append(result_dict)

            if not single_response.success:
                errors.append({
                    "index": i,
                    "calc_id": calc_request.calc_id,
                    "error": single_response.error_message
                })

                if not request.continue_on_error:
                    break

        except Exception as e:
            error_info = {
                "index": i,
                "calc_id": calc_request.calc_id,
                "error": f"Failed to process calculation: {str(e)}"
            }
            errors.append(error_info)
            results.append({
                "calc_id": calc_request.calc_id,
                "entity_id": calc_request.entity_id,
                "year_index": calc_request.year_index,
                "success": False,
                "error_message": str(e),
                "execution_time_ms": None,
                "timestamp": datetime.utcnow().isoformat()
            })

            if not request.continue_on_error:
                break

    total_execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000

    return BatchCalculationResponse(
        total_calculations=len(request.calculations),
        successful_calculations=len([r for r in results if r.get("success", False)]),
        failed_calculations=len([r for r in results if not r.get("success", True)]),
        results=results,
        errors=errors,
        total_execution_time_ms=total_execution_time,
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/run-scenario")
async def run_scenario_calculations(
    scenario_file: str,
    calc_ids: Optional[List[str]] = None,
    background_tasks: BackgroundTasks
):
    """
    Run calculations for a predefined test scenario.
    """
    try:
        # Load scenario file
        scenario_path = f"tests/test_scenarios/{scenario_file}"
        with open(scenario_path, 'r') as f:
            scenario_data = json.load(f)

        # Extract state data
        state_data = {
            "global_context": scenario_data.get("global_context", {}),
            "entities": scenario_data.get("entities", {}),
            "asset_context": scenario_data.get("asset_context", {}),
            "cashflow_context": scenario_data.get("cashflow_context", {})
        }

        # Determine which calculations to run
        if calc_ids:
            calculations_to_run = calc_ids
        else:
            # Run all calculations mentioned in expected_results
            expected_results = scenario_data.get("expected_results", {})
            calculations_to_run = list(expected_results.keys())

        # Create calculation requests
        calc_requests = []
        for calc_id in calculations_to_run:
            # Try to find an entity_id from the scenario
            entity_id = None
            if "entities" in scenario_data:
                entity_id = list(scenario_data["entities"].keys())[0]  # Use first entity

            if entity_id:
                calc_requests.append(CalculationRequest(
                    calc_id=calc_id,
                    entity_id=entity_id,
                    state_data=state_data
                ))

        # Run batch calculations
        batch_request = BatchCalculationRequest(
            calculations=calc_requests,
            continue_on_error=True
        )

        return await run_batch_calculations(batch_request, background_tasks)

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario file '{scenario_file}' not found in test_scenarios/"
        )
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON in scenario file: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run scenario: {str(e)}"
        )
