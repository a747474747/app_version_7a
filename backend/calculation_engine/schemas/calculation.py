"""
Core calculation schemas for Four-Engine Architecture.

This module defines CalculationState and ProjectionOutput models that serve
as the primary inputs and outputs for all CAL-* calculations.
"""

from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field

# Forward declarations for type hints - imported at runtime to avoid circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .entities import EntityContext
    from .assets import FinancialPositionContext
    from .cashflow import CashflowContext


class GlobalContext(BaseModel):
    """Global calculation context with rules and assumptions."""

    # Temporal context
    financial_year: int = Field(..., description="Income year for tax calculations (e.g., 2025)")
    effective_date: date = Field(..., description="Snapshot date for calculations")
    projection_years: int = Field(default=30, description="Years to project forward")

    # Geographic and regulatory context
    jurisdiction: str = Field(default="AU", description="Country/state jurisdiction (e.g., 'AU', 'NSW')")
    currency: str = Field(default="AUD", description="Base currency code")

    # Economic assumptions (Annual Rates)
    inflation_rate: Decimal = Field(..., ge=0, le=1, description="CPI inflation rate")
    wage_growth_rate: Decimal = Field(..., ge=0, le=1, description="Wage growth assumption")
    property_growth_rate: Decimal = Field(..., ge=-1, le=1, description="Property capital growth")
    equity_return_rate: Decimal = Field(..., ge=-1, le=1, description="Equity market return")
    fixed_income_return_rate: Decimal = Field(..., ge=0, le=1, description="Fixed income return")
    cash_return_rate: Decimal = Field(..., ge=0, le=1, description="Cash/bank return")
    discount_rate: Decimal = Field(..., description="Discount rate for NPV calculations")

    # Tax settings (Versioned via Rule Engine, loaded here)
    tax_brackets: List[Dict[str, Any]] = Field(..., description="Resident tax brackets")  # TODO: Import TaxBracket
    medicare_levy_rate: Decimal = Field(..., description="Medicare levy rate")
    medicare_levy_thresholds: Dict[str, Any] = Field(..., description="Medicare thresholds")  # TODO: Import MedicareThresholds

    # Superannuation settings
    concessional_cap: int = Field(..., description="Annual concessional contributions cap")
    non_concessional_cap: int = Field(..., description="Annual non-concessional cap")
    tbc_general_cap: int = Field(..., description="Transfer Balance Cap")

    # Precision and rounding
    precision_mode: str = Field(default="CENT", description="Rounding precision")  # TODO: Import PrecisionMode
    rounding_mode: str = Field(default="HALF_UP", description="Rounding strategy")  # TODO: Import RoundingMode


class AssumptionSet(BaseModel):
    """Named set of assumptions for scenario analysis."""
    id: str
    name: str
    version: str
    # Base assumptions (inherited from GlobalContext if None)
    inflation_rate: Optional[Decimal] = None
    # Stress test overrides
    stress_inflation_rate: Optional[Decimal] = None
    interest_rate_shock_flag: bool = False
    market_crash_flag: bool = False


class CalculatedIntermediariesContext(BaseModel):
    """Namespaced calculation results passed between CALs."""
    tax_results: Dict[str, Any] = Field(default_factory=dict)  # TODO: Import TaxResults
    super_results: Dict[str, Any] = Field(default_factory=dict)  # TODO: Import SuperResults
    property_results: Dict[str, Any] = Field(default_factory=dict)  # TODO: Import PropertyResults
    plan_level_results: Dict[str, Any] = Field(default_factory=dict)  # TODO: Import PlanLevelResults
    trace_log: List[Dict[str, Any]] = Field(default_factory=list)  # TODO: Import TraceEntry


class CalculationState(BaseModel):
    """Complete calculation input snapshot."""

    # Core contexts
    global_context: GlobalContext
    entity_context: "EntityContext"  # Contains list of Persons, Companies, etc.
    position_context: "FinancialPositionContext"  # Contains Assets, Loans, Insurance
    cashflow_context: "CashflowContext"  # Contains Income/Expense flows

    # Working state (populated by CALs)
    intermediates: CalculatedIntermediariesContext = Field(default_factory=CalculatedIntermediariesContext)

    # Metadata
    scenario_id: str
    assumption_set_id: str


class YearSnapshot(BaseModel):
    """Single year in projection timeline."""
    year_index: int
    financial_year: int
    position_snapshot: "FinancialPositionContext"  # Asset values at end of year
    intermediaries: CalculatedIntermediariesContext  # Flows/Tax during year


class ProjectionOutput(BaseModel):
    """Time-series projection results."""
    # Also referred to as ProjectionTimeline in functional specifications.
    base_state: CalculationState
    timeline: List[YearSnapshot] = Field(default_factory=list)


class ProjectionSummary(BaseModel):
    """Light-weight projection summary for Strategy Engine optimization loops.

    Avoids overhead of full object graph serialization.
    """
    scenario_id: str
    net_wealth_end: Decimal
    total_tax_paid: Decimal
    average_surplus: Decimal
    retirement_adequacy_score: float
    # Add other KPI fields as needed for optimization constraints
