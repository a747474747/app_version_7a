# Functional Requirements - Consolidated

This document contains all functional requirements extracted from the 7 system specification files, organized by source module.

## From Master Specification

### System Architecture

- **FR-001**: System MUST maintain six distinct modules with clear boundaries: Frankie's Finance (Consumer UX), Veris Finance (Adviser UX), LLM Orchestrator, Compute Engine, References & Research Engine, and Advice Engine.

- **FR-002**: System MUST use relational database-only architecture (no graph databases) for all data storage including canonical governance (rule definitions, effective windows, precedence, review workflow, assumptions snapshots, change logs), execution data (scenarios, facts, provenance links), and explainability (provenance chains, relationship storage, time-travel queries).

- **FR-003**: System MUST enforce the Publish → Validate → Activate workflow: rules authored as versioned artifacts (Markdown/YAML), published as `ruleset-YYYYMMDD` snapshots in relational database, validated for integrity and consistency, then activated and made available for computation.

- **FR-004**: System MUST forbid direct hand-editing of rules in the database; all rule changes MUST originate from versioned artifacts and follow the Publish → Validate → Activate workflow.

### Architectural Component Boundaries

- **FR-004A**: **Compute Engine** MUST be the single source of truth for all deterministic financial logic, including tax formulas, caps, thresholds, eligibility tests, and projections. Compute Engine MUST NOT perform judgement, advice, or free-text reasoning, and MUST NOT store or serve knowledge objects (References, Rules, Assumptions, Advice Guidance, Strategies).

- **FR-004B**: **References & Research Engine** MUST be the single source of truth for all knowledge storage and retrieval, including REFERENCES, RULES, ASSUMPTIONS, ADVICE GUIDANCE, CLIENT OUTCOME STRATEGIES, FINDINGS, RESEARCH QUESTIONS, and VERDICTS. References & Research Engine MUST NOT perform numeric calculations, execute rules, generate personalised advice, or scrape raw documents.

- **FR-004C**: **Advice Engine** MUST consume Facts from Compute Engine (never calculate them) and knowledge objects from References & Research Engine (never store them). Advice Engine MUST focus on reasoning, suitability, and compliance evaluation. **Reasoning capabilities are defined in CL-039** and include: interpretation logic based on Advice Guidance (e.g., "This is usually beneficial when...", "Preferable for clients who...", "Only valuable when balance exceeds...", "Not suitable if income unstable..."); behavioral-aware advice patterns (spending habits, biases, emotional patterns, mistakes, behavioral constraints); reasoning frameworks (problem → constraint → action → result, risk → structure → tax → behaviour → goal, prioritisation patterns, scenario comparison patterns, trade-off handling patterns); comparison and aggregation operations on Facts (e.g., comparing Fact values, summing Fact collections). Advice Engine MUST NOT define tax formulas, perform numeric calculations that produce new Facts, scrape raw documents, store knowledge objects, or override deterministic outputs from Compute Engine.

- **FR-004D**: **LLM Orchestrator** MUST be a thin natural-language router that interprets user input, builds structured requests for the three engines, calls them in sequence, validates/repairs schemas, and turns outputs back into user-facing text. LLM Orchestrator MUST NOT invent rules, perform calculations, override deterministic outputs, store knowledge objects, or contain business logic.

### Deterministic Calculations

- **FR-005**: System MUST ensure all financial calculations are deterministic and reproducible: same inputs + same `ruleset_id` + same `as_of` date MUST produce identical outputs.

- **FR-006**: System MUST pin every compute operation to explicit `ruleset_id` and `as_of` date parameters.

- **FR-007**: System MUST make all numeric tolerances and rounding standards explicit in rule definitions.

- **FR-008**: System MUST treat all computed Facts as immutable with full provenance (rule versions, inputs hash, scenario id, units, rounding).

- **FR-007A**: System MUST use fixed-point Decimal or integer cents for all monetary values; binary floating-point arithmetic is FORBIDDEN for financial calculations.

- **FR-007B**: System MUST enforce explicit units and dimensional checks for all calculations (%, basis points, dollars, years, etc.) with validation to prevent unit mismatches.

- **FR-007C**: System MUST specify rounding policy per field (ATO rules, bankers rounding vs away-from-zero) and when rounding occurs (at each step vs at end of calculation) in rule definitions.

### Provenance and Explainability

- **FR-009**: System MUST provide end-to-end provenance for every computed result (Fact) traceable through explanation requests.

- **FR-010**: System MUST link provenance chains in the format: **Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions** with versions and dates.

- **FR-010A**: System MUST include per-fact provenance details: inputs hash, rules applied (with versions), references cited, assumptions snapshot (with versions), and rounding steps applied.

- **FR-010B**: System MUST provide stable anchors/IDs for citations enabling reproducible reference links even after reference updates.

- **FR-010C**: System MUST export evidence packs in both JSON and PDF formats with version information, timestamps, and complete provenance chains.

- **FR-011**: System MUST support time-travel queries using effective dates and ruleset versions to reconstruct historical calculations.

- **FR-012**: System MUST export all recommendations with full provenance chains suitable for compliance packs.

### LLM Orchestration

- **FR-013**: System MUST use LLM Orchestrator as a stateless translator that converts natural language intent into structured compute requests; LLMs MUST NEVER determine financial outcomes or replace rule logic.

- **FR-014**: System MUST validate all LLM outputs that affect calculations against rules before execution.

- **FR-015**: System MUST provide natural language parsing that returns intent, parameters, and next action, and conversational chat that returns messages, tool calls, and citations.

### Rule Management

- **FR-016**: System MUST enforce two-person review (four-eyes principle) before rule publication.

- **FR-017**: System MUST maintain rule precedence hierarchy: Act > Regulation > Ruling > Guidance > Assumption, with strict enforcement of effective date windows.

- **FR-018**: System MUST resolve rule conflicts explicitly through review workflow when rules at the same precedence level conflict.

- **FR-019**: System MUST store all rules as structured artifacts (Markdown/YAML) with schema validation, tests, examples, edge cases, narrative summaries, version tags, and effective date windows.

### Data Extraction

- **FR-020**: System MUST extract and maintain five core data types: REFERENCES (legal/regulatory sources), RULES (calculation and taxation rules), ASSUMPTIONS (financial parameters), ADVICE GUIDANCE (professional standards), and CLIENT OUTCOME STRATEGIES (actionable planning approaches).

- **FR-021**: System MUST maintain data extraction quality standards: completeness (all relevant instances), accuracy (exact values from sources), context (narrative summaries), traceability (link to sources), consistency (standardized formats), and currency (effective dates and versions).

### Schema Evolution and Feedback

- **FR-SCHEMA-01**: Compute Engine and Advice Engine implementations MAY emit structured schema-feedback requests when a missing field, relationship, or canonical mapping blocks correct implementation.

- **FR-SCHEMA-02**: The References & Research Engine MUST treat schema-feedback as a first-class refinement type (equal priority to missing content) and update canonical_data_model.md, schema definitions, and DB migrations accordingly before relevant freezes.

- **FR-SCHEMA-03**: Post-Freeze A, only non-breaking schema changes are permitted without a major version bump (see SCHEMA_EVOLUTION_POLICY.md).

- **FR-SCHEMA-REHEARSAL**: **Schema Dress Rehearsal** MUST be completed before Freeze A is declared. This involves implementing four real end-to-end golden calculations (PAYG marginal tax 2024–25 + offsets, CGT discount event, super contributions + Div 293, negative gearing mortgage interest) using the actual PostgreSQL + SQLAlchemy models generated from research. Every schema friction point (missing relation requiring >2 joins, awkward join patterns requiring >3 table joins, missing provenance role preventing complete chain construction, excessive JSONB usage with nested depth >2) MUST be logged in `backend/compute-engine/src/schema_rehearsal/friction_log.md` and fixed before Freeze A. Freeze A only happens after Schema Dress Rehearsal passes with **zero unresolved schema-friction items**.

### Access Control

- **FR-025**: System MUST enforce access control via API keys/OAuth, tenant isolation, and rate limits.

- **FR-025A**: System MUST provide pagination for large result sets with configurable page sizes.

- **FR-025B**: System MUST implement clear error taxonomy: 4xx for validation errors, 409 for conflicts, 5xx for compute failures, with structured error responses including remediation guidance. **All modules MUST follow the standardized error taxonomy defined in CL-025 and this requirement**. Error responses MUST include structured format: `{ error_code: string, message: string, remediation: string, retryable: boolean, retry_after_seconds?: number }`. Reference: `specs/001-master-spec/master_spec.md` CL-025 for complete error taxonomy details.

- **FR-025C**: System MUST support partial-result semantics for batch operations, returning successful results alongside errors for failed items.

- **FR-025D**: System MUST implement API versioning using URL path versioning format `/api/v{major}/...` for all external-facing APIs. **All modules MUST follow the standardized API versioning policy defined in `specs/001-master-spec/API_VERSIONING_POLICY.md`**. Breaking changes require new major version; non-breaking changes (new optional parameters, new endpoints, new response fields) do not require version bump. Deprecation period: 6 months standard, 3 months for internal module-to-module APIs. Reference: `specs/001-master-spec/API_VERSIONING_POLICY.md` for complete versioning strategy, deprecation policy, and migration guides.

- **FR-025E**: System MUST implement cross-module integration tests that verify end-to-end workflows across module boundaries. **All modules MUST include integration tests that validate**: (1) API contract compatibility between modules (e.g., Compute Engine → References Engine, Advice Engine → Compute Engine, LLM Orchestrator → all engines), (2) Error propagation and handling across module boundaries, (3) Data format consistency (request/response schemas match between producer and consumer modules), (4) Performance and latency requirements met across module boundaries, (5) Tenant isolation maintained across module boundaries. Integration tests MUST be located in `backend/{module}/tests/integration/test_{target_module}_integration.py` and MUST run as part of CI/CD pipeline. Reference: `specs/001-master-spec/master_tasks.md` T324 for end-to-end integration tests across all modules.

- **FR-026**: System MUST prohibit direct end-user backend access; all access MUST be mediated by Frankie's Finance, Veris Finance, or Partner integrations.

### Authentication Flows

- **FR-047**: System MUST implement OAuth2 Authorization Code flow with PKCE (Proof Key for Code Exchange) for both web (Veris Finance) and mobile (Frankie's Finance) clients. Reference: CL-038.

- **FR-048**: System MUST use PKCE code verifier and code challenge (SHA256) to protect authorization code exchange and prevent authorization code interception attacks. Reference: CL-038.

- **FR-049**: System MUST issue short-lived access tokens with maximum lifetime of 15 minutes to minimize exposure window if tokens are compromised. Reference: CL-038.

- **FR-050**: System MUST issue refresh tokens with maximum lifetime of 7 days to balance security and user experience, requiring periodic re-authentication. Reference: CL-038.

- **FR-051**: System MUST rotate refresh tokens on every use: when a refresh token is used to obtain a new access token, the system MUST issue a new refresh token and invalidate the old refresh token. Reference: CL-038.

- **FR-052**: System MUST store refresh tokens for web clients (Veris Finance) in HTTP-only, Secure, SameSite=Strict cookies to prevent XSS and CSRF attacks. Reference: CL-038.

- **FR-053**: System MUST store refresh tokens for mobile clients (Frankie's Finance) in device SecureStore (iOS Keychain or Android Keystore) with appropriate access controls and encryption. Reference: CL-038.

- **FR-054**: System MUST validate access tokens on every API request and reject expired tokens with 401 Unauthorized status. Reference: CL-038.

- **FR-055**: System MUST automatically refresh expired access tokens using refresh tokens without requiring user interaction, maintaining seamless user experience. Reference: CL-038.

- **FR-056**: System MUST require re-authentication when refresh tokens expire or are invalidated, ensuring users periodically re-authenticate. Reference: CL-038.

- **FR-057**: System MUST support token revocation: users MUST be able to revoke their own tokens, and administrators MUST be able to revoke tokens for security incidents. Reference: CL-038.

- **FR-058**: System MUST prevent refresh token reuse: after a refresh token is used, it MUST be immediately invalidated and cannot be used again, even if the new refresh token is not yet received by the client. Reference: CL-038.

- **FR-059**: System MUST handle concurrent refresh token usage: if multiple refresh attempts occur with the same token, only the first MUST succeed, and subsequent attempts MUST be rejected. Reference: CL-038.

- **FR-060**: System MUST include tenant context in access tokens to enable tenant isolation enforcement at the API layer. Reference: CL-038.

- **FR-061**: System MUST log all authentication events (login, token refresh, token revocation, failed authentication attempts) for security auditing and compliance. Reference: CL-038.

- **FR-062**: System MUST support multiple concurrent sessions per user (multiple devices) with each session maintaining independent refresh tokens. Reference: CL-038.

- **FR-063**: System MUST validate PKCE code verifier matches the code challenge during token exchange, rejecting mismatched verifiers. Reference: CL-038.

- **FR-064**: System MUST enforce rate limiting on authentication endpoints to prevent brute force attacks and token enumeration (5 failed authentication attempts per minute per IP/user). Reference: CL-038.

- **FR-065**: System MUST handle clock skew between client and server: token expiration validation MUST allow reasonable clock skew tolerance (±5 minutes) to prevent false rejections. Reference: CL-038.

- **FR-066**: System MUST provide clear error messages for authentication failures (invalid credentials, expired tokens, revoked tokens) without leaking sensitive information about account existence or token validity. Reference: CL-038.

### User Experience

- **FR-027**: System MUST provide Frankie's Finance (Consumer UX) with emotion-first design, non-linear navigation via spatial metaphors (path → front door → living room/study/garden), where Frankie serves as a companion guide and the app provides the advice voice.

- **FR-028**: System MUST provide Veris Finance (Adviser UX) with professional calm design, minimal chrome, clear hierarchy, comparative dashboards, conversational interface, data-centric visualizations, and audit log always available.

- **FR-029**: System MUST enable navigation by intent: user questions dictate next views; system brings appropriate modules to users.

- **FR-039**: System MUST connect Frankie's Finance to compliance validation to validate all financial advice provided to consumers, ensuring compliance with best interests duty and regulatory requirements.

- **FR-040**: System MUST display compliance validation results in Frankie's Finance in a user-friendly, non-technical manner appropriate for consumers, including warnings and required actions when applicable.

### Compliance and Governance

- **FR-030**: System MUST enforce per-tenant data isolation at the data layer. **Complete security guarantee and implementation details are defined in CL-031**. User A MUST NEVER be able to see User B's data under ANY circumstances, including bugs, misconfigured queries, security vulnerabilities, or system errors. This MUST be enforced through multiple defense layers: database-level RLS policies, application-level tenant validation, automatic query filtering, and fail-safe error handling.

- **FR-030A**: System MUST include automated security tests that verify cross-tenant data access is impossible. Tests MUST simulate bugs, misconfigured queries, malicious input, missing tenant context, and other failure scenarios to ensure User A cannot access User B's data under any conditions.

- **FR-031**: System MUST maintain PII-minimal logging with field-level redaction.

- **FR-031A**: System MUST encrypt data at rest and in transit using industry-standard encryption.

- **FR-031B**: System MUST implement secrets management for API keys, database credentials, OpenRouter API keys, and OpenAI API keys (for BYOK) with no environment variable leakage into Facts or logs.

- **FR-031C**: System MUST implement input hardening to prevent code injection in formulas, expressions, or rule definitions, with validation and sanitization.

- **FR-031D**: System MUST maintain supply-chain security with pinned dependency hashes, Software Bill of Materials (SBOM), and vulnerability scanning.

- **FR-067**: System MUST display PII filtering explanation to Frankie's Finance users during initial setup, before they can ask financial questions.

- **FR-068**: System MUST collect user name, date of birth, and suburb during Frankie's Finance initial setup, and explain that this information helps personalize the experience.

- **FR-069**: System MUST clearly explain to Frankie's Finance users that their name and identifying information will be filtered out of requests to external AIs so that information cannot be connected to them.

- **FR-070**: System MUST provide access to privacy policy from the PII filtering explanation in Frankie's Finance, referencing the app's privacy rules.

- **FR-071**: System MUST use the collected user name to enhance PII filtering effectiveness in Frankie's Finance, enabling more accurate detection of name references in queries.

- **FR-072**: System MUST display detailed PII filtering explanation to Veris Finance advisers during client setup, before processing client queries.

- **FR-073**: System MUST collect comprehensive client PII during Veris Finance client setup (name, DOB, address, contact details, account numbers, TFN, etc.) and explain what information is being collected and why.

- **FR-074**: System MUST provide detailed explanation to Veris Finance advisers covering: how client PII is handled, how filtering works, how it ensures client information is not sent to external LLMs, and how this complies with privacy regulations.

- **FR-075**: System MUST provide access to privacy policy from the PII filtering explanation in Veris Finance, referencing the same privacy rules used by Frankie's Finance.

- **FR-076**: System MUST use the collected comprehensive client PII to enhance filtering effectiveness in Veris Finance, ensuring no client identifying information reaches external LLM providers.

- **FR-077**: System MUST provide professional language that advisers can use to explain privacy protections to clients.

- **FR-078**: System MUST ensure privacy explanations are displayed before any queries are processed that might involve PII, even if setup is incomplete.

---

## From Compute Engine Specification

### Calculation Execution

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

### Fact Storage and Provenance

- **FR-009**: System MUST store all computed results as Facts with full provenance: rule versions, inputs hash, scenario id, units, rounding, and timestamp.

- **FR-010**: System MUST treat Facts as immutable: once computed and stored, Facts cannot be modified; new calculations create new Facts.

- **FR-011**: System MUST link Facts to Rules via provenance relationships, enabling traversal from Fact → Rule → Reference → Assumptions.

- **FR-012**: System MUST store Facts with scenario tags, enabling scenario-based queries and comparisons without overwriting base reality Facts.

- **FR-013**: System MUST generate unique Fact identifiers that can be used to retrieve explanations and trace provenance chains.

- **FR-014**: System MUST store Facts with version information, linking to the specific ruleset version and rule versions used in calculation.

### Scenario Management

- **FR-015**: System MUST support creation and management of scenarios as tagged alternative futures that never overwrite base reality.

- **FR-016**: System MUST execute calculations for multiple scenarios independently, producing separate Facts for each scenario.

- **FR-017**: System MUST support scenario comparison queries, enabling users to retrieve Facts for multiple scenarios with consistent structure.

- **FR-018**: System MUST maintain scenario metadata (name, description, parameters) to enable scenario identification and management.

### Provenance and Explainability

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

### Access and Integration

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

### Rules Intelligence

- **FR-030**: System MUST provide rulesets listing capability returning all published rulesets with metadata: ruleset identifiers (format: `ruleset-YYYYMMDD`), publication dates, effective date ranges, status (Active, Superseded), and rule counts. **MVP**: Basic rulesets listing. **Future**: Advanced filtering, search, and metadata enrichment.

- **FR-031**: System MUST provide rules query capability returning rule metadata for rules active at a specified date, including: rule identifiers, effective date windows, precedence levels (Act > Regulation > Ruling > Guidance > Assumption), references (links to authoritative sources), and applicability conditions. **MVP**: Basic rule metadata query. **Future**: Advanced filtering by precedence, type, or applicability conditions.

- **FR-032**: System MUST return rule metadata without exposing internal implementation details (calculation expressions, code, or proprietary logic), enabling partners and internal users to understand which rules apply without accessing rule internals.

### Storage Architecture

- **FR-033**: System MUST use PostgreSQL for all data storage including: active rulesets, domain entities, scenarios, Facts, and provenance relationships (via JSONB).

- **FR-034**: System MUST use PostgreSQL for all data storage including: rule definitions, effective windows, precedence, review workflow, assumptions snapshots, and change logs.

- **FR-035**: System MUST enforce Publish → Validate → Activate workflow: rules authored as versioned artifacts (Markdown/YAML), published as `ruleset-YYYYMMDD` snapshots in PostgreSQL, validated for integrity and consistency, then activated and available for computation.

- **FR-036**: System MUST support ruleset rollback: if ruleset validation fails during Publish → Validate → Activate workflow, snapshot creation MUST be automatically rolled back. System MUST support deactivation of activated rulesets and reversion to previous ruleset version. Reference: `specs/001-master-spec/spec.md` CL-037.

- **FR-037**: System MUST provide API endpoint for ruleset rollback: `POST /api/v1/rulesets/{ruleset_id}/rollback` with `target_ruleset_id` parameter. Rollback MUST require admin privileges and generate audit log entry. Rollback procedure: deactivate current ruleset (mark as `Superseded` with `valid_to` timestamp), reactivate previous ruleset version (mark as `Published` with `valid_to` set to NULL), update ruleset references to point to previous version. Reference: `specs/001-master-spec/spec.md` CL-037.

- **FR-038**: System MUST continue to support time-travel queries for rolled-back rulesets (historical queries can still access them). Existing Facts created with rolled-back ruleset MUST remain valid and queryable. New calculations MUST use reactivated previous ruleset. Reference: `specs/001-master-spec/spec.md` CL-037.

- **FR-039**: System MUST test rollback procedures before production deployment. Test rollback scenarios MUST be included in test suite. Reference: `specs/001-master-spec/spec.md` CL-037.

- **FR-040**: System MUST forbid direct hand-editing of rules in the database; all rule changes MUST originate from versioned artifacts and follow the Publish → Validate → Activate workflow.

- **FR-041**: System MUST ensure ruleset snapshots are consistent and validated when published, ensuring all referenced rules exist and integrity checks pass.

### Performance and Scalability

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

### Error Handling and Resilience

- **FR-042**: System MUST implement structured error responses with remediation guidance when calculations fail due to missing parameters or invalid inputs, indicating which parameters are missing and what values are expected.

- **FR-043**: System MUST implement timeouts around database queries and external service lookups to prevent blocking operations (default timeout: 30 seconds, configurable per operation type). Individual calculation operations MUST timeout after 30 seconds. When a calculation exceeds this timeout, the system MUST return 504 Gateway Timeout error with structured response including calculation progress (if available) and remediation guidance (e.g., simplifying scenario parameters, splitting into smaller calculations).

- **FR-044**: System MUST implement circuit breakers around external dependencies to fail fast when services are unavailable, with automatic recovery when services restore.

- **FR-045**: System MUST implement retry policies for transient I/O failures with exponential backoff (initial delay: 1s, max delay: 30s, max retries: 3) and idempotency guarantees to prevent duplicate calculations.

- **FR-046**: System MUST implement dead-letter queue for failed calculation jobs with replay capability, error analysis, and notification mechanisms for operators.

### Validation and Reconciliation

- **FR-047**: System MUST perform cross-checks to ensure sum of components equals totals (e.g., total income = salary + interest + dividends + other) and cash in-out conservation is maintained (e.g., opening balance + inflows - outflows = closing balance).

- **FR-048**: System MUST perform tax reconciliation: taxable income → tax calculation → offsets → net tax, with validation of each step and detection of discrepancies exceeding tolerance thresholds.

- **FR-049**: System MUST reconcile superannuation caps trackers to contribution ledgers and validate Transfer Balance Cap (TBC) and Total Super Balance (TSB) roll-forward calculations. **Tolerance**: Discrepancies exceeding 0.01 cents MUST be flagged as reconciliation failures.

- **FR-050**: System MUST reconcile amortisation tables to closing balances and detect rounding drift that exceeds tolerance thresholds. **Tolerance**: Rounding drift exceeding 0.01 cents per period MUST be flagged for review.

### Concurrency and Consistency

- **FR-051**: System MUST prevent race conditions when multiple calculation runs update the same scenario, using optimistic concurrency control with version numbers. When concurrent updates are detected (version mismatch), the system MUST return 409 Conflict error with remediation guidance (e.g., retrieve latest version and retry, or merge changes appropriately).

- **FR-052**: System MUST specify isolation levels for fact writes: read-committed isolation for fact creation (default), snapshot isolation for time-travel queries, with documented consistency guarantees (strong consistency for fact writes, eventual consistency acceptable for read replicas).

- **FR-053**: System MUST document consistency guarantees per operation: strong consistency for calculation operations (facts immediately visible), eventual consistency acceptable for retrieval queries (may read from read replicas with <1s lag).

### Ruleset Consistency

- **FR-054**: System MUST perform consistency checks after ruleset publication, validating counts (rule count matches in snapshot), checksums (rule content hash matches), and referential integrity (all referenced rules exist in ruleset).

---

## From References & Research Engine Specification

### Reference Storage and Management

- **FR-001**: System MUST store Reference objects with unique identifiers, type (Act, Regulation, Guidance, Case), title, category classification, source URL, version history, and effective date windows.

- **FR-002**: System MUST extract and store pinpoints (specific sections, paragraphs, clauses) for each reference, enabling precise citation and navigation to exact locations within source documents.

- **FR-003**: System MUST maintain version history for references, tracking effective date ranges, change summaries, and relationships between versions (supersedes, amends, replaces).

- **FR-004**: System MUST normalize reference content for consistent storage regardless of source format (PDF, HTML, structured data), preserving original formatting where necessary for legal accuracy.

- **FR-005**: System MUST support time-travel queries, allowing retrieval of reference versions applicable at specific dates via `as_of` date parameters. When an `as_of` date falls before any version exists or after all versions have been superseded, the system MUST return an error (404 Not Found or 422 Unprocessable Entity) with the earliest/latest available version dates and remediation guidance suggesting appropriate dates.

### Ingestion and Processing

- **FR-006**: System MUST support ingestion of documents in multiple formats: PDF, HTML, CSV, YAML, plain text, and structured data formats.

- **FR-007**: System MUST automatically classify document types (Act, Regulation, Guidance, Case) during ingestion with configurable confidence thresholds.

- **FR-008**: System MUST extract metadata automatically from documents: title, type, effective dates, source URL, publication dates, and regulatory body.

- **FR-009**: System MUST extract pinpoints automatically from structured documents (section numbers, paragraph identifiers, clause references) and support manual pinpoint creation for unstructured documents.

- **FR-010**: System MUST flag documents requiring manual review when classification confidence is low, extraction fails, or data quality issues are detected.

- **FR-011**: System MUST support batch ingestion of multiple documents with progress tracking and error reporting. When batch ingestion fails partially (some documents succeed, others fail), the system MUST return partial success response with detailed error report per document, including success/failure status and specific error messages for failed documents.

### Data Scraping Submodule

- **FR-027**: System MUST monitor `Research/human_provided_new_sources.md` for sources with status "Pending" and automatically scrape/download them into the appropriate folders in the `Research/` directory structure.

- **FR-028**: System MUST attempt multiple scraping methods for each source: direct HTTP download, RSS feed discovery, API access, headless browser rendering, and other methods as appropriate. If standard methods fail, the system MUST create new scraping methods and log the approach for future reference.

- **FR-029**: System MUST handle audio sources (podcasts, webinars, interviews) by attempting to find transcripts via RSS feeds or external sources. If transcripts are unavailable, the system MUST generate transcripts using transcription services and store both audio and transcript files.

- **FR-030**: System MUST update `RESEARCH_PROGRESS.md` after each scraping operation, updating document counts by folder, type, and regulatory body, and tracking success/failure statistics.

- **FR-031**: System MUST update `human_provided_new_sources.md` after scraping operations, changing status from "Pending" to "Processing", then to "Completed" or "Failed", and moving entries to the Processing History section with processing date and target folder information.

- **FR-032**: System MUST log failed scraping attempts in `human_provided_new_sources.md` Failed Downloads section, including error details, methods attempted, retry count, and last attempt timestamp.

### Data Cleaning Submodule

- **FR-033**: System MUST clean scraped or human-provided data before LLM extraction, converting PDFs to text, removing headers/footers/page numbers, preserving document structure (sections, paragraphs), and removing formatting artifacts.

- **FR-034**: System MUST only chunk cleaned text if it exceeds 60,000 tokens (modern models handle this easily). Chunk sizes MUST default to 60,000 tokens to avoid unnecessary splitting. Chunking MUST be configurable for specific model requirements.

- **FR-035**: System MUST ensure chunks respect document boundaries (sections, paragraphs) and do not split content mid-sentence or mid-paragraph unless absolutely necessary for size constraints (only when document exceeds 60k token threshold).

- **FR-036**: System MUST store chunk metadata (chunk ID, position in document, size in tokens/characters, model compatibility information) only when chunking occurs, enabling dynamic chunk combination or splitting based on target model requirements for large documents.

- **FR-037**: System MUST preserve structured data (tables, lists, code) in formats readable by LLMs (markdown tables, formatted lists), maintaining relationships between structured elements and including context markers indicating structure type.

- **FR-038**: System MUST update `RESEARCH_PROGRESS.md` after cleaning operations, marking documents as extraction-ready and updating processing statistics.

### Source Management Instructions

- **FR-039**: System MUST provide clear instructions in `human_provided_new_sources.md` for when to store data locally versus linking to online sources: use URLs for online sources with stable links, use direct file placement for local files not available online, use URLs for frequently changing sources requiring periodic re-scraping, use direct file placement for large files or collections to reduce scraping overhead.

### Search and Retrieval

- **FR-012**: System MUST provide search capability supporting queries by title, section number, keyword, type, and effective date range. When a search query returns no results, the system MUST return an empty result set with suggestions (similar search terms, alternative keywords, type filters) and clear messaging to help users refine their search.

- **FR-013**: System MUST return search results ranked by relevance with metadata (type, effective dates, version, source URL) and preview text.

- **FR-014**: System MUST provide retrieval capability returning full reference details including metadata, version history, and full text content.

- **FR-015**: System MUST provide pinpoint retrieval capability returning all pinpoints for a reference with section numbers, text excerpts, and navigation paths.

- **FR-016**: System MUST provide retrieval optimized for AI models, returning references in formats suitable for embedding in prompts with structured metadata and citation-ready text.

- **FR-017**: System MUST support filtering search results by type (Act, Regulation, Guidance, Case), effective date range, and regulatory body.

### Access and Integration

- **FR-018**: System MUST provide access following the master specification's requirements.

- **FR-019**: System MUST support access control with tenant isolation and rate limits as specified in the master specification (see CL-031 and FR-030 for security guarantee that User A can NEVER see User B's data under ANY circumstances).

- **FR-019A**: System MUST include automated security tests that verify cross-tenant data access is impossible for all References & Research Engine endpoints. Tests MUST simulate bugs, misconfigured queries, malicious input, missing tenant context, and other failure scenarios to ensure User A cannot access User B's references, research documents, or extracted data under any conditions (see FR-030A in master specification).

- **FR-020**: System MUST provide reference lookups for provenance chains, enabling Fact → Rule → Reference tracing.

- **FR-021**: System MUST provide reference lookups for regulatory requirements and compliance verification.

- **FR-022**: System MUST provide reference retrieval for citation generation and context enhancement.

### Data Quality and Governance

- **FR-023**: System MUST maintain data extraction quality standards: completeness (all relevant references ingested), accuracy (exact text from sources), context (narrative summaries), traceability (source URLs), consistency (standardized formats), and currency (effective dates and versions).

- **FR-024**: System MUST validate reference data against schema requirements before storage, ensuring required fields are present and data types are correct.

- **FR-025**: System MUST maintain audit logs tracking all reference ingestion, updates, version changes, and access patterns for compliance and debugging.

- **FR-026**: System MUST detect and prevent duplicate references based on title, type, and effective dates, merging metadata when appropriate. When duplicates are detected during ingestion, the system MUST merge metadata, maintain a single canonical reference, and link versions together, ensuring no duplicate entries exist in the system.

- **FR-026A**: System MUST handle invalid reference URLs: when a reference document URL becomes invalid or the source document is removed, the system MUST mark the URL as invalid, retain the stored reference content, and log the change for review. The reference MUST remain accessible and queryable even with an invalid URL.

- **FR-026B**: System MUST provide instructions in `human_provided_new_sources.md` explaining when to use URLs versus direct file placement: URLs for online sources with stable links, direct file placement for local files not available online, URLs for frequently changing sources requiring periodic re-scraping, direct file placement for large files or collections to reduce scraping overhead.

---

## From Advice Engine Specification

### Compliance Evaluation

- **FR-001**: System MUST evaluate compliance obligations deterministically, checking best-interests duty, conflicts of interest, documentation requirements, and product replacement logic.

- **FR-002**: System MUST evaluate compliance using Advice Guidance (mandatory obligations and professional standards) stored in the system, ensuring evaluations are based on current regulatory requirements. When Advice Guidance data isn't available for a compliance evaluation (Advice Guidance hasn't been ingested yet, or retrieval fails), the system MUST return 422 Unprocessable Entity error with specific missing Advice Guidance identifiers and remediation guidance (suggesting ingesting Advice Guidance or providing Advice Guidance data).

- **FR-003**: System MUST check best-interests duty by evaluating whether recommendations serve the client's interests, considering client circumstances, objectives, and risk tolerance.

- **FR-004**: System MUST detect conflicts of interest by analyzing adviser relationships, product recommendations, and fee structures, generating warnings when conflicts are identified.

- **FR-005**: System MUST verify documentation requirements by checking whether required documents (FSG, SOA, ROA) have been created or are planned, generating required actions if documentation is missing.

- **FR-006**: System MUST evaluate product replacement logic by checking whether product switches are justified, documented, and serve the client's best interests, following regulatory requirements for product replacement.

- **FR-007**: System MUST use Fact data when evaluating compliance, ensuring evaluations are based on accurate calculations and client circumstances. When compliance evaluation requires Fact data that isn't available (Facts haven't been computed yet, or Fact retrieval fails), the system MUST return 422 Unprocessable Entity error with specific missing Fact identifiers and remediation guidance (suggesting computing Facts first or providing Fact data).

- **FR-008**: System MUST reference regulatory requirements when evaluating compliance, linking compliance outcomes to authoritative sources.

### Compliance Access

- **FR-009**: System MUST provide compliance checking capability accepting client data, computed Facts, and advice recommendations, returning compliance outcomes, warnings, and required actions.

- **FR-010**: System MUST return compliance evaluation results in structured format with clear indication of compliance status and specific issues identified.

- **FR-011**: System MUST provide compliance requirements capability returning required actions, documentation, and professional standards for specific advice contexts. When a context has no applicable requirements, the system MUST return an empty result set with clear messaging explaining that no requirements apply for this context.

- **FR-012**: System MUST support context-based requirement queries, filtering requirements based on advice type (personal advice, general advice, product recommendation) and client circumstances.

- **FR-013**: System MUST support time-travel queries for compliance requirements, using `as_of` dates to return requirements applicable at specific points in time.

- **FR-014**: System MUST enforce access control with tenant isolation and rate limits as specified in the master specification (see CL-031 and FR-030 for security guarantee that User A can NEVER see User B's data under ANY circumstances).

- **FR-014A**: System MUST include automated security tests that verify cross-tenant data access is impossible for all Advice Engine endpoints. Tests MUST simulate bugs, misconfigured queries, malicious input, missing tenant context, and other failure scenarios to ensure User A cannot access User B's compliance evaluations, advice guidance, or client outcome strategies under any conditions (see FR-030A in master specification).

### Warnings and Required Actions

- **FR-015**: System MUST generate specific, actionable warnings when compliance issues are identified, explaining what the issue is, why it matters, and how to resolve it.

- **FR-016**: System MUST generate required actions when compliance obligations are not met, listing specific steps that must be taken to achieve compliance.

- **FR-017**: System MUST prioritize warnings and required actions by severity, indicating which issues must be resolved before advice can be considered compliant.

- **FR-018**: System MUST reference regulatory sources in warnings and required actions, enabling users to verify requirements and demonstrate compliance.

- **FR-019**: System MUST format warnings for different audiences: technical language for advisers, consumer-friendly language for consumers accessing advice through Frankie's Finance.

### Compliance Documentation

- **FR-020**: System MUST generate compliance checklists including required documents (FSG, SOA, ROA), required actions (client assessment, conflict checks), and professional standards. When some checklist items cannot be determined (e.g., required documents that depend on incomplete client data), the system MUST generate a partial checklist with available items and mark undetermined items with explanations of what data is needed.

- **FR-021**: System MUST track completion status for compliance checklist items, enabling advisers to see what has been completed and what remains.

- **FR-022**: System MUST export compliance checklists in formats suitable for inclusion in compliance packs, with timestamps, completion status, and regulatory citations.

- **FR-023**: System MUST link compliance checklists to specific advice scenarios, enabling advisers to maintain compliance documentation for each client engagement.

### Integration

- **FR-024**: System MUST retrieve Fact data for compliance evaluation, ensuring evaluations are based on accurate calculations.

- **FR-025**: System MUST retrieve regulatory requirements and professional standards, ensuring compliance evaluations reference authoritative sources.

- **FR-026**: System MUST validate consumer advice, ensuring all advice provided to consumers meets compliance requirements.

- **FR-027**: System MUST validate adviser advice, providing compliance checking and documentation support for professional advisers.

### Deterministic Evaluation

- **FR-028**: System MUST evaluate compliance deterministically: same advice + same client data + same Facts + same `as_of` date MUST produce identical compliance outcomes.

- **FR-029**: System MUST pin compliance evaluations to explicit `as_of` dates and Advice Guidance versions, enabling reproducibility and historical reconstruction.

- **FR-030**: System MUST maintain audit logs of all compliance evaluations, tracking what was evaluated, when, and what outcomes were generated.

---

## From LLM Orchestrator Specification

### Intent Detection and Parsing

- **FR-001**: System MUST detect user intent from natural language queries, identifying the type of request (calculation, explanation, comparison, information request) and extracting relevant parameters.

- **FR-002**: System MUST extract structured parameters from natural language queries, identifying client data, scenario parameters, time horizons, and other inputs needed for calculations or advice.

- **FR-003**: System MUST identify missing required parameters in user queries and return structured responses indicating what information is needed, enabling clients to request clarification.

- **FR-004**: System MUST handle ambiguous queries by either requesting clarification or making reasonable inferences based on context, while maintaining transparency about assumptions made. When a user's query is ambiguous and the system cannot determine intent with sufficient confidence, the system MUST return a structured response requesting clarification, listing possible interpretations for the user to choose from.

- **FR-005**: System MUST provide intent parsing capability that accepts natural language queries and returns structured output indicating detected intent, extracted parameters, and the next action to take.

### Conversational Interface

- **FR-006**: System MUST provide conversational chat capability that accepts message history and returns conversational responses with tool calls and citations.

- **FR-007**: System MUST maintain conversation context across multiple turns, understanding references to previous messages and maintaining coherent dialogue. When conversation context exceeds LLM token limits, the system MUST summarize or truncate oldest messages, maintain recent context, and return a warning if truncation occurs to inform users that older context may not be available.

- **FR-008**: System MUST generate tool calls (structured requests to backend modules) within conversational responses, enabling natural dialogue with structured execution.

- **FR-009**: System MUST include citations to authoritative sources (References) in conversational responses, enabling users to verify information and building trust.

- **FR-010**: System MUST format conversational responses appropriately for different audiences: consumer-friendly language for Frankie's Finance, professional language for Veris Finance.

### Safety and Privacy

- **FR-011**: System MUST filter PII (personally identifiable information) before sending queries to external LLM providers, maintaining privacy while enabling intent detection.

- **FR-012**: System MUST detect and filter inappropriate or harmful content, preventing safety issues and maintaining professional standards.

- **FR-013**: System MUST preserve filtered PII for internal use (Compute Engine, Advice Engine) while ensuring external LLM providers never receive sensitive information. When PII filtering removes critical information needed for intent detection, the system MUST preserve the filtered PII internally, use an anonymized version for LLM (e.g., replacing "$450k" with "[AMOUNT]" or "super balance is [AMOUNT]"), and restore original values for downstream modules (Compute Engine, Advice Engine).

- **FR-014**: System MUST provide clear, user-friendly messaging when queries are filtered for safety or privacy reasons, without exposing technical filtering details.

### Schema Validation

- **FR-015**: System MUST validate all LLM outputs against expected schemas before they are used to generate structured requests, ensuring data types, required fields, and constraints are met.

- **FR-016**: System MUST detect schema validation errors (missing fields, invalid types, constraint violations) and handle them gracefully, either requesting regeneration or returning clear error messages.

- **FR-017**: System MUST validate that structured requests conform to calculation service requirements before forwarding them, preventing invalid operations.

- **FR-018**: System MUST provide clear error messages when validation fails, enabling users to understand what went wrong and potentially rephrase their queries.

### Schema Validation Retry and Repair

- **FR-019**: System MUST retry schema validation failures up to 3 times before failing the request, using exponential backoff with initial delay 1 second, doubling on each retry (1s, 2s, 4s), maximum delay 4 seconds. Reference: `specs/001-master-spec/spec.md` CL-035.

- **FR-020**: System MUST implement repair logic including: type coercion (attempting to coerce invalid types to expected types when safe and unambiguous, e.g., string "123" → number 123), default values (applying default values for optional missing fields when reasonable defaults exist), and field name normalization (attempting to match similar field names with case-insensitive, underscore/hyphen normalization when exact match fails). Reference: `specs/001-master-spec/spec.md` CL-035.

- **FR-021**: System MUST request LLM to regenerate output with explicit error feedback about what failed validation if repair logic cannot fix the error. Reference: `specs/001-master-spec/spec.md` CL-035.

- **FR-022**: System MUST retry transient LLM errors (rate limits, timeouts), schema validation failures that can be repaired, and missing optional fields. System MUST fail fast for structural schema mismatches (completely wrong structure), invalid required fields that cannot be repaired, and security violations (malformed requests, injection attempts). Reference: `specs/001-master-spec/spec.md` CL-035.

- **FR-023**: System MUST return clear error messages to client indicating what validation failed and suggesting how user might rephrase their query when retries are exhausted. Error messages MUST NOT expose internal schema details or LLM provider information. When schema validation fails after all retry attempts are exhausted (3 retries with repair logic), the system MUST return 422 Unprocessable Entity error with clear user-friendly message suggesting query rephrasing, without exposing internal schema details. Reference: `specs/001-master-spec/spec.md` CL-035.

- **FR-024**: System MUST log all validation failures with error patterns, retry counts, and success/failure outcomes. Validation failure patterns MUST be tracked for system improvement. High validation failure rates MUST trigger alerts for investigation. Reference: `specs/001-master-spec/spec.md` CL-035.

### Model Vendor Routing

- **FR-025**: System MUST use OpenRouter for all LLM interactions, supporting both OpenRouter credits and BYOK (Bring Your Own Key) integration. System MUST support routing to multiple models via OpenRouter's unified API with configurable model selection logic.

- **FR-025A**: System MUST prefer models that do not train on prompts, using OpenRouter's data policy filtering features (see https://openrouter.ai/docs/features/privacy-and-logging). System MAY select models that train on prompts only if such selection would significantly compromise performance metrics (e.g., >20% degradation in accuracy/latency) or increase pricing by more than 50% compared to no-training models.

- **FR-026**: System MUST handle OpenRouter API failures gracefully, leveraging OpenRouter's automatic fallback capabilities or returning appropriate error messages. When an LLM provider (via OpenRouter) is unavailable or returns an error, the system MUST retry with exponential backoff up to 3 times (initial delay: 1s, doubling on each retry: 1s, 2s, 4s), then return structured error (503 Service Unavailable) with remediation guidance if all retries fail.

- **FR-027**: System MUST support prompt templating, enabling consistent prompt structure across different models via OpenRouter while maintaining flexibility.

- **FR-028**: System MUST enforce rate limiting per tenant, preventing abuse and managing costs. Rate limits may be managed by OpenRouter (when using OpenRouter credits) or by the underlying provider (when using BYOK).

### Stateless Architecture

- **FR-029**: System MUST operate as a stateless translator and router, not maintaining persistent state between requests (conversation context may be maintained by clients).

- **FR-030**: System MUST never determine financial outcomes or replace rule logic; LLMs only structure requests; rules and deterministic engine determine outcomes.

- **FR-031**: System MUST validate all LLM outputs that affect calculations against rules before execution, ensuring LLM outputs are checked before being used.

### Integration

- **FR-032**: System MUST transform natural language queries into structured calculation requests.

- **FR-033**: System MUST retrieve references for citation generation and context enhancement in conversational responses.

- **FR-034**: System MUST provide natural language processing for consumer queries with consumer-friendly formatting.

- **FR-035**: System MUST provide natural language processing for adviser queries with professional formatting.

### Access Requirements

- **FR-036**: System MUST provide intent parsing capability returning detected intent, extracted parameters, and next action, and conversational chat capability returning messages, tool calls, and citations.

- **FR-037**: System MUST enforce access control with tenant isolation and rate limits as specified in the master specification (see CL-031 and FR-030 for security guarantee that User A can NEVER see User B's data under ANY circumstances).

- **FR-037A**: System MUST include automated security tests that verify cross-tenant data access is impossible for all LLM Orchestrator endpoints. Tests MUST simulate bugs, misconfigured queries, malicious input, missing tenant context, and other failure scenarios to ensure User A cannot access User B's conversation history, extracted parameters, or LLM-generated content under any conditions (see FR-030A in master specification).

- **FR-038**: System MUST support idempotency for LLM requests where appropriate, enabling safe retries while managing LLM provider costs.

### RAG (Retrieval-Augmented Generation) Capability

- **FR-041**: System MUST retrieve relevant structured data (rules, references, assumptions, advice guidance, client outcome strategies) from the relational database via References & Research Engine APIs (`/references/search`, `/references/{id}`) to augment LLM prompts.

- **FR-042**: System MUST support semantic search or keyword-based queries on the relational database for retrieval, using existing PostgreSQL with JSONB for metadata (no new data stores required).

- **FR-043**: System MUST retrieve data respecting tenant isolation (RLS) and PII redaction, ensuring User A cannot access User B's data through RAG retrieval under any circumstances.

- **FR-044**: System MUST limit retrieval results to the most relevant items (e.g., top 5-10 results) using relevance scoring, preventing prompt bloat from excessive retrieved data.

- **FR-045**: System MUST handle cases where no relevant data is found gracefully, proceeding with standard LLM processing without RAG augmentation and logging retrieval failures for monitoring.

- **FR-046**: System MUST respect effective dates and ruleset versions when retrieving data, using appropriate `as_of` date context from user queries or conversation history.

### Prompt Augmentation

- **FR-047**: System MUST augment LLM prompts with retrieved structured data, integrating retrieved context into prompts for intent detection, parsing, and conversational responses.

- **FR-048**: System MUST format retrieved data appropriately for prompt augmentation, ensuring retrieved context is clear, relevant, and does not exceed LLM context limits.

- **FR-049**: System MUST prioritize retrieved authoritative data in prompt augmentation, but all outputs affecting calculations MUST still be validated against deterministic rules in the Compute Engine (LLM remains a translator; retrieved data grounds prompts but does not make LLM the source of truth).

- **FR-050**: System MUST include citations to retrieved sources in conversational responses, enabling users to verify information and building trust.

### RAG API Integration

- **FR-051**: System MUST enhance `/llm/parse` API to optionally include RAG via a `use_rag` flag in requests, enabling clients to opt-in to RAG-enhanced parsing.

- **FR-052**: System MUST enhance `/llm/chat` API to optionally include RAG via a `use_rag` flag in requests, enabling clients to opt-in to RAG-enhanced conversational responses.

- **FR-053**: System MUST add a new internal tool or step for retrieval, integrating RAG retrieval into the LLM Orchestrator workflow without disrupting existing functionality.

- **FR-054**: System MUST maintain backward compatibility: when `use_rag` is not specified or set to false, the system MUST operate without RAG augmentation, preserving existing behavior.

### RAG Model Routing and Performance

- **FR-055**: System MUST use cheaper models (e.g., gpt-5-mini) for retrieval queries, optimizing cost while maintaining retrieval quality.

- **FR-056**: System MUST switch to higher-capability models (e.g., gpt-5.1) for generation when needed, enabling intelligent model selection based on query complexity and requirements.

- **FR-057**: System MUST ensure retrieval adds less than 1 second latency (p95) to maintain acceptable response times, implementing caching and optimization strategies as needed.

- **FR-058**: System MUST cache frequent retrievals in Redis, reducing latency for common queries and improving performance.

### RAG Constitution Compliance

- **FR-059**: System MUST comply with Principle IV: LLM remains a translator only; retrieved data grounds prompts but does not make LLM the source of truth.

- **FR-060**: System MUST validate all outputs affecting calculations against deterministic rules in the Compute Engine, ensuring RAG-augmented prompts do not bypass rule validation.

- **FR-061**: System MUST ensure retrieved data is used for prompt augmentation only, not for direct calculation or decision-making, maintaining the separation between LLM translation and deterministic computation.

### RAG Privacy and Security

- **FR-062**: System MUST ensure retrieved data respects tenant isolation (RLS) at the database level, preventing cross-tenant data access in RAG retrieval.

- **FR-063**: System MUST ensure retrieved data respects PII redaction policies, preventing sensitive information from appearing in RAG-augmented prompts sent to external LLM providers.

- **FR-064**: System MUST log all RAG retrieval operations for audit purposes, including query terms, retrieved items, and relevance scores, while maintaining PII redaction in logs.

### RAG Testing and Quality

- **FR-065**: System MUST include unit tests for retrieval accuracy, ensuring 95% relevance for retrieved data when validated against manually curated test queries.

- **FR-066**: System MUST include integration tests for RAG functionality, testing end-to-end flows from user query through retrieval, prompt augmentation, and LLM response generation.

- **FR-067**: System MUST include end-to-end tests via Veris/Frankie's UIs, validating RAG functionality in real user scenarios.

- **FR-068**: System MUST include golden dataset validation, testing RAG retrieval against known-good query-result pairs to ensure consistency and accuracy.

- **FR-069**: System MUST include property-based tests for edge cases (e.g., no relevant data found, excessive results, conflicting data), ensuring robust handling of edge conditions.

---

## From Frankie's Finance Specification

### Spatial Navigation and Environments

- **FR-001**: System MUST provide five distinct environments: Path to the House (entry/onboarding), Front Door (transition), Living Room (conversation/reflection), Study (forecasting/scenarios), and Garden (goals/progress).

- **FR-002**: System MUST enable non-linear navigation where user questions dictate movement between environments, with Frankie guiding transitions through visual cues (wagging, running ahead, looking expectantly). When Frankie's visual cues aren't clear or users don't understand the navigation, the system MUST provide alternative navigation methods (menu/tabs), make Frankie cues optional, and support both navigation methods to ensure accessibility and usability.

- **FR-003**: System MUST support navigation by intent: when users ask questions about numbers or strategy, Frankie guides to the study; when users ask about goals or progress, Frankie guides to the garden; general questions remain in the living room.

- **FR-004**: System MUST provide smooth, fluid transitions between environments that feel natural and calming, avoiding abrupt scene cuts or jarring changes.

- **FR-005**: System MUST maintain persistent state in each environment: living room retains conversations and reflections, study remembers experiments and models, garden visually represents ongoing goals.

- **FR-006**: System MUST allow users to stay in an environment and reflect, or follow Frankie's lead to explore, giving users control over pace and depth of interaction.

### Frankie Companion

- **FR-007**: System MUST present Frankie as a companion guide (not the adviser) who provides emotional support, visual navigation cues, and warmth, while the app itself provides the advice voice.

- **FR-008**: System MUST provide Frankie behaviors that communicate meaning: wagging and running ahead ("Follow me"), tilting head or sitting ("I'm listening"), lying beside user ("You're safe here"), soft bark ("I found something interesting"), running in garden (celebration).

- **FR-009**: System MUST make Frankie's cues non-intrusive invitations rather than demands, allowing users to control when to follow Frankie's lead.

- **FR-010**: System MUST display Frankie in every environment, providing continuity and emotional grounding throughout the user's journey.

### Natural Language Interaction

- **FR-011**: System MUST support natural language queries via text or voice input, enabling users to ask questions conversationally without learning specific commands or syntax.

- **FR-012**: System MUST integrate with natural language processing services to process natural language queries and receive conversational responses with tool calls and citations.

- **FR-013**: System MUST maintain conversation context across multiple turns, understanding references to previous messages and maintaining coherent dialogue.

- **FR-014**: System MUST format conversational responses appropriately for consumers, using plain English, avoiding jargon, and explaining financial concepts in relatable language.

- **FR-015**: System MUST support both text and voice interaction modes, allowing users to choose their preferred method and switch seamlessly between modes.

### Financial Guidance and Advice

- **FR-016**: System MUST provide personalized financial guidance based on user questions, executing calculations and presenting results with visual forecasts, pros/cons, and long-term impacts.

- **FR-017**: System MUST validate all financial advice before presenting it to users, ensuring compliance with best interests duty and regulatory requirements.

- **FR-018**: System MUST display compliance validation results in consumer-friendly, non-technical language, explaining what validation means and any warnings or required actions without exposing technical details.

- **FR-019**: System MUST provide explainable insights for all recommendations, enabling users to understand why advice was given through traces linking to rules and references, presented in consumer-friendly language.

- **FR-020**: System MUST handle advice that cannot be provided (due to compliance failures or rule coverage gaps) gracefully, informing users supportively and suggesting consulting a licensed financial adviser when appropriate. When a user's financial question cannot be answered by existing rules or calculations (question falls outside current rule coverage), the system MUST display a supportive message explaining the limitation, suggest consulting a licensed adviser, and maintain a warm, non-judgmental tone throughout the interaction. When compliance validation fails and advice cannot be provided to a consumer (e.g., BLOCK violation detected), the system MUST display a consumer-friendly message explaining that advice cannot be provided, suggest consulting a licensed adviser, and maintain a supportive, non-alarming tone throughout the interaction.

### Scenario Exploration and Forecasting

- **FR-021**: System MUST enable scenario simulation ("what-if" analysis) allowing users to test different financial scenarios and compare outcomes side-by-side.

- **FR-022**: System MUST provide interactive forecasting tools (sliders, chat-driven prompts) that allow users to adjust parameters and see outcomes update in real-time.

- **FR-023**: System MUST present forecasts and scenarios visually with charts, graphs, and simple visualizations that make financial projections understandable without requiring technical expertise.

- **FR-024**: System MUST execute scenario calculations, retrieving results and explanations for display.

- **FR-025**: System MUST tag and store scenarios for future reference, enabling users to return to previous experiments and compare outcomes over time.

### Goal Setting and Tracking

- **FR-026**: System MUST enable users to set financial goals (buying a house, paying off debt, building super) with specific parameters (amount, timeline) through natural language or structured input. Users MUST be able to modify or delete goals after creation. When a goal is modified or deleted, the system MUST maintain history of the original goal, update the visual representation in the garden accordingly, and preserve progress tracking data for audit purposes.

- **FR-027**: System MUST display goals visually in the garden environment using metaphors (trees, flowers) that show progress and growth.

- **FR-028**: System MUST track goal progress over time, updating visual representations as users make progress toward their goals.

- **FR-029**: System MUST provide milestone reminders and celebrations, with Frankie visibly celebrating achievements and the garden environment brightening to reinforce progress.

- **FR-030**: System MUST adjust advice and goal projections when user circumstances change, showing how changes affect goal achievement.

### Progress Reports and Health Checks

- **FR-031**: System MUST generate periodic progress reports (monthly or quarterly) showing financial health evolution, goal progress, and risk indicators.

- **FR-032**: System MUST present progress reports using supportive, non-alarming language, explaining risks and improvements in ways that motivate rather than discourage users.

- **FR-033**: System MUST enable on-demand progress reports, allowing users to request financial health reviews at any time.

- **FR-034**: System MUST celebrate improvements and achievements in progress reports, reinforcing positive behaviors and providing motivation to continue.

### Visual Design and Emotion

- **FR-035**: System MUST use emotion-first design that calms, reassures, and empowers users, reducing shame and replacing fear with curiosity.

- **FR-036**: System MUST provide visual elements (lighting, sound, motion) that adjust to user tone and emotional state, creating a responsive, supportive environment.

- **FR-037**: System MUST present forecasts and explanations in organic ways (notes opening, sketches forming, charts glowing) that feel natural rather than mechanical.

- **FR-038**: System MUST maintain a warm, welcoming visual language throughout all environments, using colors, typography, and imagery that create a sense of safety and comfort.

### Mobile-First Experience

- **FR-039**: System MUST provide a mobile-first experience optimized for touch interaction, with Frankie's behaviors triggered by tapping when he becomes animated.

- **FR-040**: System MUST support offline capabilities where possible, allowing users to access previously loaded content and view progress even without connectivity.

- **FR-041**: System MUST handle connectivity issues gracefully, saving progress where possible and providing clear messaging about connectivity requirements. When a user loses connectivity during an active calculation or scenario exploration, the system MUST save progress, queue the request for retry when connectivity is restored, and display a clear offline indicator explaining what functionality is available offline versus what requires connectivity.

### Offline Capabilities and Sync

- **FR-042**: System MUST support offline access to previously loaded content (conversations, scenarios, goals, visualizations), view progress and goal tracking, access to cached API responses (via TanStack Query cache), and environment state persistence (path, front door, living room, study, garden). Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-043**: System MUST require connectivity for new calculations (`POST /run`, `POST /run-batch`), new natural language queries (`POST /llm/chat`), real-time scenario updates, and fresh compliance validation. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-044**: System MUST persist state using AsyncStorage for local state persistence, including environment state, conversations, scenarios, and goals. Backend is source of truth; AsyncStorage used for caching and offline access. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-045**: System MUST implement online-first architecture with offline caching, handling connectivity issues gracefully, saving progress where possible, and providing clear messaging about connectivity requirements. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-046**: System MUST automatically sync cached changes and refetch stale data when connectivity is restored, using TanStack Query automatic cache management and background refetching. Failed requests MUST be queued and retried on reconnect. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-047**: System MUST implement conflict resolution using last-write-wins strategy for simple state updates. For critical data (scenarios, calculations), system MUST validate with backend before applying local changes. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-048**: System MUST invalidate cache based on data freshness requirements: critical data (calculations, compliance) invalidated immediately; less critical data (conversations, goals) cached longer. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-049**: System MUST display clear offline indicators and messaging when connectivity is unavailable, informing users about what functionality is available offline vs. requires connectivity. Reference: `specs/001-master-spec/spec.md` CL-034.

---

## From Veris Finance Specification

### Professional Interface Design

- **FR-001**: System MUST provide a professional, calm interface with minimal chrome, clear hierarchy, and emphasis on data clarity, using cool neutrals (graphite, silver, blue accent) and crisp typography.

- **FR-002**: System MUST provide a data-centric UI optimized for visualizing strategies, forecasts, and comparisons with professional charts, graphs, and comparative dashboards.

- **FR-003**: System MUST display audit log always available, providing transparent record of all advice logic, calculations, compliance checks, and changes with timestamps and reasoning trails.

- **FR-004**: System MUST provide clean, two-column layouts for client summaries with icons and editable fields, enabling efficient data entry and review.

- **FR-005**: System MUST use consistent formatting for charts across time horizons with clear legends and callouts, maintaining professional presentation standards.

### LLM Chat Interface

- **FR-006**: System MUST provide an LLM-powered chat interface that understands natural adviser language, enabling advisers to input queries or client data via natural language.

- **FR-007**: System MUST integrate with natural language processing services for natural language processing, receiving conversational responses formatted for professional use.

- **FR-008**: System MUST format LLM responses with structured replies and clickable commands, enabling advisers to act on recommendations efficiently.

- **FR-009**: System MUST maintain conversation context for client scenarios, enabling natural dialogue while preserving professional tone and accuracy.

### Client Management

- **FR-010**: System MUST enable advisers to create and manage client records with demographics, goals, and financial data through natural language input or structured forms.

- **FR-011**: System MUST store client data and make it available for scenario modelling and future advice sessions, enabling efficient client relationship management.

- **FR-012**: System MUST support multiple clients per adviser, enabling advisers to work with multiple clients simultaneously without data confusion. When an adviser works with multiple clients simultaneously and needs to switch between client contexts, the system MUST provide a client switcher/context menu, maintain separate sessions per client with independent state, and enable quick switching without data loss or confusion.

- **FR-013**: System MUST allow advisers to import client data from external sources or enter it manually, supporting various data input methods.

### Scenario Modelling and Forecasting

- **FR-014**: System MUST enable advisers to create and manage multiple scenarios per client, allowing comparison of different strategies, assumptions, or outcomes.

- **FR-015**: System MUST execute scenario calculations, retrieving results and maintaining full provenance.

- **FR-016**: System MUST present forecasts with professional line charts, bar graphs, and scenario tabs, enabling clear visualization of outcomes and comparisons.

- **FR-017**: System MUST support sensitivity analysis and stress-testing, allowing advisers to vary assumptions and see how outcomes change.

- **FR-018**: System MUST display forecasts with expandable tiles showing assumptions, inputs, and results, enabling advisers to understand and verify calculations.

### Strategy Comparison

- **FR-019**: System MUST enable side-by-side comparison of multiple strategies or products, presenting comparative forecasts with clear visual differentiation.

- **FR-020**: System MUST highlight key differences between strategies, enabling advisers to explain why a recommended strategy serves the client's best interests.

- **FR-021**: System MUST support evidence-based recommendations by providing comparison data that demonstrates best-interests duty to clients and auditors.

### Compliance and Validation

- **FR-022**: System MUST integrate with compliance validation services for compliance validation and requirement retrieval.

- **FR-023**: System MUST display compliance validation results clearly, showing compliance status, warnings, and required actions with links to regulatory requirements.

- **FR-024**: System MUST prevent generation of advice documents when compliance validation fails, ensuring only compliant advice is documented. When compliance validation fails and an adviser attempts to generate an advice document (SOA/ROA), the system MUST block document generation, display compliance failures clearly with specific guidance on what needs to be addressed, and require resolution of compliance issues before allowing document generation.

- **FR-025**: System MUST incorporate compliance results into generated documents, ensuring documentation matches compliance status and includes required disclosures.

### Documentation Generation

- **FR-026**: System MUST generate Statement of Advice (SOA) and Record of Advice (ROA) automatically from client scenarios, including all calculations, compliance results, and recommendations.

- **FR-027**: System MUST include traceable explanations in generated documents, linking to authoritative references, rule versions, and calculation assumptions.

- **FR-028**: System MUST export documents in formats suitable for client presentation and regulatory submission, with full audit trails and compliance information.

- **FR-029**: System MUST ensure consistency between calculations, compliance results, and documentation, preventing discrepancies that could cause compliance issues.

- **FR-030**: System MUST generate print-ready PDFs using client-side browser print-to-PDF functionality with print-optimized CSS stylesheets, enabling professional document output suitable for client presentation and regulatory submission. Reference: `specs/001-master-spec/spec.md` CL-033.

- **FR-031**: System MUST provide SOA/ROA templates that include calculations, compliance results, recommendations, required disclosures, and traceable explanations linking to authoritative references, rule versions, and calculation assumptions. Reference: `specs/001-master-spec/spec.md` CL-033.

- **FR-032**: System MUST export evidence packs in both JSON (machine-readable) and PDF (human-readable) formats with version information, timestamps, and complete provenance chains. Reference: `specs/001-master-spec/spec.md` CL-033.

### Audit Trail and Explainability

- **FR-033**: System MUST maintain a transparent audit log showing all advice logic, calculations, compliance checks, and changes with timestamps and reasoning trails.

- **FR-034**: System MUST provide access to explanation capabilities, enabling advisers to retrieve human-readable provenance chains for any calculation result.

- **FR-035**: System MUST enable export of audit trails suitable for regulatory review, including complete provenance chains with all calculations, compliance results, and regulatory references. When an adviser exports a compliance pack but some required documentation is missing or incomplete, the system MUST generate a partial compliance pack with available items, clearly mark missing items in the export, and allow export with warnings indicating what documentation is missing or incomplete.

- **FR-036**: System MUST support time-travel queries, enabling advisers to review historical advice using ruleset versions applicable at that time.

### Performance and Efficiency

- **FR-037**: System MUST enable advisers to move from idea → input → output in seconds via chat interface, reducing time spent on data entry and technical calculations.

- **FR-038**: System MUST support fast scenario comparison, enabling advisers to model and compare multiple strategies efficiently without performance degradation.

- **FR-039**: System MUST provide quick access to client records and previous scenarios, enabling efficient workflow and reducing time spent searching for information.
