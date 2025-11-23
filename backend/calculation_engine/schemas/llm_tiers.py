"""
LLM Tier Enums for the Four-Engine Architecture.

Defines the three intelligence tiers used for dynamic model selection:
- ROUTER: Fast/cheap intent recognition and classification
- NARRATOR: Balanced fluency and conversational responses
- THINKER: Complex reasoning and strategic analysis
"""

from enum import Enum


class LLMTier(Enum):
    """
    Three intelligence tiers for LLM model selection.

    Each tier optimizes for different trade-offs between speed, cost, and quality:
    - ROUTER: Maximum speed and cost efficiency for lightweight tasks
    - NARRATOR: Balanced performance for natural language generation
    - THINKER: Maximum quality for complex reasoning tasks
    """

    ROUTER = "router"
    """Fast/cheap tier for intent recognition, classification, and lightweight tasks."""

    NARRATOR = "narrator"
    """Balanced tier for natural language generation and conversational responses."""

    THINKER = "thinker"
    """Quality-focused tier for complex reasoning and strategic optimization."""


class TierCapability(Enum):
    """
    Capability metrics used for model evaluation and selection.
    """

    REASONING = "reasoning"
    """Multi-step reasoning and logical analysis capability."""

    FLUENCY = "fluency"
    """Natural language generation and coherence."""

    SPEED = "speed"
    """Inference speed and response time."""


class ModelSelectionCriteria:
    """
    Selection criteria weights for each tier.

    Defines how different factors (cost, quality, speed) are weighted
    when selecting the optimal model for each intelligence tier.
    """

    # Router: Cost-optimized for speed
    ROUTER_WEIGHTS = {
        "quality_weight": 0.3,  # Lower weight on quality
        "cost_weight": 1.4,     # Higher weight on cost efficiency (doubled)
        "min_context": 8192,    # Minimum context window
    }

    # Narrator: Balanced performance
    NARRATOR_WEIGHTS = {
        "quality_weight": 0.6,  # Balanced quality focus
        "cost_weight": 0.8,     # Moderate cost consideration (doubled)
        "min_context": 16384,   # Larger context for conversations
    }

    # Thinker: Quality-optimized
    THINKER_WEIGHTS = {
        "quality_weight": 0.8,  # High quality priority
        "cost_weight": 0.4,     # Lower cost sensitivity (doubled)
        "min_context": 32768,   # Large context for complex analysis
    }

    @classmethod
    def get_weights_for_tier(cls, tier: LLMTier) -> dict:
        """Get selection weights for a specific tier."""
        if tier == LLMTier.ROUTER:
            return cls.ROUTER_WEIGHTS
        elif tier == LLMTier.NARRATOR:
            return cls.NARRATOR_WEIGHTS
        elif tier == LLMTier.THINKER:
            return cls.THINKER_WEIGHTS
        else:
            raise ValueError(f"Unknown tier: {tier}")
