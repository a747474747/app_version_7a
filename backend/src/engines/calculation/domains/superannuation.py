"""
Superannuation Calculations - CAL-SUP-* functions.

This module contains calculations for superannuation contributions and taxes, including:
- CAL-SUP-002: Total concessional contributions
- CAL-SUP-003: Concessional contributions cap utilisation
- CAL-SUP-007: Contributions tax inside super
- CAL-SUP-008: Division 293 additional tax
- CAL-SUP-009: Net contribution added to balance
"""

from decimal import Decimal
from typing import Optional
from shared.schemas.calculation import CalculationState
from shared.schemas.orchestration import TraceEntry
from services.rule_loader import rule_loader

# Import calculation result schema
# TODO: This should be in shared/schemas once defined
class CalculationResult:
    """Result of a CAL execution."""
    def __init__(self, success: bool, value: Optional[Decimal], trace_entries: list[TraceEntry], error_message: Optional[str] = None):
        self.success = success
        self.value = value
        self.trace_entries = trace_entries
        self.error_message = error_message


def run_CAL_SUP_002(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Calculate total concessional contributions.
    CAL-SUP-002: Total concessional contributions
    """
    try:
        # Get super contributions from cashflow
        cashflow = state.cashflow_context.flows.get(entity_id)
        if not cashflow:
            return CalculationResult(
                success=False,
                value=None,
                trace_entries=[],
                error_message=f"Cashflow not found for entity {entity_id}"
            )

        # Sum concessional contributions
        employer_sg = cashflow.super_employer_sg or Decimal("0")
        salary_sacrifice = cashflow.super_salary_sacrifice or Decimal("0")
        personal_deductible = cashflow.super_personal_deductible or Decimal("0")

        total_concessional = employer_sg + salary_sacrifice + personal_deductible

        trace_entry = TraceEntry(
            calc_id="CAL-SUP-002",
            entity_id=entity_id,
            field="total_concessional_contributions",
            explanation=f"Total concessional contributions calculated: {total_concessional}",
            metadata={
                "employer_sg": employer_sg,
                "salary_sacrifice": salary_sacrifice,
                "personal_deductible": personal_deductible,
                "total": total_concessional
            }
        )

        # Update state intermediates
        if "super_results" not in state.intermediates:
            state.intermediates.super_results = {}

        state.intermediates.super_results["total_concessional"] = total_concessional
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=total_concessional,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-SUP-002: {str(e)}"
        )


def run_CAL_SUP_003(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Check concessional contributions cap utilisation.
    CAL-SUP-003: Concessional contributions cap utilisation
    """
    try:
        total_concessional = state.intermediates.super_results.get("total_concessional", Decimal("0"))

        # Load concessional cap from rules
        concessional_cap = rule_loader.get_concessional_cap()

        utilised = total_concessional
        remaining = max(Decimal("0"), concessional_cap - utilised)
        excess = max(Decimal("0"), utilised - concessional_cap)

        trace_entry = TraceEntry(
            calc_id="CAL-SUP-003",
            entity_id=entity_id,
            field="concessional_cap_utilisation",
            explanation=f"Concessional cap utilisation: {utilised} of {concessional_cap} cap",
            metadata={
                "cap_limit": concessional_cap,
                "utilised": utilised,
                "remaining": remaining,
                "excess": excess
            }
        )

        # Update state intermediates
        state.intermediates.super_results["concessional_cap_utilised"] = utilised
        state.intermediates.super_results["concessional_cap_remaining"] = remaining
        state.intermediates.super_results["concessional_cap_excess"] = excess
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=utilised,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-SUP-003: {str(e)}"
        )


def run_CAL_SUP_007(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Calculate contributions tax inside super.
    CAL-SUP-007: Contributions tax inside super
    """
    try:
        total_concessional = state.intermediates.super_results.get("total_concessional", Decimal("0"))

        # Load contributions tax rate from rules
        contributions_tax_rate = rule_loader.get_contributions_tax_rate()
        contributions_tax = total_concessional * contributions_tax_rate

        trace_entry = TraceEntry(
            calc_id="CAL-SUP-007",
            entity_id=entity_id,
            field="contributions_tax",
            explanation=f"15% contributions tax calculated on concessional contributions",
            metadata={
                "concessional_contributions": total_concessional,
                "tax_rate": contributions_tax_rate,
                "tax_amount": contributions_tax
            }
        )

        # Update state intermediates
        state.intermediates.super_results["contributions_tax"] = contributions_tax
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=contributions_tax,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-SUP-007: {str(e)}"
        )


def run_CAL_SUP_008(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Calculate Division 293 additional tax.
    CAL-SUP-008: Division 293 additional tax
    """
    try:
        # Get adjusted taxable income (ATI) - simplified calculation
        tax_results = state.intermediates.tax_results.get(entity_id, {})
        taxable_income = tax_results.get("taxable_income", Decimal("0"))

        # Simplified ATI calculation (in reality more complex)
        ati = taxable_income

        # Load Division 293 parameters from rules
        div293_threshold = rule_loader.get_division_293_threshold()
        additional_rate = rule_loader.get_division_293_rate()

        additional_tax = Decimal("0")
        if ati > div293_threshold:
            # Tax on concessional contributions above threshold
            total_concessional = state.intermediates.super_results.get("total_concessional", Decimal("0"))
            additional_tax = total_concessional * additional_rate

        trace_entry = TraceEntry(
            calc_id="CAL-SUP-008",
            entity_id=entity_id,
            field="division_293_tax",
            explanation=f"Division 293 tax calculated for ATI of {ati}",
            metadata={
                "adjusted_taxable_income": ati,
                "threshold": div293_threshold,
                "additional_rate": additional_rate,
                "additional_tax": additional_tax
            }
        )

        # Update state intermediates
        state.intermediates.super_results["division_293_tax"] = additional_tax
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=additional_tax,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-SUP-008: {str(e)}"
        )


def run_CAL_SUP_009(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Calculate net contribution added to balance.
    CAL-SUP-009: Net contribution added to balance
    """
    try:
        total_concessional = state.intermediates.super_results.get("total_concessional", Decimal("0"))
        contributions_tax = state.intermediates.super_results.get("contributions_tax", Decimal("0"))
        division_293_tax = state.intermediates.super_results.get("division_293_tax", Decimal("0"))

        # Calculate net addition to super balance
        total_taxes = contributions_tax + division_293_tax
        net_contribution = total_concessional - total_taxes

        trace_entry = TraceEntry(
            calc_id="CAL-SUP-009",
            entity_id=entity_id,
            field="net_super_contribution",
            explanation=f"Net super contribution calculated after taxes: {net_contribution}",
            metadata={
                "gross_contributions": total_concessional,
                "contributions_tax": contributions_tax,
                "division_293_tax": division_293_tax,
                "total_taxes": total_taxes,
                "net_contribution": net_contribution
            }
        )

        # Update state intermediates
        state.intermediates.super_results["net_contribution"] = net_contribution
        state.intermediates.trace_log.append(trace_entry)

        return CalculationResult(
            success=True,
            value=net_contribution,
            trace_entries=[trace_entry]
        )

    except Exception as e:
        return CalculationResult(
            success=False,
            value=None,
            trace_entries=[],
            error_message=f"Error in CAL-SUP-009: {str(e)}"
        )
