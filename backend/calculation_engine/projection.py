"""
Projection Engine - Year-over-year financial projections.

This module implements the Projection Engine that takes a CalculationState
and projects it forward through time, applying growth rates, inflation,
and recalculating financial metrics for each year.
"""

from decimal import Decimal
from typing import List
from calculation_engine.schemas.calculation import (
    CalculationState,
    ProjectionOutput,
    YearSnapshot,
    CalculatedIntermediariesContext
)
from calculation_engine.schemas.orchestration import TraceEntry
from .registry import run_calculation


class ProjectionEngine:
    """Engine for projecting financial scenarios over multiple years."""

    def project_scenario(
        self,
        base_state: CalculationState,
        projection_years: int = 30
    ) -> ProjectionOutput:
        """
        Project a financial scenario forward through time.

        Args:
            base_state: The baseline calculation state (year 0)
            projection_years: Number of years to project forward

        Returns:
            ProjectionOutput with complete timeline
        """
        timeline: List[YearSnapshot] = []

        # Start with base state as year 0
        current_state = base_state.model_copy(deep=True)  # Deep copy to avoid mutations

        for year_index in range(projection_years + 1):  # Include year 0
            # Calculate financials for this year
            year_snapshot = self._calculate_year_snapshot(current_state, year_index)

            # Add to timeline
            timeline.append(year_snapshot)

            # Prepare for next year (if not the last year)
            if year_index < projection_years:
                current_state = self._advance_to_next_year(current_state, year_index)

        return ProjectionOutput(
            base_state=base_state,
            timeline=timeline
        )

    def _calculate_year_snapshot(
        self,
        state: CalculationState,
        year_index: int
    ) -> YearSnapshot:
        """
        Calculate all financial metrics for a specific year.

        Args:
            state: Calculation state for this year
            year_index: Which year this represents (0 = current year)

        Returns:
            YearSnapshot with calculated results
        """
        # Reset intermediates for this year's calculations
        state.intermediates = CalculatedIntermediariesContext()

        # Calculate tax metrics for each entity
        for entity_id in state.cashflow_context.flows.keys():
            self._calculate_entity_tax_metrics(state, entity_id, year_index)

        # Calculate superannuation metrics for each entity
        for entity_id in state.cashflow_context.flows.keys():
            self._calculate_entity_super_metrics(state, entity_id, year_index)

        # Create year snapshot
        return YearSnapshot(
            year_index=year_index,
            financial_year=state.global_context.financial_year + year_index,
            position_snapshot=state.position_context,  # Current position (would evolve in full implementation)
            intermediaries=state.intermediates
        )

    def _calculate_entity_tax_metrics(
        self,
        state: CalculationState,
        entity_id: str,
        year_index: int
    ):
        """Calculate tax-related metrics for an entity in a specific year."""
        # Run core tax calculations
        run_calculation("CAL-PIT-001", state, entity_id, year_index)  # PAYG tax
        run_calculation("CAL-PIT-002", state, entity_id, year_index)  # Medicare levy
        run_calculation("CAL-PIT-004", state, entity_id, year_index)  # Tax offsets
        run_calculation("CAL-PIT-005", state, entity_id, year_index)  # Net tax payable

    def _calculate_entity_super_metrics(
        self,
        state: CalculationState,
        entity_id: str,
        year_index: int
    ):
        """Calculate superannuation-related metrics for an entity in a specific year."""
        # Run core super calculations
        run_calculation("CAL-SUP-002", state, entity_id, year_index)  # Total concessional
        run_calculation("CAL-SUP-003", state, entity_id, year_index)  # Cap utilisation
        run_calculation("CAL-SUP-007", state, entity_id, year_index)  # Contributions tax
        run_calculation("CAL-SUP-008", state, entity_id, year_index)  # Div 293 tax
        run_calculation("CAL-SUP-009", state, entity_id, year_index)  # Net contribution

    def _advance_to_next_year(
        self,
        current_state: CalculationState,
        year_index: int
    ) -> CalculationState:
        """
        Advance the calculation state to the next year.

        This applies growth rates, inflation, and updates cashflows accordingly.
        """
        next_state = current_state.model_copy(deep=True)

        # Update global context for next year
        next_state.global_context.financial_year += 1

        # Apply inflation to cashflows
        inflation_rate = current_state.global_context.inflation_rate
        self._apply_inflation_to_cashflows(next_state, inflation_rate)

        # Apply wage growth
        wage_growth_rate = current_state.global_context.wage_growth_rate
        self._apply_wage_growth_to_cashflows(next_state, wage_growth_rate)

        # Apply property growth to assets
        property_growth_rate = current_state.global_context.property_growth_rate
        self._apply_property_growth_to_assets(next_state, property_growth_rate)

        # Apply investment returns
        equity_return_rate = current_state.global_context.equity_return_rate
        fixed_income_return_rate = current_state.global_context.fixed_income_return_rate
        self._apply_investment_returns_to_assets(next_state, equity_return_rate, fixed_income_return_rate)

        # Add trace entry for year advancement
        trace_entry = TraceEntry(
            calc_id="PROJECTION_ADVANCE",
            entity_id=None,  # Applies to all entities
            field="year_advancement",
            explanation=f"Advanced to year {year_index + 1} with growth rates applied",
            metadata={
                "from_year": current_state.global_context.financial_year,
                "to_year": next_state.global_context.financial_year,
                "inflation_rate": inflation_rate,
                "wage_growth_rate": wage_growth_rate,
                "property_growth_rate": property_growth_rate,
                "equity_return_rate": equity_return_rate
            }
        )
        next_state.intermediates.trace_log.append(trace_entry)

        return next_state

    def _apply_inflation_to_cashflows(self, state: CalculationState, inflation_rate: Decimal):
        """Apply inflation to cashflow amounts."""
        if inflation_rate == 0:
            return

        for entity_id, cashflow in state.cashflow_context.flows.items():
            # Inflate income and expenses (simplified)
            if hasattr(cashflow, 'salary_wages_gross'):
                cashflow.salary_wages_gross = (cashflow.salary_wages_gross * (1 + inflation_rate)).quantize(Decimal('0.01'))

    def _apply_wage_growth_to_cashflows(self, state: CalculationState, wage_growth_rate: Decimal):
        """Apply wage growth to salary income."""
        if wage_growth_rate == 0:
            return

        for entity_id, cashflow in state.cashflow_context.flows.items():
            # Apply wage growth on top of inflation
            if hasattr(cashflow, 'salary_wages_gross'):
                cashflow.salary_wages_gross = (cashflow.salary_wages_gross * (1 + wage_growth_rate)).quantize(Decimal('0.01'))

    def _apply_property_growth_to_assets(self, state: CalculationState, property_growth_rate: Decimal):
        """Apply property growth to property assets."""
        # Simplified - would need to iterate through actual property assets
        pass

    def _apply_investment_returns_to_assets(
        self,
        state: CalculationState,
        equity_return_rate: Decimal,
        fixed_income_return_rate: Decimal
    ):
        """Apply investment returns to investment assets."""
        # Simplified - would need to iterate through actual investment assets
        pass


# Global projection engine instance
projection_engine = ProjectionEngine()


def run_projection(base_state: CalculationState, projection_years: int = 30) -> ProjectionOutput:
    """
    Convenience function to run a projection.

    Args:
        base_state: The baseline calculation state
        projection_years: Number of years to project

    Returns:
        Complete projection output
    """
    return projection_engine.project_scenario(base_state, projection_years)
