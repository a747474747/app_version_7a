"""
Entity schemas for Four-Engine Architecture.

This module defines Person entities, legal entities (companies, trusts, SMSFs),
and context classes that aggregate entities for calculations.
"""

from datetime import date
from math import floor
from decimal import Decimal
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field

# TODO: Import proper enum types from external model files
PersonRole = Literal["PRIMARY", "PARTNER", "DEPENDANT"]
Sex = Literal["M", "F", "OTHER"]
ResidencyStatus = Literal["RESIDENT", "NON_RESIDENT", "TEMPORARY"]
WorkStatus = Literal["FULL_TIME", "PART_TIME", "UNEMPLOYED", "STUDENT", "RETIRED"]
RelationshipType = Literal["SPOUSE", "CHILD", "PARENT", "SIBLING", "OTHER"]


class Relationship(BaseModel):
    """Relationship between persons."""
    target_person_id: str
    type: RelationshipType  # spouse, child, parent
    financial_dependence: Decimal = Field(0.0, ge=0.0, le=1.0)


class Person(BaseModel):
    """Individual person as a financial actor."""

    id: str = Field(..., description="Unique person identifier")
    role: PersonRole = Field(..., description="Role in household: primary, partner, dependant")

    # Demographics
    date_of_birth: date
    sex: Optional[Sex] = None  # For actuarial tables
    residency_status: ResidencyStatus = Field(default="RESIDENT")  # resident, non_resident, temporary
    work_status: WorkStatus = Field(default="FULL_TIME")

    # Risk Profile
    smoker_status: Optional[bool] = None
    occupation_risk_band: Optional[str] = None  # For insurance calc

    # Social Security Attributes
    residency_qualifying_years: Optional[int] = Field(default=0)
    age_pension_age_reached_flag: Optional[bool] = False

    # Relationships
    relationships: List[Relationship] = Field(default_factory=list)

    # Derived fields (calculated runtime helpers)
    def age_at(self, at_date: date) -> int:
        return floor((at_date - self.date_of_birth).days / 365.25)


class HouseholdBudget(BaseModel):
    """Shared household expenses not owned by specific entities."""

    household_id: str

    # Housing and utilities
    housing_expenses: Decimal = Field(default=0, ge=0)  # Rent or Board (Mortgages are Liabilities)
    utilities_expenses: Decimal = Field(default=0, ge=0)

    # Living expenses
    food_groceries_expenses: Decimal = Field(default=0, ge=0)
    medical_health_expenses: Decimal = Field(default=0, ge=0)
    children_education_expenses: Decimal = Field(default=0, ge=0)
    insurance_premiums_general: Decimal = Field(default=0, ge=0)  # Home/Contents, not Personal
    discretionary_expenses: Decimal = Field(default=0, ge=0)

    # Allocation strategy
    # Defines how these shared costs are split for individual surplus calcs
    allocation_strategy: Literal["EQUAL_SPLIT", "PRO_RATA_GROSS", "PRIMARY_ABSORBS"] = "EQUAL_SPLIT"


class CompanyEntity(BaseModel):
    """Corporate entity for business ownership and taxation."""
    id: str
    name: str
    aggregated_turnover: Decimal = Field(ge=0)
    base_rate_entity_flag: bool = False
    company_tax_rate: Decimal = Field(default=0.30, ge=0, le=1)
    franked_dividends_paid: Decimal = Field(default=0)
    franking_account_balance: Decimal = Field(default=0)


class TrustEntity(BaseModel):
    """Trust structure with beneficiaries and distributions."""
    id: str
    name: str
    trust_type: str  # discretionary, unit, etc.
    net_income: Decimal = Field(ge=0)
    distribution_components: Dict[str, Dict[str, Decimal]]  # beneficiary -> component -> amount
    upe_to_company_amounts: Decimal = Field(default=0)  # Div 7A risk


class SMSFEntity(BaseModel):
    """Self-Managed Super Fund entity."""
    id: str
    name: str
    taxable_income_ordinary: Decimal = Field(ge=0)
    taxable_income_nali: Decimal = Field(ge=0)  # Non-arm's length income
    ecpi_proportion: Decimal = Field(0, ge=0, le=1)  # Exempt current pension income
    members: List[str]  # List of Person IDs


class EntityContext(BaseModel):
    """Collection of all entities (persons and legal entities) in the financial position."""
    persons: Dict[str, Person] = Field(default_factory=dict)  # Keyed by person_id
    companies: Dict[str, CompanyEntity] = Field(default_factory=dict)  # Keyed by company_id
    trusts: Dict[str, TrustEntity] = Field(default_factory=dict)  # Keyed by trust_id
    smsfs: Dict[str, SMSFEntity] = Field(default_factory=dict)  # Keyed by smsf_id
