---

description: "Task list for Four-Engine System Architecture implementation"
---

# Tasks: Four-Engine System Architecture

**Feature Branch**: `001-four-engine-architecture`
**Input**: Design documents from `/specs/001-four-engine-architecture/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Tests**: The specification does not explicitly request TDD approach, so tests are NOT included in this task breakdown.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- **[IA]**: Relates to Interaction Architecture models defined in @specs/001-four-engine-architecture/design/interaction_architecture.md
- **[WM]**: Relates to Workflow Modes defined in @specs/001-four-engine-architecture/design/workflows_and_modes.md
- Include exact file paths in descriptions
- **Functional Requirements Mapping**: Tasks now include explicit FR-* references for traceability

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend project structure per plan.md in backend/src/
- [x] T002 [P] Create shared schemas library in shared/schemas/ with Pydantic models from data-model.md
- [x] T003 [P] Set up PostgreSQL database with SQLAlchemy models for core entities
- [x] T004 [P] [FR-008, FR-017, FR-018] Configure Clerk authentication middleware in backend/src/auth/
- [x] T005 [P] Initialize FastAPI application with basic routing structure in backend/src/main.py
- [x] T006 [P] Set up environment configuration management with Pydantic settings
- [x] T006b [P] Set up 'openapi-typescript-codegen' script to auto-generate frontend types from FastAPI openapi.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 [FR-001, FR-004, FR-009] Implement CalculationState and ProjectionOutput models in shared/schemas/calculation.py
- [x] T008 [P] [FR-009] Implement TraceLog mechanism in shared/schemas/orchestration.py with CAL-* ID traceability
- [x] T009 [P] [FR-001, FR-004, SC-001] Build Calculation Engine core with MVP Core tier calculations (CAL-PIT-001 to 005, CAL-CGT-001 to 002, CAL-SUP-002 to 009, CAL-PFL-104)
- [x] T009b [P] Implement 'RuleLoader' service to hydrate Calculation Engine parameters from external config files (YAML/JSON) rather than hardcoding
- [x] T010 Implement Projection Engine for year-over-year calculations in backend/src/engines/calculation/
- [x] T011 [P] Create database models for UserProfile, Scenario, Strategy, AdviceOutcome in backend/src/models/
- [x] T012 [P] Set up database migration system with Alembic
- [x] T013 [P] Implement basic CRUD operations for scenarios in backend/src/services/scenario_service.py
- [x] T014 [P] Create API router structure following contracts/api-v1.yaml
- [x] T015 [P] Add request validation and error handling middleware
- [x] T016 [P] [SC-005] Implement health check endpoint (/health) following contracts/api-v1.yaml
- [x] T016b [P] Build 'Dev Dashboard' (simple HTML/JS) to visualize real-time TraceLogs, Engine States, and Rule sets for debugging before building the full UI

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 2.35: Calculation Engine Refactor (Critical Tech Debt)

**Purpose**: Refactor the Calculation Engine from monolithic `__init__.py` to modular structure defined in @conditional_rules/calc_architecture_guide.md to support Extended Tier growth.

**⚠️ CRITICAL**: This phase must complete before Extended Tier calculations can be implemented. Addresses technical debt from MVP Core tier implementation.

### Phase 2.35a: Structure & RuleLoader (Do this first)

- [x] T017a Create the folder `backend/src/engines/calculation/domains/` and an empty `__init__.py` inside it.
- [x] T017b [P] Create `backend/src/engines/calculation/registry.py`.
- [x] T017c [P] Create `backend/src/services/rule_loader.py`. Implement a `RuleLoader` class that loads configuration from a dummy dictionary for now (we will connect YAML later). It should have methods like `get_tax_brackets()` and `get_concessional_cap()`.

### Phase 2.35b: Migration (Do this second)

- [x] T017d Create `backend/src/engines/calculation/domains/tax_personal.py`. Move `run_CAL_PIT_001`, `_002`, `_004`, `_005` from `__init__.py` to this file. Update them to use `RuleLoader` instead of hardcoded values.
- [x] T017e [P] Create `backend/src/engines/calculation/domains/cgt.py`. Move `run_CAL_CGT_001`, `_002` to this file.
- [x] T017f [P] Create `backend/src/engines/calculation/domains/superannuation.py`. Move `run_CAL_SUP_002`, `_003`, `_007`, `_008`, `_009` to this file.
- [x] T017g [P] Create `backend/src/engines/calculation/domains/property.py`. Move `run_CAL_PFL_104` to this file.

### Phase 2.35c: Wiring (Do this last)

- [x] T017h Update `backend/src/engines/calculation/registry.py` to import these new modules and register all 12 functions in a `CALCULATION_REGISTRY` dict.
- [x] T017i Refactor `backend/src/engines/calculation/__init__.py` to remove the actual logic and instead expose a generic `run_calculation(cal_id, ...)` function that delegates to the Registry.
- [x] T017j Update `backend/src/engines/calculation/projection.py` to use the Registry lookup instead of importing functions directly.

**Validation**:
- [x] T017k Ensure all tests pass and that `run_CAL_PIT_001` can still be called via the Registry.

---

## Phase 2.5: LLM Connection & Future Workflow Integration

**Purpose**: Establish OpenRouter LLM connection and integrate LLM capabilities into all future workflows

**⚠️ CRITICAL**: This phase must complete before any user story can use LLM features. Ensures prompt management, connection stability, and workflow integration patterns are established.

### 2.5.1 Domain Knowledge Base Setup

- [ ] T017 [FR-019] Create LLM source materials directory structure in /specs/001-four-engine-architecture/llm-source-materials/ following README.md
- [ ] T018 [P] [FR-019] Create Australian Financial System primer in /specs/001-four-engine-architecture/llm-source-materials/australian-financial-system.md
- [ ] T019 [P] [FR-019] Create Financial Advice Process guide in /specs/001-four-engine-architecture/llm-source-materials/financial-advice-process.md
- [ ] T020 [P] [FR-019] Create Regulatory Environment overview in /specs/001-four-engine-architecture/llm-source-materials/regulatory-environment.md
- [ ] T021 [P] [FR-019] Create Interaction Patterns library in /specs/001-four-engine-architecture/llm-source-materials/interaction-patterns.md
- [ ] T022 [P] [FR-019] Create domain-specific knowledge bases in /specs/001-four-engine-architecture/llm-source-materials/domain-knowledge/ (tax-regime.md, superannuation.md, property-investment.md, retirement-planning.md, insurance.md)
- [ ] T023 [FR-019] Create source materials catalog.json in /specs/001-four-engine-architecture/llm-source-materials/catalog.json with metadata tracking

### 2.5.2 Prompt Management System

- [ ] T024 [FR-019] Create LLM prompts directory structure in /specs/001-four-engine-architecture/llm-prompts/ following README.md
- [ ] T025 [P] [FR-019] Set up prompt catalog system in /specs/001-four-engine-architecture/llm-prompts/catalog.json
- [ ] T026 [P] [FR-019] Create core orchestrator prompts in /specs/001-four-engine-architecture/llm-prompts/core-orchestrator/ (intent-recognition.md, state-hydration.md, strategy-nomination.md, narrative-generation.md)
- [ ] T027 [P] [FR-019] Create shared utilities in /specs/001-four-engine-architecture/llm-prompts/shared-utilities/ (privacy-filter.md, rag-retrieval.md, error-handling.md, conversation-context.md)
- [ ] T028 [P] [FR-019] Create mode-specific prompt templates in /specs/001-four-engine-architecture/llm-prompts/mode-prompts/ for all 26 modes (mode-01-fact-check.md through mode-26-system-oracle.md)
- [ ] T029 [FR-019] Implement prompt loading utilities in backend/src/services/prompt_service.py following README.md patterns

### 2.5.3 OpenRouter LLM Connection

- [ ] T030 [FR-019] Implement OpenRouter client in backend/src/services/openrouter_client.py with error handling and rate limiting
- [ ] T031 [FR-019] Create LLM service abstraction layer in backend/src/services/llm_service.py with connection testing
- [ ] T032 [P] [FR-019] Add environment configuration for OpenRouter API key and model selection
- [ ] T033 [P] [FR-019] Implement connection health checks and monitoring in backend/src/services/llm_service.py
- [ ] T034 [FR-019] Create LLM response parsing and validation utilities in backend/src/utils/llm_parsing.py
- [ ] T035 [FR-019] Add LLM cost tracking and usage monitoring in backend/src/services/llm_service.py

### 2.5.4 Future Workflow Integration Patterns

- [ ] T036 [FR-019] Create LLM Orchestrator base class in backend/src/engines/llm/orchestrator.py with prompt loading patterns
- [ ] T037 [P] [FR-019] Implement state hydration patterns in backend/src/engines/llm/state_hydration.py for converting natural language to CalculationState
- [ ] T038 [P] [FR-019] Build narrative generation templates in backend/src/engines/llm/narrative_generation.py for human-readable outputs
- [ ] T039 [P] [FR-019] Create privacy filtering utilities in backend/src/engines/llm/privacy_filter.py for PII redaction
- [ ] T040 [P] [FR-019] Implement intent recognition patterns in backend/src/engines/llm/intent_recognition.py for mode selection
- [ ] T041 [FR-019] Add TraceLog integration for LLM operations with CAL-* ID tracking in backend/src/engines/llm/orchestrator.py

**Checkpoint**: LLM connection established and integrated into workflow patterns - all future LLM-dependent features can now be implemented

---

## Phase 3: User Story 1 - Consumer Fact Check 🎯 MVP

**Goal**: Enable consumers to ask factual questions about their financial situation and receive accurate, deterministic answers grounded in verified calculations

**Independent Test**: Can be fully tested by asking factual questions and verifying answers match expected calculations based on provided financial data

### Implementation for User Story 1

- [ ] T042 [US1] Implement Person entity model in shared/schemas/entities.py with demographics and relationships
- [ ] T043 [P] [US1] Implement Asset models (PropertyAsset, SuperAccount) in shared/schemas/assets.py
- [ ] T044 [P] [US1] Implement Liability models (Loan) in shared/schemas/assets.py
- [ ] T045 [P] [US1] Implement EntityContext and FinancialPositionContext in shared/schemas/entities.py
- [ ] T046 [US1] Implement CashflowContext with EntityCashflow in shared/schemas/cashflow.py
- [ ] T047 [US1] [IA MOD-001] [WM Mode 1] Create fact check endpoint (/api/v1/modes/fact-check) following contracts/api-v1.yaml
- [ ] T048 [US1] [IA MOD-001] [WM Mode 1] Implement LLM Orchestrator intent recognition for fact questions in backend/src/engines/llm/ (MVP with proper IntentRecognitionResult schema)
- [ ] T049 [US1] [IA MOD-001] [WM Mode 1] Build state hydration for basic financial data input in backend/src/engines/llm/
- [ ] T050 [US1] [IA MOD-001] [WM Mode 1] Connect Calculation Engine to fact check endpoint for net wealth and tax calculations
- [ ] T051 [US1] [IA MOD-001] [WM Mode 1] Add narrative generation for calculation results in backend/src/engines/llm/ (with NarrativeGenerationResult schema)
- [ ] T052 [US1] [IA MOD-001] [WM Mode 1] Implement privacy filtering for fact check responses
- [ ] T053 [US1] [IA MOD-001] [WM Mode 1] Add TraceLog integration for fact check calculations with CAL-* IDs

**Checkpoint**: User Story 1 should be fully functional and independently testable

---

## Phase 4: User Story 2 - Consumer Strategy Exploration (Priority: P1)

**Goal**: Enable consumers to explore "what-if" scenarios to understand different financial strategies

**Independent Test**: Can be fully tested by comparing baseline scenarios against alternative strategies and verifying the projected outcomes are mathematically consistent

### Implementation for User Story 2

- [ ] T054 [US2] [IA MOD-002] [WM Mode 4] Extend CalculationState with scenario management in shared/schemas/calculation.py
- [ ] T055 [US2] [IA MOD-003] [WM Mode 3] Implement Strategy model in shared/schemas/orchestration.py with target metrics and constraints
- [ ] T056 [US2] [IA MOD-002] [WM Mode 4] Create scenario comparison endpoint (/api/v1/scenarios/compare) following contracts/api-v1.yaml
- [ ] T057 [US2] [IA MOD-003] [WM Mode 3] Build Strategy Engine for basic optimization loops in backend/src/engines/strategy/
- [ ] T058 [US2] [IA MOD-002] [WM Mode 4] Implement scenario creation and storage with database persistence
- [ ] T059 [US2] [IA MOD-002] [WM Mode 4] Add scenario modification capabilities for "what-if" analysis
- [ ] T060 [US2] [IA MOD-002] [WM Mode 4] Connect Projection Engine to scenario analysis for multi-year outcomes
- [ ] T061 [US2] [IA MOD-003] [WM Mode 3] Implement side-by-side comparison narratives in backend/src/engines/llm/
- [ ] T062 [US2] [IA MOD-003] [WM Mode 3] Add educational explanations for strategy impacts
- [ ] T063 [US2] [IA MOD-002] [WM Mode 4] Extend TraceLog for scenario comparison operations

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Adviser Comprehensive Planning (Priority: P1)

**Goal**: Enable advisers to create comprehensive financial plans with strategy optimization, compliance checking, and regulatory governance

**Independent Test**: Can be fully tested by running a complete planning workflow and verifying all governance checks pass for approved strategies

### Implementation for User Story 3

- [ ] T064 [US3] [IA MOD-004] [WM Mode 6] Implement AdviceOutcome model for compliance results in shared/schemas/orchestration.py
- [ ] T065 [US3] [IA MOD-004] [WM Mode 6] Build Advice Engine for regulatory compliance checking in backend/src/engines/advice/
- [ ] T066 [US3] [IA MOD-004] [WM Mode 6] Create comprehensive planning endpoint (/api/v1/modes/comprehensive-plan) following contracts/api-v1.yaml
- [ ] T067 [US3] [IA MOD-004] [WM Mode 6] Implement Best Interest Duty (BID) validation rules in backend/src/engines/advice/
- [ ] T068 [US3] [IA MOD-004] [WM Mode 6] Add multi-domain strategy optimization (debt, super, tax, investment)
- [ ] T069 [US3] [IA MOD-004] [WM Mode 6] Build compliance checking integration with Strategy Engine
- [ ] T070 [US3] [IA MOD-004] [WM Mode 14] Implement structured action plans and milestone tracking
- [ ] T071 [US3] [IA MOD-004] [WM Mode 6] Add adviser-specific narrative generation for client communication
- [ ] T072 [US3] [IA MOD-004] [WM Mode 6] Extend TraceLog for comprehensive planning with rule citations
- [ ] T073 [US3] [IA MOD-004] [WM Mode 6] Implement audit trail retrieval endpoint (/api/v1/trace/{scenario_id})

**Checkpoint**: All core user stories (US1, US2, US3) should now be independently functional

---

## Phase 6: User Story 4 - System Health Monitoring (Priority: P2)

**Goal**: Enable system administrators and compliance officers to monitor ongoing performance and regulatory compliance

**Independent Test**: Can be fully tested by triggering rule changes and verifying the system correctly identifies impacted clients and re-evaluates their strategies

### Implementation for User Story 4

- [ ] T074 [US4] [IA MOD-009] [WM Mode 7] Implement regulatory rule monitoring system in backend/src/services/rule_monitor.py
- [ ] T075 [US4] [IA MOD-009] [WM Mode 7] Create system health dashboard endpoint (/api/v1/admin/health) following contracts/api-v1.yaml
- [ ] T076 [US4] [IA MOD-010] [WM Mode 11] Build compliance audit capabilities across all scenarios
- [ ] T077 [US4] [IA MOD-009] [WM Mode 7] Implement automated rule change detection and client impact analysis
- [ ] T078 [US4] [IA MOD-010] [WM Mode 22] Add performance monitoring and diagnostic endpoints
- [ ] T079 [US4] [IA MOD-010] [WM Mode 22] Implement application-level metrics collection (response times, engine performance)
- [ ] T080 [US4] [IA MOD-010] [WM Mode 22] Add infrastructure monitoring (CPU, memory, database queries)
- [ ] T081 [US4] [IA MOD-010] [WM Mode 22] Create performance testing framework with load/stress testing
- [ ] T082 [US4] [IA MOD-010] [WM Mode 22] Implement caching layer for calculation optimization (SC-001, SC-002, SC-004)
- [ ] T083 [US4] [IA MOD-009] [WM Mode 7] Create compliance officer access controls with RBAC metadata
- [ ] T084 [US4] [IA MOD-009] [WM Mode 7] Implement bulk scenario re-evaluation for rule changes
- [ ] T085 [US4] [IA MOD-009] [WM Mode 7] Add system monitoring alerts and notifications
- [ ] T086 [US4] [IA MOD-009] [WM Mode 7] Extend TraceLog for compliance monitoring operations

**Checkpoint**: User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Collaborative Client Sessions (Priority: P2)

**Goal**: Enable advisers to work with clients in real-time scenario exploration with background calculations and compliance guidance

**Independent Test**: Can be fully tested by simulating a live session with scenario changes and verifying real-time updates and compliance warnings

### Implementation for User Story 5

- [ ] T087 [US5] [IA MOD-002] [WM Mode 16] Implement optimistic UI support with background sync in backend/src/services/collaboration.py
- [ ] T088 [US5] [IA MOD-002] [WM Mode 16] Create collaborative session endpoints (/api/v1/sessions/) following contracts/api-v1.yaml
- [ ] T089 [US5] [IA MOD-002] [WM Mode 16] Add real-time scenario update capabilities with conflict detection
- [ ] T090 [US5] [IA MOD-002] [WM Mode 16] Implement session-based scenario modifications
- [ ] T091 [US5] [IA MOD-002] [WM Mode 16] Build background compliance checking during live sessions
- [ ] T092 [US5] [IA MOD-002] [WM Mode 16] Add immediate adviser warnings for compliance issues
- [ ] T093 [US5] [IA MOD-002] [WM Mode 16] Implement session state persistence and recovery
- [ ] T094 [US5] [IA MOD-002] [WM Mode 16] Create meeting notes and action item generation
- [ ] T095 [US5] [IA MOD-002] [WM Mode 16] Extend TraceLog for collaborative session operations

**Checkpoint**: User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Educational Guidance (Priority: P3)

**Goal**: Provide accurate educational responses about financial concepts based on authoritative sources

**Independent Test**: Can be fully tested by asking educational questions and verifying responses are based on authoritative financial sources

### Implementation for User Story 6

- [ ] T096 [US6] [IA MOD-001] [WM Mode 24] [FR-007] Implement RAG system for knowledge retrieval in backend/src/services/rag_service.py
- [ ] T097 [US6] [IA MOD-001] [WM Mode 24] Create educational content endpoints (/api/v1/education/) following contracts/api-v1.yaml
- [ ] T098 [US6] [IA MOD-001] [WM Mode 24] [FR-019] Build LLM integration with OpenRouter for educational responses
- [ ] T099 [US6] [IA MOD-001] [WM Mode 24] Implement privacy filtering for educational content
- [ ] T100 [US6] [IA MOD-001] [WM Mode 24] Add authoritative source citations and references
- [ ] T101 [US6] [IA MOD-001] [WM Mode 24] Create transition logic from education to personalized calculations
- [ ] T102 [US6] [IA MOD-001] [WM Mode 24] Build knowledge base loading from markdown files
- [ ] T103 [US6] [IA MOD-001] [WM Mode 24] Implement educational narrative generation
- [ ] T104 [US6] [IA MOD-001] [WM Mode 24] Add educational content validation and quality checks

### Reference Materials System Implementation (FR-007)

- [ ] T105 [IA MOD-007] [FR-007] Create reference materials storage structure in /specs/001-four-engine-architecture/reference-materials/
- [ ] T106 [IA MOD-007] [FR-007] Implement regulatory document ingestion pipeline for ASIC/ATO content
- [ ] T107 [IA MOD-007] [FR-007] Build citation and attribution system with version tracking
- [ ] T108 [IA MOD-007] [FR-007] Create rule validation library with JSON/YAML schemas
- [ ] T109 [IA MOD-007] [FR-007] Implement search and retrieval API endpoints
- [ ] T110 [IA MOD-007] [FR-007] Add content quality assurance and SME review workflow
- [ ] T111 [IA MOD-007] [FR-007] Integrate reference materials with Calculation Engine rule lookup

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T112 [P] Add comprehensive error handling and user-friendly error messages across all endpoints
- [ ] T113 [P] Implement comprehensive logging and monitoring with Sentry integration
- [ ] T114 [P] [SC-001] Add performance optimization for calculation loops targeting SC-001 (5-second responses)
- [ ] T115 [P] Implement data validation and integrity checks for all financial inputs
- [ ] T116 [P] Add security hardening and input sanitization
- [ ] T117 [P] Create comprehensive API documentation with OpenAPI spec generation
- [ ] T118 [P] Implement backup and recovery procedures for scenarios
- [ ] T119 [P] Add environment-specific configuration management
- [ ] T120 [P] Create deployment configuration for Render backend and Vercel frontend
- [ ] T121 [P] Run quickstart.md validation and update documentation

### Specification Gap Solutions

- [ ] T122 [P] [CHK027] Implement standard PaginatedResponse[T] generic and PaginationParams dependency across all list endpoints (Scenarios, Clients, Audit Logs) in contracts/api-v1.yaml
- [ ] T123 [P] [CHK034] Add sanity boundary constraints to Pydantic models: monetary cap ($1B), projection horizon (60 years), age limits (120 years), tax rate cap (100%) in shared/schemas/
- [ ] T124 [P] [CHK037] Add reference_document_id foreign key to TraceEntry model linking calculation steps to regulatory sources in shared/schemas/orchestration.py

### Logic Factory Implementation (FR-016)

- [ ] T125 [P] [IA MOD-010] [WM Mode 15] Create Logic Factory API endpoints (/api/v1/logic-factory/) following contracts/api-v1.yaml
- [ ] T126 [P] [IA MOD-010] [WM Mode 15] Implement code generation engine with template-based CAL-* patterns in backend/src/services/logic_factory.py
- [ ] T127 [P] [IA MOD-010] [WM Mode 15] Build validation pipeline (syntax, schema, reference audit) for generated code
- [ ] T128 [P] [IA MOD-010] [WM Mode 15] Add sandbox execution environment for safe code testing
- [ ] T129 [P] [IA MOD-010] [WM Mode 15] Implement human-in-the-loop review workflow with audit trails
- [ ] T130 [P] [IA MOD-010] [WM Mode 15] Create web interface for Logic Factory management and code review
- [ ] T131 [P] [IA MOD-010] [WM Mode 15] Integrate Logic Factory with TraceLog system for CAL-* ID tracking

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **LLM Connection (Phase 2.5)**: Depends on Foundational completion - BLOCKS LLM-dependent features
- **User Stories (Phase 3+)**: All depend on Foundational + LLM Connection phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent monitoring capabilities
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Builds on US1-US3 but independently testable
- **User Story 6 (P6)**: Can start after Foundational (Phase 2) - Independent educational content system

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Implement Person entity model in shared/schemas/entities.py"
Task: "Implement Asset models (PropertyAsset, SuperAccount) in shared/schemas/assets.py"
Task: "Implement Liability models (Loan) in shared/schemas/assets.py"
Task: "Implement EntityContext and FinancialPositionContext in shared/schemas/entities.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 2.5: LLM Connection (CRITICAL - enables LLM features)
4. Complete Phase 3: User Story 1
5. **STOP and VALIDATE**: Test User Story 1 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Complete LLM Connection → LLM features enabled
3. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
4. Add User Story 2 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Team completes LLM Connection together (Phase 2.5)
3. Once Foundational + LLM Connection are done:
   - Developer A: User Story 1 (Consumer Fact Check - MVP priority)
   - Developer B: User Story 2 (Strategy Exploration)
   - Developer C: User Story 3 (Adviser Planning)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Exact file paths provided for each task
- Verify tasks fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Interaction Architecture & Workflow Mode Mapping

This section highlights how tasks relate to the **10 Interaction Models** (IA) and **26 Workflow Modes** (WM) defined in the design documents:

### Interaction Models Coverage
- **[IA MOD-001] Conversational Insight**: Tasks implementing fact checking, crystal ball projections, and conversational guidance
  - **Mode 1 (Fact Check)**: T022-T028 (US1 - Consumer Fact Check)
  - **Mode 2 (Crystal Ball)**: Partially covered by T022-T028 (educational projection narratives)
  - **Mode 24 (Conversational Guide)**: T071-T079 (US6 - Educational Guidance)
- **[IA MOD-002] Scenarios & Comparison**: Tasks for scenario creation, comparison, and collaborative modeling
  - **Mode 4 (Adviser Sandbox)**: T029-T038 (US2 - Strategy Exploration)
  - **Mode 16 (Collaborative Session)**: T062-T070 (US5 - Collaborative Client Sessions)
- **[IA MOD-003] Strategy & Optimization**: Tasks for strategy exploration and optimization
  - **Mode 3 (Strategy Explorer)**: T029-T038 (US2 - Strategy Exploration)
- **[IA MOD-004] Comprehensive Advice & Governance**: Tasks for holistic planning and implementation
  - **Mode 6 (Holistic Plan)**: T039-T048 (US3 - Adviser Comprehensive Planning)
  - **Mode 14 (Implementation Orchestrator)**: T045 (within US3)
- **[IA MOD-005] Data Quality & Onboarding**: Tasks for progressive data collection and validation
  - **Mode 12 (Progressive Mapper)**: Partially covered by foundational data quality tasks (T012, T015)
- **[IA MOD-006] Privacy**: Cross-cutting privacy filtering across all modes
  - Covered by T027, T074 (privacy filtering in fact check and educational responses)
- **[IA MOD-007] Reference/RAG**: Authoritative reference materials and retrieval
  - **Reference Materials System**: T080-T086 (regulatory document ingestion and RAG)
- **[IA MOD-008] API Integration**: Stable API endpoints for partners
  - Covered by various endpoint creation tasks (T022, T031, T041, etc.)
- **[IA MOD-009] Operational Monitoring**: Background regulatory monitoring
  - **Mode 7 (Proactive Monitor)**: T049-T061 (US4 - System Health Monitoring)
- **[IA MOD-010] QA & Technical Assurance**: Testing and validation frameworks
  - **Modes 11, 15, 17-23, 26**: T051-T061 (US4), T097-T103 (Logic Factory/Rule Lab)

### Key Implementation Notes
- **MVP Priority**: Tasks for US1 (Mode 1) should be completed first for basic functionality
- **Core User Journeys**: US1-US3 cover the most critical interaction models (MOD-001, MOD-002, MOD-003, MOD-004)
- **Advanced Features**: US4-US6 add monitoring, collaboration, and educational capabilities
- **Cross-cutting**: Privacy (MOD-006), RAG (MOD-007), and QA (MOD-010) span multiple user stories
- **Foundational Tasks**: T007-T016 provide the engine infrastructure needed by all interaction models

---

## Requirements Traceability Matrix

### Functional Requirements Coverage

| Requirement | Description | Primary Tasks |
|-------------|-------------|---------------|
| **FR-001** | Four distinct computational engines | T007, T009, T032, T040, T052 |
| **FR-002** | 10 interaction models | *(See design/interaction_architecture.md)* |
| **FR-003** | 26 operational modes | *(See design/workflows_and_modes.md)* |
| **FR-004** | Separation between AI and deterministic calculations | T007, T009, T073 |
| **FR-005** | Regulatory compliance checks (BID) | T040, T042 |
| **FR-006** | Real-time calculation capabilities | T032, T089 |
| **FR-007** | Authoritative reference materials | T071-T079, T080-T086 *(RAG + Reference Materials System)* |
| **FR-008** | Multi-user support with Clerk auth | T004, T005 |
| **FR-009** | Comprehensive audit trails | T007, T008, T028, T038, T047 |
| **FR-010** | Data quality assessment | T012, T015 |
| **FR-011** | Privacy and safety filtering | T027, T074 |
| **FR-017** | HTTPS-only with JWT tokens | T004 |
| **FR-018** | Role-based data segregation | T004 |
| **FR-019** | OpenRouter LLM integration | T073 |
| **FR-020** | Exclude bank feed integrations | *(By design - no tasks needed)* |

### Success Criteria Coverage

| Success Criteria | Description | Primary Tasks |
|------------------|-------------|---------------|
| **SC-001** | 5-second fact check responses | T009, T089, T053-T061 *(Performance monitoring & optimization)* |
| **SC-002** | 30-second complex optimizations | T032, T089, T053-T061 *(Performance monitoring & optimization)* |
| **SC-003** | 95% compliance check pass rate | T040, T042 |
| **SC-004** | 100 concurrent users, 50 scenarios | T089, T094, T053-T061 *(Performance monitoring & optimization)* |
| **SC-005** | 99.9% availability | T016 |
| **SC-006** | Complete audit trails | T008, T047 |
| **SC-007** | 100% regulatory change detection | T049-T052 |
| **SC-008** | Real-time updates across 100 users | T062-T070 |
| **SC-009** | Authoritative educational citations | T071-T079 |
| **SC-010** | Optimistic UI updates < 100ms | *(Frontend - not in scope)* |

---

## Coverage Statistics

- **Total Tasks**: 159
- **Total Requirements**: 20 FR + 9 SC = 29
- **Requirements with Task Coverage**: 20/29 (69%)
- **Requirements Fully Covered**: 16/29 (55%)
- **Requirements Needing Tasks**: FR-002, FR-003 (design docs exist but may need API endpoint tasks)

**Note**: FR-002 and FR-003 are covered by design documents but may need additional implementation tasks for the mode-specific logic and API endpoints. FR-016 now has detailed specification and implementation tasks.