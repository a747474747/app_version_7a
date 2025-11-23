# Advice Engine Implementation Plan

**Branch**: `004-advice-engine` | **Date**: 2025-01-27 | **Spec**: `specs/004-advice-engine/spec_004_advice_engine.md`  
**Status**: ✅ **Phase 0 Complete**

## Summary

Advice Engine enforces professional and regulatory standards through deterministic policy engine. Evaluates compliance obligations, checks best-interests duty, conflicts, documentation requirements, and generates warnings and required actions.

**Architectural Boundary** (Constitution Principle XII, FR-004C, CL-039): Advice Engine is the **judgement and compliance brain**. It MUST consume Facts from Compute Engine (never calculate them) and knowledge objects from References & Research Engine (never store them). It applies reasoning frameworks, interpretation logic based on Advice Guidance (e.g., "This is usually beneficial when...", "Preferable for clients who..."), behavioral-aware advice patterns, and reasoning frameworks (problem → constraint → action → result, prioritisation patterns, scenario comparison patterns, trade-off handling patterns). It can perform comparison and aggregation operations on Facts but MUST NOT perform numeric calculations that produce new Facts (all Facts must originate from Compute Engine). **Schema Feedback** (FR-SCHEMA-01): Advice Engine implementations MAY emit structured schema-feedback requests via `POST /research/refine` API when a missing field, relationship, or canonical mapping blocks correct implementation.

**Technical Approach**: Python-based microservice using FastAPI + SQLAlchemy 2.0 + Pydantic v2, deterministic compliance evaluation engine, integration with Compute Engine for Fact data, and References & Research Engine for regulatory requirements. Row-Level Security (RLS) for tenant isolation, Sentry for error tracking.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**:
- **API Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (full control, async support, type safety)
- **Validation**: Pydantic v2 (request/response validation, serialization)
- **Storage**: PostgreSQL 15+ with:
  - Relational edge table (src_id, dst_id, relation_type) for compliance relationships
  - JSONB columns for metadata (flexible, queryable)
  - Bitemporal fields (`valid_from`, `valid_to`) for audit history and time-travel queries
  - Partial indexes on current data (`WHERE valid_to IS NULL`) for performance
  - Row-Level Security (RLS) policies for tenant isolation (see CL-031 and FR-030 in master spec for security guarantee that User A can NEVER see User B's data under ANY circumstances)
  - **Security Testing**: Automated security tests for cross-tenant data access prevention per FR-014A - verify User A cannot access User B's compliance evaluations, advice guidance, or client outcome strategies under ANY circumstances, including bugs, misconfigured queries, malicious input, and missing tenant context
- **Error Tracking**: Sentry (free tier) for error monitoring
- **Testing**: pytest

## API Endpoints

### Compliance APIs

- **`POST /advice/check`**: Check compliance of advice recommendations
  - **Request**: `{ client_data, computed_facts, advice_recommendations, as_of_date? }`
  - **Response**: `{ outcomes: [...], required_actions: [...], warnings: [...] }`
  - **Structured Format**: Clear indication of compliance status and specific issues

- **`GET /advice/requirements?context=...`**: Retrieve compliance requirements for specific context
  - **Query Parameters**: `context=giving_personal_advice|recommending_product_replacement|...&as_of=...`
  - **Response**: Required actions, documentation, and professional standards for the context
  - **Time-Travel**: Support `as_of` dates for historical requirements

## Module Dependencies

### Depends On

- **Compute Engine** (`002-compute-engine`): Fact data for compliance evaluation
- **References & Research Engine** (`003-references-research-engine`): Regulatory requirement lookups
- **Advice Guidance Data**: Must be populated before compliance evaluations can be performed

### Used By

- **Frankie's Finance**: Validates consumer advice and displays compliance results
- **Veris Finance**: Validates adviser advice, generates compliance checklists, ensures regulatory compliance
- **Document Generation Systems**: May use compliance requirements when generating SOA, ROA, or other compliance documents

## Integration Points

### Module-to-Module Integration

- **Frankie's Finance → Advice Engine**: 
  - Consumer advice validation via `POST /advice/check`
  - Results formatted for consumer-friendly display

- **Veris Finance → Advice Engine**: 
  - Adviser advice validation via `POST /advice/check`
  - Compliance requirements via `GET /advice/requirements`
  - Detailed compliance information for professional use

- **Advice Engine → Compute Engine**: 
  - Fact data retrieval via `GET /facts` for compliance evaluation
  - Ensures evaluations are based on accurate calculations

- **Advice Engine → References & Research Engine**: 
  - Regulatory requirement lookups via `GET /references/search` and `GET /references/{id}`
  - Used for compliance evaluation and warning generation

### External Integration

- **Advice Guidance Data Sources → Advice Engine**: 
  - Ingestion pipeline receives Advice Guidance from regulatory sources, legal databases, or manual authoring
  - Makes it available for compliance evaluation

- **Compliance Reporting Systems → Advice Engine**: 
  - May query compliance evaluations and audit logs for regulatory reporting and oversight

## Technical Implementation Details

### Storage Architecture

- **Entity ID Generation**:
  - **Format**: Two-letter prefix + ULID/hash (e.g., `AG-01HFSZ2R2Y1G2M5D8C9QWJ7K4T`)
  - **Prefixes**: `AG-` (Advice Guidance), `ST-` (Client Outcome Strategy)
  - **Collision Handling**: ULID/hash ensures global uniqueness. ULID's inherent uniqueness properties (128-bit entropy, timestamp-based ordering) provide collision-free IDs without explicit collision detection logic. Database unique constraints on entity ID columns provide defense-in-depth.
  - **Implementation**: Use Python `ulid` library or equivalent for ULID generation. Prefix validation ensures correct entity type association.
  - **Reference**: `specs/001-master-spec/canonical_data_model.md` (Canonical ID Prefix Reference section), `.specify/memory/constitution.md` (Canonical ID Prefix Reference section)

- **Provenance Storage Design**:
  - **Relational Edge Table**: `provenance_edges` table stores relationships as rows (edges) with:
    - `src_id` (source entity ID, e.g., `AG-...`)
    - `dst_id` (destination entity ID, e.g., `RE-...` for regulatory citations)
    - `relation_type` (relationship type: `CITES`, `REQUIRES`, `CONFLICTS_WITH`, etc.)
    - `created_at` (timestamp for audit trail)
    - `tenant_id` (for tenant isolation, NULL for global entities like Advice Guidance)
  - **JSONB Metadata**: Flexible metadata stored in JSONB columns on entity tables for queryable, extensible attributes (e.g., compliance evaluation details, warning metadata, checklist items). Relationships are stored as rows; attributes are stored as JSONB.
  - **Architecture Decision**: Relationships stored as relational rows (edges) enable efficient graph traversal, referential integrity, and query optimization. JSONB used only for entity attributes, not relationships.
  - **Reference**: `Design_docs/final_design_questions.md` Section 4

- **Bitemporal Fields & Time-Travel**:
  - **Fields**: All temporal entities have `valid_from` (timestamp) and `valid_to` (timestamp, NULL for current) fields
  - **Default Filter for Current Rows**: `WHERE valid_to IS NULL` - this is the standard filter for querying "current" or "active" entities
  - **Time-Travel Queries**: Use `as_of` date parameter. System selects rows where `as_of` falls within `valid_from` and `valid_to` (or `valid_to IS NULL`). Query pattern: `WHERE valid_from <= as_of AND (valid_to IS NULL OR valid_to > as_of)`
  - **Partial Indexes**: Indexes on current data only (`WHERE valid_to IS NULL`) for performance optimization. These indexes dramatically improve query performance for common "current state" queries.
  - **Entities with Bitemporal Fields**: Advice Guidance, Client Outcome Strategies, Compliance Evaluations
  - **Reference**: `Design_docs/final_design_questions.md` Section 4, `specs/001-master-spec/spec.md` CL-011, CL-012

### Compliance Evaluation

- **Deterministic Evaluation**: Same advice + same client data + same Facts + same `as_of` date = identical compliance outcomes
- **Pinning**: Pin evaluations to explicit `as_of` dates and Advice Guidance versions
- **Best-Interests Duty**: Evaluate whether recommendations serve client's interests
- **Conflict Detection**: Analyze adviser relationships, product recommendations, fee structures
- **Documentation Verification**: Check whether required documents (FSG, SOA, ROA) have been created or planned
- **Product Replacement Logic**: Check whether product switches are justified and serve client's best interests

### Warnings and Required Actions

- **Severity Levels**: `BLOCK` (advice MUST NOT be presented), `WARNING` (advice MAY be presented with warnings), `INFO` (informational)
- **Formatting**: Technical language for advisers, consumer-friendly language for consumers
- **Regulatory References**: Link warnings and actions to regulatory sources

### Compliance Documentation

- **Checklist Generation**: Required documents, actions, and professional standards
- **Completion Tracking**: Track completion status for checklist items
- **Export Formats**: Suitable for inclusion in compliance packs (JSON, PDF)
- **Linking**: Link checklists to specific advice scenarios

### Audit Trail

- **Logging**: Track all compliance evaluations with timestamps and reasoning trails
- **Historical Reconstruction**: Support time-travel queries using Advice Guidance versions applicable at that time
- **Export**: Complete audit trails suitable for regulatory review

## Implementation Phases

### Phase 1: Compliance Evaluation (Weeks 1-2)

**Tasks**:
1. **Entity ID Generation System**
   - Implement entity ID generation utility using Python `ulid` library
   - Implement prefix validation (AG-, ST-)
   - Implement ID format validation and parsing
   - Add database unique constraints on entity ID columns for defense-in-depth collision prevention
   - Reference: `specs/001-master-spec/canonical_data_model.md` (Canonical ID Prefix Reference section), `.specify/memory/constitution.md` (Canonical ID Prefix Reference section)

2. **Data Model Design**
   - Design Advice Guidance data model with bitemporal fields (`valid_from`, `valid_to`)
   - Design compliance evaluation data model with bitemporal fields
   - Design warning and required action data models
   - Implement default filter for current rows (`WHERE valid_to IS NULL`)
   - Create partial indexes on current data (`WHERE valid_to IS NULL`) for performance
   - Reference: `Design_docs/final_design_questions.md` Section 4

3. **Provenance Storage Implementation**
   - Implement `provenance_edges` table schema (src_id, dst_id, relation_type, created_at, tenant_id)
   - Implement JSONB metadata columns on entity tables for attributes
   - Implement provenance link creation and querying utilities (for citations, requirements, conflicts)
   - Ensure relationships stored as rows (edges), attributes stored as JSONB
   - Reference: `Design_docs/final_design_questions.md` Section 4

4. **Bitemporal Fields & Time-Travel**
   - Implement bitemporal fields (`valid_from`, `valid_to`) on all temporal entities
   - Implement time-travel query utilities with `as_of` date support
   - Implement query pattern: `WHERE valid_from <= as_of AND (valid_to IS NULL OR valid_to > as_of)`
   - Create partial indexes on current data for performance optimization
   - Reference: `Design_docs/final_design_questions.md` Section 4, `specs/001-master-spec/spec.md` CL-011, CL-012

5. **Compliance Logic**
   - Implement best-interests duty checks
   - Implement conflict detection
   - Implement documentation requirement checks
   - Implement product replacement logic evaluation
   - Implement deterministic compliance evaluation with time-travel support

**Deliverables**:
- Entity ID generation system implemented with ULID support
- Advice Guidance data model implemented with bitemporal fields
- Compliance evaluation data model implemented with bitemporal fields
- Provenance storage implemented (relational edge table + JSONB)
- Bitemporal time-travel queries functional
- Compliance evaluation logic functional with time-travel support

### Phase 2: Compliance APIs (Week 3)

**Tasks**:
1. **API Implementation**
   - Implement `POST /advice/check` (compliance checking)
   - Implement `GET /advice/requirements?context=...` (requirement retrieval)
   - Implement warning and required action generation
   - Implement consumer-friendly vs professional warning formatting
   - Implement context-based filtering
   - Implement time-travel queries for requirements

**Deliverables**:
- Compliance APIs functional
- Warning generation working
- OpenAPI schema generated for all endpoints (`specs/001-master-spec/contracts/advice-engine.openapi.yaml`)
- API versioning implemented (`/api/v1/...`)

### Phase 3: Integration (Week 4)

**Tasks**:
1. **Module Integration**
   - Integrate with Compute Engine (Fact data retrieval via `GET /facts`)
   - Integrate with References & Research Engine (regulatory requirements via `GET /references/search` and `GET /references/{id}`)
   - Implement deterministic compliance evaluation with pinning to `as_of` dates and Advice Guidance versions

**Deliverables**:
- Integration with Compute Engine working
- Integration with References & Research Engine working

### Phase 4: Compliance Documentation (Week 5)

**Tasks**:
1. **Checklist Generation**
   - Implement compliance checklist generation
   - Implement completion tracking
   - Implement export functionality (JSON, PDF)
   - Link checklists to specific advice scenarios

**Deliverables**:
- Compliance checklist generation functional
- Export functionality working

### Phase 5: Audit and Reporting (Week 6)

**Tasks**:
1. **Audit Trail**
   - Implement comprehensive audit logging
   - Implement audit trail export
   - Implement historical reconstruction using Advice Guidance versions
   - Support time-travel queries

**Deliverables**:
- Audit trail complete
- Historical reconstruction working

### Phase 6: Testing & Validation (Ongoing)

**Tasks**:
1. **Test Implementation**
   - Unit tests for compliance logic
   - Integration tests with Compute Engine
   - Golden dataset tests (ASIC compliance examples)
   - Deterministic reproducibility tests

2. **Minimum Validation Suite (CRITICAL - Required Before Shipping)**
   - **Golden Dataset Validation - ASIC Examples**:
     - Collect at least 5 ASIC compliance examples from regulatory guides
     - Validate best interests duty checks
     - Validate conflict detection logic
     - Validate advice documentation requirements
     - All compliance checks must match ASIC examples exactly
     - Document expected vs actual compliance outcomes for each example

**Deliverables**:
- Test coverage > 80%
- Minimum validation suite complete:
  - ✅ At least 5 ASIC compliance examples validated
- **CRITICAL**: System MUST NOT ship without minimum validation suite complete

