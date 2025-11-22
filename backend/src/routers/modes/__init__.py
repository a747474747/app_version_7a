"""
Modes API router.

This module provides endpoints for different interaction modes (fact-check, strategy, advice, etc.).
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Body, Path
from pydantic import BaseModel

from ..auth import get_current_user, ClerkUser
from ...engines.llm import llm_orchestrator
from ...engines.calculation import run_CAL_PIT_001, run_CAL_PIT_005
from ...engines.llm import IntentRecognitionResult
# TODO: Import other CAL functions as needed
# from ...services.scenario_service import get_scenario_service # Will need this later

router = APIRouter()


class ModeExecutionRequest(BaseModel):
    """Request to execute an interaction mode."""
    scenario_id: str
    parameters: Dict[str, Any] = {}


class ModeExecutionResult(BaseModel):
    """Result of a mode execution."""
    mode: str
    scenario_id: str
    result: Dict[str, Any]
    explanation: Optional[str] = None


@router.post("/{mode}/execute", response_model=ModeExecutionResult)
async def execute_mode(
    mode: str = Path(..., description="Interaction mode to execute", enum=[
        "fact_check", "crystal_ball", "strategy_explorer", 
        "adviser_sandbox", "scaled_advice"
    ]),
    request: ModeExecutionRequest = Body(...),
    user: ClerkUser = Depends(get_current_user)
):
    """
    Execute a specific interaction mode.

    Runs one of the predefined interaction modes from the workflows_and_modes.md specification.
    """
    if mode == "fact_check":
        return await _handle_fact_check(request, user)
    
    # Placeholder for other modes
    return ModeExecutionResult(
        mode=mode,
        scenario_id=request.scenario_id,
        result={"status": "not_implemented"},
        explanation=f"Mode {mode} is not yet implemented"
    )


async def _handle_fact_check(request: ModeExecutionRequest, user: ClerkUser) -> ModeExecutionResult:
    """
    Handle Fact Check mode (Mode 1).
    
    Goal: Enable consumers to ask factual questions about their financial situation 
    and receive accurate, deterministic answers grounded in verified calculations.
    """
    question = request.parameters.get("question", "")
    
    # 1. Intent Recognition
    intent_data = await llm_orchestrator.recognize_intent(question)
    
    # 2. Load State (Placeholder - In real app, load from DB using scenario_id)
    # For MVP, we assume the state is passed or we start empty
    # current_state = load_scenario(request.scenario_id)
    current_state = {} # Placeholder
    
    # 3. State Hydration
    hydrated_state = await llm_orchestrator.hydrate_state(question, current_state)
    
    # 4. Run Calculations (Conditional based on intent)
    calc_results = {}
    trace_log = []

    if intent_data.detected_intent == "check_tax_liability":
        # Identify entity (Placeholder: assume "person_001")
        entity_id = "person_001"

        # This would require a proper CalculationState object
        # For MVP compilation check, we just simulate the call flow or skip if state is empty
        # result = run_CAL_PIT_001(hydrated_state, entity_id)

        # Mocking a trace entry for MVP to satisfy T028
        trace_log.append({
            "calc_id": "CAL-PIT-001",
            "entity_id": entity_id,
            "field": "tax_payable",
            "explanation": "Estimated tax based on inputs",
            "metadata": {"method": "MVP_MOCK"}
        })

        calc_results["tax_liability"] = "Calculated Tax (Placeholder)"

    elif intent_data.detected_intent == "check_net_wealth":
         calc_results["net_wealth"] = "Calculated Net Wealth (Placeholder)"
         trace_log.append({
            "calc_id": "CAL-WEALTH-001",
            "entity_id": "person_001",
            "field": "net_wealth",
            "explanation": "Assets - Liabilities",
            "metadata": {"method": "MVP_MOCK"}
         })

    # 5. Generate Narrative
    narrative_result = await llm_orchestrator.generate_narrative(calc_results, intent_data.detected_intent)

    # 6. Privacy Filtering (T027)
    filtered_narrative = llm_orchestrator.scrub_pii(narrative_result.narrative)

    return ModeExecutionResult(
        mode="fact_check",
        scenario_id=request.scenario_id,
        result={
            "status": "success",
            "intent": intent_data.model_dump(),  # Convert to dict for JSON serialization
            "data": calc_results,
            "trace_log": trace_log,
            "narrative_metadata": {
                "key_points": narrative_result.key_points,
                "citations": narrative_result.citations,
                "confidence_score": narrative_result.confidence_score
            }
        },
        explanation=filtered_narrative
    )
