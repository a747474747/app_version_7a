from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional, Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enum-ish Literal types
# ---------------------------------------------------------------------------

PersonRole = Literal["primary", "partner", "dependant"]
ResidencyStatus = Literal["resident", "non_resident", "temporary", "working_holiday"]
WorkStatus = Literal["full_time", "part_time", "self_employed", "not_working", "retired"]
SmokerStatus = Literal["smoker", "non_smoker"]
RelationshipType = Literal["spouse", "child", "parent"]

AssetType = Literal[
    "home",
    "investment_residential",
    "commercial",
    "land",
    "super_accumulation",
    "super_pension",
    "portfolio",
    "cash",
    "vehicle",
    "business",
    "smsf_member_balance",  # Member interest in SMSF, linked to SMSFEntity
]

LoanType = Literal[
    "home_loan",
    "investment_loan",
    "personal_loan",
    "margin_loan",
    "loc",
    "credit_card",
]

InterestRateType = Literal["variable", "fixed", "split"]
RepaymentFrequency = Literal["monthly", "fortnightly", "weekly"]

ValuationSource = Literal["client_estimate", "bank_feed", "system_projection"]
BalanceSource = Literal["client", "provider_feed", "projection"]

CurrencyCode = Literal["AUD"]

ExpenseAllocationStrategy = Literal[
    "EQUAL_SPLIT",
    "PRO_RATA_GROSS",
    "PRIMARY_ABSORBS",
]

TraceSeverity = Literal["info", "warning", "decision_point"]


# ---------------------------------------------------------------------------
# Core primitives: people & relationships
# ---------------------------------------------------------------------------


class Relationship(BaseModel):
    target_person_id: str
    type: RelationshipType
    financial_dependence: float = Field(
        0.0,
        ge=0.0,
        le=1.0,
        description="0–1 weighting for financial dependency / tax dependant status.",
    )


class Person(BaseModel):
    id: str
    role: PersonRole
    date_of_birth: date
    residency_status: ResidencyStatus
    work_status: WorkStatus
    smoker_status: Optional[SmokerStatus] = None
    occupation_risk_band: Optional[str] = None

    relationships: List[Relationship] = Field(default_factory=list)


class ValuationSnapshot(BaseModel):
    amount: float
    currency: CurrencyCode = "AUD"
    effective_date: date
    source: ValuationSource


class BalanceSnapshot(BaseModel):
    amount: float
    currency: CurrencyCode = "AUD"
    effective_date: date
    source: BalanceSource


# ---------------------------------------------------------------------------
# Legal entities
# ---------------------------------------------------------------------------


class CompanyEntity(BaseModel):
    id: str
    name: str
    aggregated_turnover: float = 0.0
    base_rate_entity_flag: bool = False
    company_tax_rate: float = 0.30  # 25% or 30% typical


class TrustEntity(BaseModel):
    id: str
    name: str
    trust_type: Optional[str] = None  # discretionary/unit/fixed/etc.
    net_income: float = 0.0
    # Simplified: downstream CALs can refine this as needed.
    distribution_components_by_beneficiary: List[Dict[str, Any]] = Field(
        default_factory=list
    )
    upe_to_company_amounts: float = 0.0


class SMSFEntity(BaseModel):
    id: str
    name: str
    taxable_income_ordinary: float = 0.0
    taxable_income_non_arm_length: float = 0.0
    ecpi_proportion: float = 0.0  # 0–1 proportion of earnings exempt


# ---------------------------------------------------------------------------
# Assets & liabilities (with proper ownership model)
# ---------------------------------------------------------------------------


class Ownership(BaseModel):
    entity_id: str
    share: float = Field(..., ge=0.0, le=1.0)  # sum across owners ≈ 1.0


class Asset(BaseModel):
    """
    Base asset class, extended by specific asset types.

    For SMSF member interests:
      - asset_type = "smsf_member_balance"
      - linked_entity_id = id of SMSFEntity
      - ownership = [{entity_id: person_id, share: 1.0}]
    """

    id: str
    ownership: List[Ownership] = Field(
        default_factory=list,
        description="Ownership breakdown; sum(share) should be ≈ 1.0.",
    )
    asset_type: AssetType
    valuation: ValuationSnapshot

    # Used when this asset represents an interest in a legal entity (e.g. SMSF).
    linked_entity_id: Optional[str] = Field(
        default=None,
        description="If this asset is an interest in an entity (e.g. SMSF), link to that entity_id.",
    )

    class Config:
        extra = "allow"  # allow extensions in subclasses without breaking the model


class PropertyAsset(Asset):
    """
    Specialisation for direct property (home/investment).
    """

    state_territory: str
    acquisition_date: date
    cost_base: float
    is_main_residence: bool = False

    # Rental & costs
    weekly_rent_current: float = 0.0
    expected_occupancy_rate: float = 1.0
    rent_indexation_rate: float = 0.0

    council_rates: float = 0.0
    water_rates: float = 0.0
    strata_body_corporate: float = 0.0
    land_tax: float = 0.0
    building_insurance: float = 0.0
    landlord_insurance: float = 0.0
    repairs_maintenance: float = 0.0
    property_management_fees: float = 0.0
    other_property_costs: float = 0.0

    capital_works_deduction_rate: float = 0.0
    plant_equipment_pool_balance: float = 0.0

    acquisition_costs: float = 0.0
    sale_costs_estimate: float = 0.0

    custom_capital_growth_rate: Optional[float] = None

    def value_at(self, target_date: date, default_growth_rate: float) -> float:
        """
        Deterministic projection from valuation.effective_date to target_date.
        Implement in engine layer.
        """
        raise NotImplementedError


class Loan(BaseModel):
    id: str
    linked_asset_id: Optional[str] = None
    borrower_entity_ids: List[str] = Field(default_factory=list)
    loan_type: LoanType

    principal_original: float
    principal_outstanding: float
    interest_rate_current: float
    interest_rate_type: InterestRateType

    loan_term_years: float
    remaining_term_years: float

    repayment_frequency: RepaymentFrequency
    repayment_amount_actual: float
    minimum_repayment_amount: float

    interest_only_flag: bool = False
    interest_only_period_years: float = 0.0
    interest_only_remaining_years: float = 0.0

    offset_balance_linked: float = 0.0
    redraw_balance: float = 0.0

    split_segments: List[Dict[str, Any]] = Field(default_factory=list)

    product_fees_recurring: float = 0.0
    break_cost_estimate: float = 0.0

    stress_buffer_rate: float = 0.0  # for serviceability/stress tests

    def balance_at(self, target_date: date, assumptions: "EconomicAssumptions") -> float:
        """
        Deterministic projection of loan balance at a target date.
        Implement amortisation in engine layer.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Household budget – shared flows & allocation strategy
# ---------------------------------------------------------------------------


class AllocationRules(BaseModel):
    """
    Structured config for splitting shared household expenses.
    """

    custom_split_ratios: Optional[Dict[str, float]] = Field(
        default=None,
        description="Optional explicit ratios per entity_id, e.g. {'p1': 0.6, 'p2': 0.4}.",
    )
    primary_earner_id: Optional[str] = Field(
        default=None,
        description="entity_id to treat as primary earner for PRIMARY_ABSORBS strategy.",
    )


class HouseholdBudget(BaseModel):
    """
    Shared household-level flows (rent, groceries, etc.).
    These are allocated to entities via allocation_strategy + allocation_rules.
    """

    housing_expenses: float = 0.0
    groceries: float = 0.0
    utilities: float = 0.0
    insurance_other: float = 0.0
    transport_expenses: float = 0.0
    medical_health_expenses: float = 0.0
    children_education_expenses: float = 0.0
    discretionary_lifestyle_expenses: float = 0.0
    irregular_bills_annual: float = 0.0

    allocation_strategy: ExpenseAllocationStrategy = "EQUAL_SPLIT"
    allocation_rules: AllocationRules = Field(
        default_factory=AllocationRules,
        description="Structured configuration for overriding default allocation behaviour.",
    )


# ---------------------------------------------------------------------------
# Cashflow context – keyed by entity_id
# ---------------------------------------------------------------------------


class IncomeFlows(BaseModel):
    # Employment
    salary_gross: float = 0.0
    salary_sacrifice_super: float = 0.0
    employer_sg_contributions: float = 0.0
    employer_sg_rate: float = 0.0
    bonus_gross: float = 0.0
    allowances_gross: float = 0.0
    reportable_fringe_benefits: float = 0.0
    reportable_super_contributions: float = 0.0

    # Other income
    business_income_net: float = 0.0
    interest_income: float = 0.0
    dividend_unfranked: float = 0.0
    dividend_franked: float = 0.0
    dividend_franking_credits: float = 0.0
    rental_income_gross: float = 0.0
    foreign_employment_income: float = 0.0
    foreign_investment_income: float = 0.0
    foreign_tax_paid: float = 0.0

    # Trust distributions (simple)
    trust_distribution_components: Dict[str, float] = Field(default_factory=dict)


class DeductionFlows(BaseModel):
    work_related_expenses_total: float = 0.0
    motor_vehicle_expenses: float = 0.0
    self_education_expenses: float = 0.0
    home_office_expenses: float = 0.0
    donations_deductible: float = 0.0
    tax_agent_fees: float = 0.0
    income_protection_premiums_deductible: float = 0.0
    interest_deduction_investments: float = 0.0
    interest_deduction_rental_property: float = 0.0
    other_investment_expenses: float = 0.0
    personal_super_deductible_contributions: float = 0.0
    carried_forward_losses: float = 0.0


class ContributionFlows(BaseModel):
    salary_sacrifice_contributions: float = 0.0
    non_concessional_contributions: float = 0.0
    spouse_contributions_received: float = 0.0
    downsizer_contributions: float = 0.0
    regular_investment_contributions: Dict[str, Any] = Field(default_factory=dict)
    regular_withdrawals: Dict[str, Any] = Field(default_factory=dict)


class SocialSecurityAdjustments(BaseModel):
    reportable_fringe_benefits_for_ati: float = 0.0
    reportable_super_for_ati: float = 0.0
    net_rental_loss: float = 0.0
    net_business_loss: float = 0.0
    child_support_paid: float = 0.0


class EntityCashflow(BaseModel):
    """
    All flows that belong to a specific entity (person, company, trust, SMSF).
    """

    income: IncomeFlows = Field(default_factory=IncomeFlows)
    deductions: DeductionFlows = Field(default_factory=DeductionFlows)
    contributions: ContributionFlows = Field(default_factory=ContributionFlows)


class CashflowContext(BaseModel):
    """
    Cashflows keyed by entity_id, plus shared budget and SS adjustments.
    """

    flows: Dict[str, EntityCashflow] = Field(
        default_factory=dict,
        description="Key = entity_id (person/company/trust/smsf), value = EntityCashflow.",
    )
    shared_budget: HouseholdBudget = Field(default_factory=HouseholdBudget)
    social_security_adjustments: Dict[str, SocialSecurityAdjustments] = Field(
        default_factory=dict,
        description="Key = entity_id, value = social security adjustments.",
    )


# ---------------------------------------------------------------------------
# Global rules & assumptions
# ---------------------------------------------------------------------------


class TaxBracket(BaseModel):
    threshold: float
    rate: float
    base: float


class TaxSettings(BaseModel):
    financial_year: int
    resident_brackets: List[TaxBracket] = Field(default_factory=list)
    non_resident_brackets: List[TaxBracket] = Field(default_factory=list)

    medicare_levy_rate: float = 0.0
    medicare_levy_thresholds: Dict[str, Any] = Field(default_factory=dict)
    medicare_levy_surcharge_rates: Dict[str, Any] = Field(default_factory=dict)

    lito_max: float = 0.0
    help_thresholds: Dict[str, Any] = Field(default_factory=dict)


class SuperSettings(BaseModel):
    concessional_cap: float = 0.0
    non_concessional_cap: float = 0.0
    carry_forward_rules: Dict[str, Any] = Field(default_factory=dict)
    tsb_thresholds: Dict[str, Any] = Field(default_factory=dict)
    div293_threshold: float = 0.0
    pension_minimum_factors: Dict[int, float] = Field(default_factory=dict)
    tbc_general_cap: float = 0.0


class SocialSecuritySettings(BaseModel):
    age_pension_asset_thresholds: Dict[str, Any] = Field(default_factory=dict)
    age_pension_income_thresholds: Dict[str, Any] = Field(default_factory=dict)
    deeming_rates: Dict[str, Any] = Field(default_factory=dict)


class EconomicAssumptions(BaseModel):
    cpi_rate: float = 0.0
    wage_growth_rate: float = 0.0
    property_growth_rate_default: float = 0.0
    equity_return_assumption: float = 0.0
    fixed_income_return_assumption: float = 0.0
    cash_return_assumption: float = 0.0
    discount_rate_for_npv: float = 0.0


class GlobalContext(BaseModel):
    effective_date: date
    tax_settings: TaxSettings
    super_settings: SuperSettings
    social_security_settings: SocialSecuritySettings
    economic_assumptions: EconomicAssumptions

    assumption_set_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Entity & Financial Position contexts
# ---------------------------------------------------------------------------


class EntityContext(BaseModel):
    people: Dict[str, Person] = Field(default_factory=dict)
    companies: Dict[str, CompanyEntity] = Field(default_factory=dict)
    trusts: Dict[str, TrustEntity] = Field(default_factory=dict)
    smsfs: Dict[str, SMSFEntity] = Field(default_factory=dict)

    household_budget: HouseholdBudget = Field(default_factory=HouseholdBudget)


class FinancialPositionContext(BaseModel):
    assets: Dict[str, Asset] = Field(default_factory=dict)
    liabilities: Dict[str, Loan] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Calculated intermediaries – namespaced by entity + plan-level + trace
# ---------------------------------------------------------------------------


class TaxResults(BaseModel):
    assessable_income: Optional[float] = None
    total_deductions: Optional[float] = None
    taxable_income: Optional[float] = None
    base_tax: Optional[float] = None
    medicare_levy: Optional[float] = None
    medicare_levy_surcharge: Optional[float] = None
    tax_offsets_total: Optional[float] = None
    help_repayment: Optional[float] = None
    adjusted_taxable_income_ati: Optional[float] = None
    net_tax_payable: Optional[float] = None
    effective_tax_rate: Optional[float] = None


class SuperResults(BaseModel):
    cc_total: Optional[float] = None
    cc_cap_remaining: Optional[float] = None
    ncc_total: Optional[float] = None
    ncc_cap_remaining: Optional[float] = None
    contributions_tax: Optional[float] = None
    division_293_tax: Optional[float] = None
    net_contribution_to_balance: Optional[float] = None
    super_balance_projection: Dict[int, float] = Field(default_factory=dict)
    pension_minimum_required: Optional[float] = None
    super_runway_years: Optional[float] = None


class PropertyResults(BaseModel):
    rental_cashflow_before_tax: Optional[float] = None
    rental_cashflow_after_tax: Optional[float] = None
    rental_yield_gross: Optional[float] = None
    rental_yield_net: Optional[float] = None
    property_equity_over_time: Dict[int, float] = Field(default_factory=dict)


class PortfolioResults(BaseModel):
    investment_balance_projection: Dict[int, float] = Field(default_factory=dict)
    portfolio_fees_dollar: Optional[float] = None
    portfolio_risk_indicator: Optional[float] = None


class EntityResults(BaseModel):
    tax: TaxResults = Field(default_factory=TaxResults)
    super_: SuperResults = Field(default_factory=SuperResults)
    property_: PropertyResults = Field(default_factory=PropertyResults)
    portfolio: PortfolioResults = Field(default_factory=PortfolioResults)
    # Extend with insurance, social security, etc. as needed


class PlanLevelResults(BaseModel):
    net_wealth_by_year: Dict[int, float] = Field(default_factory=dict)
    scenario_delta_summary: Dict[str, Any] = Field(default_factory=dict)
    financial_independence_age: Optional[int] = None
    retirement_funding_gap: Optional[float] = None
    risk_resilience_scores: Dict[str, Any] = Field(default_factory=dict)


class TraceEntry(BaseModel):
    calc_id: str
    entity_id: Optional[str] = None
    field: Optional[str] = None

    year_index: Optional[int] = Field(
        default=None,
        description="Projection year index (0 = base year). None for single-year runs.",
    )
    severity: TraceSeverity = Field(
        default="info",
        description="Helps filter which traces to surface (info, warning, decision_point).",
    )

    explanation: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CalculatedIntermediariesContext(BaseModel):
    """
    Namespaced calculation outputs.

    - results[entity_id] holds domain-specific outputs for that entity.
    - plan_level holds scenario-wide aggregates.
    - trace_log records why certain outputs occurred (for LLM explanations).
    """

    results: Dict[str, EntityResults] = Field(default_factory=dict)
    plan_level: PlanLevelResults = Field(default_factory=PlanLevelResults)
    trace_log: List[TraceEntry] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Top-level CalculationState
# ---------------------------------------------------------------------------


class CalculationState(BaseModel):
    """
    Top-level container for all state used by the Calculation Engine.

    CAL functions should:
      - read from the contexts
      - write only to `intermediates` (and to snapshots in projection outputs).
    """

    global_context: GlobalContext
    entity_context: EntityContext
    position_context: FinancialPositionContext
    cashflow_context: CashflowContext
    intermediates: CalculatedIntermediariesContext = Field(
        default_factory=CalculatedIntermediariesContext
    )


# ---------------------------------------------------------------------------
# Projection model – explicit timeline output
# ---------------------------------------------------------------------------


class YearSnapshot(BaseModel):
    """
    Snapshot of state/results for a single projection year.
    """

    year_index: int
    financial_year: int
    position_snapshot: FinancialPositionContext
    intermediaries: CalculatedIntermediariesContext


class ProjectionOutput(BaseModel):
    """
    Output of a multi-year projection.

    The input is a base CalculationState (Year 0).
    The output is a sequence of YearSnapshots representing Year 0..N.
    """

    base_state: CalculationState
    timeline: List[YearSnapshot] = Field(default_factory=list)
