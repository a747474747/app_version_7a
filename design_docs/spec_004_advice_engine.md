# Feature Specification: Advice Engine

**Feature Branch**: `004-advice-engine`  
**Created**: 2025-01-27  
**Status**: Draft  
**Input**: Advice Engine module - enforces professional and regulatory standards through deterministic policy engine. Evaluates compliance obligations, checks best-interests duty, conflicts, documentation requirements, and generates warnings and required actions.

**Purpose**: This module enforces professional and regulatory standards for financial advice. It evaluates compliance obligations deterministically, checking best-interests duty, conflicts, documentation requirements, and product replacement logic. It generates warnings, required actions, and artifact checklists to ensure advice meets Australian regulatory requirements and professional standards.

**Reference**: This module implements requirements from the master specification (`001-master-spec/spec.md`), specifically FR-004C, FR-035 and FR-036.

## Architectural Boundaries

**Advice Engine** is the judgement and compliance brain. Per Constitution Principle XII:

- **MUST**: Consume Facts from Compute Engine (never calculate them); consume knowledge objects from References & Research Engine (never store them); select and sequence Client Outcome Strategies; weigh trade-offs and test suitability; evaluate compliance obligations and best-interests duty; apply interpretation logic based on Advice Guidance (e.g., "This is usually beneficial when...", "Preferable for clients who...", "Only valuable when balance exceeds...", "Not suitable if income unstable..."); apply behavioral-aware advice patterns (spending habits, biases, emotional patterns, mistakes, behavioral constraints); apply reasoning frameworks (problem → constraint → action → result, risk → structure → tax → behaviour → goal, prioritisation patterns, scenario comparison patterns, trade-off handling patterns); perform comparison and aggregation operations on Facts (e.g., comparing Fact values, summing Fact collections); emit structured advice outputs (recommendations, risks, violations, required artefacts).

- **MUST NOT**: Define its own tax formulas, caps, or raw system rules; perform numeric calculations that produce new Facts (all Facts must originate from Compute Engine); scrape raw documents (it consumes knowledge from References & Research Engine); store knowledge objects (it queries References & Research Engine); override deterministic outputs from Compute Engine.

Advice Engine focuses on reasoning, suitability, and compliance while delegating calculation and knowledge retrieval to specialized components. It applies reasoning frameworks and interpretation logic to Facts but does not perform calculations that produce new Facts.

---

## Clarifications

This section addresses ambiguous areas in the specification to eliminate implementation uncertainty.

### Session 2025-01-27

- Q: What reasoning operations can Advice Engine perform on Facts it receives from Compute Engine, given that it "MUST NOT perform numeric calculations"? → A: Advice Engine MUST perform reasoning, suitability, and compliance evaluation using: interpretation logic based on Advice Guidance (e.g., "This is usually beneficial when...", "Preferable for clients who...", "Only valuable when balance exceeds...", "Not suitable if income unstable..."); behavioral-aware advice patterns (spending habits, biases, emotional patterns, mistakes, behavioral constraints); reasoning frameworks (problem → constraint → action → result, risk → structure → tax → behaviour → goal, prioritisation patterns, scenario comparison patterns, trade-off handling patterns); comparison and aggregation operations on Facts (e.g., comparing Fact values, summing Fact collections). Advice Engine MUST NOT perform numeric calculations that produce new Facts (all Facts must originate from Compute Engine), but it CAN apply reasoning frameworks and interpretation logic to existing Facts to generate advice outputs.

- Q: What should happen when compliance evaluation requires Fact data that isn't available (e.g., Facts haven't been computed yet, or Fact retrieval fails)? → A: Return 422 Unprocessable Entity with specific missing Fact identifiers and remediation guidance (suggest computing Facts first or provide Fact data)

- Q: What should happen when compliance evaluation identifies conflicting advice recommendations (e.g., one recommendation suggests increasing super contributions while another suggests reducing them)? → A: Generate warnings for each conflicting recommendation, require resolution before compliance approval

- Q: What should happen when compliance requirements are queried for a context that has no applicable requirements (e.g., querying requirements for a scenario that doesn't trigger any compliance obligations)? → A: Return empty result set with clear messaging explaining no requirements apply for this context

- Q: What should happen when Advice Guidance data isn't available for a compliance evaluation (e.g., Advice Guidance hasn't been ingested yet, or retrieval fails)? → A: Return 422 Unprocessable Entity with specific missing Advice Guidance identifiers and remediation guidance (suggest ingesting Advice Guidance or provide Advice Guidance data)

- Q: What should happen when a compliance checklist is requested for an advice context, but some checklist items cannot be determined (e.g., required documents that depend on incomplete client data)? → A: Generate partial checklist with available items, mark undetermined items with explanation of what data is needed

---

## User Scenarios & Testing

### User Story 1 - Validate Advice Compliance (Priority: P1)

**Adviser Story**: An adviser needs to validate their recommendations against the Code of Ethics and regulatory obligations to ensure every piece of advice is compliant, traceable, and ready for audit.

**Why this priority**: This is the core function of the Advice Engine. Without compliance validation, advisers cannot ensure their advice meets regulatory requirements. This capability is essential for professional practice and regulatory compliance.

**Independent Test**: An adviser can submit advice recommendations (client data, calculated Facts, proposed strategies) to the Advice Engine, and receive compliance evaluation results indicating whether the advice meets best-interests duty, regulatory obligations, and professional standards, with specific warnings and required actions if issues are identified.

**Acceptance Scenarios**:

1. **Given** an adviser submits advice for compliance checking, **When** the system evaluates it, **Then** it checks best-interests duty, conflicts of interest, documentation requirements, and product replacement logic, returning compliance outcomes with warnings and required actions.

2. **Given** advice recommendations include calculated Facts, **When** the system evaluates compliance, **Then** it uses Fact data to assess whether recommendations align with client circumstances and regulatory requirements.

3. **Given** advice recommendations reference specific products or strategies, **When** the Advice Engine evaluates them, **Then** it checks for conflicts of interest, ensures product replacement logic is followed, and verifies that recommendations serve the client's best interests.

4. **Given** compliance evaluation identifies issues, **When** warnings and required actions are generated, **Then** they are specific, actionable, and reference relevant regulatory requirements and professional standards.

---

### User Story 2 - Consumer Advice Compliance Validation (Priority: P1)

**Consumer Story**: A consumer receives financial advice through Frankie's Finance, and the system must validate that advice meets professional standards and regulatory requirements before presenting it to the consumer.

**Why this priority**: Consumers must receive compliant advice even when accessing it through a consumer-facing application. The Advice Engine must validate all advice provided to consumers, ensuring it meets best-interests duty and regulatory requirements, with results displayed in consumer-friendly language.

**Independent Test**: When Frankie's Finance provides financial advice to a consumer, the Advice Engine validates it, and any compliance warnings or required actions are displayed in user-friendly, non-technical language appropriate for consumers.

**Acceptance Scenarios**:

1. **Given** Frankie's Finance provides financial advice to a consumer, **When** the Advice Engine evaluates it, **Then** it performs the same compliance checks as for adviser advice, ensuring consumer advice meets professional standards.

2. **Given** compliance validation identifies issues with consumer advice, **When** warnings are generated, **Then** they are displayed in consumer-friendly language, avoiding technical jargon while maintaining accuracy.

3. **Given** consumer advice cannot meet compliance requirements, **When** validation fails, **Then** the system prevents presentation of non-compliant advice and suggests consulting a licensed financial adviser.

4. **Given** consumer advice passes compliance validation, **When** results are returned, **Then** consumers can see that their advice has been validated against professional standards, building trust and confidence.

---

### User Story 3 - Retrieve Compliance Requirements (Priority: P2)

**Adviser Story**: An adviser needs to understand what compliance obligations apply in a specific context (e.g., "giving personal advice" or "recommending a product replacement") so they can prepare appropriate documentation and follow required processes.

**Why this priority**: Advisers need proactive guidance on compliance requirements before providing advice. This enables them to prepare documentation, follow processes, and avoid compliance issues. This is valuable for workflow efficiency and risk management.

**Independent Test**: An adviser can query compliance requirements for a specific context (e.g., "giving_personal_advice") and receive a list of required actions, documentation, and professional standards that apply.

**Acceptance Scenarios**:

1. **Given** an adviser queries compliance requirements for a specific context, **When** they submit a query with context parameters, **Then** the system returns required actions (e.g., provide FSG, assess client circumstances), required documentation (e.g., Statement of Advice), and relevant professional standards.

2. **Given** compliance requirements reference regulatory sources, **When** requirements are returned, **Then** they include links to relevant References (legislation, regulatory guides) enabling advisers to verify requirements.

3. **Given** compliance requirements vary by advice type or client circumstances, **When** requirements are queried, **Then** the system returns context-specific requirements, filtering out irrelevant obligations.

4. **Given** compliance requirements change over time, **When** requirements are queried with an `as_of` date, **Then** the system returns requirements applicable at that time, supporting historical reconstruction.

---

### User Story 4 - Generate Compliance Documentation Checklists (Priority: P2)

**Adviser Story**: An adviser needs automated checklists of required documentation and actions for compliance, ensuring nothing is missed when preparing advice and reducing administrative burden.

**Why this priority**: Compliance documentation is complex and error-prone. Automated checklists reduce the risk of missing required documents or actions, improve efficiency, and ensure consistency. This supports the value proposition of reducing adviser administrative burden.

**Independent Test**: An adviser can request a compliance checklist for their advice scenario, and receive a structured list of required documents (FSG, SOA, ROA), required actions (client assessment, conflict checks), and professional standards, with checkboxes for tracking completion.

**Acceptance Scenarios**:

1. **Given** an adviser requests a compliance checklist, **When** the Advice Engine generates it, **Then** it includes all required documents, actions, and professional standards applicable to the advice context.

2. **Given** compliance checklists reference specific regulatory requirements, **When** checklists are generated, **Then** they include citations to relevant References, enabling advisers to verify requirements and demonstrate compliance.

3. **Given** compliance requirements have been completed, **When** checklists are updated, **Then** the system tracks completion status, enabling advisers to see what remains to be done.

4. **Given** compliance checklists are used for audit purposes, **When** they are exported, **Then** they include timestamps, completion status, and references to regulatory sources, suitable for inclusion in compliance packs.

---

### Edge Cases

- What happens when advice recommendations conflict with each other? The system MUST detect conflicts, generate warnings for each conflicting recommendation, and require resolution before compliance approval. Compliance status MUST remain non-compliant until conflicts are resolved.

- How does the system handle advice that falls outside current regulatory coverage? The system MUST indicate when advice cannot be fully validated due to gaps in regulatory coverage, and may require manual review or suggest consulting regulatory experts.

- What happens when compliance requirements change after advice has been provided? The system MUST maintain historical compliance evaluations using the requirements applicable at the time advice was given, enabling accurate audit trails.

- How does the system handle advice for clients with complex circumstances (e.g., multiple entities, international considerations)? The system MUST evaluate compliance across all relevant contexts, identifying requirements that apply to each aspect of the client's situation.

- What happens when compliance evaluation requires data that isn't available? The system MUST indicate missing data requirements, generate warnings, and may prevent compliance validation until required data is provided.

- How does the system handle advice that meets regulatory requirements but may not serve the client's best interests? The system MUST evaluate both regulatory compliance and best-interests duty, generating warnings if advice is technically compliant but potentially not in the client's best interests.

---

## Requirements

### Functional Requirements

#### Compliance Evaluation

- **FR-001**: System MUST evaluate compliance obligations deterministically, checking best-interests duty, conflicts of interest, documentation requirements, and product replacement logic.

- **FR-002**: System MUST evaluate compliance using Advice Guidance (mandatory obligations and professional standards) stored in the system, ensuring evaluations are based on current regulatory requirements. When Advice Guidance data isn't available for a compliance evaluation (Advice Guidance hasn't been ingested yet, or retrieval fails), the system MUST return 422 Unprocessable Entity error with specific missing Advice Guidance identifiers and remediation guidance (suggesting ingesting Advice Guidance or providing Advice Guidance data).

- **FR-003**: System MUST check best-interests duty by evaluating whether recommendations serve the client's interests, considering client circumstances, objectives, and risk tolerance.

- **FR-004**: System MUST detect conflicts of interest by analyzing adviser relationships, product recommendations, and fee structures, generating warnings when conflicts are identified.

- **FR-005**: System MUST verify documentation requirements by checking whether required documents (FSG, SOA, ROA) have been created or are planned, generating required actions if documentation is missing.

- **FR-006**: System MUST evaluate product replacement logic by checking whether product switches are justified, documented, and serve the client's best interests, following regulatory requirements for product replacement.

- **FR-007**: System MUST use Fact data when evaluating compliance, ensuring evaluations are based on accurate calculations and client circumstances. When compliance evaluation requires Fact data that isn't available (Facts haven't been computed yet, or Fact retrieval fails), the system MUST return 422 Unprocessable Entity error with specific missing Fact identifiers and remediation guidance (suggesting computing Facts first or providing Fact data).

- **FR-008**: System MUST reference regulatory requirements when evaluating compliance, linking compliance outcomes to authoritative sources.

#### Compliance Access

- **FR-009**: System MUST provide compliance checking capability accepting client data, computed Facts, and advice recommendations, returning compliance outcomes, warnings, and required actions.

- **FR-010**: System MUST return compliance evaluation results in structured format with clear indication of compliance status and specific issues identified.

- **FR-011**: System MUST provide compliance requirements capability returning required actions, documentation, and professional standards for specific advice contexts. When a context has no applicable requirements, the system MUST return an empty result set with clear messaging explaining that no requirements apply for this context.

- **FR-012**: System MUST support context-based requirement queries, filtering requirements based on advice type (personal advice, general advice, product recommendation) and client circumstances.

- **FR-013**: System MUST support time-travel queries for compliance requirements, using `as_of` dates to return requirements applicable at specific points in time.

- **FR-014**: System MUST enforce access control with tenant isolation and rate limits as specified in the master specification (see CL-031 and FR-030 for security guarantee that User A can NEVER see User B's data under ANY circumstances).

- **FR-014A**: System MUST include automated security tests that verify cross-tenant data access is impossible for all Advice Engine endpoints. Tests MUST simulate bugs, misconfigured queries, malicious input, missing tenant context, and other failure scenarios to ensure User A cannot access User B's compliance evaluations, advice guidance, or client outcome strategies under any conditions (see FR-030A in master specification).

#### Warnings and Required Actions

- **FR-015**: System MUST generate specific, actionable warnings when compliance issues are identified, explaining what the issue is, why it matters, and how to resolve it.

- **FR-016**: System MUST generate required actions when compliance obligations are not met, listing specific steps that must be taken to achieve compliance.

- **FR-017**: System MUST prioritize warnings and required actions by severity, indicating which issues must be resolved before advice can be considered compliant.

- **FR-018**: System MUST reference regulatory sources in warnings and required actions, enabling users to verify requirements and demonstrate compliance.

- **FR-019**: System MUST format warnings for different audiences: technical language for advisers, consumer-friendly language for consumers accessing advice through Frankie's Finance.

#### Compliance Documentation

- **FR-020**: System MUST generate compliance checklists including required documents (FSG, SOA, ROA), required actions (client assessment, conflict checks), and professional standards. When some checklist items cannot be determined (e.g., required documents that depend on incomplete client data), the system MUST generate a partial checklist with available items and mark undetermined items with explanations of what data is needed.

- **FR-021**: System MUST track completion status for compliance checklist items, enabling advisers to see what has been completed and what remains.

- **FR-022**: System MUST export compliance checklists in formats suitable for inclusion in compliance packs, with timestamps, completion status, and regulatory citations.

- **FR-023**: System MUST link compliance checklists to specific advice scenarios, enabling advisers to maintain compliance documentation for each client engagement.

#### Integration

- **FR-024**: System MUST retrieve Fact data for compliance evaluation, ensuring evaluations are based on accurate calculations.

- **FR-025**: System MUST retrieve regulatory requirements and professional standards, ensuring compliance evaluations reference authoritative sources.

- **FR-026**: System MUST validate consumer advice, ensuring all advice provided to consumers meets compliance requirements.

- **FR-027**: System MUST validate adviser advice, providing compliance checking and documentation support for professional advisers.

#### Deterministic Evaluation

- **FR-028**: System MUST evaluate compliance deterministically: same advice + same client data + same Facts + same `as_of` date MUST produce identical compliance outcomes.

- **FR-029**: System MUST pin compliance evaluations to explicit `as_of` dates and Advice Guidance versions, enabling reproducibility and historical reconstruction.

- **FR-030**: System MUST maintain audit logs of all compliance evaluations, tracking what was evaluated, when, and what outcomes were generated.

---

### Key Entities

- **Compliance Evaluation**: Assessment of advice against regulatory requirements and professional standards. Attributes include: evaluation identifier, advice scenario, client data, computed Facts, evaluation timestamp, compliance status (compliant, non-compliant, conditional), warnings, required actions, and references to Advice Guidance and regulatory sources.

- **Advice Guidance**: Mandatory obligations and professional standards that define what must be done, when, and how for compliance. Attributes include: unique identifier, title, description, status, version, effective dates, event triggers, required artifacts (documents), required behaviours (actions), and references to source legislation. Evaluated by Advice Engine to determine compliance requirements.

- **Compliance Warning**: Specific issue identified during compliance evaluation. Attributes include: warning identifier, severity level (critical, warning, informational), description, affected advice component, regulatory reference, and resolution guidance.

- **Required Action**: Specific step that must be taken to achieve compliance. Attributes include: action identifier, description, priority, related warning (if applicable), regulatory reference, and completion status.

- **Compliance Checklist**: Structured list of required documents, actions, and professional standards for a specific advice context. Attributes include: checklist identifier, context, required documents, required actions, professional standards, completion status, and timestamps.

- **Best-Interests Assessment**: Evaluation of whether advice serves the client's best interests. Attributes include: assessment identifier, client circumstances, advice recommendations, evaluation criteria, outcome, and reasoning.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: System evaluates compliance for standard advice scenarios and returns results within 3 seconds for 95% of requests.

- **SC-002**: System correctly identifies compliance issues (best-interests duty violations, conflicts, missing documentation) with 95% accuracy when validated against expert compliance reviews.

- **SC-003**: 100% of compliance evaluations are deterministic: identical advice scenarios produce identical compliance outcomes across multiple evaluations.

- **SC-004**: System generates specific, actionable warnings for 100% of identified compliance issues, with clear descriptions and resolution guidance.

- **SC-005**: Advisers can retrieve compliance requirements for specific contexts and receive complete, accurate lists of required actions and documentation within 2 seconds for 90% of queries.

- **SC-006**: 90% of advisers successfully understand compliance warnings and required actions without requiring additional clarification or training.

- **SC-007**: 95% of consumers can understand compliance validation results displayed in Frankie's Finance without requiring technical or financial expertise.

- **SC-008**: System maintains complete audit trails for 100% of compliance evaluations, enabling historical reconstruction and regulatory verification.

- **SC-009**: System correctly applies Advice Guidance versions based on `as_of` dates, ensuring compliance evaluations use requirements applicable at the time advice was given.

- **SC-010**: Compliance checklists include all required documents, actions, and professional standards for 100% of advice contexts, reducing the risk of missing compliance obligations.

---

## Assumptions

### Domain Assumptions

- Australian financial advice regulations (Corporations Act 2001, Code of Ethics, ASIC Regulatory Guides) will continue to require best-interests duty, conflict management, and documentation requirements.

- Compliance obligations can be evaluated deterministically using Advice Guidance and regulatory requirements stored in the system, without requiring subjective human judgment during evaluation.

- Advice Guidance will be sufficiently complete and up-to-date to enable automated compliance evaluation for common advice scenarios.

- Regulatory requirements will maintain consistency in structure (best-interests duty, conflicts, documentation) enabling systematic evaluation.

### Technical Assumptions

- Advice Guidance data will be available and operational before Advice Engine can perform compliance evaluations.

- Compute Engine will provide Fact data in formats suitable for compliance evaluation.

- References & Research Engine will provide regulatory requirement lookups with acceptable performance for compliance evaluation workflows.

- Storage systems will support efficient querying of Advice Guidance, compliance evaluations, and audit logs.

### Integration Assumptions

- Consumer and adviser applications will call Advice Engine for compliance validation before presenting advice to users.

- Calculation services will be available to provide Fact data when Advice Engine performs compliance evaluations.

- Reference lookup services will be available to provide regulatory requirement lookups when Advice Engine evaluates compliance.

- Advice Guidance will be stored and versioned in a format that enables efficient querying and evaluation.

---

## Scope Boundaries

### In Scope (MVP)

- Core compliance evaluation checking best-interests duty, conflicts, documentation, and product replacement logic

- Compliance requirements retrieval for specific advice contexts

- Warning and required action generation for identified compliance issues

- Basic compliance checklist generation for common advice scenarios

- Fact data retrieval for compliance evaluation

- Regulatory requirement lookups for compliance evaluation

- Consumer-friendly warning formatting for consumer applications

- Deterministic compliance evaluation with reproducibility

### Out of Scope (Future)

- Advanced conflict detection using machine learning or pattern recognition

- Automated document generation (SOA, ROA) - Advice Engine identifies requirements, but document generation is handled by other modules

- Real-time compliance monitoring or continuous compliance checking

- Multi-jurisdiction compliance evaluation (focusing on Australian regulations)

- Advanced risk assessment or suitability analysis beyond basic best-interests evaluation

- Integration with external compliance databases or regulatory reporting systems

---

## Dependencies

### External Dependencies

- Australian financial regulatory framework (Corporations Act 2001, Code of Ethics, ASIC Regulatory Guides) maintaining current compliance structure

- Advice Guidance data must be populated before Advice Engine can perform compliance evaluations

- Storage systems for Advice Guidance, compliance evaluations, and audit logs

### Internal Dependencies

- Master specification (`001-master-spec`) for system context, requirements, and architectural constraints

- Calculation services for Fact data when evaluating compliance

- Reference lookup services for regulatory requirement lookups

- Authentication/authorization system for access control (from foundational infrastructure)

- Logging and observability infrastructure for audit trails
