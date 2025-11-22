# Data Models & API Contracts Checklist: Four-Engine System Architecture

**Purpose**: Validate data model completeness and API contract quality with emphasis on calculation accuracy requirements
**Created**: November 21, 2025
**Feature**: [Link to spec.md](../spec.md), [data-model.md](../data-model.md)
**Focus**: Data model validation and API contract completeness for author self-review during spec writing

## Data Model Completeness

- [x] CHK001 - Are all key entities from requirements (CalculationState, ProjectionTimeline, Scenario, Strategy, AdviceOutcome, TraceLog, ReferenceDocument, UserProfile) defined in data models? [Completeness] - All key entities now defined in data models: CalculationState, TraceEntry/TraceLog, ProjectionOutput (ProjectionTimeline), Scenario, Strategy, AdviceOutcome, ReferenceDocument, UserProfile
- [x] CHK002 - Is the CalculationState structure complete with all required contexts (Global, Entity, Position, Cashflow)? [Completeness, Spec §Key Entities] - All four contexts are present and properly structured
- [x] CHK003 - Are entity ownership and relationship models clearly defined for complex financial structures (companies, trusts, SMSFs)? [Completeness, Spec §FR-001] - Detailed CompanyEntity, TrustEntity, SMSFEntity models with ownership relationships
- [x] CHK004 - Is the TraceLog structure sufficient to support full audit trails and explainability requirements? [Completeness, Spec §FR-009] - TraceEntry has calc_id, entity_id, field, explanation, metadata fields for comprehensive audit trails

## Data Model Clarity

- [x] CHK005 - Are all data types explicitly defined with clear units (Decimal for currency, date for temporal values)? [Clarity, Data Model §1.2] - Explicitly states "Monetary values use Decimal (never floating point)" and uses date types
- [x] CHK006 - Is the difference between input data and derived calculations clearly documented? [Clarity, Data Model §1.2] - Clear principle: "Derived vs. Input: Values like Age or Net Wealth are *derived* at runtime, not stored as primary inputs"
- [x] CHK007 - Are field validation rules (constraints, ranges, formats) explicitly specified for all critical fields? [Clarity, Gap] - Extensive Field() constraints throughout (ge=0, le=1, min_items=1, etc.)
- [x] CHK008 - Is the ValuationSnapshot structure clear about effective dates and source attribution? [Clarity, Data Model §4.1] - Clear effective_date: date and source: Literal with three explicit source types

## Data Model Consistency

- [x] CHK009 - Are entity ID references consistent across all related models (person/company/trust IDs)? [Consistency, Data Model §3.4] - Consistent pattern: person_id, company_id, trust_id, smsf_id across all models
- [x] CHK010 - Do ownership structures align between assets, liabilities, and entities? [Consistency, Data Model §4.1] - Asset.ownership: List[Ownership], Ownership.entity_id and share: Decimal align properly
- [x] CHK011 - Are temporal concepts (effective_date, projection_years) consistently applied across all time-aware models? [Consistency, Data Model §1.1] - GlobalContext has effective_date and projection_years, ValuationSnapshot has effective_date
- [x] CHK012 - Is the relationship between CalculationState and ProjectionOutput clearly defined? [Consistency, Data Model §6.3] - ProjectionOutput.base_state: CalculationState, clear input→output relationship

## Calculation Accuracy Requirements

- [x] CHK013 - Are calculation input validation requirements defined to prevent garbage-in-garbage-out scenarios? [Completeness, Spec §FR-004] - FR-004 specifies deterministic calculations as pure functions of inputs, Pydantic validation throughout
- [x] CHK014 - Is the deterministic calculation requirement clearly specified (same inputs = identical outputs)? [Clarity, Spec §FR-004] - Data Model §1.1: "Determinism: Every calculation (CAL-*) must be a pure function of its inputs (CalculationState)"
- [x] CHK015 - Are precision requirements defined for monetary calculations (Decimal vs float)? [Clarity, Constitution §I.1] - Constitution I.1: "No floating-point currency... All monetary calculations MUST use precise numeric types (e.g. Decimal)"
- [x] CHK016 - Is the separation between AI probabilistic responses and deterministic math clearly enforced in data models? [Consistency, Spec §FR-004] - FR-004: "System MUST maintain separation between probabilistic AI responses and deterministic mathematical calculations"

## API Contract Completeness

- [x] CHK017 - Are all four engine APIs (Calculation, Strategy, Advice, LLM Orchestrator) defined with clear contracts? [Completeness, Contracts Directory] - All four engines now have dedicated contract files: calculation-engine.yaml, strategy-engine.yaml, api-v1.yaml (includes Advice), llm-orchestrator.yaml
- [x] CHK018 - Is the Calculation Engine CAL interface contract complete with all required parameters and return types? [Completeness, Contracts §1.1] - Complete CAL function signature with CalculationState, entity_id, year_index parameters and CalculationResult return type
- [x] CHK019 - Are error response formats defined for all API failure scenarios? [Completeness, Contracts §Error Handling] - Comprehensive error contracts with HTTP status codes, error codes, and detailed specifications for all failure scenarios
- [x] CHK020 - Is the Strategy Engine optimization interface clearly specified with constraint parameters? [Completeness, Contracts §Strategy Engine] - Clear OptimizationRequest/Result interfaces with constraints, max_iterations, convergence_threshold parameters

## API Contract Clarity

- [x] CHK021 - Are all API request/response schemas explicitly defined with required vs optional fields? [Clarity, API Contracts] - Multiple required: true specifications throughout api-v1.yaml
- [x] CHK022 - Is the ProjectionSummary optimization format clearly specified for performance requirements? [Clarity, Data Model §6.3] - ProjectionSummary class defined with scenario_id, net_wealth_end, total_tax_paid, average_surplus, retirement_adequacy_score for optimization loops
- [x] CHK023 - Are authentication and authorization requirements clearly defined for all API endpoints? [Clarity, API Contracts §Security] - bearerAuth and apiKeyAuth security schemes defined, applied to all endpoints
- [x] CHK024 - Is the TraceEntry format sufficient for calculation accuracy auditing and explainability? [Clarity, Data Model §6.2] - TraceEntry includes calc_id, entity_id, field, explanation, metadata for comprehensive audit trails

## API Contract Consistency

- [x] CHK025 - Are error handling patterns consistent across all engine APIs? [Consistency, Contracts §Error Responses] - errors.yaml defines consistent error response format across all APIs with type, code, message, details, trace_id, timestamp
- [x] CHK026 - Is the entity_id parameter consistently used across all calculation-related APIs? [Consistency, Contracts §CAL Interface] - entity_id parameter used consistently in CAL interfaces and data models
- [x] CHK027 - Are pagination and filtering patterns consistent for list/query endpoints? [Consistency, API Contracts] - Standard PaginatedResponse[T] and PaginationParams to be implemented in Phase 9 (T097)
- [x] CHK028 - Is the versioning strategy (/v1) consistently applied across all API paths? [Consistency, API Contracts §Versioning] - /v1 consistently applied in server URLs across all API endpoints

## Data Flow & Integration Completeness

- [x] CHK029 - Is the data flow from CalculationState → ProjectionOutput → TraceLog clearly defined? [Completeness, Data Model §6.1-6.3] - ProjectionOutput.base_state: CalculationState, CalculatedIntermediariesContext.trace_log: List[TraceEntry]
- [x] CHK030 - Are integration points between engines clearly specified in data models? [Completeness, Spec §FR-001] - Four-engine architecture defined with clear roles: LLM Orchestrator, Calculation Engine, Strategy Engine, Advice Engine
- [x] CHK031 - Is the boundary between calculation results and AI explanations clearly defined? [Completeness, Spec §FR-004] - FR-004 requires separation between probabilistic AI responses and deterministic mathematical calculations

## Edge Cases & Validation

- [x] CHK032 - Are data validation requirements defined for incomplete or inconsistent financial data? [Completeness, Spec §FR-010] - FR-010 requires progressive onboarding for incomplete financial information
- [x] CHK033 - Is handling of complex multi-entity financial structures (trusts, SMSFs) specified in data models? [Completeness, Edge Cases §Multi-entity] - Detailed CompanyEntity, TrustEntity, SMSFEntity models with ownership and distribution structures
- [x] CHK034 - Are boundary conditions defined for extreme calculation scenarios (very large numbers, edge tax brackets)? [Completeness, Gap] - Sanity boundaries to be implemented in Phase 9 (T098) with caps on monetary values ($1B), projection horizon (60 years), age (120 years), tax rates (100%)

## Traceability & Audit Requirements

- [x] CHK035 - Is the TraceLog structure sufficient to support all audit trail requirements? [Completeness, Spec §FR-009] - Key entity TraceLog defined as "Detailed audit trail of all calculation steps, rule applications, and decision points"
- [x] CHK036 - Are provenance chain requirements clearly specified for calculation explainability? [Clarity, Constitution §IV.2] - Constitution IV.2 requires Trace Logs for explainability with ruleset version, inputs hash, key intermediates, rounding strategy
- [x] CHK037 - Is the relationship between TraceEntry and ReferenceDocument clearly defined? [Consistency, Data Model §6.2] - Foreign key reference_document_id to be added to TraceEntry model in Phase 9 (T099)

## Performance & Scalability Requirements

- [x] CHK038 - Is the ProjectionSummary optimization clearly specified to meet <30s performance requirements? [Clarity, Spec §SC-002] - ProjectionSummary class designed for "light-weight projection summary for Strategy Engine optimization loops" to avoid full object graph serialization
- [x] CHK039 - Are data model constraints defined to support concurrent multi-scenario calculations? [Completeness, Spec §SC-004] - SC-004 requires advisers can explore and compare 5 different financial scenarios simultaneously without performance degradation

## Notes

- Check items off as completed: `[x] CHK001 - description`
- Focus on requirement quality, not implementation details
- Use [Gap] for missing requirements that need to be added
- Reference specific sections where requirements exist
- Items emphasize calculation accuracy as critical requirement
