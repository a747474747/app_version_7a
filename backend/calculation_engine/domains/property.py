"""
Property Investment Calculations - CAL-PFL-* functions.

This module contains calculations for property investment, including:
- CAL-PFL-104: Negative gearing tax benefit
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


def run_CAL_PFL_104(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Calculate negative gearing tax benefit (interest only).
    CAL-PFL-104: Negative gearing tax benefit
    """
    try:
        # Get property loan interest from financial position
        # This is a simplified implementation
        property_interest = Decimal("0")  # Placeholder - would come from loan data

        # Get rental income
        rental_income = Decimal("0")  # Placeholder - would come from property assets

        # Calculate deductible loss
        deductible_loss = property_interest - rental_income

        # Only calculate tax benefit if there's a loss
        tax_benefit = Decimal("0")

        # Load marginal tax rate from rules
        marginal_rate = rule_loader.get_marginal_tax_rate()

        if deductible_loss > 0:
            tax_benefit = deductible_loss * marginal_rate

        trace_entry = TraceEntry(
            calc_id="CAL-PFL-104",
            entity_id=entity_id,
            field="negative_gearing_benefit",
            explanation=f"Negative gearing tax benefit calculated: {tax_benefit}",
            metadata={
                "property_interest": property_interest,
                "rental_income": rental_income,
                "deductible_loss": deductible_loss,
                "marginal_rate": marginal_rate,
                "tax_benefit": tax_benefit
            }
        )

        # Update state intermediates
        if "property_results" not in state.intermediates:
            state.intermediates.property_results = {}

        state.intermediates.property_results["negative_gearing_benefit"] = tax_benefit
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=tax_benefit,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-PFL-104: {str(e)}"
        )
