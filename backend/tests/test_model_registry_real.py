#!/usr/bin/env python3
"""
Test the model registry with real OpenRouter API calls.
"""
import asyncio
import os
import sys

# Add backend to path (we're already in backend/tests, so go up one level)
backend_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, backend_path)

# Load environment variables from .env.local
def load_env_file():
    """Load environment variables from .env.local if it exists."""
    env_file = os.path.join(os.path.dirname(__file__), '..', '..', '.env.local')
    if os.path.exists(env_file):
        print(f'Loading environment from {env_file}')
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, _, value = line.partition('=')
                    if key and value:
                        clean_value = value.strip().strip('"').strip("'")
                        if '\x00' not in clean_value:  # Skip null characters
                            os.environ[key.strip()] = clean_value

# Load environment first
load_env_file()

# Set proper environment variables to avoid settings validation
os.environ.setdefault('CLERK_SECRET_KEY', 'dummy_clerk_secret_key_for_testing')
os.environ.setdefault('CLERK_PUBLISHABLE_KEY', 'dummy_clerk_publishable_key_for_testing')
# Keep the real API key that was loaded from .env.local

async def test_real_registry():
    """Test the model registry with real API calls."""
    print("Testing Model Registry with Real OpenRouter API...")

    api_key = os.getenv('LLM_OPENROUTER_API_KEY')
    if not api_key or api_key == 'dummy':
        print("ERROR: No valid LLM_OPENROUTER_API_KEY found")
        return

    print(f"SUCCESS: Found API key: {api_key[:12]}...")

    try:
        # Import the model registry service
        from llm_engine.model_registry import ModelRegistryService
        from calculation_engine.schemas.llm_tiers import LLMTier

        print("SUCCESS: Registry service import successful")

        # Create registry service with real API key
        registry_service = ModelRegistryService(openrouter_api_key=api_key)

        print("Fetching models from OpenRouter...")
        registry = await registry_service.get_registry(force_refresh=True)

        print(f"SUCCESS: Fetched {registry.model_count} models from OpenRouter")

        # Test tier selection
        print("\nTesting tier selection with real models:")

        for tier in LLMTier:
            result = await registry_service.select_model_for_tier(tier)
            if result:
                model = result.selected_model
                print(f"  {tier.value}: {model.id}")
                print(f"    Cost: ${model.average_cost:.6f}")
                print(f"    Alternatives: {len(result.alternatives)}")
            else:
                print(f"  {tier.value}: No suitable model found")

        # Get registry status
        status = await registry_service.get_registry_status()
        print("\nRegistry Status:")
        print(f"  Total models: {status.total_models}")
        print(f"  Models by tier: {status.models_by_tier}")
        print(f"  Cache file exists: {status.cache_file_exists}")

        # Check if cache file was created
        cache_file = registry_service.cache_file
        if cache_file.exists():
            print(f"SUCCESS: Cache file created at {cache_file}")
        else:
            print(f"ERROR: Cache file not created at {cache_file}")

        print("\nSUCCESS: Real Model Registry Test PASSED!")

    except Exception as e:
        print(f"ERROR: Test FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_real_registry())
