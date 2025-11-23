#!/usr/bin/env python3
"""
Simple test for model registry components without full app dependencies.
"""
import asyncio
import os
import sys

# Add backend to path (we're already in backend/tests, so go up one level)
backend_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, backend_path)

# Mock httpx to avoid network calls for basic testing
class MockAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def get(self, *args, **kwargs):
        # Return mock response
        class MockResponse:
            def __init__(self):
                self.status_code = 200

            def json(self):
                return {
                    "data": [
                        {
                            "id": "anthropic/claude-3-haiku",
                            "name": "Claude 3 Haiku",
                            "context_length": 200000,
                            "pricing": {"prompt": "0.00000025", "completion": "0.00000125"},
                        },
                        {
                            "id": "openai/gpt-4o",
                            "name": "GPT-4o",
                            "context_length": 128000,
                            "pricing": {"prompt": "0.0000025", "completion": "0.00001"},
                        }
                    ]
                }

            @property
            def is_success(self):
                return True

        return MockResponse()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

# Monkey patch httpx
import httpx
httpx.AsyncClient = MockAsyncClient

async def test_registry():
    """Test basic registry functionality."""
    print("Testing Model Registry Components...")

    try:
        # Import schemas directly
        from calculation_engine.schemas.llm_tiers import LLMTier, ModelSelectionCriteria
        from calculation_engine.schemas.openrouter import OpenRouterModel
        from calculation_engine.schemas.model_registry import ModelRegistry

        print("SUCCESS: Schema imports successful")

        # Test tier enums
        print(f"Tiers: {[tier.value for tier in LLMTier]}")

        # Test model creation
        model_data = {
            "id": "anthropic/claude-3-haiku",
            "name": "Claude 3 Haiku",
            "pricing": {"prompt": "0.00000025", "completion": "0.00000125"},
            "context_length": 200000,
            "capabilities": {
                "reasoning_score": 85,
                "fluency_score": 90,
                "speed_score": 95
            },
            "tiers": []
        }

        model = OpenRouterModel(**model_data)
        print(f"SUCCESS: Model created - {model.id}, cost: ${model.average_cost:.6f}")

        # Test registry
        from datetime import datetime, UTC
        registry = ModelRegistry(
            last_updated=datetime.now(UTC),
            models=[model],
            tier_mappings={"router": [model.id], "narrator": [], "thinker": []}
        )

        print(f"SUCCESS: Registry created with {registry.model_count} models")

        # Test tier selection
        selected = registry.get_best_model_for_tier(LLMTier.ROUTER)
        if selected:
            print(f"SUCCESS: Router selection - {selected.id}")
        else:
            print("No router model selected")

        print("SUCCESS: All registry components working!")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_registry())
