# Feature Specification: Compute Engine

**Feature Branch**: `002-compute-engine`  
**Created**: 2025-01-27  
**Status**: Draft  
**Input**: Compute Engine module - performs deterministic financial computations and projections. Executes rulesets, scenarios, and simulations while maintaining provenance and reproducibility using PostgreSQL-only storage.

**Purpose**: This module is the core calculation engine of the financial advice system. It performs deterministic financial computations and projections by executing rulesets, scenarios, and simulations. It maintains full provenance and reproducibility, ensuring that all calculations are traceable, auditable, and can be reproduced exactly using the same inputs, ruleset, and date parameters.

**Reference**: This module implements requirements from the master specification (`001-master-spec/spec.md`), specifically FR-002, FR-003, FR-004A, FR-005 through FR-012, and FR-022 through FR-023.

## Architectural Boundaries

**Compute Engine** is the single source of truth for all deterministic financial logic. Per Constitution Principle XII:

- **MUST own**: Tax formulas, caps, thresholds, eligibility tests, projections, all numeric calculations and arithmetic operations, rule execution and deterministic computation, structured Facts with provenance.

- **MUST NOT**: Perform judgement, advice, or free-text reasoning; define its own tax formulas, caps, or thresholds (these come from Rules); override deterministic outputs based on business logic; store or serve knowledge objects (References, Rules, Assumptions, Advice Guidance, Strategies).

All numeric calculations MUST be performed by Compute Engine. Other modules (Advice Engine, LLM Orchestrator) MUST NOT perform calculations or override Compute Engine outputs.

---

## Clarifications

This section addresses ambiguous areas in the specification to eliminate implementation uncertainty.

### Session 2025-01-27

- Q: What is the maximum batch size for batch calculation requests, and how should the system handle requests that exceed this limit? → A: 100 calculations per batch, return error suggesting pagination for larger requests

- Q: What should happen when a calculation request references a rule identifier that doesn't exist in the specified ruleset? → A: Return 422 Unprocessable Entity with specific rule identifier and remediation guidance (suggest available rulesets or rule IDs)

- Q: What timeout should apply to individual calculation operations, and how should the system handle calculations that exceed this timeout? → A: 30 seconds per calculation, return 504 Gateway Timeout with structured error including calculation progress and remediation guidance

- Q: How should the system handle calculation requests that require assumptions (e.g., inflation rate, discount rate) that aren't available in the specified assumption snapshot? → A: Return 422 Unprocessable Entity with specific missing assumption identifiers and remediation guidance (suggest available assumption snapshots or provide assumption values)

- Q: What should happen when multiple calculation runs attempt to update the same scenario concurrently, and how should conflicts be detected and resolved? → A: Optimistic concurrency control with version numbers, return 409 Conflict on version mismatch with remediation guidance

---

## User Scenarios & Testing

### User Story 1 - Execute Deterministic Financial Calculations (Priority: P1)

**User Story**: An adviser, consumer, or partner needs to execute financial calculations (e.g., tax calculations, superannuation contributions, retirement projections) and receive deterministic, reproducible results that can be verified and audited.

**Why this priority**: This is the core function of the Compute Engine. Without deterministic calculations, the system cannot provide reliable financial advice. All other capabilities depend on this foundational requirement.

**Independent Test**: A user can submit a calculation request with client data, scenario parameters, `ruleset_id`, and `as_of` date, and receive computed Facts with full provenance. Repeating the same request with identical parameters produces identical results.

**Acceptance Scenarios**:

1. **Given** a user submits a calculation request with client data, scenario parameters, `ruleset_id`, and `as_of` date, **When** the system processes it, **Then** it executes applicable rules from the specified ruleset, produces Facts with full provenance, and returns results within acceptable time limits.

2. **Given** a user submits the same calculation request twice with identical parameters, **When** both requests are processed, **Then** both produce identical Fact values, units, rounding, and provenance chains, demonstrating deterministic reproducibility.

3. **Given** a user submits a calculation request with an `as_of` date in the past, **When** the system processes it, **Then** it uses the ruleset version and rules applicable on that date, enabling time-travel queries for historical reconstruction.

4. **Given** a calculation requires multiple rules to be applied in sequence, **When** the system executes them, **Then** it respects rule precedence (Act > Regulation > Ruling > Guidance > Assumption) and effective date windows, applying the correct rules in the correct order.

---

### User Story 2 - Scenario Modelling and Comparisons (Priority: P1)

**User Story**: An adviser or consumer needs to model different financial scenarios (e.g., "What if I retire at 58 vs 65?" or "Compare debt-recycling vs offset-strategy") and compare outcomes side-by-side to make informed decisions.

**Why this priority**: Scenario modelling is essential for financial planning. Users need to explore "what-if" scenarios and compare alternatives. This capability enables informed decision-making and is a core value proposition.

**Independent Test**: A user can create multiple scenarios (A, B, C) with different parameters, execute calculations for each scenario, and retrieve comparative results showing how outcomes differ across scenarios.

**Acceptance Scenarios**:

1. **Given** a user creates multiple scenarios with different parameters (e.g., retirement age, contribution amounts), **When** they execute calculations for each scenario, **Then** the system produces separate Facts for each scenario, tagged with unique scenario IDs, enabling side-by-side comparison.

2. **Given** a user requests scenario comparison, **When** they query with scenario parameters, **Then** the system returns Facts for all requested scenarios with consistent structure, enabling comparative analysis.

3. **Given** scenarios are created as alternative futures, **When** calculations are executed, **Then** scenario Facts never overwrite base reality Facts, maintaining clear separation between actual and hypothetical outcomes.

4. **Given** a user wants to perform sensitivity analysis, **When** they vary a single parameter across multiple scenarios, **Then** the system executes calculations efficiently, showing how outcomes change with parameter variations.

---

### User Story 3 - Provenance and Explainability (Priority: P1)

**User Story**: An adviser, consumer, or regulator needs to understand how a calculation result was derived, tracing it back through rules, references, and assumptions to verify accuracy and compliance.

**Why this priority**: Provenance and explainability are non-negotiable requirements for financial advice. Users must be able to audit calculations, and regulators must be able to verify compliance. This capability builds trust and enables regulatory compliance.

**Independent Test**: A user can retrieve any computed Fact and request its explanation, receiving a human-readable trace showing Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions with versions and dates.

**Acceptance Scenarios**:

1. **Given** a Fact has been computed, **When** a user requests explanation, **Then** the system builds a provenance chain linking the Fact to the rules that produced it, the references those rules cite, and the assumptions used.

2. **Given** a Fact was computed using multiple rules, **When** the explanation is generated, **Then** it shows all applicable rules, their precedence relationships, and how they combined to produce the result.

3. **Given** a Fact references a Client Outcome Strategy, **When** the explanation is generated, **Then** it shows how the strategy combines rules, assumptions, and advice guidance, providing context for why the strategy was applied.

4. **Given** a user needs to export provenance for compliance, **When** they request explanation, **Then** the system provides a format suitable for inclusion in compliance packs, with all references, versions, and dates clearly documented.

---

### User Story 4 - Batch Processing and Performance (Priority: P2)

**User Story**: An adviser or partner needs to execute multiple calculations efficiently, either as part of a single request (batch) or as multiple sequential requests, without performance degradation.

**Why this priority**: Advisers often need to model multiple scenarios or process multiple clients. Performance is critical for user experience. Batch processing enables efficiency gains and reduces API call overhead.

**Independent Test**: A user can submit a batch of calculation requests and receive results for all calculations within acceptable time limits, with performance scaling linearly with batch size up to reasonable limits.

**Acceptance Scenarios**:

1. **Given** a user submits a batch of calculation requests, **When** the system processes them, **Then** it executes calculations efficiently, potentially in parallel where safe, and returns results for all requests with consistent structure.

2. **Given** multiple users submit calculation requests concurrently, **When** the system processes them, **Then** it maintains performance and accuracy, ensuring tenant isolation and preventing one user's requests from affecting another's results.

3. **Given** a calculation request requires complex rule resolution or large data processing, **When** the system processes it, **Then** it completes within acceptable time limits (as defined in success criteria) while maintaining accuracy and provenance.

4. **Given** a user queries historical Facts with scenario and date parameters, **When** the system retrieves them, **Then** it returns results efficiently, supporting time-travel queries without performance degradation.

---

### Edge Cases

- What happens when a calculation request references a ruleset that doesn't exist? The system MUST return an error indicating the ruleset is not found, with guidance on available rulesets.

- How does the system handle calculation requests with missing required parameters? The system MUST validate inputs before execution, returning clear error messages indicating which parameters are missing or invalid.

- What happens when multiple rules apply but conflict at the same precedence level? The system MUST detect conflicts, log warnings, and either apply conflict resolution logic (if defined) or return an error requiring manual resolution.

- How does the system handle calculations that produce invalid results (e.g., negative values where not allowed)? The system MUST validate calculation results against business rules, flagging invalid results and providing explanations.

- What happens when a calculation requires data that isn't available? The system MUST either retrieve missing data or return an error indicating the required data is not available.

- How does the system handle very large calculation requests (e.g., projecting 50 years into the future)? The system MUST process large requests efficiently, potentially using pagination or streaming for results, while maintaining accuracy and provenance.

- What happens when a Fact's provenance chain references a Reference that has been deleted or superseded? The system MUST maintain historical links, preserving the original Reference version that was used, even if it's been superseded.

- What happens when a calculation uses binary floating-point arithmetic and precision is lost? The system MUST use fixed-point Decimal or integer cents, preventing precision loss through type enforcement.

- What happens when units are mismatched (e.g., dollars + percentages)? The system MUST detect unit mismatches during validation and return clear error messages indicating the unit conflict.

- What happens when rounding drift accumulates over long horizons? The system MUST detect rounding drift exceeding tolerance thresholds and flag discrepancies for review.

- What happens when a database query times out? The system MUST implement timeouts and return appropriate error responses, preventing indefinite blocking.

- What happens when external services are unavailable? The system MUST implement circuit breakers to fail fast and prevent cascading failures.

- What happens when reconciliation checks fail (e.g., components don't sum to totals)? The system MUST detect reconciliation failures, log warnings, and return structured errors indicating which reconciliation failed and the discrepancy amount.

- What happens when multiple calculation runs attempt to update the same scenario concurrently? The system MUST prevent race conditions using optimistic concurrency control or pessimistic locking, returning appropriate conflict errors when concurrent updates are detected.

---

## Requirements

### Functional Requirements

#### Calculation Execution

- **FR-001**: System MUST execute financial calculations deterministically: same inputs + same `ruleset_id` + same `as_of` date MUST produce identical outputs.

- **FR-002**: System MUST pin every calculation operation to explicit `ruleset_id`, `as_of` date, and `scenario_id` parameters.

- **FR-003**: System MUST execute calculations using rules from the active ruleset snapshot.

- **FR-004**: System MUST resolve rule applicability using effective date windows, precedence hierarchy (Act > Regulation > Ruling > Guidance > Assumption), and temporal logic based on `as_of` date.

- **FR-005**: System MUST apply rules in the correct order based on dependencies, precedence, and effective dates, ensuring calculations reflect the intended regulatory logic.

- **FR-006**: System MUST validate calculation inputs before execution, checking required parameters, data types, and business rule constraints. When a calculation request references a rule identifier that doesn't exist in the specified ruleset, the system MUST return 422 Unprocessable Entity error with the specific rule identifier and remediation guidance suggesting available rulesets or rule IDs. When a calculation request requires assumptions that aren't available in the specified assumption snapshot, the system MUST return 422 Unprocessable Entity error with specific missing assumption identifiers and remediation guidance (suggesting available assumption snapshots or providing assumption values).

- **FR-007**: System MUST execute calculation expressions or functions defined in rules, applying mathematical operations, tax computations, and financial formulas accurately.

- **FR-008**: System MUST apply explicit numeric tolerances and rounding standards defined in rule specifications, ensuring consistent results across all calculations.

- **FR-008A**: System MUST use fixed-point Decimal or integer cents for all monetary values; binary floating-point arithmetic is FORBIDDEN for financial calculations to prevent precision loss.

- **FR-008B**: System MUST enforce explicit units and dimensional checks for all calculations (%, basis points, dollars, years, etc.) with validation to prevent unit mismatches (e.g., dollars + percentages = error).

- **FR-008C**: System MUST specify rounding policy per field in rule definitions: ATO rounding rules, bankers rounding (round half to even) vs away-from-zero, and when rounding occurs (at each calculation step vs at end of calculation).

- **FR-008D**: System MUST guard against precision loss for long horizons (e.g., 50-year projections) and large totals by using appropriate precision settings and periodic precision checks.

#### Fact Storage and Provenance

- **FR-009**: System MUST store all computed results as Facts with full provenance: rule versions, inputs hash, scenario id, units, rounding, and timestamp.

- **FR-010**: System MUST treat Facts as immutable: once computed and stored, Facts cannot be modified; new calculations create new Facts.

- **FR-011**: System MUST link Facts to Rules via provenance relationships, enabling traversal from Fact → Rule → Reference → Assumptions.

- **FR-012**: System MUST store Facts with scenario tags, enabling scenario-based queries and comparisons without overwriting base reality Facts.

- **FR-013**: System MUST generate unique Fact identifiers that can be used to retrieve explanations and trace provenance chains.

- **FR-014**: System MUST store Facts with version information, linking to the specific ruleset version and rule versions used in calculation.

#### Scenario Management

- **FR-015**: System MUST support creation and management of scenarios as tagged alternative futures that never overwrite base reality.

- **FR-016**: System MUST execute calculations for multiple scenarios independently, producing separate Facts for each scenario.

- **FR-017**: System MUST support scenario comparison queries, enabling users to retrieve Facts for multiple scenarios with consistent structure.

- **FR-018**: System MUST maintain scenario metadata (name, description, parameters) to enable scenario identification and management.

#### Provenance and Explainability

- **FR-019**: System MUST provide explanation capability that builds provenance chains.

- **FR-020**: System MUST generate provenance chains in the format: **Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions** with versions and dates.

- **FR-020A**: System MUST include per-fact provenance details: inputs hash, rules applied (with rule versions), references cited (with pinpoint identifiers), assumptions snapshot (with assumption versions), and rounding steps applied (before/after values).

- **FR-020B**: System MUST provide stable anchors/IDs for citations enabling reproducible reference links even after reference updates (e.g., use reference version IDs, not just reference IDs).

- **FR-020C**: System MUST export evidence packs in both JSON (machine-readable) and PDF (human-readable) formats with version information, timestamps, and complete provenance chains.

- **FR-020D**: System MUST support tracing all numbers in a forecast back to their sources within 50ms, including batch explain operations for multiple Facts within a single forecast scenario, even at scale (10,000 concurrent users, 1 million Facts).

- **FR-020E**: System MUST optimize explain endpoint performance at scale using pre-computed materialized views, read replicas for query distribution, connection pooling, and intelligent caching strategies to maintain sub-50ms response times.

- **FR-021**: System MUST retrieve Reference details when building provenance chains, ensuring complete traceability.

- **FR-022**: System MUST generate human-readable explanations suitable for inclusion in compliance packs, with clear formatting and citation information.

- **FR-023**: System MUST support time-travel queries, using `as_of` dates to reconstruct historical calculations using the ruleset versions applicable at that time.

#### Access and Integration

- **FR-024**: System MUST provide calculation capability accepting client data, scenario parameters, `ruleset_id`, `as_of` date, and returning computed Facts with provenance.

- **FR-025**: System MUST provide batch calculation capability accepting multiple calculation requests and returning results for all requests. Batch requests MUST be limited to a maximum of 100 calculations per batch. Requests exceeding this limit MUST return an error (422 Unprocessable Entity) with remediation guidance suggesting pagination or splitting the request into multiple smaller batches.

- **FR-026**: System MUST provide Facts retrieval capability supporting queries by scenario, date, and other filters.

- **FR-027**: System MUST provide explanation capability returning provenance chains for specified Facts.

- **FR-027D**: System MUST provide rulesets listing capability returning all published rulesets with metadata (identifiers, publication dates, effective date ranges, status, rule counts) for MVP. Future enhancements may include advanced filtering and search capabilities.

- **FR-027E**: System MUST provide rules query capability returning rule metadata (identifiers, effective dates, precedence, references, applicability conditions) for rules active at a specified date for MVP. Future enhancements may include advanced filtering by precedence, type, or applicability conditions.

- **FR-027A**: System MUST provide pagination for large fact sets with configurable page sizes.

- **FR-027B**: System MUST implement clear error taxonomy: 4xx for validation errors (missing parameters, invalid types), 409 for conflicts (concurrent scenario updates), 5xx for compute failures (rule execution errors), with structured error responses including remediation guidance.

- **FR-027C**: System MUST support partial-result semantics for batch operations, returning successful results alongside errors for failed items with clear error attribution.

- **FR-028**: System MUST enforce access control with tenant isolation and rate limits as specified in the master specification (see CL-031 and FR-030 for security guarantee that User A can NEVER see User B's data under ANY circumstances).

- **FR-028A**: System MUST include automated security tests that verify cross-tenant data access is impossible for all Compute Engine endpoints. Tests MUST simulate bugs, misconfigured queries, malicious input, missing tenant context, and other failure scenarios to ensure User A cannot access User B's calculation results, scenarios, or facts under any conditions (see FR-030A in master specification).

- **FR-029**: System MUST support idempotency keys for calculation requests, enabling safe retries and preventing duplicate calculations.

#### Rules Intelligence

- **FR-030**: System MUST provide rulesets listing capability returning all published rulesets with metadata: ruleset identifiers (format: `ruleset-YYYYMMDD`), publication dates, effective date ranges, status (Active, Superseded), and rule counts. **MVP**: Basic rulesets listing. **Future**: Advanced filtering, search, and metadata enrichment.

- **FR-031**: System MUST provide rules query capability returning rule metadata for rules active at a specified date, including: rule identifiers, effective date windows, precedence levels (Act > Regulation > Ruling > Guidance > Assumption), references (links to authoritative sources), and applicability conditions. **MVP**: Basic rule metadata query. **Future**: Advanced filtering by precedence, type, or applicability conditions.

- **FR-032**: System MUST return rule metadata without exposing internal implementation details (calculation expressions, code, or proprietary logic), enabling partners and internal users to understand which rules apply without accessing rule internals.

#### Storage Architecture

- **FR-033**: System MUST use PostgreSQL for all data storage including: active rulesets, domain entities, scenarios, Facts, and provenance relationships (via JSONB).

- **FR-034**: System MUST use PostgreSQL for all data storage including: rule definitions, effective windows, precedence, review workflow, assumptions snapshots, and change logs.

- **FR-035**: System MUST enforce Publish → Validate → Activate workflow: rules authored as versioned artifacts (Markdown/YAML), published as `ruleset-YYYYMMDD` snapshots in PostgreSQL, validated for integrity and consistency, then activated and available for computation.

- **FR-036**: System MUST support ruleset rollback: if ruleset validation fails during Publish → Validate → Activate workflow, snapshot creation MUST be automatically rolled back. System MUST support deactivation of activated rulesets and reversion to previous ruleset version. Reference: `specs/001-master-spec/spec.md` CL-037.

- **FR-037**: System MUST provide API endpoint for ruleset rollback: `POST /api/v1/rulesets/{ruleset_id}/rollback` with `target_ruleset_id` parameter. Rollback MUST require admin privileges and generate audit log entry. Rollback procedure: deactivate current ruleset (mark as `Superseded` with `valid_to` timestamp), reactivate previous ruleset version (mark as `Published` with `valid_to` set to NULL), update ruleset references to point to previous version. Reference: `specs/001-master-spec/spec.md` CL-037.

- **FR-038**: System MUST continue to support time-travel queries for rolled-back rulesets (historical queries can still access them). Existing Facts created with rolled-back ruleset MUST remain valid and queryable. New calculations MUST use reactivated previous ruleset. Reference: `specs/001-master-spec/spec.md` CL-037.

- **FR-039**: System MUST test rollback procedures before production deployment. Test rollback scenarios MUST be included in test suite. Reference: `specs/001-master-spec/spec.md` CL-037.

- **FR-040**: System MUST forbid direct hand-editing of rules in the database; all rule changes MUST originate from versioned artifacts and follow the Publish → Validate → Activate workflow.

- **FR-041**: System MUST ensure ruleset snapshots are consistent and validated when published, ensuring all referenced rules exist and integrity checks pass.

#### Performance and Scalability

- **FR-038**: System MUST execute standard calculations (e.g., single tax calculation, super contribution) within acceptable time limits as defined in success criteria.

- **FR-039**: System MUST support concurrent calculation requests from 10,000 concurrent users while maintaining accuracy, tenant isolation, and performance, including sub-50ms explain response times.

- **FR-040**: System MUST optimize rule resolution and provenance chain traversal (via closure tables/materialized views and recursive CTEs) for performance, minimizing query time while maintaining accuracy, even with 1 million Facts.

- **FR-041**: System MUST cache frequently accessed ruleset snapshots and reference data where appropriate, balancing performance with data freshness requirements.

- **FR-041A**: System MUST implement caching keyed by inputs hash + ruleset_id + as_of date with configurable TTL and invalidation rules (invalidate on ruleset publication).

- **FR-041B**: System MUST implement memory ceilings and back-pressure mechanisms to prevent memory exhaustion during large batch operations or long-horizon projections.

- **FR-041C**: System MUST implement profiling budget per endpoint with performance monitoring and alerting when thresholds are exceeded.

- **FR-041D**: System MUST implement materialized view refresh strategies (CONCURRENT refresh, incremental updates) to maintain explain performance without blocking queries, even with 1 million Facts.

- **FR-041E**: System MUST implement read replica distribution for explain queries to scale read capacity and maintain sub-50ms response times under 10,000 concurrent users.

- **FR-041F**: System MUST implement connection pooling (PgBouncer or equivalent) to efficiently manage database connections and prevent connection exhaustion at scale.

- **FR-041G**: System MUST enforce maximum recursion depth of 15 levels for provenance chain traversal (Fact → Rule → Reference → Assumption → Input) to prevent runaway queries. Typical provenance chains are 3-5 levels. Recursive CTEs MUST include depth checking (e.g., `MAX_RECURSION` clause or equivalent application-layer depth validation). Reference: `Design_docs/final_design_questions.md` Section 5.

#### Error Handling and Resilience

- **FR-042**: System MUST implement structured error responses with remediation guidance when calculations fail due to missing parameters or invalid inputs, indicating which parameters are missing and what values are expected.

- **FR-043**: System MUST implement timeouts around database queries and external service lookups to prevent blocking operations (default timeout: 30 seconds, configurable per operation type). Individual calculation operations MUST timeout after 30 seconds. When a calculation exceeds this timeout, the system MUST return 504 Gateway Timeout error with structured response including calculation progress (if available) and remediation guidance (e.g., simplifying scenario parameters, splitting into smaller calculations).

- **FR-044**: System MUST implement circuit breakers around external dependencies to fail fast when services are unavailable, with automatic recovery when services restore.

- **FR-045**: System MUST implement retry policies for transient I/O failures with exponential backoff (initial delay: 1s, max delay: 30s, max retries: 3) and idempotency guarantees to prevent duplicate calculations.

- **FR-046**: System MUST implement dead-letter queue for failed calculation jobs with replay capability, error analysis, and notification mechanisms for operators.

#### Validation and Reconciliation

- **FR-047**: System MUST perform cross-checks to ensure sum of components equals totals (e.g., total income = salary + interest + dividends + other) and cash in-out conservation is maintained (e.g., opening balance + inflows - outflows = closing balance).

- **FR-048**: System MUST perform tax reconciliation: taxable income → tax calculation → offsets → net tax, with validation of each step and detection of discrepancies exceeding tolerance thresholds.

- **FR-049**: System MUST reconcile superannuation caps trackers to contribution ledgers, validating that concessional contributions + non-concessional contributions reconcile to total contributions, and Transfer Balance Cap (TBC) and Total Super Balance (TSB) roll-forward calculations are consistent.

- **FR-050**: System MUST reconcile amortisation tables to closing balances, ensuring that opening balance + interest - repayments = closing balance, and detect rounding drift that exceeds tolerance thresholds (default: 0.01 cents per period).

#### Concurrency and Consistency

- **FR-051**: System MUST prevent race conditions when multiple calculation runs update the same scenario, using optimistic concurrency control with version numbers. When concurrent updates are detected (version mismatch), the system MUST return 409 Conflict error with remediation guidance (e.g., retrieve latest version and retry, or merge changes appropriately).

- **FR-052**: System MUST specify isolation levels for fact writes: read-committed isolation for fact creation (default), snapshot isolation for time-travel queries, with documented consistency guarantees (strong consistency for fact writes, eventual consistency acceptable for read replicas).

- **FR-053**: System MUST document consistency guarantees per operation: strong consistency for calculation operations (facts immediately visible), eventual consistency acceptable for retrieval queries (may read from read replicas with <1s lag).

#### Ruleset Consistency

- **FR-054**: System MUST perform consistency checks after ruleset publication, validating counts (rule count matches in snapshot), checksums (rule content hash matches), and referential integrity (all referenced rules exist in ruleset).

---

### Key Entities

- **Fact**: Computed outcome with units, rounding, inputs hash, rule version(s), scenario id, and full provenance. Immutable, versioned, and fully traceable. Attributes include: unique identifier, value, units, rounding precision, inputs hash, scenario id, ruleset id, as_of date, computation timestamp, and provenance relationships.

- **Rule**: Active rule in ruleset snapshot for execution. Attributes include: rule identifier, version, effective dates, precedence level, calculation expression/function, parameters, applicability conditions, and relationships to References and other Rules (via JSONB). Created in ruleset snapshot on publication.

- **Scenario**: Tagged alternative future that never overwrites base reality. Attributes include: unique scenario identifier, name, description, parameters (key-value pairs), creation timestamp, and creator information. Used to group Facts for comparison and "what-if" analysis.

- **Ruleset**: Published snapshot of rules available for computation. Attributes include: ruleset identifier (format: `ruleset-YYYYMMDD`), publication date, effective date range, status (Active, Superseded), and list of included rule versions. Stored in PostgreSQL as immutable snapshot.

- **Calculation Request**: Input to computation operation. Attributes include: client data, scenario parameters, ruleset_id, as_of date, idempotency key (optional), and tenant identifier. Transformed into structured format for rule execution.

- **Provenance Chain**: Traceable path from Fact to source rules, references, and assumptions. Enables explanation generation and compliance verification.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: System executes standard financial calculations (e.g., single tax calculation, super contribution) and returns results within 2 seconds for 95% of requests.

- **SC-002**: System maintains 100% deterministic reproducibility: identical calculation requests (same inputs, ruleset_id, as_of date) produce identical Fact values, units, and rounding across multiple executions.

- **SC-003**: System successfully builds complete provenance chains for 100% of computed Facts, with no missing links to rules, references, or assumptions.

- **SC-004**: System generates human-readable explanations within 1 second for 90% of requests, enabling real-time explainability.

- **SC-004A**: System responds to explain endpoint requests within 50ms for 95% of requests, even at scale (10,000 concurrent users, 1 million Facts), enabling fast traceability of forecast numbers back to their sources.

- **SC-005**: System supports scenario comparison queries, returning Facts for up to 10 scenarios within 5 seconds for 90% of requests.

- **SC-006**: System processes batch calculation requests with up to 100 calculations, completing within 30 seconds for 90% of batches while maintaining accuracy.

- **SC-007**: System supports concurrent calculation requests from 10,000 concurrent users without performance degradation or accuracy loss, maintaining tenant isolation and sub-50ms explain response times.

- **SC-008**: System correctly applies rule precedence and effective dates, ensuring calculations use the correct rules for the specified `as_of` date in 100% of cases.

- **SC-009**: System maintains time-travel query capability, accurately reconstructing historical calculations using ruleset versions applicable at past dates with 100% accuracy.

- **SC-010**: System stores Facts with complete provenance metadata, enabling full audit trails for 100% of computed results.

- **SC-011**: System uses fixed-point Decimal or integer cents for 100% of monetary calculations, with zero instances of binary floating-point arithmetic in financial calculations.

- **SC-012**: System detects and prevents unit mismatches (e.g., dollars + percentages) with 100% accuracy during input validation, returning clear error messages.

- **SC-013**: System detects rounding drift exceeding tolerance thresholds (0.01 cents per period) for 100% of long-horizon calculations, flagging discrepancies for review.

- **SC-014**: System implements timeouts and circuit breakers, preventing blocking operations and failing fast when external services are unavailable, with <1% false positive rate.

- **SC-015**: System performs reconciliation checks (cross-checks, tax reconciliation, super caps reconciliation, amortisation reconciliation) with 100% coverage, detecting discrepancies exceeding tolerance thresholds.

- **SC-016**: System prevents race conditions in concurrent scenario updates with 100% success rate, using appropriate concurrency control mechanisms.

- **SC-017**: System performs consistency checks after ruleset publication, detecting inconsistencies with 100% accuracy.

---

## Testing & Quality Gates

### Determinism Validation

- **SC-TEST-001**: System MUST prove deterministic reproducibility through golden dataset tests and deterministic reproducibility tests. Reference: `Design_docs/final_design_questions.md` Section 10.

- **SC-TEST-002**: System MUST validate against regulator examples:
  - **ATO examples**: At least 10 ATO tax calculation examples (taxable income, tax offsets, deductions, CGT) validated - all must match ATO examples exactly (within rounding tolerance)
  - **ASIC examples**: At least 5 ASIC compliance examples (best interests duty checks, conflict detection, advice documentation requirements) validated - all must match ASIC examples exactly
  - Test location: `backend/compute-engine/tests/golden/test_ato_minimum_validation.py` and `backend/advice-engine/tests/golden/test_asic_minimum_validation.py`
  - Reference: `specs/002-compute-engine/plan.md` Phase 8, `specs/001-master-spec/master_tasks.md` T204A, T495, T228A, T551

- **SC-TEST-003**: System MUST prove deterministic reproducibility through 1000+ iteration tests:
  - Run 1000+ iterations of same calculation (same inputs + ruleset + date)
  - Verify 100% identical outputs across all iterations
  - Test across different execution times, servers, and environments
  - Test location: `backend/compute-engine/tests/integration/test_deterministic_reproducibility_validation.py`
  - Reference: `specs/002-compute-engine/plan.md` Phase 8, `specs/001-master-spec/master_tasks.md` T205A, T497, T333

### Money Safety Validation

- **SC-TEST-004**: System MUST enforce money safety through type enforcement:
  - 100% of monetary calculations use fixed-point `decimal.Decimal` (Python) or integer cents
  - Zero instances of binary floating-point arithmetic (`float`) in financial calculations
  - Type enforcement occurs at calculation execution layer with Python type hints and runtime validation
  - Reference: `specs/002-compute-engine/spec.md` FR-008A, SC-011, `Design_docs/final_design_questions.md` Section 10

- **SC-TEST-005**: System MUST record rounding on all Facts:
  - Rounding details stored in Fact JSONB metadata columns, including rounding policy applied (ATO rules, bankers rounding), rounding precision, and rounding steps applied (before/after values)
  - Each Fact includes `rounding_precision` and `rounding_policy` fields in metadata, plus `rounding_steps` array
  - Rounding information included in provenance chains via `/explain/{fact_id}` endpoint
  - Reference: `specs/002-compute-engine/spec.md` FR-009, FR-020A, `Design_docs/final_design_questions.md` Section 10

### Performance Benchmarks

- **SC-TEST-006**: System MUST meet performance benchmarks:
  - **`/run` endpoint**: p95 latency target is 2 seconds for standard calculations (single tax calculation, super contribution). 95% of calculations complete within 2 seconds.
  - **`/explain/{fact_id}` endpoint**: p95 latency target is 50ms at scale (10,000 concurrent users, 1 million Facts). Typical performance is <10ms via closure table/materialized view. 95% of explain endpoint requests respond within 50ms at scale.
  - **Overall API response**: p95 target is 3 seconds from initial query to displayed response (excluding complex multi-scenario calculations)
  - Per-endpoint performance monitoring and alerting when thresholds exceeded
  - Reference: `specs/002-compute-engine/spec.md` SC-001, SC-004A, `specs/001-master-spec/spec.md` SC-001, `Design_docs/final_design_questions.md` Section 10

---

## Assumptions

### Domain Assumptions

- Financial calculations will continue to be rule-based and deterministic, enabling algorithmic execution without requiring human judgment during computation.

- Rule definitions will be sufficiently complete and unambiguous to enable automated execution without manual interpretation.

- Calculation inputs (client data, scenario parameters) will be provided in structured formats that can be validated and processed automatically.

- The Australian financial regulatory framework will maintain hierarchical authority (Act > Regulation > Ruling > Guidance > Assumption) enabling precedence-based rule resolution.

### Technical Assumptions

- PostgreSQL will support efficient traversal of provenance chains (via recursive CTEs) and rule applicability queries with acceptable performance.

- PostgreSQL will provide reliable access to all rule data (definitions, versions, precedence) with acceptable latency.

- Ruleset snapshot creation in PostgreSQL will complete within acceptable time limits (as defined in master spec: 5 minutes) enabling timely ruleset publication.

- Storage systems will scale to support large numbers of Facts (millions) and scenarios (thousands) with acceptable query performance.

- Access infrastructure will support concurrent requests with rate limiting and tenant isolation without performance degradation.

### Integration Assumptions

- Reference lookup services will be available and operational before Compute Engine can build complete provenance chains.

- Rule authoring and publishing workflow will be operational before Compute Engine can execute calculations.

- Natural language processing services will transform natural language requests into structured calculation requests before calling Compute Engine.

- Compliance evaluation services will query Compute Engine for Fact data when performing compliance evaluation.

---

## Scope Boundaries

### In Scope (MVP)

- Core calculation execution with deterministic results

- Scenario support for A/B comparisons and basic sensitivity analysis

- Provenance chain generation linking Facts to Rules, References, and Assumptions

- Explanation capability for human-readable provenance traces

- Facts retrieval with scenario and date filtering

- Time-travel queries using `as_of` dates and ruleset versions

- Batch processing for multiple calculations

- PostgreSQL-only storage: all data storage in single database (computation and rule management)

- Ruleset snapshot creation in PostgreSQL on ruleset publication

### Out of Scope (Future)

- Real-time streaming calculations or event-driven computation

- Advanced optimization algorithms for complex multi-rule calculations

- Machine learning-based rule inference or pattern detection

- Automated rule conflict resolution beyond precedence-based logic

- Advanced caching strategies beyond basic ruleset projection caching

- Multi-currency or international calculation support (focusing on Australian financial system)

- Real-time market data integration for dynamic calculations

---

## Dependencies

### External Dependencies

- PostgreSQL technology capable of recursive CTEs for provenance chain traversal, JSONB for relationship storage, and temporal tables for time-travel queries

- PostgreSQL technology capable of temporal queries, transactions, and audit logging

- Reference lookup services for rule-to-reference lookups in provenance chains

- Authentication/authorization system for access control (from foundational infrastructure)

- Logging and observability infrastructure for audit trails and debugging

### Internal Dependencies

- Master specification (`001-master-spec`) for system context, requirements, and architectural constraints

- Rule authoring and publishing workflow must be operational before Compute Engine can execute calculations

- Ruleset snapshot mechanism must be functional to create active ruleset snapshots in PostgreSQL

- Data extraction pipeline must populate RULES, ASSUMPTIONS, and CLIENT OUTCOME STRATEGIES before calculations can execute
