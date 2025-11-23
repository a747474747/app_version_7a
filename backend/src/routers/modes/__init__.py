"""
Modes API router.

This module provides endpoints for different interaction modes (fact-check, strategy, advice, etc.).
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Body, Path
from pydantic import BaseModel

from auth import get_current_user, ClerkUser
# Temporarily disable LLM imports for testing
# from llm_engine.intent_recognition import IntentRecognitionEngine, IntentRecognitionResult
# from llm_engine.state_hydration import StateHydrationEngine, StateHydrationResult
# from llm_engine.narrative_generation import NarrativeGenerationEngine, NarrativeGenerationResult
# from llm_engine.privacy_filter import scrub_pii
from calculation_engine import run_calculation, CalculationResult
from calculation_engine.schemas.calculation import CalculationState
# TODO: Import other CAL functions as needed
# from ...services.scenario_service import get_scenario_service # Will need this later

router = APIRouter()

# Temporarily disable LLM engine initialization for testing
# intent_engine = IntentRecognitionEngine()
# state_engine = StateHydrationEngine()
# narrative_engine = NarrativeGenerationEngine()


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

    TEMPORARY: Simplified version for testing routing without LLM dependencies.
    """
    question = request.parameters.get("question", "")

    # Simple mock response for testing
    if "tax" in question.lower():
        intent = "check_tax_liability"
        response = "Based on your financial data, your estimated tax liability is $15,230 for the current financial year. This includes PAYG tax of $12,450 and Medicare levy of $2,780."
        calc_results = {"tax_liability": 15230.00}
    elif "wealth" in question.lower() or "net worth" in question.lower():
        intent = "check_net_wealth"
        response = "Your current net wealth is calculated at $450,750, consisting of $520,000 in assets minus $69,250 in liabilities."
        calc_results = {"net_wealth": 450750.00}
    else:
        intent = "general_inquiry"
        response = f"I understand you're asking about: '{question}'. For specific financial calculations, please ask about tax liability or net wealth."
        calc_results = {}

    # Mock trace log
    trace_log = [{
        "calc_id": "CAL-DEMO-001",
        "entity_id": "demo_entity",
        "field": "demo_calculation",
        "explanation": "Demo calculation for testing",
        "metadata": {"method": "mock_data"}
    }]

    return ModeExecutionResult(
        mode="fact_check",
        scenario_id=request.scenario_id,
        result={
            "status": "success",
            "intent": intent,
            "data": calc_results,
            "trace_log": trace_log,
            "narrative_metadata": {
                "key_points": ["Demo response for testing"],
                "citations": ["Test data"],
                "confidence_score": 0.95
            }
        },
        explanation=response
    )
