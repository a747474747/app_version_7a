# Implementation Plan: Four-Engine System Architecture

**Feature Branch**: `001-four-engine-architecture`
**Created**: November 21, 2025
**Status**: Draft
**Input**: User description: "create the spec from this:@design/interaction_architecture.md @calculation_catalog.md"

---

## 1. Technical Context

### 1.1 Feature Overview

This implementation builds a **Four-Engine Architecture** for financial advice systems with four distinct computational engines (LLM Orchestrator, Calculation Engine, Strategy Engine, Advice Engine) that work together to process financial queries and generate advice. The system supports 12 interaction models and 26 operational modes representing specific user journeys.

**Primary Deliverables:**
- Four computational engines with clear separation of concerns
- 12 interaction models for different use cases
- 26 operational modes for specific user journeys
- Deterministic mathematical calculations vs probabilistic AI responses per calculation_catalog.md
- Regulatory compliance checks (Best Interest Duty requirements)
- Real-time calculation capabilities for interactive scenario exploration

### 1.2 Technical Requirements

| Component | Status | Details |
|-----------|--------|---------|
| **Backend Stack** | ✅ Confirmed | Python 3.11, FastAPI, PostgreSQL, SQLAlchemy 2.0 |
| **Frontend Stack** | ✅ Confirmed | Next.js (App Router), TypeScript, Tailwind CSS |
| **Deployment** | ✅ Confirmed | Render (backend), Vercel (frontend) |
| **State Models** | ✅ Available | CalculationState, ProjectionOutput, TraceLog defined in guidance docs |
| **Engine Separation** | ✅ Confirmed | LLM (probabilistic) vs Calculation (deterministic) separation |
| **Regulatory Compliance** | ✅ Confirmed | Best Interest Duty (BID) requirements, audit trails |
| **Multi-User Architecture (Auth & RBAC)** | ✅ CLARIFIED | Clerk (SaaS) + RBAC via Metadata. Emphasis on simplicity - avoid custom auth massive time sink. |
| **Real-Time Collaboration (Optimistic UI)** | ✅ CLARIFIED | Optimistic UI (TanStack Query). Last-write-wins acceptable for financial tool MVP. |
| **External Data Integration** | ❌ Out of Scope | Manual/Chat Entry only. Bank feeds excluded for MVP. |
| **Scale Requirements** | ✅ CLARIFIED | Target 100 concurrent users. Auto-scale Render containers. Performance solved by hosting costs, not complex code. |
| **Security Model (Data Encryption)** | ✅ CLARIFIED | HTTPS + Postgres encryption. Row Level Security handled via Application Logic, not complex DB policies for MVP. |
| **Monitoring & Observability** | ✅ CLARIFIED | Sentry + Axiom/BetterStack. Simple /health endpoint. Full visibility with minimal setup. |
| **Data Quality (Progressive Onboarding)** | ✅ CLARIFIED | "Flag, Don't Block". Allow draft calculations with defaults. Reject final advice if critical data missing. |
| **Educational Content (RAG)** | ✅ CLARIFIED | Markdown files in repo. Git versioning. Simple text search or pgvector. Zero infrastructure cost. |

### 1.3 Integration Points

| Integration | Status | Details |
|-------------|--------|---------|
| **Database** | ✅ Confirmed | PostgreSQL (Render) with JSONB. |
| **LLM Provider** | ✅ Confirmed | OpenRouter (Unified interface for hundreds of models). |
| **RAG/Knowledge** | ✅ Confirmed | Local Markdown Files (Git-versioned). Defer pgvector. |
| **External APIs** | ❌ Excluded | Bank Feeds excluded. User enters data manually or via chat. |
| **File Storage** | ✅ Confirmed | Cloudflare R2 (S3 Compatible). Best value ($0 egress) for storing reports. |
| **Email/SMS** | ❌ Excluded | Transactional notifications excluded. User views all results directly in the Dashboard. (Auth verification handled natively by Clerk). |

### 1.4 Success Criteria Alignment

| Success Criteria | Implementation Approach |
|------------------|------------------------|
| **SC-001**: 5-second fact check responses | LLM + Calculation Engine optimization |
| **SC-002**: 30-second complex optimizations | Strategy Engine efficiency |
| **SC-003**: 95% compliance check pass rate | Advice Engine rule validation |
| **SC-004**: 5 simultaneous scenario comparisons | Real-time calculation capabilities |
| **SC-005**: 99.9% availability | Render deployment, error handling |
| **SC-006**: Complete audit trails | TraceLog implementation |
| **SC-007**: 90%+ user task completion | UX optimization, error reduction |
| **SC-008**: 100% regulatory change detection | Manual/LLM Triggered review (Mode 7) |
| **SC-009**: Optimistic UI updates < 100ms | TanStack Query optimistic updates |
| **SC-010**: Authoritative educational citations | RAG integration |

### 1.5 Design References & Blueprints

This section provides access to the architectural blueprints and pattern libraries that guide the four-engine implementation:

* **`design/interaction_architecture.md`**: The **Unified Design Reference**. Consult this file for:
    * **Architectural Patterns (Models)**: The definition of the 12 Interaction Models (MOD-001 to MOD-012).
    * **User Journeys (Modes)**: The specific logic flow for Operational Modes 1–26.

---

## 2. Constitution Check

### 2.0 Data Model Validation Against Calculation Catalog

**Validation performed:** Cross-referenced calculation_catalog.md requirements against data-model.md fields.

**Key Findings:**

| Calculation | Requirement | Data Model Status | Notes |
|-------------|-------------|-------------------|-------|
| CAL-PRP-006 (Net rental cashflow after tax) | Property rental income, holding costs, loan interest | ✅ COMPLETE | All required fields now available |
| CAL-PRP-003 (Annual property holding costs) | rates, insurance, maintenance, body corporate, management, other expenses | ✅ COMPLETE | All expense fields added to PropertyAsset |
| CAL-PRP-005 (Net rental cashflow before tax) | Rental income minus holding costs and interest | ✅ COMPLETE | Loan.annual_interest_expense property added |
| Context Classes | FinancialPositionContext, EntityContext | ✅ COMPLETE | Context classes defined with proper aggregation |

**Status:** ✅ RESOLVED - All data model gaps have been fixed. Phase 2.1 Golden Four implementation can proceed.

---

### 2.1 Financial Precision & Data Integrity ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **No floating-point currency** | ✅ COMPLIANT | All monetary calculations use Decimal types |
| **Explicit units & types** | ✅ COMPLIANT | CalculationState uses strongly typed Pydantic models |
| **Validated inputs** | ✅ COMPLIANT | Pydantic schemas for all calculation inputs/outputs |
| **Single source of truth for rules** | ✅ COMPLIANT | Tax scales, thresholds in structured configuration |

### 2.2 Deterministic, Rule-Based Forecasting ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Deterministic results** | ✅ COMPLIANT | Calculation Engine is pure function of inputs + rules |
| **No randomness in core logic** | ✅ COMPLIANT | Stochastic models separate from core CALs |
| **Explicit tolerances & rounding** | ✅ COMPLIANT | Rounding rules defined in GlobalContext |
| **Traceable computations** | ✅ COMPLIANT | TraceLog provides complete audit trails |

### 2.3 Separation of Concerns & Engine Boundaries ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Calculation Engine isolation** | ✅ COMPLIANT | Only place for numeric financial results |
| **LLM authority over numbers** | ✅ COMPLIANT | LLM treats Calculation outputs as authoritative |
| **Strategy Engine constraints** | ✅ COMPLIANT | Cannot bypass Calculation Engine logic |
| **Advice Engine veto power** | ✅ COMPLIANT | Can reject strategies but not alter math |

### 2.4 State, Storage & Traceability ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **CalculationState & ProjectionOutput** | ✅ COMPLIANT | Year 0 snapshot + timeline outputs |
| **Trace Log structure** | ✅ COMPLIANT | Structured entries with calc_id, entity_id, field, explanation |
| **PostgreSQL primary store** | ✅ COMPLIANT | JSONB for flexible state storage |
| **Knowledge storage** | ✅ COMPLIANT | File-based initially, pgvector optional later |

### 2.5 LLM Orchestrator (Probabilistic Layer) ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Interface role** | ✅ COMPLIANT | Converts text ↔ structured JSON/state |
| **Prohibitions** | ✅ COMPLIANT | No financial calculations, no result overriding |
| **Hydration & serialization** | ✅ COMPLIANT | State building from inputs, narrative generation |
| **Mode selection** | ✅ COMPLIANT | Execution Modes for all non-trivial interactions |

### 2.6 Specification-Driven Development ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Specs first** | ✅ COMPLIANT | Feature specs precede substantial code changes |
| **Structured artifacts** | ✅ COMPLIANT | Markdown/YAML with clear IDs and definitions |
| **Review process** | ✅ COMPLIANT | AI-assisted + human sanity checks |
| **Context discipline** | ✅ COMPLIANT | Small, focused specs for LLM context limits |

### 2.7 Frontend-Agnostic Backend ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Backend independence** | ✅ COMPLIANT | Addressable only through documented APIs |
| **Primary frontends** | ✅ COMPLIANT | Veris (adviser) + Dev Dashboard (compliance) |

### 2.8 Experience Principles ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Veris (Advisers)** | ✅ COMPLIANT | Data-dense interfaces, scenario comparisons |
| **Frankie (Consumers)** | DEFERRED | Out of scope for MVP |
| **Universal principles** | ✅ COMPLIANT | Intent-based navigation, grounded explanations |

### 2.9 Interfaces & Modes ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Execution Modes** | ✅ COMPLIANT | 26 named modes with clear responsibilities |
| **Mode contracts** | ✅ COMPLIANT | Engine calls, state access, output classification |

### 2.10 Development Workflow ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Order of work** | ✅ COMPLIANT | Spec → Schema → Logic → Tests → API → UI |
| **Golden tests** | ✅ COMPLIANT | ATO calculator parity for key CALs |

### 2.11 Security & Privacy ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **PII handling** | ✅ COMPLIANT | Appropriate access controls, no unnecessary PII logging |
| **LLM data minimization** | ✅ COMPLIANT | Minimum state subset sent to LLM |
| **No production secrets in specs** | ✅ COMPLIANT | Environment variables for credentials |

### 2.12 Success Criteria ✅

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Determinism** | ✅ COMPLIANT | Same inputs = identical outputs |
| **Explainability** | ✅ COMPLIANT | Complete audit trails with explanations |
| **Safety** | ✅ COMPLIANT | High-risk strategies flagged/blocked |
| **Velocity** | ✅ COMPLIANT | Solo developer can extend system safely |

---

## 3. Gate Evaluation

### 3.1 Constitution Gates

All constitution principles are **COMPLIANT** or **DEFERRED** (Frankie consumer features out of scope). No violations detected.

### 3.2 Technical Feasibility Gates

| Gate | Status | Rationale |
|------|--------|-----------|
| **Engine Separation** | ✅ PASS | Clear boundaries between probabilistic (LLM) and deterministic (Calculation) layers |
| **State Management** | ✅ PASS | CalculationState and ProjectionOutput models defined in guidance docs |
| **Regulatory Compliance** | ✅ PASS | Advice Engine handles Best Interest Duty requirements |
| **Performance Requirements** | ⚠️ MONITOR | 5-second fact check, 30-second optimizations need optimization |
| **Scalability** | NEEDS CLARIFICATION | Concurrent user limits, calculation complexity bounds |

### 3.3 Business Viability Gates

| Gate | Status | Rationale |
|------|--------|-----------|
| **Market Need** | ✅ PASS | Clear user stories for consumers and advisers |
| **Technical Risk** | ✅ PASS | Four-engine architecture mitigates AI hallucination risks |
| **Development Velocity** | ✅ PASS | Solo developer friendly with spec-driven approach |
| **Regulatory Compliance** | ✅ PASS | Built-in compliance checks and audit trails |

---

## Phase 0: Outline & Research

### Prerequisites
- Feature spec complete ✅
- Constitution check passed ✅
- Technical context documented ✅

### Research Tasks

1. **Multi-User Architecture** (NEEDS CLARIFICATION)
   - Research: Authentication patterns for advisers, consumers, compliance officers
   - Research: Role-based access control for different user types
   - Research: Session management for collaborative scenarios

2. **Scale and Performance** (NEEDS CLARIFICATION)
   - Research: Concurrent user load testing
   - Research: Calculation engine optimization techniques
   - Research: Database query optimization for complex scenarios

3. **Security Implementation** (NEEDS CLARIFICATION)
   - Research: Clerk integration patterns for JWT to FastAPI
   - Research: RBAC metadata handling in application logic

4. **Monitoring & Observability** (NEEDS CLARIFICATION)
   - Research: Sentry + Axiom/BetterStack setup
   - Research: Simple /health endpoint implementation

5. **Data Quality Framework** (NEEDS CLARIFICATION)
   - Research: Progressive onboarding workflows
   - Research: Data validation and completeness checks
   - Research: Missing data handling strategies

6. **Educational Content Management** (NEEDS CLARIFICATION)
   - Research: RAG implementation approaches
   - Research: Content versioning and update processes
   - Research: Citation and source tracking

### Output: research.md
Consolidated findings with decisions, rationale, and alternatives considered for all NEEDS CLARIFICATION items.

---

## Phase 1: Design & Contracts

### Prerequisites
- research.md complete ✅ (Phase 0 output)
- All technical unknowns resolved

### 1.1 Data Model Design (data-model.md)

**Extract entities from feature spec:**

1. **CalculationState** - User's complete financial position
2. **ProjectionTimeline** - Time-series data for financial metrics
3. **Scenario** - Financial assumptions and strategy choices
4. **Strategy** - Reusable optimization templates
5. **AdviceOutcome** - Regulatory compliance results
6. **TraceLog** - Detailed audit trail
7. **ReferenceDocument** - Authoritative sources
8. **UserProfile** - User role and permissions

**Validation rules from requirements:**
- All entities must support the 12 interaction models
- Must integrate with 26 operational modes
- Regulatory compliance validation
- Real-time calculation capabilities

### 1.2 API Contract Generation (/contracts/)

**Generate API contracts from functional requirements:**

1. **Core Calculation APIs**
   - `POST /api/v1/calc/run` - Execute calculations
   - `POST /api/v1/scenarios` - Create scenarios
   - `GET /api/v1/scenarios/{id}` - Retrieve scenarios
   - `POST /api/v1/scenarios/{id}/run` - Run scenario calculations

2. **Strategy & Optimization APIs**
   - `POST /api/v1/strategies/optimize` - Run strategy optimization
   - `POST /api/v1/scenarios/compare` - Compare scenarios

3. **Advice & Compliance APIs**
   - `POST /api/v1/advice/evaluate` - Evaluate regulatory compliance
   - `GET /api/v1/trace/{scenario_id}` - Retrieve audit trails

4. **Interaction Model APIs**
   - `POST /api/v1/modes/{mode}/execute` - Execute specific modes
   - `POST /api/v1/chat/process` - Process conversational inputs

**OpenAPI/Schema Generation:**
- REST API specifications
- Request/response schemas
- Error handling contracts
- Authentication requirements

### 1.3 Agent Context Update

**Run agent context update script:**
```powershell
.specify/scripts/powershell/update-agent-context.ps1 -AgentType cursor-agent
```

**Update technology context:**
- Add four-engine architecture knowledge
- Include interaction model patterns
- Add operational mode specifications
- Preserve existing manual additions

### 1.4 Quickstart Guide (quickstart.md)

**Generate implementation quickstart:**
- Development environment setup
- Key architecture concepts
- Basic usage examples
- Testing procedures
- Deployment instructions

---

## Phase 2: Implementation Planning

### Prerequisites
- data-model.md complete ✅
- calculation_catalog.md complete ✅ (functional specification for Calculation Engine)
- /contracts/ generated ✅
- quickstart.md complete ✅
- Agent context updated ✅
- Constitution check re-evaluated ✅

### Implementation Tasks

**Phase 2.1: Engine Foundation (The "Golden Four")**
- Implement CalculationState and ProjectionOutput models in backend/src/models (shared) directory, distinct from backend/src/engines/calc directory, to avoid circular dependencies if the Strategy Engine needs to import them
- Create TraceLog mechanism with CAL-* ID traceability
- Build Calculation Engine core implementing MVP Core tier calculations from calculation_catalog.md:
  - CAL-PIT-001 to 005 (PAYG & Net Tax)
  - CAL-CGT-001 to 002 (Capital Gains)
  - CAL-SUP-002 to 009 (Super Contributions)
  - CAL-PFL-104 (Negative Gearing)
- Implement Projection Engine (year-over-year loop)
- Create golden test cases for all Core tier calculations

**Phase 2.2: Persistence Layer**
- Set up PostgreSQL with SQLAlchemy models
- Implement Scenario and ScenarioSnapshot storage
- Create database migration scripts
- Add data validation and integrity checks

**Phase 2.3: Calculation Expansion (Extended Tier)**
- Implement Extended tier calculations from calculation_catalog.md grouped by domain:
  - Sprint 1: Property Acquisition (CAL-PRP-001 to 011)
  - Sprint 2: Super Accumulation (CAL-SUP-201 to 213)
  - Sprint 3: Investment Portfolio (CAL-PFL-201 to 233)
  - Sprint 4: Cashflow & Budgeting (CAL-FND-201 to 233)
  - Sprint 5: Insurance & Protection (CAL-INS-001 to 027)
  - Sprint 6: Retirement & Age Pension (CAL-RPT-201 to 219, CAL-SSC-001 to 012)
- Create stub implementations for Extended calculations to enable parallel Strategy Engine development
- Implement Strategy Engine (optimization loops) using calculation stubs
- Build Advice Engine (policy checks)
- Create rule/policy configuration system
- Add compliance validation logic

### Phase 2.35: Calculation Engine Refactor (Critical Tech Debt)

**Goal**: Move from monolithic `__init__.py` to domain-driven module structure to support Extended Tier growth.

**Implementation Tasks**:

1.  **Create Directory Structure**: Set up `backend/src/engines/calculation/domains/`.

2.  **Implement RuleLoader**: Build service to read `specs/rules/*.yaml` instead of hardcoding values (Completes T009b).

3.  **Migrate Core Calculations**: Move existing CAL-PIT/SUP/CGT functions from `__init__.py` to their respective domain files (`tax_personal.py`, etc.).

4.  **Build Registry**: Implement `registry.py` to map string IDs to functions.

5.  **Update Consumers**: Refactor `projection.py` and API routers to use the Registry instead of direct imports.

6. Follow @conditional_rules/calc_architecture_guide.md

## **Phase 2.4: LLM Integration**

### 2.4.1 Domain Knowledge Base Creation
**Create comprehensive internal source materials for LLM prompt development:**

- Create Australian Financial System primer (`/specs/001-four-engine-architecture/llm-source-materials/australian-financial-system.md`)
  - Overview of Australian financial institutions and products
  - Key financial concepts and terminology
  - Tax system fundamentals (PAYG, CGT, superannuation)
  - Investment vehicles and structures

- Create Financial Advice Process guide (`/specs/001-four-engine-architecture/llm-source-materials/financial-advice-process.md`)
  - Stages of financial advice (fact-finding, needs analysis, strategy development, implementation)
  - Adviser responsibilities and obligations
  - Client communication patterns
  - Documentation and disclosure requirements

- Create Regulatory Environment overview (`/specs/001-four-engine-architecture/llm-source-materials/regulatory-environment.md`)
  - ASIC regulatory framework and RG 175 (Financial Advice)
  - Best Interest Duty (BID) requirements
  - AFSL and ACL requirements
  - Consumer protection laws
  - Privacy and data handling requirements

- Create Interaction Pattern library (`/specs/001-four-engine-architecture/llm-source-materials/interaction-patterns.md`)
  - Common user question types and appropriate responses
  - Educational content delivery patterns
  - Risk communication frameworks
  - Goal-setting and strategy discussion flows

- Create domain-specific knowledge bases (`/specs/001-four-engine-architecture/llm-source-materials/domain-knowledge/`)
  - `tax-regime.md`: Detailed tax rules and thresholds
  - `superannuation.md`: Super contribution strategies and rules
  - `property-investment.md`: Property investment considerations
  - `retirement-planning.md`: Retirement income strategies
  - `insurance.md`: Insurance product types and suitability

- Track all source materials in `/specs/001-four-engine-architecture/llm-source-materials/catalog.json`

**Purpose**: These materials provide comprehensive context for developers creating and maintaining LLM prompts, ensuring consistent understanding of Australian financial services without exposing sensitive internal knowledge to external LLMs.

### 2.4.2 Prompt Management System Setup
**Create structured system for managing LLM prompts:**

- Create prompt directory structure:
  - `/specs/001-four-engine-architecture/llm-prompts/core-orchestrator/` - Core LLM Orchestrator function prompts
  - `/specs/001-four-engine-architecture/llm-prompts/mode-prompts/` - All 26 mode-specific prompts aligned with workflows_and_modes.md
  - `/specs/001-four-engine-architecture/llm-prompts/shared-utilities/` - Cross-cutting prompt utilities

- Set up catalog tracking system (`/specs/001-four-engine-architecture/llm-prompts/catalog.json`)
  - Track all prompt files with metadata (prompt_id, title, description, mode_id, category, version, etc.)
  - Link prompts to related specification files

- Create prompt templates aligned with 26 operational modes:
  - Core orchestrator prompts (intent recognition, state hydration, strategy nomination, narrative generation)
  - Mode-specific prompts (modes 1-26 from workflows_and_modes.md)
  - Shared utility prompts (privacy filter, RAG retrieval, error handling, conversation context)

- Implement prompt loading utilities in backend
  - Scripts must load prompts from files, never embed prompt text directly
  - Each unique prompt/primer gets its own file
  - Prompts must be in format suitable for LLMs (markdown with clear sections)

**Purpose**: Ensure prompts are separated from scripts, catalogued, reusable, and aligned with the 26 operational modes defined in workflows_and_modes.md.

### 2.4.3 LLM Orchestrator Implementation
- Implement LLM Orchestrator (intent classification)
- Add state hydration capabilities
- Create narrative generation templates
- Implement Hypothesis-Driven Logic Factory (LLM writes the math code)
- Integrate RAG for educational responses

**Phase 2.5: LLM Connection & Future Workflow Integration**

### 2.5.1 Domain Knowledge Base Setup
**Create comprehensive internal source materials for LLM prompt development:**

- Create Australian Financial System primer (`/specs/001-four-engine-architecture/llm-source-materials/australian-financial-system.md`)
  - Overview of Australian financial institutions and products
  - Key financial concepts and terminology
  - Tax system fundamentals (PAYG, CGT, superannuation)
  - Investment vehicles and structures

- Create Financial Advice Process guide (`/specs/001-four-engine-architecture/llm-source-materials/financial-advice-process.md`)
  - Stages of financial advice (fact-finding, needs analysis, strategy development, implementation)
  - Adviser responsibilities and obligations
  - Client communication patterns
  - Documentation and disclosure requirements

- Create Regulatory Environment overview (`/specs/001-four-engine-architecture/llm-source-materials/regulatory-environment.md`)
  - ASIC regulatory framework and RG 175 (Financial Advice)
  - Best Interest Duty (BID) requirements
  - AFSL and ACL requirements
  - Consumer protection laws
  - Privacy and data handling requirements

- Create Interaction Pattern library (`/specs/001-four-engine-architecture/llm-source-materials/interaction-patterns.md`)
  - Common user question types and appropriate responses
  - Educational content delivery patterns
  - Risk communication frameworks
  - Goal-setting and strategy discussion flows

- Create domain-specific knowledge bases (`/specs/001-four-engine-architecture/llm-source-materials/domain-knowledge/`)
  - `tax-regime.md`: Detailed tax rules and thresholds
  - `superannuation.md`: Super contribution strategies and rules
  - `property-investment.md`: Property investment considerations
  - `retirement-planning.md`: Retirement income strategies
  - `insurance.md`: Insurance product types and suitability

- Track all source materials in `/specs/001-four-engine-architecture/llm-source-materials/catalog.json`

**Purpose**: These materials provide comprehensive context for developers creating and maintaining LLM prompts, ensuring consistent understanding of Australian financial services without exposing sensitive internal knowledge to external LLMs.

### 2.5.2 Prompt Management System Setup
**Create structured system for managing LLM prompts:**

- Create prompt directory structure:
  - `/specs/001-four-engine-architecture/llm-prompts/core-orchestrator/` - Core LLM Orchestrator function prompts
  - `/specs/001-four-engine-architecture/llm-prompts/mode-prompts/` - All 26 mode-specific prompts aligned with workflows_and_modes.md
  - `/specs/001-four-engine-architecture/llm-prompts/shared-utilities/` - Cross-cutting prompt utilities

- Set up catalog tracking system (`/specs/001-four-engine-architecture/llm-prompts/catalog.json`)
  - Track all prompt files with metadata (prompt_id, title, description, mode_id, category, version, etc.)
  - Link prompts to related specification files

- Create prompt templates aligned with 26 operational modes:
  - Core orchestrator prompts (intent recognition, state hydration, strategy nomination, narrative generation)
  - Mode-specific prompts (modes 1-26 from workflows_and_modes.md)
  - Shared utility prompts (privacy filter, RAG retrieval, error handling, conversation context)

- Implement prompt loading utilities in backend
  - Scripts must load prompts from files, never embed prompt text directly
  - Each unique prompt/primer gets its own file
  - Prompts must be in format suitable for LLMs (markdown with clear sections)

**Purpose**: Ensure prompts are separated from scripts, catalogued, reusable, and aligned with the 26 operational modes defined in workflows_and_modes.md.

### 2.5.3 LLM Orchestrator Implementation
- Implement LLM Orchestrator (intent classification)
- Add state hydration capabilities
- Create narrative generation templates
- Implement Hypothesis-Driven Logic Factory (LLM writes the math code)
- Integrate RAG for educational responses

**Phase 2.6: API Layer**
- Build FastAPI endpoints following contracts
- Implement authentication and authorization
- Add request validation and error handling
- Create API documentation

**Phase 2.7: Frontend Development**
- Set up Next.js application structure
- Implement Veris adviser interface
- Build Dev/Compliance dashboard

**Phase 2.8: Testing & Quality Assurance**
- Implement golden test cases using CAL-* IDs as primary keys (Mode 17: Calculation Harness)
- Create unit test files for every Core calculation (CAL-PIT-001 to 005, CAL-CGT-001 to 002, CAL-SUP-002 to 009, CAL-PFL-104)
- Create stub functions for Extended calculations returning estimated values per calculation_catalog.md
- Build integration tests for engines using calculation catalog as checklist
- Add performance testing framework targeting SC-001 (5-second fact checks) and SC-002 (30-second optimizations)

**Phase 2.9: Deployment & Operations**
- Configure Render backend deployment
- Set up Vercel frontend deployment
- Implement monitoring and alerting
- Create backup and recovery procedures

---

## Risk Mitigation

### Technical Risks
1. **Engine Coupling** - Strict adherence to constitution boundaries
2. **Performance Bottlenecks** - Early optimization of calculation loops
3. **Data Integrity** - Comprehensive validation and audit trails
4. **Regulatory Compliance** - Built-in compliance checks and testing

### Business Risks
1. **Scope Creep** - Clear MVP boundaries, Frankie features deferred
2. **Timeline Delays** - Phased approach with working increments
3. **Quality Issues** - Comprehensive testing and review processes

---

## Success Metrics

- **Technical Completeness**: All four engines implemented with clear boundaries
- **Performance Targets**: Meet 5-second and 30-second response requirements
- **Compliance Coverage**: 95% automated regulatory compliance checks
- **User Experience**: 90%+ task completion rates for primary use cases
- **Code Quality**: Comprehensive test coverage and audit trails

---

## Integration Summary: Calculation Catalog

The `calculation_catalog.md` now serves as the definitive functional specification for the Calculation Engine:

### Development Workflow Integration

1. **Phase 2.1 (Golden Four)**: Implement Core tier calculations (CAL-PIT-001 to 005, CAL-CGT-001 to 002, CAL-SUP-002 to 009, CAL-PFL-104)

2. **Phase 2.3 (Expansion)**: Implement Extended tier calculations grouped by domain (Property, Super, Investment, etc.)

3. **Naming Convention**: All Python functions must follow `run_CAL_XXX_YYY` pattern with CAL-* IDs

4. **Traceability**: TraceLog entries use CAL-* IDs for complete audit trails

5. **Testing**: Golden test cases keyed by CAL-* IDs, stub functions for Extended calculations

6. **Data Model**: Must support all fields required by Core calculations before Phase 2.1

### Constitution Compliance
- ✅ Deterministic calculations with explicit CAL-* IDs
- ✅ Separation between Calculation (deterministic) and LLM (probabilistic) layers
- ✅ Complete audit trails with calculation provenance
- ✅ Single source of truth for financial rules

**Next Steps**: Proceed to Phase 2.1 Golden Four implementation - all data model gaps resolved.
