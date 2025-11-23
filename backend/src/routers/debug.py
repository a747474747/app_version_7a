"""
Debug API router for Four-Engine System Architecture.

This module provides debug endpoints for the dev dashboard to visualize
real-time TraceLogs, Engine States, and Rule configurations.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from auth import get_current_user, get_current_user_optional, ClerkUser
from calculation_engine.registry import get_registered_calculations
from services.rule_loader import rule_loader
from calculation_engine.schemas.orchestration import TraceEntry


router = APIRouter()


class EngineState(BaseModel):
    """Engine state information."""
    status: str
    last_run: Optional[str] = None
    function_count: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


class SystemState(BaseModel):
    """Complete system state."""
    calculation_engine: EngineState
    projection_engine: EngineState
    strategy_engine: EngineState
    llm_orchestrator: EngineState
    registry_count: int


class TraceLogResponse(BaseModel):
    """Response containing trace log entries."""
    entries: List[TraceEntry]
    total_count: int
    last_updated: str


class RulesResponse(BaseModel):
    """Response containing loaded rule configurations."""
    rules: Dict[str, Any]
    last_loaded: str
    config_files: List[str]


# In-memory trace log storage for development
# In production, this would be persisted to database
_trace_logs: List[TraceEntry] = []


def add_trace_entry(entry: TraceEntry) -> None:
    """Add a trace entry to the debug log (development only)."""
    global _trace_logs
    _trace_logs.append(entry)
    # Keep only last 1000 entries to prevent memory issues
    if len(_trace_logs) > 1000:
        _trace_logs = _trace_logs[-1000:]


def clear_trace_logs() -> int:
    """Clear all trace logs. Returns number of entries cleared."""
    global _trace_logs
    cleared_count = len(_trace_logs)
    _trace_logs = []
    return cleared_count


@router.get("/trace-logs", response_model=TraceLogResponse)
async def get_trace_logs(
    limit: int = 50,
    user: Optional[ClerkUser] = Depends(get_current_user_optional)
):
    """
    Get recent trace log entries for debugging.

    Args:
        limit: Maximum number of entries to return (default: 50)

    Returns:
        TraceLogResponse with entries and metadata
    """
    try:
        global _trace_logs
        # Return most recent entries first
        entries = _trace_logs[-limit:] if _trace_logs else []

        return TraceLogResponse(
            entries=entries,
            total_count=len(_trace_logs),
            last_updated=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve trace logs: {str(e)}"
        )


@router.delete("/trace-logs")
async def delete_trace_logs(user: Optional[ClerkUser] = Depends(get_current_user_optional)):
    """
    Clear all trace log entries.

    Returns:
        Message indicating number of entries cleared
    """
    try:
        cleared_count = clear_trace_logs()
        return {
            "message": f"Cleared {cleared_count} trace log entries",
            "cleared_count": cleared_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear trace logs: {str(e)}"
        )


@router.get("/engine-states", response_model=SystemState)
async def get_engine_states(user: Optional[ClerkUser] = Depends(get_current_user_optional)):
    """
    Get current state of all four engines.

    Returns:
        SystemState with status of each engine
    """
    try:
        # Get calculation registry info
        registered_calcs = get_registered_calculations()

        # Count functions by domain
        domain_counts = {}
        for cal_id in registered_calcs.keys():
            domain = cal_id.split('-')[1]  # Extract domain from CAL-DOMAIN-NNN
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        return SystemState(
            calculation_engine=EngineState(
                status="healthy",
                function_count=len(registered_calcs),
                details={
                    "registry_functions": len(registered_calcs),
                    "domain_breakdown": domain_counts
                }
            ),
            projection_engine=EngineState(
                status="idle",
                details={"uses_registry": True, "years_projected": 30, "active_scenarios": 0}
            ),
            strategy_engine=EngineState(
                status="idle",
                last_run=None
            ),
            llm_orchestrator=EngineState(
                status="disconnected",
                details={"prompts_loaded": 0}
            ),
            registry_count=len(registered_calcs)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve engine states: {str(e)}"
        )


@router.get("/rules", response_model=RulesResponse)
async def get_rules(user: Optional[ClerkUser] = Depends(get_current_user_optional)):
    """
    Get loaded rule configurations.

    Returns:
        RulesResponse with all rule sets and metadata
    """
    try:
        # Load all rules
        rules = rule_loader.load_rules()

        # Convert dataclasses to dictionaries for JSON response
        rules_dict = {
            "tax": {
                "brackets": [
                    {
                        "min": float(bracket["min"]),
                        "max": float(bracket["max"]) if bracket["max"] else None,
                        "rate": float(bracket["rate"])
                    }
                    for bracket in rules.tax.brackets
                ],
                "medicare_levy_rate": float(rules.tax.medicare_levy_rate),
                "medicare_levy_thresholds": {
                    k: float(v) for k, v in rules.tax.medicare_levy_thresholds.items()
                },
                "lito_parameters": {
                    k: float(v) for k, v in rules.tax.lito_parameters.items()
                }
            },
            "superannuation": {
                "concessional_cap": float(rules.superannuation.concessional_cap),
                "contributions_tax_rate": float(rules.superannuation.contributions_tax_rate),
                "division_293_threshold": float(rules.superannuation.division_293_threshold),
                "division_293_rate": float(rules.superannuation.division_293_rate)
            },
            "capital_gains": {
                "individual_discount_rate": float(rules.capital_gains.individual_discount_rate)
            },
            "property": {
                "marginal_tax_rate": float(rules.property.marginal_tax_rate)
            }
        }

        # Get config file paths
        config_files = []
        config_dir = rule_loader.config_dir
        if config_dir.exists():
            for config_file in config_dir.glob("*"):
                if config_file.is_file() and config_file.suffix in ['.yaml', '.json']:
                    config_files.append(str(config_file.name))

        return RulesResponse(
            rules=rules_dict,
            last_loaded=datetime.utcnow().isoformat(),
            config_files=config_files
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve rules: {str(e)}"
        )


@router.post("/trace-logs/test")
async def add_test_trace_entry(
    calc_id: str = "CAL-PIT-001",
    entity_id: str = "person_1",
    field: str = "tax_payable",
    explanation: str = "Test trace entry for debugging",
    user: Optional[ClerkUser] = Depends(get_current_user_optional)
):
    """
    Add a test trace entry for debugging purposes.

    Args:
        calc_id: Calculation ID (default: CAL-PIT-001)
        entity_id: Entity identifier (default: person_1)
        field: Field being calculated (default: tax_payable)
        explanation: Description of the calculation

    Returns:
        Success message
    """
    try:
        test_entry = TraceEntry(
            calc_id=calc_id,
            entity_id=entity_id,
            field=field,
            explanation=explanation,
            metadata={
                "test_entry": True,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "debug_endpoint"
            }
        )

        add_trace_entry(test_entry)

        return {
            "message": "Test trace entry added successfully",
            "entry": test_entry.dict(),
            "total_entries": len(_trace_logs)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add test trace entry: {str(e)}"
        )
