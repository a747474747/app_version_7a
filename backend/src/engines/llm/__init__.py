"""
Legacy LLM Engine Package

This package has been migrated to backend/llm_engine/ for better separation of concerns.
The LLM Orchestrator components are now located in the dedicated llm_engine directory.

For new implementations, import from backend.llm_engine instead.

Legacy components will be maintained here during transition period.
"""

# Re-export from new location for backward compatibility
from llm_engine import (
    LLMOrchestratorBase,
    IntentRecognitionResult,
    StateHydrationResult,
    NarrativeGenerationResult,
    LLMOrchestratorResponse
)

# Legacy global instance (deprecated - use new LLMOrchestratorBase implementations)
from llm_engine.orchestrator import LLMOrchestratorBase as _BaseOrchestrator

class LLMOrchestrator(_BaseOrchestrator):
    """
    Legacy LLM Orchestrator class for backward compatibility.

    DEPRECATED: Use LLMOrchestratorBase from backend.llm_engine instead.
    This class will be removed in a future version.
    """

    def __init__(self):
        super().__init__()
        import warnings
        warnings.warn(
            "LLMOrchestrator is deprecated. Use LLMOrchestratorBase from backend.llm_engine",
            DeprecationWarning,
            stacklevel=2
        )

    # Simple stub implementations for backward compatibility
    async def recognize_intent(self, user_query: str, context=None):
        """Stub implementation - migrate to proper LLMOrchestratorBase subclass."""
        raise NotImplementedError("Use LLMOrchestratorBase subclass instead")

    async def hydrate_state(self, user_query: str, current_state: dict, calc_id=None):
        """Stub implementation - migrate to proper LLMOrchestratorBase subclass."""
        raise NotImplementedError("Use LLMOrchestratorBase subclass instead")

    async def generate_narrative(self, data: dict, template: str, calc_id=None):
        """Stub implementation - migrate to proper LLMOrchestratorBase subclass."""
        raise NotImplementedError("Use LLMOrchestratorBase subclass instead")

# Global instance (deprecated)
llm_orchestrator = LLMOrchestrator()

