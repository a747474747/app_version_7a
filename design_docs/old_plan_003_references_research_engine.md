# References & Research Engine Implementation Plan

**Branch**: `003-references-research-engine` | **Date**: 2025-01-27 | **Spec**: `specs/003-references-research-engine/spec_003_references_research_engine.md`  
**Status**: ✅ **Phase 0 Complete**

## Summary

References & Research Engine manages authoritative legal and regulatory sources with pinpoints, versions, and metadata. Provides RAG-style retrieval for humans and AI models. Implements a **fully-automated research loop** that continuously extracts, validates, and refines knowledge from reference materials without human reviewers.

**Architectural Boundary** (Constitution Principle XII, FR-004B): References & Research Engine is the **single source of truth** for all knowledge storage and retrieval, including REFERENCES, RULES, ASSUMPTIONS, ADVICE GUIDANCE, CLIENT OUTCOME STRATEGIES, FINDINGS, RESEARCH QUESTIONS, and VERDICTS. It MUST NOT perform numeric calculations, execute rules, or generate personalised advice. Note: The Data Scraping Submodule downloads and organizes source documents as part of the ingestion process, but the module stores processed, structured knowledge objects rather than raw unprocessed documents. All knowledge objects MUST be stored and served by References & Research Engine; other modules MUST query this module for knowledge and MUST NOT store knowledge objects themselves.

**Technical Approach**: Python-based microservice using FastAPI + SQLAlchemy 2.0 + Pydantic v2, document ingestion pipeline with **Data Scraping Submodule** (automated downloading from `Research/human_provided_new_sources.md` using multiple methods including RSS feeds, transcription services, and adaptive scraping) and **Data Cleaning Submodule** (PDF to text conversion, chunking for OpenRouter model compatibility), version management with bitemporal fields, RAG-style retrieval optimized for AI models, and an automated research loop (Auto-Extract → Auto-Question → Auto-Validate → Auto-Curate) with trust scoring and continuous learning. Row-Level Security (RLS) for tenant isolation, Sentry for error tracking.

**Research Coverage**: The system validates coverage against the comprehensive research checklist (`specs/004-advice-engine/checklists/Research_checklist_do_we_understand_these.md`) covering calculation types, assumptions, edge cases, and Australia-specific design considerations.

## Technical Context

**Language/Version**: Python 3.11+

**Canonical Schemas**: Import from `specs/001-master-spec/schemas/` - data models, API schemas, database schemas (see master plan for canonical schemas structure)

**Primary Dependencies**:
- **API Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (full control, async support, type safety)
- **Validation**: Pydantic v2 (request/response validation, serialization)
- **Document Parsing**: Libraries for PDF (pypdf, pdfplumber), HTML (BeautifulSoup4, lxml), CSV, YAML, plain text
- **Data Scraping**: 
  - HTTP clients: `requests`, `httpx` (async)
  - Web scraping: `BeautifulSoup4`, `selenium` (headless browser), `playwright` (for JavaScript-heavy sites)
  - RSS feed parsing: `feedparser`
  - Audio transcription: `whisper` (OpenAI) or cloud transcription APIs
- **Data Cleaning**:
  - PDF to text: `pypdf`, `pdfplumber`, `pymupdf` (fitz)
  - Text processing: `nltk`, `spacy` (for structure detection)
  - Chunking: Custom chunking utilities with configurable context sizes
- **Storage**: PostgreSQL 15+ with:
  - Relational edge table (src_id, dst_id, relation_type) for reference relationships
  - JSONB columns for metadata (flexible, queryable)
  - Bitemporal fields (`valid_from`, `valid_to`) for version history and time-travel queries
  - Partial indexes on current data (`WHERE valid_to IS NULL`) for performance
  - Row-Level Security (RLS) policies for tenant isolation (see CL-031 and FR-030 in master spec for security guarantee that User A can NEVER see User B's data under ANY circumstances)
  - **Security Testing**: Automated security tests for cross-tenant data access prevention per FR-019A - verify User A cannot access User B's references, research documents, or extracted data under ANY circumstances, including bugs, misconfigured queries, malicious input, and missing tenant context
- **LLM Services**: Required for automated research loop (extraction, validation, questioning)
- **Error Tracking**: Sentry (free tier) for error monitoring
- **Testing**: pytest

## API Endpoints

### Search and Retrieval APIs

- **`GET /references/search`**: Search references
  - **Query Parameters**: `q=...&type=Act|RG|Case&effective_date_from=...&effective_date_to=...&regulatory_body=...`
  - **Response**: Ranked search results with metadata (type, effective dates, version, source URL) and preview text

- **`GET /references/{id}`**: Retrieve full reference
  - **Response**: Full reference details including metadata, version history, and full text content

- **`GET /pinpoints/{reference_id}`**: Retrieve all pinpoints for a reference
  - **Response**: All pinpoints with section numbers, text excerpts, and navigation paths

- **`GET /references/{id}/versions`**: Get version history
  - **Response**: All versions with effective date ranges, change summaries, and links between versions

- **`GET /references/{id}?as_of=YYYY-MM-DD`**: Time-travel query
  - **Response**: Version applicable on specified date

### RAG-Style Retrieval API

- **`POST /references/rag-retrieve`**: RAG-optimized retrieval for AI models
  - **Request**: `{ query, context?, max_results? }`
  - **Response**: References in formats suitable for embedding in prompts with structured metadata and citation-ready text

### Data Scraping APIs

- **`POST /scraping/process-pending`**: Process all pending sources from `human_provided_new_sources.md`
  - **Request**: `{ force?: boolean }` (force reprocessing of failed sources)
  - **Response**: `{ job_id, sources_processed, sources_succeeded, sources_failed }`
  - **Async**: Returns 202 Accepted with job_id for long-running operations

- **`GET /scraping/jobs/{job_id}`**: Get status of scraping job
  - **Response**: `{ job_id, status: "queued"|"running"|"completed"|"failed", sources_processed, sources_succeeded, sources_failed, errors: [...] }`

- **`POST /scraping/scrape-source`**: Manually trigger scraping for a specific source
  - **Request**: `{ url, title?, type?, regulatory_body?, priority? }`
  - **Response**: `{ job_id, source_id, status }`

### Data Cleaning APIs

- **`POST /cleaning/clean-document`**: Clean a specific document for LLM processing
  - **Request**: `{ document_path, chunk_size?, model_compatibility? }`
  - **Response**: `{ job_id, document_id, chunks_created, status }`
  - **Note**: Chunking only occurs if document exceeds 60,000 tokens (models handle this easily, so most documents won't be chunked)

- **`GET /cleaning/jobs/{job_id}`**: Get status of cleaning job
  - **Response**: `{ job_id, status: "queued"|"running"|"completed"|"failed", chunks_created, chunk_metadata: [...], errors: [...] }`

- **`POST /cleaning/batch-clean`**: Batch clean multiple documents
  - **Request**: `{ document_paths: [...], chunk_size?, model_compatibility? }`
  - **Response**: `{ job_id, documents_processed, chunks_created, status }`

## Module Dependencies

### Depends On

- **Document Parsing Libraries**: PDF (pypdf, pdfplumber, pymupdf), HTML (BeautifulSoup4, lxml), structured data formats
- **Scraping Libraries**: HTTP clients (requests, httpx), web scraping (BeautifulSoup4, selenium, playwright), RSS parsing (feedparser), audio transcription (whisper or cloud APIs)
- **Cleaning Libraries**: PDF to text (pypdf, pdfplumber, pymupdf), text processing (nltk, spacy), custom chunking utilities
- **LLM Services**: Optional for automated classification and extraction (via OpenRouter)
- **Storage Systems**: PostgreSQL (all data storage including relationships via relational edge table + JSONB, bitemporal fields for version history, RLS for tenant isolation)
- **Background Jobs**: RQ (Redis Queue) for async scraping and cleaning jobs

### Used By

- **Compute Engine**: Rule-to-reference lookups in provenance chains
- **Advice Engine**: Regulatory requirement lookups for compliance evaluation
- **LLM Orchestrator**: Citation generation and context enhancement
- **Rules Authoring System**: Citing authoritative sources when authoring rules

## Integration Points

### Module-to-Module Integration

- **Compute Engine → References & Research Engine**: 
  - Rule-to-reference lookups via `GET /references/{id}` and `GET /pinpoints/{reference_id}`
  - Used for building provenance chains

- **Advice Engine → References & Research Engine**: 
  - Regulatory requirement lookups via `GET /references/search`
  - Used for compliance verification

- **LLM Orchestrator → References & Research Engine**: 
  - Reference retrieval via RAG-style API for citation generation and context enhancement

- **Rules Authoring System → References & Research Engine**: 
  - Reference search and retrieval for citing authoritative sources

### External Integration

- **Document Sources → References & Research Engine**: 
  - Ingestion pipeline receives documents from regulatory body websites, legal databases, or manual uploads

- **LLM Services → References & Research Engine**: 
  - Optional integration with external LLM services for document classification and metadata extraction during ingestion

## Technical Implementation Details

### Data Scraping Submodule

- **Source Monitoring**: Monitors `Research/human_provided_new_sources.md` for sources with status "Pending"
- **Scraping Methods**: Attempts multiple methods in order:
  1. Direct HTTP/HTTPS download (`requests`, `httpx`)
  2. RSS feed discovery and parsing (`feedparser`)
  3. API endpoint detection and access
  4. Headless browser rendering (`selenium`, `playwright`) for JavaScript-heavy sites
  5. Custom scraping method creation and logging for future reference
- **Audio Handling**: For podcasts/webinars/interviews:
  - Attempts to find transcripts via RSS feeds or external sources
  - If transcripts unavailable, generates transcripts using transcription services (`whisper` or cloud APIs)
  - Stores both audio and transcript files
- **Adaptive Scraping**: Creates new scraping methods when standard methods fail, logs approach for future reference
- **Progress Tracking**: Updates `RESEARCH_PROGRESS.md` and `human_provided_new_sources.md` after each scraping operation
- **Error Handling**: Logs failed attempts in `human_provided_new_sources.md` Failed Downloads section with error details, methods attempted, retry count

### Data Cleaning Submodule

- **PDF to Text Conversion**: Converts PDFs to clean text using `pypdf`, `pdfplumber`, or `pymupdf`
- **Text Cleaning**: Removes headers, footers, page numbers, formatting artifacts while preserving document structure (sections, paragraphs)
- **Chunking Strategy**: 
  - **No unnecessary chunking**: Modern LLM models can handle 60,000+ input tokens easily. Documents should only be chunked if they exceed model context limits (typically 60,000+ tokens).
  - Chunking only when necessary: Documents exceeding 60,000 tokens are chunked to fit within model context windows
  - Configurable chunk sizes for specific model requirements (default: 60,000 tokens to avoid unnecessary splitting)
  - Respects document boundaries (sections, paragraphs) - does not split mid-sentence or mid-paragraph unless necessary
  - Dynamic chunk combination/splitting based on target model requirements
- **Structured Data Preservation**: Preserves tables, lists, code in LLM-readable formats (markdown tables, formatted lists) with context markers
- **Chunk Metadata**: Stores chunk ID, position in document, size (tokens/characters), model compatibility information
- **Progress Tracking**: Updates `RESEARCH_PROGRESS.md` after cleaning operations, marking documents as extraction-ready

### Ingestion Pipeline

- **Document Formats**: PDF, HTML, CSV, YAML, plain text, structured data (after scraping and cleaning)
- **Automatic Classification**: Document type (Act, Regulation, Guidance, Case) with confidence thresholds
- **Metadata Extraction**: Title, type, effective dates, source URL, publication dates, regulatory body
- **Pinpoint Extraction**: Section numbers, paragraph identifiers, clause references
- **Manual Review**: Flag documents with low confidence or extraction failures

### Research Folder Architecture

The system uses a hierarchical folder structure in `Research/` to organize reference materials by authority, document type, and version:

```
Research/
├── 01-primary-authorities/          # Authoritative legal/regulatory sources
│   ├── legislation/                  # Acts of Parliament
│   │   ├── corporations-act-2001/
│   │   │   ├── v2024-01-01/
│   │   │   │   ├── corporations-act-2001-2024-01-01.pdf
│   │   │   │   └── metadata.yaml
│   │   │   └── v2023-07-01/
│   │   ├── income-tax-assessment-act-1997/
│   │   └── superannuation-industry-supervision-act-1993/
│   │
│   ├── regulations/                  # Statutory Rules/Regulations
│   │   ├── corporations-regulations-2001/
│   │   └── superannuation-industry-supervision-regulations-1994/
│   │
│   ├── asic/                         # ASIC Regulatory Guides & Rulings
│   │   ├── regulatory-guides/
│   │   │   ├── RG-175/
│   │   │   │   ├── v2024-03-15/
│   │   │   │   └── v2023-01-01/
│   │   │   ├── RG-146/
│   │   │   └── RG-250/
│   │   ├── class-orders/
│   │   └── information-sheets/
│   │
│   ├── ato/                          # ATO Rulings & Determinations
│   │   ├── tax-determinations/
│   │   ├── tax-rulings/
│   │   ├── practice-statements/
│   │   └── interpretative-decisions/
│   │
│   ├── apra/                         # APRA Prudential Standards & Guidance
│   │   ├── prudential-standards/
│   │   └── guidance-notes/
│   │
│   └── case-law/                     # Court decisions & tribunal rulings
│       ├── high-court/
│       ├── federal-court/
│       ├── administrative-appeals-tribunal/
│       └── state-courts/
│
├── 02-secondary-sources/             # Educational & interpretive materials
│   ├── educational/
│   │   ├── lecture-notes/
│   │   │   ├── financial-planning-fundamentals/
│   │   │   ├── taxation-principles/
│   │   │   └── superannuation-law/
│   │   ├── course-materials/
│   │   └── textbooks/
│   │
│   ├── professional-guidance/        # FPA, AFA, etc.
│   │   ├── fpa/
│   │   └── afa/
│   │
│   └── industry-publications/        # Industry journals, articles
│
├── 03-media-transcripts/             # Podcasts, webinars, interviews
│   ├── podcasts/
│   │   ├── financial-planning-weekly/
│   │   └── tax-talk/
│   ├── webinars/
│   └── interviews/
│
├── 04-structured-data/              # CSV, YAML, JSON data files
│   ├── assumptions/
│   │   ├── tax-rates/
│   │   ├── superannuation-contribution-caps/
│   │   └── age-pension-rates/
│   ├── rules/
│   └── client-outcome-strategies/
│
├── 05-raw-documents/                 # Unprocessed originals (before chunking)
│   └── [same structure as above, but raw files]
│
├── 99-manual-review/                 # Documents flagged for manual review
│   ├── low-confidence-classification/
│   ├── extraction-errors/
│   └── duplicates/
│
├── RESEARCH_PROGRESS.md              # Tracks ingestion progress and status
└── human_provided_new_sources.md     # Human-curated list of sources to integrate
```

**Folder Discovery Priority**: The ingestion pipeline scans folders in priority order (`01-primary-authorities/` first, then `02-secondary-sources/`, etc.) and applies source-specific primers based on folder path and document type.

**Version Management**: Each document can have multiple versions stored in `vYYYY-MM-DD/` folders, with each version containing the document file and optional `metadata.yaml` for effective dates, source URLs, and other metadata.

**Research Progress Tracking**: `Research/RESEARCH_PROGRESS.md` maintains a comprehensive log of all ingested documents, extraction status, coverage metrics, and research checklist validation progress.

**Human-Provided Sources**: `Research/human_provided_new_sources.md` contains URLs, document references, and notes about sources that should be integrated. The ingestion pipeline monitors this file and attempts to download and integrate listed sources into the appropriate subfolders.

### Storage Architecture

- **Entity ID Generation**:
  - **Format**: Two-letter prefix + ULID/hash (e.g., `RE-01HFSZ2R2Y1G2M5D8C9QWJ7K4T`)
  - **Prefixes**: `RE-` (Reference), `FN-` (Finding), `RQ-` (Research Question), `VD-` (Verdict)
  - **Collision Handling**: ULID/hash ensures global uniqueness. ULID's inherent uniqueness properties (128-bit entropy, timestamp-based ordering) provide collision-free IDs without explicit collision detection logic. Database unique constraints on entity ID columns provide defense-in-depth.
  - **Implementation**: Use Python `ulid` library or equivalent for ULID generation. Prefix validation ensures correct entity type association.
  - **Reference**: `specs/001-master-spec/canonical_data_model.md` (Canonical ID Prefix Reference section), `.specify/memory/constitution.md` (Canonical ID Prefix Reference section)

- **Provenance Storage Design**:
  - **Relational Edge Table**: `provenance_edges` table stores relationships as rows (edges) with:
    - `src_id` (source entity ID, e.g., `RE-...`)
    - `dst_id` (destination entity ID, e.g., `RE-...` for supersedes/amends relationships)
    - `relation_type` (relationship type: `SUPERSEDES`, `AMENDS`, `CITES`, `CONFLICTS_WITH`, etc.)
    - `created_at` (timestamp for audit trail)
    - `tenant_id` (for tenant isolation, NULL for global entities like References)
  - **JSONB Metadata**: Flexible metadata stored in JSONB columns on entity tables for queryable, extensible attributes (e.g., reference pinpoints, finding confidence scores, extraction metadata). Relationships are stored as rows; attributes are stored as JSONB.
  - **Architecture Decision**: Relationships stored as relational rows (edges) enable efficient graph traversal, referential integrity, and query optimization. JSONB used only for entity attributes, not relationships.
  - **Reference**: `Design_docs/final_design_questions.md` Section 4

- **Bitemporal Fields & Time-Travel**:
  - **Fields**: All temporal entities have `valid_from` (timestamp) and `valid_to` (timestamp, NULL for current) fields
  - **Default Filter for Current Rows**: `WHERE valid_to IS NULL` - this is the standard filter for querying "current" or "active" entities
  - **Time-Travel Queries**: Use `as_of` date parameter. System selects rows where `as_of` falls within `valid_from` and `valid_to` (or `valid_to IS NULL`). Query pattern: `WHERE valid_from <= as_of AND (valid_to IS NULL OR valid_to > as_of)`
  - **Partial Indexes**: Indexes on current data only (`WHERE valid_to IS NULL`) for performance optimization. These indexes dramatically improve query performance for common "current state" queries.
  - **Entities with Bitemporal Fields**: References, Findings, Research Questions, Verdicts
  - **Reference**: `Design_docs/final_design_questions.md` Section 4, `specs/001-master-spec/master_spec.md` CL-011, CL-012

### Version Management

- **Version History**: Track effective date ranges, change summaries, relationships (supersedes, amends) using bitemporal fields
- **Time-Travel Queries**: Retrieve versions applicable at specific dates via `as_of` parameter using bitemporal query pattern
- **Version Linking**: Automatic linking of versions (supersedes, amends relationships) via relational edge table

### RAG-Style Retrieval

- **Optimization**: Formats suitable for AI model embedding
- **Structured Metadata**: Citation-ready text with reference identifiers
- **Context Enhancement**: Include surrounding context and relevance scores

### Data Quality

- **Quality Standards**: Completeness, accuracy, context, traceability, consistency, currency
- **Validation**: Schema validation before storage
- **Duplicate Detection**: Based on title, type, and effective dates
- **Audit Logs**: Track all ingestion, updates, version changes, and access patterns

### Fully-Automated Research Loop

The References & Research Engine implements a **fully-automated research loop** that continuously learns from reference materials, improves understanding, and checks its own work without human reviewers. See `specs/003-references-research-engine/research_guidance/fully-automated-research-loop.md` for detailed conceptual overview.

**Knowledge Extraction Taxonomy**: The research loop extracts knowledge according to the comprehensive taxonomy defined in `specs/003-references-research-engine/research_guidance/research_knowledge_map.md`. This knowledge map describes the full landscape of knowledge categories (System Rules, Calculations, Client Context Variables, Eligibility Tests, Client Outcome Strategies, Exceptions & Edge Cases, Interpretation Logic, Risk Frameworks, Financial Behaviours, Advice Construction Patterns, Red Flags & Compliance Tests, Canonical Case Types, Misconceptions, Values & Preferences, Goal Taxonomy) and maps each to canonical types (RULE, ASSUMPTION, ADVICE GUIDANCE, CLIENT OUTCOME STRATEGY, FINDING). The knowledge map expands subcategories and extraction targets without altering canonical types, ensuring consistent knowledge extraction across all research phases.

**Loop Stages**:

1. **Auto-Extraction**
   - Automatically reads all available reference materials (legislation, ASIC regulatory guides, lecture notes, articles, podcasts)
   - Extracts potential facts, rules, definitions, limits, and examples
   - Tags each finding with source pinpoint, confidence score, date, and version

2. **Auto-Questioning**
   - Creates research questions when information is uncertain, contradictory, incomplete, or out-of-date
   - Stores questions and schedules them for re-reading passes
   - Examples: "Does this rule still apply after 1 July 2025?", "Is there a conflict between RG 175 and the Corporations Act?"

3. **Auto-Validation**
   - Runs built-in validation tests:
     - **Pinpoint check**: Confirm cited paragraph exists
     - **Version check**: Confirm rule matches right time period
     - **Conflict check**: Detect contradictory statements between sources
     - **Completeness check**: Ensure each topic has definition, exceptions, limits, and timing
     - **Simulation check**: Run small examples to verify logical behavior
   - Findings that pass all checks move forward; others trigger re-reading or new questions

4. **Auto-Curation**
   - Ranks and merges validated findings
   - Keeps most recent, highest-confidence version
   - Discards duplicates or outdated findings
   - Publishes findings as "Approved" when confidence is high and no questions remain

**Trust and Confidence Scoring**:

Each finding receives a trust score (0-100) based on:
- Strength and number of evidence pinpoints
- Agreement between multiple models or sources
- Recency of the material
- Validation pass rate and simulation success

| Score | Status | Action |
|-------|---------|--------|
| ≥85 | Approved | Ready for Advice/Compute engines |
| 60–84 | Needs work | Keep looping until confidence improves |
| <60 | Rejected | Discarded or re-read next cycle |

**Continuous Learning**:

After every loop iteration:
- Updates trust scores and merges duplicate findings
- Re-reads areas linked to open questions
- Generates "delta report" summarizing changes since last snapshot
- Publishes new verified snapshot when confidence is stable and coverage is high

**Safety and Quality Controls**:

- **Fail-closed**: If a rule cannot be verified, it is excluded
- **Quarantine**: Low-confidence or conflicting items isolated until resolved
- **Drift alarm**: New source versions that change previously approved rules trigger comparison and flagging
- **Kill switch**: If overall confidence in a topic drops below target, previous verified snapshot remains in use

**Research Checklist Validation**:

The system validates coverage against the comprehensive research checklist (`specs/004-advice-engine/checklists/Research_checklist_do_we_understand_these.md`) to ensure:
- **Calculation Types**: All required calculation functions (CAL-*) are understood and extractable
- **Assumption Types**: All assumption categories (ASM-*) are identified and versioned
- **Edge Cases**: Edge cases (EDGE-*) are detected and documented
- **Australia-Specific Considerations**: All Australian financial system peculiarities are captured

**Success Criteria**:

- ≥95% of priority topics approved with trust ≥85
- 0 unresolved "high-priority" questions before publishing
- 100% pinpoint and version verification pass rate
- Simulation and self-consistency tests ≥99% pass rate
- Less than 1% of findings marked "contested" at publication time

**Finding Record Structure**:

Each finding record includes:
- ID and topic name
- Normalized rule text
- Source and pinpoint reference
- Version and effective date
- Trust score and validator results
- Linked open questions (if any)
- Current status: Draft → Validated → Approved/Rejected

## Implementation Phases

### Phase 1: Reference Storage (Week 1)

**Tasks**:
1. **Entity ID Generation System**
   - Implement entity ID generation utility using Python `ulid` library
   - Implement prefix validation (RE-, FN-, RQ-, VD-)
   - Implement ID format validation and parsing
   - Add database unique constraints on entity ID columns for defense-in-depth collision prevention
   - Reference: `specs/001-master-spec/canonical_data_model.md` (Canonical ID Prefix Reference section), `.specify/memory/constitution.md` (Canonical ID Prefix Reference section)

2. **Data Model Design**
   - Design Reference data model with bitemporal fields (`valid_from`, `valid_to`)
   - Implement Reference CRUD operations
   - Implement default filter for current rows (`WHERE valid_to IS NULL`)
   - Create partial indexes on current data (`WHERE valid_to IS NULL`) for performance
   - Reference: `Design_docs/final_design_questions.md` Section 4

3. **Provenance Storage Implementation**
   - Implement `provenance_edges` table schema (src_id, dst_id, relation_type, created_at, tenant_id)
   - Implement JSONB metadata columns on entity tables for attributes
   - Implement provenance link creation and querying utilities (for supersedes, amends, conflicts relationships)
   - Ensure relationships stored as rows (edges), attributes stored as JSONB
   - Reference: `Design_docs/final_design_questions.md` Section 4

4. **Bitemporal Fields & Time-Travel**
   - Implement bitemporal fields (`valid_from`, `valid_to`) on all temporal entities
   - Implement time-travel query utilities with `as_of` date support
   - Implement query pattern: `WHERE valid_from <= as_of AND (valid_to IS NULL OR valid_to > as_of)`
   - Create partial indexes on current data for performance optimization
   - Reference: `Design_docs/final_design_questions.md` Section 4, `specs/001-master-spec/master_spec.md` CL-011, CL-012

5. **Version Tracking and History**
   - Implement version tracking using bitemporal fields
   - Implement version history queries with time-travel support
   - Implement pinpoint extraction and storage (JSONB metadata)

**Deliverables**:
- Entity ID generation system implemented with ULID support
- Reference data model implemented with bitemporal fields
- Provenance storage implemented (relational edge table + JSONB)
- Bitemporal time-travel queries functional
- CRUD operations functional
- Version tracking working with time-travel support

### Phase 2: Basic Ingestion Pipeline (Week 2)

**Tasks**:
1. **Research Folder Architecture Setup**
   - Create hierarchical folder structure in `Research/` directory:
     - `01-primary-authorities/` (legislation, regulations, asic, ato, apra, case-law)
     - `02-secondary-sources/` (educational, professional-guidance, industry-publications)
     - `03-media-transcripts/` (podcasts, webinars, interviews)
     - `04-structured-data/` (assumptions, rules, client-outcome-strategies)
     - `05-raw-documents/` (unprocessed originals)
     - `99-manual-review/` (low-confidence, extraction-errors, duplicates)
   - Create `Research/RESEARCH_PROGRESS.md` template for tracking ingestion progress
   - Create `Research/human_provided_new_sources.md` template for human-curated source list
   - Implement folder discovery system that scans folders in priority order
   - Implement source-specific primer selection based on folder path and document type

2. **Document Ingestion**
   - Build document ingestion pipeline (PDF, HTML, structured data)
   - Implement document parsing for multiple formats
   - Set up manual review workflow for low-confidence classifications
   - Implement batch ingestion job processing using RQ (Redis Queue) workers
   - Implement ingestion job idempotency: `hash(source_file_path + file_checksum + tenant_id)` to prevent duplicate processing
   - Implement ingestion job status tracking (queued, processing, completed, failed)
   - Implement ingestion job result storage and retrieval (minimum 7 days retention)
   - Set up ingestion job retry/backoff policy: exponential backoff (1s initial, 30s max, 3 retries) for transient failures
   - Implement dead-letter queue for failed ingestion jobs with replay capability
   - Implement version folder detection (`vYYYY-MM-DD/`) and metadata.yaml parsing
   - Implement automatic document placement in appropriate folder structure based on classification

3. **Data Scraping Submodule Implementation**
   - Implement parser for `Research/human_provided_new_sources.md` that monitors for "Pending" status sources
   - Implement multiple scraping methods with fallback chain:
     - Direct HTTP/HTTPS download using `requests` and `httpx` (async)
     - RSS feed discovery and parsing using `feedparser`
     - API endpoint detection and access
     - Headless browser rendering using `selenium` or `playwright` for JavaScript-heavy sites
     - Custom scraping method creation and logging for future reference
   - Implement audio source handling:
     - RSS feed transcript discovery
     - External transcript source detection
     - Audio transcription using `whisper` or cloud transcription APIs if transcripts unavailable
     - Storage of both audio and transcript files
   - Implement adaptive scraping: create new methods when standard methods fail, log approach
   - Implement scraping job tracking with status (queued, running, completed, failed)
   - Implement progress tracking: update `RESEARCH_PROGRESS.md` and `human_provided_new_sources.md` after each operation
   - Implement error logging: update `human_provided_new_sources.md` Failed Downloads section with error details, methods attempted, retry count
   - Implement automatic folder placement based on classification
   - Implement scraping job idempotency: `hash(url + title + tenant_id)` to prevent duplicate scraping
   - Implement scraping job retry/backoff: exponential backoff (1s initial, 30s max, 3 retries) for transient failures
   - Reference: `specs/003-references-research-engine/spec_003_references_research_engine.md` FR-027 through FR-032, User Story 4

4. **Data Cleaning Submodule Implementation**
   - Implement PDF to text conversion using `pypdf`, `pdfplumber`, or `pymupdf`
   - Implement text cleaning: remove headers, footers, page numbers, formatting artifacts
   - Implement structure preservation: maintain document structure (sections, paragraphs) during cleaning
   - Implement chunking system:
     - **No unnecessary chunking**: Only chunk documents that exceed 60,000 tokens (modern models handle this easily)
     - Default chunk size: 60,000 tokens (to avoid unnecessary splitting)
     - Configurable chunk sizes for specific model requirements
     - Document boundary respect (sections, paragraphs) - no mid-sentence/mid-paragraph splits unless necessary
     - Dynamic chunk combination/splitting based on target model requirements
   - Implement structured data preservation: convert tables, lists, code to LLM-readable formats (markdown tables, formatted lists) with context markers
   - Implement chunk metadata storage: chunk ID, position in document, size (tokens/characters), model compatibility information
   - Implement cleaning job tracking with status (queued, running, completed, failed)
   - Implement progress tracking: update `RESEARCH_PROGRESS.md` after cleaning operations, mark documents as extraction-ready
   - Implement cleaning job idempotency: `hash(document_path + file_checksum + chunk_config)` to prevent duplicate cleaning
   - Implement batch cleaning support for multiple documents
   - Reference: `specs/003-references-research-engine/spec_003_references_research_engine.md` FR-033 through FR-038, User Story 5

5. **Human-Provided Sources Integration**
   - Implement parser for `human_provided_new_sources.md` with clear instructions for when to use URLs vs direct file placement
   - Integrate with Data Scraping Submodule for automatic source download
   - Implement automatic classification and folder placement for downloaded sources
   - Implement progress tracking in `RESEARCH_PROGRESS.md` when sources are integrated
   - Implement status updates in `human_provided_new_sources.md` (Pending → Processing → Completed/Failed)
   - Implement notification/alert when new sources are added to `human_provided_new_sources.md`
   - Reference: `specs/003-references-research-engine/spec_003_references_research_engine.md` FR-039, User Story 6

**Deliverables**:
- Research folder architecture created and documented
- RESEARCH_PROGRESS.md and human_provided_new_sources.md templates created with clear instructions
- Folder discovery system operational with priority-based scanning
- Data Scraping Submodule operational with multiple methods and adaptive scraping
- Data Cleaning Submodule operational with PDF conversion, text cleaning, and LLM-ready chunking
- Basic ingestion pipeline operational (processes cleaned documents)
- Multiple document formats supported
- Batch ingestion jobs functional with async processing
- Ingestion job idempotency and retry handling implemented
- Version folder detection and metadata.yaml parsing implemented
- Human-provided sources integration functional with automatic scraping and cleaning

### Phase 3: Search and Retrieval (Week 3)

**Tasks**:
1. **Search APIs**
   - Implement search API (`GET /references/search`)
   - Implement retrieval API (`GET /references/{id}`)
   - Implement pinpoint retrieval API (`GET /pinpoints/{reference_id}`)
   - Implement time-travel queries (`as_of` date support)

**Deliverables**:
- Search and retrieval APIs functional
- Time-travel queries working
- OpenAPI schema generated for all endpoints (`specs/001-master-spec/contracts/references-research-engine.openapi.yaml`)
- API versioning implemented (`/api/v1/...`)

### Phase 4: Fully-Automated Research Loop (Week 4)

**Tasks**:
1. **Auto-Extraction Engine**
   - Implement automatic document reading and extraction from all reference materials
   - **Knowledge Taxonomy**: Extract knowledge according to the 15 knowledge categories defined in `specs/003-references-research-engine/research_guidance/research_knowledge_map.md`:
     - System Rules (RULE) - tax rates, CGT rules, contribution caps, super preservation rules, etc.
     - Calculations (RULE with subtype "Calculation") - net income formulas, offsets sequencing, CGT discount logic, etc.
     - Client Context Variables (ASSUMPTION) - personal, financial, and behavioural inputs
     - Eligibility Tests (RULE) - work test, bring-forward, catch-up concessional, etc.
     - Client Outcome Strategies (CLIENT OUTCOME STRATEGY) - wealth-building, tax, retirement, liquidity, structural, insurance strategies
     - Exceptions & Edge Cases (RULE) - transitional rules, grandfathering, anti-avoidance, timing quirks
     - Interpretation Logic (ADVICE GUIDANCE) - semantic patterns for Advice Engine
     - Risk Frameworks (ADVICE GUIDANCE) - investment, personal, and advice risks
     - Financial Behaviours & Psychology (ASSUMPTION or ADVICE GUIDANCE) - spending habits, biases, emotional patterns
     - Advice Construction Patterns (ADVICE GUIDANCE) - metalogic for reasoning frameworks
     - Red Flags & Compliance Tests (RULE or ADVICE GUIDANCE) - best interest duty, Standard 3 conflicts, etc.
     - Canonical Case Types (ASSUMPTION or ADVICE GUIDANCE) - client archetypes
     - Misconceptions, Mistakes, Failure Modes (ADVICE GUIDANCE or FINDING) - common errors and failure patterns
     - Values & Preferences Logic (ASSUMPTION) - ESG preference, simplicity preference, etc.
     - Goal Taxonomy (ASSUMPTION or ADVICE GUIDANCE) - all financial goals
   - Extract facts, rules, definitions, limits, and examples according to knowledge map taxonomy
   - Tag findings with source pinpoint, confidence score, date, and version
   - Map extracted knowledge to canonical types per knowledge map (RULE, ASSUMPTION, ADVICE GUIDANCE, CLIENT OUTCOME STRATEGY, FINDING)
   - Implement extraction for legislation, ASIC regulatory guides, lecture notes, articles, and podcasts

2. **Auto-Questioning System**
   - Implement research question generation for uncertain, contradictory, incomplete, or out-of-date information
   - Store questions and schedule re-reading passes
   - Implement question prioritization (high-priority vs normal)

3. **Auto-Validation System**
   - Implement pinpoint check (verify cited paragraph exists)
   - Implement version check (verify rule matches time period)
   - Implement conflict check (detect contradictory statements)
   - Implement completeness check (ensure definition, exceptions, limits, timing)
   - Implement simulation check (run small examples for logical verification)
   - Implement validation result tracking and scoring

4. **Auto-Curation System**
   - Implement finding ranking and merging
   - Implement duplicate detection and removal
   - Implement approval workflow (Draft → Validated → Approved/Rejected)
   - Implement trust score calculation (0-100) based on evidence strength, source agreement, recency, validation pass rate

5. **Continuous Learning Loop**
   - Implement trust score updates after each loop iteration
   - Implement delta report generation (summarize changes since last snapshot)
   - Implement verified snapshot publishing when confidence is stable
   - Implement re-reading scheduler for areas with open questions

6. **Safety and Quality Controls**
   - Implement fail-closed behavior (exclude unverifiable rules)
   - Implement quarantine system for low-confidence/conflicting items
   - Implement drift alarm (detect and flag changes in approved rules)
   - Implement kill switch (revert to previous snapshot if confidence drops)

7. **Research Checklist Integration**
   - Integrate validation against research checklist (`specs/004-advice-engine/checklists/Research_checklist_do_we_understand_these.md`)
   - Implement coverage tracking for calculation types (CAL-*)
   - Implement coverage tracking for assumption types (ASM-*)
   - Implement edge case detection (EDGE-*)
   - Implement Australia-specific consideration validation
   - Generate coverage reports showing which checklist items are understood/extracted

8. **Canonical Calculation List Generation**
   - Build comprehensive canonical list of all calculation functions required by Compute Engine from extracted research findings
   - Extract calculation types from all reference materials (legislation, ASIC guides, ATO rulings, lecture notes, articles)
   - Categorize calculations by domain (tax, superannuation, retirement, loans, etc.)
   - **CRITICAL**: Use Compute Engine requirements context to guide extraction and validate completeness
   - For each calculation, extract ALL required fields per Compute Engine requirements context:
     - Calculation function identifier (CAL-* format)
     - Calculation name and description
     - Input parameters and data types (with validation rules, units, examples)
     - Output format and units (with precision, rounding rules)
     - Formula or algorithm description (detailed enough for implementation)
     - Edge cases and exceptions (with handling instructions)
     - Regulatory sources (References with pinpoints, effective dates)
     - Effective date ranges and version information
     - Rounding rules and precision requirements (method, precision, when, tolerance)
     - Dependencies (other calculations, assumptions, rules)
     - Testing requirements (test cases, golden dataset references)
   - **Completeness Validation**: After extraction, validate each calculation against Compute Engine requirements context completeness checklist
   - Calculate completeness score (0-100%) for each calculation based on required fields present
   - Generate structured output file: `Research/canonical_calculations.yaml` (or JSON) with complete calculation specifications
   - **Incomplete Calculation Handling**: Flag calculations with insufficient information (completeness_score < 100%) for further research
     - Document missing fields in `missing_fields` array
     - Generate refinement requests for next research loop iteration
     - Prioritize incomplete calculations based on Compute Engine implementation order
   - Validate completeness against research checklist calculation types
   - Export canonical list to Compute Engine for function implementation, script generation, and data schema creation
   - **Relationship to Explanations Repository**: The canonical list serves as the authoritative source specification that feeds into Compute Engine Phase 7 Explanation Repository. Explanations derive from canonical list data (formulas, regulatory sources, edge cases, rounding rules) and add implementation-specific details (rationale, testing approach, code references). Each explanation MUST reference its canonical source via `canonical_calculation_id` field.
   - Update canonical list as new research findings are validated and approved
   - **Versioning**: When canonical list is updated, Compute Engine Explanation Repository should be notified to flag affected explanations for review
   - Reference: This canonical list feeds directly into Compute Engine Phase 1 implementation tasks (calculation function generation) and Phase 7 (explanation repository bootstrap)

9. **LLM-Assisted Research**
   - **CRITICAL**: Load Compute Engine requirements context (`specs/003-references-research-engine/research_guidance/compute-engine-requirements-context.md`) BEFORE starting research extraction
   - **CRITICAL**: Load knowledge taxonomy (`specs/003-references-research-engine/research_guidance/research_knowledge_map.md`) to guide extraction of all knowledge categories and their mapping to canonical types
   - Integrate external LLM research using `primer_external_research_v1a.md` from `specs/005-llm-orchestrator/primers-prompts/` for structured knowledge extraction
   - **Primer Enhancement**: Ensure `primer_external_research_v1a.md` includes or loads Compute Engine requirements context and knowledge map to guide extraction from the FIRST iteration
   - Implement primer loading system that combines:
     - Base primer (`primer_external_research_v1a.md`)
     - Compute Engine requirements context (for calculation function extraction)
     - Research knowledge map (`specs/003-references-research-engine/research_guidance/research_knowledge_map.md`) - for knowledge category taxonomy and canonical type mapping
     - Research checklist (`specs/004-advice-engine/checklists/Research_checklist_do_we_understand_these.md`)
   - **Iterative Priming**: Each research loop iteration should re-load and apply Compute Engine requirements context and knowledge map to ensure extraction completeness and correct canonical type mapping
   - **Note**: The primer provides domain knowledge and extraction guidance. Data schemas are determined during the research phase based on extracted content, not predefined in the primer. The knowledge map expands subcategories and extraction targets without altering canonical types.
   - Implement structured output parsing from LLM research (References, Rules, Assumptions, Advice Guidance, Client Outcome Strategies) according to knowledge map taxonomy
   - **Schema Definition**: Define data schemas during research phase based on actual extracted content patterns and requirements, guided by Compute Engine requirements context and knowledge map canonical type mappings
   - Integrate LLM extraction into automated loop (use LLM for initial extraction, then validate against Compute Engine requirements and knowledge map taxonomy)
   - **Completeness Validation**: After each extraction iteration, validate extracted knowledge against both Compute Engine requirements context (for calculations) and knowledge map taxonomy (for all knowledge categories), flagging incomplete entries for next iteration

10. **Research Progress Tracking**
   - Implement automatic updates to `Research/RESEARCH_PROGRESS.md` after each ingestion batch
   - Track document counts by folder, document type, and regulatory body
   - Track extraction status (pending, processing, completed, failed, manual-review)
   - Track research checklist coverage metrics (calculation types, assumptions, edge cases)
   - Track calculation function completeness scores (0-100% per calculation)
   - Track incomplete calculations with missing fields for iterative refinement
   - Generate summary statistics (total documents, extraction success rate, coverage percentage, completeness scores)
   - Implement delta reporting (new documents since last update, changed documents, removed documents, completeness improvements)

11. **Iterative Research Priming**
   - Implement research iteration tracking that includes Compute Engine requirements context in each loop
   - Before each research loop iteration:
     - Load Compute Engine requirements context
     - Identify incomplete calculation functions from previous iterations
     - Generate targeted extraction prompts using requirements context for missing fields
     - Apply requirements context to LLM prompts for focused extraction
   - After each iteration:
     - Validate extracted data against Compute Engine requirements context
     - Calculate completeness scores for each calculation function (0-100%)
     - Generate refinement requests for incomplete calculations with specific missing fields
     - Update prompts for next iteration with targeted prompts for missing information
   - Ensure requirements context is applied from FIRST iteration, not just refinement passes
   - Track iteration count per calculation function and refinement request history
   - Prioritize incomplete calculations based on Compute Engine implementation order

12. **Research Refinement API**
   - Implement `POST /research/refine` endpoint for structured refinement requests from Compute Engine and Advice Engine
   - Request format: `{ calculation_id?, schema_suggestion?, missing_fields: [...], specific_questions: [...], priority: high|normal, iteration_number }`
   - **Schema Feedback Support** (FR-SCHEMA-02): Accept `schema_suggestion` payload for structural schema feedback:
     - `missing_relation`: Missing relationship between canonical types
     - `suggested_field`: Suggested new field for existing schema
     - `missing_provenance_role`: Missing provenance role type
     - `awkward_join`: Awkward join pattern requiring schema improvement
     - `excessive_jsonb`: Excessive JSONB usage indicating missing relational structure
   - Treat schema-feedback as first-class refinement type (equal priority to missing content)
   - Store refinement requests in database with status tracking (pending, in_progress, completed, failed)
   - Integrate refinement requests into research loop prioritization
   - After refinement completion, update calculation function completeness score and notify Compute Engine
   - **Schema Remediation**: Update `canonical_data_model.md`, schema definitions in `specs/001-master-spec/schemas/`, and DB migrations accordingly before relevant freezes
   - Implement refinement request status tracking and reporting
   - Support batch refinement requests for multiple calculations

**Deliverables**:
- Fully-automated research loop operational (Auto-Extract → Auto-Question → Auto-Validate → Auto-Curate)
- Trust scoring system functional
- Continuous learning loop working
- Safety and quality controls implemented
- Research checklist integration complete
- Coverage reports showing checklist item status
- LLM-assisted research integrated into automated loop with Compute Engine requirements context
- Compute Engine requirements context loaded and applied from FIRST research iteration
- Iterative research priming system operational (requirements context applied in each loop iteration)
- Research refinement API implemented (`POST /research/refine`) with schema feedback support (FR-SCHEMA-02)
- Schema feedback treated as first-class refinement type (equal priority to missing content)
- Schema remediation workflow operational (updates canonical_data_model.md, schema definitions, DB migrations before freezes)
- Research progress tracking system operational with automatic updates to RESEARCH_PROGRESS.md
- Calculation function completeness scores tracked and reported
- Canonical calculation list generated (`Research/canonical_calculations.yaml`) with complete specifications for all required calculations, validated against Compute Engine requirements context, ready for Compute Engine consumption

### Phase 5: RAG-Style Retrieval (Week 5)

**Tasks**:
1. **RAG Optimization**
   - Implement RAG-style retrieval for AI models
   - Optimize for AI model embedding
   - Implement citation-ready formatting
   - Implement structured metadata and relevance scoring

**Deliverables**:
- RAG-style retrieval API functional
- Citation-ready formatting implemented

### Phase 6: Version Management (Week 6)

**Tasks**:
1. **Version History**
   - Implement version history tracking
   - Implement version linking (supersedes, amends relationships)
   - Implement change summary tracking

**Deliverables**:
- Version management complete
- Version linking functional

### Phase 7: Testing (Ongoing)

**Tasks**:
1. **Test Implementation**
   - Unit tests for storage operations
   - Integration tests for ingestion pipeline
   - Golden dataset tests (regulator examples)
   - Performance tests for search/retrieval
   - **Automated Research Loop Tests**:
     - Test auto-extraction accuracy and completeness
     - Test auto-questioning generation and prioritization
     - Test auto-validation checks (pinpoint, version, conflict, completeness, simulation)
     - Test trust score calculation accuracy
     - Test continuous learning loop iterations
     - Test safety controls (fail-closed, quarantine, drift alarm, kill switch)
     - Test research checklist coverage validation
   - **Success Criteria Validation**:
     - Verify ≥95% of priority topics approved with trust ≥85
     - Verify 0 unresolved high-priority questions before publishing
     - Verify 100% pinpoint and version verification pass rate
     - Verify ≥99% simulation and self-consistency test pass rate
     - Verify <1% contested findings at publication time

**Deliverables**:
- Test coverage > 80%
- Automated research loop fully tested
- Success criteria validated and met

