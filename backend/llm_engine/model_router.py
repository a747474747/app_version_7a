"""
LLM Model Router - Implements the tiered routing strategy
"""
import json
import logging
from typing import Dict, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ModelSelection:
    """Represents a selected model with its performance data"""
    model_id: str
    name: str
    tier: str
    response_time_seconds: float
    tokens_used: int
    context_length: int
    pricing_input: float
    priority: int

class LLMModelRouter:
    """
    Routes tasks to appropriate LLM models based on the tiered routing strategy.

    This implements the validated tier assignments from our performance testing:
    - ROUTER: Fast intent recognition and classification
    - NARRATOR: Balanced conversational and educational tasks
    - THINKER: Complex reasoning and strategic analysis
    """

    def __init__(self, tier_mapping_path: str = "backend/llm_engine/model_tier_mapping.json"):
        self.tier_mapping_path = tier_mapping_path
        self.tier_data = {}
        self._load_tier_mapping()

    def _load_tier_mapping(self):
        """Load the tier mapping data"""
        try:
            with open(self.tier_mapping_path, 'r') as f:
                self.tier_data = json.load(f)
            logger.info(f"Loaded tier mapping with {len(self.tier_data)} tiers")
        except Exception as e:
            logger.error(f"Failed to load tier mapping: {e}")
            self.tier_data = {}

    def route_task(self, task_type: str) -> Optional[ModelSelection]:
        """
        Route a task to the appropriate model based on task type.

        Args:
            task_type: Type of task (e.g., "intent_recognition", "conversation", "strategy")

        Returns:
            ModelSelection with the chosen model, or None if no suitable model found
        """
        # Map task types to tiers
        task_to_tier = {
            # ROUTER tier tasks
            "intent_recognition": "ROUTER",
            "classification": "ROUTER",
            "fact_extraction": "ROUTER",
            "mode_selection": "ROUTER",
            "fast_query": "ROUTER",

            # NARRATOR tier tasks
            "conversation": "NARRATOR",
            "education": "NARRATOR",
            "narration": "NARRATOR",
            "explanation": "NARRATOR",
            "content_generation": "NARRATOR",
            "chat": "NARRATOR",

            # THINKER tier tasks
            "strategy": "THINKER",
            "compliance": "THINKER",
            "complex_analysis": "THINKER",
            "optimization": "THINKER",
            "reasoning": "THINKER",
            "planning": "THINKER"
        }

        tier = task_to_tier.get(task_type.lower())
        if not tier:
            logger.warning(f"Unknown task type: {task_type}")
            return None

        return self.select_model_for_tier(tier)

    def select_model_for_tier(self, tier: str) -> Optional[ModelSelection]:
        """
        Select the best model for a given tier.

        Args:
            tier: The tier to select from (ROUTER, NARRATOR, THINKER)

        Returns:
            ModelSelection with the highest priority model for the tier
        """
        if tier not in self.tier_data:
            logger.warning(f"Tier not found: {tier}")
            return None

        tier_info = self.tier_data[tier]
        if not tier_info.get("models"):
            logger.warning(f"No models available for tier: {tier}")
            return None

        # Select the model with the highest priority (lowest priority number)
        best_model = min(tier_info["models"], key=lambda m: m.get("priority", 999))

        return ModelSelection(
            model_id=best_model["id"],
            name=best_model["name"],
            tier=tier,
            response_time_seconds=best_model.get("response_time_seconds", 0),
            tokens_used=best_model.get("tokens_used", 0),
            context_length=best_model.get("context_length", 0),
            pricing_input=best_model.get("pricing_input", 0),
            priority=best_model.get("priority", 0)
        )

    def get_tier_stats(self, tier: str) -> Dict:
        """Get statistics for a specific tier"""
        if tier not in self.tier_data:
            return {"error": f"Tier not found: {tier}"}

        tier_info = self.tier_data[tier]
        models = tier_info.get("models", [])

        if not models:
            return {"tier": tier, "model_count": 0, "status": "empty"}

        response_times = [m.get("response_time_seconds", 0) for m in models if m.get("response_time_seconds")]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        return {
            "tier": tier,
            "description": tier_info.get("description", ""),
            "model_count": len(models),
            "avg_response_time": round(avg_response_time, 3),
            "fastest_model": min(models, key=lambda m: m.get("response_time_seconds", 999))["name"] if response_times else "N/A",
            "target_response_time": tier_info.get("target_response_time", "N/A")
        }

    def get_all_tier_stats(self) -> List[Dict]:
        """Get statistics for all tiers"""
        return [self.get_tier_stats(tier) for tier in ["ROUTER", "NARRATOR", "THINKER", "FAILED"]]

# Global router instance
_router_instance = None

def get_model_router() -> LLMModelRouter:
    """Get the global model router instance"""
    global _router_instance
    if _router_instance is None:
        _router_instance = LLMModelRouter()
    return _router_instance

# Convenience functions for the LLM orchestrator
def route_task_to_model(task_type: str) -> Optional[ModelSelection]:
    """Route a task to the appropriate model"""
    router = get_model_router()
    return router.route_task(task_type)

def get_tier_model(tier: str) -> Optional[ModelSelection]:
    """Get the best model for a specific tier"""
    router = get_model_router()
    return router.select_model_for_tier(tier)

# API endpoints for the dev dashboard
def get_tier_candidates_for_dashboard():
    """Get tier candidate data formatted for the dev dashboard"""
    router = get_model_router()

    result = {}
    for tier in ["ROUTER", "NARRATOR", "THINKER", "FAILED"]:
        if tier in router.tier_data and router.tier_data[tier].get("models"):
            result[tier.lower()] = [
                {
                    "id": model["id"],
                    "name": model["name"],
                    "response_time": f"{model.get('response_time_seconds', 'N/A')}s",
                    "tokens": model.get("tokens_used", "N/A"),
                    "cost": f"${model.get('pricing_input', 0):.7f}",
                    "priority": model.get("priority", "N/A")
                }
                for model in router.tier_data[tier]["models"]
            ]
        else:
            result[tier.lower()] = []

    return result

def test_tier_selection_api(tier: str):
    """API endpoint for tier selection testing"""
    router = get_model_router()
    selection = router.select_model_for_tier(tier)

    if selection:
        return {
            "selected_model": {
                "id": selection.model_id,
                "name": selection.name
            },
            "tier": selection.tier,
            "response_time_seconds": selection.response_time_seconds,
            "tokens_used": selection.tokens_used,
            "pricing_input": selection.pricing_input,
            "selection_criteria": router.tier_data.get(tier, {}).get("description", ""),
            "alternatives_count": len(router.tier_data.get(tier, {}).get("models", [])) - 1
        }
    else:
        return {"error": f"No model available for tier {tier}"}

if __name__ == "__main__":
    # Test the router
    router = get_model_router()

    # Test task routing
    test_tasks = [
        "intent_recognition",
        "conversation",
        "strategy",
        "classification",
        "education",
        "compliance"
    ]

    print("Task Routing Test:")
    print("=" * 50)

    for task in test_tasks:
        selection = router.route_task(task)
        if selection:
            print(f"{task:<20} -> {selection.tier:<8} -> {selection.name}")
        else:
            print(f"{task:<20} -> NO MODEL FOUND")

    # Show tier statistics
    print("\nTier Statistics:")
    print("=" * 50)

    for stat in router.get_all_tier_stats():
        if stat.get("model_count", 0) > 0:
            print(f"{stat['tier']}: {stat['model_count']} models, avg {stat['avg_response_time']}s response")
            print(f"  Target: {stat['target_response_time']}")
            print(f"  Fastest: {stat['fastest_model']}")
            print()
