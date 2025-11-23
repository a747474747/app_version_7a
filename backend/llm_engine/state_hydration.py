"""
State Hydration Module

This module provides patterns for converting natural language inputs to structured
CalculationState objects for the Four-Engine Architecture.

Key Responsibilities:
- Parse natural language financial data
- Convert to CalculationState schema
- Validate data completeness
- Generate clarification questions for missing data
- Maintain TraceLog integration

Author: AI Assistant
Created: 2025-11-22
Timezone: Australia/Brisbane (UTC+10)
"""

import json
import logging
import re
from decimal import Decimal
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from .orchestrator import LLMOrchestratorBase, StateHydrationResult
from ..calculation_engine.schemas.calculation import CalculationState, GlobalContext
from ..calculation_engine.schemas.entities import Person, EntityContext
from ..calculation_engine.schemas.assets import FinancialPositionContext, Asset, Loan
from ..calculation_engine.schemas.cashflow import CashflowContext, CashflowEntity

logger = logging.getLogger(__name__)


class StateHydrationEngine(LLMOrchestratorBase):
    """
    Engine for hydrating natural language inputs into CalculationState.

    This class uses LLM-powered parsing to extract financial data from user queries
    and convert them into structured CalculationState objects.
    """

    def __init__(self, specs_base_path: Optional[Path] = None):
        super().__init__(specs_base_path)
        self.hydration_prompt_id = "core-orchestrator-state-hydration"

    async def hydrate_state(
        self,
        user_query: str,
        current_state: Optional[Dict[str, Any]] = None,
        calc_id: Optional[str] = None
    ) -> StateHydrationResult:
        """
        Convert natural language input to structured CalculationState.

        Args:
            user_query: User's natural language financial description
            current_state: Optional existing state to update/merge
            calc_id: Optional CAL-* ID for tracking

        Returns:
            StateHydrationResult with structured data and validation info
        """
        try:
            # Prepare context for LLM
            context = {
                "user_query": user_query,
                "current_state": current_state or {},
                "timestamp": datetime.now().isoformat(),
                "hydration_rules": self._get_hydration_rules()
            }

            # Execute LLM operation
            llm_response = await self._execute_llm_operation(
                operation_name="state_hydration",
                prompt_id=self.hydration_prompt_id,
                messages=[{
                    "role": "user",
                    "content": f"Please convert this financial description to structured data:\n\n{user_query}"
                }],
                calc_id=calc_id,
                temperature=0.1,  # Low temperature for consistent parsing
                max_tokens=2000
            )

            # Parse LLM response
            parsed_data = self._parse_hydration_response(llm_response["content"])

            # Validate and enhance the parsed data
            validation_result = self._validate_hydrated_state(parsed_data)

            # Merge with existing state if provided
            if current_state:
                merged_data = self._merge_states(current_state, parsed_data)
            else:
                merged_data = parsed_data

            return StateHydrationResult(
                hydrated_state=merged_data,
                missing_fields=validation_result["missing_fields"],
                validation_errors=validation_result["errors"],
                confidence_score=self._calculate_confidence_score(validation_result),
                suggested_questions=self._generate_clarification_questions(validation_result["missing_fields"])
            )

        except Exception as e:
            logger.error(f"State hydration failed: {str(e)}")
            return StateHydrationResult(
                hydrated_state=current_state or {},
                missing_fields=[],
                validation_errors=[f"Hydration failed: {str(e)}"],
                confidence_score=0.0,
                suggested_questions=["Could you please rephrase your financial information?"]
            )

    def _get_hydration_rules(self) -> Dict[str, Any]:
        """Get the rules and schema for state hydration."""
        return {
            "required_fields": {
                "global_context": ["financial_year", "effective_date", "inflation_rate"],
                "entity_context": ["entities"],
                "position_context": ["assets", "liabilities"],
                "cashflow_context": ["flows"]
            },
            "data_types": {
                "currency_fields": ["salary", "income", "expenses", "asset_values", "loan_amounts"],
                "percentage_fields": ["rates", "growth_rates"],
                "date_fields": ["birth_date", "effective_date"],
                "integer_fields": ["financial_year", "projection_years"]
            },
            "validation_rules": {
                "currency_positive": True,
                "percentage_bounds": {"min": 0, "max": 1},
                "date_reasonable": {"min_year": 1900, "max_year": 2100}
            }
        }

    def _parse_hydration_response(self, llm_content: str) -> Dict[str, Any]:
        """
        Parse the LLM response into structured data.

        Args:
            llm_content: Raw LLM response content

        Returns:
            Parsed dictionary matching CalculationState structure
        """
        try:
            # Try to parse as JSON first
            if llm_content.strip().startswith('{'):
                return json.loads(llm_content)

            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', llm_content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))

            # Fallback: extract key-value pairs manually
            return self._extract_key_value_pairs(llm_content)

        except json.JSONDecodeError:
            logger.warning("Failed to parse LLM response as JSON, using fallback extraction")
            return self._extract_key_value_pairs(llm_content)

    def _extract_key_value_pairs(self, content: str) -> Dict[str, Any]:
        """Fallback extraction of key-value pairs from text."""
        extracted = {}

        # Common patterns to extract
        patterns = {
            "salary": r'(?:salary|income|earn(?:ing)?)\s+(?:of\s+)?(?:\$|AUD\s*)?([\d,]+(?:\.\d{2})?)',
            "age": r'age\s+(?:of\s+)?(\d+)',
            "financial_year": r'(?:financial\s+year|fy|year)\s+(\d{4})',
            "assets": r'(?:assets?|worth|net\s+worth)\s+(?:of\s+)?(?:\$|AUD\s*)?([\d,]+(?:\.\d{2})?)',
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                value = match.group(1).replace(',', '')
                if '.' in value:
                    extracted[field] = float(value)
                else:
                    extracted[field] = int(value)

        return extracted

    def _validate_hydrated_state(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the hydrated state and identify issues.

        Args:
            data: Parsed state data

        Returns:
            Validation result with missing fields and errors
        """
        missing_fields = []
        errors = []

        # Check required global context fields
        global_ctx = data.get("global_context", {})
        required_global = ["financial_year", "effective_date", "inflation_rate"]
        for field in required_global:
            if field not in global_ctx:
                missing_fields.append(f"global_context.{field}")

        # Check entity context
        entity_ctx = data.get("entity_context", {})
        if not entity_ctx.get("entities"):
            missing_fields.append("entity_context.entities")
        else:
            # Validate entities have required fields
            for i, entity in enumerate(entity_ctx["entities"]):
                if "name" not in entity:
                    missing_fields.append(f"entity_context.entities[{i}].name")
                if "type" not in entity:
                    missing_fields.append(f"entity_context.entities[{i}].type")

        # Check position context
        position_ctx = data.get("position_context", {})
        if not position_ctx.get("assets"):
            missing_fields.append("position_context.assets")

        # Check cashflow context
        cashflow_ctx = data.get("cashflow_context", {})
        if not cashflow_ctx.get("flows"):
            missing_fields.append("cashflow_context.flows")

        # Validate data types and ranges
        type_errors = self._validate_data_types(data)
        errors.extend(type_errors)

        return {
            "missing_fields": missing_fields,
            "errors": errors
        }

    def _validate_data_types(self, data: Dict[str, Any]) -> List[str]:
        """Validate data types and value ranges."""
        errors = []

        # Check currency fields are positive
        currency_paths = [
            "global_context.inflation_rate",
            "position_context.assets[*].value",
            "position_context.liabilities[*].amount",
            "cashflow_context.flows[*].salary_wages_gross"
        ]

        for path in currency_paths:
            try:
                value = self._get_nested_value(data, path)
                if value is not None and value < 0:
                    errors.append(f"Currency field {path} cannot be negative: {value}")
            except (KeyError, TypeError, IndexError):
                continue

        # Check percentage fields are between 0 and 1
        percentage_paths = [
            "global_context.inflation_rate",
            "global_context.wage_growth_rate"
        ]

        for path in percentage_paths:
            try:
                value = self._get_nested_value(data, path)
                if value is not None and not (0 <= value <= 1):
                    errors.append(f"Percentage field {path} must be between 0 and 1: {value}")
            except (KeyError, TypeError):
                continue

        return errors

    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get a nested value from a dictionary using dot notation."""
        keys = path.split('.')
        current = data

        for key in keys:
            if '[' in key and ']' in key:
                # Handle array indexing
                base_key, index_part = key.split('[', 1)
                index = int(index_part.rstrip(']'))
                current = current[base_key][index]
            else:
                current = current[key]

        return current

    def _merge_states(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new state data with existing state."""
        merged = existing.copy()

        # Deep merge dictionaries
        for key, value in new.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_states(merged[key], value)
            else:
                merged[key] = value

        return merged

    def _calculate_confidence_score(self, validation_result: Dict[str, Any]) -> float:
        """Calculate confidence score based on validation results."""
        missing_count = len(validation_result["missing_fields"])
        error_count = len(validation_result["errors"])

        # Base score starts at 1.0, reduced by issues
        base_score = 1.0
        penalty_per_missing = 0.1
        penalty_per_error = 0.2

        score = base_score - (missing_count * penalty_per_missing) - (error_count * penalty_per_error)
        return max(0.0, min(1.0, score))

    def _generate_clarification_questions(self, missing_fields: List[str]) -> List[str]:
        """Generate user-friendly questions for missing fields."""
        questions = []

        field_questions = {
            "global_context.financial_year": "What financial year are you planning for?",
            "global_context.effective_date": "What is the effective date for your financial situation?",
            "global_context.inflation_rate": "What inflation rate should we use for projections?",
            "entity_context.entities": "Could you tell me about the people/entities involved?",
            "position_context.assets": "What assets do you own?",
            "cashflow_context.flows": "What are your income and expense details?"
        }

        for field in missing_fields:
            if field in field_questions:
                questions.append(field_questions[field])
            else:
                # Generic question for unknown fields
                clean_field = field.replace('_', ' ').replace('.', ' ')
                questions.append(f"Could you provide more details about: {clean_field}?")

        return questions[:5]  # Limit to 5 questions to avoid overwhelming user

    async def recognize_intent(self, user_query: str, context=None):
        """Not implemented - use IntentRecognitionEngine instead."""
        raise NotImplementedError("Use IntentRecognitionEngine for intent recognition")

    async def generate_narrative(self, data: dict, template: str, calc_id=None):
        """Not implemented - use NarrativeGenerationEngine instead."""
        raise NotImplementedError("Use NarrativeGenerationEngine for narrative generation")


# Convenience function for easy access
async def hydrate_state_from_text(
    user_query: str,
    current_state: Optional[Dict[str, Any]] = None,
    calc_id: Optional[str] = None
) -> StateHydrationResult:
    """
    Convenience function to hydrate state from natural language text.

    Args:
        user_query: User's natural language description
        current_state: Optional existing state to update
        calc_id: Optional CAL-* ID for tracking

    Returns:
        StateHydrationResult
    """
    engine = StateHydrationEngine()
    return await engine.hydrate_state(user_query, current_state, calc_id)
