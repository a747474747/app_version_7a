# Canonical Calculations – MVP

This file defines the **canonical calculation types** the Compute Engine must eventually support for the **MVP** of Frankie’s Finance / Veris Finance.

- Each item is a **calculation type**, not an implementation.
- IDs use the pattern `CAL-<DOMAIN>-<NNN>`.
- `mvp_tier`:
  - `core` = essential for early MVP (Phase 2–3 “golden” calculations).
  - `extended` = still part of MVP, but can land in later phases.

---

## 0. Legend

Each row:

- **ID** – Canonical calculation identifier.
- **Name** – Short human-readable label.
- **Domain** – Tax / Super / Property / Debt / Insurance / Plan / etc.
- **MVP Tier** – `core` or `extended`.
- **Description** – What this calculation is for (high-level only).

---

## 1. Core income tax & offsets (Personal Income Tax – `CAL-PIT-*`)

| ID              | Name                                                | Domain | MVP Tier | Description |
|-----------------|-----------------------------------------------------|--------|----------|-------------|
| CAL-PIT-001     | PAYG income tax on taxable income (resident)        | Tax    | core     | Compute income tax based on taxable income and marginal tax scales for a resident individual. |
| CAL-PIT-002     | Medicare levy                                       | Tax    | core     | Compute Medicare levy payable based on taxable income and relevant thresholds. |
| CAL-PIT-003     | Medicare levy surcharge                             | Tax    | extended | Compute MLS based on income, private health insurance status and thresholds. |
| CAL-PIT-004     | Tax offsets aggregation                             | Tax    | core     | Aggregate applicable tax offsets to reduce basic tax (e.g. low-income, seniors where applicable). |
| CAL-PIT-005     | Net tax payable / refund                            | Tax    | core     | Derive final tax payable or refundable after PAYG withheld, offsets and credits. |
| CAL-PIT-006     | Effective tax rate                                  | Tax    | extended | Compute average and marginal tax rates for the client for the tax year. |
| CAL-PIT-007     | Deductible expenses impact                          | Tax    | extended | Calculate tax saving from additional deductible expenses (work-related, donations, fees). |
| CAL-PIT-008     | HELP / HECS compulsory repayment                    | Tax    | extended | Estimate HELP/HECS repayment based on repayment income and thresholds. |
| CAL-PIT-009     | Tax on interest income                              | Tax    | extended | Combine interest income into taxable income and show marginal tax impact. |
| CAL-PIT-010     | Tax on other non-salary income (simple)             | Tax    | extended | Incorporate side-hustle or other assessable income into total taxable income. |
| CAL-PIT-011     | Assessable income aggregation                       | Tax    | core     | Aggregate all assessable income components (salary, allowances, interest, dividends, rent, business, net capital gain) into total assessable income. |
| CAL-PIT-012     | Taxable income derivation                           | Tax    | core     | Derive taxable income from assessable income by subtracting allowable deductions and applying any loss offsets. |
| CAL-PIT-013     | Tax-free threshold application                      | Tax    | core     | Apply the tax-free threshold (or its removal where elected/required) to determine tax on lower income ranges. |
| CAL-PIT-014     | Low Income Tax Offset (LITO)                        | Tax    | extended | Compute LITO entitlement and reduction based on taxable income. |
| CAL-PIT-015     | Low and Middle/Successor Offsets (LIMTO-style)      | Tax    | extended | Compute any additional low/middle income or successor offsets (as per current law) and integrate into total offsets. |
| CAL-PIT-016     | Senior Australians & Pensioners Offset (SAPTO)      | Tax    | extended | Estimate SAPTO entitlement for eligible clients based on income and marital status (simplified rules). |
| CAL-PIT-017     | Spouse / dependant-related offsets (simple)         | Tax    | extended | Calculate simple spouse/dependant offsets where applicable, under a simplified assumptions model. |
| CAL-PIT-018     | Foreign income & foreign tax offset (simple)        | Tax    | extended | Incorporate foreign employment/investment income and apply a simplified foreign tax offset calculation. |
| CAL-PIT-019     | Reportable fringe benefits inclusion                | Tax    | extended | Add reportable fringe benefits to adjusted taxable income (ATI) where relevant for means-tested items. |
| CAL-PIT-020     | Lump sum in arrears averaging (simplified)          | Tax    | extended | Provide a simplified tax estimate for employment-related lump sums attributable to prior years. |
| CAL-PIT-021     | PAYG withholding aggregation                        | Tax    | core     | Aggregate PAYG withheld from multiple employers/payers for comparison against final tax payable. |
| CAL-PIT-022     | Reportable super contributions adjustment           | Tax    | extended | Include reportable employer and personal deductible contributions in adjusted income for tests and offsets. |
| CAL-PIT-023     | Adjusted Taxable Income (ATI) for means tests       | Tax    | extended | Derive ATI by starting from taxable income and adjusting for fringe benefits, foreign income, reportable super and investment losses. |
| CAL-PIT-024     | Rental loss / business loss offset against salary   | Tax    | extended | Apply rules for offsetting net rental or business losses against salary/wage income in deriving taxable income. |
| CAL-PIT-025     | Investment expense deductibility check (simple)     | Tax    | extended | Determine whether basic investment-related expenses are deductible and quantify their effect on taxable income. |
| CAL-PIT-026     | Salary sacrifice vs after-tax contribution impact   | Tax    | extended | Compare net-of-tax outcomes when redirecting part of salary into pre-tax (salary sacrifice) versus after-tax contributions. |
| CAL-PIT-027     | Bracket indexation effect (reference-only)          | Tax    | extended | Model the effect of projected indexation of tax brackets on future-year tax, for scenario projections and rule maintenance. |
| CAL-PIT-028     | Medicare & MLS combined liability summary           | Tax    | extended | Summarise total Medicare levy and MLS liability as a combined figure for reporting and planning. |
| CAL-PIT-029     | Tax payable by income segment (bracket breakdown)   | Tax    | extended | Break down tax payable by marginal tax bracket to support explanations and visualisations. |
| CAL-PIT-030     | Year-on-year tax comparison                         | Tax    | extended | Compare current-year tax, taxable income and effective rates with prior year(s) for trend and shock analysis. |

**Notes (golden/core):**  
- `CAL-PIT-001`, `CAL-PIT-002`, `CAL-PIT-004`, `CAL-PIT-005` form the core “PAYG + offsets” golden calculation set.  
- For MVP, you can treat many of the extended items (e.g. `CAL-PIT-014`–`CAL-PIT-030`) as **stubs or simplified rules** and prioritise full implementation of 001–005, 011–013, and 021.

---

## 2. Investment tax, CGT & franking (`CAL-CGT-*`, `CAL-PFL-*`)

| ID              | Name                                                | Domain | MVP Tier | Description |
|-----------------|-----------------------------------------------------|--------|----------|-------------|
| CAL-CGT-001     | Capital gain/loss on asset disposal                 | Tax    | core     | Compute capital gain or loss on disposal of a single CGT asset (proceeds minus cost base/reduced cost base). |
| CAL-CGT-002     | CGT discount (individuals)                          | Tax    | core     | Apply 50% CGT discount for eligible assets held > 12 months by individuals (and 33⅓% for certain funds, if modelled). |
| CAL-CGT-003     | Capital loss calculation & classification           | Tax    | extended | Determine capital losses on disposal and classify as current-year or carried-forward losses. |
| CAL-CGT-004     | Net capital gain for the year                       | Tax    | extended | Net capital gains and losses across assets (including prior-year losses) to derive net capital gain under ordering rules. |
| CAL-CGT-005     | CGT tax payable on net capital gain                 | Tax    | extended | Incorporate net capital gain into taxable income and compute incremental tax attributable to CGT events. |
| CAL-CGT-006     | CGT event type (simplified classification)          | Tax    | extended | Classify common CGT events for individuals (e.g. A1, C1) under a simplified rule set for scenario modelling and explanation. |
| CAL-CGT-007     | CGT cost base components (simplified)               | Tax    | extended | Aggregate basic cost base elements (purchase price, incidental costs, capital improvements) for common assets. |
| CAL-CGT-008     | CGT main residence interaction (simple flag)        | Tax    | extended | Provide a simple flag/estimate for main-residence versus investment use where relevant to CGT projections (no complex 6-year rule modelling in MVP). |
| CAL-CGT-009     | CGT discount eligibility test                       | Tax    | extended | Determine whether an asset meets minimum criteria for discount (ownership period, entity type, asset type). |
| CAL-CGT-010     | CGT on managed fund/ETF CGT components (simple)     | Tax    | extended | Incorporate CGT-attributed components from managed funds/ETFs into the individual’s CGT and net capital gain calculation. |

| ID              | Name                                                | Domain | MVP Tier | Description |
|-----------------|-----------------------------------------------------|--------|----------|-------------|
| CAL-PFL-101     | Dividend gross-up (franking credits)                | Tax    | extended | Gross up franked dividends and compute franking credit amounts for inclusion in assessable income and offset calculations. |
| CAL-PFL-102     | Tax impact of franked / unfranked dividends         | Tax    | extended | Combine franked and unfranked dividends into taxable income and reflect franking credits as tax offsets. |
| CAL-PFL-103     | Managed fund tax components (simple split)          | Tax    | extended | Handle basic splitting of trust/fund distributions into interest, dividends, CGT and other components for tax purposes. |
| CAL-PFL-104     | Negative gearing tax benefit (interest only)        | Tax    | core     | Compute deductible loss from investment property or portfolio interest and quantify the resulting tax saving. |
| CAL-PFL-105     | Investment income after tax                         | Tax    | extended | Calculate after-tax income from a simple investment portfolio (interest, dividends, basic trust distributions) for a given year. |
| CAL-PFL-106     | Foreign-sourced investment income (simple)          | Tax    | extended | Incorporate foreign dividends/interest into assessable income and apply a simplified foreign tax offset when foreign tax has been withheld. |
| CAL-PFL-107     | DRP / reinvested distributions cost-base adjustment | Tax    | extended | Adjust cost base of share/ETF holdings for dividend reinvestment plans and reinvested managed fund distributions. |
| CAL-PFL-108     | Investment expense allocation to income types       | Tax    | extended | Allocate common investment expenses (e.g. brokerage, platform fees) across interest, dividends and CGT components for deduction modelling. |
| CAL-PFL-109     | Portfolio tax drag estimate                         | Tax    | extended | Estimate the reduction in pre-tax portfolio returns due to ongoing income tax on interest, dividends and realised gains. |
| CAL-PFL-110     | Simple tax-lot selection effect (FIFO vs parcel)    | Tax    | extended | Provide a simplified comparison of capital gains under FIFO versus manual parcel selection for a single disposal event. |

**Notes (golden/core):**  
- `CAL-CGT-002` (CGT discount) and `CAL-PFL-104` (negative gearing interest) appear in the “four golden” set.  
- For early MVP, prioritise full implementation of `CAL-CGT-001`–`CAL-CGT-002`, `CAL-CGT-004`–`CAL-CGT-005`, and `CAL-PFL-101`–`CAL-PFL-105`, with the remaining items treated as simplified or stubbed calculations.

---

## 3. Superannuation contributions & tax (`CAL-SUP-*` – contributions)

| ID              | Name                                                        | Domain   | MVP Tier | Description |
|-----------------|-------------------------------------------------------------|----------|----------|-------------|
| CAL-SUP-001     | Employer SG contribution amount                             | Super    | extended | Compute mandatory employer SG contributions from salary/wage base (using a configurable SG rate and base definition). |
| CAL-SUP-002     | Total concessional contributions                            | Super    | core     | Sum employer SG, salary sacrifice and deductible personal contributions for the year. |
| CAL-SUP-003     | Concessional contributions cap utilisation                  | Super    | core     | Check total concessional contributions against the applicable concessional cap and show remaining cap or excess. |
| CAL-SUP-004     | Carry-forward concessional cap availability                 | Super    | extended | Track unused concessional caps over prior years and estimate available carry-forward amount (simplified rules for eligibility). |
| CAL-SUP-005     | Non-concessional contributions total                        | Super    | extended | Sum non-concessional contributions (after-tax contributions, spouse contributions received, etc.) for the year. |
| CAL-SUP-006     | Non-concessional contributions cap utilisation              | Super    | extended | Check non-concessional contributions against the relevant cap and bring-forward rules (simplified age/TSB logic). |
| CAL-SUP-007     | Contributions tax inside super                              | Super    | core     | Compute 15% contributions tax on concessional contributions at the fund level. |
| CAL-SUP-008     | Division 293 additional tax                                 | Super    | core     | Estimate additional 15% tax on concessional contributions for high-income individuals (simplified Div 293 threshold test). |
| CAL-SUP-009     | Net contribution added to balance                           | Super    | core     | Calculate net amount added to super account after contributions tax and Division 293 adjustments. |
| CAL-SUP-010     | Super caps & TSB / TBC flags (simplified)                   | Super    | extended | Flag if current-year or planned contributions are likely affected by TSB/TBC limits using a simplified ruleset. |

| ID              | Name                                                        | Domain   | MVP Tier | Description |
|-----------------|-------------------------------------------------------------|----------|----------|-------------|
| CAL-SUP-011     | Salary sacrifice capacity                                   | Super    | extended | Determine maximum additional salary sacrifice possible without breaching concessional cap, given existing SG and planned deductible contributions. |
| CAL-SUP-012     | Personal deductible contribution limit                      | Super    | extended | Estimate maximum personal deductible contribution allowed, considering SG, salary sacrifice and concessional caps. |
| CAL-SUP-013     | Concessional vs non-concessional mix comparison             | Super    | extended | Compare after-tax outcomes of directing additional savings into concessional versus non-concessional contributions. |
| CAL-SUP-014     | Government co-contribution eligibility & amount (simple)    | Super    | extended | Assess basic eligibility for the government co-contribution and estimate the potential co-contribution amount based on income and NCC level. |
| CAL-SUP-015     | Spouse contribution tax offset estimate                     | Super    | extended | Estimate potential spouse contribution tax offset based on receiving spouse’s income and contribution amount. |
| CAL-SUP-016     | Downsizer contribution eligibility & capacity (simple)      | Super    | extended | Provide a simplified eligibility check and maximum contribution amount for downsizer contributions after sale of a qualifying home. |
| CAL-SUP-017     | End-of-year TSB projection for cap tests                    | Super    | extended | Project total super balance at 30 June to support TSB-related tests (contribution eligibility, bring-forward, co-contribution flags). |
| CAL-SUP-018     | Concessional excess contributions estimate                  | Super    | extended | Estimate the amount by which concessional contributions exceed the cap and approximate additional tax/liability under simplified excess rules. |
| CAL-SUP-019     | Non-concessional bring-forward trigger & remaining capacity | Super    | extended | Determine if NCCs have triggered a bring-forward period and calculate remaining NCC capacity for the bring-forward window under simplified rules. |
| CAL-SUP-020     | Aggregate contributions summary by type                     | Super    | core     | Summarise all contributions for the year by type (SG, salary sacrifice, personal deductible, NCC, spouse, downsizer) for reporting and scenario comparisons. |
| CAL-SUP-021     | Employer SG shortfall estimate                              | Super    | extended | Compare actual SG contributions received against expected statutory minimum to flag potential SG shortfalls (approximate only, not compliance-grade). |
| CAL-SUP-022     | Contribution timing effect (intra-year vs year-end)         | Super    | extended | Show impact of making contributions earlier or later in the year on end-of-year balance and contributions tax (simple earnings assumption). |
| CAL-SUP-023     | Multi-fund concessional cap aggregation                     | Super    | extended | Aggregate concessional contributions across multiple funds to test against a single cap for the individual. |
| CAL-SUP-024     | Multi-fund non-concessional cap aggregation                 | Super    | extended | Aggregate non-concessional contributions across multiple funds for cap and bring-forward tests. |
| CAL-SUP-025     | Contribution source tracing (personal vs employer)          | Super    | extended | Attribute contributions back to source (employer, personal, spouse, downsizer) to assist with tax treatment and reporting explanations. |

**Notes (golden/core):**  
- `CAL-SUP-002`, `CAL-SUP-003`, `CAL-SUP-007`, `CAL-SUP-008`, `CAL-SUP-009` collectively cover the “super contributions + Div 293” golden path.  
- For early MVP, focus on full implementation of `CAL-SUP-001`–`CAL-SUP-003`, `CAL-SUP-007`–`CAL-SUP-009`, and `CAL-SUP-020`, with the other items available as simplified or stubbed calculations for later refinement.


---

## 4. Super accumulation & retirement projections (`CAL-SUP-*` – accumulation & pensions)

### 4.1 Accumulation phase (`CAL-SUP-2xx`)

| ID              | Name                                                        | Domain   | MVP Tier | Description |
|-----------------|-------------------------------------------------------------|----------|----------|-------------|
| CAL-SUP-201     | Super balance projection (accumulation)                     | Super    | extended | Project super balance over time using contributions, fees and assumed investment return (single option, constant return). |
| CAL-SUP-202     | Component split (taxable vs tax-free, simple)               | Super    | extended | Track rough split between taxable and tax-free components under simplified rules based on contribution types. |
| CAL-SUP-203     | Super earnings tax (accumulation phase)                     | Super    | extended | Estimate annual tax on earnings inside accumulation super using a flat tax rate assumption. |
| CAL-SUP-204     | Multi-option investment projection (simple)                 | Super    | extended | Project super balance where funds are allocated across multiple investment options, each with its own assumed return and fee structure. |
| CAL-SUP-205     | Salary growth & contributions escalation effect             | Super    | extended | Model impact of wage growth and escalating contribution rates on long-term accumulation balances. |
| CAL-SUP-206     | Fees impact & fee drag analysis                             | Super    | extended | Quantify the impact of administration, investment and advice fees on super balance over time (dollar and % reduction). |
| CAL-SUP-207     | Insurance premiums inside super (impact on balance)         | Super    | extended | Model the reduction to contributions/earnings flow from insurance premiums deducted within the fund. |
| CAL-SUP-208     | Blended contributions scenario comparison                   | Super    | extended | Compare projected balances under different contribution mixes (more concessional vs more non-concessional, or different salary sacrifice settings). |
| CAL-SUP-209     | Accumulation vs non-super investment comparison             | Super    | extended | Compare future values of investing via super versus investing outside super using different tax and fee assumptions. |
| CAL-SUP-210     | Total Super Balance (TSB) projection                        | Super    | extended | Project total super balance at key dates (e.g. each 30 June) to support TSB-related tests (contribution rules, TBC, NCC eligibility flags). |
| CAL-SUP-211     | Preservation age & condition of release flagging (simple)   | Super    | extended | Indicate when a member reaches preservation age and simple condition-of-release milestones for planning transitions to pension phase. |
| CAL-SUP-212     | Early access / lump sum withdrawal impact                   | Super    | extended | Model the impact of a lump sum withdrawal/partial commutation during accumulation on future balances. |
| CAL-SUP-213     | Accumulation risk band / volatility indicator               | Super    | extended | Provide a simple risk indicator for accumulation strategy based on asset allocation and member age. |

---

### 4.2 Retirement / pension phase (`CAL-SUP-3xx`)

| ID              | Name                                                        | Domain     | MVP Tier | Description |
|-----------------|-------------------------------------------------------------|------------|----------|-------------|
| CAL-SUP-301     | Retirement super income drawdown (simple)                   | Retirement | extended | Model a simple account-based pension drawdown pattern given a starting balance, draw rate and investment return assumption. |
| CAL-SUP-302     | Minimum pension drawdown requirement                        | Retirement | extended | Compute minimum pension draw amounts using simplified age-based factors and current year balance. |
| CAL-SUP-303     | Longevity of super under given drawdown                     | Retirement | extended | Estimate years until pension balance exhausts under specified drawdown pattern and return assumptions. |
| CAL-SUP-304     | Pension vs lump sum commencement strategy comparison         | Retirement | extended | Compare projected outcomes of taking benefits predominantly as an account-based pension versus lump sums at retirement. |
| CAL-SUP-305     | Transfer Balance Cap (TBC) usage at commencement (simple)   | Retirement | extended | Estimate TBC used when starting an account-based pension, using a simplified TBC and ignoring complex credits/debits. |
| CAL-SUP-306     | Mixed accumulation & pension arrangement projection          | Retirement | extended | Model a scenario where part of the balance remains in accumulation while part is in pension, projecting both and the combined outcome. |
| CAL-SUP-307     | Pension tax-free vs taxable payment split (member level)     | Retirement | extended | Estimate tax-free and taxable components of pension payments, feeding into personal income tax projections. |
| CAL-SUP-308     | Reversionary pension continuation (simple)                   | Retirement | extended | Provide a simplified projection of a reversionary pension continuing to a spouse, ignoring complex estate/planning rules. |
| CAL-SUP-309     | Sequencing risk illustration (basic)                         | Retirement | extended | Provide example scenarios of different return sequences on the same average return to illustrate sequencing risk for a pension strategy. |
| CAL-SUP-310     | Dynamic drawdown strategy comparison                         | Retirement | extended | Compare fixed-dollar, fixed-percentage and “floor and ceiling” dynamic drawdown strategies on pension sustainability. |
| CAL-SUP-311     | Retirement income floor from super                           | Retirement | extended | Estimate minimum sustainable income level from super that can be supported to a target age or probability of survival. |
| CAL-SUP-312     | Retirement income replacement ratio from super               | Retirement | extended | Compute proportion of pre-retirement income replaced by projected super-based income at and after retirement. |
| CAL-SUP-313     | Post-retirement super balance at target age                  | Retirement | extended | Project residual super balance at a specified age under given drawdown and investment assumptions. |
| CAL-SUP-314     | Commutation / lump-sum withdrawal impact in pension phase    | Retirement | extended | Model the impact of a partial commutation/lump-sum withdrawal from pension on future pension payments and balance longevity. |

**Notes (prioritisation for MVP):**  
- For early MVP, prioritise robust implementations of:  
  - `CAL-SUP-201` (accumulation projection),  
  - `CAL-SUP-203` (earnings tax),  
  - `CAL-SUP-210` (TSB projection – even if simplified),  
  - `CAL-SUP-301`–`CAL-SUP-303` (basic pension modelling and longevity).  
- Treat the remaining items as **simplified models or stubs** that can be refined once the core accumulation and pension engine is stable.

---
## 5. Debt, Mortgages & Lending (Reorganised by Calculation Category)

### 5.1 Foundation – Loan Mechanics & Stress Metrics (`CAL-FND-*`)

| ID           | Name                                            | Category   | MVP Tier | Description |
|--------------|-------------------------------------------------|------------|----------|-------------|
| CAL-FND-101  | P&I loan repayment schedule                     | Foundation | core     | Compute repayment amount and full amortisation schedule for a principal-and-interest loan. |
| CAL-FND-102  | Interest-only loan schedule                     | Foundation | extended | Compute interest-only repayments and interest cost over an interest-only period. |
| CAL-FND-103  | Extra repayment effect on loan term             | Foundation | extended | Estimate reduction in loan term and interest cost from making additional repayments. |
| CAL-FND-104  | Total interest cost over horizon                | Foundation | extended | Compute total interest paid over a specified period or over the life of a loan. |
| CAL-FND-105  | Interest rate change sensitivity                | Foundation | extended | Calculate new repayments and total interest cost under alternative interest rates. |
| CAL-FND-106  | Loan term sensitivity                           | Foundation | extended | Compare repayments and total interest cost for different loan terms (e.g. 25 vs 30 years). |
| CAL-FND-107  | Credit card payoff projection                   | Foundation | extended | Project time to repay a credit card balance under current versus recommended repayments. |
| CAL-FND-108  | Interest rate buffer tolerance                  | Foundation | extended | Estimate the maximum interest rate increase that can be sustained before cashflow turns negative. |
| CAL-FND-109  | IO vs P&I total cost comparison                 | Foundation | extended | Compare total interest cost and principal repaid between an interest-only strategy and immediate P&I. |
| CAL-FND-110  | Multi-debt payoff strategy (snowball/avalanche) | Foundation | extended | Model paydown time and interest cost under different debt payoff strategies (e.g. highest interest first). |
| CAL-FND-111  | Repayment holiday impact                        | Foundation | extended | Project additional interest and new term or repayment required after a repayment pause/holiday. |
| CAL-FND-112  | Arrears catch-up plan                           | Foundation | extended | Calculate extra repayments required over a given period to clear overdue amounts and normalise the loan. |
| CAL-FND-113  | Debt paydown time (adjusted)                    | Foundation | core     | Calculate time required to clear a debt given minimum repayments plus a recurring surplus cashflow amount. |
| CAL-FND-114  | Debt-to-income ratio                            | Foundation | extended | Compute gross debt-to-income ratio as a basic serviceability indicator. |
| CAL-FND-115  | Minimum repayment coverage                      | Foundation | extended | Calculate the ratio of actual repayments to minimum required repayments across all debts. |
| CAL-FND-116  | Mortgage stress indicator                       | Foundation | core     | Compute repayment-to-income ratios and classify mortgage stress based on defined thresholds. |
| CAL-FND-117  | Debt servicing ratio (DSR)                      | Foundation | core     | Calculate the ratio of total required debt payments (monthly) to net disposable income. |
| CAL-FND-118  | IO-to-P&I transition repayment                  | Foundation | core     | Compute the new minimum repayment and resulting “repayment shock” when an interest-only period ends and P&I begins. |

---

### 5.2 Property-Secured Lending & Home Loans (`CAL-PRP-*`)

| ID           | Name                                            | Category | MVP Tier | Description |
|--------------|-------------------------------------------------|----------|----------|-------------|
| CAL-PRP-301  | Loan-to-value ratio (LVR)                       | Property | core     | Compute LVR for a secured loan given property/security value and loan amount. |
| CAL-PRP-302  | Debt recycling capacity                         | Property | extended | Estimate how much non-deductible home debt can be progressively converted to deductible investment debt, given surplus cashflow and loan structure. |
| CAL-PRP-303  | Debt consolidation comparison                   | Property | extended | Compare total cost, term and repayments for existing separate debts versus a consolidated facility secured against property. |
| CAL-PRP-304  | Refinance comparison                            | Property | extended | Compare key metrics (repayments, interest, term) between current and proposed mortgage structures. |
| CAL-PRP-305  | Total refinance costs                           | Property | core     | Aggregate all upfront costs associated with refinancing (break fees, establishment fees, government charges, valuation). |
| CAL-PRP-306  | Net refinance benefit (NPV savings)             | Property | extended | Calculate the net present value (NPV) savings over a horizon after factoring in all refinance costs and interest differences. |
| CAL-PRP-307  | Equity release / cash-out capacity              | Property | extended | Calculate how much equity can be released while maintaining a target maximum LVR. |
| CAL-PRP-308  | Lenders Mortgage Insurance (LMI) estimate       | Property | extended | Provide a rough estimate of LMI premium based on loan amount and LVR bands. |
| CAL-PRP-309  | Bridging loan interest cost                     | Property | extended | Estimate interest and cashflow impact of a bridging loan over a specified bridging period. |
| CAL-PRP-310  | Offset account interest saving                  | Property | extended | Estimate reduction in interest cost and effective term from maintaining a given offset account balance linked to a mortgage. |
| CAL-PRP-311  | Redraw vs offset structure impact               | Property | extended | Compare cashflow flexibility and potential deductibility outcomes of using redraw versus offset for surplus cash. |
| CAL-PRP-312  | Split loan interest allocation                  | Property | extended | Allocate repayments and interest across multiple mortgage splits (e.g. home vs investment split). |
| CAL-PRP-313  | Borrowing capacity estimate (simple)            | Property | extended | Provide a simplified estimate of maximum mortgage borrowing capacity using standard income, expense and buffer assumptions. |
| CAL-PRP-314  | Borrowing capacity (comprehensive)              | Property | extended | Detailed calculation of maximum mortgage size based on gross income, declared expenses and lender assessment rate methodology. |
| CAL-PRP-315  | Serviceability repayment (stressed)             | Property | core     | Compute the monthly mortgage repayment using a stressed assessment rate (e.g. +3% buffer) for APRA-style serviceability testing. |
| CAL-PRP-316  | Fixed-rate break cost estimate                  | Property | extended | Provide a simple estimate of potential break costs for exiting a fixed-rate mortgage early. |
| CAL-PRP-317  | Fixed vs variable loan comparison               | Property | extended | Compare repayments, interest cost and qualitative risk characteristics for fixed, variable and split-rate mortgage structures. |

---

### 5.3 Investment & Margin Lending (`CAL-PFL-*`)

| ID           | Name                                            | Category           | MVP Tier | Description |
|--------------|-------------------------------------------------|--------------------|----------|-------------|
| CAL-PFL-401  | Line of credit interest cost                    | Investment Portfolio | extended | Estimate interest paid and potential tax deductibility for a flexible line-of-credit facility used for investment purposes. |
| CAL-PFL-402  | Deductible vs non-deductible interest split     | Investment Portfolio | extended | Split interest amounts between deductible (investment-related) and non-deductible (private/home) components for portfolio-related borrowing. |

---

### 5.4 Reporting & Governance – Lending Documentation (`CAL-RGX-*`)

| ID           | Name                                            | Category            | MVP Tier | Description |
|--------------|-------------------------------------------------|---------------------|----------|-------------|
| CAL-RGX-501  | Required interest deduction documentation       | Reporting/Governance | core     | Determine the documentation trail required to justify interest deductibility for investment loans (feeds the Advice/Compliance Engine, not client-facing maths). |

---

## 6. Property acquisition, holding & disposal (`CAL-PRP-*`)

### 6.1 Acquisition

| ID              | Name                                                | Domain   | MVP Tier | Description |
|-----------------|-----------------------------------------------------|----------|----------|-------------|
| CAL-PRP-001     | Upfront property purchase costs                     | Property | extended | Estimate total upfront costs: stamp duty, legal fees, inspections, lender fees, and other purchase-related costs. |
| CAL-PRP-002     | Net equity contribution                             | Property | extended | Compute buyer’s equity contribution including deposit and all upfront costs, net of any vendor rebates or incentives. |
| CAL-PRP-009     | Purchase price affordability band                   | Property | extended | Derive a minimum/maximum affordable purchase price band based on available deposit, target LVR and basic borrowing capacity inputs (links to debt calcs). |
| CAL-PRP-011     | Stamp duty estimate (simplified, per state)         | Property | extended | Provide a simplified estimate of stamp duty based on purchase price, property type and state/territory (banded assumptions, not exact schedule). |
| CAL-PRP-012     | Government vs non-government cost split             | Property | extended | Split upfront purchase costs into government charges (duty, registration) vs other costs (legal, inspections, lender fees) for clearer explanations. |

---

### 6.2 Holding / cashflow

| ID              | Name                                                | Domain   | MVP Tier | Description |
|-----------------|-----------------------------------------------------|----------|----------|-------------|
| CAL-PRP-003     | Annual property holding costs                       | Property | extended | Sum ongoing costs: rates, insurance, maintenance, body corporate, management, and other recurring expenses. |
| CAL-PRP-004     | Gross rental income                                 | Property | extended | Compute expected annual rental income using rent, occupancy rate and indexation assumptions. |
| CAL-PRP-005     | Net rental cashflow before tax                      | Property | core     | Compute rental income minus holding costs and interest, before tax. |
| CAL-PRP-006     | Net rental cashflow after tax                       | Property | core     | Combine net rental cashflow with negative gearing benefit and other rental-related tax effects to derive after-tax cashflow. |
| CAL-PRP-007     | Rental yield (gross and net)                        | Property | extended | Compute gross and net yield percentages based on property value and net cashflows. |
| CAL-PRP-013     | Property growth projection                          | Property | extended | Project property value over time using configurable growth rates (single or scenario-based). |
| CAL-PRP-014     | Capital works deduction (Div 43, simplified)        | Property | extended | Estimate annual building write-off for eligible income-producing properties under a simplified capital works depreciation model. |
| CAL-PRP-015     | Plant & equipment depreciation (Div 40, simplified) | Property | extended | Estimate annual decline in value of depreciable assets (e.g. fixtures, fittings) in a simplified schedule for rental properties. |
| CAL-PRP-016     | Land tax estimate (simplified)                      | Property | extended | Provide a rough estimate of land tax based on land value and state thresholds (ignoring complex aggregation rules). |
| CAL-PRP-017     | Cash-on-cash return                                 | Property | extended | Calculate cash-on-cash return for an investment property using net pre-tax or after-tax cashflow divided by total equity invested. |
| CAL-PRP-018     | Break-even rent level                               | Property | extended | Compute the rent required for the property to be cashflow neutral before tax (and optionally after tax). |
| CAL-PRP-021     | Property holding risk indicators                    | Property | extended | Provide simple risk metrics such as vacancy buffer (months of costs), interest rate sensitivity, and proportion of income tied to the property. |
| CAL-PRP-022     | Property concentration in net wealth                | Property | extended | Compute the percentage of total net wealth tied up in property (home + investments) to assess concentration risk. |

---

### 6.3 Equity, leverage & portfolio impact

| ID              | Name                                                | Domain   | MVP Tier | Description |
|-----------------|-----------------------------------------------------|----------|----------|-------------|
| CAL-PRP-008     | Property equity over time                           | Property | extended | Project outstanding loan balance, property value and owner’s equity over time using assumed growth and amortisation. |
| CAL-PRP-023     | Equity release capacity (property-specific view)    | Property | extended | Estimate how much equity can be released from one or more properties while respecting a specified maximum LVR across the portfolio. |
| CAL-PRP-024     | Investment vs home-equity allocation comparison     | Property | extended | Compare scenarios where additional borrowings are secured against the home versus an investment property, focusing on deductibility and risk. |

---

### 6.4 Disposal & CGT interaction

| ID              | Name                                                | Domain   | MVP Tier | Description |
|-----------------|-----------------------------------------------------|----------|----------|-------------|
| CAL-CGT-201     | Property CGT calculation (simple)                   | Tax      | extended | Compute capital gain and CGT on sale of an investment property under simple assumptions (single acquisition, no complex adjustments). |
| CAL-CGT-202     | Main residence exemption indicator (property)       | Tax      | extended | Provide a simplified indication of main residence CGT exemption applicability (full/partial/none) based on basic ownership and use inputs. |
| CAL-CGT-203     | 6-year rule / temporary absence (simple flag)       | Tax      | extended | Add a simple flag or adjustment for scenarios where the 6-year temporary absence rule might apply (no complex partial-year calculations). |
| CAL-PRP-025     | Sale transaction costs                              | Property | extended | Estimate selling costs such as agent commission, advertising, legal fees and other disbursements for a property sale. |
| CAL-PRP-026     | Net sale proceeds after loan payout & costs         | Property | core     | Compute net cash received on sale after paying out the loan, CGT estimate (from `CAL-CGT-201`) and selling costs. |
| CAL-PRP-027     | Hold vs sell comparison (investment property)       | Property | extended | Compare long-term outcomes (equity, cashflow, after-tax position) for holding a property versus selling and reinvesting elsewhere. |

---

### 6.5 Tenure decisions & housing strategy

| ID              | Name                                                | Domain   | MVP Tier | Description |
|-----------------|-----------------------------------------------------|----------|----------|-------------|
| CAL-PRP-010     | Buy vs rent comparison (simple)                     | Property | extended | Compare cashflows and equity outcomes for buying vs renting a home over a chosen horizon using simplified assumptions. |
| CAL-PRP-028     | Upgrade vs renovate comparison                      | Property | extended | Compare financial impact of renovating the existing home versus selling and purchasing an upgraded property. |
| CAL-PRP-029     | Rentvesting vs buy-to-live comparison               | Property | extended | Compare long-term wealth outcomes from rentvesting (renting home, owning investment property) versus buying a home to live in, with or without investment property. |
| CAL-PRP-030     | Time-to-upgrade / deposit build-up projection       | Property | extended | Project how long it will take to accumulate a sufficient deposit and equity position to upgrade to a target property value. |

**Notes (prioritisation for MVP):**  
- For early MVP, prioritise:  
  - Acquisition & holding: `CAL-PRP-001`–`CAL-PRP-006`, `CAL-PRP-007`, `CAL-PRP-008`.  
  - Disposal: `CAL-CGT-201`, `CAL-PRP-025`, `CAL-PRP-026`.  
  - Strategy views: `CAL-PRP-010` (buy vs rent) and `CAL-PRP-027` (hold vs sell) in simplified form.  
- Other items can start as **stubs or simplified formulas** that you refine as property-specific features become a bigger part of the app.

---

## 7. Non-property investment accumulation (Investment Portfolio – `CAL-PFL-*`)

### 7.1 Balance & cashflow projections

| ID              | Name                                                | Domain     | MVP Tier | Description |
|-----------------|-----------------------------------------------------|------------|----------|-------------|
| CAL-PFL-201     | Investment balance projection                       | Investment | extended | Project investment account balance with deposits, withdrawals, returns and fees (single blended return). |
| CAL-PFL-202     | Asset allocation breakdown                          | Investment | extended | Calculate allocation by asset class (cash, fixed interest, property, shares, alternatives, etc.). |
| CAL-PFL-203     | Required savings rate for target wealth             | Investment | extended | Compute required periodic contribution to reach a target balance by a given date, given starting balance and assumed return. |
| CAL-PFL-204     | Portfolio fees as % and $                           | Investment | extended | Compute total portfolio fees in dollars and percentage across platforms, funds and direct holdings. |
| CAL-PFL-205     | Simple volatility / risk indicator                  | Investment | extended | Provide a simple risk score using asset allocation, client risk profile and age-based heuristics. |
| CAL-PFL-206     | Rebalancing trades required                         | Investment | extended | Calculate trades (buy/sell amounts) needed to restore target asset allocation from current allocation. |
| CAL-PFL-207     | Lump sum vs dollar-cost-averaging comparison        | Investment | extended | Compare outcomes of investing a lump sum immediately versus staging contributions over time. |
| CAL-PFL-208     | Multi-account portfolio roll-up                     | Investment | extended | Aggregate holdings and cashflows across multiple investment accounts to a single consolidated portfolio. |
| CAL-PFL-209     | Contribution escalation impact                      | Investment | extended | Model the effect of escalating contributions (e.g. +X% per year) on long-term portfolio balance. |
| CAL-PFL-210     | Withdrawal strategy projection (pre-retirement)     | Investment | extended | Project portfolio under occasional/irregular withdrawals for goals (education, renovations, etc). |

---

### 7.2 Returns, yield & performance

| ID              | Name                                                | Domain     | MVP Tier | Description |
|-----------------|-----------------------------------------------------|------------|----------|-------------|
| CAL-PFL-211     | Portfolio income yield (cash yield)                 | Investment | extended | Calculate current income yield (dividends, distributions, interest) as a percentage of portfolio value. |
| CAL-PFL-212     | Total return decomposition                          | Investment | extended | Break portfolio total return into income (dividends/interest) and capital growth components. |
| CAL-PFL-213     | Time-weighted rate of return (TWRR, simple)         | Investment | extended | Estimate time-weighted return over a period under simplified assumptions about cashflow timing. |
| CAL-PFL-214     | Money-weighted rate of return (MWRR/IRR, simple)    | Investment | extended | Approximate investor-specific return (IRR) considering timing and size of contributions/withdrawals. |
| CAL-PFL-215     | Benchmark comparison                                | Investment | extended | Compare portfolio performance to a chosen benchmark index or composite (return difference, tracking gap). |
| CAL-PFL-216     | After-tax return estimate                           | Investment | extended | Estimate after-tax return on the portfolio using simple tax assumptions for interest, dividends and realised gains. |
| CAL-PFL-217     | Real (inflation-adjusted) return estimate           | Investment | extended | Compute real return by adjusting nominal returns for inflation assumptions. |

---

### 7.3 Risk, diversification & constraints

| ID              | Name                                                | Domain     | MVP Tier | Description |
|-----------------|-----------------------------------------------------|------------|----------|-------------|
| CAL-PFL-218     | Diversification score (by asset class)              | Investment | extended | Provide a simple diversification score based on spread across major asset classes. |
| CAL-PFL-219     | Security concentration check                        | Investment | extended | Identify and quantify concentration risk in single securities or managers above a defined threshold. |
| CAL-PFL-220     | Sector/industry concentration check                 | Investment | extended | Assess exposure to particular sectors/industries relative to simple guide rails or benchmarks. |
| CAL-PFL-221     | Currency exposure estimate                          | Investment | extended | Estimate proportion of portfolio exposed to foreign currency versus AUD. |
| CAL-PFL-222     | Portfolio risk band vs risk profile                 | Investment | extended | Compare current strategic allocation risk band to client risk profile (e.g. defensive vs growth) and flag misalignment. |
| CAL-PFL-223     | Drawdown risk illustration (simple)                 | Investment | extended | Provide simple historical/statistical drawdown scenarios for the portfolio mix (e.g. typical max drawdown). |
| CAL-PFL-224     | Liquidity profile                                   | Investment | extended | Categorise holdings by liquidity (daily, monthly, illiquid) and compute percentages in each bucket. |

---

### 7.4 Tax-aware accumulation & structure comparison

| ID              | Name                                                | Domain     | MVP Tier | Description |
|-----------------|-----------------------------------------------------|------------|----------|-------------|
| CAL-PFL-225     | Tax-aware accumulation comparison (inside vs outside super) | Investment | extended | Compare long-term accumulation in a standard investment account versus super using different tax assumptions. |
| CAL-PFL-226     | Investment structure comparison (individual vs trust vs company – simple) | Investment | extended | Provide a simplified comparison of after-tax outcomes across holding structures using assumed tax rates. |
| CAL-PFL-227     | Realisation strategy impact (realise now vs later)  | Investment | extended | Compare tax and after-tax value outcomes when realising a capital gain now versus deferring to a later date. |
| CAL-PFL-228     | Distribution vs accumulation fund comparison        | Investment | extended | Compare after-tax accumulation between distribution-paying versus accumulation-focused investment options. |

---

### 7.5 Behaviour, strategy & “what if” settings

| ID              | Name                                                | Domain     | MVP Tier | Description |
|-----------------|-----------------------------------------------------|------------|----------|-------------|
| CAL-PFL-229     | Risk profile to model portfolio mapping             | Investment | extended | Map a risk profile (e.g. Balanced, High Growth) to a model asset allocation and expected risk/return inputs. |
| CAL-PFL-230     | Behavioural “stay invested vs switch to cash” impact| Investment | extended | Illustrate the long-term impact of staying invested versus switching to cash during a market downturn. |
| CAL-PFL-231     | Savings vs investing trade-off                      | Investment | extended | Compare long-term balances if surplus cash is held in a low-yield savings account versus invested according to the portfolio. |
| CAL-PFL-232     | ESG / screen impact (simple)                        | Investment | extended | Provide a simplified projection of how applying ESG or exclusion screens might affect diversification and expected returns. |
| CAL-PFL-233     | Glidepath / de-risking strategy projection          | Investment | extended | Model a gradual shift from growth to defensive asset allocation as the client approaches a target date (e.g. retirement). |

**Notes (prioritisation for MVP):**  
- For early MVP, robust implementations of these are most valuable:  
  - Core accumulation engine: `CAL-PFL-201`, `CAL-PFL-203`, `CAL-PFL-204`, `CAL-PFL-207`.  
  - Risk & allocation: `CAL-PFL-202`, `CAL-PFL-205`, `CAL-PFL-218`, `CAL-PFL-222`.  
  - Simple tax-aware view: `CAL-PFL-216`, `CAL-PFL-225`.  
- The rest can be **simplified or stubbed** at first, then deepened as the portfolio module matures.

---

## 8. Cashflow, budgeting & buffers (Foundation – `CAL-FND-*`)

### 8.1 Normalisation & surplus

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-FND-201     | Normalised income (annual / monthly)                | Cashflow  | core     | Convert and aggregate different income streams (salary, bonus, rental, business, benefits) to a consistent period. |
| CAL-FND-202     | Normalised expenses (annual / monthly)              | Cashflow  | core     | Convert and aggregate expenses (fixed and variable) to a consistent period. |
| CAL-FND-203     | Savings capacity (surplus / deficit)                | Cashflow  | core     | Compute surplus/deficit per period after normalised income and expenses. |
| CAL-FND-204     | Savings rate (% of income)                          | Cashflow  | extended | Calculate savings as a percentage of gross and net income. |
| CAL-FND-205     | Emergency fund months of expenses                   | Cashflow  | extended | Compute how many months of core expenses current cash buffer can cover. |
| CAL-FND-206     | Discretionary vs fixed expense split                | Cashflow  | extended | Estimate the proportion of expenses that are fixed/committed versus discretionary. |
| CAL-FND-207     | Income volatility indicator                         | Cashflow  | extended | Provide a simple indicator of income stability (e.g. proportion from stable salary vs variable/irregular sources). |
| CAL-FND-208     | Expense categorisation by bucket                    | Cashflow  | extended | Allocate expenses into key buckets (housing, transport, food, lifestyle, children, debt, etc.) and compute each bucket’s share. |
| CAL-FND-209     | Discretionary headroom after commitments            | Cashflow  | extended | Calculate surplus after fixed commitments (rent/mortgage, utilities, debt repayments), highlighting “true” discretionary capacity. |
| CAL-FND-210     | Irregular bill smoothing requirement                | Cashflow  | extended | Compute the average monthly amount required to smooth irregular/annual bills (regos, insurance, holidays) into a steady provision. |
| CAL-FND-211     | Cashflow seasonality / month-to-month variance      | Cashflow  | extended | Provide a simple variability score for month-to-month cashflows where data is available or estimated. |
| CAL-FND-212     | Net disposable income after tax & mandatory items   | Cashflow  | extended | Estimate net disposable income after tax, super contributions and mandatory deductions to feed affordability tests. |

---

### 8.2 Buffers, goals & “time to target”

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-FND-213     | Buffer build time to target emergency fund          | Cashflow  | extended | Estimate how long it will take to reach a target emergency fund level, given current surplus and contributions to savings. |
| CAL-FND-214     | Savings goal timeline                               | Cashflow  | extended | Project how long it will take to reach a specific short–medium-term savings goal at current contribution levels. |
| CAL-FND-215     | Required surplus for time-bound goal                | Cashflow  | extended | Compute the required ongoing savings amount to reach a specific cash-based goal by a target date. |
| CAL-FND-216     | One-off purchase affordability check                | Cashflow  | extended | Assess whether a planned lump-sum purchase (e.g. car, holiday) is affordable without breaching buffer thresholds. |
| CAL-FND-217     | Multi-goal cash allocation suggestion (simple)      | Cashflow  | extended | Provide a simple allocation of surplus across multiple goals (buffer, debt reduction, investing) based on configurable priorities. |
| CAL-FND-218     | Pay-yourself-first allocation                       | Cashflow  | extended | Calculate recommended “pay-yourself-first” savings contributions as a fixed amount or percentage of income. |

---

### 8.3 Affordability, debt service & stress tests

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-FND-219     | Debt servicing coverage from surplus                | Cashflow  | extended | Determine how much additional debt repayment (or new debt) can be supported by current surplus without going negative. |
| CAL-FND-220     | New recurring commitment affordability              | Cashflow  | extended | Test whether a new recurring expense (e.g. private school fees, gym membership, subscription) is affordable under current and stressed assumptions. |
| CAL-FND-221     | Cashflow shock test – interest rate rise            | Cashflow  | extended | Model the impact on surplus/deficit if interest rates on variable debts increase by a specified buffer (e.g. +2–3%). |
| CAL-FND-222     | Cashflow shock test – income reduction              | Cashflow  | extended | Model the effect of a partial income loss (e.g. one partner ceases work, hours reduced) on cashflow and buffer sustainability. |
| CAL-FND-223     | Minimum sustainable living cost estimate            | Cashflow  | extended | Provide an estimate of “bare-bones” living expenses by stripping out discretionary categories. |
| CAL-FND-224     | Lifestyle inflation detection                       | Cashflow  | extended | Compare year-on-year (or scenario vs baseline) expense levels to detect lifestyle creep relative to income changes. |
| CAL-FND-225     | Household affordability index                       | Cashflow  | extended | Provide a simple index of affordability using ratios such as housing cost to income, total commitments to income, and buffer months. |
| CAL-FND-226     | Financial stress indicator                          | Cashflow  | extended | Combine surplus, buffer months, and commitment ratios into a simple stress flag (e.g. Comfortable / Tight / At Risk). |

---

### 8.4 Planning, pipeline & behavioural views

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-FND-227     | 12-month cash pipeline forecast (simple)            | Cashflow  | extended | Project month-by-month cash position over the next 12 months using normalised income, expenses and known one-off items. |
| CAL-FND-228     | Tax bill provisioning estimate                      | Cashflow  | extended | Estimate the provision required each month to cover expected end-of-year tax payable for PAYG-withholding gaps or business income. |
| CAL-FND-229     | Irregular income smoothing (contractor/freelancer)  | Cashflow  | extended | Suggest a target “personal PAYG” draw and savings buffer for clients with lumpy or self-employed income. |
| CAL-FND-230     | Spending category caps (derived limits)             | Cashflow  | extended | Derive suggested monthly caps for key discretionary categories (e.g. dining, entertainment, shopping) based on surplus and goals. |
| CAL-FND-231     | Income diversification score                        | Cashflow  | extended | Score how diversified household income is across employers, industries and income types (salary, rent, business). |
| CAL-FND-232     | Budget adherence variance (plan vs actual)          | Cashflow  | extended | Calculate variance between planned and actual spending by category where historical data is available. |
| CAL-FND-233     | Savings habit consistency indicator                 | Cashflow  | extended | Assess consistency of savings behaviour over time (e.g. % of months target savings were achieved). |

**Notes (prioritisation for MVP):**  
- For early MVP, the **essential cashflow engine** is:  
  - `CAL-FND-201`–`CAL-FND-203`, `CAL-FND-205`, `CAL-FND-213`, `CAL-FND-219`, `CAL-FND-221`, `CAL-FND-222`, `CAL-FND-226`.  
- Many of the others can start as **lightweight or heuristic** calculations that you refine as you integrate real transaction data or richer categorisation in later phases.

---

## 9. Insurance & protection needs (Insurance & Risk – `CAL-INS-*`)

### 9.1 Capital needs – lump sum (Life/TPD/Trauma)

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-INS-001     | Debt clearance requirement                          | Insurance | extended | Compute capital required to clear all debts on death or total permanent disablement (with optional selection of which debts to clear). |
| CAL-INS-002     | Family income replacement requirement               | Insurance | extended | Estimate capital needed to replace after-tax income for dependants for a set period, allowing for indexation and investment return assumptions. |
| CAL-INS-003     | Total life/TPD insurance need                       | Insurance | extended | Aggregate capital needs (debts, income replacement, education, final expenses) and subtract existing assets and cover to determine total life/TPD needs. |
| CAL-INS-006     | Education funding requirement                       | Insurance | extended | Estimate lump sum required to fund children’s education costs (school fees, tertiary expenses) over the desired timeframe. |
| CAL-INS-007     | Final expenses & emergency buffer requirement       | Insurance | extended | Estimate lump sum required for funeral, medical, estate, and an emergency buffer for the surviving family. |
| CAL-INS-008     | Trauma/critical illness lump sum need               | Insurance | extended | Estimate lump sum needed on trauma/critical illness to cover medical gaps, home modifications, temporary income support and debt reduction (partial). |
| CAL-INS-009     | Business/key person capital requirement (simple)    | Insurance | extended | Provide a simplified estimate of capital required for key person cover, such as revenue replacement or debt coverage for a small business. |

---

### 9.2 Income protection & short-term resilience

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-INS-004     | Income protection shortfall                         | Insurance | extended | Compare existing income protection benefits (monthly benefit, waiting period, benefit period) to required after-tax income and identify shortfall. |
| CAL-INS-010     | Target income protection benefit                    | Insurance | extended | Calculate the ideal monthly IP benefit based on a target replacement ratio (e.g. 70–80% of pre-disability income) and policy limits. |
| CAL-INS-011     | Waiting period buffer adequacy                      | Insurance | extended | Assess whether available cash/savings and other resources can cover expenses during the chosen waiting period. |
| CAL-INS-012     | Benefit period suitability (simple)                 | Insurance | extended | Provide a simplified indication of whether a 2-year vs to-age-65 benefit period is appropriate, based on occupation, age and resilience metrics. |
| CAL-INS-013     | Short-term sickness/accident buffer requirement     | Insurance | extended | Estimate the cash buffer required to cover a short-term illness/accident period not covered by IP or sick leave. |

---

### 9.3 Existing cover, gaps & overlaps

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-INS-014     | Existing cover roll-up (by type)                    | Insurance | extended | Aggregate existing cover amounts by type (life, TPD, trauma, IP) across super and non-super policies. |
| CAL-INS-015     | Cover sufficiency gap analysis                      | Insurance | extended | Compare total existing cover to calculated needs (from CAL-INS-001–003, 006–008) and quantify gaps or excesses for each cover type. |
| CAL-INS-016     | Super vs non-super cover split                      | Insurance | extended | Split existing cover between inside and outside super for structural analysis and tax considerations. |
| CAL-INS-017     | Policy overlap & duplication indicator              | Insurance | extended | Flag potential duplication or overlap in cover (e.g. multiple IP policies or overlapping trauma benefits). |

---

### 9.4 Premiums, affordability & sustainability

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-INS-005     | Premium affordability vs budget                     | Insurance | extended | Check total insurance premiums against surplus cashflow or affordability thresholds (monthly and annual). |
| CAL-INS-018     | Premiums as % of income                             | Insurance | extended | Calculate total insurance premiums as a percentage of gross and net household income. |
| CAL-INS-019     | Stepped vs level premium comparison (simple)        | Insurance | extended | Compare estimated long-term premium costs and cashflow impact of stepped versus level premium structures for a single policy. |
| CAL-INS-020     | Premium funding source impact (super vs personal)   | Insurance | extended | Compare outcomes of funding premiums inside super versus from personal cashflow, including impact on super balance projections. |
| CAL-INS-021     | Long-term premium sustainability indicator          | Insurance | extended | Provide an indicator of whether projected premiums remain affordable over time, considering expected income growth and life-stage changes. |

---

### 9.5 Risk exposure & residual risk

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-INS-022     | Household dependency risk score                     | Insurance | extended | Provide a simple score based on number and age of dependants, single vs dual income, and reliance on one key earner. |
| CAL-INS-023     | Self-insurance capacity                             | Insurance | extended | Estimate how much risk the household can self-insure using existing assets, buffers and future earning capacity. |
| CAL-INS-024     | Underinsurance risk indicator                       | Insurance | extended | Combine cover gaps, self-insurance capacity and dependency score into an underinsurance flag (e.g. Low / Medium / High). |
| CAL-INS-025     | Overinsurance / inefficiency indicator              | Insurance | extended | Highlight potential overinsurance where cover significantly exceeds calculated needs or premiums materially constrain other goals. |
| CAL-INS-026     | Single point-of-failure exposure (earner risk)      | Insurance | extended | Assess the financial impact if the primary earner cannot work, combining income, cover and buffers. |
| CAL-INS-027     | Event impact summaries (death, TPD, trauma, IP)     | Insurance | extended | Summarise projected financial position of the household under different events (death, TPD, trauma, income loss) with current versus recommended cover. |

**Notes (prioritisation for MVP):**  
- For early MVP, focus first on:  
  - Needs & capital: `CAL-INS-001`–`CAL-INS-003`, `CAL-INS-006`, `CAL-INS-007`.  
  - Income protection: `CAL-INS-004`, `CAL-INS-010`, `CAL-INS-011`.  
  - Affordability & gaps: `CAL-INS-005`, `CAL-INS-014`, `CAL-INS-015`, `CAL-INS-024`.  
- The remaining items can start as **simple heuristics** you refine once core protection logic and UI flows are stable.

---

## 10. Retirement readiness & Age Pension (Foundation & Social Security)

### 10.1 Retirement readiness & spending (`CAL-RPT-*` – retirement focus)

| ID              | Name                                                       | Domain     | MVP Tier | Description |
|-----------------|------------------------------------------------------------|------------|----------|-------------|
| CAL-RPT-201     | Net wealth at retirement age                              | Retirement | extended | Project total net wealth (inside and outside super) at a chosen retirement age. |
| CAL-RPT-202     | Sustainable withdrawal estimate (simple)                  | Retirement | extended | Estimate sustainable annual spending using simple rules (e.g. fixed percentage of assets, 4% rule). |
| CAL-RPT-203     | Retirement funding gap                                    | Retirement | extended | Compute shortfall or surplus between projected retirement spending needs and sustainable withdrawals from assets. |
| CAL-RPT-204     | Retirement spending projection timeline                   | Retirement | extended | Project year-by-year retirement spending (essential + discretionary) and compare with projected income streams. |
| CAL-RPT-205     | Income replacement ratio at retirement                    | Retirement | extended | Calculate ratio of projected retirement income to pre-retirement income (gross and net) to gauge lifestyle continuity. |
| CAL-RPT-206     | Target retirement wealth requirement                      | Retirement | extended | Compute lump sum required at retirement to fund target spending to a chosen age, given assumed returns and inflation. |
| CAL-RPT-207     | Contribution / savings gap to target retirement wealth    | Retirement | extended | Estimate additional annual savings or contributions needed to reach the target retirement wealth figure by a given age. |
| CAL-RPT-208     | Retirement age trade-off curve                            | Retirement | extended | Show how required retirement wealth and savings change if retirement age is brought forward or pushed back. |
| CAL-RPT-209     | Years until assets exhausted at chosen spending level     | Retirement | extended | Estimate how long assets will last given a specified spending pattern and investment return assumptions. |
| CAL-RPT-210     | Sequence-of-returns stress test (simple)                  | Retirement | extended | Compare baseline retirement outcomes with a simple “bad sequence early” scenario to illustrate sequencing risk. |
| CAL-RPT-211     | Longevity risk indicator                                  | Retirement | extended | Provide a simple indicator of probability of outliving assets to a target age (e.g. 90 or 95) based on assumed mortality tables. |
| CAL-RPT-212     | Retirement income sources breakdown                       | Retirement | extended | Break down projected retirement income by source (Age Pension, super pensions, investments, rental, work). |
| CAL-RPT-213     | Staged retirement / part-time work impact                 | Retirement | extended | Model the impact on net wealth and retirement income of working part-time or delaying full retirement. |
| CAL-RPT-214     | Annuity vs account-based pension comparison (simple)      | Retirement | extended | Provide a basic comparison of projected income stability and residual capital under an annuity versus an account-based pension. |
| CAL-RPT-215     | Retirement readiness index                                | Retirement | extended | Combine metrics (replacement ratio, buffer, reliance on Age Pension) into a simple readiness score (e.g. Low / Medium / High). |

---

### 10.2 Age Pension & means tests (`CAL-SSC-*` – Social Security)

| ID              | Name                                                       | Domain        | MVP Tier | Description |
|-----------------|------------------------------------------------------------|---------------|----------|-------------|
| CAL-SSC-001     | Basic Age Pension eligibility (very simple)                | Retirement    | extended | Provide a coarse estimate of Age Pension eligibility based on age, residency and simple assets/income tests. |
| CAL-SSC-002     | Age Pension assets test threshold & reduction (simple)     | Social Sec.   | extended | Estimate Age Pension payable under the assets test using simplified thresholds and taper rates. |
| CAL-SSC-003     | Age Pension income test calculation (simple)               | Social Sec.   | extended | Estimate Age Pension payable under the income test using deemed income on financial assets plus other assessable income. |
| CAL-SSC-004     | Age Pension payable (higher of tests)                      | Social Sec.   | extended | Combine assets and income test results to estimate total Age Pension entitlement (single or couple rate) under simplified rules. |
| CAL-SSC-005     | Full vs part pension classification                        | Social Sec.   | extended | Classify estimated entitlement as Full, Part or Nil Age Pension, with simple explanation of binding test. |
| CAL-SSC-006     | Deemed income on financial assets                          | Social Sec.   | extended | Calculate deemed income from financial assets using simple deeming thresholds and rates. |
| CAL-SSC-007     | Homeowner vs non-homeowner threshold adjustment            | Social Sec.   | extended | Adjust assets test thresholds for homeowner vs non-homeowner status in estimating Age Pension. |
| CAL-SSC-008     | Work Bonus impact estimate (simple)                        | Social Sec.   | extended | Provide a simplified estimate of the effect of the Work Bonus on assessable employment income for Age Pension recipients. |
| CAL-SSC-009     | Gifting impact on means tests (simple)                     | Social Sec.   | extended | Indicate potential effect of gifts above allowed thresholds on assets and income tests over a simplified time horizon. |
| CAL-SSC-010     | Pre-retirement Age Pension preview                         | Social Sec.   | extended | Project likely Age Pension eligibility and approximate payment at Age Pension age using projected assets and incomes. |
| CAL-SSC-011     | Age Pension + super drawdown interaction (simple)          | Social Sec.   | extended | Estimate effect of different super drawdown levels on means-tested Age Pension entitlement (simplified interaction). |
| CAL-SSC-012     | Rent assistance estimate (simple)                          | Social Sec.   | extended | Provide a rough estimate of rent assistance entitlement where client is renting and otherwise Age Pension-eligible. |

---

### 10.3 Combined retirement & pension view

| ID              | Name                                                       | Domain     | MVP Tier | Description |
|-----------------|------------------------------------------------------------|------------|----------|-------------|
| CAL-RPT-216     | Total retirement income with Age Pension                   | Retirement | extended | Combine projected private income (super/investments) with estimated Age Pension to show total retirement income. |
| CAL-RPT-217     | Age Pension reliance ratio                                 | Retirement | extended | Calculate the proportion of total retirement income expected to come from Age Pension versus private sources. |
| CAL-RPT-218     | Strategy impact on Age Pension (simple)                    | Retirement | extended | Illustrate how alternative strategies (e.g. extra super contributions, gifting, downsizing) may change Age Pension eligibility and total income. |
| CAL-RPT-219     | Retirement “floor and upside” income structure             | Retirement | extended | Decompose retirement plan into a secure income floor (Age Pension, annuities) and variable upside (super/investments), for communication and risk analysis. |

**Notes (prioritisation for MVP):**  
- For early MVP, focus on robust implementations of:  
  - Retirement readiness: `CAL-RPT-201`–`CAL-RPT-203`, `CAL-RPT-205`, `CAL-RPT-209`.  
  - Age Pension basics: `CAL-SSC-001`–`CAL-SSC-004`, `CAL-SSC-006`, `CAL-SSC-010`.  
  - Combined view: `CAL-RPT-216`, `CAL-RPT-217`.  
- Other items can initially be **simplified or heuristic** and refined as you build richer retirement and Social Security flows.

---

## 10. Retirement readiness & Age Pension (Foundation & Social Security)

### 10.1 Retirement readiness & spending (`CAL-RPT-*` – retirement focus)

| ID              | Name                                                       | Domain     | MVP Tier | Description |
|-----------------|------------------------------------------------------------|------------|----------|-------------|
| CAL-RPT-201     | Net wealth at retirement age                              | Retirement | extended | Project total net wealth (inside and outside super) at a chosen retirement age. |
| CAL-RPT-202     | Sustainable withdrawal estimate (simple)                  | Retirement | extended | Estimate sustainable annual spending using simple rules (e.g. fixed percentage of assets, 4% rule). |
| CAL-RPT-203     | Retirement funding gap                                    | Retirement | extended | Compute shortfall or surplus between projected retirement spending needs and sustainable withdrawals from assets. |
| CAL-RPT-204     | Retirement spending projection timeline                   | Retirement | extended | Project year-by-year retirement spending (essential + discretionary) and compare with projected income streams. |
| CAL-RPT-205     | Income replacement ratio at retirement                    | Retirement | extended | Calculate ratio of projected retirement income to pre-retirement income (gross and net) to gauge lifestyle continuity. |
| CAL-RPT-206     | Target retirement wealth requirement                      | Retirement | extended | Compute lump sum required at retirement to fund target spending to a chosen age, given assumed returns and inflation. |
| CAL-RPT-207     | Contribution / savings gap to target retirement wealth    | Retirement | extended | Estimate additional annual savings or contributions needed to reach the target retirement wealth figure by a given age. |
| CAL-RPT-208     | Retirement age trade-off curve                            | Retirement | extended | Show how required retirement wealth and savings change if retirement age is brought forward or pushed back. |
| CAL-RPT-209     | Years until assets exhausted at chosen spending level     | Retirement | extended | Estimate how long assets will last given a specified spending pattern and investment return assumptions. |
| CAL-RPT-210     | Sequence-of-returns stress test (simple)                  | Retirement | extended | Compare baseline retirement outcomes with a simple “bad sequence early” scenario to illustrate sequencing risk. |
| CAL-RPT-211     | Longevity risk indicator                                  | Retirement | extended | Provide a simple indicator of probability of outliving assets to a target age (e.g. 90 or 95) based on assumed mortality tables. |
| CAL-RPT-212     | Retirement income sources breakdown                       | Retirement | extended | Break down projected retirement income by source (Age Pension, super pensions, investments, rental, work). |
| CAL-RPT-213     | Staged retirement / part-time work impact                 | Retirement | extended | Model the impact on net wealth and retirement income of working part-time or delaying full retirement. |
| CAL-RPT-214     | Annuity vs account-based pension comparison (simple)      | Retirement | extended | Provide a basic comparison of projected income stability and residual capital under an annuity versus an account-based pension. |
| CAL-RPT-215     | Retirement readiness index                                | Retirement | extended | Combine metrics (replacement ratio, buffer, reliance on Age Pension) into a simple readiness score (e.g. Low / Medium / High). |

---

### 10.2 Age Pension & means tests (`CAL-SSC-*` – Social Security)

| ID              | Name                                                       | Domain        | MVP Tier | Description |
|-----------------|------------------------------------------------------------|---------------|----------|-------------|
| CAL-SSC-001     | Basic Age Pension eligibility (very simple)                | Retirement    | extended | Provide a coarse estimate of Age Pension eligibility based on age, residency and simple assets/income tests. |
| CAL-SSC-002     | Age Pension assets test threshold & reduction (simple)     | Social Sec.   | extended | Estimate Age Pension payable under the assets test using simplified thresholds and taper rates. |
| CAL-SSC-003     | Age Pension income test calculation (simple)               | Social Sec.   | extended | Estimate Age Pension payable under the income test using deemed income on financial assets plus other assessable income. |
| CAL-SSC-004     | Age Pension payable (higher of tests)                      | Social Sec.   | extended | Combine assets and income test results to estimate total Age Pension entitlement (single or couple rate) under simplified rules. |
| CAL-SSC-005     | Full vs part pension classification                        | Social Sec.   | extended | Classify estimated entitlement as Full, Part or Nil Age Pension, with simple explanation of binding test. |
| CAL-SSC-006     | Deemed income on financial assets                          | Social Sec.   | extended | Calculate deemed income from financial assets using simple deeming thresholds and rates. |
| CAL-SSC-007     | Homeowner vs non-homeowner threshold adjustment            | Social Sec.   | extended | Adjust assets test thresholds for homeowner vs non-homeowner status in estimating Age Pension. |
| CAL-SSC-008     | Work Bonus impact estimate (simple)                        | Social Sec.   | extended | Provide a simplified estimate of the effect of the Work Bonus on assessable employment income for Age Pension recipients. |
| CAL-SSC-009     | Gifting impact on means tests (simple)                     | Social Sec.   | extended | Indicate potential effect of gifts above allowed thresholds on assets and income tests over a simplified time horizon. |
| CAL-SSC-010     | Pre-retirement Age Pension preview                         | Social Sec.   | extended | Project likely Age Pension eligibility and approximate payment at Age Pension age using projected assets and incomes. |
| CAL-SSC-011     | Age Pension + super drawdown interaction (simple)          | Social Sec.   | extended | Estimate effect of different super drawdown levels on means-tested Age Pension entitlement (simplified interaction). |
| CAL-SSC-012     | Rent assistance estimate (simple)                          | Social Sec.   | extended | Provide a rough estimate of rent assistance entitlement where client is renting and otherwise Age Pension-eligible. |

---

### 10.3 Combined retirement & pension view

| ID              | Name                                                       | Domain     | MVP Tier | Description |
|-----------------|------------------------------------------------------------|------------|----------|-------------|
| CAL-RPT-216     | Total retirement income with Age Pension                   | Retirement | extended | Combine projected private income (super/investments) with estimated Age Pension to show total retirement income. |
| CAL-RPT-217     | Age Pension reliance ratio                                 | Retirement | extended | Calculate the proportion of total retirement income expected to come from Age Pension versus private sources. |
| CAL-RPT-218     | Strategy impact on Age Pension (simple)                    | Retirement | extended | Illustrate how alternative strategies (e.g. extra super contributions, gifting, downsizing) may change Age Pension eligibility and total income. |
| CAL-RPT-219     | Retirement “floor and upside” income structure             | Retirement | extended | Decompose retirement plan into a secure income floor (Age Pension, annuities) and variable upside (super/investments), for communication and risk analysis. |

**Notes (prioritisation for MVP):**  
- For early MVP, focus on robust implementations of:  
  - Retirement readiness: `CAL-RPT-201`–`CAL-RPT-203`, `CAL-RPT-205`, `CAL-RPT-209`.  
  - Age Pension basics: `CAL-SSC-001`–`CAL-SSC-004`, `CAL-SSC-006`, `CAL-SSC-010`.  
  - Combined view: `CAL-RPT-216`, `CAL-RPT-217`.  
- Other items can initially be **simplified or heuristic** and refined as you build richer retirement and Social Security flows.

---

## 11. Plan-level, scenario & reporting calculations (Reporting – `CAL-RPT-*`)

### 11.1 Core scenario metrics & timelines

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-RPT-001     | Net wealth timeline                                 | Plan      | core     | Compute year-by-year net wealth for a scenario (assets minus liabilities) at defined time steps. |
| CAL-RPT-002     | Scenario comparison (A vs B)                        | Plan      | core     | Compare key metrics (net wealth, cashflow, tax, super balance) between two scenarios at key dates. |
| CAL-RPT-003     | Financial independence age (simple)                 | Plan      | extended | Estimate the earliest age at which projected passive/portfolio income meets or exceeds target spending. |
| CAL-RPT-004     | Major goal funding status                           | Plan      | extended | Check whether a specific goal (e.g. buy house, retire at X) is fully funded, partially funded, or unfunded under the scenario. |
| CAL-RPT-005     | Risk & resilience indicators                        | Plan      | extended | Compute simple metrics like debt ratios, buffer months, diversification indicators and protection gaps at scenario milestones. |
| CAL-RPT-006     | Reporting & reconciliation checks                   | Plan      | core     | Perform internal consistency checks (cash conservation, double-count detection, tax reconciliation, rounding tolerance). |

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-RPT-007     | Asset allocation over time                          | Plan      | extended | Summarise how total balance is split by asset class (cash, fixed interest, property, shares, etc.) at key points along the timeline. |
| CAL-RPT-008     | Debt profile over time                              | Plan      | extended | Track total debt, debt-to-income ratios, and loan mix (home vs investment vs consumer) across the projection horizon. |
| CAL-RPT-009     | Tax paid over time                                  | Plan      | extended | Summarise annual and cumulative tax paid (income tax, CGT, super tax) to support strategy comparisons. |
| CAL-RPT-010     | Cashflow timeline                                   | Plan      | extended | Provide year-by-year (or period-by-period) net cashflow, highlighting surplus/deficit periods and large one-off items. |
| CAL-RPT-011     | Scenario KPI snapshot at key ages                   | Plan      | extended | Generate a table of key metrics (net wealth, debt ratio, super balance, Age Pension estimate) at user-defined ages. |
| CAL-RPT-012     | Best / base / worst case scenario summary           | Plan      | extended | Summarise outcomes across three scenarios (e.g. optimistic, base, pessimistic returns) for quick comparison. |

---

### 11.2 Goals, strategies & “what if” scenario deltas

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-RPT-013     | Multi-goal funding matrix                           | Plan      | extended | Summarise funding status (in %, shortfall $) for multiple goals (home, kids, retirement, travel) under a single scenario. |
| CAL-RPT-014     | Strategy delta – implement vs do nothing            | Plan      | extended | Compare key metrics (net wealth, retirement income, debt) between a recommended strategy scenario and a “do nothing” baseline. |
| CAL-RPT-015     | Strategy delta – strategy A vs strategy B           | Plan      | extended | Compare multiple advice strategies (e.g. aggressive debt reduction vs aggressive investing) across shared KPIs. |
| CAL-RPT-016     | Contribution strategy impact summary                | Plan      | extended | Isolate the impact of changed contribution behaviour (to super, investing, mortgage extra repayments) on retirement and net wealth outcomes. |
| CAL-RPT-017     | Leverage strategy impact summary                    | Plan      | extended | Quantify impact of taking on, increasing or reducing leverage (e.g. investment loan, margin loan) on wealth, risk and cashflow. |
| CAL-RPT-018     | Sensitivity to investment return                    | Plan      | extended | Show how net wealth and retirement outcomes change under different average return assumptions (e.g. ±1–2% p.a.). |
| CAL-RPT-019     | Sensitivity to savings rate                         | Plan      | extended | Show how outcomes change if the client saves more or less than baseline (e.g. ±10–20% of current savings rate). |
| CAL-RPT-020     | Sensitivity to retirement age                       | Plan      | extended | Illustrate changes in retirement readiness, net wealth and Age Pension reliance for alternative retirement ages. |

---

### 11.3 Risk, resilience & dependency views

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-RPT-021     | Household balance sheet strength index              | Plan      | extended | Combine leverage, liquidity, and diversification metrics into an index of balance sheet strength at key dates. |
| CAL-RPT-022     | Income dependency & concentration analysis          | Plan      | extended | Assess how dependent the plan is on one income source (e.g. primary earner) and show impact of losing/falling income. |
| CAL-RPT-023     | Shock resilience test – loss of primary income      | Plan      | extended | Model the plan’s ability to cope with the primary earner’s income ceasing for a defined period (e.g. 6–12 months) without breaching buffer thresholds. |
| CAL-RPT-024     | Shock resilience test – market downturn             | Plan      | extended | Model the effect of a one-off market drop (e.g. –20%) at various times on net wealth and retirement outcomes. |
| CAL-RPT-025     | Debt stress scenario (rate rise + income dip)       | Plan      | extended | Combine interest rate rise and modest income reduction in a stress test and measure impact on cashflow and debt ratios. |
| CAL-RPT-026     | Protection dependency indicator                     | Plan      | extended | Show how reliant the plan is on existing or recommended insurance cover to meet goals under adverse events. |

---

### 11.4 Reporting, auditability & internal QA

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-RPT-027     | Input change log & version delta summary            | Plan      | extended | Summarise differences in key inputs between two scenarios or versions (e.g. incomes, contributions, assumptions). |
| CAL-RPT-028     | Calculation provenance map (summary-level)          | Plan      | extended | Provide a summary linking key reported outputs back to calculation modules (IDs) and core assumptions for auditability. |
| CAL-RPT-029     | Cashflow and balance sheet reconciliation           | Plan      | core     | Check that changes in balances across periods reconcile with net cashflows, earnings and contributions/withdrawals. |
| CAL-RPT-030     | Tax & contribution reconciliation                    | Plan      | core     | Verify that tax, contributions and withdrawals used in scenario outputs reconcile with underlying tax and super modules. |
| CAL-RPT-031     | Scenario sanity checks (heuristic)                  | Plan      | core     | Run heuristic checks to flag obviously unrealistic scenario inputs or outputs (e.g. negative balances, extreme ratios). |
| CAL-RPT-032     | Client-facing summary metrics pack                  | Plan      | extended | Assemble a standardised set of key figures (net wealth, retirement income, buffers, Age Pension reliance) for presentation/export. |
| CAL-RPT-033     | Adviser-facing diagnostic metrics pack              | Plan      | extended | Provide a more detailed metrics pack for advisers, including reconciliation flags, sensitivity results and rule triggers. |

**Notes (prioritisation for MVP):**  
- For early MVP, the **must-have reporting layer** is:  
  - `CAL-RPT-001`, `CAL-RPT-002`, `CAL-RPT-003`, `CAL-RPT-004`, `CAL-RPT-006`, `CAL-RPT-011`, `CAL-RPT-029`, `CAL-RPT-030`.  
- The other items can start as **simplified summaries** or heuristic checks that become richer as other modules (tax, super, portfolio, social security, insurance) mature.


---

## 11. Entities (`CAL-ENT-*`)

### Entities – Companies (`CAL-ENT-*`)

| ID              | Name                                                | Domain        | MVP Tier | Description |
|-----------------|-----------------------------------------------------|---------------|----------|-------------|
| CAL-ENT-101     | Company taxable income & tax liability              | Tax / Entity  | core     | Aggregate assessable income and deductions for a company and compute tax using the Base Rate Entity (25%) or Standard (30%) rate. |
| CAL-ENT-102     | Base Rate Entity eligibility check                  | Tax / Entity  | core     | Determine eligibility for the 25% base rate entity tax by testing turnover and passive income proportion (simplified tests). |
| CAL-ENT-103     | Company franking account movement & balance         | Tax / Entity  | extended | Track notional franking account balance: add credits from company tax paid, deduct debits from franked dividends, and expose franking capacity. |
| CAL-ENT-104     | Maximum franked distribution capacity (simple)      | Tax / Entity  | extended | Estimate the maximum dividends that can be fully franked given the franking account balance and current-year company tax. |
| CAL-ENT-105     | Retained earnings vs dividend split                 | Tax / Entity  | extended | Split after-tax profit between retained earnings and distributions under simple dividend policy assumptions. |
| CAL-ENT-106     | Div 7A minimum yearly repayment                     | Tax / Entity  | extended | Calculate minimum yearly repayment for a complying Div 7A loan based on principal, benchmark rate and term (simplified). |
| CAL-ENT-107     | Div 7A deemed dividend estimate (loans & UPEs)      | Tax / Entity  | extended | Estimate potential deemed dividends arising from non-complying shareholder loans and unpaid present entitlements from trusts (simple model). |

---

### Entities – Trusts (`CAL-ENT-*` + CGT)

| ID              | Name                                                | Domain        | MVP Tier | Description |
|-----------------|-----------------------------------------------------|---------------|----------|-------------|
| CAL-ENT-111     | Trust net income (simplified)                       | Tax / Entity  | extended | Calculate the trust’s taxable net income (for tax purposes) split into ordinary income, capital gains and franked components. |
| CAL-ENT-112     | Beneficiary distribution allocation                 | Tax / Entity  | extended | Allocate trust net income components to beneficiaries according to unit holdings or discretionary percentages. |
| CAL-ENT-113     | Streaming by class (CGT / franked income)           | Tax / Entity  | extended | Model streaming of CGT and franked income components to specific beneficiaries under a simplified streaming rule set. |
| CAL-ENT-114     | Trustee-assessed tax on undistributed income        | Tax / Entity  | extended | Estimate tax on any undistributed trust income at trustee level using top marginal tax assumptions (simplified Sec 99/99A style). |
| CAL-ENT-115     | Trust distribution to individual – tax impact       | Tax / Entity  | extended | Calculate an individual beneficiary’s share of trust net income and resulting personal tax at marginal rates. |
| CAL-CGT-103     | CGT: trust distribution CGT components              | CGT / Entity  | extended | Process discounted, indexed and other CGT components received via trust distributions and feed them into individual/entity CGT calculations. |

---

### Entities – Partnerships (`CAL-ENT-*`)

| ID              | Name                                                | Domain        | MVP Tier | Description |
|-----------------|-----------------------------------------------------|---------------|----------|-------------|
| CAL-ENT-121     | Partnership net income (simplified)                 | Tax / Entity  | extended | Aggregate partnership business income and deductions to derive partnership net income for tax purposes. |
| CAL-ENT-122     | Partner share of income, losses & credits           | Tax / Entity  | extended | Allocate partnership net income/loss and relevant credits to partners according to their profit-sharing percentages. |
| CAL-ENT-123     | Partner capital account / basis tracking (simple)   | Tax / Entity  | extended | Track each partner’s capital contributions and retained share of profits/losses in a simplified capital account for CGT context. |

---

### Entities – PSI, GST & Small Business (`CAL-ENT-*`)

| ID              | Name                                                | Domain        | MVP Tier | Description |
|-----------------|-----------------------------------------------------|---------------|----------|-------------|
| CAL-ENT-131     | PSI classification indicator (simplified tests)     | Tax / Entity  | extended | Provide a simple Personal Services Income vs business income flag using high-level PSI tests (results, tools, employees, multiple clients). |
| CAL-ENT-132     | PSI deduction limitation effect (simple)            | Tax / Entity  | extended | Estimate impact of PSI rules on allowable deductions and resulting taxable income for PSI-affected individuals/entities. |
| CAL-ENT-141     | GST collected vs input tax credits (simple BAS)     | Tax / Entity  | extended | Estimate net GST payable or refundable from taxable supplies and input-taxed credits, with a cash/accrual basis toggle. |
| CAL-ENT-142     | GST cash vs accrual impact comparison               | Tax / Entity  | extended | Provide a simple comparison of GST timing and cashflow impact under cash vs accrual reporting for a small business. |
| CAL-ENT-151     | Small business income tax offset (individual)       | Tax / Entity  | extended | Estimate the small business tax offset for eligible individuals based on their share of small business income (simplified). |
| CAL-ENT-152     | Small business CGT concessions eligibility flag     | Tax / Entity  | extended | Provide a coarse eligibility flag for small business CGT concessions using turnover and basic active asset tests (no detailed CGT calculation). |

---

### CGT – Entity-specific & advanced (`CAL-CGT-*`)

| ID              | Name                                                | Domain        | MVP Tier | Description |
|-----------------|-----------------------------------------------------|---------------|----------|-------------|
| CAL-CGT-101     | CGT: Corporate & SMSF discount rules                | CGT / Entity  | core     | Apply appropriate CGT discount: 0% for companies, 33⅓% for complying super funds, and ensure correct interaction with individual/trust discount rules. |
| CAL-CGT-102     | CGT: Indexation method for pre-21 Sep 1999 assets   | CGT           | extended | Calculate inflation-adjusted cost base under the indexation method for assets acquired before 21 September 1999. |
| CAL-CGT-104     | CGT: FIFO vs specific parcel selection              | CGT           | extended | Model CGT liability under First-In-First-Out (FIFO) or specific parcel identification methods for disposals (complements portfolio-level tax-lot logic). |

---

### Super – Entity / SMSF level (`CAL-SUP-*` – entity focus)

| ID              | Name                                                | Domain        | MVP Tier | Description |
|-----------------|-----------------------------------------------------|---------------|----------|-------------|
| CAL-SUP-101     | Employer SG compliance check                        | Super / Entity | core    | Verify that an employer (company/trust) has met quarterly SG obligations using the correct OTE base and statutory rate (simplified). |
| CAL-SUP-102     | SMSF earnings tax & ECPI application                | Super / Entity | extended | Calculate tax payable on SMSF investment earnings, accounting for Exempt Current Pension Income (ECPI) under a simplified approach. |
| CAL-SUP-103     | SMSF Non-Arm’s Length Income (NALI) tax estimate    | Super / Entity | extended | Identify potential non-arm’s length income/expenditure and apply the maximum tax rate to affected income (simple NALI model). |

---

### Entity-level reporting (`CAL-RPT-*` – entity focus)

| ID              | Name                                                | Domain          | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------------|----------|-------------|
| CAL-RPT-101     | P&L statement (entity, simple)                      | Reporting / Entity | extended | Compute a simple Profit & Loss statement by subtracting cost of goods/services and operating expenses from revenue. |
| CAL-RPT-102     | Balance sheet equity (entity, simple)               | Reporting / Entity | extended | Calculate entity equity as Total Assets minus Total Liabilities at a point in time. |

---

### Ownership & Fractional Interests (Foundation / Property / Portfolio)

| ID              | Name                                                | Domain      | MVP Tier | Description |
|-----------------|-----------------------------------------------------|------------|----------|-------------|
| CAL-FND-301     | Ownership share apportionment (cross-asset)         | Foundation | core     | Apportion income, expenses, gains and losses across owners based on specified ownership percentages or units, for any asset type. |
| CAL-PRP-301     | Property joint ownership split                      | Property   | extended | Apply ownership/apportionment logic specifically to jointly held properties (spouses or other co-owners), including rent, expenses and interest. |
| CAL-PFL-301     | Portfolio joint account apportionment               | Investment | extended | Split investment income, franking credits and realised gains from joint investment accounts between account holders. |

---

### Look-through & Consolidation (Entities & Plan-level)

| ID              | Name                                                | Domain    | MVP Tier | Description |
|-----------------|-----------------------------------------------------|-----------|----------|-------------|
| CAL-ENT-161     | Look-through economic ownership (simple)            | Entities  | extended | Calculate an individual’s effective ownership of underlying assets/income through companies, trusts or SMSFs using simple percentage chains. |
| CAL-RPT-241     | Consolidated net wealth & income across entities    | Plan      | extended | Roll up assets, liabilities and income from personally held and controlled entities into a consolidated view for planning and reporting. |

---

### Other advanced / foundation calcs

| ID              | Name                                                | Domain      | MVP Tier | Description |
|-----------------|-----------------------------------------------------|------------|----------|-------------|
| CAL-FND-101     | Present value / NPV of cashflows                    | Foundation | core     | Calculate the present value or Net Present Value (NPV) of a series of future cashflows using a given discount rate. |
| CAL-DBT-101     | Risk-Weighted Assets (RWA) impact (conceptual)      | Debt / Entity | extended | Calculate risk-weighted assets for a financial institution–style balance sheet to support conceptual regulatory/comparison scenarios (not core retail advice). |


---

## 13. MVP “four golden” calculations (summary)

For the MVP, the **highest priority** calculations (cross-referencing above IDs) are:

- **PAYG + offsets & net tax**  
  - `CAL-PIT-001` – PAYG income tax  
  - `CAL-PIT-002` – Medicare levy  
  - `CAL-PIT-004` – Tax offsets aggregation  
  - `CAL-PIT-005` – Net tax payable / refund  

- **CGT discount event (simple asset)**  
  - `CAL-CGT-001` – Capital gain on asset disposal  
  - `CAL-CGT-002` – CGT discount (individuals)  

- **Super contributions + Div 293**  
  - `CAL-SUP-002` – Total concessional contributions  
  - `CAL-SUP-003` – Concessional cap utilisation  
  - `CAL-SUP-007` – Contributions tax inside super  
  - `CAL-SUP-008` – Division 293 additional tax  
  - `CAL-SUP-009` – Net contribution added to balance  

- **Negative gearing mortgage interest**  
  - `CAL-PFL-104` – Negative gearing tax benefit  
  - plus links to property cashflow: `CAL-PRP-005` / `CAL-PRP-006`.

These should be implemented and fully validated first, with golden examples, before expanding into the rest of the MVP calculations.

---
