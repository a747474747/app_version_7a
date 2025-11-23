# LLM Orchestrator Implementation Plan

**Branch**: `005-llm-orchestrator` | **Date**: 2025-01-27 | **Spec**: `specs/005-llm-orchestrator/spec_005_llm_orchestrator.md`  
**Status**: ✅ **Phase 0 Complete**

## Summary

LLM Orchestrator translates human language into structured, auditable requests. Stateless translator and router that performs intent detection, schema validation, safety/PII filtering, prompt templating, model vendor routing, and RAG (Retrieval-Augmented Generation) capability. Never the source of truth.

**Architectural Boundary** (Constitution Principle XII, FR-004D): LLM Orchestrator is a **thin natural-language router and controller**. It MUST interpret user input, build structured requests for the three engines (Compute, References, Advice), call them in sequence, validate/repair schemas, and turn outputs back into user-facing text. It MUST NOT invent rules, perform calculations, override deterministic outputs, store knowledge objects, or contain business logic. It serves as a translation layer between natural language and structured APIs; all business logic, calculations, and knowledge remain in their designated components.

**CRITICAL INPUT REQUIREMENT**: LLMs MUST ONLY receive text content. All binary formats (PDF, DOCX, images, audio, video, etc.) MUST be converted to plain text before being passed to any LLM provider. This conversion MUST happen in the ingestion/preprocessing layer (References & Research Engine) using appropriate parsers (DocumentParser for PDFs/DOCX, transcription services for audio, OCR for images). The LLM Orchestrator MUST validate that all content sent to LLM providers is plain text strings, never binary data or file paths. This ensures LLM providers receive properly formatted text input and prevents errors from binary data corruption.

**Technical Approach**: Python-based microservice using FastAPI + SQLAlchemy 2.0 + Pydantic v2, OpenRouter integration (unified API for all LLM providers, supporting both OpenRouter credits and BYOK), PII filtering, schema validation, prompt templating with primer loading from centralized location, and RAG capability for prompt augmentation. RAG retrieves relevant structured data (rules, references, assumptions, advice guidance, client outcome strategies) from the relational database via References & Research Engine APIs to augment LLM prompts, improving intent detection accuracy, parsing quality, and conversational response relevance while maintaining compliance with Principle IV (LLM remains translator only). All content sent to LLM providers MUST be plain text (validated before API calls). Sentry for error tracking.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**:
- **API Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (full control, async support, type safety) - for storing conversation history, token tracking, cost tracking, and cost cap configuration
- **Validation**: Pydantic v2 (request/response validation, serialization)
- **LLM Providers**: OpenRouter (MVP) - unified API for all LLM providers, supporting both OpenRouter credits and BYOK (Bring Your Own Key) integration for existing OpenAI API keys
- **PII Filtering**: Rule-based filtering (MVP), ML-based (future)
- **Error Tracking**: Sentry (free tier) for error monitoring
- **Testing**: pytest
- **Security**: Row-Level Security (RLS) policies for tenant isolation (see CL-031 and FR-030 in master spec for security guarantee that User A can NEVER see User B's data under ANY circumstances)
- **Security Testing**: Automated security tests for cross-tenant data access prevention per FR-031A - verify User A cannot access User B's conversation history, extracted parameters, or LLM-generated content under ANY circumstances, including bugs, misconfigured queries, malicious input, and missing tenant context
- **RAG**: Retrieval-Augmented Generation capability for prompt augmentation
  - **Retrieval**: PostgreSQL with JSONB for semantic/keyword search, Redis caching for frequent retrievals
  - **Model Routing**: gpt-5-mini for retrieval queries, gpt-5.1 for generation when needed
  - **Performance**: <1 second (p95) retrieval latency, 80% cache hit rate target, 95% retrieval relevance target
  - **Compliance**: Principle IV compliant (LLM remains translator only), tenant isolation (RLS), PII redaction
  - **Integration**: References & Research Engine APIs (`/references/search`, `/references/{id}`) for data retrieval

## API Endpoints

### Intent Parsing API

- **`POST /llm/parse`**: Parse natural language intent (enhanced with optional RAG)
  - **Request**: `{ query, context?, use_rag?: boolean }`
  - **Response**: `{ intent, params, next_call, retrieved_context?: [...] }`
  - **Output**: Detected intent, extracted parameters, next action, optional retrieved context for citation
  - **RAG**: When `use_rag=true`, retrieves relevant structured data to augment prompts, improving intent detection accuracy

### Conversational Chat API

- **`POST /llm/chat`**: Conversational interface (enhanced with optional RAG)
  - **Request**: `{ messages: [...], conversation_id?, context?, use_rag?: boolean }`
  - **Response**: `{ messages: [...], tool_calls: [...], citations: [...], retrieved_context?: [...] }`
  - **Features**: Multi-turn conversation, tool calls, citations to authoritative sources, optional RAG-augmented context
  - **RAG**: When `use_rag=true`, retrieves relevant structured data to augment prompts, improving conversational response relevance

### Cost Management APIs

- **`GET /llm/costs`**: Get cost tracking data per tenant
  - **Query Parameters**: `tenant_id, start_date?, end_date?, model?`
  - **Response**: `{ costs: [...], total_cost, period }`

- **`GET /llm/costs/caps`**: Get cost cap configuration
  - **Query Parameters**: `tenant_id`
  - **Response**: `{ tenant_id, cap_amount, period, current_usage, alerts_enabled }`

- **`PUT /llm/costs/caps`**: Update cost cap configuration
  - **Request**: `{ tenant_id, cap_amount, period, alerts_enabled }`
  - **Response**: `{ success, updated_cap }`

## User Communication Flow

### Extraction Process

The LLM Orchestrator does NOT extract advice directly. It translates natural language into structured requests:

1. **Intent Detection**: Parses user queries to identify intent (calculation, explanation, comparison, information request)
2. **Parameter Extraction**: Extracts structured parameters (client data, scenario parameters, time horizons)
3. **RAG Retrieval (Optional)**: When `use_rag=true`, retrieves relevant structured data from References & Research Engine:
   - Rules, references, assumptions, advice guidance, client outcome strategies
   - Retrieves via `/references/search` and `/references/{id}` APIs
   - Uses semantic/keyword search on PostgreSQL JSONB metadata
   - Caches frequent retrievals in Redis (target: 80% hit rate)
4. **PII Filtering**: Filters personally identifiable information before sending to external LLM providers
5. **Schema Validation**: Validates LLM outputs against expected schemas with retry/repair logic (3 attempts, exponential backoff)

### Advice Provision Flow

The LLM Orchestrator does NOT generate advice. It structures requests that are executed by backend engines:

```
User Query (Natural Language)
    ↓
LLM Orchestrator (Intent Detection + Parameter Extraction)
    ↓
Structured Request Generation
    ↓
Compute Engine (Deterministic Calculations) → Facts
    ↓
Advice Engine (Compliance Validation) → Compliance Checks
    ↓
LLM Orchestrator (Format Response) → User-Facing Text
```

**Key Points**:
- **Translation Layer**: Converts natural language → structured API requests
- **Engine Coordination**: Calls Compute Engine (`POST /run`), Advice Engine (`POST /advice/check`), and References Engine (`GET /references/search`) in sequence
- **Response Formatting**: Converts structured outputs back into user-facing text with citations
- **Never Determines Outcomes**: All calculations and compliance checks happen in deterministic engines

### User Communication APIs

Two main APIs handle user communication:

1. **`POST /llm/parse`**: Intent parsing
   - Input: `{ query, context?, use_rag?: boolean }`
   - Output: `{ intent, params, next_call, retrieved_context?: [...] }`
   - Use case: Single-turn intent detection

2. **`POST /llm/chat`**: Conversational interface
   - Input: `{ messages: [...], conversation_id?, context?, use_rag?: boolean }`
   - Output: `{ messages: [...], tool_calls: [...], citations: [...], retrieved_context?: [...] }`
   - Features:
     - Multi-turn conversation support
     - Tool calls (structured requests to backend modules)
     - Citations to authoritative sources
     - Consumer-friendly (Frankie's Finance) or professional (Veris Finance) formatting

## Integration Points

### Compute Engine Integration

- **Purpose**: Transform natural language queries into structured calculation requests
- **APIs Used**: 
  - `POST /run` - Execute single calculation
  - `POST /run-batch` - Execute batch calculations
  - `GET /facts` - Retrieve computed Facts
  - `GET /explain/{fact_id}` - Get provenance chain for a Fact
- **Integration Pattern**: LLM Orchestrator generates structured requests from natural language, forwards to Compute Engine, receives Facts, formats responses conversationally

### Advice Engine Integration

- **Purpose**: Transform natural language queries into compliance check requests
- **APIs Used**:
  - `POST /advice/check` - Check compliance of advice recommendations
  - `GET /advice/requirements` - Retrieve compliance requirements for specific context
- **Integration Pattern**: LLM Orchestrator generates structured compliance check requests, forwards to Advice Engine, receives compliance results, formats responses conversationally

### References & Research Engine Integration

- **Purpose**: Retrieve references for citation generation and RAG augmentation
- **APIs Used**:
  - `GET /references/search` - Search references (used for RAG retrieval)
  - `GET /references/{id}` - Retrieve full reference (used for citation generation)
- **Integration Pattern**: 
  - **RAG Retrieval**: When `use_rag=true`, LLM Orchestrator queries References Engine for relevant structured data to augment prompts
  - **Citation Generation**: LLM Orchestrator retrieves full references to include in conversational responses

## Referenced Files and Documentation

### Core Specification Files
- `specs/005-llm-orchestrator/spec_005_llm_orchestrator.md` - Main specification
- `specs/001-master-spec/master_spec.md` - Master specification (references: FR-004D, FR-013, FR-014, FR-015, CL-035, CL-042)
- `specs/001-master-spec/master_plan.md` - Master implementation plan
- `specs/001-master-spec/master_tasks.md` - Task breakdown

### Primer and Prompt Files
- `specs/005-llm-orchestrator/primers-prompts/primer_external_research_v1a.md` - External research primer
- `specs/005-llm-orchestrator/primers-prompts/primer_intent_detection_v1a.md` - Intent detection primer
- `specs/005-llm-orchestrator/primers-prompts/primer_conversational_v1a.md` - Conversational primer
- `specs/005-llm-orchestrator/primers-prompts/primer_general_v1a.md` - General primer
- `specs/005-llm-orchestrator/primers-prompts/INDEX.md` - Primer index
- `specs/005-llm-orchestrator/primers-prompts/PRIMER_CONSISTENCY_REPORT.md` - Consistency report

### Related Module Specifications
- `specs/002-compute-engine/spec_002_compute_engine.md` - Compute Engine spec
- `specs/002-compute-engine/plan_002_compute_engine.md` - Compute Engine plan
- `specs/003-references-research-engine/plan_003_references_research_engine.md` - References Engine plan
- `specs/003-references-research-engine/research_guidance/compute-engine-requirements-context.md` - Compute Engine requirements context
- `specs/003-references-research-engine/research_guidance/fully-automated-research-loop.md` - Research loop guidance
- `specs/004-advice-engine/plan_004_advice_engine.md` - Advice Engine plan
- `specs/004-advice-engine/checklists/Research_checklist_do_we_understand_these.md` - Research checklist

### API Contract Files
- `specs/001-master-spec/contracts/llm-orchestrator.openapi.yaml` - OpenAPI schema (to be generated)

### Design and Guidance Files
- `Design_docs/Advice_engine_calc_guidance.md` - Calculation guidance
- `Design_docs/final_design_questions.md` - Design questions

## Technical Implementation Details

### Phase 1: Intent Detection and Parsing

**Goal**: Detect user intent from natural language queries and extract structured parameters.

**Tasks**:
- Implement intent detection from natural language in `backend/llm-orchestrator/src/intent/detection.py`
- Implement parameter extraction in `backend/llm-orchestrator/src/intent/parameter_extraction.py`
- Implement missing parameter identification in `backend/llm-orchestrator/src/intent/missing_params.py`
- Implement ambiguous query handling in `backend/llm-orchestrator/src/intent/ambiguity.py`
- **CRITICAL**: Implement text-only input validation in `backend/llm-orchestrator/src/validation/text_only_validation.py` - validate that all content sent to LLM providers is plain text strings (never binary data, file paths, or non-text formats)
- Implement LLM output validation against schemas with retry/repair loop (max 3 retries, exponential backoff, type coercion, defaults, normalization, LLM regeneration) in `backend/llm-orchestrator/src/validation/schema_validation.py`
- Implement validation error handling in `backend/llm-orchestrator/src/validation/error_handling.py`
- Implement request validation before forwarding to Compute Engine in `backend/llm-orchestrator/src/validation/request_validation.py`

**Deliverables**:
- Intent detection operational (90% accuracy target)
- Parameter extraction operational (85% accuracy target)
- Schema validation with retry/repair logic operational
- `POST /llm/parse` endpoint functional

### Phase 2: Conversational Interface

**Goal**: Provide multi-turn conversational interface with tool calls and citations.

**Tasks**:
- Implement multi-turn conversation support in `backend/llm-orchestrator/src/conversation/multi_turn.py`
- Implement conversation context management in `backend/llm-orchestrator/src/conversation/context.py`
- Implement tool call generation in `backend/llm-orchestrator/src/conversation/tool_calls.py`
- Implement schema validation for LLM-generated tool calls before forwarding to Compute Engine in `backend/llm-orchestrator/src/conversation/tool_call_validation.py`
- Implement schema versioning for tool calls in `backend/llm-orchestrator/src/conversation/tool_call_versioning.py`
- Implement citation generation (References) in `backend/llm-orchestrator/src/conversation/citations.py`

**Deliverables**:
- Multi-turn conversation support operational
- Tool call generation operational
- Citation generation operational
- `POST /llm/chat` endpoint functional

### Phase 3: LLM Model Routing

**Goal**: Implement intelligent model selection and OpenRouter integration.

**Tasks**:
- Implement model selection method for selecting models for different tasks based on OpenRouter model data schema (performance quality, developer preferences, pricing, speed) in `backend/llm-orchestrator/src/models/selector.py`
- Implement model metadata fetching from OpenRouter API (`/api/v1/models` endpoint) in `backend/llm-orchestrator/src/models/metadata_fetcher.py`
- Implement performance tracking and storage system (task-specific performance metrics, historical analysis) in `backend/llm-orchestrator/src/models/performance_tracking.py`
- Implement configuration system for developer preferences per task type in `backend/llm-orchestrator/src/models/preferences.py` (reads from `backend/llm-orchestrator/model-config/preferred_models.yaml` - **CRITICAL**: Models MUST NEVER be hardcoded, always read from configuration file)
- Implement selection algorithm with weighted factors (performance quality, developer preferences, pricing, speed) in `backend/llm-orchestrator/src/models/selection_algorithm.py`
- Implement OpenRouter API integration using OpenRouter SDK or direct API calls in `backend/llm-orchestrator/src/routing/openrouter_client.py`
- Implement BYOK (Bring Your Own Key) configuration for OpenAI API keys via OpenRouter in `backend/llm-orchestrator/src/routing/byok_config.py`
- Implement data policy filtering to prefer models that do not train on prompts using OpenRouter's data policy filtering features in `backend/llm-orchestrator/src/routing/data_policy_filter.py`
- Implement intelligent model switching based on task type (MVP: within models available via OpenRouter) in `backend/llm-orchestrator/src/routing/model_switching.py`
- Implement preference for cheaper models with performance fallback via OpenRouter in `backend/llm-orchestrator/src/routing/cost_optimization.py`
- Implement prompt templating compatible with OpenRouter API in `backend/llm-orchestrator/src/routing/prompt_templates.py`
- Implement token tracking (input/output/cached tokens per request) in `backend/llm-orchestrator/src/routing/token_tracking.py`
- Implement cost calculation based on token usage and model pricing in `backend/llm-orchestrator/src/routing/cost_calculation.py`

**Deliverables**:
- OpenRouter integration operational
- Model selection logic operational
- Token tracking operational
- Cost calculation operational

### Phase 3A: Cost Management & Budget Controls

**Goal**: Implement cost tracking, caps, and budget controls per tenant.

**Tasks**:
- Implement cost tracking database schema (store cost data per tenant, per model, per time period) in `infrastructure/database/postgres/schema.sql`
- Implement cost storage and retrieval in `backend/llm-orchestrator/src/costs/storage.py`
- Implement configurable LLM cost caps per tenant and per time period (daily, weekly, monthly, default $100/month) in `backend/llm-orchestrator/src/costs/caps.py`
- Implement budget alert system (80% warning, 100% critical) in `backend/llm-orchestrator/src/costs/alerts.py`
- Implement cost rejection mechanism (reject requests when cap reached) in `backend/llm-orchestrator/src/costs/rejection.py`
- Implement cost reporting API (`GET /llm/costs`, `GET /llm/costs/caps`, `PUT /llm/costs/caps`) in `backend/llm-orchestrator/src/api/costs.py`
- Integrate cost cap checking into `POST /llm/parse` and `POST /llm/chat` endpoints in `backend/llm-orchestrator/src/api/parse.py` and `backend/llm-orchestrator/src/api/chat.py`
- Implement daily query tracking for rate-limited models (track queries per model per day, enforce 1k/day limit for `alibaba/tongyi-deepresearch-30b-a3b:free`, reject requests when limit exceeded) in `backend/llm-orchestrator/src/routing/query_tracking.py`

**Deliverables**:
- Cost tracking operational
- Cost caps operational
- Budget alerts operational
- Cost rejection operational
- Cost reporting APIs functional

### Phase 4: Primers and Prompts Management

**Goal**: Implement centralized primer/prompt loading and versioning system.

**Tasks**:
- Create `specs/005-llm-orchestrator/primers-prompts/` folder structure
- Organize all LLM primers and prompts as `.md` files in this folder
- Implement primer loader system in `backend/llm-orchestrator/src/prompts/loader.py` to load primers from `specs/005-llm-orchestrator/primers-prompts/`
- Implement A/B versioning system for primers and prompts in `backend/llm-orchestrator/src/prompts/versioning.py` (supports `_v1a.md`, `_v1b.md` naming)
- Implement performance measurement system for A/B variants in `backend/llm-orchestrator/src/prompts/performance_tracking.py`
- Implement metrics tracking (accuracy, latency, cost, user satisfaction) per variant in `backend/llm-orchestrator/src/prompts/metrics.py`
- Implement variant selection logic based on performance data in `backend/llm-orchestrator/src/prompts/variant_selection.py`
- Create primer index (`specs/005-llm-orchestrator/primers-prompts/INDEX.md`) documenting all primers, versions, and performance metrics

**Deliverables**:
- Primer loader operational
- A/B versioning system operational
- Performance tracking operational
- Primer index maintained

### Phase 5: Safety and Privacy

**Goal**: Implement PII filtering and safety content filtering.

**Tasks**:
- Implement PII profile storage system (receive known PII from Frankie's Finance and Veris Finance) in `backend/llm-orchestrator/src/safety/pii_profiles.py`
- Implement PII detection using known PII profiles (check queries against known names, addresses, account numbers) in `backend/llm-orchestrator/src/safety/pii_detection.py`
- Implement pattern-based PII detection (regex patterns for structured PII) in `backend/llm-orchestrator/src/safety/pii_patterns.py`
- Implement PII filtering before sending to OpenRouter API (MANDATORY pre-processing step) in `backend/llm-orchestrator/src/safety/pii_filtering.py`
- Implement PII redaction with placeholder replacement in `backend/llm-orchestrator/src/safety/pii_redaction.py`
- Implement audit logging to verify no PII in LLM API request payloads in `backend/llm-orchestrator/src/safety/pii_audit.py`
- Implement safety content filtering in `backend/llm-orchestrator/src/safety/content_filtering.py`
- Implement PII preservation for internal use (separate storage, mapping system) in `backend/llm-orchestrator/src/safety/pii_preservation.py`
- Implement user-friendly error messaging in `backend/llm-orchestrator/src/safety/error_messaging.py`

**Deliverables**:
- PII filtering operational (100% of queries filtered before external LLM calls)
- PII preservation operational (original data preserved for internal use)
- Safety content filtering operational
- Audit logging operational

### Phase 6: APIs

**Goal**: Implement main API endpoints.

**Tasks**:
- Implement `POST /llm/parse` (intent parsing) in `backend/llm-orchestrator/src/api/parse.py`
- Implement `POST /llm/chat` (conversational interface) in `backend/llm-orchestrator/src/api/chat.py`
- Implement circuit breaker for Compute Engine calls from LLM Orchestrator in `backend/llm-orchestrator/src/api/compute_engine_circuit_breaker.py`
- Implement timeout handling for LLM→Compute Engine calls in `backend/llm-orchestrator/src/api/compute_engine_timeout.py`
- Implement rate limiting per vendor and tenant in `backend/llm-orchestrator/src/api/rate_limiting.py`

**Deliverables**:
- `POST /llm/parse` endpoint functional
- `POST /llm/chat` endpoint functional
- Circuit breaker operational
- Timeout handling operational
- Rate limiting operational

### Phase 7: RAG Capability Integration

**Goal**: Implement RAG (Retrieval-Augmented Generation) capability for prompt augmentation.

**Tasks**:
- Implement RAGRetriever class for retrieving relevant structured data (rules, references, assumptions, advice guidance, client outcome strategies) from relational database in `backend/llm-orchestrator/src/rag/retriever.py`
- Integrate RAG retrieval with References & Research Engine APIs (`/references/search`, `/references/{id}`) in `backend/llm-orchestrator/src/rag/references_integration.py`
- Implement query builder for semantic/keyword search on PostgreSQL JSONB metadata (no new data stores) in `backend/llm-orchestrator/src/rag/query_builder.py`
- Implement Redis caching for frequent RAG retrievals (cache key: `rag:{query_hash}:{filters_hash}:{tenant_id}`, TTL: 1 hour, target: 80% cache hit rate, <1s latency p95) in `backend/llm-orchestrator/src/rag/cache.py`
- Implement formatter for prompt augmentation with citation generation in `backend/llm-orchestrator/src/rag/formatter.py`
- Enhance intent detection with RAG retrieval (augment prompts, include citations) in `backend/llm-orchestrator/src/intent/rag_enhancement.py`
- Enhance conversational interface with RAG retrieval (augment prompts, include citations) in `backend/llm-orchestrator/src/conversation/rag_enhancement.py`
- Add optional `use_rag` flag to `/llm/parse` and `/llm/chat` APIs for RAG-enhanced processing in `backend/llm-orchestrator/src/api/parse.py` and `backend/llm-orchestrator/src/api/chat.py`
- Implement model routing for RAG (use cheaper models gpt-5-mini for retrieval queries, switch to higher-capability models gpt-5.1 for generation when needed) in `backend/llm-orchestrator/src/rag/model_routing.py`
- Ensure RAG complies with Principle IV: LLM remains translator only; retrieved data grounds prompts but does not make LLM the source of truth in `backend/llm-orchestrator/src/rag/compliance.py`
- Ensure retrieved data respects tenant isolation (RLS) and PII redaction in `backend/llm-orchestrator/src/rag/tenant_isolation.py`

**Deliverables**:
- RAG retrieval operational (95% relevance target)
- Redis caching operational (80% hit rate target)
- Prompt augmentation operational
- Model routing operational
- Principle IV compliance verified
- Tenant isolation verified

### Phase 8: Testing

**Goal**: Comprehensive test coverage for all functionality.

**Tasks**:
- Unit tests for intent detection in `backend/llm-orchestrator/tests/unit/test_intent.py`
- Integration tests with Compute Engine in `backend/llm-orchestrator/tests/integration/test_compute_engine.py`
- LLM output validation tests in `backend/llm-orchestrator/tests/unit/test_validation.py`
- PII filtering tests in `backend/llm-orchestrator/tests/unit/test_pii_filtering.py`
- Performance tests (latency, cost) in `backend/llm-orchestrator/tests/performance/test_performance.py`
- Tests for token tracking (input/output/cached tokens) in `backend/llm-orchestrator/tests/unit/test_token_tracking.py`
- Tests for cost calculation based on token usage in `backend/llm-orchestrator/tests/unit/test_cost_calculation.py`
- Tests for primer/prompt A/B versioning system in `backend/llm-orchestrator/tests/unit/test_prompts_versioning.py`
- Tests for performance measurement and variant selection in `backend/llm-orchestrator/tests/unit/test_prompts_performance.py`
- Security tests for cross-tenant data access prevention in LLM Orchestrator per FR-031A in `backend/llm-orchestrator/tests/security/test_cross_tenant_access.py`
- Tests for RAG retrieval (95% relevance target, <1s latency p95, tenant isolation) in `backend/llm-orchestrator/tests/integration/test_rag.py`
- Tests for RAG constitution compliance (Principle IV validation, tenant isolation, PII redaction) in `backend/llm-orchestrator/tests/integration/test_rag_compliance.py`
- End-to-end tests for RAG via Veris/Frankie's UIs in `backend/llm-orchestrator/tests/e2e/test_rag_ui_integration.py`
- Golden dataset validation for RAG retrieval accuracy in `backend/llm-orchestrator/tests/golden/test_rag_golden.py`
- Property-based tests for RAG edge cases in `backend/llm-orchestrator/tests/property/test_rag_edge_cases.py`

**Deliverables**:
- Test coverage > 80%
- All success criteria validated
- Security tests passing
- RAG tests passing

## Success Criteria

### Measurable Outcomes

- **SC-001**: System correctly detects user intent from natural language queries with 90% accuracy when validated against manually classified test queries.
- **SC-002**: System extracts structured parameters from natural language queries with 85% accuracy for standard financial queries (superannuation, tax, investment scenarios).
- **SC-003**: System processes intent parsing requests and returns structured output within 2 seconds for 95% of requests.
- **SC-004**: System maintains coherent conversation context across up to 10 message turns, enabling natural multi-turn dialogue for 90% of conversations.
- **SC-005**: System filters PII from 100% of queries before sending to external LLM providers, maintaining privacy while enabling intent detection.
- **SC-006**: System validates LLM outputs against schemas and catches 95% of invalid outputs before they reach backend modules, preventing downstream errors.
- **SC-007**: System handles LLM provider failures gracefully, routing to alternative providers or returning appropriate errors within 5 seconds for 90% of failure scenarios.
- **SC-008**: 90% of users successfully complete their intended task (calculation, explanation, comparison) when interacting via natural language, demonstrating effective intent detection and request structuring.
- **SC-009**: System generates citations to authoritative sources in 80% of conversational responses that reference financial concepts or regulations, enabling verification and building trust.
- **SC-010**: System formats conversational responses appropriately for different audiences (consumers vs advisers) with 90% user satisfaction when tested with target user groups.
- **SC-011**: System achieves 95% retrieval relevance when validated against manually curated test queries, ensuring retrieved data is contextually appropriate for user queries.
- **SC-012**: System improves intent detection accuracy by 90% when RAG is enabled compared to baseline without RAG, measured against a golden dataset of financial queries.
- **SC-013**: System maintains retrieval latency under 1 second (p95) for RAG operations, ensuring acceptable response times for user interactions.
- **SC-014**: System achieves 80% cache hit rate for frequent retrieval queries in Redis, reducing latency and improving performance for common queries.
- **SC-015**: System correctly handles tenant isolation in 100% of RAG retrieval operations, preventing cross-tenant data access under all conditions including edge cases and error scenarios.
- **SC-016**: System generates citations to authoritative sources in 90% of RAG-augmented conversational responses that reference financial concepts or regulations, enabling verification and building trust.
- **SC-017**: System maintains 100% compliance with Principle IV (LLM remains translator only) in all RAG-augmented operations, ensuring retrieved data grounds prompts but does not make LLM the source of truth.
- **SC-018**: System correctly validates all RAG-augmented outputs affecting calculations against deterministic rules in the Compute Engine in 100% of cases, ensuring rule validation is never bypassed.
- **SC-019**: System gracefully handles no-relevant-data scenarios in 100% of cases, proceeding with standard LLM processing without errors or degraded user experience.
- **SC-020**: System passes all property-based tests for edge cases (no relevant data, excessive results, conflicting data) with 100% success rate, ensuring robust handling of edge conditions.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle IV: LLM as Translator, Not Source of Truth
- **Status**: COMPLIANT
- **Verification**: LLM Orchestrator translates natural language to structured requests; never determines financial outcomes
- **Implementation**: All LLM outputs validated against rules before execution; LLM never replaces rule logic; RAG retrieved data grounds prompts but does not make LLM the source of truth

### ✅ Principle X: Privacy, Tenancy, and Compliance
- **Status**: COMPLIANT
- **Verification**: Per-tenant isolation at data layer; PII-minimal logging; audit logs track all operations
- **Implementation**: Row-Level Security (RLS) policies enforced at PostgreSQL database level; PII filtering before external LLM calls; API keys/OAuth with rate limits; compliance with Australian Privacy Act 1988

**Constitution Check Result**: ✅ **PASS** - All principles compliant. No violations requiring justification.

