# Calculation Engine – State & Context Plan

## 1. Purpose & Scope

This document defines the **state architecture** for the Calculation Engine in Frankie’s Finance / Veris Finance.

It covers:

- The **canonical State Contexts** used by all calculations (CALs).
- How people, entities, assets, liabilities, cashflows and rules are represented.
- How **intermediates** are passed between CALs in a deterministic way.
- How the Calculation Engine integrates with upstream modules (LLM Orchestrator, Advice Engine) and downstream UI/Reporting.

This plan does **not** define implementation details of individual calculations (e.g. exact tax formulas); those live in the CAL specifications (e.g. `inferred_rules_CAL-PIT-001.yaml` and related docs).

---

## 2. Design Principles

1. **Determinism**
   - Every calculation (CAL-*) must be a pure function of its inputs and reference data.
   - No hidden global state, and no mutation of inputs in-place.

2. **Separation of Concerns**
   - **State** (who/what/flows) is separate from **Rules** (tax brackets, caps, thresholds).
   - CAL logic is separate from orchestration and summarisation.

3. **Time Awareness**
   - Values such as balances and valuations are only valid at a specific **effective date**.
   - Projections are expressed as deterministic transformations from a baseline snapshot + assumptions.

4. **Legal Ownership, Not “Households”**
   - A “Household” is a **configuration of shared flows**, not a legal entity.
   - Legal ownership sits with Persons and Legal Entities (Companies, Trusts, SMSFs).

5. **Derived vs Input**
   - Certain values (e.g. age, household size, net wealth) are **always derived**.
   - Inputs are the smallest set needed for deterministic recomputation.

6. **Composability via Intermediates**
   - Outputs of one CAL become inputs of another via an explicit **Calculated Intermediaries Context**.
   - No CAL reads the internal implementation of another CAL; they share state via well-defined fields.

---

## 3. High-Level Architecture

### 3.1 Five State Contexts

The engine uses five canonical contexts:

1. **Entity Context (`EntityContext`) – “Who”**
   - People (actors) + relationships.
   - Legal entities: companies, trusts, SMSFs.
   - Household configuration for shared flows.

2. **Financial Position Context (`FinancialPositionContext`) – “What They Own & Owe”**
   - Assets (property, super, portfolios, cash, business, etc.).
   - Liabilities (mortgages, loans, credit, margin, LOC).
   - All valuations and balances are time-aware snapshots.

3. **Cashflow Context (`CashflowContext`) – “Flows”**
   - Income, expenses, deductions, contributions, withdrawals, premiums.
   - Both tax-oriented flows (PIT inputs) and budget-oriented flows.

4. **Global Reference Context (`GlobalContext`) – “Rules & Assumptions”**
   - Tax brackets, Medicare settings, offsets, HELP, super caps, TBC, social security thresholds.
   - Economic assumptions: inflation, wage growth, property growth, returns, discount rates.
   - Versioned per financial year and assumption set.

5. **Calculated Intermediaries Context (`CalculatedIntermediariesContext`) – “Wiring Between CALs”**
   - Derived values: assessable income, taxable income, net tax payable, contributions tax, negative gearing benefit, rental cashflows, net wealth timelines, etc.
   - Explicit outputs from CALs that become inputs to other CALs and to reporting/LLM summaries.

### 3.2 CalculationState Wrapper

All five contexts are wrapped in a single top-level object:

- `CalculationState`
  - `global_context: GlobalContext`
  - `entity_context: EntityContext`
  - `position_context: FinancialPositionContext`
  - `cashflow_context: CashflowContext`
  - `intermediates: CalculatedIntermediariesContext`

This makes it easy to:

- Clone state for scenario comparisons (e.g. strategy A vs B).
- Pass a single object into orchestration layers.
- Enforce that CALs only write to allowed areas (primarily `intermediates` and, for projections, future-year snapshots in `position_context`).

---

## 4. Entity Context – Actors & Legal Structures

### 4.1 Persons (Actors)

People are modelled as **actors** with DOB and relationships:

- `Person`
  - `id: str`
  - `role: 'primary' | 'partner' | 'dependant'`
  - `date_of_birth: date` (required)
  - `residency_status: 'resident' | 'non_resident' | 'temporary' | 'working_holiday'`
  - `work_status: 'full_time' | 'part_time' | 'self_employed' | 'not_working' | 'retired'`
  - `smoker_status: 'smoker' | 'non_smoker' | None`
  - `occupation_risk_band: str | None`
  - `relationships: list[Relationship]`

- `Relationship`
  - `target_person_id: str`
  - `type: 'spouse' | 'child' | 'parent'`
  - `financial_dependence: float` (0.0–1.0, indicates tax dependency weighting if needed)

**Invariants**

- **Age is always derived**, never stored:
  - `age = floor((global_context.effective_date - date_of_birth).days / 365.25)`
- Dependants are recognised dynamically using DOB + relationship (e.g. Age Pension, MLS, insurance/education logic).

### 4.2 Legal Entities

Legal wrappers that can own assets and income:

- `CompanyEntity`
  - `id: str`
  - `name: str`
  - `aggregated_turnover: float`
  - `base_rate_entity_flag: bool`
  - `company_tax_rate: float`
  - Other fields as needed for CAL-TAX-101/102/106.

- `TrustEntity`
  - `id: str`
  - `name: str`
  - `trust_type: str` (discretionary/unit/etc.)
  - `net_income: float`
  - `distribution_components_by_beneficiary: list[...]`
  - `upe_to_company_amounts: float`

- `SMSFEntity`
  - `id: str`
  - `name: str`
  - `taxable_income_ordinary: float`
  - `taxable_income_nali: float`
  - `ecpi_proportion: float`

### 4.3 HouseholdBudget (Shared Flows & Allocation Strategy)

`HouseholdBudget` holds shared, household-level expenses that are not owned by a specific entity (e.g. rent, groceries, utilities).

- `HouseholdBudget`
  - `housing_expenses`
  - `groceries`
  - `utilities`
  - `insurance_other`
  - `discretionary_lifestyle_expenses`
  - `children_education_expenses`
  - `allocation_strategy: ExpenseAllocationStrategy`
  - `allocation_rules: Dict[str, Any]` (optional overrides)

- `ExpenseAllocationStrategy` (enum)
  - `EQUAL_SPLIT` – 50/50 between adult members.
  - `PRO_RATA_GROSS` – split by gross income proportion.
  - `PRIMARY_ABSORBS` – primary earner pays first up to net income, partner covers remainder.

CAL-FND and PIT CALs use this strategy whenever they need per-entity views of shared costs (e.g. individual savings capacity or affordability).

**Key point:** Household is a **config of shared flows**, not an entity that owns assets or earns income.

---

## 5. Financial Position Context – Assets & Liabilities

### 5.1 Time-aware ValuationSnapshots

All “values” are represented as snapshots:

- `ValuationSnapshot`
  - `amount: float`
  - `currency: 'AUD'` (default)
  - `effective_date: date`
  - `source: 'client_estimate' | 'bank_feed' | 'system_projection'`

For liquid accounts, you can use a more generic:

- `BalanceSnapshot`
  - `amount: float`
  - `effective_date: date`
  - `source: 'client' | 'provider_feed' | 'projection'`

**Invariants**

- There is always at least one snapshot per asset (baseline).
- Projections from snapshot to target dates are deterministic and use `GlobalContext` assumptions, unless a custom growth rate is specified.

### 5.2 Assets

Assets share a common base structure and are specialised per type.

#### 5.2.1 Ownership model (no parallel arrays)

Ownership is represented explicitly to avoid brittle “parallel lists”:

- `Ownership`
  - `entity_id: str`
  - `share: float` (0.0–1.0; typically sum = 1.0 across owners)

**Base Asset**

- `Asset` (base class / union tag)
  - `id: str`
  - `ownership: list[Ownership]`  
    - Invariant: `sum(o.share for o in ownership)` ≈ 1.0
  - `asset_type: enum` (e.g. `home`, `investment_residential`, `super_accumulation`, etc.)
  - `valuation: ValuationSnapshot`

This removes the risk of misaligned arrays when owners are re-ordered or filtered.

#### 5.2.2 PropertyAsset (specialisation)

`PropertyAsset` extends `Asset` with:

- Identity / acquisition
  - `state_territory: str`
  - `acquisition_date: date`
  - `cost_base: float`
  - `is_main_residence: bool`
- Rental & costs
  - `weekly_rent_current: float`
  - `expected_occupancy_rate: float`
  - `rent_indexation_rate: float`
  - `council_rates: float`
  - `water_rates: float`
  - `strata_body_corporate: float`
  - `land_tax: float`
  - `building_insurance: float`
  - `landlord_insurance: float`
  - `repairs_maintenance: float`
  - `property_management_fees: float`
  - `other_property_costs: float`
- Depreciation
  - `capital_works_deduction_rate: float`
  - `plant_equipment_pool_balance: float`
- Transaction costs
  - `acquisition_costs: float`
  - `sale_costs_estimate: float`
- Optional growth override
  - `custom_capital_growth_rate: float | None`

All other asset types (super, portfolios, businesses, etc.) follow the same pattern: `Asset` + type-specific fields.


### 5.3 Liabilities

Liabilities (loans, credit) include structure for amortisation and stress testing.

- `Loan`
  - `id: str`
  - `linked_asset_id: str | None`
  - `borrower_entity_ids: list[str]`
  - `loan_type: 'home_loan' | 'investment_loan' | 'personal_loan' | 'margin_loan' | 'loc' | 'credit_card'`
  - `principal_original: float`
  - `principal_outstanding: float`
  - `interest_rate_current: float`
  - `interest_rate_type: 'variable' | 'fixed' | 'split'`
  - `loan_term_years: float`
  - `remaining_term_years: float`
  - `repayment_frequency: 'monthly' | 'fortnightly' | 'weekly'`
  - `repayment_amount_actual: float`
  - `minimum_repayment_amount: float`
  - `interest_only_flag: bool`
  - `interest_only_period_years: float`
  - `interest_only_remaining_years: float`
  - `offset_balance_linked: float`
  - `redraw_balance: float`
  - `split_segments: list[...]`
  - `product_fees_recurring: float`
  - `break_cost_estimate: float`
  - `stress_buffer_rate: float` (for serviceability calcs)

---

## 6. Cashflow Context – Income, Expenses & Contributions

The Cashflow Context aggregates all **flows** over a period (usually annual for CALs).

To avoid ambiguity in multi-person scenarios, all entity-specific flows are **keyed by entity_id** (person or legal entity), and household/shared flows are stored separately.

### 6.1 Structure

- `CashflowContext`
  - `flows: Dict[str, EntityCashflow]`  
    - Key = `entity_id` (person, company, trust, SMSF)
  - `shared_budget: HouseholdBudget`  
    - Shared household expenses (rent, utilities, groceries, etc.)
  - `social_security_adjustments: Dict[str, SocialSecurityAdjustments]`  
    - Keyed by `entity_id` where needed.

### 6.2 EntityCashflow

`EntityCashflow` contains all flows that can be attributed to a specific entity:

- Employment & super
  - `salary_gross`
  - `salary_sacrifice_super`
  - `employer_sg_contributions`
  - `employer_sg_rate`
  - `bonus_gross`
  - `allowances_gross`
  - `reportable_fringe_benefits`
  - `reportable_super_contributions`
- Investment & other income
  - `business_income_net`
  - `interest_income`
  - `dividend_unfranked`
  - `dividend_franked`
  - `dividend_franking_credits`
  - `rental_income_gross`
  - `trust_distribution_components` (structured)
  - `foreign_employment_income`
  - `foreign_investment_income`
  - `foreign_tax_paid`
- Deductions
  - `work_related_expenses_total`
  - `motor_vehicle_expenses`
  - `self_education_expenses`
  - `home_office_expenses`
  - `donations_deductible`
  - `tax_agent_fees`
  - `income_protection_premiums_deductible`
  - `interest_deduction_investments`
  - `interest_deduction_rental_property`
  - `other_investment_expenses`
  - `personal_super_deductible_contributions`
  - `carried_forward_losses`
- Contributions & withdrawals (entity level)
  - `regular_investment_contributions`
  - `regular_withdrawals`
  - `non_concessional_contributions`
  - `spouse_contributions_received`
  - `downsizer_contributions`

This structure guarantees that when the engine processes `salary_gross`, it always knows whose salary it is.

### 6.3 Shared budget & allocation

`HouseholdBudget` represents shared flows **not directly owned** by one entity:

- `housing_expenses`
- `groceries`
- `utilities`
- `insurance_other`
- `discretionary_lifestyle_expenses`
- `children_education_expenses`
- etc.

To avoid ambiguity, the allocation of these shared flows to entities is driven by an explicit strategy:

- `ExpenseAllocationStrategy` (enum)
  - `EQUAL_SPLIT` – split 50/50 between adults.
  - `PRO_RATA_GROSS` – split by gross income proportions.
  - `PRIMARY_ABSORBS` – primary earner pays first up to their net income, then partner.

The chosen strategy is stored either:

- in `HouseholdBudget.allocation_strategy`, or  
- in `GlobalContext` as a default, with household-level overrides.

CAL-FND cashflow/wealth calculations must use the declared strategy whenever they need per-entity views (e.g., individual savings capacity).


---

## 7. Global Reference Context – Rules & Assumptions

### 7.1 Tax settings

- `financial_year: int`
- Resident and non-resident brackets
  - `tax_brackets: list[{threshold, rate, base}]`
  - `non_resident_brackets: list[...]`
- Medicare & MLS
  - `medicare_levy_rate`
  - `medicare_levy_thresholds`
  - `medicare_levy_surcharge_rates`
- Offsets & HELP
  - `lito_max`
  - `help_thresholds`
  - Any additional offsets required.

### 7.2 Super settings

- `concessional_cap`
- `non_concessional_cap`
- `carry_forward_rules`
- `tsb_thresholds`
- `div293_threshold`
- `pension_minimum_factors`
- `tbc_general_cap`

### 7.3 Social security

- `age_pension_asset_thresholds`
- `age_pension_income_thresholds`
- `deeming_rates`

### 7.4 Economic assumptions

- `cpi_rate`
- `wage_growth_rate`
- `property_growth_rate_default`
- `equity_return_assumption`
- `fixed_income_return_assumption`
- `cash_return_assumption`
- `discount_rate_for_npv`

---

## 8. Calculated Intermediaries – Namespaced Results

In multi-person or multi-entity scenarios, we cannot store a single global `taxable_income` or `net_tax_payable` without overwriting values.

Instead, all CAL outputs are:

- **Namespaced by entity_id**, and
- Grouped by domain (tax, super, property, plan-level metrics).

### 8.1 Overall structure

- `CalculatedIntermediariesContext`
  - `results: Dict[str, EntityResults]`
    - Key = `entity_id` (person/company/trust/SMSF)
  - `plan_level: PlanLevelResults`
    - Scenario-wide metrics that are not specific to one entity (e.g. total net wealth).
  - `trace_log: list[TraceEntry]` (optional but recommended)
    - Used to explain *why* particular outputs occurred.

### 8.2 EntityResults

`EntityResults` groups domain-specific outputs:

- `tax: TaxResults`
  - `assessable_income`
  - `total_deductions`
  - `taxable_income`
  - `base_tax`
  - `medicare_levy`
  - `medicare_levy_surcharge`
  - `tax_offsets_total`
  - `help_repayment`
  - `adjusted_taxable_income_ati`
  - `net_tax_payable`
  - `effective_tax_rate`
- `super: SuperResults`
  - `cc_total`
  - `cc_cap_remaining`
  - `ncc_total`
  - `ncc_cap_remaining`
  - `contributions_tax`
  - `division_293_tax`
  - `net_contribution_to_balance`
  - `super_balance_projection` (by year index)
- `property: PropertyResults`
  - `rental_cashflow_before_tax`
  - `rental_cashflow_after_tax`
  - `rental_yield_gross`
  - `rental_yield_net`
  - `property_equity_over_time` (by year index)
- `portfolio: PortfolioResults`
  - `investment_balance_projection`
  - `portfolio_fees_dollar`
  - `portfolio_risk_indicator`
- `other_domains: ...`  
  - Placeholders for insurance, social security, etc.

### 8.3 PlanLevelResults

Scenario-wide aggregates:

- `net_wealth_by_year: Dict[int, float]`
- `scenario_delta_summary: Dict[str, Any]`
- `financial_independence_age: Optional[int]`
- `retirement_funding_gap: Optional[float]`
- `risk_resilience_scores: Dict[str, Any]`

### 8.4 Trace log (for explainability)

To support rich explanations (“your tax is X because Y”), CALs may write trace entries:

- `TraceEntry`
  - `calc_id: str` (e.g. `CAL-PIT-001`)
  - `entity_id: Optional[str]` (if applicable)
  - `field: str` (e.g. `net_tax_payable`)
  - `explanation: str` (short human-or-LLM-friendly reason)
  - `metadata: Dict[str, Any]` (optional parameters, bracket tier, etc.)

The LLM/Advice Engine can then consume `trace_log` to generate faithful explanations instead of hallucinating rationale.

---

## 9. Projection Model – Timeline as Explicit Output

The CalculationState represents the **Year 0** state (as at `global_context.effective_date`).

Longer-term projections (e.g. 10+ years) should not mutate the same state object multiple times in place. Instead, the engine produces a **projection timeline**.

### 9.1 ProjectionOutput

- `ProjectionOutput`
  - `base_state: CalculationState`  
    - The original Year 0 state used as the starting point.
  - `timeline: list[YearSnapshot]`  
    - Ordered by `year_index` (0, 1, 2, …).

### 9.2 YearSnapshot

Each `YearSnapshot` captures:

- `year_index: int`  
  - 0 = base year, 1 = base year + 1, etc.
- `financial_year: int`  
  - Income year label (e.g. 2025, 2026).
- `position_snapshot: FinancialPositionContext`  
  - Asset/liability values as at the end of that year.
- `intermediaries: CalculatedIntermediariesContext`  
  - Namespaced tax/super/etc outputs for that year.

The projection engine:

1. Takes `CalculationState` (Year 0).
2. For each future year:
   - Applies economic assumptions & strategy.
   - Produces a new `YearSnapshot`.
3. Returns a single `ProjectionOutput`.

This design keeps Year 0 state immutable while still allowing rich multi-year reporting and scenario comparison.



---

## 10. CAL Function Pattern

Each CAL has a consistent function signature at spec level:

```python
def run_CAL_X(
    state: CalculationState,
) -> CalculationState:
    """
    Reads from:
      - state.global_context
      - state.entity_context
      - state.position_context
      - state.cashflow_context
      - state.intermediates (previous outputs)
    Writes to:
      - state.intermediates (new or updated fields)
      - optionally: future-year projections in position_context
    """
