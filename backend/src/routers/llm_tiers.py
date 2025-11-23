"""
LLM Tier Management Router

Provides endpoints for the LLM tiered routing strategy,
including model selection and tier information for the dev dashboard.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import sys
import os

# Add the llm_engine path to sys.path so we can import the router
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'llm_engine'))

try:
    from model_router import (
        get_tier_candidates_for_dashboard,
        test_tier_selection_api,
        get_model_router
    )
except ImportError as e:
    print(f"Warning: Could not import model_router: {e}")
    # Fallback functions if import fails
    def get_tier_candidates_for_dashboard():
        return {"error": "Model router not available"}

    def test_tier_selection_api(tier: str):
        return {"error": "Model router not available"}

    def get_model_router():
        return None

router = APIRouter(prefix="/llm-tiers", tags=["llm-tiers"])

@router.get("/candidates")
async def get_tier_candidates():
    """
    Get all tier candidates for the dev dashboard.

    Returns tier-organized model information with performance data.
    """
    try:
        return get_tier_candidates_for_dashboard()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load tier candidates: {str(e)}")

@router.post("/test-selection")
async def test_tier_selection(request: Dict[str, str]):
    """
    Test tier selection for a specific tier.

    Args:
        request: Dictionary with 'tier' key (ROUTER, NARRATOR, THINKER)

    Returns:
        Selected model information and selection criteria
    """
    try:
        tier = request.get("tier", "").upper()
        if tier not in ["ROUTER", "NARRATOR", "THINKER"]:
            raise HTTPException(status_code=400, detail="Invalid tier. Must be ROUTER, NARRATOR, or THINKER")

        result = test_tier_selection_api(tier)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tier selection test failed: {str(e)}")

@router.get("/stats")
async def get_tier_stats():
    """
    Get statistics for all tiers.

    Returns performance metrics and model counts for each tier.
    """
    try:
        router = get_model_router()
        if router:
            return router.get_all_tier_stats()
        else:
            return {"error": "Model router not available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tier stats: {str(e)}")

@router.get("/route-task/{task_type}")
async def route_task(task_type: str):
    """
    Route a task to the appropriate model based on task type.

    Args:
        task_type: Type of task (intent_recognition, conversation, strategy, etc.)

    Returns:
        Selected model information for the task
    """
    try:
        from model_router import route_task_to_model

        selection = route_task_to_model(task_type)
        if selection:
            return {
                "task_type": task_type,
                "selected_model": {
                    "id": selection.model_id,
                    "name": selection.name,
                    "tier": selection.tier
                },
                "performance": {
                    "response_time_seconds": selection.response_time_seconds,
                    "tokens_used": selection.tokens_used,
                    "pricing_input": selection.pricing_input
                }
            }
        else:
            raise HTTPException(status_code=404, detail=f"No suitable model found for task type: {task_type}")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task routing failed: {str(e)}")

@router.get("/tier-mapping")
async def get_full_tier_mapping():
    """
    Get the complete tier mapping data.

    Returns the full JSON structure used by the model router.
    """
    try:
        router = get_model_router()
        if router and hasattr(router, 'tier_data'):
            return router.tier_data
        else:
            return {"error": "Tier mapping not available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tier mapping: {str(e)}")
