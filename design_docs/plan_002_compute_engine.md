# Compute Engine Implementation Plan

**Branch**: `002-compute-engine` | **Date**: 2025-01-27 | **Spec**: `specs/002-compute-engine/spec_002_compute_engine.md`  
**Status**: ✅ **Phase 0 Complete**

## Summary

Compute Engine is the core calculation engine that performs deterministic financial computations and projections. It executes rulesets, scenarios, and simulations while maintaining full provenance and reproducibility.

**Architectural Boundary** (Constitution Principle XII, FR-004A): Compute Engine is the **single source of truth** for all deterministic financial logic, including tax formulas, caps, thresholds, eligibility tests, and projections. It MUST NOT perform judgement, advice, or free-text reasoning, and MUST NOT store or serve knowledge objects (References, Rules, Assumptions, Advice Guidance, Strategies). All numeric calculations MUST be performed by Compute Engine; other modules MUST NOT perform calculations or override Compute Engine outputs.

**Technical Approach**: Python-based microservice using FastAPI + SQLAlchemy 2.0 + Pydantic v2, PostgreSQL-only storage (governance and execution) with relational edge table + JSONB + bitemporal fields + closure table/materialized view, deterministic calculation engine with fixed-point Decimal arithmetic, and full provenance chain building via closure table/materialized view (<10ms response time).

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**:
- **API Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (full control, async support, type safety)
- **Validation**: Pydantic v2 (request/response validation, serialization)
- **Database**: PostgreSQL 15+ with:
  - Relational edge table (src_id, dst_id, relation_type) for provenance relationships
  - JSONB columns for metadata (flexible, queryable)
  - Bitemporal fields (`valid_from`, `valid_to`) for time-travel queries
  - Partial indexes on current data (`WHERE valid_to IS NULL`) for performance
  - Closure table or materialized view for instant `/explain` chains (<10ms)
  - Row-Level Security (RLS) policies for tenant isolation (see CL-031 and FR-030 in master spec for security guarantee)
- **Deployment**: Render (Sydney) - AU data residency, 15-min timeout, zero ops
- **Numeric Precision**: Python `decimal.Decimal` for all monetary calculations (binary `float` FORBIDDEN)
- **Cache**: Redis (Render) for hot facts (<1ms lookup times)
- **Background Jobs**: RQ (Redis Queue) worker for long-running calculations (returns 202 + job ID)
- **Error Tracking**: Sentry (free tier) for error monitoring
- **Testing**: pytest, Hypothesis (property-based testing)

**Storage**:
- **PostgreSQL Database (Render Sydney)**: All data storage including:
  - Rule definitions, effective windows, precedence, review workflow, assumptions snapshots, change logs
  - Active rulesets, domain entities, scenarios, Facts
  - Provenance links via relational edge table (src_id, dst_id, relation_type) + JSONB metadata
  - Closure table or materialized view for instant `/explain` chains (<10ms)
  - Bitemporal fields (`valid_from`, `valid_to`) on all temporal entities
  - Partial indexes on current data for performance optimization
  - Row-Level Security (RLS) policies for tenant isolation (see CL-031 and FR-030 in master spec for security guarantee)
- **Redis Cache (Render)**: Hot facts and frequently accessed data (<1ms lookup times)
- **Background Jobs**: RQ (Redis Queue) for long-running calculations and batch operations

## API Endpoints

### Calculation APIs

- **`POST /run`**: Execute single calculation
  - **Request**: `{ client_data, scenario_parameters, ruleset_id, as_of_date, idempotency_key? }`
  - **Response**: `{ facts: [...], provenance: {...} }`
  - **Idempotent**: Yes (via idempotency_key)
  
- **`POST /run-batch`**: Execute batch calculations
  - **Request**: `{ requests: [...], ruleset_id, as_of_date }`
  - **Response**: `{ results: [...], errors: [...] }` (partial-result semantics) OR `{ job_id, status: "queued" }` (202 for long-running jobs)
  - **Idempotent**: Per-request idempotency keys
  - **Async Support**: Long-running batch jobs return 202 + job ID; status via `GET /jobs/{job_id}`

### Facts Retrieval APIs

- **`GET /facts`**: Retrieve computed Facts
  - **Query Parameters**: `scenario=...&as_of=...&page=...&limit=...`
  - **Response**: Paginated Facts with metadata
  - **Pagination**: Cursor-based or offset-based (default 100, max 1000)

- **`GET /explain/{fact_id}`**: Get provenance chain for a Fact
  - **Response**: `{ fact, rules: [...], references: [...], assumptions: [...], provenance_chain }`
  - **Format**: Human-readable trace (Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions)
  - **Performance**: <50ms response time for 95% of requests at scale (10,000 concurrent users, 1 million Facts) via closure table/materialized view, read replicas, and connection pooling

- **`GET /explain/batch`**: Get provenance chains for multiple Facts (batch explain)
  - **Query Parameters**: `fact_ids=...&scenario_id=...`
  - **Response**: Array of explain chains `[{ fact_id, fact, rules: [...], references: [...], assumptions: [...], provenance_chain }, ...]`
  - **Performance**: <50ms for up to 100 Facts per forecast scenario at scale

### Rules Intelligence APIs

- **`GET /rulesets`**: List all published rulesets
  - **Response**: `{ rulesets: [{ id, publication_date, effective_date_range, status, rule_count }] }`
  - **MVP**: Basic listing, future: filtering and search

- **`GET /rules`**: Query rules active at a date
  - **Query Parameters**: `active=true&as_of=...&precedence=...&type=...`
  - **Response**: Rule metadata (identifiers, effective dates, precedence, references, applicability conditions)
  - **MVP**: Basic query, future: advanced filtering

### Background Job APIs

- **`GET /jobs/{job_id}`**: Get status of background job
  - **Response**: `{ job_id, status: "queued"|"running"|"completed"|"failed", progress?: number, result?: {...}, error?: {...} }`
  - **Status**: Polling endpoint for async job status
  - **Polling Strategy**: Clients should poll with exponential backoff (e.g., 1s, 2s, 4s, 8s intervals) up to maximum wait time
  - **Result Retention**: Job results retained for configurable period (minimum 7 days) for retrieval

## Module Dependencies

### Depends On

- **References & Research Engine** (`003-references-research-engine`): 
  - Rule-to-reference lookups for provenance chains
  - **Integration**: `GET /references/{id}` and `GET /pinpoints/{reference_id}`
  - **Canonical Calculation List**: **CRITICAL DEPENDENCY** - Must receive complete canonical calculation list (`Research/canonical_calculations.yaml`) from References & Research Engine Phase 4 before Compute Engine Phase 1 can begin implementation. If canonical list is incomplete or insufficient, Compute Engine MUST request further research and block implementation of incomplete calculations until research provides required details.
  
- **PostgreSQL Database (Render Sydney)**: All data storage (governance and execution) including rule definitions, versions, precedence, Facts, provenance links

### Used By

- **LLM Orchestrator**: Receives structured calculation requests (transformed from natural language)
- **Advice Engine**: Retrieves Fact data for compliance evaluation
- **Frankie's Finance**: Executes consumer calculations and retrieves explanations
- **Veris Finance**: Executes adviser scenario modelling and comparative analysis
- **Partner API**: Direct calculation requests matching internal capabilities

## Integration Points

### Module-to-Module Integration

- **LLM Orchestrator → Compute Engine**: 
  - Transformed structured calculation requests via `POST /run` and `POST /run-batch`
  - Never receives natural language directly
  - Never receives direct financial outcomes from LLM

- **Advice Engine → Compute Engine**: 
  - Fact data retrieval via `GET /facts` for compliance evaluation

- **Frankie's Finance → Compute Engine**: 
  - Consumer calculation requests via `POST /run`
  - Results via `GET /facts`
  - Explanations via `GET /explain/{fact_id}`

- **Veris Finance → Compute Engine**: 
  - Adviser calculation requests via `POST /run` and `POST /run-batch`
  - Scenario comparisons via `GET /facts`
  - Explanations via `GET /explain/{fact_id}`

- **Compute Engine → References & Research Engine**: 
  - Rule-to-reference lookups via `GET /references/{id}` and `GET /pinpoints/{reference_id}`
  - Used for building provenance chains

- **Partner API → Compute Engine**: 
  - Direct calculation requests via `POST /run`, `GET /facts`, `GET /explain/{fact_id}`

### External Integration

- **Rule Authoring System → Compute Engine**: 
  - Ruleset publication creates snapshot in PostgreSQL
  - Makes rules available for computation

- **Storage Systems → Compute Engine**: 
  - PostgreSQL (Render Sydney) provides all data storage (governance and execution) including rule definitions, versions, precedence, Facts, provenance links (via relational edge table + JSONB), and explainability (via closure table/materialized view)

## Technical Implementation Details

### Calculation Execution

- **Determinism**: Same inputs + same `ruleset_id` + same `as_of` date = identical outputs
- **Numeric Precision**: Fixed-point `decimal.Decimal` or integer cents (binary `float` FORBIDDEN)
- **Unit Validation**: Explicit units and dimensional checks (%, basis points, dollars, years)
- **Rounding**: Policy per field in rule definitions (ATO rounding rules, bankers rounding)
- **Precision Guard**: Protection against precision loss for long horizons (50-year projections)

### Background Jobs and Async Processing

- **Queue System**: RQ (Redis Queue) workers using Redis on Render for background job processing
- **Jobs that run async**:
  - **Long-running batch calculations**: `POST /run-batch` requests exceeding time threshold (default: 15 seconds) return `202 Accepted` with `job_id` instead of synchronous results
  - **Large-scale simulations**: Multi-scenario projections or long-horizon calculations (e.g., 50-year retirement projections) that exceed synchronous timeout limits
- **Job idempotency**:
  - **Job key format**: `hash(inputs_hash + ruleset_id + as_of_date + scenario_id + tenant_id)` for calculation jobs
  - **Idempotency guarantees**: Identical requests (same `inputs_hash`, `ruleset_id`, `as_of`, `scenario_id`, `idempotency_key`) return existing `job_id` or cached results if job already completed
- **Retry/backoff policy**:
  - **Transient failures**: Exponential backoff with initial delay 1s, max delay 30s, max retries 3
  - **Dead-letter queue**: Failed jobs after max retries moved to dead-letter queue with replay capability, error analysis, and operator notifications
  - **Job timeout**: Configurable timeout (default: 15 minutes for Render deployment limits). Jobs exceeding timeout marked as failed and moved to dead-letter queue
  - **Idempotency enforcement**: All retries use the same job idempotency key, ensuring exactly-once semantics for successful jobs and preventing duplicate calculations
- **Client interaction**:
  - **Polling endpoint**: `GET /jobs/{job_id}` returns job status (`queued`, `running`, `completed`, `failed`), progress percentage (if available), result data (when completed), or error details (when failed)
  - **Polling strategy**: Clients should poll with exponential backoff (e.g., 1s, 2s, 4s, 8s intervals) up to maximum wait time
  - **Result retention**: Job results retained for configurable period (minimum 7 days) for retrieval
  - **Webhook support**: Not in MVP scope; polling is the primary mechanism
- **Reference**: `Design_docs/final_design_questions.md` Section 6, `specs/002-compute-engine/spec.md` FR-045, FR-046, FR-029

### Storage Architecture

- **Publish → Validate → Activate Workflow**: 
  - Rules authored as versioned artifacts (Markdown/YAML)
  - Published as `ruleset-YYYYMMDD` snapshots in PostgreSQL
  - Validated for integrity and consistency
  - Then activated and available for computation

- **Entity ID Generation**:
  - **Format**: Two-letter prefix + ULID/hash (e.g., `RU-01HFSZ2R2Y1G2M5D8C9QWJ7K4T`)
  - **Prefixes**: `RU-` (Rule), `RE-` (Reference), `AS-` (Assumption), `AG-` (Advice Guidance), `ST-` (Client Outcome Strategy), `SC-` (Scenario), `EV-` (Client Event), `IN-` (Input), `FA-` (Fact), `FN-` (Finding), `RQ-` (Research Question), `VD-` (Verdict), `RS-` (Ruleset Snapshot), `PL-` (Provenance Link)
  - **Collision Handling**: ULID/hash ensures global uniqueness across tenants/modules. ULID's inherent uniqueness properties (128-bit entropy, timestamp-based ordering) provide collision-free IDs without explicit collision detection logic. IDs are immutable and never reused or reassigned.
  - **Implementation**: Use Python `ulid` library or equivalent for ULID generation. Prefix validation ensures correct entity type association.
  - **Reference**: `specs/001-master-spec/canonical_data_model.md` (Canonical ID Prefix Reference section), `.specify/memory/constitution.md` (Canonical ID Prefix Reference section)

- **Provenance Storage Design**:
  - **Relational Edge Table**: `provenance_edges` table stores relationships as rows (edges) with:
    - `src_id` (source entity ID, e.g., `FA-...`)
    - `dst_id` (destination entity ID, e.g., `RU-...`)
    - `relation_type` (relationship type: `PRODUCED_BY`, `JUSTIFIED_BY`, `CITES`, `DERIVED_FROM`, etc.)
    - `created_at` (timestamp for audit trail)
    - `tenant_id` (for tenant isolation, NULL for global entities)
  - **JSONB Metadata**: Flexible metadata stored in JSONB columns on entity tables for queryable, extensible attributes (e.g., rule parameters, fact rounding details, reference pinpoints). Relationships are stored as rows; attributes are stored as JSONB.
  - **Architecture Decision**: Relationships stored as relational rows (edges) enable efficient graph traversal, referential integrity, and query optimization. JSONB used only for entity attributes, not relationships.
  - **Reference**: `Design_docs/final_design_questions.md` Section 4

- **Bitemporal Fields & Time-Travel**:
  - **Fields**: All temporal entities have `valid_from` (timestamp) and `valid_to` (timestamp, NULL for current) fields
  - **Default Filter for Current Rows**: `WHERE valid_to IS NULL` - this is the standard filter for querying "current" or "active" entities
  - **Time-Travel Queries**: Use `as_of` date parameter. System selects rows where `as_of` falls within `valid_from` and `valid_to` (or `valid_to IS NULL`). Query pattern: `WHERE valid_from <= as_of AND (valid_to IS NULL OR valid_to > as_of)`
  - **Partial Indexes**: Indexes on current data only (`WHERE valid_to IS NULL`) for performance optimization. These indexes dramatically improve query performance for common "current state" queries.
  - **Entities with Bitemporal Fields**: Rules, References, Assumptions, Advice Guidance, Client Outcome Strategies, Scenarios, Facts, Provenance Links
  - **Reference**: `Design_docs/final_design_questions.md` Section 4, `specs/001-master-spec/spec.md` CL-011, CL-012

- **Closure Table/Materialized View**: Pre-computed provenance chains for instant `/explain` queries (<50ms at scale with 10,000 concurrent users, 1 million Facts)
- **Row-Level Security (RLS)**: Database-level policies enforce tenant isolation on all tables
- **Read Replicas**: PostgreSQL read replicas for explain query distribution and read scaling
- **Connection Pooling**: PgBouncer or equivalent for efficient connection management at scale (see CL-031 and FR-030 in master spec for security guarantee that User A can NEVER see User B's data under ANY circumstances)

- **No Direct Database Edits**: All rule changes MUST originate from versioned artifacts
- **Consistency Checks**: After ruleset publication, validate counts, checksums, referential integrity

### Performance & Scalability

**Latency Targets (p95):**
- **`/run` endpoint**: 2 seconds for standard calculations (single tax calculation, super contribution). Reference: `specs/002-compute-engine/spec.md` SC-001, `Design_docs/final_design_questions.md` Section 5.
- **`/explain/{fact_id}` endpoint**: 50ms at scale (10,000 concurrent users, 1 million Facts). Typical performance is <10ms via closure table/materialized view. Reference: `specs/002-compute-engine/spec.md` SC-004A, FR-020D, FR-020E, `Design_docs/final_design_questions.md` Section 5.
- **Overall API response**: 3 seconds from initial query to displayed response (excluding complex multi-scenario calculations). Reference: `specs/001-master-spec/spec.md` SC-001, `Design_docs/final_design_questions.md` Section 5.

**Caching Strategy:**
- **What gets cached:**
  - **Ruleset snapshots**: Frequently accessed ruleset snapshots cached in memory/Redis. Reference: `specs/002-compute-engine/spec.md` FR-041, `Design_docs/final_design_questions.md` Section 5.
  - **Hot Facts**: Frequently accessed Facts cached in Redis with <1ms lookup times. Reference: `specs/001-master-spec/plan.md` (Cache section), `Design_docs/final_design_questions.md` Section 5.
  - **Explain chains**: Pre-computed via closure table/materialized view (not traditional cache, but materialized for performance). Reference: `specs/002-compute-engine/spec.md` FR-020E, `Design_docs/final_design_questions.md` Section 5.
  - **Reference data**: Frequently accessed reference metadata cached where appropriate. Reference: `specs/002-compute-engine/spec.md` FR-041, `Design_docs/final_design_questions.md` Section 5.
- **Cache invalidation:**
  - **Ruleset publication**: Cache invalidated when new ruleset is published (keyed by `ruleset_id`). Reference: `specs/002-compute-engine/spec.md` FR-041A, `Design_docs/final_design_questions.md` Section 5.
  - **Cache keys**: Format is `inputs_hash + ruleset_id + as_of_date` with configurable TTL. Reference: `specs/002-compute-engine/spec.md` FR-041A, `Design_docs/final_design_questions.md` Section 5.
  - **Materialized view refresh**: CONCURRENT refresh strategy to avoid blocking queries during updates. Reference: `specs/002-compute-engine/spec.md` FR-041D, `Design_docs/final_design_questions.md` Section 5.

**Depth Limits & Runaway Query Prevention:**
- **Max recursion depth**: 15 levels maximum for provenance chain traversal (Fact → Rule → Reference → Assumption → Input). Typical chains are 3-5 levels. Reference: `Design_docs/final_design_questions.md` Section 5.
- **Query timeout**: Default 30 seconds, configurable per operation type. Reference: `specs/002-compute-engine/spec.md` FR-043, `Design_docs/final_design_questions.md` Section 5.
- **Depth limit enforcement**: Recursive CTEs include `MAX_RECURSION` clause or equivalent depth checking in application layer. Reference: `Design_docs/final_design_questions.md` Section 5.
- **Circuit breakers**: Implemented around database queries and external service lookups to fail fast. Reference: `specs/002-compute-engine/spec.md` FR-044, `Design_docs/final_design_questions.md` Section 5.
- **Memory ceilings**: Back-pressure mechanisms prevent memory exhaustion during large batch operations. Reference: `specs/002-compute-engine/spec.md` FR-041B, `Design_docs/final_design_questions.md` Section 5.
- **Profiling budget**: Per-endpoint performance monitoring and alerting when thresholds exceeded. Reference: `specs/002-compute-engine/spec.md` FR-041C, `Design_docs/final_design_questions.md` Section 5.

**Performance Optimization:**
- **Materialized View Refresh**: CONCURRENT refresh strategy to avoid blocking queries, incremental updates where possible, scheduled refresh during low-traffic periods
- **Read Replicas**: Distribute explain queries across read replicas to scale read capacity and maintain performance under high concurrent load
- **Connection Pooling**: PgBouncer or equivalent connection pooler to efficiently manage database connections and prevent connection exhaustion
- **Explain Performance**: Closure table/materialized view pre-computation, Redis caching of hot explain chains, query optimization with partial indexes
- **Concurrency**: Support 10,000 concurrent users with tenant isolation and sub-50ms explain response times

### Error Handling

- **Error Taxonomy**: 
  - 4xx: Validation errors (missing parameters, invalid types)
  - 409: Conflicts (concurrent scenario updates)
  - 5xx: Compute failures (rule execution errors)
- **Timeouts**: Default 30 seconds, configurable per operation type
- **Circuit Breakers**: Around external dependencies (PostgreSQL, Redis, References & Research Engine)
- **Retry Policies**: Exponential backoff (initial 1s, max 30s, max 3 retries)

### Consistency Guarantees

- **Strong Consistency**: `/run` and `/run-batch` (facts immediately visible)
- **Eventual Consistency**: `/facts` queries (may read from read replicas with <1s lag)

## Implementation Phases

### Phase 1: Schema Dress Rehearsal & Rule Execution (Weeks 1-2)

**Prerequisites**:
- **Canonical Calculation List**: Must receive canonical calculation list from References & Research Engine (`Research/canonical_calculations.yaml`) with complete specifications for all required calculations. If canonical list is incomplete or insufficient for implementing required calculations, **further research MUST be conducted** before proceeding with implementation.
- **Research Completeness Check**: Before starting implementation, verify that canonical calculation list contains sufficient information for each calculation type:
  - Input parameters and data types are clearly defined
  - Formulas or algorithms are specified or extractable
  - Edge cases and exceptions are documented
  - Regulatory sources are cited with pinpoints
  - Rounding rules and precision requirements are specified
- **Insufficient Information Handling**: If any calculation in the canonical list lacks sufficient information to implement:
  - **Flag calculation as "INSUFFICIENT_INFO"** in implementation tracking
  - **Generate structured refinement request** via References & Research Engine API (`POST /research/refine`) with:
    - `calculation_id`: The calculation identifier (CAL-*)
    - `missing_fields`: Array of specific missing required fields (e.g., ["input_parameters", "formula", "rounding_rules"])
    - `specific_questions`: Array of specific questions about missing information
    - `priority`: Priority level (`high` for blocking calculations, `normal` for others)
    - `iteration_number`: Track which iteration this refinement request is for
  - **Block implementation** of incomplete calculations until research provides required details
  - **Document gaps** in `backend/compute-engine/docs/research_gaps.md` for tracking
  - **Track refinement request status** and resume implementation when research completes
  - **Reference**: Dependencies on References & Research Engine canonical calculation list output and refinement API

**Tasks**:
1. **Schema Dress Rehearsal (Pre-Freeze A)** - **CRITICAL**: Must be completed before Freeze A is declared
   - Implement four full golden calculations using live PostgreSQL + SQLAlchemy models:
     - PAYG marginal tax 2024–25 + offsets
     - CGT discount event
     - Super contributions + Div 293
     - Negative gearing mortgage interest
   - Log every schema friction point in `backend/compute-engine/src/schema_rehearsal/friction_log.md`:
     - Missing relations between canonical types
     - Awkward join patterns
     - Missing provenance roles
     - Excessive JSONB gymnastics (indicating missing relational structure)
   - **Schema Friction Remediation**: Update `specs/001-master-spec/canonical_data_model.md`, SQL migrations in `infrastructure/database/postgres/migrations/`, OpenAPI/Pydantic schemas in `specs/001-master-spec/schemas/` based on findings
   - **Provenance Chain Verification**: Verify full provenance chains (Fact → Rule/Strategy → Reference → Assumption) are stored and retrievable for all dress-rehearsal calculations
   - **Zero Friction Requirement**: Zero open schema-friction items required before Freeze A
   - **Schema Feedback**: Emit structured schema-feedback requests via `POST /research/refine` API when schema issues block implementation (FR-SCHEMA-01)
   - Reference: `specs/001-master-spec/master_plan.md` (Phase 1 – Schema Dress Rehearsal & Feedback Loop), `specs/001-master-spec/master_tasks.md` (T041.5, T041.6, T041.65)

2. **Entity ID Generation System**
   - Implement entity ID generation utility using Python `ulid` library
   - Implement prefix validation (RU-, RE-, AS-, AG-, ST-, SC-, EV-, IN-, FA-, FN-, RQ-, VD-, RS-, PL-)
   - Implement ID format validation and parsing
   - Add database unique constraints on entity ID columns for defense-in-depth collision prevention
   - Reference: `specs/001-master-spec/canonical_data_model.md` (Canonical ID Prefix Reference section), `.specify/memory/constitution.md` (Canonical ID Prefix Reference section)

2. **Fact Data Model & Storage**
   - Design Fact data model with bitemporal fields (`valid_from`, `valid_to`)
   - Implement Fact storage with full provenance using relational edge table
   - Implement immutable Fact semantics
   - Implement default filter for current rows (`WHERE valid_to IS NULL`)
   - Create partial indexes on current data (`WHERE valid_to IS NULL`) for performance
   - Reference: `Design_docs/final_design_questions.md` Section 4

3. **Provenance Storage Implementation**
   - Implement `provenance_edges` table schema (src_id, dst_id, relation_type, created_at, tenant_id)
   - Implement JSONB metadata columns on entity tables for attributes
   - Implement provenance link creation and querying utilities
   - Ensure relationships stored as rows (edges), attributes stored as JSONB
   - Reference: `Design_docs/final_design_questions.md` Section 4

4. **Bitemporal Fields & Time-Travel**
   - Implement bitemporal fields (`valid_from`, `valid_to`) on all temporal entities
   - Implement time-travel query utilities with `as_of` date support
   - Implement query pattern: `WHERE valid_from <= as_of AND (valid_to IS NULL OR valid_to > as_of)`
   - Create partial indexes on current data for performance optimization
   - Reference: `Design_docs/final_design_questions.md` Section 4, `specs/001-master-spec/spec.md` CL-011, CL-012

5. **Rule Resolution**
   - Implement rule resolution (precedence, effective dates)
   - Implement temporal logic based on `as_of` date using bitemporal fields
   - Implement rule applicability checking with time-travel support

6. **Calculation Execution Engine**
   - **Load canonical calculation list** from References & Research Engine (`Research/canonical_calculations.yaml`)
   - **Validate calculation completeness**: Verify all calculations have sufficient information for implementation using Compute Engine requirements context checklist
   - **Check completeness scores**: Review completeness_score (0-100%) for each calculation from canonical list
   - **Flag incomplete calculations**: If any calculation lacks required information (completeness_score < 100% or missing required fields), mark as "INSUFFICIENT_INFO" and generate refinement request
   - **Generate refinement requests**: For incomplete calculations, create structured refinement requests via `POST /research/refine` API with:
     - Specific missing fields identified from requirements context checklist
     - Specific questions about missing information
     - Priority level based on implementation order
   - **Track refinement requests**: Monitor refinement request status and wait for completion before proceeding
   - **Resume after refinement**: When refinement requests are completed, re-validate completeness and proceed with implementation
   - **Generate calculation function stubs** from canonical list specifications (one Python function per calculation with CAL-* identifier) - ONLY for complete calculations (completeness_score = 100%)
   - Implement deterministic calculation logic based on canonical list specifications
   - Implement calculation expression/function execution using formulas/algorithms from canonical list
   - Implement numeric tolerance and rounding standards per canonical list specifications
   - **Generate data schemas** from canonical list input/output specifications
   - **Create calculation scripts** for each calculation type based on canonical list
   - **Reference**: Canonical calculation list from References & Research Engine Phase 4, Compute Engine requirements context, Research refinement API

7. **Numerical Fidelity**
   - Implement fixed-point Decimal (Python `decimal.Decimal`) for all monetary values
   - Enforce explicit units and dimensional checks (% vs bps vs dollars vs years)
   - Implement rounding policy per field (ATO rules, bankers rounding vs away-from-zero)
   - Specify when rounding occurs (step vs end) in rule definitions
   - Guard against precision loss for long horizons (50+ years) and large totals

**Deliverables**:
- **Schema Dress Rehearsal complete**: Four golden calculations (PAYG tax + offsets, CGT discount event, super contributions + Div 293, negative gearing mortgage interest) implemented using live schemas with zero unresolved schema-friction items
- Schema friction log created with all identified issues documented
- Schema friction remediation complete (canonical_data_model.md, SQL migrations, OpenAPI/Pydantic schemas updated)
- Full provenance chains verified and retrievable for all dress-rehearsal calculations
- Entity ID generation system implemented with ULID support
- Fact data model implemented with bitemporal fields
- Provenance storage implemented (relational edge table + JSONB)
- Bitemporal time-travel queries functional
- Rule resolution working with temporal logic
- Canonical calculation list loaded and validated for completeness using Compute Engine requirements context
- Completeness scores reviewed for all calculations
- Refinement requests generated for incomplete calculations via `POST /research/refine` API (including schema feedback when needed)
- Refinement request tracking system operational
- Calculation function stubs generated from canonical list (all complete calculations with completeness_score = 100%)
- Incomplete calculations flagged, documented in `research_gaps.md`, and refinement requests submitted
- Deterministic calculation execution functional (for complete calculations only)
- Fixed-point Decimal arithmetic enforced
- Data schemas generated from canonical list specifications

### Phase 2: Scenario Management (Week 3)

**Tasks**:
1. **Scenario Creation**
   - Implement scenario creation and tagging
   - Ensure scenarios never overwrite base reality
   - Implement scenario metadata management

2. **Scenario Comparison**
   - Implement scenario comparison queries
   - Implement side-by-side Fact retrieval
   - Implement sensitivity analysis support

**Deliverables**:
- Scenario creation and management working
- Scenario comparison queries functional

### Phase 3: Provenance and Explainability (Week 4)

**Tasks**:
1. **Provenance Chain Building**
   - Implement provenance chain building (Fact → Rule → Reference → Assumptions)
   - Integrate with References & Research Engine for reference lookups
   - Implement time-travel queries (`as_of` date support)

2. **Explanation Endpoint**
   - Implement `/explain/{fact_id}` endpoint
   - Implement `/explain/batch` endpoint for batch explain operations
   - Implement human-readable trace generation
   - Implement provenance export for compliance packs
   - Implement materialized view with CONCURRENT refresh strategy
   - Configure read replicas for explain query distribution
   - Set up connection pooling (PgBouncer) for efficient connection management
   - Implement Redis caching for hot explain chains

**Deliverables**:
- Provenance chains complete
- `/explain/{fact_id}` endpoint functional (<50ms at scale)
- `/explain/batch` endpoint functional (<50ms for up to 100 Facts)
- Time-travel queries working
- Materialized view refresh strategy implemented
- Read replicas configured
- Connection pooling operational

### Phase 4: PostgreSQL Storage Integration (Week 5)

**Tasks**:
1. **Publish → Validate → Activate Workflow**
   - Implement ruleset snapshot creation in PostgreSQL
   - Implement ruleset validation (integrity, consistency, referential checks)
   - Forbid direct database edits outside of versioned artifacts (enforce via code review)

2. **Consistency Checks**
   - Implement consistency checks after ruleset publication
   - Validate rule count matches in ruleset snapshot
   - Validate rule content hash matches
   - Validate all referenced rules exist in ruleset
   - Validate provenance link integrity (JSONB relationships)

**Deliverables**:
- Publish → Validate → Activate workflow implemented
- Ruleset validation checks functional

### Phase 5: APIs and Integration (Week 6)

**Tasks**:
1. **Calculation APIs**
   - Implement `POST /api/v1/run` (calculation API)
   - Implement `POST /api/v1/run-batch` (batch calculations)
   - Implement idempotency support with job key format: `hash(inputs_hash + ruleset_id + as_of_date + scenario_id + tenant_id)`
   - Implement async job handling: return `202 Accepted` with `job_id` for requests exceeding time threshold (default: 15 seconds)
   - Implement API versioning (URL path versioning: `/api/v1/...`)

2. **Facts Retrieval APIs**
   - Implement `GET /api/v1/facts` (Facts retrieval)
   - Implement pagination (cursor-based or offset-based)

3. **Rules Intelligence APIs**
   - Implement `GET /api/v1/rulesets` (rulesets listing)
   - Implement `GET /api/v1/rules` (rules query)

4. **Background Job Infrastructure**
   - Set up RQ (Redis Queue) workers on Render
   - Configure Redis connection for job queue
   - Implement job queue management (enqueue, dequeue, status tracking)
   - Set up job monitoring and health checks for RQ workers

5. **Background Job APIs**
   - Implement `GET /api/v1/jobs/{job_id}` (job status polling endpoint)
   - Implement job status tracking (queued, running, completed, failed)
   - Implement progress reporting (percentage when available)
   - Implement result storage and retrieval (minimum 7 days retention)
   - Implement job result caching for idempotent requests

5. **OpenAPI Schema Generation**
   - Generate OpenAPI 3.0 schema for all Compute Engine endpoints
   - Output to `specs/001-master-spec/contracts/compute-engine.openapi.yaml`
   - Include all request/response schemas, error responses, and examples
   - Include background job endpoints and job status response schemas
   - Validate schema against OpenAPI 3.0 specification

6. **API Versioning Implementation**
   - Implement URL path versioning (`/api/v1/...`)
   - Add deprecation header support for deprecated versions
   - Document versioning strategy per `API_VERSIONING_POLICY.md`

**Deliverables**:
- All APIs functional with versioning
- Idempotency support working with job key format
- Async job handling implemented (202 responses for long-running operations)
- Background job status endpoint functional
- OpenAPI schema generated and validated (including job endpoints)
- API versioning implemented

### Phase 6: Error Handling and Resilience (Week 7)

**Tasks**:
1. **Error Handling**
   - Implement structured error responses with remediation guidance
   - Implement timeouts (default 30s) around database and external service lookups
   - Implement circuit breakers around external dependencies
   - Implement retry policies with exponential backoff (1s initial, 30s max, 3 retries) for transient failures
   - Implement dead-letter queue for failed calculation jobs with replay capability, error analysis, and operator notifications
   - Implement job timeout handling (default: 15 minutes for Render limits) - jobs exceeding timeout marked as failed
   - Implement idempotency enforcement: all retries use same job idempotency key for exactly-once semantics

2. **Validation and Reconciliation**
   - Implement cross-checks (sum of components = totals, cash conservation)
   - Implement tax reconciliation (taxable income → tax → offsets → net tax)
   - Implement super caps reconciliation (concessional + non-concessional = total, TBC/TSB roll-forward)
   - Implement amortisation reconciliation (opening + interest - repayments = closing)
   - Implement rounding drift detection (tolerance: 0.01 cents per period)

3. **Concurrency and Consistency**
   - Implement optimistic concurrency control (version numbers) or pessimistic locking for scenario updates
   - Specify isolation levels (read-committed for fact writes, snapshot for time-travel)
   - Document consistency guarantees per endpoint (strong for `/run`, eventual for `/facts`)

**Deliverables**:
- Error handling and resilience patterns implemented
- Reconciliation checks implemented
- Concurrency control implemented

### Phase 7: Calculation Function Explanation Repository (Week 8)

**Prerequisites**:
- **Canonical Calculation List**: Must receive canonical calculation list (`Research/canonical_calculations.yaml`) from References & Research Engine Phase 4. The canonical list serves as the authoritative source for calculation specifications (formulas, regulatory sources, edge cases, rounding rules) that explanations derive from.

**Tasks**:
1. **Repository Structure**
   - Create `explanations/` directory structure with `index.yaml` and `functions/` subdirectory
   - Define explanation file schema (function ID, comprehensive explanation, implementation rationale, rule references, testing approach, creation date, version tracking, canonical source reference)
   - **Canonical List Integration**: Explanation schema MUST include `canonical_source: Research/canonical_calculations.yaml` and `canonical_calculation_id: CAL-*` fields to link explanations back to their source specifications
   - Create explanation repository documentation in `explanations/README.md` documenting relationship to canonical list

2. **Canonical List Bootstrap**
   - Load canonical calculation list from `Research/canonical_calculations.yaml`
   - **Auto-populate explanation templates** from canonical list data:
     - Formulas/algorithms from canonical list → "How the Calculation Works" section
     - Regulatory sources from canonical list → "Rule References" section
     - Edge cases from canonical list → "How the Calculation Works" section
     - Rounding rules from canonical list → "How the Calculation Works" section
   - Generate initial explanation file stubs for all calculations in canonical list
   - Link each explanation to its canonical source via `canonical_calculation_id` field

3. **Loader Implementation**
   - Implement explanation repository loader in `backend/compute-engine/src/explanations/loader.py`
   - Implement explanation index builder in `backend/compute-engine/src/explanations/index_builder.py` that can sync with canonical list updates
   - Implement explanation file validator to ensure all required fields are present and canonical references are valid
   - Create explanation template generator that auto-populates from canonical list data
   - Implement explanation lookup system that every Python calculation function must use
   - **Canonical Sync**: Implement mechanism to detect canonical list updates and flag explanations that may need updates

4. **Code Review Enforcement**
   - Enforce explanation reference requirement in code review (every calculation function must reference explanation repository)
   - Verify explanations reference valid canonical calculation IDs
   - Implement explanation version tracking and change history
   - Ensure explanations stay synchronized with canonical list when canonical list is updated

**Relationship to Canonical List**:
- **Canonical List** (Module 3): Research-derived specification of WHAT calculations should do (from regulations/research)
- **Explanations Repository** (Module 2): Implementation documentation of HOW calculations were implemented (derived from canonical list)
- Explanations MUST derive from canonical list and add implementation-specific details (rationale, testing approach, code references)
- When canonical list is updated, explanations should be flagged for review to ensure they remain synchronized

**Deliverables**:
- Calculation Function Explanation Repository operational
- Explanation repository loader and index builder implemented
- All calculation functions documented with comprehensive explanations
- Explanations linked to canonical calculation list via canonical_calculation_id references
- Canonical list bootstrap process functional (auto-populate explanations from canonical list)

### Phase 8: Testing & Validation (Ongoing)

**Tasks**:
1. **Test Implementation**
   - Unit tests for calculation logic
   - Property-based tests (Hypothesis) for edge cases
   - Metamorphic tests (scaling inputs scales outputs appropriately)
   - Snapshot tests for `/explain` chains
   - Integration tests with References & Research Engine
   - Tests for explanation repository loader and index builder
   - Tests to verify all calculation functions have corresponding explanation entries

2. **Minimum Validation Suite (CRITICAL - Required Before Shipping)**
   - **Golden Dataset Validation - ATO Examples**:
     - Collect at least 10 ATO tax calculation examples from published ATO materials
     - Validate taxable income calculations (salary, interest, dividends, other income)
     - Validate tax offsets and deductions (low income offset, medicare levy, etc.)
     - Validate CGT calculations (capital gains, discounts, exemptions)
     - Validate tax payable calculations (marginal rates, offsets, final tax)
     - All calculations must match ATO examples exactly (within rounding tolerance)
     - Document expected vs actual results for each example
   - **Golden Dataset Validation - ASIC Examples**:
     - Collect at least 5 ASIC compliance examples from regulatory guides
     - Validate best interests duty checks
     - Validate conflict detection logic
     - Validate advice documentation requirements
     - All compliance checks must match ASIC examples exactly
     - Document expected vs actual compliance outcomes for each example
   - **Deterministic Reproducibility Tests**:
     - Run 1000+ iterations of same calculation (same inputs + ruleset + date)
     - Verify 100% identical outputs across all iterations
     - Test across different execution times, servers, and environments
     - Document any non-deterministic behavior (must be zero)
   - **Veris Finance Test Forecasts**:
     - Each calculation must be tested via Veris Finance test forecasts
     - Test forecasts validate calculation accuracy and provenance chains
     - Test forecasts ensure compliance validation works correctly
     - Test forecasts document expected behavior for future reference

**Deliverables**:
- Test coverage > 85%
- Minimum validation suite complete:
  - ✅ At least 10 ATO tax examples validated
  - ✅ At least 5 ASIC compliance examples validated
  - ✅ 100% deterministic reproducibility verified (1000+ iterations)
  - ✅ All calculations validated via Veris Finance test forecasts
- **CRITICAL**: System MUST NOT ship without minimum validation suite complete

