# Canonical Calculation Engine Parameters

This document defines the **canonical parameter shapes** that the Calculation Engine and related modules use.

- These are **logical fields**, not implementation types.
- In code, they’ll typically be grouped into domain-specific models, e.g.:
  - `CalculationContext`
  - `PersonProfile`
  - `SuperAccountInputs`
  - `PropertyInputs`
  - `LoanInputs`
  - `PortfolioInputs`
  - `InsurancePolicyInputs`
  - `ScenarioAssumptions`
- CALs (canonical calculations) consume and produce these structures, passing them between modules.

---

## 1. Global / Meta Context

| ID                     | Type / Shape         | Scope            | Description |
|------------------------|----------------------|------------------|-------------|
| `calculation_id`       | string               | per-calculation  | Identifier of the CAL being executed (e.g. `CAL-PIT-001`). |
| `tax_year`             | int                  | per-scenario     | Income year for tax calculations (e.g. 2025). |
| `scenario_id`          | string               | per-scenario     | Identifier for scenario (e.g. `base`, `alt_a`, `stress`). |
| `projection_year_index`| int                  | per-scenario     | Index relative to “now” (0 = current year, 1 = +1 year, etc.). |
| `entity_scope`         | enum                 | per-scenario     | Scope for calc: `individual`, `couple`, `household`, `company`, `trust`, `smsf`. |
| `jurisdiction`         | string/enum          | per-scenario     | Country + state context (e.g. `AU`, `NSW`, `VIC`) for tax/stamp duty/land tax. |
| `currency`             | string               | per-scenario     | Currency code, typically `AUD`. |
| `precision_mode`       | enum/struct          | per-scenario     | Rounding policy and decimal precision for outputs. |
| `effective_date`       | date                 | per-scenario     | Snapshot date for point-in-time calculations. |
| `assumption_set_id`    | string               | per-scenario     | Identifier for which assumption set (returns, inflation, fees) is in use. |

---

## 2. Person & Household Profile

### 2.1 Person parameters

| ID                      | Type / Shape | Scope         | Description |
|-------------------------|--------------|---------------|-------------|
| `person_id`             | string       | per-person    | Unique identifier for a person. |
| `date_of_birth`         | date         | per-person    | Date of birth. |
| `age`                   | int          | per-person    | **Derived:** age in years from `date_of_birth` and the scenario effective date (not normally entered as a primary input). |
| `sex`                   | enum         | per-person    | Optional, for actuarial or life expectancy assumptions. |
| `marital_status`        | enum         | per-person    | `single`, `married`, `de_facto`, etc. |
| `relationship_role`     | enum         | per-person    | Role in household: `primary`, `partner`, `child`, `other_dependant`. |
| `residency_status`      | enum         | per-person    | ATO sense: `resident`, `non_resident`, `temporary`. |
| `work_status`           | enum         | per-person    | `full_time`, `part_time`, `self_employed`, `not_working`, `retired`. |
| `occupation_risk_band`  | enum         | per-person    | Simple band for insurance/IP risk assumptions. |
| `smoker_status`         | enum         | per-person    | `smoker` / `non_smoker` for insurance assumptions. |
| `dependants_count`      | int          | per-person    | **Derived:** count of linked dependant persons (role = `dependant`); primarily used for summaries and eligibility checks. |
| `dependants_age_bands`  | list/array   | per-person    | **Derived/optional:** buckets of dependant ages (e.g. `[0–5, 6–12, 13–18]`) for education and family-cost modelling. |

### 2.2 Household parameters

| ID                       | Type / Shape | Scope         | Description |
|--------------------------|--------------|---------------|-------------|
| `household_id`           | string       | per-household | Unique identifier for household unit. |
| `household_type`         | enum         | per-household | `single`, `couple_no_children`, `couple_with_children`, etc. |
| `location`               | struct       | per-household | State/territory, metro/regional flags for cost-of-living. |
| `homeowner_flag`         | bool         | per-household | Whether the household owns their primary residence. |
| `household_size`         | int          | per-household | **Derived:** total number of people linked to this household; typically not entered manually. |

---

## 3. Income & Employment

This section lists per-person / per-entity income fields.

In implementation, these do **not** live in a flat structure. Instead they are stored under a keyed map like
`CashflowContext.flows[entity_id]` for each person or legal entity, while shared household expenses
(e.g. rent, groceries, utilities) live in a separate `HouseholdBudget` structure and are later allocated
to entities via an `ExpenseAllocationStrategy` (equal split, pro-rata by income, primary-earner-first, etc.).


### 3.1 Employment income (per person)

| ID                               | Type / Shape | Scope      | Description |
|----------------------------------|--------------|------------|-------------|
| `salary_wages_gross`             | number       | per-person | Gross salary and wage income. |
| `salary_wages_tax_withheld`      | number       | per-person | PAYG withheld on salary/wages. |
| `bonus_gross`                    | number       | per-person | Bonus/commission income. |
| `allowances_gross`               | number       | per-person | Allowances (car, travel, etc.). |
| `reportable_fringe_benefits`     | number       | per-person | RFBA amount for the year. |
| `reportable_super_contributions` | number       | per-person | Reportable employer super contributions (e.g. salary sacrifice). |
| `lump_sum_in_arrears_gross`      | number       | per-person | Lump sums in arrears. |
| `lump_sum_in_arrears_years`      | int          | per-person | Number of prior years the arrears relate to. |

### 3.2 Other assessable income (per person/entity)

| ID                          | Type / Shape   | Scope              | Description |
|-----------------------------|----------------|--------------------|-------------|
| `business_income_net`       | number         | per-person/entity  | Net business income (or loss). |
| `interest_income`           | number         | per-person/entity  | Bank/TD interest income. |
| `dividend_unfranked`        | number         | per-person/entity  | Unfranked dividend income. |
| `dividend_franked`          | number         | per-person/entity  | Franked dividend component. |
| `dividend_franking_credits` | number         | per-person/entity  | Attached franking credits. |
| `trust_distribution_components` | struct    | per-person/entity  | Split of trust distributions by component (interest, ordinary, discounted CGT, other CGT, tax-free, tax-deferred, etc.). |
| `rental_income_gross`       | number         | per-person/entity  | Gross rental income from properties. |
| `other_rental_incentives`   | number         | per-person/entity  | Rental incentives/other property income (e.g. NRAS). |
| `foreign_employment_income` | number         | per-person         | Foreign salary/wage income. |
| `foreign_investment_income` | number         | per-person/entity  | Foreign interest/dividends. |
| `foreign_tax_paid`          | number         | per-person/entity  | Foreign tax credits paid on foreign income. |

### 3.3 Adjustments for ATI / means tests

| ID                                  | Type / Shape | Scope      | Description |
|-------------------------------------|--------------|------------|-------------|
| `reportable_fringe_benefits_for_ATI` | number      | per-person | RFBA used in adjusted taxable income calculations. |
| `reportable_super_for_ATI`           | number      | per-person | Reportable super contributions included in ATI. |
| `net_rental_loss`                    | number      | per-person | Net rental loss used in ATI calculations. |
| `net_business_loss`                  | number      | per-person | Net business loss for ATI. |
| `child_support_paid`                 | number      | per-person | Child support (impacting family tax benefits / other means tests). |

---

## 4. Deductions & Expenses

### 4.1 Tax-deductible expenses

| ID                                    | Type / Shape | Scope      | Description |
|---------------------------------------|--------------|------------|-------------|
| `work_related_expenses_total`         | number       | per-person | Total work-related expenses claimed. |
| `motor_vehicle_expenses`              | number       | per-person | Deductible motor vehicle expenses. |
| `self_education_expenses`            | number       | per-person | Self-education expenses (where deductible). |
| `home_office_expenses`                | number       | per-person | Deductible home office expenses. |
| `donations_deductible`               | number       | per-person | Gifts and donations deductible under tax law. |
| `tax_agent_fees`                      | number       | per-person | Tax agent/accountant fees. |
| `income_protection_premiums_deductible` | number    | per-person | Deductible IP premiums (held outside super). |
| `interest_deduction_investments`      | number       | per-person/entity | Interest deduction on non-property investment loans. |
| `interest_deduction_rental_property`  | number       | per-person/entity | Interest deduction on property/investment loans. |
| `other_investment_expenses`          | number       | per-person/entity | Other investment-related expenses (brokerage, platform admin). |
| `personal_super_deductible_contributions` | number  | per-person | Personal concessional contributions claimed as a deduction. |
| `other_specific_deductions`           | list/struct  | per-person/entity | Other specific deduction items with tagged types. |

### 4.2 Household / budget expenses

| ID                               | Type / Shape | Scope         | Description |
|----------------------------------|--------------|---------------|-------------|
| `housing_expenses`               | number       | per-household | Total housing costs (rent or mortgage+rates+insurance) per period. |
| `utilities_expenses`             | number       | per-household | Electricity, gas, water, internet per period. |
| `transport_expenses`             | number       | per-household | Transport costs (fuel, public transport, rego). |
| `food_groceries_expenses`        | number       | per-household | Food and groceries. |
| `medical_health_expenses`        | number       | per-household | Out-of-pocket medical, health insurance gap, etc. |
| `children_education_expenses`    | number       | per-household | Education-related costs for children. |
| `insurance_premiums_total`       | number       | per-household | Total non-tax-deductible insurance premiums. |
| `discretionary_lifestyle_expenses` | number     | per-household | Discretionary / lifestyle spending. |
| `irregular_bills_annual`         | number       | per-household | Annualised irregular costs (e.g. holidays, rego, big once-offs). |

---

## 5. Superannuation & Pensions

Implementation note: retail / industry / employer super accounts are represented as per-account balances
owned directly by a person, while Self-Managed Super Funds (SMSFs) are also modelled as entities.
Each member’s interest in an SMSF is exposed to the Calculation Engine as an asset of type
`smsf_member_balance` linked to the SMSF entity, so member balances appear in net-wealth views
without double-counting the underlying SMSF assets.

### 5.1 Per super account

| ID                         | Type / Shape | Scope           | Description |
|----------------------------|--------------|-----------------|-------------|
| `fund_id`                  | string       | per-account     | Unique identifier for the super fund/account. |
| `owner_person_id`          | string       | per-account     | Person who owns this account. |
| `fund_type`                | enum         | per-account     | `industry`, `retail`, `employer`, `smsf`. |
| `phase`                    | enum         | per-account     | `accumulation` or `pension`. |
| `balance_start_year`       | number       | per-account     | Opening balance at start of year. |
| `balance_current`          | number       | per-account     | Current estimated balance. |
| `taxable_component`        | number       | per-account     | Taxable component balance. |
| `tax_free_component`       | number       | per-account     | Tax-free component balance. |
| `preservation_status`      | enum         | per-account     | Preserved / restricted non-preserved / unrestricted. |
| `investment_option_allocations` | map    | per-account     | Asset allocation (e.g. `{shares: 0.7, fixed_interest: 0.2, cash: 0.1}`). |

### 5.2 Contributions (per account per year)

| ID                                    | Type / Shape | Scope        | Description |
|---------------------------------------|--------------|--------------|-------------|
| `employer_sg_contributions`           | number       | per-account  | Employer SG contributions for year. |
| `salary_sacrifice_contributions`      | number       | per-account  | Pre-tax salary sacrificed contributions. |
| `personal_deductible_contributions`   | number       | per-account  | Personal concessional contributions claimed as a deduction. |
| `non_concessional_contributions`      | number       | per-account  | After-tax (non-concessional) contributions. |
| `spouse_contributions_received`       | number       | per-account  | Contributions made by a spouse into this account. |
| `downsizer_contributions`             | number       | per-account  | Downsizer contributions. |
| `government_co_contribution_received` | number       | per-account  | Government co-contribution amounts. |
| `rollover_in_amounts`                 | number       | per-account  | Rollovers into this account from other funds. |

### 5.3 Super tax inputs

| ID                                | Type / Shape | Scope      | Description |
|-----------------------------------|--------------|------------|-------------|
| `concessional_cap_amount`         | number       | per-person | Annual concessional contributions cap. |
| `non_concessional_cap_amount`     | number       | per-person | Annual non-concessional contributions cap. |
| `carried_forward_concessional_unused` | number   | per-person | Total unused concessional cap available to carry forward (simple). |
| `prior_years_concessional_history` | list/array | per-person | Past concessional contributions for carry-forward logic. |
| `tsb_prior_30_june`              | number       | per-person | Total super balance at prior 30 June. |
| `div293_threshold`               | number       | per-person | Div 293 income threshold. |
| `div293_income`                  | number       | per-person | Income used to test Div 293 applicability. |

### 5.4 Pension / retirement drawdown

| ID                           | Type / Shape | Scope      | Description |
|------------------------------|--------------|------------|-------------|
| `pension_commencement_balance` | number     | per-account| Balance at pension commencement. |
| `pension_minimum_factor`     | number       | per-account| Age-based minimum drawdown factor. |
| `pension_drawdown_requested` | number       | per-account| Planned annual pension payment. |
| `lump_sum_withdrawals_this_year` | number   | per-account| Lump-sum withdrawals taken in year. |
| `tbc_used`                  | number       | per-person | Transfer balance cap used to date. |
| `planned_retirement_age`    | int          | per-person | Target retirement age. |
| `retirement_spending_target`| number       | per-household/person | Target annual spending in retirement. |

---

## 6. Property Assets & Debt

### 6.1 Property asset parameters

| ID                        | Type / Shape | Scope        | Description |
|---------------------------|--------------|--------------|-------------|
| `property_id`             | string       | per-property | Unique identifier for a property. |
| `ownership`               | list/struct  | per-property | Ownership list with entries `{entity_id, share}`; shares for a property should sum to approximately 1.0. |
| `property_type`           | enum         | per-property | `home`, `investment_residential`, `commercial`, `land`. |
| `state_territory`         | enum         | per-property | State/territory where the property is located (for stamp duty / land tax context). |
| `purchase_price`          | number       | per-property | Original purchase price. |
| `purchase_date`          | date         | per-property | Acquisition date. |
| `valuation_snapshot`      | struct       | per-property | Point-in-time valuation `{amount, currency, effective_date, source}` used as the base for projections (rather than a timeless `current_valuation`). |
| `land_value`              | number       | per-property | Land value, for land tax calculations. |
| `rental_status`           | enum         | per-property | `owner_occupied`, `rented`, `holiday_home`, `vacant`. |
| `weekly_rent_current`     | number       | per-property | Current weekly rent. |
| `expected_occupancy_rate` | number       | per-property | Expected occupancy rate (0–1). |
| `rent_indexation_rate`    | number       | per-property | Annual rent growth assumption. |
| `council_rates`           | number       | per-property | Annual council rates. |
| `water_rates`             | number       | per-property | Annual water/sewerage charges. |
| `body_corporate_fees`     | number       | per-property | Annual body corporate / strata fees (if applicable). |
| `insurance_premiums`      | number       | per-property | Annual building/landlord insurance premiums. |
| `maintenance_allowance`   | number       | per-property | Annual allowance for maintenance/capex. |

### 6.2 Loan / debt parameters

| ID                           | Type / Shape | Scope      | Description |
|------------------------------|--------------|------------|-------------|
| `loan_id`                    | string       | per-loan   | Unique identifier for loan. |
| `linked_asset_id`            | string       | per-loan   | Asset the loan is secured against (property, portfolio, etc.). |
| `borrower_entity_ids`        | list/array   | per-loan   | IDs of borrowing entities (persons, companies, trusts). |
| `loan_type`                  | enum         | per-loan   | `home_loan`, `investment_loan`, `personal_loan`, `credit_card`, `margin_loan`, `loc`. |
| `principal_original`         | number       | per-loan   | Original principal amount. |
| `principal_outstanding`      | number       | per-loan   | Current outstanding principal. |
| `interest_rate_current`      | number       | per-loan   | Current annual interest rate. |
| `interest_rate_type`         | enum         | per-loan   | `variable`, `fixed`, `split`. |
| `loan_term_years`            | number       | per-loan   | Original total loan term. |
| `remaining_term_years`       | number       | per-loan   | Remaining term. |
| `repayment_frequency`        | enum         | per-loan   | `monthly`, `fortnightly`, `weekly`. |
| `repayment_amount_actual`    | number       | per-loan   | Actual repayment amount per period. |
| `minimum_repayment_amount`   | number       | per-loan   | Minimum required repayment amount per period. |
| `interest_only_flag`         | bool         | per-loan   | Whether loan is currently interest-only. |
| `interest_only_period_years` | number       | per-loan   | Total IO period in years. |
| `interest_only_remaining_years` | number   | per-loan   | Remaining IO period. |
| `offset_balance_linked`      | number       | per-loan   | Offset account balance linked to loan. |
| `redraw_balance`             | number       | per-loan   | Available redraw balance. |
| `split_segments`             | list/struct  | per-loan   | Loan splits (each with its own principal, purpose, rate). |
| `lvr_current`                | number       | per-loan   | **Derived:** current loan-to-value ratio from linked security value and loan balance; generally not required as a primary input field. |
| `product_fees_recurring`     | number       | per-loan   | Ongoing loan fees. |
| `break_cost_estimate`        | number       | per-loan   | Estimated break cost for fixed loans. |
| `stress_buffer_rate`         | number       | per-loan   | Assessment rate buffer (e.g. +3% above current rate). |

---

## 7. Portfolio & Other Investments

### 7.1 Portfolio-level parameters

| ID                          | Type / Shape | Scope        | Description |
|-----------------------------|--------------|--------------|-------------|
| `portfolio_id`              | string       | per-portfolio| Unique identifier for an investment portfolio/account. |
| `entity_id`                 | string       | per-portfolio| Owner entity (person, couple, trust, company). |
| `account_type`              | enum         | per-portfolio| `broker`, `platform`, `managed_fund`, `ETF`, `cash_account`, `term_deposit`, etc. |
| `current_value_total`       | number       | per-portfolio| Total portfolio value. |
| `cash_balance`              | number       | per-portfolio| Cash balance within portfolio. |
| `target_asset_allocation`   | map          | per-portfolio| Target allocation by asset class. |
| `current_asset_allocation`  | map          | per-portfolio| Current allocation by asset class. |
| `contribution_schedule`     | struct       | per-portfolio| Schedule of regular contributions (amount, frequency). |
| `withdrawal_schedule`       | struct       | per-portfolio| Schedule of planned withdrawals. |
| `expected_return_nominal`   | number       | per-portfolio| Expected nominal return (per annum). |
| `expected_volatility`       | number       | per-portfolio| Optional: standard deviation or risk score. |
| `fee_structure`             | struct       | per-portfolio| Breakdown of admin/investment/advice fees (pct + flat). |

### 7.2 Holding-level parameters

| ID                     | Type / Shape | Scope       | Description |
|------------------------|--------------|-------------|-------------|
| `holding_id`           | string       | per-holding | Unique identifier for holding. |
| `instrument_type`      | enum         | per-holding | `share`, `ETF`, `managed_fund`, `bond`, `term_deposit`, `crypto`, etc. |
| `ticker_or_code`       | string       | per-holding | Security code / ticker / fund code. |
| `units_held`           | number       | per-holding | Units/shares held. |
| `cost_base_total`      | number       | per-holding | Total cost base for CGT purposes. |
| `current_price`        | number       | per-holding | Current price per unit. |
| `franking_level`       | number       | per-holding | Proportion of distributions that are franked. |
| `income_yield`         | number       | per-holding | Distribution/dividend yield. |
| `currency`             | string       | per-holding | Currency of the asset. |
| `liquidity_band`       | enum         | per-holding | `daily`, `monthly`, `illiquid`, etc. |

---

## 8. Insurance

### 8.1 Policy-level parameters

| ID                         | Type / Shape | Scope       | Description |
|----------------------------|--------------|-------------|-------------|
| `policy_id`                | string       | per-policy  | Unique identifier for insurance policy. |
| `owner_entity_id`          | string       | per-policy  | Payer/owner of policy (person/entity). |
| `insured_person_id`        | string       | per-policy  | Insured life. |
| `cover_type`               | enum         | per-policy  | `life`, `TPD`, `trauma`, `IP`, `business_key_person`. |
| `sum_insured`              | number       | per-policy  | Lump-sum cover for life/TPD/trauma. |
| `monthly_benefit`          | number       | per-policy  | Monthly benefit for IP. |
| `waiting_period_days`      | int          | per-policy  | IP waiting period in days. |
| `benefit_period_years`     | number       | per-policy  | IP benefit period. |
| `premium_amount`           | number       | per-policy  | Premium amount per period. |
| `premium_frequency`        | enum         | per-policy  | `monthly`, `annual`, etc. |
| `premium_basis`            | enum         | per-policy  | `stepped`, `level`. |
| `inside_super_flag`        | bool         | per-policy  | Whether policy is held inside super. |
| `linked_benefits_flags`    | struct       | per-policy  | Flags for linked benefits (e.g. combined life/TPD, trauma riders). |
| `indexation_flag`          | bool         | per-policy  | Whether cover indexed to CPI/fixed. |
| `tax_deductible_flag`      | bool         | per-policy  | Whether premiums are deductible. |

### 8.2 Needs-analysis parameters

| ID                                   | Type / Shape | Scope       | Description |
|--------------------------------------|--------------|-------------|-------------|
| `desired_income_replacement_ratio`   | number       | per-person  | Target % of income to replace on death/disablement. |
| `income_replacement_period_years`    | number       | per-person  | Period over which income is to be replaced. |
| `desired_debt_clearance_debts_ids`   | list/array   | per-person  | Debt IDs to be fully cleared on claim. |
| `desired_children_education_cost_per_child` | number | per-person/household | Target education cost per child. |
| `desired_education_years_per_child`  | number       | per-person/household | Years of education to fund per child. |
| `final_expenses_lump_sum_target`     | number       | per-person  | Target lump sum for final expenses. |
| `emergency_buffer_target_months`     | number       | per-household | Target months of expenses as cash buffer. |

---

## 9. Social Security / Age Pension

| ID                                | Type / Shape | Scope       | Description |
|-----------------------------------|--------------|-------------|-------------|
| `age_pension_age_reached_flag`    | bool         | per-person  | Whether person has reached Age Pension age. |
| `residency_qualifying_years`      | number       | per-person  | Years of Australian residency for Age Pension tests. |
| `couple_status_for_pension`       | enum         | per-person  | `single` or `couple` for Age Pension purposes. |
| `assessable_assets_breakdown`     | struct       | per-person/household | Breakdown of assets by category (home exempt value, other real property, financial assets, vehicles, contents, business assets). |
| `assessable_income_breakdown`     | struct       | per-person/household | Breakdown of assessable income for pension tests (employment, self-employed, deemed income, rental income, foreign pensions). |
| `gifting_over_threshold_past_5_years` | number   | per-person  | Value of gifts over thresholds in past 5 years. |
| `rent_paid`                       | number       | per-person/household | Rent paid (for rent assistance). |
| `work_bonus_eligible_flag`        | bool         | per-person  | Whether work bonus rules may apply. |

---

## 10. Entity: Company, Trust, SMSF

### 10.1 Company parameters

| ID                                | Type / Shape | Scope     | Description |
|-----------------------------------|--------------|-----------|-------------|
| `company_id`                      | string       | per-company | Company identifier. |
| `aggregated_turnover`            | number       | per-company | Aggregated turnover for BRE tests. |
| `base_rate_entity_flag`          | bool         | per-company | Eligibility for base rate entity tax rate. |
| `company_tax_rate`               | number       | per-company | Applicable tax rate (25% / 30%). |
| `profit_before_tax`              | number       | per-company | Accounting profit before tax. |
| `taxable_income`                 | number       | per-company | Taxable income. |
| `franked_dividends_paid`         | number       | per-company | Franked dividends paid. |
| `unfranked_dividends_paid`       | number       | per-company | Unfranked dividends paid. |
| `franking_account_opening_balance` | number     | per-company | Opening franking account balance. |
| `franking_credits_generated`     | number       | per-company | Credits generated (company tax paid, etc.). |
| `franking_debits`                | number       | per-company | Debits (dividends, tax refunds, etc.). |
| `retained_earnings`              | number       | per-company | Retained earnings balance. |

### 10.2 Trust parameters

| ID                               | Type / Shape | Scope     | Description |
|----------------------------------|--------------|-----------|-------------|
| `trust_id`                       | string       | per-trust | Trust identifier. |
| `trust_net_income`              | number       | per-trust | Trust net income for distribution. |
| `trust_distribution_components_by_beneficiary` | list/struct | per-trust | Per-beneficiary components: ordinary income, capital gains, franked income, etc. |
| `upe_to_company_amounts`        | number       | per-trust | Unpaid present entitlements to corporate beneficiaries (Div 7A risk). |
| `trust_deed_distribution_constraints_flag` | bool | per-trust | Whether distributions are constrained (simple flag). |

### 10.3 SMSF (entity-level) parameters

| ID                               | Type / Shape | Scope     | Description |
|----------------------------------|--------------|-----------|-------------|
| `smsf_id`                        | string       | per-smsf  | SMSF identifier. |
| `smsf_taxable_income_ordinary`  | number       | per-smsf  | Ordinary taxable income in SMSF. |
| `smsf_taxable_income_non_arm_length` | number   | per-smsf  | Non-arm’s length income (NALI). |
| `smsf_ecpi_proportion`          | number       | per-smsf  | ECPI proportion for exempt pension income. |
| `smsf_contributions_by_member`  | list/struct  | per-smsf  | Contributions by member (links to super contributions). |
| `smsf_pensions_by_member`       | list/struct  | per-smsf  | Pensions (balances and drawdowns) by member. |

---

## 11. Scenario & Assumption Controls

| ID                           | Type / Shape | Scope         | Description |
|------------------------------|--------------|---------------|-------------|
| `inflation_rate`             | number       | per-scenario  | CPI assumption (annual). |
| `wage_growth_rate`           | number       | per-scenario  | Wage growth assumption (annual). |
| `property_growth_rate_default` | number     | per-scenario  | Default property price growth assumption. |
| `equity_return_assumption`   | number       | per-scenario  | Expected equity return. |
| `fixed_income_return_assumption` | number   | per-scenario  | Expected fixed income return. |
| `cash_return_assumption`     | number       | per-scenario  | Expected cash return. |
| `tax_brackets_set_id`        | string       | per-scenario  | Identifier for tax bracket set in use. |
| `super_contribution_caps_set_id` | string   | per-scenario  | Identifier for super cap settings. |
| `age_pension_thresholds_set_id` | string    | per-scenario  | Identifier for Age Pension thresholds. |
| `interest_rate_shock_flag`   | bool         | per-scenario  | Whether a rate shock applies in stress scenario. |
| `income_shock_flag`          | bool         | per-scenario  | Whether an income shock applies. |
| `market_crash_flag`          | bool         | per-scenario  | Whether a market crash scenario applies. |
| `projection_horizon_years`   | int          | per-scenario  | Number of years to project. |
| `discount_rate_for_npv`      | number       | per-scenario  | Discount rate for NPV calculations. |
| `explainability_mode`        | enum         | per-scenario  | Whether outputs should include short/long explanations. |

---

## 12. Explainability & Trace

| ID          | Type / Shape | Scope        | Description |
|-------------|--------------|--------------|-------------|
| `trace_log` | list/struct  | per-scenario | Optional structured trace entries `{calc_id, entity_id, field, year_index, severity, explanation, metadata}` used for debugging, auditability, and LLM-generated explanations. |
