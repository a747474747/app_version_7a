# Master Implementation Plan: App Version 5 System

**Branch**: `001-master-spec` | **Date**: 2025-01-27 | **Spec**: `specs/001-master-spec/master_spec.md`  
**Status**: ✅ **Phase 0 Complete**  
**Input**: Master specification coordinating all six modules of the App Version 5 financial advice system

## Summary

App Version 5 is a specification-driven, deterministic financial advice system that converts Australian financial regulations into auditable rules and reproducible forecasts. The system consists of six modules: **References & Research Engine** (foundational), **Compute Engine** (core calculations), **Advice Engine** (compliance), **LLM Orchestrator** (natural language translation), **Veris Finance** (adviser UX), and **Frankie's Finance** (consumer UX).

**Technical Approach**: Relational database-only architecture (PostgreSQL with recursive CTEs, JSONB, temporal tables), API-first backend, deterministic calculation engine with full provenance, and LLM orchestration for natural language interfaces. The system enforces specification-driven development with two-person review, versioned artifacts, and comprehensive testing.

**Key Guidance**:
- **Timeline**: Compressed to 2 weeks total with AI-assisted development (Cursor AI agents)
- **Version Control**: Automated commits after each task has been tested
- **Sequencing**: Frankie's Finance developed after Veris Finance (testing Veris is easier and resolves backend features)
- **LLM Model Selection**: Different LLM models for different tasks (research/rule transformation vs client interactions) with intelligent switching, preference for cheaper models based on performance requirements
- **Database Schemas**: Created during Phase 1 research phase based on extracted logic from MVP research documents
- **Parallel Development**: Modules can be developed in parallel by Cursor AI agents where dependencies allow

## Technical Context

### Technology Stack

| Layer | Technology | Deployment | Rationale |
|-------|------------|------------|-----------|
| **Monorepo** | **Turborepo** | GitHub | 70–80% code share, 10× faster builds, parallel agent workflows |
| **Frontend (Consumer)** | **Expo + React Native + TanStack Query + Tamagui** | **Expo EAS** → iOS/Android | Native push, offline sync, App Store trust, spatial UX, API caching, shared design tokens |
| **Frontend (Adviser)** | **Next.js App Router + TanStack Query + Tamagui** | **Vercel** | Desktop-first, print-ready, AG Grid, keyboard shortcuts, API caching, shared design tokens |
| **Backend** | **FastAPI (Python 3.11) + SQLAlchemy 2.0 + Pydantic v2** | **Render (Sydney)** | AU data residency, 15-min timeout, zero ops, full ORM control, async support |
| **Database** | **PostgreSQL 15+** | **Render Sydney** | Relational edge table + JSONB + bitemporal fields + partial indexes + closure table/materialized view + RLS |
| **Cache** | **Redis** | **Render** | Hot facts in <1ms, RQ workers for background jobs |
| **Background Jobs** | **RQ (Redis Queue)** | **Render** | Long-running jobs return 202 + job ID, async processing |
| **Error Tracking** | **Sentry (free tier)** | **Cloud** | Error monitoring across all modules |
| **LLM Orchestrator** | **OpenRouter** (OpenAI models via BYOK) | — | Intent → structured request only (never source of truth); RAG retrieval for prompt augmentation; unified API via OpenRouter supporting both credits and BYOK |
| **Dev Tool** | **Cursor AI** | Local + 3 Agent Chats | Backend, Frankie's, Veris — parallel, filter-aware |

### Key Decisions

- **No Graph DB** → **PostgreSQL-only**  
  → 10× faster `/explain` (<10ms via closure table/materialized view), full auditability via relational edge table + JSONB  
  → Bitemporal fields (`valid_from`/`valid_to`) = built-in `as_of` time-travel  
  → Partial indexes on current data for performance  
  → Row-Level Security (RLS) for tenant isolation  
  → **$14/mo** vs $65+ for Neo4j

- **Split UI Frameworks**  
  → **Expo** = mobile-native (Frankie's)  
  → **Next.js** = desktop power tool (Veris)  
  → **70%+ shared logic** (`types`, `api`, `hooks`, `validation`)  
  → **TanStack Query** = API caching in both frontends  
  → **Tamagui** = shared design tokens (mobile + web)

- **Backend Upgrades**  
  → **SQLAlchemy 2.0** = full control, async support, type safety  
  → **Pydantic v2** = validation, serialization  
  → **RQ workers** = background jobs (202 + job ID for long operations)  
  → **Sentry** = error tracking across all modules

- **Constitution Compliance**  
  - Determinism: `ruleset_id` + `as_of` + immutable `facts`  
  - Auditability: `/explain` via closure table/materialized view (<10ms)  
  - Privacy: PII in `inputs`, redacted logs, AU region, RLS for tenant isolation  
  - Reproducibility: Idempotency keys, golden datasets

### Cost Breakdown (AU, Nov 2025)

| Service | Cost |
|---------|------|
| Render (FastAPI + Postgres + Redis) | **$21/mo** |
| Vercel Pro (Veris) | **$20/mo** |
| Expo EAS Pro (Frankie's) | **$29/mo** |
| **Total** | **~$70/mo** |

**Language/Version**: 
- **Backend**: Python 3.11+ (Compute Engine, Advice Engine, References & Research Engine, LLM Orchestrator)
- **Frontend Consumer**: TypeScript/React Native (Expo) for Frankie's Finance
- **Frontend Adviser**: TypeScript/Next.js App Router for Veris Finance
- **Monorepo**: Turborepo for shared code and parallel builds

**Primary Dependencies**:
- **Monorepo**: Turborepo (70-80% code share, 10× faster builds, parallel agent workflows)
- **API Framework**: FastAPI (Python backend) deployed on Render (Sydney region)
- **ORM**: SQLAlchemy 2.0 (full control, async support, type safety) + Pydantic v2 (validation, serialization)
- **Deployment Platforms**: 
  - Render (Sydney) for backend, PostgreSQL, Redis - AU data residency
  - Vercel for Veris Finance (Next.js web app)
  - Expo EAS for Frankie's Finance (iOS/Android native apps)
- **Database**: PostgreSQL 15+ with relational edge table + JSONB + bitemporal fields + closure table/materialized view + RLS
- **Cache**: Redis (Render) for hot facts (<1ms lookup times)
- **Background Jobs**: RQ (Redis Queue) worker for long-running jobs (returns 202 + job ID)
- **Frontend State Management**: TanStack Query (React Query) for API caching in both frontends
- **Design System**: Tamagui for shared design tokens (mobile + web)
- **Error Tracking**: Sentry (free tier) for error monitoring and tracking
- **LLM Providers**: OpenRouter for all LLM interactions (see `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` for details)
- **Testing**: pytest (Python), Jest/React Testing Library (TypeScript)
- **CI/CD**: GitHub Actions for automated testing, Render/Vercel/Expo EAS for deployments

**Storage**:
- **PostgreSQL Database (Render Sydney)**: All data storage (canonical governance, execution data, provenance links)
- **Redis Cache (Render)**: Hot facts (<1ms lookup times), RQ workers for background jobs
- **Object Storage**: Reference documents (PDFs, HTML), rule artifacts (Markdown/YAML)

**Testing**:
- **Unit Tests**: pytest for Python modules, Jest for TypeScript modules
- **Integration Tests**: API contract tests, database integration tests
- **Property-Based Tests**: Hypothesis (Python) for calculation edge cases
- **Golden Datasets**: Regulator examples (ATO, ASIC) for validation
  - **Minimum Validation Suite (CRITICAL - Required Before Shipping)**:
    - At least 10 ATO tax calculation examples validated (taxable income, tax offsets, deductions, CGT)
    - At least 5 ASIC compliance examples validated (best interests duty, conflict detection, advice documentation)
    - 100% deterministic reproducibility verified (same inputs + ruleset + date = identical outputs)
    - All calculations tested via Veris Finance test forecasts
- **End-to-End Tests**: Playwright/Cypress for UX modules
- **Security Tests**: Automated tests for cross-tenant data access prevention (FR-030A) - verify User A cannot access User B's data under ANY circumstances, including bugs, misconfigured queries, malicious input, and other failure scenarios

**Target Platform**:
- **Backend**: Render (Sydney) - FastAPI Python runtime, PostgreSQL, Redis, RQ workers
- **Veris Finance**: Vercel-hosted Next.js web application (desktop-first, responsive) with TanStack Query, Tamagui
- **Frankie's Finance**: Expo EAS → iOS/Android native apps (mobile-first, spatial UX) with TanStack Query, Tamagui
- **Error Tracking**: Sentry (free tier) integrated across all modules

**Project Type**: Multi-module system (6 modules with API boundaries)

**Performance Goals** (p95 targets):
- **Compute Engine `/run`**: 95% of calculations complete within **2 seconds** for standard calculations (single tax calculation, super contribution). Reference: `specs/002-compute-engine/spec_002_compute_engine.md` SC-001, `Design_docs/final_design_questions.md` Section 5.
- **Compute Engine `/explain/{fact_id}`**: 95% respond within **50ms** at scale (10,000 concurrent users, 1 million Facts). Typical performance is **<10ms** via closure table/materialized view. Reference: `specs/002-compute-engine/spec_002_compute_engine.md` SC-004A, FR-020D, FR-020E, `Design_docs/final_design_questions.md` Section 5.
- **LLM Orchestrator**: 95% of intent parsing within 2 seconds
- **API Response**: 95% of API calls complete within **3 seconds** from initial query to displayed response (excluding complex multi-scenario calculations). Reference: `specs/001-master-spec/master_spec.md` SC-001, `Design_docs/final_design_questions.md` Section 5.
- **Explain Chains**: 95% of single `/explain` endpoints respond within 10ms (via closure table/materialized view); 95% respond within 50ms at scale (10,000 concurrent users, 1 million Facts) via read replicas and connection pooling
- **Background Jobs**: Long-running jobs return 202 + job ID immediately; job status via polling endpoint
- **Concurrent Users**: Support 10,000 concurrent users without performance degradation

**Caching Strategy**:
- **Ruleset snapshots**: Cached in memory/Redis, invalidated on ruleset publication. Reference: `Design_docs/final_design_questions.md` Section 5.
- **Hot Facts**: Cached in Redis with <1ms lookup times. Reference: `Design_docs/final_design_questions.md` Section 5.
- **Explain chains**: Pre-computed via closure table/materialized view. Reference: `Design_docs/final_design_questions.md` Section 5.
- **Reference data**: Frequently accessed reference metadata cached. Reference: `Design_docs/final_design_questions.md` Section 5.
- **Cache keys**: Format `inputs_hash + ruleset_id + as_of_date` with configurable TTL. Reference: `Design_docs/final_design_questions.md` Section 5.

**Depth Limits & Query Safety**:
- **Max recursion depth**: 15 levels for provenance chain traversal (typical 3-5 levels). Reference: `Design_docs/final_design_questions.md` Section 5.
- **Query timeout**: Default 30 seconds, configurable per operation type. Reference: `Design_docs/final_design_questions.md` Section 5.
- **Runaway prevention**: Circuit breakers, memory ceilings, profiling budgets, depth limit enforcement. Reference: `Design_docs/final_design_questions.md` Section 5.

**Constraints**:
- **Determinism**: 100% reproducibility (same inputs + ruleset + date = identical outputs)
- **Provenance**: 100% of Facts have complete provenance chains
- **Uptime**: 99.9% uptime for core compute APIs during business hours (8 AM - 8 PM AEST)
- **Privacy**: PII-minimal logging with field-level redaction
- **Compliance**: All advice validated by Advice Engine before presentation

**Scale/Scope**:
- **Users**: 10,000 concurrent users across all client applications
- **Rules**: Thousands of rules (calculation, taxation, compliance)
- **References**: Thousands of legal/regulatory sources with pinpoints
- **Facts**: Millions of computed Facts with full provenance
- **Scenarios**: Thousands of scenarios per user/adviser

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle I: Deterministic, Rule-Based Forecasting
- **Status**: COMPLIANT
- **Verification**: All calculations pin `ruleset_id` and `as_of` date; Facts are immutable with full provenance
- **Implementation**: Compute Engine enforces deterministic execution; all numeric tolerances explicit in rule definitions

### ✅ Principle II: Transparent, Auditable Advice
- **Status**: COMPLIANT
- **Verification**: All Facts have provenance chains (Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions)
- **Implementation**: `/explain/{fact_id}` endpoints use closure table/materialized view for instant chains (<10ms typical, <50ms at scale); relational edge table (src → dst with relation type) + JSONB metadata; bitemporal fields (`valid_from`/`valid_to`) for time-travel queries; partial indexes on current data for performance; read replicas for query distribution; connection pooling (PgBouncer) for efficient connection management; CONCURRENT materialized view refresh to avoid blocking queries

### ✅ Principle III: Relational Database Architecture
- **Status**: COMPLIANT
- **Verification**: PostgreSQL-only architecture; recursive CTEs for provenance, JSONB for relationships, temporal tables for time-travel
- **Implementation**: All data storage in PostgreSQL; no graph database; explainability via recursive CTEs

### ✅ Principle IV: LLM as Translator, Not Source of Truth
- **Status**: COMPLIANT
- **Verification**: LLM Orchestrator translates natural language to structured requests; never determines financial outcomes
- **Implementation**: All LLM outputs validated against rules before execution; LLM never replaces rule logic

### ✅ Principle V: Specification-Driven Development
- **Status**: COMPLIANT
- **Verification**: All rules authored as structured artifacts (Markdown/YAML) with schema validation, tests, two-person review
- **Implementation**: Versioned artifacts with effective-date time travel; signed bundles on publication

### ✅ Principle VI: Frontend-Agnostic Backend
- **Status**: COMPLIANT
- **Verification**: Backend accessible only through documented APIs; no direct end-user backend access
- **Implementation**: All access mediated by Frankie's Finance, Veris Finance, or Partner API

### ✅ Principle VII: Experience Principles
- **Status**: COMPLIANT
- **Verification**: Consumer experience (emotion-first, spatial metaphors) and adviser experience (professional calm, data-centric) defined
- **Implementation**: UX modules implement experience principles; navigation by intent

### ✅ Principle VIII: Reproducibility Over Convenience
- **Status**: COMPLIANT
- **Verification**: All compute operations pin `ruleset_id` and `as_of` date; scenarios never overwrite base reality
- **Implementation**: Idempotent runs with explicit idempotency keys; Facts immutable

### ✅ Principle IX: Precedence and Temporal Logic
- **Status**: COMPLIANT
- **Verification**: Rule resolution respects authority rank (Act > Regulation > Ruling > Guidance > Assumption)
- **Implementation**: Effective date windows enforced; temporal queries use `as_of` dates

### ✅ Principle X: Privacy, Tenancy, and Compliance
- **Status**: COMPLIANT
- **Verification**: Per-tenant isolation at data layer; PII-minimal logging; audit logs track all operations
- **Implementation**: Row-Level Security (RLS) policies enforced at PostgreSQL database level; API keys/OAuth with rate limits; compliance with Australian Privacy Act 1988

### ✅ Principle XI: Data Extraction and Quality Standards
- **Status**: COMPLIANT
- **Verification**: Five core data types (REFERENCES, RULES, ASSUMPTIONS, ADVICE GUIDANCE, CLIENT OUTCOME STRATEGIES) with quality standards
- **Implementation**: Completeness, accuracy, context, traceability, consistency, currency maintained

### ✅ Principle XII: Architectural Component Boundaries
- **Status**: COMPLIANT
- **Verification**: 
  - **Compute Engine** (FR-004A): Single source of truth for all deterministic financial logic; does not perform judgement, advice, or store knowledge objects
  - **References & Research Engine** (FR-004B): Single source of truth for all knowledge storage; does not perform calculations or generate advice
  - **Advice Engine** (FR-004C): Consumes Facts from Compute Engine and knowledge from References & Research Engine; applies reasoning frameworks, interpretation logic, and behavioral patterns; does not perform calculations that produce new Facts
  - **LLM Orchestrator** (FR-004D): Thin natural-language router; does not invent rules, perform calculations, or contain business logic
- **Implementation**: 
  - Compute Engine owns all tax formulas, caps, thresholds, eligibility tests, projections
  - References & Research Engine stores all REFERENCES, RULES, ASSUMPTIONS, ADVICE GUIDANCE, CLIENT OUTCOME STRATEGIES, FINDINGS, RESEARCH QUESTIONS, VERDICTS
  - Advice Engine applies interpretation logic, behavioral patterns, and reasoning frameworks to Facts (per CL-039)
  - LLM Orchestrator coordinates calls to engines but does not contain business logic

**Constitution Check Result**: ✅ **PASS** - All principles compliant. No violations requiring justification.

## Project Structure

### Documentation (Master Plan)

```text
specs/001-master-spec/
├── master_spec.md             # Master specification
├── master_plan.md             # This file (master implementation plan)
├── MODULE_SPEC_STRUCTURE.md  # Module spec structure guidance
├── CONSISTENCY_CHECK.md       # Consistency check report
├── research.md                # Phase 0 output (technology research)
├── data-model.md              # Phase 1 output (canonical data model)
├── quickstart.md              # Phase 1 output (developer quickstart)
├── contracts/                 # Phase 1 output (API contracts)
│   ├── compute-engine.openapi.yaml
│   ├── advice-engine.openapi.yaml
│   ├── llm-orchestrator.openapi.yaml
│   ├── references-research-engine.openapi.yaml
│   └── partner-api.openapi.yaml
└── schemas/                   # Canonical schemas (shared across all modules)
    ├── README.md              # Schema documentation and usage guide
    ├── data/                  # Data model schemas (Pydantic, JSON Schema)
    │   ├── rule.yaml          # Rule schema definition
    │   ├── reference.yaml     # Reference schema definition
    │   ├── assumption.yaml    # Assumption schema definition
    │   ├── advice_guidance.yaml  # Advice Guidance schema definition
    │   ├── client_outcome_strategy.yaml  # Client Outcome Strategy schema
    │   ├── scenario.yaml      # Scenario schema definition
    │   ├── client_event.yaml  # Client Event schema definition
    │   └── fact.yaml          # Fact schema definition
    ├── api/                   # API request/response schemas
    │   ├── compute-engine/    # Compute Engine API schemas
    │   ├── advice-engine/     # Advice Engine API schemas
    │   ├── llm-orchestrator/  # LLM Orchestrator API schemas
    │   └── references-research-engine/  # References & Research Engine API schemas
    └── database/              # Database schema definitions
        └── postgres/          # PostgreSQL schema (SQL, Alembic migrations) - no Neo4j
```

### Module Specifications

```text
specs/
├── 001-master-spec/          # Master spec and plan (this module)
├── 002-compute-engine/        # Compute Engine module spec
├── 003-references-research-engine/  # References & Research Engine spec
├── 004-advice-engine/         # Advice Engine spec
├── 005-llm-orchestrator/     # LLM Orchestrator spec
│   └── primers-prompts/       # LLM primers and prompts (.md files with A/B versioning)
├── 006-frankies-finance/     # Frankie's Finance UX spec
└── 007-veris-finance/        # Veris Finance UX spec
```

### Source Code (Repository Root)

```text
backend/
├── compute-engine/           # Compute Engine module
│   ├── src/
│   │   ├── calculation/      # Calculation logic
│   │   ├── rules/            # Rule execution
│   │   ├── provenance/       # Provenance chain building
│   │   ├── storage/          # PostgreSQL storage adapters
│   │   ├── explanations/     # Explanation repository index and loader
│   │   └── api/              # FastAPI endpoints
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── property/         # Property-based tests
│
├── references-research-engine/  # References & Research Engine module
│   ├── src/
│   │   ├── ingestion/        # Document ingestion pipeline
│   │   ├── storage/          # Reference storage and versioning
│   │   ├── search/           # RAG-style retrieval
│   │   └── api/              # FastAPI endpoints
│   └── tests/
│
├── advice-engine/             # Advice Engine module
│   ├── src/
│   │   ├── compliance/       # Compliance evaluation logic
│   │   ├── best-interests/    # Best-interests duty checks
│   │   ├── validation/       # Advice validation
│   │   └── api/              # FastAPI endpoints
│   └── tests/
│
├── llm-orchestrator/         # LLM Orchestrator module
│   ├── src/
│   │   ├── intent/           # Intent detection
│   │   ├── parsing/          # Natural language parsing
│   │   ├── routing/          # Model vendor routing
│   │   ├── filtering/        # PII/safety filtering
│   │   ├── prompts/          # Prompt/primer loading (references specs/005-llm-orchestrator/primers-prompts/)
│   │   └── api/              # FastAPI endpoints
│   └── tests/
│
└── shared/                   # Shared backend code
    ├── models/                # Canonical data models (imported from specs/001-master-spec/schemas/)
    ├── storage/               # Storage abstractions
    ├── auth/                  # Authentication/authorization
    └── observability/         # Logging, metrics, tracing

frontend/
├── veris-finance/            # Veris Finance (adviser UX)
│   ├── src/
│   │   ├── components/       # React components (Tamagui)
│   │   ├── pages/            # Page components
│   │   ├── services/         # API clients (TanStack Query)
│   │   ├── hooks/           # React hooks
│   │   └── theme/           # Tamagui design tokens
│   └── tests/
│
└── frankies-finance/         # Frankie's Finance (consumer UX)
    ├── src/
    │   ├── components/       # React Native components (Tamagui)
    │   ├── screens/         # Screen components
    │   ├── services/        # API clients (TanStack Query)
    │   ├── navigation/      # Spatial navigation
    │   ├── frankie/         # Frankie companion logic
    │   └── theme/           # Tamagui design tokens
    └── tests/

infrastructure/
├── vercel/                   # Vercel configuration files (vercel.json per module)
├── env/                      # Environment variable templates (.env.example)
└── ci-cd/                    # CI/CD pipelines (GitHub Actions for testing, Vercel for deployment)

rules/                        # Rule artifacts (Markdown/YAML)
├── calculation/              # Calculation rules
├── taxation/                # Taxation rules
└── compliance/              # Compliance rules

explanations/                 # Calculation function explanations repository
├── index.yaml                # Central index of all calculation functions
├── functions/                # Individual function explanation files
│   ├── CAL-FND-001_time_axis.md
│   ├── CAL-FND-002_compounding.md
│   ├── CAL-PIT-001_taxable_income.md
│   └── ...                  # One file per calculation function
└── README.md                # Explanation repository documentation

tests/
├── golden-datasets/          # Regulator examples (ATO, ASIC)
├── integration/              # End-to-end integration tests
└── performance/              # Performance/load tests
```

**Structure Decision**: Multi-module monorepo with clear module boundaries. Backend modules are Python-based FastAPI applications deployed on Render with SQLAlchemy 2.0 + Pydantic v2, RQ workers for background jobs, and Sentry for error tracking. Frontend modules are separate applications (web for Veris with Next.js + TanStack Query + Tamagui, mobile for Frankie with Expo + TanStack Query + Tamagui). **Canonical schemas stored in `specs/001-master-spec/schemas/`** - all modules import from this master folder (no local copies). Shared code in `backend/shared/` for common models and utilities (models imported from canonical schemas). Shared design tokens via Tamagui across both frontends. GitHub Actions for testing, Render/Vercel/Expo EAS handle deployments automatically.

## Core Artifacts

This section documents the core artifacts across the repository. Each code module (Type 1) **MUST** maintain a `FILE_MANIFEST.md` at its root that tracks important files and their purposes. See `.cursor/rules/file-manifest.mdc` for detailed requirements.

### Backend Modules

**Compute Engine** (`backend/compute-engine/`):
- Core calculation services and rule execution
- Deterministic financial calculations with full provenance
- Test suites including property-based tests
- **Spec**: `specs/002-compute-engine/`

**References & Research Engine** (`backend/references-research-engine/`):
- Reference storage and ingestion services
- Research automation (scraping, cleaning, extraction)
- Version management and provenance tracking
- Search and RAG capabilities
- **Spec**: `specs/003-references-research-engine/`

**Advice Engine** (`backend/advice-engine/`):
- Compliance checking and suitability analysis
- Advice generation and documentation
- **Spec**: `specs/004-advice-engine/`

**LLM Orchestrator** (`backend/llm-orchestrator/`):
- Natural language intent parsing
- LLM routing and prompt management
- RAG integration for prompt augmentation
- **Spec**: `specs/005-llm-orchestrator/`

**Shared Backend Code** (`backend/shared/`):
- Common models and utilities (imported from canonical schemas)
- Authentication and authorization
- Storage abstractions and database connections
- Observability (logging, metrics, tracing)
- Security utilities

### Frontend Modules

**Veris Finance** (`frontend/veris-finance/`):
- Adviser-facing web application (Next.js)
- Desktop-first UX with print-ready outputs
- **Spec**: `specs/007-veris-finance/`

**Frankie's Finance** (`frontend/frankies-finance/`):
- Consumer-facing mobile application (Expo/React Native)
- Mobile-first spatial UX
- **Spec**: `specs/006-frankies-finance/`

### Spec Directories

**Master Spec** (`specs/001-master-spec/`):
- Master specification coordinating all modules
- Canonical schemas (`schemas/`)
- API contracts (`contracts/`)
- Master plan and tasks

**Module Specs** (`specs/002-*` through `specs/007-*`):
- Feature-specific specifications
- Implementation plans
- Task lists
- Research decisions and data models

### Research and Design Folders

**Research** (`Research/`):
- Primary authorities, secondary sources, media transcripts
- Structured data and raw documents
- Research progress tracking

**Design Docs** (`Design_docs/`):
- High-level design concepts
- Architecture decisions
- User stories and UX concepts

**Explanations** (`explanations/`):
- Calculation function explanations
- Central index (`index.yaml`)

### Infrastructure and Tooling

**Infrastructure** (`infrastructure/`):
- Database schemas and migrations
- Cache configuration (Redis)
- Monitoring and observability configs
- Security policies

**CI/CD** (`.github/workflows/`):
- Automated testing workflows
- Deployment pipelines

## Complexity Tracking

> **No Constitution Violations** - All architecture decisions comply with constitution principles. No complexity justification required.

## Implementation Phases

### Phase 0: Foundational Infrastructure (Days 1-2)

**Goal**: Establish foundational infrastructure enabling all modules.

**Timeline**: Compressed to 2 days for AI-assisted development (total project timeline: 2 weeks)

**Tasks**: See `specs/001-master-spec/master_tasks.md` Phase 0 for detailed task breakdown. High-level areas:
1. **Storage Setup** - PostgreSQL database, provenance architecture, Redis cache, RQ workers
2. **API Framework** - FastAPI, SQLAlchemy 2.0, Pydantic v2, background job processing
3. **Authentication/Authorization** - OAuth2/JWT, tenant isolation, RBAC
4. **Observability** - Structured logging, Sentry, distributed tracing, cost tracking
5. **Security Hardening** - Encryption, secrets management, input hardening, security tests
6. **CI/CD Pipeline** - GitHub Actions, Vercel/Render/Expo EAS deployments, preview environments

**Dependencies**: None (foundational)

**Deliverables**:
- Vercel projects configured for all modules
- CI/CD pipeline functional (GitHub Actions for testing, Vercel for deployment)
- Authentication/authorization working
- Observability configured (with correlation IDs, health checks, feature flags)
- Security hardening implemented (encryption, Vercel secrets management, input hardening, SBOM)
- Immutable audit logs configured
- Vercel environment variables and secrets configured

### Phase 1: Research & References & Research Engine (Days 3-5)

**Goal**: Research phase - Build References & Research Engine, extract logic from MVP research documents, and create database schemas.

**Timeline**: 3 days (Days 3-5 of 2-week timeline)

**Pre-Phase 1 Prerequisites** (Must be completed before Phase 1 research begins):
1. **Compute Engine Requirements Context Creation**
   - Create `specs/003-references-research-engine/research_guidance/compute-engine-requirements-context.md`
   - Document all required fields for calculation function extraction (input parameters, output format, formula, edge cases, regulatory sources, rounding rules)
   - Define extraction templates for each calculation type (CAL-*)
   - Create completeness validation checklist
   - Document incomplete extraction handling procedures
   - Reference: This context guides LLM-assisted research to extract complete, implementation-ready specifications

2. **Primer Enhancement**
   - Enhance `specs/005-llm-orchestrator/primers-prompts/primer_external_research_v1a.md` to include Compute Engine requirements context
   - Add section on Compute Engine requirements context integration (Section 1.1)
   - Add calculation function extraction requirements (Section 5.3)
   - Update practical guidelines to include completeness validation (Section 13)
   - Ensure primer loads/applies requirements context from FIRST research iteration

**Tasks**: See `specs/001-master-spec/master_tasks.md` Phase 1 for detailed task breakdown. High-level areas:
1. **LLM Orchestrator Setup (Research Support)** - Basic functionality for research support, primer configuration
2. **References & Research Engine** - See `specs/003-references-research-engine/plan_003_references_research_engine.md` for detailed 7-phase implementation plan
3. **Research & Logic Extraction** - Process MVP research documents, extract logic using knowledge taxonomy, validate extraction quality
4. **Database Schema Creation** - Create schemas based on extracted logic, set up Alembic migrations with rollback support
5. **Canonical Schemas Creation** - Create canonical schemas in `specs/001-master-spec/schemas/` for all 14 Canonical Concepts
6. **API Contracts and Client SDK Generation** - Generate OpenAPI schemas, set up client SDK generation pipeline

**Cross-Module Coordination**:
- LLM Orchestrator must support research phase (basic functionality)
- References & Research Engine processes all MVP research documents
- Extracted logic informs Compute Engine and Advice Engine design
- Database schemas created based on research findings
- Canonical schemas created in master folder for all modules to import

**API Contracts**: See module-specific plans for detailed API specifications.

**API Contract Freeze Points**:
- **Freeze A (Phase 1 end)**: All OpenAPI schemas finalized, client SDK generation operational
  - **Phase 1 – Schema Dress Rehearsal & Feedback Loop (Pre-Freeze A)**: Before Freeze A is declared, a mandatory Schema Dress Rehearsal must be completed. This involves implementing four real end-to-end golden calculations (PAYG marginal tax 2024–25 + offsets, CGT discount event, super contributions + Div 293, negative gearing mortgage interest) using the actual PostgreSQL + SQLAlchemy models generated from the research so far. Every place the schema exhibits friction (missing relation requiring >2 joins to traverse, awkward join patterns requiring >3 table joins, missing provenance role preventing complete chain construction, excessive JSONB usage with nested depth >2 or JSONB queries where relational structure would be more appropriate) must be logged in `backend/compute-engine/src/schema_rehearsal/friction_log.md` and fixed before Freeze A is declared. Freeze A only happens after Schema Dress Rehearsal passes with zero open schema-friction items.
- **Freeze B (mid Phase 2)**: `/run`, `/facts`, `/explain/{fact_id}` schemas stable
- **Freeze C (Phase 3 start)**: LLM Orchestrator `parse/chat` schemas + validation rules stable

**Deliverables**:
- References & Research Engine operational (see `specs/003-references-research-engine/plan_003_references_research_engine.md` for detailed deliverables)
- LLM Orchestrator basic functionality for research support
- All logic extracted from MVP research documents
- All relational database schemas created and migrated
- Canonical schemas created in `specs/001-master-spec/schemas/`
- OpenAPI contracts generated for all modules
- API client SDK generation pipeline operational

### Phase 2: Knowledge Base Seeding & Compute Engine Foundation (Days 6-8)

**Goal**: Go from "empty pipeline" to "we have a meaningful set of findings, rules and calculations", then build Compute Engine using real canonical data.

**Timeline**: 3 days (Days 6-8 of 2-week timeline)

#### Phase 2A – Seed the knowledge base with real documents (Days 6-7)

**Goal**: Go from "empty pipeline" to "we have a meaningful set of findings, rules and calculations".

**Tasks**: See `specs/001-master-spec/master_tasks.md` Phase 2A for detailed task breakdown. High-level areas:
1. **Populate /Research** - High-leverage document set (ATO tax essentials, super contributions & Div 293, CGT, ASIC RGs)
2. **Run ingestion + cleaning pipeline** - Process documents through Data Cleaning Submodule, batch process with RQ workers
3. **Run auto-extraction loop** - Auto-Extract → Auto-Question → Auto-Validate → Auto-Curate, generate findings with provenance
4. **Manual review sample** - Verify key calculations (PAYG, CGT discount, super caps) against primary sources

**Cross-Module Coordination**:
- Uses References & Research Engine infrastructure built in Phase 1
- Applies Compute Engine requirements context for extraction completeness validation
- Findings stored in database with proper lifecycle states (Draft → Pending Review → Approved)

**Deliverables**:
- High-leverage document set populated in `/Research`
- Documents processed and stored in References & Research Engine
- Real findings (rules, calculations, strategies) extracted and stored in database
- Sample calculations manually verified against primary sources

#### Phase 2B – Make canonical_calculations.yaml real and trustworthy (Day 7.5)

**Goal**: Canonical list that the compute engine can safely rely on.

**Tasks**: See `specs/001-master-spec/master_tasks.md` Phase 2B for detailed task breakdown. High-level areas:
1. **Run canonical list generator** - Generate `Research/canonical_calculations.yaml` with actual IDs, inputs, completeness/trust scores
2. **Verify MVP calculations** - Confirm "four golden" calculations appear, check inputs/assumptions, review completeness scores
3. **Add "Ready for Compute" checklist** - Track readiness status (≥85% completeness, ≥85 trust score, at least one golden example)

**Cross-Module Coordination**:
- Canonical list generator queries Finding model from References & Research Engine
- Completeness validation uses Compute Engine requirements context
- Flagged incomplete calculations trigger research refinement requests

**Deliverables**:
- `Research/canonical_calculations.yaml` populated with real findings
- Each calculation has completeness/trust scores
- "Ready for Compute" status tracked for each calculation
- Incomplete calculations flagged with refinement requests

#### Phase 2B.5 – Automated Calculation Refinement (Day 7.75)

**Goal**: Automatically refine calculations based on LLM review feedback to achieve correctness and completeness.

**Key Innovation**: Implements an iterative refinement pipeline that:
1. **Reviews calculations** - LLM reviews each calculation for accuracy, completeness, and correctness
2. **Extracts issues** - Parses LLM review feedback into structured issues (formula errors, missing elements, incorrect regulatory references)
3. **Generates fixes** - LLM generates corrected calculation YAML based on identified issues
4. **Applies fixes** - Merges fixes into original calculations while preserving metadata
5. **Validates fixes** - Re-reviews fixed calculations to verify issues were addressed
6. **Tracks iterations** - Monitors refinement progress and prevents infinite loops

**Architecture**: 
- Module: `backend/references-research-engine/src/research/calculation_refinement/`
- Components: Review extractor, fix generator, fix applier, fix validator, iteration tracker, refinement orchestrator
- Integration: Uses existing LLM infrastructure (OpenRouter, DeepSeek), integrates with refinement tracking system
- Output: Updated `MVP_canonical_calculations.yaml` with corrected calculations

**Workflow**:
- Takes LLM review results from `review_mvp_calculations.py`
- Iteratively refines each calculation until marked CORRECT or max iterations reached
- Tracks all iterations with before/after assessments
- Provides detailed logs of fixes applied

**Deliverables**:
- Automated refinement module implemented
- MVP calculations refined based on LLM review feedback
- Iteration tracking and validation in place
- Updated `MVP_canonical_calculations.yaml` with corrections

**Validation Considerations** (Deferred to Phase 4):
- **Independent verification mechanisms** were considered but not implemented in Phase 2B.5:
  - Test case execution validation (execute calculations and verify outputs match expected values)
  - Golden dataset validation (compare against ATO official examples)
  - Independent LLM review (cross-check with different model)
  - Mathematical formula verification (syntax and logic checks)
  - Change diff analysis (detailed before/after comparison)
- **Current validation** relies on LLM self-assessment (same model that fixed validates its own fixes)
- **Future enhancement**: Implement comprehensive validation mechanisms in Phase 4 to ensure LLM improvements are independently verified and calculations are mathematically correct

**Tasks**: See `specs/001-master-spec/master_tasks.md` Phase 2B.5 for detailed task breakdown.

#### Phase 2C – Build test harness around research output (Day 8)

**Goal**: Makes the whole thing safe enough to base advice on.

**Tasks**: See `specs/001-master-spec/master_tasks.md` Phase 2C for detailed task breakdown. High-level areas:
1. **Create golden examples set** - Store official inputs + outputs + citations for "four golden" calculations in `tests/golden-datasets/`
2. **Write tests that pull rules/findings from DB** - Validate extracted logic matches official behaviour, test findings → canonical list chain
3. **Add tests that validate research integrity** - No orphaned rules, complete provenance chains, proper lifecycle states
4. **Test research drift detection** - Catch canonical list drift, validate finding-reference links remain valid

**Cross-Module Coordination**:
- Tests query References & Research Engine for findings and references
- Tests validate canonical list matches database state
- Tests ensure provenance chains are complete before Compute Engine uses them

**Deliverables**:
- Golden examples set created from ATO/ASIC worked examples
- Tests validate extracted logic against official examples
- Tests validate research integrity (no orphaned rules, complete provenance)
- Research drift detection tests operational

#### Phase 2D – Compute Engine "Phase 2 proper" (Days 7.5-8)

**Goal**: Build Compute Engine consuming real canonical data rather than theoretical stubs.

**Prerequisites**:
- Phase 2A complete: Real findings in database
- Phase 2B complete: Populated `canonical_calculations.yaml`
- Phase 2C complete: Verified golden examples

**Tasks**: See `specs/001-master-spec/master_tasks.md` Phase 2D for detailed task breakdown. High-level areas:
1. **Compute Engine** - See `specs/002-compute-engine/plan_002_compute_engine.md` for detailed 8-phase implementation plan
2. **PostgreSQL Data Structures Setup** - Create schema and structures, implement Publish → Validate → Activate workflow
3. **LLM Orchestrator Progress** - See `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` for detailed 8-phase implementation plan

**Cross-Module Coordination**:
- Compute Engine uses References & Research Engine for rule-to-reference lookups
- Compute Engine loads canonical calculation list (generated in Phase 2B) from `Research/canonical_calculations.yaml`
- Compute Engine creates ruleset snapshots in PostgreSQL (from Phase 1 schemas)
- LLM Orchestrator transforms natural language to structured Compute Engine requests
- All modules depend on Phase 0 foundational infrastructure
- Compute Engine validates calculations against golden examples from Phase 2C

**API Contracts**: See module-specific plans for detailed API specifications.

**Deliverables**:
- Compute Engine operational (see `specs/002-compute-engine/plan_002_compute_engine.md`)
- PostgreSQL schema created and populated with all data structures
- Ruleset snapshots created in PostgreSQL
- LLM Orchestrator can convert natural language to structured calculation requests
- Calculations validated against golden examples (100% match for golden examples)

### Phase 3: Advice Engine (Days 9-10)

**Goal**: Build Advice Engine and progress LLM Orchestrator for compliance checking workflows.

**Timeline**: 2 days (Days 9-10 of 2-week timeline)

**Tasks**: See `specs/001-master-spec/master_tasks.md` Phase 3 for detailed task breakdown. High-level areas:
1. **Advice Engine** - See `specs/004-advice-engine/plan_004_advice_engine.md` for detailed 6-phase implementation plan
2. **LLM Orchestrator Progress** - Progress sufficient for Advice Engine workflows, natural language to compliance check transformation
3. **RAG Capability Implementation** - See `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7 for detailed RAG implementation

**Cross-Module Coordination**:
- Advice Engine depends on Compute Engine for Fact data
- Advice Engine depends on References & Research Engine for regulatory requirements
- LLM Orchestrator supports Advice Engine compliance workflows
- All modules depend on Phase 1 and Phase 2 modules

**API Contracts**: See module-specific plans for detailed API specifications.

**Deliverables**:
- Advice Engine operational (see `specs/004-advice-engine/plan_004_advice_engine.md` for detailed deliverables)
- LLM Orchestrator supports Advice Engine workflows
- RAG capability implemented (see `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7)

### Phase 4: Veris Finance (Days 11-12)

**Goal**: Build Veris Finance (adviser UX) and update LLM Orchestrator to deliver this application.

**Timeline**: 2 days (Days 11-12 of 2-week timeline)

**Tasks**: See `specs/001-master-spec/master_tasks.md` Phase 4 for detailed task breakdown. High-level areas:
1. **Veris Finance** - See `specs/007-veris-finance/plan_007_veris_finance.md` for detailed 9-phase implementation plan
2. **LLM Orchestrator Update** - Update to deliver Veris Finance application, professional language formatting

**Cross-Module Coordination**:
- Veris Finance depends on all Phase 1, 2, and 3 backend modules
- Veris Finance consumes backend APIs via documented contracts
- LLM Orchestrator provides natural language interface for Veris Finance
- Testing Veris Finance validates backend features before Frankie's Finance

**API Contracts**: See module-specific plans for detailed API integration specifications.

**Deliverables**:
- Veris Finance operational (see `specs/007-veris-finance/plan_007_veris_finance.md` for detailed deliverables)
- LLM Orchestrator updated to support Veris Finance

### Phase 5: Frankie's Finance (Days 13-14)

**Goal**: Build Frankie's Finance (consumer UX) and update LLM Orchestrator to deliver this application.

**Timeline**: 2 days (Days 13-14 of 2-week timeline)

**Tasks**: See `specs/001-master-spec/master_tasks.md` Phase 5 for detailed task breakdown. High-level areas:
1. **Frankie's Finance** - See `specs/006-frankies-finance/plan_006_frankies_finance.md` for detailed 9-phase implementation plan
2. **LLM Orchestrator Update** - Update to deliver Frankie's Finance application, consumer-friendly language formatting

**Cross-Module Coordination**:
- Frankie's Finance depends on all Phase 1, 2, 3, and 4 modules
- Frankie's Finance consumes backend APIs via documented contracts
- LLM Orchestrator provides natural language interface for Frankie's Finance
- Backend features validated through Veris Finance before consumer experience

**API Contracts**: See module-specific plans for detailed API integration specifications.

**Deliverables**:
- Frankie's Finance operational (see `specs/006-frankies-finance/plan_006_frankies_finance.md` for detailed deliverables)
- LLM Orchestrator updated to support Frankie's Finance

## Cross-Module Coordination

### Canonical Schemas (Shared Master Folder)

**Requirement**: All modules MUST use canonical schemas stored in `specs/001-master-spec/schemas/`. This master folder contains the single source of truth for all data models, API contracts, and database schemas shared across modules.

**Schema Organization**:
- **`schemas/data/`**: Canonical data model schemas (Rule, Reference, Assumption, Advice Guidance, Client Outcome Strategy, Scenario, Client Event, Fact) in YAML/JSON Schema format
- **`schemas/api/`**: API request/response schemas organized by module (OpenAPI schemas, Pydantic models)
- **`schemas/database/`**: Database schema definitions (PostgreSQL SQL/Alembic migrations only - no Neo4j)

**Usage Pattern**:
- All modules MUST import canonical schemas from `specs/001-master-spec/schemas/`
- Backend modules load schemas into `backend/shared/models/` (Python Pydantic models)
- Frontend modules load schemas into `frontend/shared/types/` (TypeScript types)
- Database migrations reference schemas from master folder
- API contracts reference schemas from master folder

**Benefits**:
- Single source of truth for all data structures
- Consistency across modules (no schema drift)
- Version-controlled schema evolution
- Schema validation at build time
- Type safety across module boundaries

**Cross-Module Impact**: All modules depend on canonical schemas. Schema changes require coordination across affected modules. Schema versioning ensures backward compatibility.

**Implementation**:
- Phase 1: Create canonical schemas based on extracted logic from MVP research documents
- All modules reference schemas from master folder (no local copies)
- Schema changes require PR review and affect all dependent modules
- Schema versioning strategy documented in `specs/001-master-spec/schemas/README.md`

### API Contracts and Client SDK Generation

**Requirement**: All API endpoints MUST have OpenAPI schemas, and client SDKs MUST be generated from these schemas to ensure type safety and prevent drift.

**OpenAPI Schema Location**:
- **`specs/001-master-spec/contracts/`**: OpenAPI 3.0 schemas for all modules
  - `compute-engine.openapi.yaml` - See `specs/002-compute-engine/plan_002_compute_engine.md` for API details
  - `advice-engine.openapi.yaml` - See `specs/004-advice-engine/plan_004_advice_engine.md` for API details
  - `llm-orchestrator.openapi.yaml` - See `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` for API details
  - `references-research-engine.openapi.yaml` - See `specs/003-references-research-engine/plan_003_references_research_engine.md` for API details
  - `partner-api.openapi.yaml` - Partner API (aggregated endpoints from all modules)

**Client SDK Generation**:
- **Tooling**: Use openapi-typescript-codegen or orms to generate TypeScript clients from OpenAPI schemas
- **Output Location**: `frontend/shared/api-client/` - Generated TypeScript API client packages
- **Version Pinning**: Generated clients MUST be pinned to specific OpenAPI schema versions
- **Generation Process**: Automated via CI/CD on OpenAPI schema changes
- **Type Safety**: Generated clients provide full TypeScript type safety for all API requests/responses

**CI/CD Validation**:
- **Contract Drift Detection**: CI MUST fail if OpenAPI/TS types drift vs generated clients (see T029B)
- **Schema Validation**: Validate OpenAPI schemas against OpenAPI 3.0 specification
- **Client Generation Check**: Ensure generated clients match OpenAPI schemas exactly
- **Breaking Changes Detection**: Detect breaking changes in OpenAPI schemas and require version bump

**API Versioning**:
- **URL Path Versioning**: All APIs use `/api/v{major}/...` format (see `API_VERSIONING_POLICY.md`)
- **Breaking Changes**: Require new major version (`/api/v2/...`) with 6-month deprecation timeline
- **Deprecation Warnings**: Include deprecation headers in responses for deprecated versions
- **Migration Support**: Provide migration guides and code examples for version upgrades

**Contract Freeze Points** (see `master_tasks.md` for enforcement):
- **Freeze A (Phase 1 end)**: All OpenAPI schemas finalized, client SDK generation operational
- **Freeze B (mid Phase 2)**: `/run`, `/facts`, `/explain/{fact_id}` schemas stable
- **Freeze C (Phase 3 start)**: LLM Orchestrator `parse/chat` schemas + validation rules stable

**Cross-Module Impact**: All frontend modules (Frankie's Finance, Veris Finance) depend on generated API clients. Backend modules validate requests/responses against OpenAPI schemas. Schema changes require coordination and may trigger version bumps.

**Implementation**:
- Phase 1: Generate OpenAPI schemas for all modules, set up client SDK generation pipeline
- Phase 1: Configure CI validation for contract drift detection
- Phase 1: Document API client generation process and versioning strategy
- Ongoing: Maintain OpenAPI schemas, regenerate clients on schema changes, enforce contract freeze points

### Calculation Function Explanation Repository

**Requirement**: Compute Engine maintains a central explanation repository for all calculation functions. See `specs/002-compute-engine/plan_002_compute_engine.md` for detailed implementation.

**Relationship to Canonical Calculation List**: The explanation repository derives from and extends the canonical calculation list (`Research/canonical_calculations.yaml`) generated by References & Research Engine (Module 3, Phase 4). The canonical list provides research-derived specifications (WHAT calculations should do), while explanations document implementation details (HOW calculations were implemented). Explanations are auto-populated from canonical list data and add implementation-specific details (rationale, testing approach, code references). Each explanation MUST reference its canonical source via `canonical_calculation_id` field.

**Cross-Module Impact**: 
- Explanation repository enables provenance chains and `/explain` endpoints used by Veris Finance and Frankie's Finance
- Explanation repository depends on canonical calculation list from References & Research Engine
- When canonical list is updated, explanations should be flagged for review to ensure synchronization

### Version Control and Testing Strategy

**Per User Guidance**: Automated commits after each task has been tested.

**Key Requirements**:
- Test coverage > 80% for backend modules, > 75% for frontend modules
- Golden dataset tests for calculation accuracy (ATO/ASIC examples)
- Minimum Validation Suite required before shipping (see Success Metrics section)
- See `specs/001-master-spec/master_tasks.md` for detailed testing requirements per phase

### LLM Model Selection Strategy

**Per User Guidance**: Different LLM models for different tasks with intelligent switching, preference for cheaper models based on performance requirements.

**MVP Constraint**: OpenRouter for all LLM interactions, supporting both OpenRouter credits and BYOK integration. See `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` for detailed implementation.

**Cross-Module Impact**: LLM Orchestrator routes requests to appropriate models. References & Research Engine uses LLM-assisted research. Both UX modules consume LLM Orchestrator services.

### Primer Management Strategy

**Location**: All primers stored in `specs/005-llm-orchestrator/primers-prompts/` directory

**Cross-Module Usage**: See `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` for detailed primer management implementation.

## Integration Checkpoints

**Timeline**: All checkpoints compressed to 2-week timeline (AI-assisted development)

### Checkpoint 1: Phase 1 Complete (Day 5)
- References & Research Engine operational (all 7 phases complete per `specs/003-references-research-engine/plan_003_references_research_engine.md`)
- LLM Orchestrator basic functionality for research support
- All logic extracted from MVP research documents
- All relational database schemas created and migrated
- Core reference data populated

### Checkpoint 2A: Phase 2A Complete (Day 7)
- High-leverage document set populated in `/Research`
- Documents processed and stored in References & Research Engine
- Real findings (rules, calculations, strategies) extracted and stored in database
- Sample calculations manually verified against primary sources (PAYG, CGT discount, super caps)

### Checkpoint 2B: Phase 2B Complete (Day 7.5)
- `Research/canonical_calculations.yaml` populated with real findings
- Each calculation has completeness/trust scores
- "Ready for Compute" status tracked for each calculation
- Incomplete calculations flagged with refinement requests

### Checkpoint 2C: Phase 2C Complete (Day 8 morning)
- Golden examples set created from ATO/ASIC worked examples
- Tests validate extracted logic against official examples
- Tests validate research integrity (no orphaned rules, complete provenance)
- Research drift detection tests operational

### Checkpoint 2D: Phase 2D Complete (Day 8)
- Compute Engine operational (see `specs/002-compute-engine/plan_002_compute_engine.md`)
- PostgreSQL schema created and populated with all data structures
- Ruleset snapshots created in PostgreSQL
- LLM Orchestrator can convert natural language to structured calculation requests
- Integration between References & Research Engine and Compute Engine validated
- Calculations validated against golden examples (100% match for golden examples)

### Checkpoint 3: Phase 3 Complete (Day 10)
- Advice Engine operational (see `specs/004-advice-engine/plan_004_advice_engine.md`)
- LLM Orchestrator supports Advice Engine workflows
- Integration between all backend modules validated

### Checkpoint 4: Veris Finance Complete (Day 12)
- Veris Finance operational (see `specs/007-veris-finance/plan_007_veris_finance.md`)
- LLM Orchestrator updated to support Veris Finance
- Integration with all backend modules validated
- Professional workflow end-to-end tested

### Checkpoint 5: Frankie's Finance Complete (Day 14)
- Frankie's Finance operational (see `specs/006-frankies-finance/plan_006_frankies_finance.md`)
- LLM Orchestrator updated to support Frankie's Finance
- Integration with all backend modules validated
- Consumer experience end-to-end tested

## Risk Management

### High-Risk Areas

1. **Deterministic Calculations**
   - **Risk**: Non-deterministic calculations undermine trust
   - **Mitigation**: Comprehensive testing, property-based tests, golden datasets
   - **Validation**: 
     - Minimum validation suite: 10 ATO examples + 5 ASIC examples + 100% deterministic reproducibility + Veris Finance test forecasts
     - Veris Finance test forecasts for every calculation
     - **CRITICAL**: System MUST NOT ship without minimum validation suite complete

2. **Provenance Chains**
   - **Risk**: Missing provenance links break auditability
   - **Mitigation**: Comprehensive testing, recursive CTE validation for provenance chains
   - **Validation**: 100% provenance chain completeness tests

3. **LLM Model Routing**
   - **Risk**: Incorrect model selection impacts performance/cost
   - **Mitigation**: Performance monitoring, automatic fallback, cost tracking
   - **Validation**: A/B testing, performance benchmarks

4. **Compliance Validation**
   - **Risk**: Non-compliant advice breaks regulatory requirements
   - **Mitigation**: Comprehensive compliance testing, golden datasets (ASIC examples)
   - **Validation**: 
     - Minimum validation suite: At least 5 ASIC compliance examples validated before shipping
     - 100% advice validated by Advice Engine before presentation
     - **CRITICAL**: System MUST NOT ship without ASIC compliance examples validated

5. **PostgreSQL Storage Architecture**
   - **Risk**: Ruleset snapshot consistency issues break reproducibility
   - **Mitigation**: Comprehensive validation checks, forbidden direct database edits outside of versioned artifacts
   - **Validation**: Ruleset integrity tests, time-travel query tests, provenance link integrity tests

6. **RAG Retrieval**
   - **Risk**: Low retrieval relevance reduces RAG effectiveness; high latency degrades user experience; cross-tenant data access in RAG retrieval; RAG augmentation bypasses rule validation (Principle IV violation)
   - **Mitigation**: Comprehensive testing, golden dataset validation (95% relevance target), Redis caching (80% hit rate target), query optimization, database-level RLS policies, application-level validation, strict validation that retrieved data grounds prompts only
   - **Validation**: 
     - 95% retrieval relevance (validated against golden dataset)
     - <1 second (p95) retrieval latency
     - 100% tenant isolation in RAG retrieval operations
     - 100% compliance with Principle IV (LLM remains translator only)
     - Property-based tests for edge cases (no relevant data, excessive results, conflicting data)

### Medium-Risk Areas

1. **Performance at Scale**
   - **Risk**: Performance degradation with 10,000 concurrent users
   - **Mitigation**: Load testing, performance optimization, caching
   - **Validation**: Load tests, performance benchmarks

2. **UX Complexity**
   - **Risk**: Complex UX (spatial navigation, emotion-first design) difficult to implement
   - **Mitigation**: Prototyping, user testing, iterative development
   - **Validation**: User acceptance tests, usability testing

3. **API Contract Drift**
   - **Risk**: OpenAPI schemas and generated clients drift, causing type errors and integration failures
   - **Mitigation**: CI validation, automated client generation, contract freeze points, versioning policy
   - **Validation**: Contract drift detection in CI, automated schema validation, breaking changes detection

## Success Metrics

### Phase 0 Success Criteria (Day 2)
- ✅ Infrastructure operational
- ✅ CI/CD pipeline functional
- ✅ Authentication/authorization working
- ✅ Observability configured

### Phase 1 Success Criteria (Day 5)
- ✅ References & Research Engine operational (all 7 phases complete per `specs/003-references-research-engine/plan_003_references_research_engine.md`):
  - ✅ 95% search accuracy, <2s response time
  - ✅ Fully-automated research loop operational (≥95% priority topics approved with trust ≥85, 0 unresolved high-priority questions, 100% pinpoint verification, ≥99% simulation pass rate)
  - ✅ Canonical calculation list generated (`Research/canonical_calculations.yaml`)
- ✅ LLM Orchestrator basic functionality for research support
- ✅ All logic extracted from MVP research documents
- ✅ All relational database schemas created and migrated
- ✅ Core reference data populated
- ✅ Schema dress rehearsal complete: four golden calculations (PAYG tax + offsets, CGT discount event, super contributions + Div 293, negative gearing mortgage interest) execute end-to-end using real DB + canonical schemas with zero unresolved schema-friction items
- ✅ OpenAPI contracts generated for all modules in `specs/001-master-spec/contracts/`
- ✅ API client SDK generation pipeline operational
- ✅ Shared TypeScript API client packages generated and pinned to OpenAPI schemas
- ✅ CI validation configured for contract drift detection

### Phase 2A Success Criteria (Day 7)
- ✅ High-leverage document set populated in `/Research` (ATO tax essentials, super contributions & Div 293, CGT, ASIC RGs)
- ✅ Documents processed and stored in References & Research Engine
- ✅ Real findings (rules, calculations, strategies) extracted and stored in database
- ✅ Sample calculations manually verified against primary sources (PAYG, CGT discount, super caps)

### Phase 2B Success Criteria (Day 7.5)
- ✅ `Research/canonical_calculations.yaml` populated with real findings
- ✅ Each calculation has completeness/trust scores
- ✅ "Ready for Compute" status tracked for each calculation (≥85% completeness, ≥85 trust score, at least one golden example)
- ✅ Incomplete calculations flagged with refinement requests

### Phase 2C Success Criteria (Day 8 morning)
- ✅ Golden examples set created from ATO/ASIC worked examples (PAYG marginal tax + offsets, CGT discount event, super contributions + Div 293, negative gearing mortgage interest)
- ✅ Tests validate extracted logic against official examples (100% match for golden examples)
- ✅ Tests validate research integrity (no orphaned rules, complete provenance)
- ✅ Research drift detection tests operational

### Phase 2D Success Criteria (Day 8)
- ✅ Compute Engine operational: 100% deterministic reproducibility, 95% calculations <2s (see module plan)
- ✅ PostgreSQL schema created and populated with all data structures
- ✅ Ruleset snapshots created in PostgreSQL
- ✅ LLM Orchestrator can convert natural language to structured calculation requests
- ✅ Calculations validated against golden examples (100% match for golden examples)

### Phase 3 Success Criteria (Day 10)
- ✅ Advice Engine operational: 95% compliance issue detection accuracy, <3s response time (see module plan)
- ✅ LLM Orchestrator supports Advice Engine workflows: 90% intent detection accuracy, <2s response time (see module plan)

### Phase 4 Success Criteria (Day 12)
- ✅ Veris Finance operational: 5 seconds for strategy comparison, 30 minutes for SOA generation (see module plan)
- ✅ LLM Orchestrator updated to support Veris Finance
- ✅ 100% advice validated by Advice Engine

### Phase 5 Success Criteria (Day 14)
- ✅ Frankie's Finance operational: 5 seconds for financial guidance, 90% user understanding (see module plan)
- ✅ LLM Orchestrator updated to support Frankie's Finance
- ✅ 100% advice validated by Advice Engine

## Next Steps

**Timeline**: 2-week compressed timeline with AI-assisted development

1. **Phase 0** (Days 1-2): Begin foundational infrastructure setup
2. **Phase 1** (Days 3-5): Research phase - Build References & Research Engine, extract logic, create schemas
3. **Phase 2** (Days 6-8): Build Compute Engine, create PostgreSQL data structures, progress LLM Orchestrator
4. **Phase 3** (Days 9-10): Build Advice Engine, progress LLM Orchestrator
5. **Phase 4** (Days 11-12): Build Veris Finance, update LLM Orchestrator
6. **Phase 5** (Days 13-14): Build Frankie's Finance, update LLM Orchestrator

**Parallel Development**: Modules can be developed in parallel by Cursor AI agents where dependencies allow.

---

**Plan Status**: Draft  
**Last Updated**: 2025-01-27  
**Next Review**: After Phase 0 completion

