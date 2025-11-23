"""
LLM Orchestrator Base Class

This module provides the core LLM Orchestrator base class with prompt loading patterns
and CAL-* ID tracking integration for the Four-Engine Architecture.

Key Responsibilities:
- Load prompts from external files (never embedded)
- Orchestrate LLM operations with TraceLog integration
- Provide base patterns for intent recognition, state hydration, and narrative generation
- Maintain separation from deterministic Calculation Engine operations

Author: AI Assistant
Created: 2025-11-22
Timezone: Australia/Brisbane (UTC+10)
"""

import asyncio
import json
import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from pydantic import BaseModel, Field

from src.services.llm_service import get_llm_service
from src.services.prompt_service import PromptService
from calculation_engine.schemas.orchestration import TraceEntry, TraceLog

logger = logging.getLogger(__name__)


class IntentRecognitionResult(BaseModel):
    """Result of intent recognition aligned with LLM Orchestrator contract."""
    detected_intent: str = Field(..., description="Detected user intent")
    selected_mode: str = Field(..., description="Execution mode ID")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence score 0.0-1.0")
    extracted_entities: Dict[str, Any] = Field(default_factory=dict, description="Parsed entities")
    clarification_questions: Optional[List[str]] = Field(None, description="Questions for clarification")
    requires_calculation: bool = Field(default=False, description="Whether calculation is needed")


class StateHydrationResult(BaseModel):
    """Result of state hydration aligned with LLM Orchestrator contract."""
    hydrated_state: Dict[str, Any] = Field(..., description="Structured state fragments")
    missing_fields: List[str] = Field(default_factory=list, description="Fields that need clarification")
    validation_errors: List[str] = Field(default_factory=list, description="Data quality issues")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence score 0.0-1.0")
    suggested_questions: List[str] = Field(default_factory=list, description="Questions for missing data")


class NarrativeGenerationResult(BaseModel):
    """Result of narrative generation aligned with LLM Orchestrator contract."""
    narrative: str = Field(..., description="Human-readable text")
    key_points: List[str] = Field(default_factory=list, description="Important information points")
    citations: List[Dict[str, Any]] = Field(default_factory=list, description="References to rules/sources")
    confidence_score: float = Field(..., ge=0, le=1, description="Generation quality score")


class LLMOrchestratorResponse(BaseModel):
    """Unified response schema for LLM Orchestrator operations."""
    success: bool
    result: Dict[str, Any] = Field(default_factory=dict, description="Operation-specific result data")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Processing metadata")
    trace_log: Optional[TraceLog] = Field(None, description="Trace log for the operation")
    error_message: Optional[str] = None


class LLMOrchestratorBase(ABC):
    """
    Base class for LLM Orchestrator operations.

    This class provides the foundation for all LLM operations in the four-engine architecture,
    with built-in prompt loading, TraceLog integration, and CAL-* ID tracking.

    Key Features:
    - External prompt loading (never embedded)
    - TraceLog integration for audit trails
    - CAL-* ID tracking for all operations
    - Separation from deterministic calculation logic
    """

    def __init__(self, specs_base_path: Optional[Path] = None):
        """
        Initialize the LLM Orchestrator.

        Args:
            specs_base_path: Base path for specs directory (auto-detected if None)
        """
        self.specs_base_path = specs_base_path or Path(__file__).parent.parent.parent / "specs"
        self.prompt_service = PromptService(self.specs_base_path)
        self._llm_service = None

        # Initialize trace log for this orchestrator session
        self.current_trace_log = TraceLog(
            entries=[],
            session_id=f"llm-{datetime.now().isoformat()}",
            operation_type="llm_orchestration"
        )

    async def get_llm_service(self):
        """Get or initialize the LLM service."""
        if self._llm_service is None:
            self._llm_service = await get_llm_service()
        return self._llm_service

    def _load_prompt(self, prompt_id: str) -> str:
        """
        Load prompt text from external file.

        Args:
            prompt_id: Unique identifier for the prompt

        Returns:
            Prompt text content

        Raises:
            FileNotFoundError: If prompt file doesn't exist
        """
        try:
            return self.prompt_service.load_prompt(prompt_id)
        except Exception as e:
            logger.error(f"Failed to load prompt {prompt_id}: {str(e)}")
            raise

    def _create_trace_entry(
        self,
        calc_id: str,
        entity_id: str,
        field: str,
        explanation: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TraceEntry:
        """
        Create a TraceEntry for LLM operations with CAL-* ID tracking.

        Args:
            calc_id: CAL-* ID for the operation
            entity_id: Entity identifier
            field: Field being processed
            explanation: Human-readable explanation
            metadata: Additional metadata

        Returns:
            TraceEntry instance
        """
        return TraceEntry(
            calc_id=calc_id,
            entity_id=entity_id,
            field=field,
            explanation=explanation,
            metadata=metadata or {},
            timestamp=datetime.now()
        )

    async def _execute_llm_operation(
        self,
        operation_name: str,
        prompt_id: str,
        messages: List[Dict[str, str]],
        calc_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute an LLM operation with full TraceLog integration.

        Args:
            operation_name: Name of the operation for logging
            prompt_id: Prompt ID to load
            messages: Chat messages for the LLM
            calc_id: Optional CAL-* ID for tracking
            **kwargs: Additional parameters for LLM call

        Returns:
            LLM response data
        """
        llm_service = await self.get_llm_service()

        # Load prompt
        try:
            system_prompt = self._load_prompt(prompt_id)
            full_messages = [{"role": "system", "content": system_prompt}] + messages
        except Exception as e:
            error_msg = f"Failed to load prompt {prompt_id}: {str(e)}"
            logger.error(error_msg)
            raise

        # Add trace entry for operation start
        if calc_id:
            trace_entry = self._create_trace_entry(
                calc_id=calc_id,
                entity_id="llm_orchestrator",
                field=f"operation_{operation_name}",
                explanation=f"Starting LLM operation: {operation_name}",
                metadata={"prompt_id": prompt_id, "messages_count": len(messages)}
            )
            self.current_trace_log.entries.append(trace_entry)

        # Execute LLM call
        try:
            start_time = datetime.now()
            response = await llm_service.generate_completion(
                messages=full_messages,
                **kwargs
            )
            end_time = datetime.now()

            # Add success trace entry
            if calc_id:
                success_entry = self._create_trace_entry(
                    calc_id=calc_id,
                    entity_id="llm_orchestrator",
                    field=f"operation_{operation_name}_result",
                    explanation=f"LLM operation {operation_name} completed successfully",
                    metadata={
                        "duration_ms": (end_time - start_time).total_seconds() * 1000,
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                )
                self.current_trace_log.entries.append(success_entry)

            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.model_dump(),
                "metadata": {
                    "operation": operation_name,
                    "prompt_id": prompt_id,
                    "duration_ms": (end_time - start_time).total_seconds() * 1000
                }
            }

        except Exception as e:
            error_msg = f"LLM operation {operation_name} failed: {str(e)}"
            logger.error(error_msg)

            # Add error trace entry
            if calc_id:
                error_entry = self._create_trace_entry(
                    calc_id=calc_id,
                    entity_id="llm_orchestrator",
                    field=f"operation_{operation_name}_error",
                    explanation=error_msg,
                    metadata={"error": str(e)}
                )
                self.current_trace_log.entries.append(error_entry)

            raise

    @abstractmethod
    async def recognize_intent(
        self,
        user_query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> IntentRecognitionResult:
        """
        Recognize user intent from natural language query.

        Args:
            user_query: User's natural language query
            context: Optional context information

        Returns:
            Intent recognition result
        """
        pass

    @abstractmethod
    async def hydrate_state(
        self,
        user_query: str,
        current_state: Dict[str, Any],
        calc_id: Optional[str] = None
    ) -> StateHydrationResult:
        """
        Convert natural language to structured CalculationState.

        Args:
            user_query: User's natural language input
            current_state: Current calculation state
            calc_id: Optional CAL-* ID for tracking

        Returns:
            State hydration result
        """
        pass

    @abstractmethod
    async def generate_narrative(
        self,
        data: Dict[str, Any],
        template: str,
        calc_id: Optional[str] = None
    ) -> NarrativeGenerationResult:
        """
        Generate human-readable narrative from structured data.

        Args:
            data: Structured data to narrate
            template: Template identifier
            calc_id: Optional CAL-* ID for tracking

        Returns:
            Narrative generation result
        """
        pass

    def get_trace_log(self) -> TraceLog:
        """
        Get the current TraceLog for this orchestrator session.

        Returns:
            Complete trace log
        """
        return self.current_trace_log

    def reset_trace_log(self) -> None:
        """Reset the trace log for a new session."""
        self.current_trace_log = TraceLog(
            entries=[],
            session_id=f"llm-{datetime.now().isoformat()}",
            operation_type="llm_orchestration"
        )
