"""
Narrative Generation Module

This module provides patterns for converting structured calculation results into
human-readable narratives for the Four-Engine Architecture.

Key Responsibilities:
- Generate natural language explanations of calculation results
- Create contextual narratives for different user scenarios
- Provide citations and references to calculation rules
- Maintain appropriate confidence scoring
- Support multiple narrative templates and styles

Author: AI Assistant
Created: 2025-11-22
Timezone: Australia/Brisbane (UTC+10)
"""

import logging
import re
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from .orchestrator import LLMOrchestratorBase, NarrativeGenerationResult
from ..calculation_engine.schemas.calculation import ProjectionOutput, ProjectionSummary

logger = logging.getLogger(__name__)


class NarrativeGenerationEngine(LLMOrchestratorBase):
    """
    Engine for generating human-readable narratives from calculation results.

    This class uses LLM-powered generation to create contextual, understandable
    explanations of complex financial calculation results.
    """

    def __init__(self, specs_base_path: Optional[Path] = None):
        super().__init__(specs_base_path)
        self.narrative_prompt_id = "core-orchestrator-narrative-generation"

    async def generate_narrative(
        self,
        data: Union[Dict[str, Any], ProjectionOutput, ProjectionSummary],
        template: str = "default",
        calc_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> NarrativeGenerationResult:
        """
        Generate human-readable narrative from calculation data.

        Args:
            data: Structured calculation results (dict, ProjectionOutput, or ProjectionSummary)
            template: Narrative template to use
            calc_id: Optional CAL-* ID for tracking
            context: Additional context for narrative generation

        Returns:
            NarrativeGenerationResult with human-readable explanation
        """
        try:
            # Convert data to dictionary if needed
            if hasattr(data, 'model_dump'):
                data_dict = data.model_dump()
            elif isinstance(data, dict):
                data_dict = data
            else:
                data_dict = {"raw_data": str(data)}

            # Prepare context for LLM
            generation_context = {
                "data": data_dict,
                "template": template,
                "user_context": context or {},
                "narrative_rules": self._get_narrative_rules(template),
                "timestamp": self._get_current_timestamp()
            }

            # Select appropriate prompt based on template
            prompt_id = self._get_template_prompt_id(template)

            # Create user message with structured data
            user_message = self._format_data_for_narrative(data_dict, template, context)

            # Execute LLM operation
            llm_response = await self._execute_llm_operation(
                operation_name=f"narrative_generation_{template}",
                prompt_id=prompt_id,
                messages=[{"role": "user", "content": user_message}],
                calc_id=calc_id,
                temperature=0.3,  # Moderate temperature for natural but consistent language
                max_tokens=1500
            )

            # Parse and structure the narrative response
            narrative_data = self._parse_narrative_response(llm_response["content"])

            return NarrativeGenerationResult(
                narrative=narrative_data["narrative"],
                key_points=narrative_data["key_points"],
                citations=narrative_data["citations"],
                confidence_score=narrative_data["confidence_score"]
            )

        except Exception as e:
            logger.error(f"Narrative generation failed: {str(e)}")
            return self._generate_fallback_narrative(data, template, str(e))

    def _get_narrative_rules(self, template: str) -> Dict[str, Any]:
        """Get narrative generation rules for the specified template."""
        base_rules = {
            "tone": "professional",
            "audience": "financial_adviser",
            "complexity": "intermediate",
            "citations_required": True,
            "confidence_scoring": True
        }

        template_rules = {
            "tax_liability": {
                "focus": "tax_calculation",
                "key_elements": ["taxable_income", "tax_brackets", "deductions", "credits"],
                "audience": "tax_adviser"
            },
            "net_wealth": {
                "focus": "balance_sheet",
                "key_elements": ["assets", "liabilities", "equity", "changes"],
                "audience": "wealth_adviser"
            },
            "retirement_projection": {
                "focus": "long_term_planning",
                "key_elements": ["current_balance", "contributions", "growth", "adequacy"],
                "audience": "retirement_planner"
            },
            "investment_scenario": {
                "focus": "scenario_comparison",
                "key_elements": ["returns", "risk", "comparison", "recommendations"],
                "audience": "investment_adviser"
            }
        }

        rules = base_rules.copy()
        if template in template_rules:
            rules.update(template_rules[template])

        return rules

    def _get_template_prompt_id(self, template: str) -> str:
        """Get the appropriate prompt ID for the template."""
        template_prompts = {
            "tax_liability": "core-orchestrator-narrative-generation-tax",
            "net_wealth": "core-orchestrator-narrative-generation-wealth",
            "retirement_projection": "core-orchestrator-narrative-generation-retirement",
            "investment_scenario": "core-orchestrator-narrative-generation-investment"
        }

        return template_prompts.get(template, self.narrative_prompt_id)

    def _format_data_for_narrative(
        self,
        data: Dict[str, Any],
        template: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Format calculation data for narrative generation."""
        formatted_sections = []

        # Add context information
        if context:
            formatted_sections.append(f"Context: {context}")

        # Add template-specific data formatting
        if template == "tax_liability":
            formatted_sections.append(self._format_tax_data(data))
        elif template == "net_wealth":
            formatted_sections.append(self._format_wealth_data(data))
        elif template == "retirement_projection":
            formatted_sections.append(self._format_retirement_data(data))
        else:
            formatted_sections.append(f"Data: {data}")

        # Add generation instructions
        instructions = f"""
Please generate a clear, professional narrative explaining these {template.replace('_', ' ')} results.
Focus on the key insights and implications for financial planning.
Include specific numbers and cite the calculation methods used.
"""

        formatted_sections.append(instructions)

        return "\n\n".join(formatted_sections)

    def _format_tax_data(self, data: Dict[str, Any]) -> str:
        """Format tax calculation data for narrative generation."""
        sections = ["Tax Calculation Data:"]

        # Extract key tax figures
        tax_results = data.get("intermediates", {}).get("tax_results", {})
        global_ctx = data.get("global_context", {})

        if tax_results:
            sections.append(f"- Taxable Income: ${tax_results.get('taxable_income', 'N/A')}")
            sections.append(f"- Tax Liability: ${tax_results.get('total_tax', 'N/A')}")
            sections.append(f"- Effective Rate: {tax_results.get('effective_rate', 'N/A')}%")

        sections.append(f"- Financial Year: {global_ctx.get('financial_year', 'N/A')}")

        return "\n".join(sections)

    def _format_wealth_data(self, data: Dict[str, Any]) -> str:
        """Format wealth/balance sheet data for narrative generation."""
        sections = ["Net Wealth Data:"]

        position_ctx = data.get("position_context", {})
        assets = position_ctx.get("assets", [])
        liabilities = position_ctx.get("liabilities", [])

        total_assets = sum(float(asset.get("value", 0)) for asset in assets)
        total_liabilities = sum(float(liability.get("amount", 0)) for liability in liabilities)
        net_wealth = total_assets - total_liabilities

        sections.append(f"- Total Assets: ${total_assets:,.2f}")
        sections.append(f"- Total Liabilities: ${total_liabilities:,.2f}")
        sections.append(f"- Net Wealth: ${net_wealth:,.2f}")

        return "\n".join(sections)

    def _format_retirement_data(self, data: Dict[str, Any]) -> str:
        """Format retirement projection data for narrative generation."""
        sections = ["Retirement Projection Data:"]

        # This would extract retirement-specific metrics
        # For now, provide a basic structure
        sections.append("- Current superannuation balance")
        sections.append("- Projected retirement income")
        sections.append("- Retirement adequacy assessment")

        return "\n".join(sections)

    def _parse_narrative_response(self, llm_content: str) -> Dict[str, Any]:
        """
        Parse the LLM narrative response into structured components.

        Args:
            llm_content: Raw LLM response

        Returns:
            Dictionary with narrative, key_points, citations, confidence_score
        """
        try:
            # Default structure
            result = {
                "narrative": llm_content.strip(),
                "key_points": [],
                "citations": [],
                "confidence_score": 0.8
            }

            # Try to extract structured elements
            lines = llm_content.split('\n')

            # Look for key points (bullet points or numbered lists)
            key_points = []
            citations = []

            for line in lines:
                line = line.strip()
                if line.startswith(('- ', '• ', '* ', '1. ', '2. ', '3. ')):
                    # Extract key point
                    clean_point = re.sub(r'^[-•*]\s*|\d+\.\s*', '', line)
                    if clean_point:
                        key_points.append(clean_point)
                elif 'CAL-' in line or 'rule' in line.lower():
                    # Extract citation
                    citations.append({
                        "reference": line.strip(),
                        "type": "calculation_rule"
                    })

            if key_points:
                result["key_points"] = key_points[:5]  # Limit to 5 key points

            if citations:
                result["citations"] = citations[:3]  # Limit to 3 citations

            return result

        except Exception as e:
            logger.warning(f"Failed to parse narrative response: {str(e)}")
            return {
                "narrative": llm_content.strip(),
                "key_points": [],
                "citations": [],
                "confidence_score": 0.7
            }

    def _generate_fallback_narrative(
        self,
        data: Union[Dict[str, Any], ProjectionOutput, ProjectionSummary],
        template: str,
        error: str
    ) -> NarrativeGenerationResult:
        """Generate a fallback narrative when LLM generation fails."""
        return NarrativeGenerationResult(
            narrative=f"I have analyzed your {template.replace('_', ' ')} information, but encountered an issue generating the detailed explanation: {error}",
            key_points=[
                "Analysis completed with limitations",
                "Please review the raw calculation results",
                "Consider providing additional context for better explanations"
            ],
            citations=[],
            confidence_score=0.3
        )

    def _get_current_timestamp(self) -> str:
        """Get current timestamp for narrative context."""
        from datetime import datetime
        return datetime.now().isoformat()

    async def recognize_intent(self, user_query: str, context=None):
        """Not implemented - use IntentRecognitionEngine instead."""
        raise NotImplementedError("Use IntentRecognitionEngine for intent recognition")

    async def hydrate_state(self, user_query: str, current_state: dict, calc_id=None):
        """Not implemented - use StateHydrationEngine instead."""
        raise NotImplementedError("Use StateHydrationEngine for state hydration")


# Convenience functions for common narrative types
async def generate_tax_narrative(
    tax_data: Dict[str, Any],
    calc_id: Optional[str] = None
) -> NarrativeGenerationResult:
    """Generate tax liability narrative."""
    engine = NarrativeGenerationEngine()
    return await engine.generate_narrative(tax_data, "tax_liability", calc_id)


async def generate_wealth_narrative(
    wealth_data: Dict[str, Any],
    calc_id: Optional[str] = None
) -> NarrativeGenerationResult:
    """Generate net wealth narrative."""
    engine = NarrativeGenerationEngine()
    return await engine.generate_narrative(wealth_data, "net_wealth", calc_id)


async def generate_retirement_narrative(
    retirement_data: Dict[str, Any],
    calc_id: Optional[str] = None
) -> NarrativeGenerationResult:
    """Generate retirement projection narrative."""
    engine = NarrativeGenerationEngine()
    return await engine.generate_narrative(retirement_data, "retirement_projection", calc_id)
