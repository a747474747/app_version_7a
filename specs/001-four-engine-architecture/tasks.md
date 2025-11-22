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

- [ ] T001 Create backend project structure per plan.md in backend/src/
- [ ] T002 [P] Create shared schemas library in shared/schemas/ with Pydantic models from data-model.md
- [ ] T003 [P] Set up PostgreSQL database with SQLAlchemy models for core entities
- [ ] T004 [P] [FR-008, FR-017, FR-018] Configure Clerk authentication middleware in backend/src/auth/
- [ ] T005 [P] Initialize FastAPI application with basic routing structure in backend/src/main.py
- [ ] T006 [P] Set up environment configuration management with Pydantic settings

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 [FR-001, FR-004, FR-009] Implement CalculationState and ProjectionOutput models in shared/schemas/calculation.py
- [ ] T008 [P] [FR-009] Implement TraceLog mechanism in shared/schemas/orchestration.py with CAL-* ID traceability
- [ ] T009 [P] [FR-001, FR-004, SC-001] Build Calculation Engine core with MVP Core tier calculations (CAL-PIT-001 to 005, CAL-CGT-001 to 002, CAL-SUP-002 to 009, CAL-PFL-104)
- [ ] T010 Implement Projection Engine for year-over-year calculations in backend/src/engines/calculation/
- [ ] T011 [P] Create database models for UserProfile, Scenario, Strategy, AdviceOutcome in backend/src/models/
- [ ] T012 [P] Set up database migration system with Alembic
- [ ] T013 [P] Implement basic CRUD operations for scenarios in backend/src/services/scenario_service.py
- [ ] T014 [P] Create API router structure following contracts/api-v1.yaml
- [ ] T015 [P] Add request validation and error handling middleware
- [ ] T016 [P] [SC-005] Implement health check endpoint (/health) following contracts/api-v1.yaml

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Consumer Fact Check 🎯 MVP

**Goal**: Enable consumers to ask factual questions about their financial situation and receive accurate, deterministic answers grounded in verified calculations

**Independent Test**: Can be fully tested by asking factual questions and verifying answers match expected calculations based on provided financial data

### Implementation for User Story 1

- [ ] T017 [US1] Implement Person entity model in shared/schemas/entities.py with demographics and relationships
- [ ] T018 [P] [US1] Implement Asset models (PropertyAsset, SuperAccount) in shared/schemas/assets.py
- [ ] T019 [P] [US1] Implement Liability models (Loan) in shared/schemas/assets.py
- [ ] T020 [P] [US1] Implement EntityContext and FinancialPositionContext in shared/schemas/entities.py
- [ ] T021 [US1] Implement CashflowContext with EntityCashflow in shared/schemas/cashflow.py
- [ ] T022 [US1] [IA MOD-001] [WM Mode 1] Create fact check endpoint (/api/v1/modes/fact-check) following contracts/api-v1.yaml
- [ ] T023 [US1] [IA MOD-001] [WM Mode 1] Implement LLM Orchestrator intent recognition for fact questions in backend/src/engines/llm/
- [ ] T024 [US1] [IA MOD-001] [WM Mode 1] Build state hydration for basic financial data input in backend/src/engines/llm/
- [ ] T025 [US1] [IA MOD-001] [WM Mode 1] Connect Calculation Engine to fact check endpoint for net wealth and tax calculations
- [ ] T026 [US1] [IA MOD-001] [WM Mode 1] Add narrative generation for calculation results in backend/src/engines/llm/
- [ ] T027 [US1] [IA MOD-001] [WM Mode 1] Implement privacy filtering for fact check responses
- [ ] T028 [US1] [IA MOD-001] [WM Mode 1] Add TraceLog integration for fact check calculations with CAL-* IDs

**Checkpoint**: User Story 1 should be fully functional and independently testable

---

## Phase 4: User Story 2 - Consumer Strategy Exploration (Priority: P1)

**Goal**: Enable consumers to explore "what-if" scenarios to understand different financial strategies

**Independent Test**: Can be fully tested by comparing baseline scenarios against alternative strategies and verifying the projected outcomes are mathematically consistent

### Implementation for User Story 2

- [ ] T029 [US2] [IA MOD-002] [WM Mode 4] Extend CalculationState with scenario management in shared/schemas/calculation.py
- [ ] T030 [US2] [IA MOD-003] [WM Mode 3] Implement Strategy model in shared/schemas/orchestration.py with target metrics and constraints
- [ ] T031 [US2] [IA MOD-002] [WM Mode 4] Create scenario comparison endpoint (/api/v1/scenarios/compare) following contracts/api-v1.yaml
- [ ] T032 [US2] [IA MOD-003] [WM Mode 3] Build Strategy Engine for basic optimization loops in backend/src/engines/strategy/
- [ ] T033 [US2] [IA MOD-002] [WM Mode 4] Implement scenario creation and storage with database persistence
- [ ] T034 [US2] [IA MOD-002] [WM Mode 4] Add scenario modification capabilities for "what-if" analysis
- [ ] T035 [US2] [IA MOD-002] [WM Mode 4] Connect Projection Engine to scenario analysis for multi-year outcomes
- [ ] T036 [US2] [IA MOD-003] [WM Mode 3] Implement side-by-side comparison narratives in backend/src/engines/llm/
- [ ] T037 [US2] [IA MOD-003] [WM Mode 3] Add educational explanations for strategy impacts
- [ ] T038 [US2] [IA MOD-002] [WM Mode 4] Extend TraceLog for scenario comparison operations

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Adviser Comprehensive Planning (Priority: P1)

**Goal**: Enable advisers to create comprehensive financial plans with strategy optimization, compliance checking, and regulatory governance

**Independent Test**: Can be fully tested by running a complete planning workflow and verifying all governance checks pass for approved strategies

### Implementation for User Story 3

- [ ] T039 [US3] [IA MOD-004] [WM Mode 6] Implement AdviceOutcome model for compliance results in shared/schemas/orchestration.py
- [ ] T040 [US3] [IA MOD-004] [WM Mode 6] Build Advice Engine for regulatory compliance checking in backend/src/engines/advice/
- [ ] T041 [US3] [IA MOD-004] [WM Mode 6] Create comprehensive planning endpoint (/api/v1/modes/comprehensive-plan) following contracts/api-v1.yaml
- [ ] T042 [US3] [IA MOD-004] [WM Mode 6] Implement Best Interest Duty (BID) validation rules in backend/src/engines/advice/
- [ ] T043 [US3] [IA MOD-004] [WM Mode 6] Add multi-domain strategy optimization (debt, super, tax, investment)
- [ ] T044 [US3] [IA MOD-004] [WM Mode 6] Build compliance checking integration with Strategy Engine
- [ ] T045 [US3] [IA MOD-004] [WM Mode 14] Implement structured action plans and milestone tracking
- [ ] T046 [US3] [IA MOD-004] [WM Mode 6] Add adviser-specific narrative generation for client communication
- [ ] T047 [US3] [IA MOD-004] [WM Mode 6] Extend TraceLog for comprehensive planning with rule citations
- [ ] T048 [US3] [IA MOD-004] [WM Mode 6] Implement audit trail retrieval endpoint (/api/v1/trace/{scenario_id})

**Checkpoint**: All core user stories (US1, US2, US3) should now be independently functional

---

## Phase 6: User Story 4 - System Health Monitoring (Priority: P2)

**Goal**: Enable system administrators and compliance officers to monitor ongoing performance and regulatory compliance

**Independent Test**: Can be fully tested by triggering rule changes and verifying the system correctly identifies impacted clients and re-evaluates their strategies

### Implementation for User Story 4

- [ ] T049 [US4] [IA MOD-009] [WM Mode 7] Implement regulatory rule monitoring system in backend/src/services/rule_monitor.py
- [ ] T050 [US4] [IA MOD-009] [WM Mode 7] Create system health dashboard endpoint (/api/v1/admin/health) following contracts/api-v1.yaml
- [ ] T051 [US4] [IA MOD-010] [WM Mode 11] Build compliance audit capabilities across all scenarios
- [ ] T052 [US4] [IA MOD-009] [WM Mode 7] Implement automated rule change detection and client impact analysis
- [ ] T053 [US4] [IA MOD-010] [WM Mode 22] Add performance monitoring and diagnostic endpoints
- [ ] T054 [US4] [IA MOD-010] [WM Mode 22] Implement application-level metrics collection (response times, engine performance)
- [ ] T055 [US4] [IA MOD-010] [WM Mode 22] Add infrastructure monitoring (CPU, memory, database queries)
- [ ] T056 [US4] [IA MOD-010] [WM Mode 22] Create performance testing framework with load/stress testing
- [ ] T057 [US4] [IA MOD-010] [WM Mode 22] Implement caching layer for calculation optimization (SC-001, SC-002, SC-004)
- [ ] T058 [US4] [IA MOD-009] [WM Mode 7] Create compliance officer access controls with RBAC metadata
- [ ] T059 [US4] [IA MOD-009] [WM Mode 7] Implement bulk scenario re-evaluation for rule changes
- [ ] T060 [US4] [IA MOD-009] [WM Mode 7] Add system monitoring alerts and notifications
- [ ] T061 [US4] [IA MOD-009] [WM Mode 7] Extend TraceLog for compliance monitoring operations

**Checkpoint**: User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Collaborative Client Sessions (Priority: P2)

**Goal**: Enable advisers to work with clients in real-time scenario exploration with background calculations and compliance guidance

**Independent Test**: Can be fully tested by simulating a live session with scenario changes and verifying real-time updates and compliance warnings

### Implementation for User Story 5

- [ ] T062 [US5] [IA MOD-002] [WM Mode 16] Implement optimistic UI support with background sync in backend/src/services/collaboration.py
- [ ] T063 [US5] [IA MOD-002] [WM Mode 16] Create collaborative session endpoints (/api/v1/sessions/) following contracts/api-v1.yaml
- [ ] T064 [US5] [IA MOD-002] [WM Mode 16] Add real-time scenario update capabilities with conflict detection
- [ ] T065 [US5] [IA MOD-002] [WM Mode 16] Implement session-based scenario modifications
- [ ] T066 [US5] [IA MOD-002] [WM Mode 16] Build background compliance checking during live sessions
- [ ] T067 [US5] [IA MOD-002] [WM Mode 16] Add immediate adviser warnings for compliance issues
- [ ] T068 [US5] [IA MOD-002] [WM Mode 16] Implement session state persistence and recovery
- [ ] T069 [US5] [IA MOD-002] [WM Mode 16] Create meeting notes and action item generation
- [ ] T070 [US5] [IA MOD-002] [WM Mode 16] Extend TraceLog for collaborative session operations

**Checkpoint**: User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Educational Guidance (Priority: P3)

**Goal**: Provide accurate educational responses about financial concepts based on authoritative sources

**Independent Test**: Can be fully tested by asking educational questions and verifying responses are based on authoritative financial sources

### Implementation for User Story 6

- [ ] T071 [US6] [IA MOD-001] [WM Mode 24] [FR-007] Implement RAG system for knowledge retrieval in backend/src/services/rag_service.py
- [ ] T072 [US6] [IA MOD-001] [WM Mode 24] Create educational content endpoints (/api/v1/education/) following contracts/api-v1.yaml
- [ ] T073 [US6] [IA MOD-001] [WM Mode 24] [FR-019] Build LLM integration with OpenRouter for educational responses
- [ ] T074 [US6] [IA MOD-001] [WM Mode 24] Implement privacy filtering for educational content
- [ ] T075 [US6] [IA MOD-001] [WM Mode 24] Add authoritative source citations and references
- [ ] T076 [US6] [IA MOD-001] [WM Mode 24] Create transition logic from education to personalized calculations
- [ ] T077 [US6] [IA MOD-001] [WM Mode 24] Build knowledge base loading from markdown files
- [ ] T078 [US6] [IA MOD-001] [WM Mode 24] Implement educational narrative generation
- [ ] T079 [US6] [IA MOD-001] [WM Mode 24] Add educational content validation and quality checks

### Reference Materials System Implementation (FR-007)

- [ ] T080 [IA MOD-007] [FR-007] Create reference materials storage structure in /specs/001-four-engine-architecture/reference-materials/
- [ ] T081 [IA MOD-007] [FR-007] Implement regulatory document ingestion pipeline for ASIC/ATO content
- [ ] T082 [IA MOD-007] [FR-007] Build citation and attribution system with version tracking
- [ ] T083 [IA MOD-007] [FR-007] Create rule validation library with JSON/YAML schemas
- [ ] T084 [IA MOD-007] [FR-007] Implement search and retrieval API endpoints
- [ ] T085 [IA MOD-007] [FR-007] Add content quality assurance and SME review workflow
- [ ] T086 [IA MOD-007] [FR-007] Integrate reference materials with Calculation Engine rule lookup

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T087 [P] Add comprehensive error handling and user-friendly error messages across all endpoints
- [ ] T088 [P] Implement comprehensive logging and monitoring with Sentry integration
- [ ] T089 [P] [SC-001] Add performance optimization for calculation loops targeting SC-001 (5-second responses)
- [ ] T090 [P] Implement data validation and integrity checks for all financial inputs
- [ ] T091 [P] Add security hardening and input sanitization
- [ ] T092 [P] Create comprehensive API documentation with OpenAPI spec generation
- [ ] T093 [P] Implement backup and recovery procedures for scenarios
- [ ] T094 [P] Add environment-specific configuration management
- [ ] T095 [P] Create deployment configuration for Render backend and Vercel frontend
- [ ] T096 [P] Run quickstart.md validation and update documentation

### Logic Factory Implementation (FR-016)

- [ ] T097 [P] [IA MOD-010] [WM Mode 15] Create Logic Factory API endpoints (/api/v1/logic-factory/) following contracts/api-v1.yaml
- [ ] T098 [P] [IA MOD-010] [WM Mode 15] Implement code generation engine with template-based CAL-* patterns in backend/src/services/logic_factory.py
- [ ] T099 [P] [IA MOD-010] [WM Mode 15] Build validation pipeline (syntax, schema, reference audit) for generated code
- [ ] T100 [P] [IA MOD-010] [WM Mode 15] Add sandbox execution environment for safe code testing
- [ ] T101 [P] [IA MOD-010] [WM Mode 15] Implement human-in-the-loop review workflow with audit trails
- [ ] T102 [P] [IA MOD-010] [WM Mode 15] Create web interface for Logic Factory management and code review
- [ ] T103 [P] [IA MOD-010] [WM Mode 15] Integrate Logic Factory with TraceLog system for CAL-* ID tracking

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
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
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Consumer Fact Check - MVP priority)
   - Developer B: User Story 2 (Strategy Exploration)
   - Developer C: User Story 3 (Adviser Planning)
3. Stories complete and integrate independently

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

- **Total Requirements**: 20 FR + 9 SC = 29
- **Requirements with Task Coverage**: 20/29 (69%)
- **Requirements Fully Covered**: 16/29 (55%)
- **Requirements Needing Tasks**: FR-002, FR-003 (design docs exist but may need API endpoint tasks)

**Note**: FR-002 and FR-003 are covered by design documents but may need additional implementation tasks for the mode-specific logic and API endpoints. FR-016 now has detailed specification and implementation tasks.