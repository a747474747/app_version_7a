"""
Personal Income Tax Calculations - CAL-PIT-* functions.

This module contains calculations for personal income tax, including:
- CAL-PIT-001: PAYG tax on taxable income
- CAL-PIT-002: Medicare levy
- CAL-PIT-004: Tax offsets (LITO)
- CAL-PIT-005: Net tax payable/refund
"""

from decimal import Decimal
from typing import Optional, Dict, Any, List
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


def run_CAL_PIT_001(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Calculate PAYG tax for residents.
    CAL-PIT-001: Personal Income Tax on taxable income (resident)
    """
    try:
        # Get entity cashflow
        if entity_id not in state.cashflow_context.flows:
            return CalculationResult(
                success=False,
                value=None,
                trace_entries=[],
                error_message=f"Entity {entity_id} not found in cashflow context"
            )

        cashflow = state.cashflow_context.flows[entity_id]

        # Calculate taxable income (simplified - assumes assessable income = salary/wages)
        assessable_income = cashflow.salary_wages_gross or Decimal("0")
        deductions = Decimal("0")  # Simplified - no deductions in MVP
        taxable_income = assessable_income - deductions

        # Load tax brackets from rules
        tax_brackets = rule_loader.get_tax_brackets()

        # Calculate tax using progressive brackets
        tax_payable = _calculate_progressive_tax(taxable_income, tax_brackets)

        # Create trace entry
        trace_entry = TraceEntry(
            calc_id="CAL-PIT-001",
            entity_id=entity_id,
            field="tax_payable",
            explanation=f"PAYG tax calculated for resident on taxable income of {taxable_income}",
            metadata={
                "assessable_income": assessable_income,
                "deductions": deductions,
                "taxable_income": taxable_income,
                "tax_brackets_applied": len(tax_brackets)
            }
        )

        # Update state intermediates
        if entity_id not in state.intermediates.tax_results:
            state.intermediates.tax_results[entity_id] = {}

        state.intermediates.tax_results[entity_id]["payg_tax"] = tax_payable
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=tax_payable,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-PIT-001: {str(e)}"
        )


def _calculate_progressive_tax(taxable_income: Decimal, tax_brackets: list) -> Decimal:
    """
    Calculate progressive tax using marginal tax brackets.

    Args:
        taxable_income: The income to tax
        tax_brackets: List of tax bracket dicts with 'min', 'max', 'rate' keys

    Returns:
        Total tax payable
    """
    if not tax_brackets:
        return Decimal("0")

    total_tax = Decimal("0")
    remaining_income = taxable_income

    for bracket in sorted(tax_brackets, key=lambda x: x.get('min', 0)):
        bracket_min = Decimal(str(bracket.get('min', 0)))
        bracket_max = Decimal(str(bracket.get('max', float('inf')))) if bracket.get('max') else Decimal('inf')
        rate = Decimal(str(bracket.get('rate', 0)))

        if remaining_income <= 0:
            break

        # Calculate tax for this bracket
        taxable_in_bracket = min(remaining_income, bracket_max - bracket_min)
        tax_in_bracket = taxable_in_bracket * rate

        total_tax += tax_in_bracket
        remaining_income -= taxable_in_bracket

    return total_tax


def run_CAL_PIT_002(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Calculate Medicare levy.
    CAL-PIT-002: Medicare levy on taxable income
    """
    try:
        # Get taxable income from previous calculations
        if entity_id not in state.intermediates.tax_results or "taxable_income" not in state.intermediates.tax_results[entity_id]:
            return CalculationResult(
                success=False,
                value=None,
                trace_entries=[],
                error_message=f"Taxable income not available for entity {entity_id}. Run CAL-PIT-001 first."
            )

        taxable_income = state.intermediates.tax_results[entity_id]["taxable_income"]

        # Get Medicare levy rate and thresholds from rules
        medicare_rate = rule_loader.get_medicare_levy_rate()
        thresholds = rule_loader.get_medicare_levy_thresholds()

        # Calculate Medicare levy with threshold
        threshold = Decimal(str(thresholds.get('single', 0)))  # Simplified - using single threshold
        medicare_levy = Decimal("0")

        if taxable_income > threshold:
            medicare_levy = (taxable_income - threshold) * medicare_rate

        # Create trace entry
        trace_entry = TraceEntry(
            calc_id="CAL-PIT-002",
            entity_id=entity_id,
            field="medicare_levy",
            explanation=f"Medicare levy calculated at {medicare_rate} on income above threshold of {threshold}",
            metadata={
                "taxable_income": taxable_income,
                "threshold": threshold,
                "rate": medicare_rate,
                "levy_payable": medicare_levy
            }
        )

        # Update state intermediates
        state.intermediates.tax_results[entity_id]["medicare_levy"] = medicare_levy
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=medicare_levy,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-PIT-002: {str(e)}"
        )


def run_CAL_PIT_004(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Aggregate tax offsets.
    CAL-PIT-004: Tax offsets aggregation
    """
    try:
        # In MVP, we'll implement basic LITO (Low Income Tax Offset)
        # More offsets can be added in extended calculations

        if entity_id not in state.intermediates.tax_results or "taxable_income" not in state.intermediates.tax_results[entity_id]:
            return CalculationResult(
                success=False,
                value=None,
                trace_entries=[],
                error_message=f"Taxable income not available for entity {entity_id}. Run CAL-PIT-001 first."
            )

        taxable_income = state.intermediates.tax_results[entity_id]["taxable_income"]

        # Calculate LITO (simplified)
        lito_amount = _calculate_lito(taxable_income)

        # Total offsets (just LITO in MVP)
        total_offsets = lito_amount

        # Create trace entry
        trace_entry = TraceEntry(
            calc_id="CAL-PIT-004",
            entity_id=entity_id,
            field="tax_offsets",
            explanation=f"Tax offsets aggregated including LITO of {lito_amount}",
            metadata={
                "lito_amount": lito_amount,
                "total_offsets": total_offsets,
                "taxable_income": taxable_income
            }
        )

        # Update state intermediates
        state.intermediates.tax_results[entity_id]["tax_offsets"] = total_offsets
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=total_offsets,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-PIT-004: {str(e)}"
        )


def _calculate_lito(taxable_income: Decimal) -> Decimal:
    """
    Calculate Low Income Tax Offset (LITO) using configured parameters.
    """
    lito_params = rule_loader.get_lito_parameters()

    max_offset = lito_params["max_offset"]
    income_limit = lito_params["income_limit"]
    phase_out_start = lito_params["phase_out_start"]
    phase_out_rate = lito_params["phase_out_rate"]

    if taxable_income <= income_limit:
        return max_offset
    elif taxable_income <= phase_out_start + ((max_offset / phase_out_rate)):
        # Phase out calculation
        excess = taxable_income - phase_out_start
        reduction = excess * phase_out_rate
        return max(Decimal("0"), max_offset - reduction)
    else:
        return Decimal("0")


def run_CAL_PIT_005(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Calculate net tax payable/refund.
    CAL-PIT-005: Net tax payable / refund
    """
    try:
        tax_results = state.intermediates.tax_results.get(entity_id, {})

        # Get required components
        payg_tax = tax_results.get("payg_tax", Decimal("0"))
        medicare_levy = tax_results.get("medicare_levy", Decimal("0"))
        tax_offsets = tax_results.get("tax_offsets", Decimal("0"))

        # Get PAYG withheld from cashflow
        cashflow = state.cashflow_context.flows.get(entity_id)
        payg_withheld = cashflow.payg_withheld if cashflow else Decimal("0")

        # Calculate gross tax
        gross_tax = payg_tax + medicare_levy

        # Apply offsets
        net_tax_before_withheld = gross_tax - tax_offsets

        # Calculate final tax position
        net_tax_payable = net_tax_before_withheld - payg_withheld

        # Determine if refund or payable
        is_refund = net_tax_payable < 0

        # Create trace entry
        trace_entry = TraceEntry(
            calc_id="CAL-PIT-005",
            entity_id=entity_id,
            field="net_tax_payable",
            explanation=f"Net tax position calculated: {'refund' if is_refund else 'payable'} of {abs(net_tax_payable)}",
            metadata={
                "gross_tax": gross_tax,
                "tax_offsets": tax_offsets,
                "payg_withheld": payg_withheld,
                "net_tax_before_withheld": net_tax_before_withheld,
                "final_position": net_tax_payable,
                "is_refund": is_refund
            }
        )

        # Update state intermediates
        state.intermediates.tax_results[entity_id]["net_tax_payable"] = net_tax_payable
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=net_tax_payable,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-PIT-005: {str(e)}"
        )
