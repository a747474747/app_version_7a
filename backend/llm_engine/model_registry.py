"""
Model Registry Service for the Four-Engine Architecture.

Provides dynamic model catalog management with caching, refresh, and
tier-based model selection capabilities for the LLM Tiered Routing Strategy.
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import httpx

from ..calculation_engine.schemas.llm_tiers import LLMTier
from ..calculation_engine.schemas.openrouter import (
    OpenRouterModel,
    OpenRouterModelsResponse,
    ModelSelectionResult
)
from ..calculation_engine.schemas.model_registry import (
    ModelRegistry,
    RegistryStatus
)

logger = logging.getLogger(__name__)


class ModelRegistryService:
    """
    Service for managing OpenRouter model catalog with caching and tier selection.

    This service fetches the complete model list from OpenRouter, caches it locally,
    and provides efficient querying and selection capabilities for the tiered routing system.
    """

    def __init__(
        self,
        cache_file: str = "backend/llm_engine/model_registry_cache.json",
        cache_ttl_hours: int = 24,
        openrouter_api_key: Optional[str] = None
    ):
        """
        Initialize the model registry service.

        Args:
            cache_file: Path to cache file for storing model registry
            cache_ttl_hours: Cache time-to-live in hours
            openrouter_api_key: OpenRouter API key (optional, can be set via env)
        """
        self.cache_file = Path(cache_file)
        self.cache_ttl_hours = cache_ttl_hours
        self.openrouter_api_key = openrouter_api_key or self._get_api_key()
        self._registry: Optional[ModelRegistry] = None

    def _get_api_key(self) -> str:
        """Get OpenRouter API key from environment or config."""
        # TODO: Integrate with settings service
        import os
        return os.getenv("OPENROUTER_API_KEY", "")

    async def get_registry(self, force_refresh: bool = False) -> ModelRegistry:
        """
        Get the current model registry, refreshing from API if needed.

        Args:
            force_refresh: Force refresh from OpenRouter API

        Returns:
            Current model registry instance
        """
        if self._registry is None or force_refresh:
            await self._load_or_refresh_registry()

        return self._registry

    async def _load_or_refresh_registry(self) -> None:
        """Load registry from cache or refresh from API."""
        # Try to load from cache first
        if self._try_load_from_cache():
            # Check if cache is still valid
            if not self._registry.is_stale:
                logger.info("Loaded valid model registry from cache")
                return

        # Cache is stale or missing, refresh from API
        logger.info("Refreshing model registry from OpenRouter API")
        await self._refresh_from_api()

    def _try_load_from_cache(self) -> bool:
        """Try to load registry from cache file."""
        try:
            if not self.cache_file.exists():
                return False

            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)

            self._registry = ModelRegistry.from_cache_dict(cache_data)
            return True

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to load registry from cache: {e}")
            return False

    async def _refresh_from_api(self) -> None:
        """Refresh registry from OpenRouter API."""
        if not self.openrouter_api_key:
            raise ValueError("OpenRouter API key not configured")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    "https://openrouter.ai/api/v1/models",
                    headers={
                        "Authorization": f"Bearer {self.openrouter_api_key}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()

                api_response = response.json()
                models_data = api_response.get("data", [])

                # Convert API response to our models
                models = []
                for model_data in models_data:
                    try:
                        model = self._convert_api_model_to_schema(model_data)
                        models.append(model)
                    except Exception as e:
                        logger.warning(f"Failed to process model {model_data.get('id', 'unknown')}: {e}")
                        continue

                # Create registry
                self._registry = ModelRegistry(
                    last_updated=datetime.utcnow(),
                    models=models
                )

                # Auto-assign tiers and build mappings
                self._registry.refresh_tier_mappings()

                # Save to cache
                self._save_to_cache()

                logger.info(f"Successfully refreshed registry with {len(models)} models")

        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch models from OpenRouter API: {e}")
            raise

    def _convert_api_model_to_schema(self, api_model: Dict[str, Any]) -> OpenRouterModel:
        """Convert OpenRouter API model format to our schema."""
        # Extract pricing (convert from per million tokens to our format)
        pricing_data = api_model.get("pricing", {})
        pricing = {
            "prompt": float(pricing_data.get("prompt", "0")) / 1000000,  # Convert to USD per token
            "completion": float(pricing_data.get("completion", "0")) / 1000000
        }

        # Extract capabilities (use defaults if not available)
        # Note: OpenRouter API may not provide detailed capability scores
        # We'll use placeholder values that can be enhanced with actual benchmarking
        capabilities = {
            "reasoning_score": 75,  # Default moderate reasoning
            "fluency_score": 80,    # Default good fluency
            "speed_score": 70       # Default moderate speed
        }

        # Create model with auto-assigned tiers (empty initially, will be set by refresh_tier_mappings)
        model = OpenRouterModel(
            id=api_model["id"],
            name=api_model.get("name", api_model["id"]),
            pricing=pricing,
            context_length=api_model.get("context_length", 4096),
            capabilities=capabilities,
            tiers=[]  # Will be populated by tier assignment logic
        )

        return model

    def _save_to_cache(self) -> None:
        """Save current registry to cache file."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)

            cache_data = self._registry.to_cache_dict()

            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2, default=str)

            logger.info(f"Saved registry to cache: {self.cache_file}")

        except Exception as e:
            logger.error(f"Failed to save registry to cache: {e}")

    async def select_model_for_tier(self, tier: LLMTier) -> Optional[ModelSelectionResult]:
        """
        Select the best model for a specific intelligence tier.

        Args:
            tier: Intelligence tier to select model for

        Returns:
            Model selection result with chosen model and alternatives
        """
        registry = await self.get_registry()

        selected_model = registry.get_best_model_for_tier(tier)
        if not selected_model:
            return None

        # Get alternatives (other models in the same tier, sorted by score)
        tier_models = registry.get_models_for_tier(tier)
        alternatives = [m for m in tier_models if m.id != selected_model.id]

        # Calculate selection score (simple cost-value ratio for now)
        if tier == LLMTier.ROUTER:
            score = 1.0 / max(selected_model.average_cost, 0.01)  # Lower cost = higher score
        elif tier == LLMTier.THINKER:
            score = selected_model.capabilities.reasoning_score
        else:  # NARRATOR
            score = selected_model.capabilities.fluency_score / max(selected_model.average_cost, 0.01)

        return ModelSelectionResult(
            tier=tier,
            selected_model=selected_model,
            selection_score=score,
            alternatives=alternatives[:3]  # Top 3 alternatives
        )

    async def get_registry_status(self) -> RegistryStatus:
        """Get current registry status for monitoring."""
        registry = await self.get_registry()
        cache_exists = self.cache_file.exists()

        return RegistryStatus.from_registry(registry, cache_exists)

    async def force_refresh(self) -> None:
        """Force a refresh of the model registry from the API."""
        logger.info("Forcing registry refresh")
        await self._refresh_from_api()


# Global instance for easy access
_registry_service: Optional[ModelRegistryService] = None


def get_model_registry_service() -> ModelRegistryService:
    """Get the global model registry service instance."""
    global _registry_service
    if _registry_service is None:
        _registry_service = ModelRegistryService()
    return _registry_service
