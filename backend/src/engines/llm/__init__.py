"""
LLM Orchestrator Engine.

This module handles interactions with Large Language Models for:
1. Intent Recognition
2. State Hydration
3. Narrative Generation
4. Strategy Nomination
"""

from typing import Optional, Dict, Any, List
import json
import os
from pydantic import BaseModel


# LLM Response Schemas (aligned with contracts/llm-orchestrator.yaml)
class IntentRecognitionResult(BaseModel):
    """Result of intent recognition."""
    detected_intent: str  # e.g., "fact_check", "strategy_explore", "scenario_compare"
    selected_mode: str  # Execution mode ID, e.g., "MODE-FACT-CHECK"
    confidence_score: float  # 0.0 to 1.0
    extracted_entities: Dict[str, Any]  # Parsed entities like amounts, dates, etc.
    clarification_questions: Optional[List[str]] = None
    requires_calculation: bool = False


class StateHydrationResult(BaseModel):
    """Result of state hydration."""
    hydrated_state: Dict[str, Any]  # Structured state fragments
    missing_fields: List[str]  # Fields that need clarification
    validation_errors: List[str]  # Data quality issues found
    confidence_score: float  # 0.0 to 1.0
    suggested_questions: List[str]  # Questions to ask user for missing data


class NarrativeGenerationResult(BaseModel):
    """Result of narrative generation."""
    narrative: str  # Human-readable text
    key_points: List[str]  # Bullet points of important information
    citations: List[Dict[str, Any]]  # References to rules/sources used
    confidence_score: float  # 0.0 to 1.0 in generation quality


class OrchestratorResponse(BaseModel):
    """Unified response schema for LLM Orchestrator operations."""
    success: bool
    result: Dict[str, Any]  # Operation-specific result data
    metadata: Dict[str, Any]  # Processing metadata, tokens used, etc.
    error_message: Optional[str] = None


class LLMOrchestrator:
    """
    Orchestrates LLM interactions.
    """
    
    def __init__(self):
        # TODO: Initialize LLM client (e.g., OpenAI, Anthropic)
        pass

    async def recognize_intent(self, user_query: str, context: Optional[Dict[str, Any]] = None) -> IntentRecognitionResult:
        """
        Analyze user query to determine intent using LLM-powered recognition.

        Returns structured IntentRecognitionResult aligned with LLM Orchestrator contract.

        MVP: Uses actual LLM calls for intent recognition (not simple keyword matching).
        TODO: Load intent-recognition prompt from specs/001-four-engine-architecture/llm-prompts/core-orchestrator/intent-recognition.md
        TODO: Make actual LLM API call to OpenRouter/Anthropic
        TODO: Parse and validate JSON response using IntentRecognitionResult schema
        """
        # TODO: Load intent-recognition prompt from specs/001-four-engine-architecture/llm-prompts/core-orchestrator/intent-recognition.md
        # TODO: Make actual LLM API call to OpenRouter/Anthropic
        # TODO: Parse and validate JSON response using IntentRecognitionResult schema

        # CURRENT MVP FALLBACK: Simple keyword matching until LLM integration is complete
        # This should be replaced with actual LLM calls in production
        query_lower = user_query.lower()

        if "tax" in query_lower or "payg" in query_lower:
            return IntentRecognitionResult(
                detected_intent="check_tax_liability",
                selected_mode="MODE-FACT-CHECK",
                confidence_score=0.9,
                extracted_entities={"tax": True, "income": True},
                requires_calculation=True
            )
        elif "wealth" in query_lower or "assets" in query_lower:
            return IntentRecognitionResult(
                detected_intent="check_net_wealth",
                selected_mode="MODE-FACT-CHECK",
                confidence_score=0.9,
                extracted_entities={"assets": True, "liabilities": True},
                requires_calculation=True
            )
        elif "super" in query_lower:
             return IntentRecognitionResult(
                detected_intent="check_super_balance",
                selected_mode="MODE-FACT-CHECK",
                confidence_score=0.9,
                extracted_entities={"superannuation": True},
                requires_calculation=True
            )

        return IntentRecognitionResult(
            detected_intent="unknown",
            selected_mode="",
            confidence_score=0.0,
            extracted_entities={},
            clarification_questions=["Could you please provide more details about your financial question?"]
        )

    async def hydrate_state(self, user_query: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract financial data from query to update state.
        """
        import re
        
        # Simple regex extraction for MVP (Replace with LLM extraction in future)
        # Matches "salary $100,000" or "income 100000"
        salary_match = re.search(r'(?:salary|income|earn)\s+(?:\$)?([\d,]+)', user_query.lower())
        
        if salary_match:
            amount_str = salary_match.group(1).replace(',', '')
            try:
                amount = float(amount_str) # Use float for intermediate, convert to Decimal in model
                
                # Assume updating the primary entity
                # This requires knowing the structure of current_state
                # We'll assume it matches CalculationState.model_dump()
                
                # Basic safety check for structure
                if "cashflow_context" in current_state and "flows" in current_state["cashflow_context"]:
                    flows = current_state["cashflow_context"]["flows"]
                    if flows:
                        # Update first entity found
                        first_entity_id = list(flows.keys())[0]
                        flows[first_entity_id]["salary_wages_gross"] = amount
                        
            except ValueError:
                pass
                
        return current_state

    async def generate_narrative(self, data: Dict[str, Any], template: str) -> NarrativeGenerationResult:
        """
        Generate human-readable explanation of data using LLM-powered narrative generation.

        Returns structured NarrativeGenerationResult aligned with LLM Orchestrator contract.

        MVP: Uses actual LLM calls for narrative generation (not simple templates).
        TODO: Load narrative-generation prompt from specs/001-four-engine-architecture/llm-prompts/core-orchestrator/narrative-generation.md
        TODO: Make actual LLM API call with structured context
        TODO: Parse and validate response using NarrativeGenerationResult schema
        """
        # TODO: Load narrative-generation prompt from specs/001-four-engine-architecture/llm-prompts/core-orchestrator/narrative-generation.md
        # TODO: Make actual LLM API call with structured context
        # TODO: Parse and validate response using NarrativeGenerationResult schema

        # CURRENT MVP FALLBACK: Simple templates until LLM integration is complete
        # This should be replaced with actual LLM calls in production

        if template == "check_tax_liability":
            narrative = f"Based on your inputs, your estimated tax liability is {data.get('tax_liability', 'calculated')}. This includes Medicare Levy."
            key_points = [
                "Tax calculated using current Australian tax rates",
                "Includes Medicare Levy assessment",
                "Based on your reported income and deductions"
            ]
        elif template == "check_net_wealth":
            narrative = f"Your calculated net wealth is {data.get('net_wealth', 'calculated')}. This is derived from your total assets minus liabilities."
            key_points = [
                "Net wealth = Total Assets - Total Liabilities",
                "Includes all reported financial positions",
                "Excludes contingent liabilities"
            ]
        else:
            narrative = "I have analyzed your financial data."
            key_points = ["Analysis completed successfully"]

        return NarrativeGenerationResult(
            narrative=narrative,
            key_points=key_points,
            citations=[],  # TODO: Add actual rule citations when LLM integrated
            confidence_score=0.8
        )

    def scrub_pii(self, text: str) -> str:
        """
        Remove PII from text before sending to external LLM.
        """
        # Simple placeholder for MVP
        # In production, use Microsoft Presidio or similar
        return text

# Global instance
llm_orchestrator = LLMOrchestrator()

