Markdown

# Data Model Design: Four-Engine System Architecture

**Version**: 2.0 (Consolidated)
**Date**: November 21, 2025
**Status**: Design Complete
**Supersedes**: `calculation_engine_state_plan.md`, `canonical_calc_engine_parameters.md`

This document defines the canonical data models for the Four-Engine System Architecture. It serves as the Single Source of Truth for the Calculation Engine state, incorporating design principles, entity relationships, and precise field definitions.

> **External Types**
>
> The following types are imported from other canonical model files and are
> not defined here: `TaxBracket`, `MedicareThresholds`, `PrecisionMode`,
> `RoundingMode`, `PersonRole`, `Sex`, `ResidencyStatus`, `WorkStatus`,
> `RelationshipType`, `AssetType`, `TaxResults`, `SuperResults`,
> `PropertyResults`, `PlanLevelResults`, `TraceEntry`.
>
> See the dedicated rules/results model files for their definitions.

---

## 1. Core Principles & Design Philosophy

### 1.1 The "Physics Engine" Approach
- **Determinism**: Every calculation (`CAL-*`) must be a pure function of its inputs (`CalculationState`). No hidden global state.
- **Immutable Calculations**: Inputs and outputs are immutable snapshots.
- **Time-Awareness**: All valuations and balances include `effective_date`. Projections are deterministic transformations from a baseline snapshot.

### 1.2 Data Structure Principles
- **Pydantic-First**: All models defined as Pydantic v2 schemas for validation and type safety.
- **Legal Ownership, Not "Households"**: A "Household" is a configuration of shared flows/expenses, not a legal entity. Assets and income are owned by Persons or Legal Entities (Companies, Trusts, SMSFs).
- **Derived vs. Input**: Values like Age or Net Wealth are *derived* at runtime, not stored as primary inputs.
- **Explicit Units**: Monetary values use `Decimal` (never floating point).

```python
class ValueSource[T](BaseModel):

    """Wrapper for tracking data provenance and confidence."""

    value: T

    source: Literal["VERIFIED", "ESTIMATE", "DEFAULT"]

    confidence: float = Field(..., ge=0, le=1, description="Confidence score 0.0-1.0")

    source_metadata: Dict[str, Any] = Field(default_factory=dict, description="e.g. {'doc_id': 'stm_123'}")

```

### 1.3 Naming Conventions
- **PascalCase**: Class names (e.g., `CalculationState`, `TaxResults`).
- **snake_case**: Field names (e.g., `entity_id`, `taxable_income`).
- **SCREAMING_SNAKE_CASE**: Constants and enums (e.g., `RESIDENT`, `AUD`).

---

## 2. Global Context Models

The global context contains system-wide settings, assumptions, and rules that apply across all calculations.

```python
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
    tax_brackets: List[TaxBracket] = Field(..., description="Resident tax brackets")
    medicare_levy_rate: Decimal = Field(..., description="Medicare levy rate")
    medicare_levy_thresholds: MedicareThresholds = Field(..., description="Medicare thresholds")

    # Superannuation settings
    concessional_cap: int = Field(..., description="Annual concessional contributions cap")
    non_concessional_cap: int = Field(..., description="Annual non-concessional cap")
    tbc_general_cap: int = Field(..., description="Transfer Balance Cap")

    # Precision and rounding
    precision_mode: PrecisionMode = Field(default="CENT", description="Rounding precision")
    rounding_mode: RoundingMode = Field(default="HALF_UP", description="Rounding strategy")

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
```

## 3. Entity Context Models

### 3.1 Person Entity
Core actor model with demographic and relationship information.

```Python

class Person(BaseModel):
    """Individual person as a financial actor."""

    id: str = Field(..., description="Unique person identifier")
    role: PersonRole = Field(..., description="Role in household: primary, partner, dependant")

    # Demographics
    date_of_birth: date
    sex: Optional[Sex] = None # For actuarial tables
    residency_status: ResidencyStatus = Field(default="RESIDENT") # resident, non_resident, temporary
    work_status: WorkStatus = Field(default="FULL_TIME")
    
    # Risk Profile
    smoker_status: Optional[bool] = None
    occupation_risk_band: Optional[str] = None # For insurance calc

    # Social Security Attributes
    residency_qualifying_years: Optional[int] = Field(default=0)
    age_pension_age_reached_flag: Optional[bool] = False
    
    # Relationships
    relationships: List[Relationship] = Field(default_factory=list)

    # Derived fields (calculated runtime helpers)
    def age_at(self, at_date: date) -> int:
        return floor((at_date - self.date_of_birth).days / 365.25)

class Relationship(BaseModel):
    target_person_id: str
    type: RelationshipType # spouse, child, parent
    financial_dependence: Decimal = Field(0.0, ge=0.0, le=1.0)
```

### 3.2 Household Configuration
A "Household" is a configuration of shared flows.

```Python

class HouseholdBudget(BaseModel):
    """Shared household expenses not owned by specific entities."""
    
    household_id: str
    
    # Housing and utilities
    housing_expenses: Decimal = Field(default=0, ge=0) # Rent or Board (Mortgages are Liabilities)
    utilities_expenses: Decimal = Field(default=0, ge=0)

    # Living expenses
    food_groceries_expenses: Decimal = Field(default=0, ge=0)
    medical_health_expenses: Decimal = Field(default=0, ge=0)
    children_education_expenses: Decimal = Field(default=0, ge=0)
    insurance_premiums_general: Decimal = Field(default=0, ge=0) # Home/Contents, not Personal
    discretionary_expenses: Decimal = Field(default=0, ge=0)

    # Allocation strategy
    # Defines how these shared costs are split for individual surplus calcs
    allocation_strategy: Literal["EQUAL_SPLIT", "PRO_RATA_GROSS", "PRIMARY_ABSORBS"] = "EQUAL_SPLIT"
```

### 3.3 Legal Entity Models
Models for companies, trusts, and SMSFs that can own assets and incur tax liabilities.

```Python

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
    upe_to_company_amounts: Decimal = Field(default=0) # Div 7A risk

class SMSFEntity(BaseModel):
    """Self-Managed Super Fund entity."""
    id: str
    name: str
    taxable_income_ordinary: Decimal = Field(ge=0)
    taxable_income_nali: Decimal = Field(ge=0)  # Non-arm's length income
    ecpi_proportion: Decimal = Field(0, ge=0, le=1)  # Exempt current pension income
    members: List[str] # List of Person IDs
```

### 3.4 Context Classes
Context classes aggregate entities and positions for calculation snapshots.

```Python

class EntityContext(BaseModel):
    """Collection of all entities (persons and legal entities) in the financial position."""
    persons: Dict[str, Person] = Field(default_factory=dict)  # Keyed by person_id
    companies: Dict[str, CompanyEntity] = Field(default_factory=dict)  # Keyed by company_id
    trusts: Dict[str, TrustEntity] = Field(default_factory=dict)  # Keyed by trust_id
    smsfs: Dict[str, SMSFEntity] = Field(default_factory=dict)  # Keyed by smsf_id

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

```

## 4. Financial Position Context (Assets & Liabilities)

### 4.1 Asset Models

```Python

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
    state_territory: str # For Stamp Duty/Land Tax
    acquisition_date: date
    cost_base: Decimal
    is_main_residence: bool = False
    land_value: Optional[Decimal] = None # Critical for Land Tax

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
```

### 4.2 Liability Models

```Python

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
    stress_buffer_rate: Optional[Decimal] = None # +3% buffer if applied by engine/assumption set

    @property
    def annual_interest_expense(self) -> Decimal:
        """Calculate annual interest expense for this loan."""
        if self.interest_only_flag:
            # Interest-only loan: all repayments are interest
            return self.repayment_amount * Decimal(12) if self.repayment_frequency == "MONTHLY" else self.repayment_amount * Decimal(26) if self.repayment_frequency == "FORTNIGHTLY" else self.repayment_amount * Decimal(52)
        else:
            # Principal + interest loan: calculate interest portion
            # Simplified calculation: interest = principal * rate / frequency_factor
            frequency_factor = 12 if self.repayment_frequency == "MONTHLY" else 26 if self.repayment_frequency == "FORTNIGHTLY" else 52
            periodic_interest = (self.principal_outstanding * self.interest_rate_current) / frequency_factor
            return periodic_interest * frequency_factor  # Annualize
```

### 4.3 Insurance Models
Integrated from.

```Python

class InsurancePolicy(BaseModel):
    """Personal insurance policy."""
    id: str
    owner_entity_id: str # Can be Person or Super Fund
    insured_person_id: str
    cover_type: Literal["LIFE", "TPD", "TRAUMA", "IP"]
    
    # Benefits
    sum_insured: Decimal = Field(ge=0) # For Life/TPD/Trauma
    monthly_benefit: Optional[Decimal] = None # For IP
    waiting_period_days: Optional[int] = None # For IP
    benefit_period_years: Optional[int] = None # For IP (e.g., 2, 5, 65)

    # Premiums
    premium_amount: Decimal = Field(ge=0)
    premium_frequency: Literal["MONTHLY", "ANNUAL"]
    premium_basis: Literal["STEPPED", "LEVEL"]
    tax_deductible_flag: bool = False
```

## 5. Cashflow Context
Income and expenses are attributed to specific entities (Person or Legal Entity).

```Python

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
    foreign_tax_paid: Decimal = Field(default=0) # Foreign Tax Credits

    # Deductions
    work_related_expenses: Decimal = Field(default=0)
    personal_super_contributions: Decimal = Field(default=0) # Concessional
    interest_deductions: Decimal = Field(default=0)

    # Super contributions
    employer_super_guarantee: Decimal = Field(default=0)
    personal_non_concessional_contributions: Decimal = Field(default=0)
    spouse_contributions_received: Decimal = Field(default=0)
    downsizer_contributions: Decimal = Field(default=0)

class CashflowContext(BaseModel):
    """Complete cashflow context."""
    flows: Dict[str, EntityCashflow] = Field(default_factory=dict) # Keyed by entity_id
    shared_budget: Optional[HouseholdBudget] = None
```

## 6. Calculation State & Results

### 6.1 CalculationState Wrapper
The complete immutable input snapshot for any calculation CAL-*.

```Python

class CalculationState(BaseModel):
    """Complete calculation input snapshot."""
    
    # Core contexts
    global_context: GlobalContext
    entity_context: EntityContext # Contains list of Persons, Companies, etc.
    position_context: FinancialPositionContext # Contains Assets, Loans, Insurance
    cashflow_context: CashflowContext # Contains Income/Expense flows

    # Working state (populated by CALs)
    intermediates: CalculatedIntermediariesContext = Field(default_factory=CalculatedIntermediariesContext)

    # Metadata
    scenario_id: str
    assumption_set_id: str
```
### 6.2 CalculatedIntermediariesContext
Namespaced calculation results passed between CALs.

```Python

class CalculatedIntermediariesContext(BaseModel):
    """Namespaced calculation results."""
    
    # Results keyed by entity_id
    results: Dict[str, EntityResults] = Field(default_factory=dict)
    
    # Scenario-level aggregates
    plan_level: PlanLevelResults = Field(default_factory=PlanLevelResults)
    
    # Trace log for explainability
    trace_log: List[TraceEntry] = Field(default_factory=list)

class EntityResults(BaseModel):
    tax: TaxResults = Field(default_factory=TaxResults)
    super: SuperResults = Field(default_factory=SuperResults)
    property: PropertyResults = Field(default_factory=PropertyResults)

class TraceEntry(BaseModel):
    """Audit trail entry for explainability."""
    calc_id: str
    entity_id: Optional[str]
    field: str
    explanation: str
    metadata: Dict[str, Any]
```

### 6.3 Projection Output


```Python

class ProjectionOutput(BaseModel):
    """Time-series projection results."""
    # Also referred to as ProjectionTimeline in functional specifications.
    base_state: CalculationState
    timeline: List[YearSnapshot] = Field(default_factory=list)

class YearSnapshot(BaseModel):
    year_index: int
    financial_year: int
    position_snapshot: FinancialPositionContext # Asset values at end of year
    intermediaries: CalculatedIntermediariesContext # Flows/Tax during year

class ProjectionSummary(BaseModel):

    """Light-weight projection summary for Strategy Engine optimization loops.

    Avoids overhead of full object graph serialization."""

    scenario_id: str

    net_wealth_end: Decimal

    total_tax_paid: Decimal

    average_surplus: Decimal

    retirement_adequacy_score: float



    # Add other KPI fields as needed for optimization constraints

ProjectionOutput and YearSnapshot are used for multi-year scenario reports and are the preferred output format for the Scenario Engine.

---

## 7. Orchestration & Persistence Models

```python
from datetime import datetime, date
from typing import Optional, List, Dict, Any

class UserProfile(BaseModel):

    """System user with role-based access control."""

    id: str

    email: str

    full_name: str

    # Roles defined in research.md 1.2

    role: Literal["CONSUMER", "ADVISER", "COMPLIANCE", "PARTNER"]

    permissions: List[str] = Field(default_factory=list)



    # Adviser specific context

    practice_id: Optional[str] = None

    licensee_id: Optional[str] = None



class Scenario(BaseModel):

    """A specific configuration of financial assumptions and state."""

    id: str

    owner_user_id: str

    name: str

    description: Optional[str] = None

    created_at: datetime

    updated_at: datetime



    # The starting point

    base_state: CalculationState



    # Configuration for engines

    strategy_config: Optional['Strategy'] = None



    # Metadata

    status: Literal["DRAFT", "ACTIVE", "ARCHIVED"] = "DRAFT"

    mode: str = Field(..., description="Execution Mode ID, e.g., MODE-FACT-CHECK")



class Strategy(BaseModel):

    """Optimization template and constraints."""

    id: str

    name: str

    domain: Literal["DEBT", "SUPER", "TAX", "INVESTMENT", "RETIREMENT"]



    # Tunable parameters for the Strategy Engine

    target_metric: Literal["NET_WEALTH", "CASHFLOW_SURPLUS", "RETIREMENT_AGE"]

    constraints: Dict[str, Any] = Field(default_factory=dict, description="e.g. {'min_cash_buffer': 20000}")



    # Flags

    is_active: bool = True

    risk_level: Literal["CONSERVATIVE", "BALANCED", "GROWTH", "HIGH_GROWTH"]



class AdviceOutcome(BaseModel):

    """The result of regulatory compliance checking (Advice Engine)."""

    id: str

    scenario_id: str

    generated_at: datetime



    # Gatekeeping decision

    status: Literal["APPROVED", "REJECTED", "WARNING"]



    # Regulatory checks

    bid_check_passed: bool = Field(..., description="Best Interest Duty compliance")

    suitability_check_passed: bool



    # Explainability

    reasoning: str

    flagged_risks: List[str]

    applied_rules: List[str] = Field(..., description="List of RULE- IDs applied")



class ReferenceDocument(BaseModel):

    """Authoritative source material for RAG."""

    id: str

    title: str

    source_type: Literal["LEGISLATION", "RULING", "GUIDE", "PRODUCT_PDS"]



    # Citation metadata (Research 8.3)

    version: str

    publication_date: date

    url: Optional[str] = None



    # Content

    content_hash: str

    summary_text: str

    vector_id: Optional[str] = None # For future pgvector integration

```

## 8. LLM Orchestrator API Contract Models

Models for the LLM Orchestrator component that handles natural language processing, intent recognition, and narrative generation.

```python
class IntentRecognitionRequest(BaseModel):
    """Request for intent recognition and mode selection."""

    user_input: str
    conversation_context: Optional[List[Dict[str, Any]]] = None
    user_profile: Optional[Dict[str, Any]] = None
    available_modes: List[str]  # List of available execution modes

class IntentRecognitionResult(BaseModel):
    """Result of intent recognition."""

    detected_intent: str  # e.g., "fact_check", "strategy_explore", "scenario_compare"
    selected_mode: str  # Execution mode ID, e.g., "MODE-FACT-CHECK"
    confidence_score: float  # 0.0 to 1.0
    extracted_entities: Dict[str, Any]  # Parsed entities like amounts, dates, etc.
    clarification_questions: Optional[List[str]] = None
    requires_calculation: bool = False

class StateHydrationRequest(BaseModel):
    """Request for building structured state from user inputs."""

    user_input: str
    intent_result: IntentRecognitionResult
    existing_state: Optional[Dict[str, Any]] = None  # Partial state to extend
    validation_context: Optional[Dict[str, Any]] = None  # Field definitions, constraints

class StateHydrationResult(BaseModel):
    """Result of state hydration."""

    hydrated_state: Dict[str, Any]  # Structured state fragments
    missing_fields: List[str]  # Fields that need clarification
    validation_errors: List[str]  # Data quality issues found
    confidence_score: float  # 0.0 to 1.0
    suggested_questions: List[str]  # Questions to ask user for missing data

class FieldValidationRule(BaseModel):
    """Validation rule for a specific field."""

    field_name: str
    field_type: str  # "string", "decimal", "date", "enum"
    required: bool
    constraints: Optional[Dict[str, Any]] = None  # min, max, pattern, etc.
    description: str
    examples: List[str]

class StrategyNominationRequest(BaseModel):
    """Request for strategy suggestions."""

    user_intent: str
    current_state: Dict[str, Any]  # User's financial state
    available_strategies: List[Dict[str, Any]]  # Strategy templates available
    risk_tolerance: Optional[str] = None  # "conservative", "balanced", "aggressive"
    time_horizon: Optional[int] = None  # Years

class StrategyNominationResult(BaseModel):
    """Result of strategy nomination."""

    nominated_strategies: List[Dict[str, Any]]  # Ranked strategy suggestions
    reasoning: str  # Explanation of why these strategies were selected
    risk_assessment: str  # Risk implications of suggestions
    alternative_options: List[Dict[str, Any]]  # Backup suggestions

class NarrativeGenerationRequest(BaseModel):
    """Request for generating human-readable narratives."""

    narrative_type: str  # "explanation", "advice", "education", "summary"
    data_source: Dict[str, Any]  # Calculation results, scenario data, etc.
    audience: str  # "consumer", "adviser", "compliance"
    context: Optional[Dict[str, Any]] = None  # Additional context
    tone: Optional[str] = "professional"  # "professional", "conversational", "educational"

class NarrativeGenerationResult(BaseModel):
    """Result of narrative generation."""

    narrative: str  # Human-readable text
    key_points: List[str]  # Bullet points of important information
    citations: List[Dict[str, Any]]  # References to rules/sources used
    confidence_score: float  # 0.0 to 1.0 in generation quality

class ModeExecutionRequest(BaseModel):
    """Request for executing a complete interaction mode."""

    mode_id: str  # e.g., "MODE-FACT-CHECK", "MODE-CRYSTAL-BALL"
    user_input: str
    user_context: Optional[Dict[str, Any]] = None
    execution_options: Optional[Dict[str, Any]] = None

class ModeExecutionResult(BaseModel):
    """Result of mode execution."""

    mode_id: str
    status: str  # "success", "clarification_needed", "error"
    result_data: Dict[str, Any]  # Mode-specific results
    narrative_response: str  # Human-readable response
    follow_up_questions: Optional[List[str]] = None
    execution_trace: List[Dict[str, Any]]  # Processing steps taken

class ReferenceRetrievalRequest(BaseModel):
    """Request for retrieving relevant reference materials."""

    query: str
    context_type: str  # "educational", "rule_validation", "explanation"
    domain_filters: Optional[List[str]] = None  # e.g., ["tax", "super", "property"]
    max_results: int = 5

class ReferenceRetrievalResult(BaseModel):
    """Result of reference retrieval."""

    references: List[Dict[str, Any]]  # Retrieved documents/snippets
    relevance_scores: List[float]  # Relevance ranking
    context_summary: str  # How references relate to query

```