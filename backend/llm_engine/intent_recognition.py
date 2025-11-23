"""
Intent Recognition Module

This module provides patterns for recognizing user intent and selecting appropriate
operational modes for the Four-Engine Architecture.

Key Responsibilities:
- Analyze natural language queries for intent patterns
- Map intents to operational modes (1-26)
- Extract entities and context from user input
- Provide confidence scoring and fallback options
- Support mode-specific prompt routing

Author: AI Assistant
Created: 2025-11-22
Timezone: Australia/Brisbane (UTC+10)
"""

import logging
import re
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from enum import Enum

from .orchestrator import LLMOrchestratorBase, IntentRecognitionResult

logger = logging.getLogger(__name__)


class OperationalMode(Enum):
    """Operational modes from the Four-Engine Architecture."""

    # Fact Check Modes (1-5)
    FACT_CHECK_TAX = "MODE-FACT-CHECK-TAX"
    FACT_CHECK_WEALTH = "MODE-FACT-CHECK-WEALTH"
    FACT_CHECK_RETIREMENT = "MODE-FACT-CHECK-RETIREMENT"
    FACT_CHECK_INVESTMENT = "MODE-FACT-CHECK-INVESTMENT"
    FACT_CHECK_GENERAL = "MODE-FACT-CHECK-GENERAL"

    # Strategy Exploration Modes (6-10)
    STRATEGY_EXPLORE_PORTFOLIO = "MODE-STRATEGY-EXPLORE-PORTFOLIO"
    STRATEGY_EXPLORE_RETIREMENT = "MODE-STRATEGY-EXPLORE-RETIREMENT"
    STRATEGY_EXPLORE_TAX = "MODE-STRATEGY-EXPLORE-TAX"
    STRATEGY_EXPLORE_RISK = "MODE-STRATEGY-EXPLORE-RISK"
    STRATEGY_EXPLORE_SCENARIO = "MODE-STRATEGY-EXPLORE-SCENARIO"

    # Crystal Ball Modes (11-15)
    CRYSTAL_BALL_PROJECTION = "MODE-CRYSTAL-BALL-PROJECTION"
    CRYSTAL_BALL_SCENARIO = "MODE-CRYSTAL-BALL-SCENARIO"
    CRYSTAL_BALL_SENSITIVITY = "MODE-CRYSTAL-BALL-SENSITIVITY"
    CRYSTAL_BALL_STRESS_TEST = "MODE-CRYSTAL-BALL-STRESS-TEST"
    CRYSTAL_BALL_MARKET_IMPACT = "MODE-CRYSTAL-BALL-MARKET-IMPACT"

    # Adviser Sandbox Modes (16-20)
    ADVISER_SANDBOX_CALCULATION = "MODE-ADVISER-SANDBOX-CALCULATION"
    ADVISER_SANDBOX_STRATEGY = "MODE-ADVISER-SANDBOX-STRATEGY"
    ADVISER_SANDBOX_COMPLIANCE = "MODE-ADVISER-SANDBOX-COMPLIANCE"
    ADVISER_SANDBOX_CLIENT = "MODE-ADVISER-SANDBOX-CLIENT"
    ADVISER_SANDBOX_REPORTING = "MODE-ADVISER-SANDBOX-REPORTING"

    # Additional modes (21-26) - simplified for implementation
    CALCULATION_HARNESS = "MODE-CALCULATION-HARNESS"
    SCENARIO_FUZZER = "MODE-SCENARIO-FUZZER"
    ADVICE_HARNESS = "MODE-ADVICE-HARNESS"
    PROMPT_CONTRACT_TESTER = "MODE-PROMPT-CONTRACT-TESTER"
    RAG_AUDITOR = "MODE-RAG-AUDITOR"
    CROSS_ENGINE_CONSISTENCY = "MODE-CROSS-ENGINE-CONSISTENCY"


class IntentCategory(Enum):
    """High-level intent categories."""
    FACT_CHECK = "fact_check"
    STRATEGY_EXPLORE = "strategy_explore"
    PROJECTION = "projection"
    SCENARIO_ANALYSIS = "scenario_analysis"
    CALCULATION_TEST = "calculation_test"
    COMPLIANCE_CHECK = "compliance_check"
    GENERAL_INQUIRY = "general_inquiry"


class IntentRecognitionEngine(LLMOrchestratorBase):
    """
    Engine for recognizing user intent and selecting operational modes.

    This class uses pattern matching and LLM-powered analysis to determine
    the appropriate operational mode for user queries.
    """

    def __init__(self, specs_base_path: Optional[Path] = None):
        super().__init__(specs_base_path)
        self.intent_prompt_id = "core-orchestrator-intent-recognition"
        self._intent_patterns = self._initialize_patterns()

    def _initialize_patterns(self) -> List[Dict[str, Any]]:
        """Initialize intent recognition patterns."""
        return [
            # Tax-related patterns
            {
                "keywords": ["tax", "payg", "ato", "deduction", "bracket", "marginal", "income tax"],
                "entities": ["tax", "income", "deductions"],
                "mode": OperationalMode.FACT_CHECK_TAX,
                "category": IntentCategory.FACT_CHECK,
                "confidence_boost": 0.2
            },

            # Wealth/net worth patterns
            {
                "keywords": ["wealth", "net worth", "assets", "liabilities", "balance sheet", "equity"],
                "entities": ["assets", "liabilities", "wealth"],
                "mode": OperationalMode.FACT_CHECK_WEALTH,
                "category": IntentCategory.FACT_CHECK,
                "confidence_boost": 0.2
            },

            # Superannuation patterns
            {
                "keywords": ["super", "superannuation", "retirement", "pension", "aged pension"],
                "entities": ["superannuation", "retirement"],
                "mode": OperationalMode.FACT_CHECK_RETIREMENT,
                "category": IntentCategory.FACT_CHECK,
                "confidence_boost": 0.2
            },

            # Investment patterns
            {
                "keywords": ["investment", "portfolio", "shares", "property", "diversification"],
                "entities": ["investments", "portfolio"],
                "mode": OperationalMode.FACT_CHECK_INVESTMENT,
                "category": IntentCategory.FACT_CHECK,
                "confidence_boost": 0.2
            },

            # Strategy exploration patterns
            {
                "keywords": ["strategy", "optimize", "what if", "scenario", "compare", "alternative"],
                "entities": ["strategy", "scenario"],
                "mode": OperationalMode.STRATEGY_EXPLORE_SCENARIO,
                "category": IntentCategory.STRATEGY_EXPLORE,
                "confidence_boost": 0.15
            },

            # Projection patterns
            {
                "keywords": ["projection", "forecast", "future", "project", "estimate", "predict"],
                "entities": ["projection", "forecast"],
                "mode": OperationalMode.CRYSTAL_BALL_PROJECTION,
                "category": IntentCategory.PROJECTION,
                "confidence_boost": 0.15
            },

            # Calculation testing patterns
            {
                "keywords": ["test", "validate", "verify", "check calculation", "audit", "harness"],
                "entities": ["test", "validation"],
                "mode": OperationalMode.CALCULATION_HARNESS,
                "category": IntentCategory.CALCULATION_TEST,
                "confidence_boost": 0.25
            },

            # Compliance patterns
            {
                "keywords": ["compliance", "regulation", "bid", "best interest", "disclosure"],
                "entities": ["compliance", "regulation"],
                "mode": OperationalMode.COMPLIANCE_CHECK,
                "category": IntentCategory.COMPLIANCE_CHECK,
                "confidence_boost": 0.2
            }
        ]

    async def recognize_intent(
        self,
        user_query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> IntentRecognitionResult:
        """
        Recognize user intent and select appropriate operational mode.

        Args:
            user_query: User's natural language query
            context: Optional context information

        Returns:
            IntentRecognitionResult with detected intent and mode
        """
        # First try pattern-based recognition (fast)
        pattern_result = self._recognize_with_patterns(user_query, context)

        # If pattern recognition has high confidence, use it
        if pattern_result.confidence_score >= 0.8:
            return pattern_result

        # Otherwise, use LLM-powered recognition
        try:
            llm_result = await self._recognize_with_llm(user_query, context, pattern_result)
            return llm_result
        except Exception as e:
            logger.warning(f"LLM intent recognition failed: {str(e)}, using pattern result")
            return pattern_result

    def _recognize_with_patterns(
        self,
        user_query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> IntentRecognitionResult:
        """Recognize intent using pattern matching."""
        query_lower = user_query.lower()
        best_match = None
        best_score = 0.0
        extracted_entities = []

        for pattern in self._intent_patterns:
            score = self._calculate_pattern_score(query_lower, pattern)
            if score > best_score:
                best_score = score
                best_match = pattern

        if best_match:
            # Extract entities based on pattern
            extracted_entities = [
                entity for entity in best_match["entities"]
                if entity.lower() in query_lower
            ]

            return IntentRecognitionResult(
                detected_intent=best_match["category"].value,
                selected_mode=best_match["mode"].value,
                confidence_score=min(best_score, 1.0),
                extracted_entities=extracted_entities,
                requires_calculation=self._requires_calculation(best_match["category"])
            )

        # Default fallback
        return IntentRecognitionResult(
            detected_intent="general_inquiry",
            selected_mode=OperationalMode.FACT_CHECK_GENERAL.value,
            confidence_score=0.3,
            extracted_entities=[],
            clarification_questions=[
                "Could you please provide more details about your financial question?",
                "Are you asking about tax calculations, investment strategies, or retirement planning?"
            ]
        )

    def _calculate_pattern_score(self, query: str, pattern: Dict[str, Any]) -> float:
        """Calculate confidence score for a pattern match."""
        base_score = 0.0
        keyword_matches = 0

        for keyword in pattern["keywords"]:
            if keyword.lower() in query:
                keyword_matches += 1

        if keyword_matches > 0:
            # Base score from keyword matches
            base_score = min(keyword_matches / len(pattern["keywords"]), 0.7)

            # Boost for exact matches or position
            if query.startswith(tuple(pattern["keywords"])) or query.endswith(tuple(pattern["keywords"])):
                base_score += 0.1

            # Add pattern-specific boost
            base_score += pattern.get("confidence_boost", 0.0)

        return min(base_score, 1.0)

    async def _recognize_with_llm(
        self,
        user_query: str,
        context: Optional[Dict[str, Any]],
        pattern_result: IntentRecognitionResult
    ) -> IntentRecognitionResult:
        """Use LLM for intent recognition when pattern matching is uncertain."""
        # Prepare context for LLM
        llm_context = {
            "user_query": user_query,
            "pattern_analysis": {
                "detected_intent": pattern_result.detected_intent,
                "confidence": pattern_result.confidence_score,
                "extracted_entities": pattern_result.extracted_entities
            },
            "available_modes": [mode.value for mode in OperationalMode],
            "intent_categories": [cat.value for cat in IntentCategory]
        }

        if context:
            llm_context["additional_context"] = context

        # Execute LLM operation
        llm_response = await self._execute_llm_operation(
            operation_name="intent_recognition",
            prompt_id=self.intent_prompt_id,
            messages=[{
                "role": "user",
                "content": f"Analyze this user query and determine the most appropriate operational mode:\n\n{user_query}"
            }],
            temperature=0.1  # Low temperature for consistent mode selection
        )

        # Parse LLM response
        parsed_result = self._parse_llm_intent_response(llm_response["content"])

        # Merge with pattern results if LLM confidence is not higher
        if parsed_result.confidence_score <= pattern_result.confidence_score:
            return IntentRecognitionResult(
                detected_intent=parsed_result.detected_intent or pattern_result.detected_intent,
                selected_mode=parsed_result.selected_mode or pattern_result.selected_mode,
                confidence_score=max(parsed_result.confidence_score, pattern_result.confidence_score),
                extracted_entities=list(set(
                    (parsed_result.extracted_entities or []) +
                    (pattern_result.extracted_entities or [])
                )),
                clarification_questions=parsed_result.clarification_questions,
                requires_calculation=parsed_result.requires_calculation
            )

        return parsed_result

    def _parse_llm_intent_response(self, llm_content: str) -> IntentRecognitionResult:
        """Parse LLM response for intent recognition."""
        try:
            # Try to extract structured information from LLM response
            content_lower = llm_content.lower()

            # Look for mode selection
            selected_mode = None
            for mode in OperationalMode:
                if mode.value.lower() in content_lower:
                    selected_mode = mode.value
                    break

            # Look for intent category
            detected_intent = None
            for category in IntentCategory:
                if category.value.lower() in content_lower:
                    detected_intent = category.value
                    break

            # Extract entities (simple keyword extraction)
            entities = []
            entity_keywords = [
                "tax", "income", "super", "retirement", "investment", "portfolio",
                "assets", "liabilities", "strategy", "scenario", "projection"
            ]
            for keyword in entity_keywords:
                if keyword in content_lower:
                    entities.append(keyword)

            # Determine if calculation is required
            requires_calculation = any(word in content_lower for word in [
                "calculate", "compute", "determine", "find out", "work out"
            ])

            # Calculate confidence based on content
            confidence_score = 0.6  # Base confidence for LLM responses
            if selected_mode:
                confidence_score += 0.2
            if detected_intent:
                confidence_score += 0.1
            if entities:
                confidence_score += 0.1

            return IntentRecognitionResult(
                detected_intent=detected_intent,
                selected_mode=selected_mode,
                confidence_score=min(confidence_score, 1.0),
                extracted_entities=entities,
                requires_calculation=requires_calculation
            )

        except Exception as e:
            logger.warning(f"Failed to parse LLM intent response: {str(e)}")
            return IntentRecognitionResult(
                detected_intent="unknown",
                selected_mode=None,
                confidence_score=0.0,
                extracted_entities=[]
            )

    def _requires_calculation(self, intent_category: IntentCategory) -> bool:
        """Determine if the intent category requires calculation."""
        calculation_required = {
            IntentCategory.FACT_CHECK: True,
            IntentCategory.STRATEGY_EXPLORE: True,
            IntentCategory.PROJECTION: True,
            IntentCategory.SCENARIO_ANALYSIS: True,
            IntentCategory.CALCULATION_TEST: False,
            IntentCategory.COMPLIANCE_CHECK: False,
            IntentCategory.GENERAL_INQUIRY: False
        }
        return calculation_required.get(intent_category, False)

    def get_available_modes(self) -> List[Dict[str, Any]]:
        """Get information about available operational modes."""
        return [
            {
                "mode": mode.value,
                "category": self._get_mode_category(mode).value,
                "description": self._get_mode_description(mode)
            }
            for mode in OperationalMode
        ]

    def _get_mode_category(self, mode: OperationalMode) -> IntentCategory:
        """Get the intent category for a mode."""
        category_mapping = {
            # Fact Check modes
            OperationalMode.FACT_CHECK_TAX: IntentCategory.FACT_CHECK,
            OperationalMode.FACT_CHECK_WEALTH: IntentCategory.FACT_CHECK,
            OperationalMode.FACT_CHECK_RETIREMENT: IntentCategory.FACT_CHECK,
            OperationalMode.FACT_CHECK_INVESTMENT: IntentCategory.FACT_CHECK,
            OperationalMode.FACT_CHECK_GENERAL: IntentCategory.FACT_CHECK,

            # Strategy modes
            OperationalMode.STRATEGY_EXPLORE_PORTFOLIO: IntentCategory.STRATEGY_EXPLORE,
            OperationalMode.STRATEGY_EXPLORE_RETIREMENT: IntentCategory.STRATEGY_EXPLORE,
            OperationalMode.STRATEGY_EXPLORE_TAX: IntentCategory.STRATEGY_EXPLORE,
            OperationalMode.STRATEGY_EXPLORE_RISK: IntentCategory.STRATEGY_EXPLORE,
            OperationalMode.STRATEGY_EXPLORE_SCENARIO: IntentCategory.STRATEGY_EXPLORE,

            # Crystal Ball modes
            OperationalMode.CRYSTAL_BALL_PROJECTION: IntentCategory.PROJECTION,
            OperationalMode.CRYSTAL_BALL_SCENARIO: IntentCategory.SCENARIO_ANALYSIS,
            OperationalMode.CRYSTAL_BALL_SENSITIVITY: IntentCategory.SCENARIO_ANALYSIS,
            OperationalMode.CRYSTAL_BALL_STRESS_TEST: IntentCategory.SCENARIO_ANALYSIS,
            OperationalMode.CRYSTAL_BALL_MARKET_IMPACT: IntentCategory.SCENARIO_ANALYSIS,

            # Test modes
            OperationalMode.CALCULATION_HARNESS: IntentCategory.CALCULATION_TEST,
            OperationalMode.SCENARIO_FUZZER: IntentCategory.CALCULATION_TEST,
            OperationalMode.ADVICE_HARNESS: IntentCategory.CALCULATION_TEST,
        }
        return category_mapping.get(mode, IntentCategory.GENERAL_INQUIRY)

    def _get_mode_description(self, mode: OperationalMode) -> str:
        """Get human-readable description for a mode."""
        descriptions = {
            OperationalMode.FACT_CHECK_TAX: "Verify tax calculations and liability",
            OperationalMode.FACT_CHECK_WEALTH: "Calculate and verify net wealth",
            OperationalMode.FACT_CHECK_RETIREMENT: "Assess retirement readiness and projections",
            OperationalMode.FACT_CHECK_INVESTMENT: "Analyze investment portfolio performance",
            OperationalMode.STRATEGY_EXPLORE_SCENARIO: "Explore and compare financial scenarios",
            OperationalMode.CRYSTAL_BALL_PROJECTION: "Generate financial projections and forecasts",
            OperationalMode.CALCULATION_HARNESS: "Test and validate calculation engines",
        }
        return descriptions.get(mode, f"Execute {mode.value} operations")

    async def hydrate_state(self, user_query: str, current_state: dict, calc_id=None):
        """Not implemented - use StateHydrationEngine instead."""
        raise NotImplementedError("Use StateHydrationEngine for state hydration")

    async def generate_narrative(self, data: dict, template: str, calc_id=None):
        """Not implemented - use NarrativeGenerationEngine instead."""
        raise NotImplementedError("Use NarrativeGenerationEngine for narrative generation")


# Convenience functions
async def recognize_user_intent(
    user_query: str,
    context: Optional[Dict[str, Any]] = None
) -> IntentRecognitionResult:
    """
    Convenience function to recognize user intent.

    Args:
        user_query: User's natural language query
        context: Optional context information

    Returns:
        IntentRecognitionResult
    """
    engine = IntentRecognitionEngine()
    return await engine.recognize_intent(user_query, context)


def get_operational_modes() -> List[str]:
    """Get list of available operational mode identifiers."""
    return [mode.value for mode in OperationalMode]
