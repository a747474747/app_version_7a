"""
Asset, liability, and insurance schemas for Four-Engine Architecture.

This module defines PropertyAsset, SuperAccount, Loan, InsurancePolicy models
and the FinancialPositionContext that aggregates them.
"""

from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field

# TODO: Import proper enum types from external model files
AssetType = Literal["HOME", "INVESTMENT_RESIDENTIAL", "COMMERCIAL", "SUPER_INDUSTRY", "SUPER_RETAIL", "SUPER_SMSF", "CASH", "SHARES", "BONDS", "OTHER"]


class ValuationSnapshot(BaseModel):
    """Point-in-time asset or liability valuation."""
    amount: Decimal
    currency: str = "AUD"
    effective_date: date
    source: Literal["CLIENT_ESTIMATE", "BANK_FEED", "SYSTEM_PROJECTION"] = "CLIENT_ESTIMATE"


class Ownership(BaseModel):
    """Ownership share in an asset or liability."""
    entity_id: str
    share: Decimal = Field(..., ge=0, le=1)


class Asset(BaseModel):
    """Base asset model."""
    id: str
    asset_type: AssetType
    ownership: List[Ownership]
    valuations: List[ValuationSnapshot] = Field(..., min_items=1)
    linked_entity_id: Optional[str] = None  # Links to related entity (e.g., SMSF for member balances)

    @property
    def current_valuation(self) -> ValuationSnapshot:
        return max(self.valuations, key=lambda v: v.effective_date)


class PropertyAsset(Asset):
    """Real property asset."""
    asset_type: Literal["HOME", "INVESTMENT_RESIDENTIAL", "COMMERCIAL"]
    state_territory: str  # For Stamp Duty/Land Tax
    acquisition_date: date
    cost_base: Decimal
    is_main_residence: bool = False
    land_value: Optional[Decimal] = None  # Critical for Land Tax

    # Rental information
    rental_status: Literal["OWNER_OCCUPIED", "RENTED", "HOLIDAY"] = "OWNER_OCCUPIED"
    weekly_rent: Optional[Decimal] = None
    expected_occupancy_rate: Decimal = Field(default=1.0, ge=0, le=1)

    # Expenses
    council_rates: Decimal = Field(default=0)
    body_corporate_fees: Decimal = Field(default=0)
    landlord_insurance: Decimal = Field(default=0)
    maintenance: Decimal = Field(default=0)  # Regular maintenance and repairs
    management_fees: Decimal = Field(default=0)  # Property management fees
    other_recurring_expenses: Decimal = Field(default=0)  # Other ongoing costs


class SuperAccount(BaseModel):
    """Superannuation account."""
    id: str
    owner_person_id: str
    fund_type: Literal["INDUSTRY", "RETAIL", "SMSF"]
    phase: Literal["ACCUMULATION", "PENSION"]

    # Balances
    balance_current: Decimal = Field(ge=0)
    taxable_component: Decimal = Field(ge=0)
    tax_free_component: Decimal = Field(ge=0)
    preserved_amount: Decimal = Field(ge=0)

    # Investment allocation
    investment_option: Dict[str, Decimal]  # asset_class -> proportion


class Loan(BaseModel):
    """Loan or debt obligation."""
    id: str
    linked_asset_id: Optional[str] = None
    borrower_entity_ids: List[str]
    loan_type: Literal["HOME", "INVESTMENT", "PERSONAL", "CREDIT_CARD"]

    # Balances
    principal_outstanding: Decimal = Field(ge=0)
    offset_balance: Decimal = Field(default=0, ge=0)
    redraw_balance: Decimal = Field(default=0, ge=0)

    # Interest terms
    interest_rate_current: Decimal = Field(ge=0, le=1)
    interest_rate_type: Literal["VARIABLE", "FIXED"] = "VARIABLE"

    # Term details
    remaining_term_years: Decimal = Field(ge=0)

    # Repayment
    repayment_frequency: Literal["WEEKLY", "FORTNIGHTLY", "MONTHLY"] = "MONTHLY"
    repayment_amount: Decimal = Field(ge=0)
    interest_only_flag: bool = False

    # Stress Testing
    stress_buffer_rate: Optional[Decimal] = None  # +3% buffer if applied by engine/assumption set

    @property
    def annual_interest_expense(self) -> Decimal:
        """Calculate annual interest expense for this loan."""
        if self.interest_only_flag:
            # Interest-only loan: all repayments are interest
            frequency_factor = 12 if self.repayment_frequency == "MONTHLY" else 26 if self.repayment_frequency == "FORTNIGHTLY" else 52
            return self.repayment_amount * Decimal(frequency_factor)
        else:
            # Principal + interest loan: calculate interest portion
            # Simplified calculation: interest = principal * rate / frequency_factor
            frequency_factor = 12 if self.repayment_frequency == "MONTHLY" else 26 if self.repayment_frequency == "FORTNIGHTLY" else 52
            periodic_interest = (self.principal_outstanding * self.interest_rate_current) / frequency_factor
            return periodic_interest * Decimal(frequency_factor)  # Annualize


class InsurancePolicy(BaseModel):
    """Personal insurance policy."""
    id: str
    owner_entity_id: str  # Can be Person or Super Fund
    insured_person_id: str
    cover_type: Literal["LIFE", "TPD", "TRAUMA", "IP"]

    # Benefits
    sum_insured: Decimal = Field(ge=0)  # For Life/TPD/Trauma
    monthly_benefit: Optional[Decimal] = None  # For IP
    waiting_period_days: Optional[int] = None  # For IP
    benefit_period_years: Optional[int] = None  # For IP (e.g., 2, 5, 65)

    # Premiums
    premium_amount: Decimal = Field(ge=0)
    premium_frequency: Literal["MONTHLY", "ANNUAL"]
    premium_basis: Literal["STEPPED", "LEVEL"]
    tax_deductible_flag: bool = False


class FinancialPositionContext(BaseModel):
    """Complete financial position including assets, liabilities, and insurance."""
    assets: Dict[str, Asset] = Field(default_factory=dict)  # All assets keyed by asset_id
    loans: Dict[str, Loan] = Field(default_factory=dict)  # All loans keyed by loan_id
    insurance_policies: Dict[str, InsurancePolicy] = Field(default_factory=dict)  # All policies keyed by policy_id

    @property
    def net_worth(self) -> Decimal:
        """Calculate total net worth across all assets and liabilities."""
        total_assets = sum(asset.current_valuation.amount for asset in self.assets.values())
        total_liabilities = sum(loan.principal_outstanding for loan in self.loans.values())
        return total_assets - total_liabilities
