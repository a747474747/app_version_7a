"""
OpenRouter API schemas for the Four-Engine Architecture.

Defines Pydantic models for interacting with the OpenRouter API,
including model information, pricing, and capabilities.
"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from .llm_tiers import LLMTier, TierCapability


class OpenRouterPricing(BaseModel):
    """
    Pricing information for an OpenRouter model.

    Costs are in USD per million tokens (input) or per million tokens (output).
    """

    prompt: float = Field(..., description="Cost per million input tokens in USD")
    completion: float = Field(..., description="Cost per million output tokens in USD")

    @property
    def average_cost_per_token(self) -> float:
        """Calculate average cost per token (rough estimate)."""
        # Assume 1:3 input to output ratio for average cost
        return (self.prompt + 3 * self.completion) / 4


class OpenRouterCapabilities(BaseModel):
    """
    Capability scores for model evaluation.

    Scores are normalized 0-100, where higher is better.
    """

    reasoning_score: int = Field(..., ge=0, le=100, description="Multi-step reasoning capability")
    fluency_score: int = Field(..., ge=0, le=100, description="Natural language generation quality")
    speed_score: int = Field(..., ge=0, le=100, description="Inference speed relative to peers")

    def get_score(self, capability: TierCapability) -> int:
        """Get score for a specific capability."""
        if capability == TierCapability.REASONING:
            return self.reasoning_score
        elif capability == TierCapability.FLUENCY:
            return self.fluency_score
        elif capability == TierCapability.SPEED:
            return self.speed_score
        else:
            raise ValueError(f"Unknown capability: {capability}")


class OpenRouterModel(BaseModel):
    """
    Complete model information from OpenRouter API.

    Represents a single model available through OpenRouter,
    including pricing, capabilities, and suitability for different tiers.
    """

    id: str = Field(..., description="OpenRouter model identifier (e.g., 'anthropic/claude-3-haiku')")
    name: str = Field(..., description="Human-readable model name")
    pricing: OpenRouterPricing = Field(..., description="Token pricing information")
    context_length: int = Field(..., description="Maximum context window in tokens")
    capabilities: OpenRouterCapabilities = Field(..., description="Model capability scores")

    # Dynamic tier assignment based on capabilities and pricing
    tiers: List[LLMTier] = Field(default_factory=list, description="Suitable intelligence tiers for this model")

    @property
    def average_cost(self) -> float:
        """Get average cost per token."""
        return self.pricing.average_cost_per_token

    def is_suitable_for_tier(self, tier: LLMTier) -> bool:
        """
        Check if model is suitable for a specific intelligence tier.

        Uses simple heuristics based on pricing and capabilities.
        """
        if tier == LLMTier.ROUTER:
            # Router: Low cost, good speed
            return (
                self.average_cost < 1.0 and  # Relatively cheap
                self.capabilities.speed_score >= 70 and  # Fast
                self.context_length >= 8192  # Sufficient context
            )
        elif tier == LLMTier.NARRATOR:
            # Narrator: Balanced cost-quality, good fluency
            return (
                self.capabilities.fluency_score >= 75 and  # Good language generation
                self.context_length >= 16384  # Larger context for conversations
            )
        elif tier == LLMTier.THINKER:
            # Thinker: High reasoning, large context
            return (
                self.capabilities.reasoning_score >= 80 and  # Strong reasoning
                self.context_length >= 32768  # Large context for complex tasks
            )
        return False


class OpenRouterModelsResponse(BaseModel):
    """
    Response from OpenRouter models API.

    Contains the complete list of available models with their metadata.
    """

    models: List[OpenRouterModel] = Field(..., description="List of available models")
    retrieved_at: datetime = Field(default_factory=datetime.utcnow, description="When data was retrieved")


class ModelSelectionResult(BaseModel):
    """
    Result of model selection for a specific tier.

    Includes the selected model and selection rationale.
    """

    tier: LLMTier = Field(..., description="Intelligence tier")
    selected_model: OpenRouterModel = Field(..., description="Selected model for the tier")
    selection_score: float = Field(..., description="Selection algorithm score (higher is better)")
    alternatives: List[OpenRouterModel] = Field(default_factory=list, description="Alternative models considered")

    class Config:
        arbitrary_types_allowed = True
