"""
Model Registry schemas for the Four-Engine Architecture.

Defines the cached registry structure for storing and querying
available OpenRouter models with tier mappings.
"""

from datetime import datetime, timedelta
from typing import Dict, List
from pydantic import BaseModel, Field

from .openrouter import OpenRouterModel
from .llm_tiers import LLMTier


class ModelRegistry(BaseModel):
    """
    Cached registry of OpenRouter models with tier mappings.

    Stores the complete model catalog with automatic tier assignment
    and provides efficient querying capabilities.
    """

    last_updated: datetime = Field(..., description="When registry was last refreshed from OpenRouter")
    models: List[OpenRouterModel] = Field(..., description="Complete list of available models")
    tier_mappings: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Model IDs mapped by tier (tier_name -> [model_ids])"
    )

    @property
    def is_stale(self) -> bool:
        """Check if registry needs refresh (24 hour TTL)."""
        return datetime.utcnow() - self.last_updated > timedelta(hours=24)

    @property
    def model_count(self) -> int:
        """Get total number of models in registry."""
        return len(self.models)

    def get_models_for_tier(self, tier: LLMTier) -> List[OpenRouterModel]:
        """Get all models suitable for a specific tier."""
        model_ids = self.tier_mappings.get(tier.value, [])
        return [model for model in self.models if model.id in model_ids]

    def get_best_model_for_tier(self, tier: LLMTier) -> Optional[OpenRouterModel]:
        """Get the best model for a tier based on selection criteria."""
        tier_models = self.get_models_for_tier(tier)
        if not tier_models:
            return None

        # Simple selection: lowest cost for Router, highest reasoning for Thinker, balanced for Narrator
        if tier == LLMTier.ROUTER:
            return min(tier_models, key=lambda m: m.average_cost)
        elif tier == LLMTier.THINKER:
            return max(tier_models, key=lambda m: m.capabilities.reasoning_score)
        elif tier == LLMTier.NARRATOR:
            # Balanced: cost-value ratio (quality/cost)
            return max(
                tier_models,
                key=lambda m: m.capabilities.fluency_score / max(m.average_cost, 0.01)
            )
        return None

    def refresh_tier_mappings(self) -> None:
        """
        Rebuild tier mappings based on current model capabilities.

        Automatically categorizes models into appropriate tiers based on
        their pricing and capability scores.
        """
        self.tier_mappings = {
            tier.value: [] for tier in LLMTier
        }

        for model in self.models:
            # Auto-assign tiers based on model characteristics
            suitable_tiers = []
            for tier in LLMTier:
                if model.is_suitable_for_tier(tier):
                    suitable_tiers.append(tier.value)

            # Update mappings
            for tier_name in suitable_tiers:
                if tier_name not in self.tier_mappings:
                    self.tier_mappings[tier_name] = []
                self.tier_mappings[tier_name].append(model.id)

    def to_cache_dict(self) -> dict:
        """Convert to dictionary for JSON caching."""
        return {
            "last_updated": self.last_updated.isoformat(),
            "models": [model.dict() for model in self.models],
            "tier_mappings": self.tier_mappings
        }

    @classmethod
    def from_cache_dict(cls, data: dict) -> "ModelRegistry":
        """Reconstruct from cached dictionary."""
        from dateutil import parser

        models = [OpenRouterModel(**model_data) for model_data in data["models"]]
        return cls(
            last_updated=parser.parse(data["last_updated"]),
            models=models,
            tier_mappings=data.get("tier_mappings", {})
        )


class RegistryStatus(BaseModel):
    """
    Status information about the model registry.

    Used for monitoring and debugging the registry system.
    """

    total_models: int = Field(..., description="Total models in registry")
    models_by_tier: Dict[str, int] = Field(..., description="Model count per tier")
    last_updated: datetime = Field(..., description="Last update timestamp")
    is_stale: bool = Field(..., description="Whether registry needs refresh")
    cache_file_exists: bool = Field(..., description="Whether cache file is present")

    @classmethod
    def from_registry(cls, registry: ModelRegistry, cache_exists: bool = True) -> "RegistryStatus":
        """Create status from registry instance."""
        tier_counts = {}
        for tier in LLMTier:
            tier_counts[tier.value] = len(registry.get_models_for_tier(tier))

        return cls(
            total_models=registry.model_count,
            models_by_tier=tier_counts,
            last_updated=registry.last_updated,
            is_stale=registry.is_stale,
            cache_file_exists=cache_exists
        )
