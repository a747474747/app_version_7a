"""
Cashflow schemas for Four-Engine Architecture.

This module defines EntityCashflow and CashflowContext models for
income, expenses, and cashflow calculations.
"""

from decimal import Decimal
from typing import Dict, Optional
from pydantic import BaseModel, Field

# Forward declaration - will be imported in __init__.py
from .entities import HouseholdBudget


class EntityCashflow(BaseModel):
    """Cashflows for a specific person or legal entity."""
    entity_id: str

    # Employment income
    salary_wages_gross: Decimal = Field(default=0)
    salary_sacrifice_super: Decimal = Field(default=0)
    bonus_gross: Decimal = Field(default=0)
    allowances_gross: Decimal = Field(default=0)
    reportable_fringe_benefits: Decimal = Field(default=0)

    # Investment income
    interest_income: Decimal = Field(default=0)
    dividend_unfranked: Decimal = Field(default=0)
    dividend_franked: Decimal = Field(default=0)
    dividend_franking_credits: Decimal = Field(default=0)
    rental_income_gross: Decimal = Field(default=0)
    foreign_income: Decimal = Field(default=0)
    foreign_tax_paid: Decimal = Field(default=0)  # Foreign Tax Credits

    # Deductions
    work_related_expenses: Decimal = Field(default=0)
    personal_super_contributions: Decimal = Field(default=0)  # Concessional
    interest_deductions: Decimal = Field(default=0)

    # Super contributions
    employer_super_guarantee: Decimal = Field(default=0)
    personal_non_concessional_contributions: Decimal = Field(default=0)
    spouse_contributions_received: Decimal = Field(default=0)
    downsizer_contributions: Decimal = Field(default=0)


class CashflowContext(BaseModel):
    """Complete cashflow context."""
    flows: Dict[str, EntityCashflow] = Field(default_factory=dict)  # Keyed by entity_id
    shared_budget: Optional[HouseholdBudget] = None
