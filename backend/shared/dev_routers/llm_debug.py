"""
LLM Debug Router for Four-Engine Architecture.

Provides debug endpoints for LLM tiered routing, model registry,
and orchestrator functionality in the development dashboard.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from llm_engine.model_registry import get_model_registry_service
from calculation_engine.schemas.llm_tiers import LLMTier

router = APIRouter(prefix="/debug/llm", tags=["llm-debug"])


class TierSelectionTestRequest(BaseModel):
    """Request model for tier selection testing."""
    tier: str  # "ROUTER", "NARRATOR", or "THINKER"


class TierSelectionTestResponse(BaseModel):
    """Response model for tier selection testing."""
    selected_model: Optional[Dict[str, Any]] = None
    selection_score: Optional[float] = None
    reasoning: Optional[str] = None
    alternatives: Optional[List[Dict[str, Any]]] = None


@router.get("/tier-candidates")
async def get_tier_candidates() -> Dict[str, Any]:
    """
    Get available models for each intelligence tier.

    Returns the top candidates for ROUTER, NARRATOR, and THINKER tiers
    based on current model registry and selection criteria.
    """
    try:
        registry_service = get_model_registry_service()
        registry = await registry_service.get_registry()

        result = {
            "router": [],
            "narrator": [],
            "thinker": []
        }

        # Get models for each tier
        for tier in LLMTier:
            tier_models = registry.get_models_for_tier(tier)
            # Convert to dict format for JSON response
            result[tier.value.lower()] = [
                {
                    "id": model.id,
                    "name": model.name,
                    "average_cost": model.average_cost,
                    "context_length": model.context_length,
                    "capabilities": {
                        "reasoning_score": model.capabilities.reasoning_score,
                        "fluency_score": model.capabilities.fluency_score,
                        "speed_score": model.capabilities.speed_score
                    }
                }
                for model in tier_models[:10]  # Top 10 candidates
            ]

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tier candidates: {str(e)}")


@router.post("/test-tier-selection")
async def test_tier_selection(request: TierSelectionTestRequest) -> TierSelectionTestResponse:
    """
    Test model selection for a specific intelligence tier.

    This endpoint simulates the model selection process and returns
    detailed information about which model would be chosen and why.
    """
    try:
        # Validate tier
        try:
            tier = LLMTier(request.tier)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid tier: {request.tier}")

        registry_service = get_model_registry_service()
        selection_result = await registry_service.select_model_for_tier(tier)

        if not selection_result:
            return TierSelectionTestResponse(
                reasoning=f"No suitable model found for tier {tier.value}"
            )

        # Convert to response format
        return TierSelectionTestResponse(
            selected_model={
                "id": selection_result.selected_model.id,
                "name": selection_result.selected_model.name,
                "average_cost": selection_result.selected_model.average_cost,
                "context_length": selection_result.selected_model.context_length,
                "capabilities": {
                    "reasoning_score": selection_result.selected_model.capabilities.reasoning_score,
                    "fluency_score": selection_result.selected_model.capabilities.fluency_score,
                    "speed_score": selection_result.selected_model.capabilities.speed_score
                }
            },
            selection_score=selection_result.selection_score,
            reasoning=_get_selection_reasoning(tier, selection_result),
            alternatives=[
                {
                    "id": alt.id,
                    "name": alt.name,
                    "average_cost": alt.average_cost
                }
                for alt in selection_result.alternatives
            ]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tier selection test failed: {str(e)}")


def _get_selection_reasoning(tier: LLMTier, result: Any) -> str:
    """Generate human-readable reasoning for model selection."""
    if tier == LLMTier.ROUTER:
        return f"Selected for ROUTER tier: Lowest cost (${result.selected_model.average_cost:.4f}/token) with good speed score ({result.selected_model.capabilities.speed_score}/100)"
    elif tier == LLMTier.NARRATOR:
        return f"Selected for NARRATOR tier: Balanced cost-quality ratio with high fluency score ({result.selected_model.capabilities.fluency_score}/100)"
    elif tier == LLMTier.THINKER:
        return f"Selected for THINKER tier: Highest reasoning capability ({result.selected_model.capabilities.reasoning_score}/100) with large context ({result.selected_model.context_length} tokens)"
    else:
        return "Selected based on tier-specific criteria"


@router.get("/registry-status")
async def get_registry_status() -> Dict[str, Any]:
    """
    Get current model registry status.

    Returns information about registry health, model counts,
    and cache status for debugging purposes.
    """
    try:
        registry_service = get_model_registry_service()
        status = await registry_service.get_registry_status()

        return {
            "total_models": status.total_models,
            "models_by_tier": status.models_by_tier,
            "last_updated": status.last_updated.isoformat() if status.last_updated else None,
            "is_stale": status.is_stale,
            "cache_file_exists": status.cache_file_exists,
            "registry_service_available": True
        }

    except Exception as e:
        return {
            "error": str(e),
            "registry_service_available": False,
            "total_models": 0,
            "models_by_tier": {},
            "last_updated": None,
            "is_stale": True,
            "cache_file_exists": False
        }


@router.post("/refresh-registry")
async def refresh_registry() -> Dict[str, Any]:
    """
    Force refresh the model registry from OpenRouter API.

    This endpoint triggers an immediate refresh of the model catalog,
    bypassing the cache TTL. Useful for testing registry updates.
    """
    try:
        registry_service = get_model_registry_service()
        await registry_service.force_refresh()

        # Get updated status
        status = await registry_service.get_registry_status()

        return {
            "success": True,
            "message": "Registry refreshed successfully",
            "total_models": status.total_models,
            "models_by_tier": status.models_by_tier,
            "last_updated": status.last_updated.isoformat() if status.last_updated else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registry refresh failed: {str(e)}")


@router.get("/health")
async def get_llm_health() -> Dict[str, Any]:
    """
    Get LLM system health status.

    Returns connection status, model availability, and performance metrics.
    This is used by the development dashboard for LLM health monitoring.
    """
    try:
        registry_service = get_model_registry_service()
        registry = await registry_service.get_registry()
        status = await registry_service.get_registry_status()

        # Basic health check
        return {
            "status": "healthy" if not status.is_stale and status.total_models > 0 else "unhealthy",
            "connection": {
                "models_available": status.total_models,
                "registry_initialized": True,
                "response_time_ms": None  # Could be added with actual timing
            },
            "usage": {
                "total_requests": 0,  # Would need actual tracking
                "uptime_percentage": 100.0,  # Placeholder
                "error_rate": 0.0  # Placeholder
            },
            "models": {
                "total": status.total_models,
                "by_tier": status.models_by_tier
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "connection": {
                "models_available": 0,
                "registry_initialized": False,
                "response_time_ms": None
            },
            "usage": {
                "total_requests": 0,
                "uptime_percentage": 0.0,
                "error_rate": 100.0
            },
            "models": {
                "total": 0,
                "by_tier": {"router": 0, "narrator": 0, "thinker": 0}
            }
        }
