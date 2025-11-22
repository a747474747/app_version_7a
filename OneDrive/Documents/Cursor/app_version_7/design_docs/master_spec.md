# Master Specification: App Version 5 System

**Feature Branch**: `001-master-spec`  
**Created**: 2025-01-27  
**Status**: ✅ **Ready for Implementation**  
**Input**: Create the master spec with guidance from design documents where constitution is not clear

**Purpose**: This master specification serves as the single source of truth for the App Version 5 financial advice system. It defines user requirements, acceptance scenarios, and success criteria that can be validated through user testing. This specification is readable and validatable by non-technical stakeholders.

---

## User Scenarios & Testing

### User Story 1 - Consumer Financial Guidance (Priority: P1)

**Consumer Story**: An everyday Australian user opens Frankie's Finance on their mobile device seeking guidance on a financial question. They feel anxious about money decisions and need a safe, non-judgmental environment to explore options and understand recommendations.

**Why this priority**: This represents the primary consumer value proposition. The system must provide emotionally supportive, transparent financial guidance accessible to non-experts. Without this capability, the consumer-facing product cannot deliver value.

**Independent Test**: A user can ask "Should I contribute more to super?" and receive:
- A clear, jargon-free explanation
- A visual forecast showing different contribution scenarios
- Transparency on how the recommendation was calculated
- Compliance validation ensuring the advice meets professional standards
- The ability to explore follow-up questions without judgment

**Acceptance Scenarios**:

1. **Given** a user opens Frankie's Finance for the first time, **When** they interact with Frankie on the path, **Then** they are welcomed into the home environment (path → front door → living room/study/garden) and can ask questions naturally.

2. **Given** a user asks a financial question in the living room, **When** the system processes their intent, **Then** they receive a conversational response with underlying calculations executed, traceable explanations, and compliance validation ensuring the advice meets professional standards.

3. **Given** a user wants to explore "what-if" scenarios, **When** they follow Frankie to the study, **Then** they can view comparative forecasts, charts, and sensitivity analyses with full provenance linking back to rules and references, with compliance checks performed for each scenario.

4. **Given** a user receives financial advice, **When** they want to understand why a recommendation was made, **Then** they can access a human-readable explanation tracing Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions with versions and dates, and see compliance validation results indicating whether the advice meets best interests duty and regulatory requirements.

5. **Given** a user receives financial advice through Frankie's Finance, **When** the system evaluates the recommendation for compliance, **Then** any compliance warnings or required actions are displayed in a user-friendly, non-technical manner appropriate for consumers.

---

### User Story 2 - Adviser Professional Workflow (Priority: P1)

**Adviser Story**: A licensed financial adviser needs to quickly model client strategies, compare scenarios, and generate compliant documentation. They require professional tools that reduce administrative burden while maintaining auditability and compliance standards.

**Why this priority**: This represents the primary adviser value proposition. The system must enable efficient, compliant advice generation while preserving transparency and regulatory compliance. This is critical for professional adoption.

**Independent Test**: An adviser can enter client data via natural language ("Add client aged 42 with $450k super") or structured input, request strategy comparisons ("Compare debt-recycling vs offset-strategy over 10 years"), and export compliance documentation with full audit trails.

**Acceptance Scenarios**:

1. **Given** an adviser opens Veris Finance, **When** they input client information via chat or structured forms, **Then** the system stores client data and makes it available for scenario modelling and future advice sessions.

2. **Given** an adviser requests a strategy comparison, **When** they specify scenarios and assumptions, **Then** the system executes deterministic calculations, returns comparative forecasts, and maintains full provenance for audit purposes.

3. **Given** an adviser generates advice documentation, **When** they export compliance packs, **Then** all recommendations include traceable explanations linking to authoritative references, rule versions, and calculation assumptions.

4. **Given** an adviser needs to review past advice, **When** they query historical calculations, **Then** the system uses time-travel capabilities with `as_of` dates to reconstruct exact recommendations using the ruleset versions applicable at that time.

---

### User Story 3 - Partner Integration (Priority: P2)

**Partner Story**: A third-party financial services provider wants to integrate App Version 5's calculation engine and rule intelligence into their own platform. They need stable, well-documented interfaces that match internal capabilities.

**Why this priority**: Partner integrations expand the system's reach and create additional revenue streams. However, core consumer and adviser functionality must be stable before partner integrations can be reliably delivered.

**Independent Test**: A partner can submit calculation requests with client payloads, receive forecasts and comparisons, query active rules, and embed explainability traces in their own UI for transparency.

**Acceptance Scenarios**:

1. **Given** a partner has valid credentials, **When** they submit a calculation request with client data, scenario parameters, and pin `ruleset_id` and `as_of`, **Then** they receive deterministic calculation results identical to internal system calls with no logic forks.

2. **Given** a partner needs to understand which rules apply to a client situation, **When** they query active rules, **Then** they receive rule metadata including effective dates, precedence, and references without exposing internal implementation details.

3. **Given** a partner wants to surface explainability to their users, **When** they request explanation for a calculation result, **Then** they receive human-readable provenance chains suitable for embedding in their own interfaces.

---

### User Story 4 - Consumer PII Filtering Transparency (Frankie's Finance) (Priority: P1)

**Consumer Story**: A user opens Frankie's Finance for the first time and is asked to provide basic identifying information (name, date of birth, suburb) during initial setup. The app explains that this information will be used to personalize their experience, but that their name and any identifying information will be filtered out of requests sent to external AI services so that the information cannot be connected to them and they cannot be identified from their information. The app references its privacy policy for more details.

**Why this priority**: Privacy transparency is essential for building consumer trust, especially when dealing with financial information. Users need to understand how their data is protected before they feel comfortable using the service. This is a foundational trust-building element that must be present from the first interaction.

**Independent Test**: A new user can complete the initial setup flow, see a clear explanation of PII filtering, understand that their identifying information will not be sent to external AIs, and access the privacy policy—all before asking their first financial question.

**Acceptance Scenarios**:

1. **Given** a user opens Frankie's Finance for the first time, **When** they reach the initial setup screen, **Then** they are prompted to enter their name, date of birth, and suburb, with a clear explanation that this information helps personalize their experience.

2. **Given** a user enters their name, date of birth, and suburb during setup, **When** they submit this information, **Then** they see a privacy explanation screen that clearly states: "Your name and any identifying information about you will be filtered out of requests to external AIs so that your information is not connected to you and you cannot be identified from your information."

3. **Given** a user views the privacy explanation, **When** they want more details, **Then** they can access the app's privacy policy through a clear link or button, which explains the full privacy practices and compliance with Australian Privacy Act 1988.

4. **Given** the app has collected the user's full name during setup, **When** the user asks financial questions that might reference their name or other identifying information, **Then** the system uses the known name to more effectively filter PII from queries before sending to external LLM providers.

5. **Given** a user has completed setup and understands PII filtering, **When** they ask a financial question like "Should I contribute more to super?", **Then** they can use the service with confidence that their identifying information is protected, even if their query contains references to personal details.

---

### User Story 5 - Adviser PII Filtering Transparency (Veris Finance) (Priority: P1)

**Adviser Story**: A licensed financial adviser opens Veris Finance and enters client personal information during initial client setup. The system explains in detail how client PII is handled, how it complies with privacy regulations, and how the filtering process ensures that client identifying information is not sent to external LLM providers. The explanation is more detailed than the consumer version, appropriate for professional users who need to understand compliance requirements. The system references the same privacy policy used by Frankie's Finance.

**Why this priority**: Professional advisers have legal and ethical obligations to protect client information. They need detailed understanding of how the system handles PII to ensure compliance and to explain privacy practices to clients. This transparency is essential for professional adoption and regulatory compliance.

**Independent Test**: An adviser can complete client setup, view a detailed explanation of PII filtering and compliance, understand how client information is protected, and access the privacy policy—all before processing any client queries through the LLM system.

**Acceptance Scenarios**:

1. **Given** an adviser opens Veris Finance and begins setting up a new client, **When** they enter client personal information (name, date of birth, address, contact details, financial account numbers, TFN, etc.), **Then** the system collects this information with clear labels indicating what information is being collected and why.

2. **Given** an adviser enters comprehensive client PII during setup, **When** they complete the client setup, **Then** they see a detailed privacy explanation that covers: how client PII is handled, how the filtering process works, how it ensures client identifying information is not sent to external LLMs, and how this complies with Australian Privacy Act 1988 and professional obligations.

3. **Given** an adviser views the detailed privacy explanation, **When** they want more information, **Then** they can access the full privacy policy (same as Frankie's Finance) which provides comprehensive details about data handling, retention, security, and compliance.

4. **Given** the system has collected comprehensive client PII during setup, **When** the adviser processes client queries or scenarios, **Then** the system uses the known client information to more effectively filter PII from all queries before sending to external LLM providers, ensuring no client identifying information reaches external services.

5. **Given** an adviser understands the PII filtering process, **When** they process client scenarios or ask questions about client situations, **Then** they can use the service with confidence that client information is protected, and they can explain the privacy protections to clients if asked.

6. **Given** an adviser needs to explain privacy practices to a client, **When** they reference the system's privacy handling, **Then** they have access to clear, professional language they can use to explain how client information is protected when using the system.

---

### Edge Cases

- What happens when a user's question cannot be answered by existing rules? The system MUST gracefully indicate when questions fall outside current rule coverage and suggest consulting a human adviser.

- How does the system handle conflicts between rules at the same precedence level? Conflicts MUST be explicitly documented in the rule review workflow and resolved before publication; runtime conflicts MUST generate warnings.

- What happens when a calculation requires data that the user hasn't provided? The system MUST request missing parameters in a conversational, non-technical manner.

- How does the system handle time-travel queries for dates before rules existed? The system MUST either indicate no rules are applicable or use the earliest available ruleset with appropriate warnings.

- What happens when a partner request exceeds rate limits? The system MUST return appropriate rate-limit responses with clear retry guidance while maintaining tenant isolation.

- What happens when compliance validation identifies issues with advice provided through Frankie's Finance? The system MUST display warnings or required actions in consumer-friendly language, and may prevent presentation of non-compliant advice depending on severity.

- How does Frankie's Finance handle compliance validation failures? The system MUST gracefully handle validation failures, inform users that advice cannot be provided, and suggest consulting a licensed financial adviser when compliance cannot be assured.

- Can User A ever see User B's data, even in a bug or misconfigured query? User A MUST NEVER be able to see User B's data under ANY circumstances. The system MUST enforce this through multiple defense layers: database-level RLS policies, application-level tenant validation, automatic query filtering, and fail-safe error handling. If tenant isolation cannot be verified, the system MUST reject the request with an error rather than allowing access to any data. See CL-031 for detailed requirements.

- What happens when a user skips or cancels the initial setup? The system MUST still display privacy information before allowing any queries that might involve PII.

- How does the system handle users who want to update their privacy preferences or review what information has been collected? Users MUST be able to access their privacy settings and see what information is stored at any time.

- What happens if a user's query contains PII that wasn't collected during setup (e.g., a different name or identifier)? The system MUST still filter this information using pattern-based detection, even if it wasn't in the known PII list.

- How does the system handle advisers who enter incomplete client information? The privacy explanation MUST still be displayed, and the system MUST filter whatever PII is available.

- What happens when privacy policy updates occur? Users and advisers MUST be notified of significant changes and given the opportunity to review updated policies.

---

## Clarifications

This section addresses ambiguous areas in the specification to eliminate implementation uncertainty. Each clarification includes a proposed default answer and a decision status: [ACCEPT] (approved), [REJECT] (rejected, alternative needed), or [DISCUSS] (requires stakeholder review).

### Advice Engine Reasoning Capabilities

**CL-039**: What reasoning operations can Advice Engine perform on Facts it receives from Compute Engine, given that it "MUST NOT perform numeric calculations"?

**Answer**: Advice Engine MUST perform reasoning, suitability, and compliance evaluation using: interpretation logic based on Advice Guidance (e.g., "This is usually beneficial when...", "Preferable for clients who...", "Only valuable when balance exceeds...", "Not suitable if income unstable..."); behavioral-aware advice patterns (spending habits, biases, emotional patterns, mistakes, behavioral constraints); reasoning frameworks (problem → constraint → action → result, risk → structure → tax → behaviour → goal, prioritisation patterns, scenario comparison patterns, trade-off handling patterns); comparison and aggregation operations on Facts (e.g., comparing Fact values, summing Fact collections). Advice Engine MUST NOT perform numeric calculations that produce new Facts (all Facts must originate from Compute Engine), but it CAN apply reasoning frameworks and interpretation logic to existing Facts to generate advice outputs.

**Status**: [ACCEPT]

---

### Rule Precedence Ties

**CL-001**: When two or more rules at the same precedence level (e.g., two Regulations) conflict and both are effective for the same `as_of` date, which rule should be applied?

**Answer**: Rules at the same precedence level MUST be ordered by publication timestamp (earliest first), then by rule ID lexicographically. The system MUST find a solution using this ordering and record a WARNING in the output log. Rules MUST NOT be auto-resolved at runtime, but calculation MUST proceed with the selected rule and the warning recorded.

**Status**: [ACCEPT]

---

**CL-002**: Can a rule with lower precedence override a higher-precedence rule if it has a more recent effective date window?

**Proposed Answer**: No. Precedence hierarchy (Act > Regulation > Ruling > Guidance > Assumption) is absolute and MUST NOT be overridden by effective date windows. Effective date windows only determine applicability; precedence determines which rule applies when multiple applicable rules conflict.

**Status**: [ACCEPT]

---

**CL-003**: How should the system handle rules that have overlapping effective date windows but different precedence levels?

**Proposed Answer**: The rule with higher precedence MUST always apply, regardless of effective date windows. Effective date windows only filter which rules are considered; precedence resolves conflicts among applicable rules.

**Status**: [ACCEPT]

---

**CL-004**: When a rule is superseded by a new rule at the same precedence level, should the old rule remain queryable via time-travel for historical calculations?

**Proposed Answer**: Yes. Superseded rules MUST remain accessible with their original effective date windows preserved. Time-travel queries using `as_of` dates within the old rule's effective window MUST use the old rule, even if a newer rule exists at a later date.

**Status**: [ACCEPT]

---

**CL-005**: What happens when a rule references another rule that has been superseded or deleted?

**Proposed Answer**: Rule references MUST be versioned and immutable. If Rule A references Rule B at version v1, and Rule B is later updated to v2, Rule A's reference MUST continue pointing to Rule B v1. The system MUST validate referential integrity during rule publication and reject publications that reference non-existent rule versions.

**Status**: [ACCEPT]

---

### Rounding Policies by Field

**CL-006**: What rounding method should be applied to Australian dollar amounts (e.g., tax calculations, superannuation contributions)?

**Answer**: Australian dollar amounts MUST use ATO rounding rules: round to nearest cent using standard rounding (0.5 rounds up). All monetary values MUST be stored with appropriate precision. Rounding MUST occur at the final step of each calculation, not at intermediate steps, unless explicitly specified in the rule definition.

**Status**: [ACCEPT]

---

**CL-007**: Should percentage values (e.g., tax rates, contribution rates) be rounded, and if so, to how many decimal places?

**Proposed Answer**: Percentage values MUST NOT be rounded unless explicitly specified in the rule definition. They MUST be stored with sufficient precision and displayed with appropriate precision (typically 2 decimal places for rates, 4 decimal places for precise calculations). Rounding of percentages MUST only occur when specified in the rule (e.g., "round to nearest 0.1%").

**Status**: [ACCEPT]

---

**CL-008**: How should rounding be handled when multiple monetary values are summed (e.g., income components, tax offsets)?

**Proposed Answer**: Each component MUST be calculated to full precision, summed without intermediate rounding, then rounded once at the final total. The rule definition MUST specify whether rounding occurs per component or only at the total. If not specified, default to rounding only at the total.

**Status**: [ACCEPT]

---

**CL-009**: What rounding policy should apply to Transfer Balance Cap (TBC) and Total Super Balance (TSB) calculations?

**Answer**: TBC and TSB MUST use integer dollar rounding (round to nearest dollar, 0.5 rounds up) as per ATO requirements. These values MUST be stored as integer dollars and rounded at each calculation step, not only at the final value.

**Status**: [ACCEPT]

---

**CL-010**: Should rounding policies be configurable per rule, or should there be a system-wide default with rule-level overrides?

**Proposed Answer**: System MUST provide system-wide defaults (ATO rounding for dollars, no rounding for percentages unless specified) but MUST allow rule-level overrides. Each rule definition MUST explicitly specify its rounding policy in the rule metadata. If not specified, system defaults apply.

**Status**: [ACCEPT]

---

### Time-Travel / as_of Behavior

**CL-011**: When a user queries with an `as_of` date that falls between two ruleset publication dates, which ruleset should be used?

**Proposed Answer**: The system MUST use the most recent ruleset published on or before the `as_of` date. If `as_of=2024-06-15` and rulesets exist for `2024-05-01` and `2024-07-01`, the system MUST use `2024-05-01`. If no ruleset exists on or before the `as_of` date, the system MUST return an error indicating no applicable ruleset.

**Status**: [ACCEPT]

---

**CL-012**: Should `as_of` date queries support time-of-day granularity, or only date granularity?

**Proposed Answer**: `as_of` MUST support date-only granularity (YYYY-MM-DD) for MVP. Time-of-day granularity (YYYY-MM-DDTHH:MM:SS) MAY be supported in future versions but is out of scope for initial implementation. All `as_of` dates MUST be interpreted as end-of-day (23:59:59) for that date.

**Status**: [ACCEPT]

---

**CL-013**: When a rule's effective date window spans the `as_of` date but the ruleset containing that rule was published after the `as_of` date, should the rule be applied?

**Answer**: No. Rules MUST only be applied if they exist in a ruleset published on or before the `as_of` date. A rule cannot be retroactively applied to historical calculations. The system MUST validate that all rules in a ruleset have effective date windows that include or precede the ruleset publication date.

**Status**: [ACCEPT]

---

**CL-014**: How should the system handle `as_of` dates that fall before any ruleset exists in the system?

**Proposed Answer**: The system MUST return a structured error response with error code `NO_RULESET_FOR_DATE` and a message indicating the earliest available ruleset date. The error response MUST include remediation guidance suggesting the earliest available `as_of` date.

**Status**: [ACCEPT]

---

**CL-015**: When querying historical calculations, should assumptions (e.g., market rates, economic parameters) be time-traveled to their values at the `as_of` date, or use current assumptions?

**Proposed Answer**: Assumptions MUST be time-traveled to their snapshot values effective at the `as_of` date. Each assumption snapshot MUST include an effective date range. The system MUST use the assumption snapshot that was effective at the `as_of` date, not current assumptions. If no assumption snapshot exists for the `as_of` date, the system MUST return an error indicating missing assumptions.

**Status**: [ACCEPT]

---

### Scenario Idempotency

**CL-016**: If a user submits the same calculation request twice with identical `scenario_id`, `ruleset_id`, `as_of`, and input parameters, should the system return cached results or recalculate?

**Proposed Answer**: The system MUST return cached results if they exist and are valid. However, if the ruleset has been updated since the cached result was generated, the system MUST recalculate. The system MUST include a `cache_hit` boolean in the response and a `calculated_at` timestamp. Idempotency keys MUST be supported to ensure exactly-once semantics.

**Status**: [ACCEPT]

---

**CL-017**: Should scenario IDs be user-provided or system-generated? What happens if a user provides a duplicate scenario ID?

**Proposed Answer**: Scenario IDs MUST be user-provided. If a duplicate scenario ID is provided with different input parameters, the system MUST return a conflict error with error code `SCENARIO_ID_CONFLICT` and include the existing scenario's metadata. Users MUST use unique scenario IDs or update existing scenarios explicitly.

**Status**: [ACCEPT]

---

**CL-018**: Can a scenario be updated after initial calculation, or are scenarios immutable once created?

**Answer**: Scenarios CAN be modified multiple times after initial calculation. Users MAY update a scenario with new input parameters. Each time a scenario is modified, new calculations MUST be performed. The system MUST maintain version history of scenario changes and calculation results to ensure auditability and reproducibility. Historical calculation results MUST remain accessible even after scenario modifications.

**Status**: [ACCEPT]

---

**CL-019**: Should batch operations guarantee atomicity (all succeed or all fail) or allow partial success?

**Proposed Answer**: Batch operations MUST support partial success semantics. Each item in the batch MUST be processed independently. The response MUST include both successful results and errors for failed items. The system MUST NOT roll back successful calculations if some items in the batch fail.

**Status**: [ACCEPT]

---

**CL-020**: How long should scenario results be retained before automatic cleanup?

**Proposed Answer**: Scenario results MUST be retained for a minimum of 7 years per Australian regulatory requirements. The system MUST implement configurable retention policies per tenant, with a minimum of 7 years. Scenarios older than the retention period MAY be archived but MUST remain queryable for audit purposes.

**Status**: [ACCEPT]

---

### Privacy / PII Redaction

**CL-021**: Which fields are considered PII and must be redacted from logs and audit trails?

**Proposed Answer**: PII fields MUST include: full names, email addresses, phone numbers, residential addresses, tax file numbers (TFN), Australian Business Numbers (ABN), bank account numbers, credit card numbers, and any government-issued identification numbers. The system MUST maintain a configurable PII field list per tenant and redact these fields from all logs, except encrypted audit logs that require full data for regulatory compliance.

**Status**: [ACCEPT]

---

**CL-022**: Should PII redaction occur at the application layer or database layer?

**Proposed Answer**: PII redaction MUST occur at the application layer before data is written to logs. Database audit logs MAY contain encrypted PII for regulatory compliance, but application logs MUST be PII-minimal. The system MUST implement field-level redaction functions that can be applied to log entries and responses based on user permissions.

**Status**: [ACCEPT]

---

**CL-023**: How should the system handle PII in explanation requests when facts contain client-specific values?

**Answer**: Personally identifying information (PII) MUST be separated from the calculation engine. The calculation engine MUST operate on anonymized or pseudonymized data identifiers. PII MUST be stored separately and linked to calculations only through secure, permissioned access patterns. Explanation requests MUST return full provenance chains including calculated values using anonymized identifiers, with PII resolution handled by the requesting application based on user permissions and context.

**Status**: [ACCEPT]

---

**CL-024**: Should tenant isolation prevent PII leakage between tenants at the database query level, or only at the application API level?

**Proposed Answer**: Tenant isolation MUST be enforced at both the database query level AND at the application level. Database queries MUST automatically filter by tenant_id, and application logic MUST validate tenant context before processing requests. This defense-in-depth approach ensures PII cannot leak even if application logic has bugs. See CL-031 for the complete security guarantee that User A can NEVER see User B's data under any circumstances.

**Status**: [ACCEPT]

---

### Error Taxonomy

**CL-025**: What is the complete error taxonomy for system responses, and how should clients distinguish between retryable and non-retryable errors?

**Proposed Answer**: Error taxonomy MUST follow: 4xx for client errors (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 429 Too Many Requests), 5xx for server errors (500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout). All errors MUST include structured response: `{ error_code: string, message: string, remediation: string, retryable: boolean, retry_after_seconds?: number }`. 5xx errors (except 501 Not Implemented) are retryable; 4xx errors (except 429) are not retryable without client action.

**Status**: [ACCEPT]

---

### Advice Engine Blocking Rules

**CL-026**: What severity levels should Advice Engine use to classify compliance violations, and which levels should block advice presentation?

**Answer**: Advice Engine MUST classify violations as: `BLOCK` (advice MUST NOT be presented, calculation may proceed but result MUST NOT be shown to user), `WARNING` (advice MAY be presented with prominent warnings), `INFO` (informational compliance notes, advice may be presented normally). For Frankie's Finance (consumer), `BLOCK` violations MUST prevent advice presentation. For Veris Finance (adviser), `BLOCK` violations MUST be prominently displayed but advice MAY be shown for professional review.

**Status**: [ACCEPT]

---

**CL-027**: Should Advice Engine blocking rules be configurable per tenant, or system-wide?

**Answer**: Advice Engine blocking rules MUST be system-wide and based on regulatory requirements (Corporations Act 2001, Code of Ethics). However, the severity classification (BLOCK vs WARNING) for specific violation types MAY be configurable per tenant for Veris Finance advisers, with system-wide defaults. Frankie's Finance MUST always use system-wide BLOCK rules with no tenant overrides.

**Status**: [ACCEPT]

---

**CL-028**: When Advice Engine identifies a BLOCK violation, should the underlying calculation still be executed and stored, or should calculation be prevented?

**Proposed Answer**: Calculation MUST still be executed and stored (for audit purposes), but the result MUST NOT be returned to the requesting client application. The system MUST log the BLOCK violation with full context. For Frankie's Finance, the user MUST receive a consumer-friendly message explaining that advice cannot be provided and suggesting consultation with a licensed adviser. For Veris Finance, advisers MUST see the calculation results alongside BLOCK violations for professional review.

**Status**: [ACCEPT]

---

**CL-029**: How should Advice Engine handle partial compliance (e.g., some recommendations pass, others fail)?

**Proposed Answer**: Advice Engine MUST evaluate each recommendation independently and return per-recommendation compliance results. If any recommendation has a BLOCK violation, that specific recommendation MUST NOT be presented, but other compliant recommendations MAY be shown. The response MUST include a summary indicating overall compliance status and per-recommendation details.

**Status**: [ACCEPT]

---

**CL-030**: Should Advice Engine blocking rules be versioned alongside rulesets, or maintained independently?

**Answer**: Advice Engine rules MUST be entirely separate from calculation rules. They MUST be versioned independently with their own versioning scheme and lifecycle. Advice Engine evaluations MUST be pinned to both a `ruleset_id` (for calculation rules) and an `advice_ruleset_id` (for compliance rules) to ensure reproducibility. The system MUST support time-travel queries for both rule types independently. Advice Engine rules MUST NOT be included in calculation rulesets.

**Status**: [ACCEPT]

---

### Data Isolation Security Guarantee

**CL-031**: Can User A ever see User B's data — even in a bug or misconfigured query?

**Proposed Answer**: User A MUST NEVER be able to see User B's data under ANY circumstances, including:
- Application logic bugs or errors
- Misconfigured database queries
- SQL injection attempts or other security vulnerabilities
- Database-level misconfigurations or RLS policy failures
- API endpoint bugs or missing validation
- Race conditions or concurrency issues
- System errors, exceptions, or crashes
- Developer mistakes or accidental code changes

The system MUST enforce this guarantee through multiple defense layers:
1. **Database-level enforcement**: Row-Level Security (RLS) policies MUST be enforced at the PostgreSQL database level, preventing any query from accessing data outside the authenticated user's tenant context, even if application code fails to filter correctly.
2. **Application-level validation**: All API endpoints MUST validate tenant context before processing requests and MUST reject requests that attempt to access data outside the authenticated user's tenant.
3. **Query construction safeguards**: All database queries MUST automatically include tenant_id filtering through middleware or query builders that cannot be bypassed.
4. **Security testing**: The system MUST include automated security tests that verify cross-tenant data access is impossible, including tests that simulate bugs, misconfigured queries, and malicious input.
5. **Fail-safe behavior**: If tenant isolation cannot be verified (e.g., tenant context is missing or invalid), the system MUST reject the request with an error rather than allowing access to any data.

This is a non-negotiable security requirement. Any implementation that allows User A to see User B's data under any circumstances is a critical security failure that MUST be prevented and tested.

**Status**: [ACCEPT]

---

### Authentication Flows

**CL-032**: What are the authentication flows for web and mobile, including token lifetimes and rotation strategy?

**Answer**: 
- **Web (Veris Finance)**: OAuth2 Authorization Code flow with PKCE. Refresh tokens stored in HTTP-only, Secure, SameSite=Strict cookies. Access tokens: 15 minutes lifetime. Refresh tokens: 7 days lifetime, rotated on every use.
- **Mobile (Frankie's Finance)**: OAuth2 Authorization Code flow with PKCE. Refresh tokens stored in device SecureStore (iOS Keychain/Android Keystore). Access tokens: 15 minutes lifetime. Refresh tokens: 7 days lifetime, rotated on every use.
- **Token lifetimes and rotation**: Access tokens: 15 minutes maximum lifetime. Refresh tokens: 7 days maximum lifetime. Refresh tokens rotated on every use (new token issued, old token invalidated immediately).

**Status**: [ACCEPT]

---

### Frontend Architecture

**CL-033**: How does Veris Finance generate print-ready PDFs for SOA and compliance packs?

**Proposed Answer**: 
- **PDF Generation Approach**: Client-side generation using browser print-to-PDF functionality with print-optimized CSS stylesheets. Next.js provides print-ready CSS capabilities suitable for desktop-first design and print workflows.
- **SOA/ROA Templates**: Statement of Advice (SOA) and Record of Advice (ROA) generation automated from client scenarios. Templates include calculations, compliance results, recommendations, required disclosures, and traceable explanations linking to authoritative references, rule versions, and calculation assumptions.
- **Export Formats**: Documents exported in formats suitable for client presentation and regulatory submission (PDF, print-ready formats). Evidence packs exported in both JSON (machine-readable) and PDF (human-readable) formats with version information, timestamps, and complete provenance chains.
- **Consistency**: System ensures consistency between calculations, compliance results, and documentation. All generated documents include full audit trails suitable for compliance packs.

**Status**: [ACCEPT]

---

**CL-034**: What offline capabilities does Frankie's Finance support and how does it sync?

**Proposed Answer**:
- **Offline Capabilities**:
  - **What works offline**: Previously loaded content (conversations, scenarios, goals, visualizations), view progress and goal tracking, access to cached API responses (via TanStack Query cache), environment state persistence (path, front door, living room, study, garden).
  - **What requires connectivity**: New calculations (`POST /run`, `POST /run-batch`), new natural language queries (`POST /llm/chat`), real-time scenario updates, fresh compliance validation.
- **State Persistence**: AsyncStorage for local state persistence. Persisted state includes environment state, conversations, scenarios, goals. Backend is source of truth; AsyncStorage used for caching and offline access. No local database required for MVP.
- **Sync Strategy**: 
  - **Architecture**: Online-first architecture with offline caching. System handles connectivity issues gracefully, saving progress where possible and providing clear messaging about connectivity requirements.
  - **API Caching**: TanStack Query provides automatic cache management and background refetching when connectivity is restored.
  - **Sync on Reconnect**: When connectivity is restored, system automatically syncs cached changes and refetches stale data. Failed requests are queued and retried on reconnect.
  - **Conflict Resolution**: Last-write-wins strategy for simple state updates. For critical data (scenarios, calculations), system validates with backend before applying local changes.
  - **Cache Invalidation**: Cache invalidated based on data freshness requirements. Critical data (calculations, compliance) invalidated immediately; less critical data (conversations, goals) cached longer.
  - **Offline UI Indicators**: System displays clear offline indicators and messaging when connectivity is unavailable. Users informed about what functionality is available offline vs. requires connectivity.

**Status**: [ACCEPT]

---

### LLM/AI Use

**CL-035**: What is the retry and repair strategy when LLM outputs fail schema validation?

**Proposed Answer**:
- **Maximum Retry Attempts**: System MUST retry schema validation failures up to 3 times before failing the request.
- **Retry Backoff Strategy**: Exponential backoff with initial delay 1 second, doubling on each retry (1s, 2s, 4s), maximum delay 4 seconds.
- **Repair Logic**: 
  - **Type Coercion**: System attempts to coerce invalid types to expected types (e.g., string "123" → number 123) when safe and unambiguous.
  - **Default Values**: System applies default values for optional missing fields when reasonable defaults exist.
  - **Field Name Normalization**: System attempts to match similar field names (case-insensitive, underscore/hyphen normalization) when exact match fails.
  - **LLM Regeneration**: If repair logic cannot fix the error, system requests LLM to regenerate the output with explicit error feedback about what failed validation.
- **When to Retry vs. Fail Fast**: 
  - **Retry**: Transient LLM errors (rate limits, timeouts), schema validation failures that can be repaired, missing optional fields.
  - **Fail Fast**: Structural schema mismatches (completely wrong structure), invalid required fields that cannot be repaired, security violations (malformed requests, injection attempts).
- **Error Message Format**: When retries exhausted, system returns clear error messages to client indicating what validation failed and suggesting how user might rephrase their query. Error messages MUST NOT expose internal schema details or LLM provider/OpenRouter information.
- **Logging and Monitoring**: System logs all validation failures with error patterns, retry counts, and success/failure outcomes. Validation failure patterns tracked for system improvement. High validation failure rates trigger alerts for investigation.

**Status**: [ACCEPT]

---

### CI/CD & Environments

**CL-036**: What preview environments are set up for PRs (Vercel preview, Render staging, Expo preview)?

**Proposed Answer**:
- **Vercel Preview (Web - Veris Finance)**: YES - Vercel preview deployments automatically created for all pull requests. Preview URLs generated and posted as PR comments. Preview environments use separate environment variables and connect to staging database. Preview deployments automatically cleaned up when PR is merged or closed.
- **Render Staging (API)**: YES - Render staging environment configured for backend API previews. PRs trigger staging deployments with separate staging database. Staging environment uses staging database (isolated from production). Staging deployments automatically cleaned up after PR merge/close or after configurable retention period (default: 7 days).
- **Expo Preview (Mobile - Frankie's Finance)**: YES - Expo EAS preview builds generated for pull requests. Preview builds generate QR codes posted as PR comments for easy mobile testing. Preview builds use staging API endpoints and staging configuration. Preview builds automatically cleaned up after PR merge/close or after configurable retention period (default: 14 days).
- **Preview Environment Data Isolation**: All preview environments use separate databases with no production data. Preview environments use staging/test data sets. Preview environment cleanup ensures no data leakage between PRs or to production.
- **Preview Environment Configuration**: Preview environments use environment-specific configuration (staging API keys, staging database URLs, OpenRouter API keys, OpenAI API keys for BYOK). Configuration managed via platform-specific environment variable systems (Vercel Environment Variables, Render Environment Variables, Expo EAS Environment Variables).

**Status**: [ACCEPT]

---

**CL-037**: How do we roll back bad rulesets or database migrations?

**Proposed Answer**:
- **Ruleset Rollback**:
  - **Snapshot Rollback on Validation Failure**: If ruleset validation fails during Publish → Validate → Activate workflow, snapshot creation is automatically rolled back. Rollback implemented in `backend/compute-engine/src/storage/snapshot_rollback.py`. Rollback occurs if validation fails (integrity checks, consistency checks, referential integrity).
  - **Activated Ruleset Rollback**: System MUST support deactivation of activated rulesets and reversion to previous ruleset version. Rollback procedure:
    1. Deactivate current ruleset (mark as `Superseded` with `valid_to` timestamp)
    2. Reactivate previous ruleset version (mark as `Published` with `valid_to` set to NULL)
    3. Update ruleset references to point to previous version
    4. System continues to support time-travel queries for rolled-back ruleset (historical queries can still access it)
    5. Impact on existing Facts: Existing Facts created with rolled-back ruleset remain valid and queryable. New calculations use reactivated previous ruleset.
  - **Rollback API**: System provides API endpoint for ruleset rollback: `POST /api/v1/rulesets/{ruleset_id}/rollback` with `target_ruleset_id` parameter. Rollback requires admin privileges and generates audit log entry.
  - **Rollback Testing**: Rollback procedures MUST be tested before production deployment. Test rollback scenarios included in test suite.
- **Migration Rollback**:
  - **Alembic Down Migrations**: System uses Alembic migrations framework with support for down migrations (reversible migrations). All migrations MUST include both `upgrade()` and `downgrade()` functions.
  - **Migration Rollback Procedure**: 
    1. Identify target migration version to rollback to
    2. Run `alembic downgrade <target_version>` to execute down migrations
    3. Verify database schema matches target version
    4. Test application functionality with rolled-back schema
  - **Data Migration Rollback**: For data migrations (not just schema changes), rollback procedure MUST include data restoration steps. System maintains backup/export of data before data migrations. Rollback includes data restoration from backup if needed.
  - **Migration Conflict Resolution**: System detects migration conflicts (multiple developers creating migrations simultaneously). Conflict resolution requires manual intervention and coordination. Migration versioning uses timestamp-based sequential numbering to minimize conflicts.
  - **Rollback Testing**: All migrations MUST be tested with rollback procedures before production deployment. Test suite includes rollback tests for each migration.
  - **Rollback Monitoring**: System logs all migration rollbacks with timestamps, target versions, and reasons. Rollback frequency tracked and alerts triggered for frequent rollbacks.

**Status**: [ACCEPT]

---

### Authentication Flows

**CL-038**: What authentication flows are implemented for web (Veris Finance) and mobile (Frankie's Finance) clients, including token lifetimes and rotation strategy?

**Answer**: System MUST implement OAuth2 Authorization Code flow with PKCE (Proof Key for Code Exchange) for both web and mobile clients. 

**Web Authentication (Veris Finance)**:
- OAuth2 Authorization Code flow with PKCE: generates code verifier and challenge, redirects to authorization server
- Token exchange: exchanges authorization code for tokens using PKCE verifier, receives access and refresh tokens
- Refresh token storage: stored in HTTP-only, Secure, SameSite=Strict cookies to prevent XSS and CSRF attacks
- Automatic token refresh: expired access tokens automatically refreshed using refresh token cookie without user interaction
- Token rotation: refresh tokens rotated on every use (new refresh token issued, old one invalidated) to prevent token reuse attacks

**Mobile Authentication (Frankie's Finance)**:
- OAuth2 Authorization Code flow with PKCE: generates code verifier and challenge, opens secure browser/webview for authorization
- Token exchange: exchanges authorization code for tokens using PKCE verifier, receives access and refresh tokens
- Refresh token storage: stored securely in device SecureStore (iOS Keychain or Android Keystore) with appropriate access controls and encryption
- Automatic token refresh: expired access tokens automatically refreshed using refresh token from SecureStore without user interaction
- Token rotation: refresh tokens rotated on every use (new refresh token issued, stored in SecureStore, old one invalidated) to prevent token reuse attacks
- Session persistence: app checks SecureStore for valid refresh token on launch, automatically refreshes access token if valid, or prompts for re-authentication if expired

**Token Security**:
- Access token lifetime: maximum 15 minutes to minimize exposure window if tokens are compromised
- Refresh token lifetime: maximum 7 days to balance security and user experience, requiring periodic re-authentication
- Token rotation: refresh tokens MUST be rotated on every use (new refresh token issued, old refresh token invalidated immediately)
- Token reuse prevention: after a refresh token is used, it MUST be immediately invalidated and cannot be reused, even if the new refresh token is not yet received by the client
- Concurrent refresh handling: if multiple refresh attempts occur with the same token, only the first MUST succeed, and subsequent attempts MUST be rejected
- Token revocation: users MUST be able to revoke their own tokens, and administrators MUST be able to revoke tokens for security incidents
- Clock skew tolerance: token expiration validation MUST allow reasonable clock skew tolerance (±5 minutes) to prevent false rejections

**Session Management**:
- Multiple concurrent sessions: system MUST support multiple concurrent sessions per user (up to 5 devices) with each session maintaining independent refresh tokens
- Session tracking: each session tracked with device/browser identifier, creation time, last activity time, and revocation status
- Session revocation: users MUST be able to view and revoke active sessions from account settings
- Device-specific revocation: system MUST support device-specific token invalidation for lost or stolen devices

**Security Features**:
- PKCE validation: system MUST validate PKCE code verifier matches the code challenge during token exchange, rejecting mismatched verifiers
- Rate limiting: system MUST enforce rate limiting on authentication endpoints (5 failed authentication attempts per minute per IP/user) to prevent brute force attacks and token enumeration
- Error messages: system MUST provide clear error messages for authentication failures (invalid credentials, expired tokens, revoked tokens) without leaking sensitive information about account existence or token validity
- Network failure handling: system MUST gracefully handle network errors during token refresh, retry with exponential backoff, and prompt for re-authentication if refresh fails after maximum retries
- Storage failure handling: system MUST handle token storage failures (e.g., SecureStore unavailable) gracefully, prompt user to retry, and fall back to requiring re-authentication if storage cannot be accessed

**Audit and Compliance**:
- Authentication event logging: system MUST log all authentication events (login, token refresh, token revocation, failed authentication attempts) with timestamps, user identifiers, and device/browser information for security auditing and compliance
- Tenant context: access tokens MUST include tenant context to enable tenant isolation enforcement at the API layer

**Note**: Authentication flows requirements integrated into master spec (previously `specs/001-auth-flows/spec_001_auth_flows.md`)

**Status**: [ACCEPT]

---

### Observability & Operations

**CL-041**: Where are traces and metrics sent for observability? What observability backend is used?

**Proposed Answer**: 
- **Traces**: OpenTelemetry traces sent to OpenTelemetry Collector (deployed on Render or cloud provider), which exports to observability backend. For MVP, traces can be exported to console/stdout for development, with production export to cloud observability service (e.g., Grafana Cloud, Datadog, or Render's built-in observability) based on cost and requirements.
- **Metrics**: Prometheus metrics collected locally and scraped by Prometheus server (deployed on Render or cloud provider). Metrics can be exported to Grafana for visualization or cloud metrics service. For MVP, metrics can be exposed via `/metrics` endpoint and scraped by monitoring service.
- **Logs**: Structured JSON logs written to stdout/stderr, collected by Render's log aggregation (Render automatically collects stdout/stderr logs). Logs can be forwarded to external log aggregation service (e.g., Logtail, Datadog Logs) if needed for advanced analysis.
- **Error Tracking**: Sentry (free tier) cloud service for error monitoring and alerting.
- **Observability Backend**: For MVP, use Render's built-in monitoring and logging capabilities. For production, consider cloud observability service (Grafana Cloud, Datadog, or similar) based on cost and feature requirements. System MUST support exporting traces/metrics/logs to external observability backends for production use.

**Status**: [ACCEPT]

---

**CL-042**: What are the LLM cost caps and budget alerts?

**Proposed Answer**:
- **LLM Cost Caps**: System MUST implement configurable LLM cost caps per tenant and per time period (daily, weekly, monthly). Default cost cap: $100/month per tenant for MVP. Cost caps configurable per tenant via admin interface.
- **Budget Alerts**: System MUST alert when LLM costs exceed 80% of cost cap (warning alert) and 100% of cost cap (critical alert). Alerts sent to tenant administrators and system operators. When cost cap reached, system MUST reject new LLM requests for that tenant until cap is increased or reset.
- **Cost Tracking**: System tracks LLM costs per tenant, per model, and per time period. Cost tracking includes token usage (input/output/cached), model pricing, and total cost per request. Cost data stored in database for reporting and analysis.
- **Cost Reporting**: System provides cost reports per tenant showing token usage, model usage, and costs by time period. Reports accessible via admin interface or API.
- **Cost Optimization**: System uses intelligent model selection (cheaper models for cost-effective tasks) and cached input pricing (10x cost savings) to minimize costs while maintaining quality.

**Status**: [ACCEPT]

---

**CL-043**: What are the infrastructure cost caps and budget alerts?

**Proposed Answer**:
- **Infrastructure Cost Caps**: System MUST implement configurable infrastructure cost caps per environment (staging, production). Default cost cap: $100/month for MVP (allows ~40% buffer above baseline $70/mo). Cost caps configurable via infrastructure configuration.
- **Budget Alerts**: System MUST alert when infrastructure costs exceed 80% of cost cap (warning alert) and 100% of cost cap (critical alert). Alerts sent to system operators. When cost cap reached, system MUST prevent new deployments or scale-down non-critical services to stay within budget.
- **Cost Tracking**: Infrastructure costs tracked via platform dashboards (Render, Vercel, Expo EAS). System aggregates costs from all platforms and tracks total infrastructure spend. Cost data stored for reporting and analysis.
- **Cost Monitoring**: System monitors infrastructure costs daily and provides cost reports showing spend by platform, service, and time period. Reports accessible via admin interface or monitoring dashboard.
- **Cost Optimization**: System uses cost-effective platforms (Render Sydney $21/mo, Vercel Pro $20/mo, Expo EAS Pro $29/mo) and optimizes resource usage (connection pooling, caching, efficient deployments) to minimize costs.

**Status**: [ACCEPT]

---

## Requirements

### Functional Requirements

#### System Architecture

- **FR-001**: System MUST maintain six distinct modules with clear boundaries: Frankie's Finance (Consumer UX), Veris Finance (Adviser UX), LLM Orchestrator, Compute Engine, References & Research Engine, and Advice Engine.

- **FR-002**: System MUST use relational database-only architecture (no graph databases) for all data storage including canonical governance (rule definitions, effective windows, precedence, review workflow, assumptions snapshots, change logs), execution data (scenarios, facts, provenance links), and explainability (provenance chains, relationship storage, time-travel queries).

- **FR-003**: System MUST enforce the Publish → Validate → Activate workflow: rules authored as versioned artifacts (Markdown/YAML), published as `ruleset-YYYYMMDD` snapshots in relational database, validated for integrity and consistency, then activated and made available for computation.

- **FR-004**: System MUST forbid direct hand-editing of rules in the database; all rule changes MUST originate from versioned artifacts and follow the Publish → Validate → Activate workflow.

#### Architectural Component Boundaries

- **FR-004A**: **Compute Engine** MUST be the single source of truth for all deterministic financial logic, including tax formulas, caps, thresholds, eligibility tests, and projections. Compute Engine MUST NOT perform judgement, advice, or free-text reasoning, and MUST NOT store or serve knowledge objects (References, Rules, Assumptions, Advice Guidance, Strategies).

- **FR-004B**: **References & Research Engine** MUST be the single source of truth for all knowledge storage and retrieval, including REFERENCES, RULES, ASSUMPTIONS, ADVICE GUIDANCE, CLIENT OUTCOME STRATEGIES, FINDINGS, RESEARCH QUESTIONS, and VERDICTS. References & Research Engine MUST NOT perform numeric calculations, execute rules, generate personalised advice, or scrape raw documents.

- **FR-004C**: **Advice Engine** MUST consume Facts from Compute Engine (never calculate them) and knowledge objects from References & Research Engine (never store them). Advice Engine MUST focus on reasoning, suitability, and compliance evaluation. **Reasoning capabilities are defined in CL-039** and include: interpretation logic based on Advice Guidance (e.g., "This is usually beneficial when...", "Preferable for clients who...", "Only valuable when balance exceeds...", "Not suitable if income unstable..."); behavioral-aware advice patterns (spending habits, biases, emotional patterns, mistakes, behavioral constraints); reasoning frameworks (problem → constraint → action → result, risk → structure → tax → behaviour → goal, prioritisation patterns, scenario comparison patterns, trade-off handling patterns); comparison and aggregation operations on Facts (e.g., comparing Fact values, summing Fact collections). Advice Engine MUST NOT define tax formulas, perform numeric calculations that produce new Facts, scrape raw documents, store knowledge objects, or override deterministic outputs from Compute Engine.

- **FR-004D**: **LLM Orchestrator** MUST be a thin natural-language router that interprets user input, builds structured requests for the three engines, calls them in sequence, validates/repairs schemas, and turns outputs back into user-facing text. LLM Orchestrator MUST NOT invent rules, perform calculations, override deterministic outputs, store knowledge objects, or contain business logic.

#### Deterministic Calculations

- **FR-005**: System MUST ensure all financial calculations are deterministic and reproducible: same inputs + same `ruleset_id` + same `as_of` date MUST produce identical outputs.

- **FR-006**: System MUST pin every compute operation to explicit `ruleset_id` and `as_of` date parameters.

- **FR-007**: System MUST make all numeric tolerances and rounding standards explicit in rule definitions.

- **FR-008**: System MUST treat all computed Facts as immutable with full provenance (rule versions, inputs hash, scenario id, units, rounding).

- **FR-007A**: System MUST use fixed-point Decimal or integer cents for all monetary values; binary floating-point arithmetic is FORBIDDEN for financial calculations.

- **FR-007B**: System MUST enforce explicit units and dimensional checks for all calculations (%, basis points, dollars, years, etc.) with validation to prevent unit mismatches.

- **FR-007C**: System MUST specify rounding policy per field (ATO rules, bankers rounding vs away-from-zero) and when rounding occurs (at each step vs at end of calculation) in rule definitions.

#### Provenance and Explainability

- **FR-009**: System MUST provide end-to-end provenance for every computed result (Fact) traceable through explanation requests.

- **FR-010**: System MUST link provenance chains in the format: **Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions** with versions and dates.

- **FR-010A**: System MUST include per-fact provenance details: inputs hash, rules applied (with versions), references cited, assumptions snapshot (with versions), and rounding steps applied.

- **FR-010B**: System MUST provide stable anchors/IDs for citations enabling reproducible reference links even after reference updates.

- **FR-010C**: System MUST export evidence packs in both JSON and PDF formats with version information, timestamps, and complete provenance chains.

- **FR-011**: System MUST support time-travel queries using effective dates and ruleset versions to reconstruct historical calculations.

- **FR-012**: System MUST export all recommendations with full provenance chains suitable for compliance packs.

#### LLM Orchestration

- **FR-013**: System MUST use LLM Orchestrator as a stateless translator that converts natural language intent into structured compute requests; LLMs MUST NEVER determine financial outcomes or replace rule logic.

- **FR-014**: System MUST validate all LLM outputs that affect calculations against rules before execution.

- **FR-015**: System MUST provide natural language parsing that returns intent, parameters, and next action, and conversational chat that returns messages, tool calls, and citations.

#### Rule Management

- **FR-016**: System MUST enforce two-person review (four-eyes principle) before rule publication.

- **FR-017**: System MUST maintain rule precedence hierarchy: Act > Regulation > Ruling > Guidance > Assumption, with strict enforcement of effective date windows.

- **FR-018**: System MUST resolve rule conflicts explicitly through review workflow when rules at the same precedence level conflict.

- **FR-019**: System MUST store all rules as structured artifacts (Markdown/YAML) with schema validation, tests, examples, edge cases, narrative summaries, version tags, and effective date windows.

#### Data Extraction

- **FR-020**: System MUST extract and maintain five core data types: REFERENCES (legal/regulatory sources), RULES (calculation and taxation rules), ASSUMPTIONS (financial parameters), ADVICE GUIDANCE (professional standards), and CLIENT OUTCOME STRATEGIES (actionable planning approaches).

- **FR-021**: System MUST maintain data extraction quality standards: completeness (all relevant instances), accuracy (exact values from sources), context (narrative summaries), traceability (link to sources), consistency (standardized formats), and currency (effective dates and versions).

#### Schema Evolution and Feedback

- **FR-SCHEMA-01**: Compute Engine and Advice Engine implementations MAY emit structured schema-feedback requests when a missing field, relationship, or canonical mapping blocks correct implementation.

- **FR-SCHEMA-02**: The References & Research Engine MUST treat schema-feedback as a first-class refinement type (equal priority to missing content) and update canonical_data_model.md, schema definitions, and DB migrations accordingly before relevant freezes.

- **FR-SCHEMA-03**: Post-Freeze A, only non-breaking schema changes are permitted without a major version bump (see SCHEMA_EVOLUTION_POLICY.md).

- **FR-SCHEMA-REHEARSAL**: **Schema Dress Rehearsal** MUST be completed before Freeze A is declared. This involves implementing four real end-to-end golden calculations (PAYG marginal tax 2024–25 + offsets, CGT discount event, super contributions + Div 293, negative gearing mortgage interest) using the actual PostgreSQL + SQLAlchemy models generated from research. Every schema friction point (missing relation requiring >2 joins, awkward join patterns requiring >3 table joins, missing provenance role preventing complete chain construction, excessive JSONB usage with nested depth >2) MUST be logged in `backend/compute-engine/src/schema_rehearsal/friction_log.md` and fixed before Freeze A. Freeze A only happens after Schema Dress Rehearsal passes with **zero unresolved schema-friction items**.

#### Access Control

- **FR-025**: System MUST enforce access control via API keys/OAuth, tenant isolation, and rate limits.

- **FR-025A**: System MUST provide pagination for large result sets with configurable page sizes.

- **FR-025B**: System MUST implement clear error taxonomy: 4xx for validation errors, 409 for conflicts, 5xx for compute failures, with structured error responses including remediation guidance. **All modules MUST follow the standardized error taxonomy defined in CL-025 and this requirement**. Error responses MUST include structured format: `{ error_code: string, message: string, remediation: string, retryable: boolean, retry_after_seconds?: number }`. Reference: `specs/001-master-spec/master_spec.md` CL-025 for complete error taxonomy details.

- **FR-025C**: System MUST support partial-result semantics for batch operations, returning successful results alongside errors for failed items.

- **FR-025D**: System MUST implement API versioning using URL path versioning format `/api/v{major}/...` for all external-facing APIs. **All modules MUST follow the standardized API versioning policy defined in `specs/001-master-spec/API_VERSIONING_POLICY.md`**. Breaking changes require new major version; non-breaking changes (new optional parameters, new endpoints, new response fields) do not require version bump. Deprecation period: 6 months standard, 3 months for internal module-to-module APIs. Reference: `specs/001-master-spec/API_VERSIONING_POLICY.md` for complete versioning strategy, deprecation policy, and migration guides.

- **FR-025E**: System MUST implement cross-module integration tests that verify end-to-end workflows across module boundaries. **All modules MUST include integration tests that validate**: (1) API contract compatibility between modules (e.g., Compute Engine → References Engine, Advice Engine → Compute Engine, LLM Orchestrator → all engines), (2) Error propagation and handling across module boundaries, (3) Data format consistency (request/response schemas match between producer and consumer modules), (4) Performance and latency requirements met across module boundaries, (5) Tenant isolation maintained across module boundaries. Integration tests MUST be located in `backend/{module}/tests/integration/test_{target_module}_integration.py` and MUST run as part of CI/CD pipeline. Reference: `specs/001-master-spec/master_tasks.md` T324 for end-to-end integration tests across all modules.

- **FR-026**: System MUST prohibit direct end-user backend access; all access MUST be mediated by Frankie's Finance, Veris Finance, or Partner integrations.

#### Authentication Flows

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

#### User Experience

- **FR-027**: System MUST provide Frankie's Finance (Consumer UX) with emotion-first design, non-linear navigation via spatial metaphors (path → front door → living room/study/garden), where Frankie serves as a companion guide and the app provides the advice voice.

- **FR-028**: System MUST provide Veris Finance (Adviser UX) with professional calm design, minimal chrome, clear hierarchy, comparative dashboards, conversational interface, data-centric visualizations, and audit log always available.

- **FR-029**: System MUST enable navigation by intent: user questions dictate next views; system brings appropriate modules to users.

- **FR-039**: System MUST connect Frankie's Finance to compliance validation to validate all financial advice provided to consumers, ensuring compliance with best interests duty and regulatory requirements.

- **FR-040**: System MUST display compliance validation results in Frankie's Finance in a user-friendly, non-technical manner appropriate for consumers, including warnings and required actions when applicable.

#### Compliance and Governance

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

- **FR-079**: System MUST allow users and advisers to access privacy settings and review what information has been collected at any time.

- **FR-032**: System MUST align data retention and erasure policies with Australian Privacy Act 1988 obligations.

- **FR-033**: System MUST support compliance with Corporations Act 2001, Privacy Act 1988, Anti-Money Laundering and Counter-Terrorism Financing Act 2006, and Code of Ethics for financial advisers.

- **FR-034**: System MUST maintain audit logs tracking all rule changes, compute operations, data access, and document generation.

- **FR-034A**: System MUST implement immutable audit logs with retention policies aligned with Australian regulatory requirements (minimum 7 years for financial advice records).

- **FR-034B**: System MUST support periodic certification runs against published regulator examples (ATO, ASIC) to validate calculation accuracy and compliance.

#### Error Handling and Resilience

- **FR-034C**: System MUST implement structured error responses with remediation guidance when calculations fail due to missing parameters or invalid inputs.

- **FR-034D**: System MUST implement timeouts and circuit breakers around database, cache, and OpenRouter API lookups to prevent blocking operations. **Timeouts**: Default 30 seconds per operation, configurable per operation type. **Circuit breakers**: Open after 5 consecutive failures, remain open for 30 seconds, then attempt half-open state.

- **FR-034E**: System MUST implement retry policies for transient I/O failures with exponential backoff and idempotency guarantees. **Retry policy**: Exponential backoff with initial delay 1 second, maximum delay 30 seconds, maximum 3 retries. All retries MUST use the same idempotency key to ensure exactly-once semantics.

- **FR-034F**: System MUST implement dead-letter queue for failed calculation jobs with replay capability and error analysis. Failed jobs after maximum retries MUST be moved to dead-letter queue with error details, timestamps, and operator notifications.

#### Validation and Reconciliation

- **FR-034G**: System MUST perform cross-checks to ensure sum of components equals totals and cash in-out conservation is maintained. **Tolerance**: Discrepancies exceeding 0.01 cents MUST be flagged as reconciliation failures.

- **FR-034H**: System MUST perform tax reconciliation: taxable income → tax calculation → offsets → net tax, with validation of each step. **Tolerance**: Each reconciliation step MUST validate that intermediate calculations match expected values within 0.01 cents tolerance.

- **FR-034I**: System MUST reconcile superannuation caps trackers to contribution ledgers and validate Transfer Balance Cap (TBC) and Total Super Balance (TSB) roll-forward calculations. **Tolerance**: Discrepancies exceeding 0.01 cents MUST be flagged as reconciliation failures.

- **FR-034J**: System MUST reconcile amortisation tables to closing balances and detect rounding drift that exceeds tolerance thresholds. **Tolerance**: Rounding drift exceeding 0.01 cents per period MUST be flagged for review.

#### Concurrency and Consistency

- **FR-034K**: System MUST prevent race conditions when multiple calculation runs update the same scenario, using appropriate locking or optimistic concurrency control.

- **FR-034L**: System MUST specify isolation levels for fact writes and document consistency guarantees per endpoint.

#### Advice Engine

- **FR-035**: System MUST provide Advice Engine that evaluates compliance obligations deterministically, checking best-interests duty, conflicts, documentation requirements, and product replacement logic.

- **FR-036**: System MUST generate warnings, required actions, and artifact checklists for compliance checking and requirement retrieval.

#### References and Research

- **FR-037**: System MUST maintain References & Research Engine managing authoritative legal and regulatory sources (legislation, RGs, rulings, case law) with normalized Reference objects including pinpoints, versions, and metadata.

- **FR-037A**: System MUST support LLM-assisted research for document ingestion and knowledge extraction, using external LLM research capabilities to extract structured entities (References, Rules, Assumptions, Advice Guidance, Client Outcome Strategies) from Australian financial documents, with human oversight for accuracy validation. Knowledge extraction MUST follow the comprehensive taxonomy defined in `specs/003-references-research-engine/research_guidance/research_knowledge_map.md`, which maps all knowledge categories (System Rules, Calculations, Client Context Variables, Eligibility Tests, Strategies, Exceptions, Interpretation Logic, Risk Frameworks, Behaviours, Advice Patterns, Compliance Tests, Case Types, Misconceptions, Values, Goals) to canonical types (RULE, ASSUMPTION, ADVICE GUIDANCE, CLIENT OUTCOME STRATEGY, FINDING).

- **FR-038**: System MUST provide search and retrieval capabilities for humans and AI models to access references.

---

### Key Entities

These concepts are applicable across all six modules and ensure determinism, traceability, and explainability across the system:

- **Rule**: A formal, deterministic statement that defines how a calculation, condition, or logical test must operate. Includes unique `RU-` identifier, effective window, precedence level, parameters, tests, linked References, and status/version.

- **Reference**: An authoritative legal or regulatory source (Act, Regulation, ASIC Regulatory Guide, ATO Ruling, Case, or Standard) with full citation, pinpoints, effective version, and checksum of source text.

- **Assumptions**: Non-authoritative constants required for modelling (e.g., inflation, CPI, earnings growth, discount rate). Snapshot-able, versioned, with scope (`global`, `tenant`, or `scenario`) and source/rationale tags.

- **Advice Guidance**: Codified professional obligations and ethical or procedural standards (ASIC RG 175, RG 244, FASEA Code, licensee policies) that embed compliance within the Advice Engine.

- **Client Outcome Strategy**: An actionable plan that orchestrates multiple Rules under relevant Advice Guidance to achieve measurable financial outcomes. Strategies must not contain calculation logic; they orchestrate Rules, eligibility tests, sequencing, and trade-offs only.

- **Scenario**: A tagged, versioned set of Facts, Inputs, and Assumptions representing a possible financial future (baseline, what-if, or historical). Scenarios include references to Client Events but do not own them.

- **Client Event**: A discrete financial or life action affecting a client (income change, purchase, policy start, marriage, retirement) with timestamp, description, financial impact, and linked Rules/Assumptions/References.

- **Input**: Immutable, versioned client-supplied or imported data (balances, income, holdings, contributions) captured at an `as_of` date. Distinguishes raw client data from Assumptions or derived Facts.

- **Fact**: An immutable computed result produced by applying Rules and Assumptions to Inputs within a Scenario. Includes unique `FA-` id, units, rounding policy, rounding plan hash, inputs hash, linked Rules/References/Assumptions/Provenance Links, scenario id, `as_of` date, and tolerance/computation method.

- **Finding**: A provisional rule, assumption, or principle extracted automatically from reference material. Findings exist before validation and separate unverified knowledge from governance-approved logic.

- **Research Question**: A structured record of uncertainty, ambiguity, or conflict identified during extraction or validation. Includes topic, source, priority, and reason. Transforms uncertainty into actionable research tasks.

- **Verdict**: A formal decision outcome attached to a Finding after validation. Possible values: `Approved`, `Rejected`, `Needs Revision`. Includes validator summary, timestamp, reason, and actor (`system` or `reviewer`). Finding state machine: `Draft → In_Validation → Contested → Approved | Rejected`.

- **Provenance Link**: A first-class relationship object connecting Facts ↔ Rules/Strategies ↔ References ↔ Assumptions ↔ Inputs. Supports many-to-many links with role tags, effective windows per link, and evidence metadata.

- **Ruleset Snapshot**: A frozen, versioned collection of validated Rules, References, and Assumptions identified by a unique `ruleset_id` and `as_of` date. May be composed into domain bundles. Defines the exact knowledge state used by deterministic computations.

**Note**: Detailed schemas, fields, and lifecycle/state-machine definitions for all canonical concepts are documented in `specs/001-master-spec/canonical_data_model.md`. The constitution (`.specify/memory/constitution.md`) defines what these concepts are and why they matter.

- **Access Token**: Short-lived credential (15 minutes) used to authenticate API requests. Contains user identity, tenant context, permissions, and expiration time. Must be validated on every request. Reference: CL-038.

- **Refresh Token**: Long-lived credential (7 days) used to obtain new access tokens without re-authentication. Stored securely (HTTP-only cookies for web, SecureStore for mobile). Rotated on every use. Reference: CL-038.

- **Authorization Code**: Temporary credential exchanged for tokens during OAuth2 flow. Valid for short duration (typically 10 minutes) and can only be used once with matching PKCE verifier. Reference: CL-038.

- **PKCE Code Verifier**: Cryptographically random string generated by client, transformed into code challenge using SHA256, used to prove possession of authorization code during token exchange. Reference: CL-038.

- **PKCE Code Challenge**: SHA256 hash of code verifier, sent to authorization server during authorization request, verified during token exchange to prevent authorization code interception. Reference: CL-038.

- **User Session**: Represents an authenticated user session with associated access token, refresh token, device/browser identifier, creation time, last activity time, and revocation status. Supports multiple concurrent sessions per user (up to 5 devices). Reference: CL-038.

- **Privacy Explanation**: User-facing content that explains PII filtering practices. Attributes include: explanation text (consumer vs. professional versions), privacy policy reference, display timing (during setup), and access controls.

- **User PII Profile** (Frankie's Finance): Collected identifying information for personalization and filtering. Attributes include: name, date of birth, suburb, collection timestamp, and consent acknowledgment.

- **Client PII Profile** (Veris Finance): Collected identifying information for client management and filtering. Attributes include: name, date of birth, address, contact details, account numbers, TFN, collection timestamp, and consent acknowledgment.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can receive answers to financial questions within 3 seconds from initial query submission to displayed response, excluding complex multi-scenario calculations. This includes LLM processing time, backend calculation time, and frontend rendering time. Complex multi-scenario calculations (e.g., 50-year projections, batch comparisons) may exceed this threshold and are excluded from this success criterion.

- **SC-002**: System supports 10,000 concurrent authenticated sessions with active requests within a 5-minute window across all client applications (Frankie's Finance, Veris Finance, Partner integrations) without performance degradation. Performance degradation is defined as: API response times exceeding p95 targets by >20%, error rates exceeding 1%, or system unavailability.

- **SC-003**: 95% of financial calculations execute deterministically with identical results for same inputs, ruleset, and date parameters when tested across multiple runs.

- **SC-004**: 100% of computed Facts have complete provenance chains traceable through explanation requests with no missing links to rules, references, or assumptions.

- **SC-005**: Advisers can model and compare three different strategies for a client in under 2 minutes from initial data entry to comparative forecast display.

- **SC-006**: 90% of users successfully understand why a recommendation was made when accessing explanation output without requiring technical knowledge.

- **SC-007**: System maintains 99.9% uptime for core calculation services during business hours (8 AM - 8 PM AEST).

- **SC-008**: All rule publications complete the Publish → Validate → Activate workflow within 5 minutes, ensuring rulesets are available for computation immediately after activation.

- **SC-009**: Partner integrations can execute calculations at the same performance and accuracy levels as internal system calls with zero logic forks.

- **SC-010**: 100% of advice recommendations generated through Veris Finance include compliance check results, with warnings and required actions clearly displayed.

- **SC-011**: 100% of financial advice provided through Frankie's Finance is validated for compliance with best interests duty and regulatory requirements before being presented to consumers.

- **SC-012**: 95% of consumers can understand compliance validation results displayed in Frankie's Finance without requiring technical or financial expertise.

- **SC-013**: Users can authenticate and begin using the system within 30 seconds of initiating login, measured from login initiation to first successful API request. Reference: CL-038.

- **SC-014**: System maintains seamless user sessions: 95% of token refresh operations complete automatically without requiring user interaction, maintaining uninterrupted user experience. Reference: CL-038.

- **SC-015**: System prevents token reuse attacks: 100% of used refresh tokens are immediately invalidated and cannot be reused, verified through security testing. Reference: CL-038.

- **SC-016**: System handles authentication failures gracefully: 99% of expired token scenarios result in automatic refresh without user-visible errors, with remaining 1% requiring clear re-authentication prompts. Reference: CL-038.

- **SC-017**: System supports concurrent sessions: users can maintain authenticated sessions on up to 5 devices simultaneously without conflicts or security issues. Reference: CL-038.

- **SC-018**: System enforces security requirements: access tokens expire within 15 minutes, refresh tokens expire within 7 days, and token rotation occurs on 100% of refresh operations. Reference: CL-038.

- **SC-019**: System protects against common attacks: authentication flow prevents authorization code interception (PKCE), XSS attacks (HTTP-only cookies), CSRF attacks (SameSite cookies), and token replay (rotation and expiration). Reference: CL-038.

- **SC-020**: System provides auditability: 100% of authentication events (login, refresh, revocation, failures) are logged with timestamps, user identifiers, and device/browser information for security auditing and compliance. Reference: CL-038.

- **SC-021**: 100% of new Frankie's Finance users see the PII filtering explanation before asking their first financial question.

- **SC-022**: 90% of Frankie's Finance users who view the privacy explanation can correctly explain that their identifying information will not be sent to external AIs (measured through user testing).

- **SC-023**: 100% of Veris Finance advisers see the detailed PII filtering explanation before processing their first client query.

- **SC-024**: 95% of Veris Finance advisers who view the privacy explanation can correctly explain how client PII is protected (measured through professional user testing).

- **SC-025**: Users and advisers can access the privacy policy from the PII filtering explanation within 2 clicks or taps.

- **SC-026**: Privacy explanations are displayed within 30 seconds of completing initial setup (Frankie's Finance) or client setup (Veris Finance).

- **SC-027**: 85% of users report feeling confident about privacy protections after viewing the explanation (measured through user satisfaction surveys).

---

## Assumptions

### Domain Assumptions

- Australian financial regulations (Corporations Act 2001, ASIC Regulatory Guides, ATO Rulings) will continue to operate under hierarchical authority structure (Act > Regulation > Ruling > Guidance > Assumption).

- Financial advisers will continue to be required to demonstrate best interests duty and maintain traceable audit trails under Australian regulations.

- Users (both consumers and advisers) will access the system primarily via mobile devices (consumers) and desktop/web interfaces (advisers).

### Technical Assumptions

- Relational database technology will be available and capable of supporting the relational-only architecture with required performance characteristics (recursive CTEs, JSONB, temporal tables).

- OpenRouter will continue to offer a unified API suitable for intent detection and natural language translation with acceptable latency and reliability.

- Integration patterns will remain stable enough for partner integrations to rely on documented interfaces.

### User Behavior Assumptions

- Consumers will prefer conversational, non-technical interactions over complex financial terminology.

- Advisers will prefer efficiency and speed in scenario modelling over extensive configuration options.

- Partners will require stable, versioned interfaces that match internal capabilities rather than custom integrations.

### Compliance Assumptions

- Australian privacy laws (Privacy Act 1988) will continue to require strict data handling, tenant isolation, and PII protection measures.

- Financial advice regulations will continue to require reproducibility, auditability, and explicit rule-based calculations.

---

## Scope Boundaries

### In Scope (MVP)

- Core calculation rules: personal income tax, superannuation contributions and caps, core Capital Gains Tax (CGT)

- Basic scenario support: A/B scenario comparisons, sensitivity basics

- Core calculation capabilities: deterministic calculations and provenance

- Consumer UX: Frankie's Finance with path, front door, living room, study, and garden environments

- Adviser UX: Veris Finance with conversational interface and forecast visualization

- References & Research Engine with basic search and retrieval

- Advice Engine with basic compliance checking

### Out of Scope (Future)

- Product purchase rails (direct financial product transactions)

- External data aggregation from banks or financial institutions

- Advanced client outcome strategies library beyond basic tax and super strategies

- Comprehensive advice guidance strategies framework beyond core compliance obligations

- Automated trade execution

- Real-time market data integration

---

## Dependencies

### External Dependencies

- Australian financial regulatory framework (ASIC, APRA, ATO) maintaining current regulatory structure

- OpenRouter API for unified LLM provider access (supporting both OpenRouter credits and BYOK integration) for natural language processing

- Relational database technology capable of recursive CTEs, JSONB relationships, and temporal queries

- Relational database technology capable of temporal queries and audit logging

### Internal Dependencies

- Constitution principles must be maintained and validated across all modules

- Rule authoring and publishing workflow must be operational before calculations can execute

- References & Research Engine must be populated with authoritative sources before rules can cite references

- Data extraction pipeline must be operational to populate REFERENCES, RULES, ASSUMPTIONS, ADVICE GUIDANCE, and CLIENT OUTCOME STRATEGIES

