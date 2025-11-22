# Feature Specification: Veris Finance

**Feature Branch**: `007-veris-finance`  
**Created**: 2025-01-27  
**Status**: Draft  
**Input**: Veris Finance module - professional adviser console with calm, data-centric UI. Provides LLM-powered chat interface, client scenario management, compliant forecasting, comparative analysis, and automated documentation generation. Built for speed, compliance, and explainability.

**Purpose**: Veris Finance is the professional adviser companion that transforms complex financial modelling into a fast, conversational, and compliant experience. It is designed for licensed financial advisers who need a simple, auditable, and intelligent workspace to generate, test, and present client strategies efficiently. The system reduces administrative and technical burden while maintaining full transparency, compliance, and explainability.

**Reference**: This module implements requirements from the master specification (`001-master-spec/spec.md`), specifically FR-028 and FR-029.

## Architectural Boundaries

**Veris Finance** is a professional UX module that consumes backend services. Per Constitution Principle XII:

- **MUST**: Call backend APIs (LLM Orchestrator for natural language processing, Compute Engine for calculations, Advice Engine for compliance validation, References & Research Engine for knowledge retrieval); display results and visualizations; provide professional interfaces for advisers.

- **MUST NOT**: Perform calculations (it calls Compute Engine APIs); store knowledge objects (it queries References & Research Engine APIs); contain business logic or decision-making rules (it calls Advice Engine APIs).

All calculations, knowledge storage, and business logic are handled by backend modules. Veris Finance focuses on professional user experience and presentation.

---

## Clarifications

This section addresses ambiguous areas in the specification to eliminate implementation uncertainty.

### Session 2025-01-27

- Q: What should happen when an adviser needs to model a client scenario that falls outside current rule coverage (e.g., complex multi-entity structures not yet supported)? → A: Return structured error (422) with specific limitation, suggest alternative approaches, allow partial modelling if possible

- Q: What should happen when compliance validation fails and an adviser attempts to generate an advice document (SOA/ROA)? → A: Block document generation, display compliance failures clearly, require resolution before allowing generation

- Q: What should happen when an adviser needs to modify assumptions or scenario parameters after calculations have been executed? → A: Allow modifications, trigger recalculation, maintain audit trail showing what changed and when

- Q: What should happen when an adviser needs to export a compliance pack but some required documentation is missing or incomplete? → A: Generate partial compliance pack with available items, clearly mark missing items, allow export with warnings

- Q: What should happen when an adviser works with multiple clients simultaneously and needs to switch between client contexts quickly? → A: Provide client switcher/context menu, maintain separate sessions per client, enable quick switching without data loss

---

## User Scenarios & Testing

### User Story 1 - "Model my client's scenario." Data-Driven Forecasting (Priority: P1)

**Adviser Story**: An adviser wants to enter or import a client's financial profile and run multiple scenarios so they can compare outcomes (e.g., retirement age, investment mix, contribution strategy) and produce deterministic forecasts backed by explainable rules.

**Why this priority**: This is the core professional workflow. Advisers need to model client scenarios quickly and accurately. Without this capability, advisers cannot provide value to clients or generate compliant advice.

**Independent Test**: An adviser can enter client data via natural language ("Add client aged 42 with $450k super") or structured input, create multiple scenarios, execute calculations, and view comparative forecasts with full provenance—all within a professional, efficient interface.

**Acceptance Scenarios**:

1. **Given** an adviser opens Veris Finance, **When** they input client information via natural language chat ("Add new client aged 42 with $450k super") or structured forms, **Then** the system stores client data and makes it available for scenario modelling and future advice sessions.

2. **Given** an adviser creates a client scenario, **When** they specify parameters (retirement age, investment mix, contribution strategy), **Then** the system executes deterministic calculations and presents forecasts with professional charts and visualizations.

3. **Given** an adviser wants to compare multiple scenarios, **When** they create scenario A, B, and C with different parameters, **Then** the system executes calculations for each scenario and presents side-by-side comparisons with clear visual differentiation.

4. **Given** an adviser views forecast results, **When** they examine the data, **Then** all calculations are traceable through explanation capabilities, with provenance chains linking to rules, references, and assumptions clearly displayed in the audit log.

---

### User Story 2 - "Check my advice for compliance." Best-Interests & Conduct Verification (Priority: P1)

**Adviser Story**: An adviser wants to validate their recommendations against the Code of Ethics and regulatory obligations so they can ensure every piece of advice is compliant, traceable, and ready for audit.

**Why this priority**: Compliance is non-negotiable for professional advisers. Every recommendation must meet regulatory requirements. This capability ensures advisers can confidently provide advice knowing it meets professional standards.

**Independent Test**: An adviser can submit advice recommendations for compliance checking, receive validation results with warnings and required actions, and see compliance status clearly displayed with links to regulatory requirements.

**Acceptance Scenarios**:

1. **Given** an adviser prepares advice recommendations, **When** they request compliance checking, **Then** the system validates best-interests duty, conflicts, documentation requirements, and product replacement logic, returning compliance outcomes.

2. **Given** compliance validation identifies issues, **When** warnings and required actions are generated, **Then** they are displayed clearly with specific guidance on what needs to be addressed, linked to relevant regulatory requirements.

3. **Given** an adviser needs to understand compliance requirements, **When** they query with context parameters, **Then** the system returns required actions, documentation, and professional standards applicable to their advice context.

4. **Given** compliance validation passes, **When** advice is approved, **Then** the system clearly indicates compliance status, enabling advisers to proceed with confidence.

---

### User Story 3 - "Generate the advice documents." Automated SOA/ROA Creation (Priority: P1)

**Adviser Story**: An adviser wants to produce a Statement or Record of Advice automatically from the client scenario so they can save time and guarantee consistency with their calculations and compliance results.

**Why this priority**: Document generation is a major time burden for advisers. Automated generation reduces administrative work while ensuring consistency between calculations, compliance results, and documentation. This directly supports the value proposition of reducing adviser burden.

**Independent Test**: An adviser can generate a Statement of Advice from a client scenario, and the document includes all calculations, compliance results, recommendations, and required disclosures, formatted consistently and ready for client presentation.

**Acceptance Scenarios**:

1. **Given** an adviser has completed client scenario modelling and compliance checking, **When** they request document generation, **Then** the system generates a Statement or Record of Advice including all calculations, compliance results, recommendations, and required disclosures.

2. **Given** a document is generated, **When** it is created, **Then** it includes traceable explanations linking to authoritative references, rule versions, and calculation assumptions, suitable for compliance packs.

3. **Given** a document includes compliance information, **When** it is generated, **Then** it incorporates compliance validation results, warnings, and required actions, ensuring documentation matches compliance status.

4. **Given** an adviser needs to export documentation, **When** they request export, **Then** the system provides documents in formats suitable for client presentation and regulatory submission, with full audit trails.

---

### User Story 4 - "Compare products and strategies." Evidence-Based Recommendations (Priority: P1)

**Adviser Story**: An adviser wants to test alternative products or strategies side-by-side so they can demonstrate to clients—and auditors—that their recommendation represents the client's best interest.

**Why this priority**: Advisers must demonstrate best-interests duty by comparing alternatives. This capability enables evidence-based recommendations and supports regulatory compliance. It's essential for professional practice.

**Independent Test**: An adviser can compare multiple strategies (e.g., "Compare debt-recycling vs offset-strategy over 10 years"), view side-by-side forecasts, and export comparison results showing how the recommended strategy serves the client's best interests.

**Acceptance Scenarios**:

1. **Given** an adviser wants to compare strategies, **When** they request comparison ("Compare debt-recycling vs offset-strategy over 10 years"), **Then** the system executes calculations for each strategy and presents comparative forecasts with professional charts showing differences and trade-offs.

2. **Given** strategy comparison results are displayed, **When** an adviser reviews them, **Then** they can see clear visual differentiation between strategies, with key differences highlighted and explained.

3. **Given** an adviser selects a recommended strategy, **When** they document the recommendation, **Then** the system enables them to explain why this strategy serves the client's best interests, with evidence from the comparison.

4. **Given** comparison results are used for client presentation, **When** they are exported, **Then** they include all calculations, assumptions, and visualizations needed to demonstrate best-interests duty to clients and auditors.

---

### User Story 5 - "Explain and justify my advice." Transparent Audit Trail (Priority: P1)

**Adviser Story**: An adviser wants to show regulators or clients why a recommendation was made so they can demonstrate transparency, ethical reasoning, and adherence to professional standards.

**Why this priority**: Auditability is essential for professional practice. Advisers must be able to justify recommendations to regulators and clients. This capability builds trust and ensures regulatory compliance.

**Independent Test**: An adviser can access the audit log for any recommendation, see the complete reasoning chain (Fact → Rule → Reference → Assumptions), and export audit trails suitable for regulatory review or client explanation.

**Acceptance Scenarios**:

1. **Given** an adviser has generated advice, **When** they access the audit log, **Then** they see a transparent record of all advice logic, calculations, compliance checks, and changes, with timestamps and reasoning trails.

2. **Given** an adviser needs to explain a recommendation, **When** they request explanation via `/explain/{fact_id}`, **Then** the system provides a human-readable trace showing Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions with versions and dates.

3. **Given** an adviser needs to justify advice to regulators, **When** they export audit trails, **Then** the system provides complete provenance chains with all calculations, compliance results, and regulatory references, suitable for regulatory submission.

4. **Given** an adviser needs to explain advice to clients, **When** they access explanations, **Then** the system provides client-friendly versions that explain recommendations clearly while maintaining technical accuracy for professional use.

---

### User Story 6 - "Forecast with Precision." Professional Forecasting Engine (Priority: P2)

**Adviser Story**: An adviser wants to build accurate financial forecasts for clients quickly and confidently so they can model outcomes, stress-test strategies, and present compliant projections backed by deterministic rules and assumptions.

**Why this priority**: Forecasting is essential for financial planning. Advisers need precise, reliable forecasts that can be stress-tested and validated. This capability enables confident client presentations and strategy evaluation.

**Independent Test**: An adviser can create financial forecasts quickly, adjust assumptions, stress-test scenarios, and present projections with confidence that they are backed by deterministic rules and can be explained and validated.

**Acceptance Scenarios**:

1. **Given** an adviser wants to create a financial forecast, **When** they specify client data and assumptions, **Then** the system executes calculations and presents professional forecasts with clear visualizations and key metrics.

2. **Given** an adviser wants to stress-test a strategy, **When** they vary assumptions (e.g., different return rates, contribution amounts), **Then** the system executes sensitivity analysis, showing how outcomes change with assumption variations.

3. **Given** forecasts are presented to clients, **When** they are displayed, **Then** they use professional charts and visualizations with consistent formatting, clear legends, and appropriate detail levels for client understanding.

4. **Given** forecasts are based on deterministic rules, **When** they are generated, **Then** all assumptions and rule versions are clearly documented, enabling advisers to explain forecasts and demonstrate compliance.

---

### Edge Cases

- What happens when an adviser needs to model a client scenario that falls outside current rule coverage? The system MUST return a structured error (422 Unprocessable Entity) with specific limitation details, suggest alternative approaches (e.g., simplified scenarios, manual calculation, external resources), and allow partial modelling if possible (e.g., model supported aspects while indicating unsupported aspects).

- How does the system handle advisers who work with multiple clients simultaneously? The system MUST support multiple client records, scenario management per client, and efficient switching between clients without data loss or confusion.

- What happens when compliance validation fails and advice cannot be provided? The system MUST clearly indicate compliance failures, provide specific guidance on what needs to be addressed, and prevent generation of non-compliant advice documents.

- How does the system handle advisers who need to modify assumptions or scenarios after calculations have been executed? The system MUST allow modifications to assumptions or scenario parameters after calculations have been executed, trigger recalculation automatically when modifications occur, and maintain a complete audit trail showing what changed, when it changed, and the impact on calculation results.

- What happens when an adviser needs to access historical advice that was generated using older ruleset versions? The system MUST support time-travel queries, reconstructing historical advice using the ruleset versions applicable at that time, enabling accurate historical review.

- How does the system handle very large client portfolios or complex scenarios that require extensive calculations? The system MUST process complex scenarios efficiently, potentially using batch processing or pagination, while maintaining accuracy and providing progress indicators.

---

## Requirements

### Functional Requirements

#### Professional Interface Design

- **FR-001**: System MUST provide a professional, calm interface with minimal chrome, clear hierarchy, and emphasis on data clarity, using cool neutrals (graphite, silver, blue accent) and crisp typography.

- **FR-002**: System MUST provide a data-centric UI optimized for visualizing strategies, forecasts, and comparisons with professional charts, graphs, and comparative dashboards.

- **FR-003**: System MUST display audit log always available, providing transparent record of all advice logic, calculations, compliance checks, and changes with timestamps and reasoning trails.

- **FR-004**: System MUST provide clean, two-column layouts for client summaries with icons and editable fields, enabling efficient data entry and review.

- **FR-005**: System MUST use consistent formatting for charts across time horizons with clear legends and callouts, maintaining professional presentation standards.

#### LLM Chat Interface

- **FR-006**: System MUST provide an LLM-powered chat interface that understands natural adviser language, enabling advisers to input queries or client data via natural language.

- **FR-007**: System MUST integrate with natural language processing services for natural language processing, receiving conversational responses formatted for professional use.

- **FR-008**: System MUST format LLM responses with structured replies and clickable commands, enabling advisers to act on recommendations efficiently.

- **FR-009**: System MUST maintain conversation context for client scenarios, enabling natural dialogue while preserving professional tone and accuracy.

#### Client Management

- **FR-010**: System MUST enable advisers to create and manage client records with demographics, goals, and financial data through natural language input or structured forms.

- **FR-011**: System MUST store client data and make it available for scenario modelling and future advice sessions, enabling efficient client relationship management.

- **FR-012**: System MUST support multiple clients per adviser, enabling advisers to work with multiple clients simultaneously without data confusion. When an adviser works with multiple clients simultaneously and needs to switch between client contexts, the system MUST provide a client switcher/context menu, maintain separate sessions per client with independent state, and enable quick switching without data loss or confusion.

- **FR-013**: System MUST allow advisers to import client data from external sources or enter it manually, supporting various data input methods.

#### Scenario Modelling and Forecasting

- **FR-014**: System MUST enable advisers to create and manage multiple scenarios per client, allowing comparison of different strategies, assumptions, or outcomes.

- **FR-015**: System MUST execute scenario calculations, retrieving results and maintaining full provenance.

- **FR-016**: System MUST present forecasts with professional line charts, bar graphs, and scenario tabs, enabling clear visualization of outcomes and comparisons.

- **FR-017**: System MUST support sensitivity analysis and stress-testing, allowing advisers to vary assumptions and see how outcomes change.

- **FR-018**: System MUST display forecasts with expandable tiles showing assumptions, inputs, and results, enabling advisers to understand and verify calculations.

#### Strategy Comparison

- **FR-019**: System MUST enable side-by-side comparison of multiple strategies or products, presenting comparative forecasts with clear visual differentiation.

- **FR-020**: System MUST highlight key differences between strategies, enabling advisers to explain why a recommended strategy serves the client's best interests.

- **FR-021**: System MUST support evidence-based recommendations by providing comparison data that demonstrates best-interests duty to clients and auditors.

#### Compliance and Validation

- **FR-022**: System MUST integrate with compliance validation services for compliance validation and requirement retrieval.

- **FR-023**: System MUST display compliance validation results clearly, showing compliance status, warnings, and required actions with links to regulatory requirements.

- **FR-024**: System MUST prevent generation of advice documents when compliance validation fails, ensuring only compliant advice is documented. When compliance validation fails and an adviser attempts to generate an advice document (SOA/ROA), the system MUST block document generation, display compliance failures clearly with specific guidance on what needs to be addressed, and require resolution of compliance issues before allowing document generation.

- **FR-025**: System MUST incorporate compliance results into generated documents, ensuring documentation matches compliance status and includes required disclosures.

#### Documentation Generation

- **FR-026**: System MUST generate Statement of Advice (SOA) and Record of Advice (ROA) automatically from client scenarios, including all calculations, compliance results, and recommendations.

- **FR-027**: System MUST include traceable explanations in generated documents, linking to authoritative references, rule versions, and calculation assumptions.

- **FR-028**: System MUST export documents in formats suitable for client presentation and regulatory submission, with full audit trails and compliance information.

- **FR-029**: System MUST ensure consistency between calculations, compliance results, and documentation, preventing discrepancies that could cause compliance issues.

- **FR-030**: System MUST generate print-ready PDFs using client-side browser print-to-PDF functionality with print-optimized CSS stylesheets, enabling professional document output suitable for client presentation and regulatory submission. Reference: `specs/001-master-spec/spec.md` CL-033.

- **FR-031**: System MUST provide SOA/ROA templates that include calculations, compliance results, recommendations, required disclosures, and traceable explanations linking to authoritative references, rule versions, and calculation assumptions. Reference: `specs/001-master-spec/spec.md` CL-033.

- **FR-032**: System MUST export evidence packs in both JSON (machine-readable) and PDF (human-readable) formats with version information, timestamps, and complete provenance chains. Reference: `specs/001-master-spec/spec.md` CL-033.

#### Audit Trail and Explainability

- **FR-033**: System MUST maintain a transparent audit log showing all advice logic, calculations, compliance checks, and changes with timestamps and reasoning trails.

- **FR-034**: System MUST provide access to explanation capabilities, enabling advisers to retrieve human-readable provenance chains for any calculation result.

- **FR-035**: System MUST enable export of audit trails suitable for regulatory review, including complete provenance chains with all calculations, compliance results, and regulatory references. When an adviser exports a compliance pack but some required documentation is missing or incomplete, the system MUST generate a partial compliance pack with available items, clearly mark missing items in the export, and allow export with warnings indicating what documentation is missing or incomplete.

- **FR-036**: System MUST support time-travel queries, enabling advisers to review historical advice using ruleset versions applicable at that time.

#### Performance and Efficiency

- **FR-037**: System MUST enable advisers to move from idea → input → output in seconds via chat interface, reducing time spent on data entry and technical calculations.

- **FR-038**: System MUST support fast scenario comparison, enabling advisers to model and compare multiple strategies efficiently without performance degradation.

- **FR-039**: System MUST provide quick access to client records and previous scenarios, enabling efficient workflow and reducing time spent searching for information.

---

### Key Entities

- **Client Record**: Professional client profile managed by adviser. Attributes include: client identifier, demographics (age, income, goals), financial data (assets, liabilities, superannuation), goals, risk tolerance, and relationship metadata. Linked to multiple scenarios and advice sessions.

- **Advice Session**: Single client engagement producing advice recommendations. Attributes include: session identifier, client identifier, date, scenarios modelled, calculations executed, compliance results, recommendations made, and documents generated. Maintains complete audit trail.

- **Strategy Comparison**: Side-by-side analysis of multiple strategies or products. Attributes include: comparison identifier, strategies compared, calculation results for each strategy, visualizations generated, and recommendation rationale. Used to demonstrate best-interests duty.

- **Advice Document**: Generated Statement or Record of Advice. Attributes include: document identifier, client identifier, session identifier, recommendations, calculations, compliance results, traceable explanations, and export format. Linked to source calculations and compliance validation.

- **Audit Log Entry**: Individual entry in audit trail. Attributes include: entry identifier, timestamp, action type (calculation, compliance check, document generation), details, user identifier, and links to related data (Facts, compliance evaluations). Maintains complete history of all actions.

- **Forecast Visualization**: Professional chart or graph displaying financial projections. Attributes include: visualization identifier, data source (Facts from Compute Engine), chart type (line, bar, comparison), time horizon, assumptions used, and presentation format. Generated for client presentation or analysis.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Advisers can model and compare three different strategies for a client in under 2 minutes from initial data entry to comparative forecast display.

- **SC-002**: Advisers can generate a Statement of Advice from a client scenario within 5 minutes, including all calculations, compliance results, and required disclosures.

- **SC-003**: 100% of advice recommendations generated through Veris Finance include compliance check results from Advice Engine, with warnings and required actions clearly displayed.

- **SC-004**: 95% of advisers successfully complete client scenario modelling using natural language input without requiring multiple clarification rounds.

- **SC-005**: Advisers can access audit trails and explanations for any recommendation within 2 seconds, enabling real-time transparency and compliance verification.

- **SC-006**: 90% of advisers successfully understand compliance warnings and required actions without requiring additional training or clarification.

- **SC-007**: System supports advisers working with up to 50 active clients simultaneously without performance degradation or data confusion.

- **SC-008**: 100% of generated advice documents include traceable explanations linking to authoritative references, rule versions, and calculation assumptions.

- **SC-009**: Advisers can export compliance packs suitable for regulatory submission within 3 minutes, including all required documentation and audit trails.

- **SC-010**: 85% of advisers report reduced time spent on administrative tasks (data entry, calculations, documentation) compared to traditional methods.

---

## Assumptions

### Domain Assumptions

- Advisers will primarily access Veris Finance via desktop or web interfaces (not mobile), enabling larger screens and more complex data visualizations.

- Advisers will prefer efficiency and speed over extensive customization options, valuing quick workflows over deep configuration.

- Advisers will work with multiple clients simultaneously, requiring efficient client management and scenario organization.

- Advisers will need to demonstrate compliance and auditability to regulators and clients, requiring comprehensive audit trails and explainability.

### Technical Assumptions

- Desktop/web interfaces will provide sufficient screen space for complex data visualizations and comparative dashboards.

- LLM Orchestrator will provide natural language processing with acceptable latency for professional workflows.

- Compute Engine will execute calculations within acceptable time limits for real-time scenario exploration.

- Advice Engine will validate compliance within acceptable time limits for seamless workflow integration.

### User Behavior Assumptions

- Advisers will prefer natural language input for speed, but will also use structured forms when precision is required.

- Advisers will value transparency and auditability, wanting to understand how calculations and recommendations are derived.

- Advisers will need to export documentation frequently for client presentation and regulatory submission.

- Advisers will work in sessions focused on individual clients, requiring efficient context switching between clients.

### Integration Assumptions

- Natural language processing services will transform natural language queries into structured requests that calculation services can execute.

- Calculation services will return calculation results in formats suitable for professional visualization and analysis.

- Compliance validation services will provide compliance validation results formatted appropriately for professional display and documentation.

- Backend services will maintain acceptable performance to support efficient professional workflows.

---

## Scope Boundaries

### In Scope (MVP)

- Core professional interface with LLM chat and data-centric visualizations

- Client record management with natural language and structured input

- Scenario modelling and forecasting with professional charts

- Strategy comparison with side-by-side analysis

- Compliance validation integration

- Basic documentation generation (SOA, ROA) with calculations and compliance results

- Audit log with transparent reasoning trails

- Time-travel queries for historical advice review

### Out of Scope (Future)

- Advanced client relationship management features beyond basic records

- Integration with external CRM or practice management systems

- Advanced document customization or branding beyond standard templates

- Multi-adviser collaboration or team features

- Advanced analytics or reporting beyond basic audit trails

- Integration with external product databases or marketplaces

- Advanced workflow automation or rule-based triggers

- Integration with external compliance databases or regulatory reporting systems

---

## Dependencies

### External Dependencies

- Desktop/web platform capabilities (sufficient screen space, processing power, connectivity)

- LLM provider APIs (via LLM Orchestrator) for natural language processing

- Web application platform or desktop framework for professional interface deployment

### Internal Dependencies

- Master specification (`001-master-spec`) for system context, requirements, and architectural constraints

- Natural language processing services for processing adviser queries

- Calculation services for executing financial calculations and scenario modelling

- Compliance validation services for validating compliance and generating compliance checklists

- Reference lookup services for citation generation and context enhancement

- Authentication/authorization system for adviser accounts and session management (from foundational infrastructure)
