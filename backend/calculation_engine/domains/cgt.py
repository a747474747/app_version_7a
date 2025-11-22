"""
Capital Gains Tax Calculations - CAL-CGT-* functions.

This module contains calculations for capital gains tax, including:
- CAL-CGT-001: Capital gain/loss on asset disposal
- CAL-CGT-002: CGT discount for individuals
"""

from decimal import Decimal
from typing import Optional
from calculation_engine.schemas.calculation import CalculationState
from calculation_engine.schemas.orchestration import TraceEntry
from src.services.rule_loader import rule_loader

# Import calculation result schema
# TODO: This should be in shared/schemas once defined
class CalculationResult:
    """Result of a CAL execution."""
    def __init__(self, success: bool, value: Optional[Decimal], trace_entries: list[TraceEntry], error_message: Optional[str] = None):
        self.success = success
        self.value = value
        self.trace_entries = trace_entries
        self.error_message = error_message


def run_CAL_CGT_001(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Calculate capital gain/loss on asset disposal.
    CAL-CGT-001: Capital gain/loss on asset disposal
    """
    try:
        # This is a simplified implementation for a single asset disposal
        # In full implementation, this would iterate through asset disposals

        # For MVP, we'll assume asset disposal data is in the financial position context
        # This is a placeholder - real implementation would need asset disposal events
        capital_gain = Decimal("0")  # Placeholder

        # In a real scenario, this would calculate:
        # capital_gain = proceeds - (cost_base - reductions)

        trace_entry = TraceEntry(
            calc_id="CAL-CGT-001",
            entity_id=entity_id,
            field="capital_gain",
            explanation="Capital gain/loss calculated on asset disposal (MVP placeholder)",
            metadata={
                "proceeds": Decimal("0"),
                "cost_base": Decimal("0"),
                "capital_gain": capital_gain
            }
        )

        # Update state intermediates
        if "cgt_results" not in state.intermediates:
            state.intermediates.cgt_results = {}

        state.intermediates.cgt_results["capital_gain"] = capital_gain
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=capital_gain,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-CGT-001: {str(e)}"
        )


def run_CAL_CGT_002(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Apply CGT discount for individuals.
    CAL-CGT-002: CGT discount (individuals)
    """
    try:
        # Get capital gain from previous calculation
        capital_gain = state.intermediates.cgt_results.get("capital_gain", Decimal("0"))

        # Apply CGT discount for individuals (loaded from rules)
        discount_rate = rule_loader.get_cgt_discount_rate()
        cgt_discount = capital_gain * discount_rate
        discounted_gain = capital_gain - cgt_discount

        trace_entry = TraceEntry(
            calc_id="CAL-CGT-002",
            entity_id=entity_id,
            field="discounted_capital_gain",
            explanation=f"50% CGT discount applied to capital gain of {capital_gain}",
            metadata={
                "original_gain": capital_gain,
                "discount_rate": discount_rate,
                "discount_amount": cgt_discount,
                "discounted_gain": discounted_gain
            }
        )

        # Update state intermediates
        state.intermediates.cgt_results["discounted_gain"] = discounted_gain
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=discounted_gain,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-CGT-002: {str(e)}"
        )
