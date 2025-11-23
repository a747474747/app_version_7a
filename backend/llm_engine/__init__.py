"""
LLM Engine Package

This package contains the LLM Orchestrator components for the Four-Engine Architecture.
The LLM Engine handles probabilistic AI operations including:

- Intent recognition and mode selection
- State hydration from natural language
- Narrative generation for human-readable outputs
- Privacy filtering and PII redaction
- Orchestration of LLM operations with TraceLog integration

Key Principles:
- Strict separation from deterministic Calculation Engine
- CAL-* ID tracking for all LLM operations
- Prompt management via external files
- TraceLog integration for audit trails
"""

from .orchestrator import LLMOrchestratorBase, IntentRecognitionResult, StateHydrationResult, NarrativeGenerationResult, LLMOrchestratorResponse
from .state_hydration import StateHydrationEngine, hydrate_state_from_text
from .narrative_generation import NarrativeGenerationEngine, generate_tax_narrative, generate_wealth_narrative, generate_retirement_narrative
from .privacy_filter import PrivacyFilter, PrivacyLevel, PIIType, PrivacyFilterResult, get_privacy_filter, filter_text_for_llm, scrub_pii
from .intent_recognition import IntentRecognitionEngine, OperationalMode, IntentCategory, recognize_user_intent, get_operational_modes
from .model_registry import ModelRegistryService, get_model_registry_service

__all__ = [
    "LLMOrchestratorBase",
    "IntentRecognitionResult",
    "StateHydrationResult",
    "NarrativeGenerationResult",
    "LLMOrchestratorResponse",
    "StateHydrationEngine",
    "hydrate_state_from_text",
    "NarrativeGenerationEngine",
    "generate_tax_narrative",
    "generate_wealth_narrative",
    "generate_retirement_narrative",
    "PrivacyFilter",
    "PrivacyLevel",
    "PIIType",
    "PrivacyFilterResult",
    "get_privacy_filter",
    "filter_text_for_llm",
    "scrub_pii",
    "IntentRecognitionEngine",
    "OperationalMode",
    "IntentCategory",
    "recognize_user_intent",
    "get_operational_modes",
    "ModelRegistryService",
    "get_model_registry_service"
]
