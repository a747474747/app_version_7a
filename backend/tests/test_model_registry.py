#!/usr/bin/env python3
"""
Test script to run the model registry service directly.
"""
import asyncio
import sys
import os

# Add backend to path (we're already in backend/tests, so go up one level)
backend_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, backend_path)

# Set dummy environment variables to avoid settings validation
os.environ['CLERK_SECRET_KEY'] = 'dummy'
os.environ['CLERK_PUBLISHABLE_KEY'] = 'dummy'
os.environ['LLM_OPENROUTER_API_KEY'] = 'dummy'

async def test_model_registry():
    """Test the model registry service."""
    print("Testing Model Registry Service...")

    try:
        # Import the model registry service directly
        from llm_engine.model_registry import ModelRegistryService
        from calculation_engine.schemas.llm_tiers import LLMTier

        print("SUCCESS: Imports successful")

        # Get registry service
        registry_service = ModelRegistryService()
        print("SUCCESS: Registry service initialized")

        # Get registry (this will fetch models if needed)
        print("Fetching models from OpenRouter...")
        registry = await registry_service.get_registry(force_refresh=True)
        print(f"SUCCESS: Fetched {registry.model_count} models")

        # Test tier selection
        print("\nTesting tier selection:")

        for tier in LLMTier:
            result = await registry_service.select_model_for_tier(tier)
            if result:
                model = result.selected_model
                print(f"  {tier.value}: {model.id} (cost: ${model.average_cost:.4f})")
            else:
                print(f"  {tier.value}: No suitable model found")

        # Get registry status
        status = await registry_service.get_registry_status()
        print("\nRegistry Status:")
        print(f"  Total models: {status.total_models}")
        print(f"  Models by tier: {status.models_by_tier}")
        print(f"  Last updated: {status.last_updated}")
        print(f"  Cache file exists: {status.cache_file_exists}")

        print("\nSUCCESS: Model Registry Test PASSED!")

    except Exception as e:
        print(f"ERROR: Test FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_model_registry())
