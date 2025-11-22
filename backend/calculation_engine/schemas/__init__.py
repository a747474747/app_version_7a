"""
Shared schemas for Four-Engine Architecture.

This package provides Pydantic models for the entire four-engine system,
organized by domain: calculation, entities, assets, cashflow, and orchestration.
"""

# Import base models first
from .entities import (
    EntityContext,
    Person,
    Relationship,
    HouseholdBudget,
    CompanyEntity,
    TrustEntity,
    SMSFEntity,
)

from .assets import (
    FinancialPositionContext,
    Asset,
    PropertyAsset,
    SuperAccount,
    Loan,
    InsurancePolicy,
    ValuationSnapshot,
    Ownership,
)

from .cashflow import (
    CashflowContext,
    EntityCashflow,
)

from .orchestration import (
    TraceEntry,
    TraceLog,
    Strategy,
    AdviceOutcome,
)

# Import calculation models (depends on others)
from .calculation import (
    GlobalContext,
    AssumptionSet,
    CalculatedIntermediariesContext,
    CalculationState,
    YearSnapshot,
    ProjectionOutput,
    ProjectionSummary,
)

# Export all models
__all__ = [
    # Entities
    "EntityContext",
    "Person",
    "Relationship",
    "HouseholdBudget",
    "CompanyEntity",
    "TrustEntity",
    "SMSFEntity",

    # Assets & Liabilities
    "FinancialPositionContext",
    "Asset",
    "PropertyAsset",
    "SuperAccount",
    "Loan",
    "InsurancePolicy",
    "ValuationSnapshot",
    "Ownership",

    # Cashflow
    "CashflowContext",
    "EntityCashflow",

    # Orchestration
    "TraceEntry",
    "TraceLog",
    "Strategy",
    "AdviceOutcome",

    # Calculation
    "GlobalContext",
    "AssumptionSet",
    "CalculatedIntermediariesContext",
    "CalculationState",
    "YearSnapshot",
    "ProjectionOutput",
    "ProjectionSummary",
]
