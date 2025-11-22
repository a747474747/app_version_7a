# Feature Specification: References & Research Engine

**Feature Branch**: `003-references-research-engine`  
**Created**: 2025-01-27  
**Status**: Draft  
**Input**: References & Research Engine module - manages authoritative legal and regulatory sources with pinpoints, versions, and metadata. Provides RAG-style retrieval for humans and AI models.

**Purpose**: This module manages authoritative legal and regulatory sources that form the foundation of the financial advice system. It provides ingestion, storage, versioning, and retrieval capabilities for legislation, regulatory guides, rulings, and case law. The module includes two key submodules: **Data Scraping Submodule** (automatically downloads sources from `Research/human_provided_new_sources.md` using multiple methods including RSS feeds, transcription services, and adaptive scraping techniques) and **Data Cleaning Submodule** (converts documents to clean text, chunks content for LLM processing compatible with OpenRouter models, and prepares data for extraction). All other modules depend on this module for traceability and compliance verification.

**Reference**: This module implements requirements from the master specification (`001-master-spec/spec.md`), specifically FR-004B, FR-037 and FR-038, and supports the canonical Reference entity definition.

## Architectural Boundaries

**References & Research Engine** is the single source of truth for all knowledge storage and retrieval. Per Constitution Principle XII:

- **MUST own**: REFERENCES (legal and regulatory sources with pinpoints and versions), RULES (calculation and taxation rule definitions - stored, not executed), ASSUMPTIONS (financial parameters and constants), ADVICE GUIDANCE (mandatory obligations and professional standards), CLIENT OUTCOME STRATEGIES (actionable financial planning approaches), FINDINGS (provisional knowledge discovered during research), RESEARCH QUESTIONS (uncertainty and ambiguity records), VERDICTS (validation decisions on Findings).

- **MUST NOT**: Perform numeric calculations or execute rules; generate personalised advice or recommendations; define tax formulas, caps, or thresholds (it stores them as Rules). Note: The Data Scraping Submodule downloads and organizes source documents as part of the ingestion process, but the module stores processed, structured knowledge objects rather than raw unprocessed documents.

All knowledge objects MUST be stored and served by References & Research Engine. Other modules (Compute Engine, Advice Engine) MUST query this module for knowledge; they MUST NOT store knowledge objects themselves.

---

## Clarifications

This section addresses ambiguous areas in the specification to eliminate implementation uncertainty.

### Session 2025-01-27

- Q: What should happen when a document ingestion job fails partially (e.g., 5 of 10 documents succeed)? → A: Return partial success with detailed error report per document (success/failure status, error messages for failures)

- Q: What should happen when a search query returns no results, and how should the system help users refine their search? → A: Return empty result set with suggestions (similar search terms, alternative keywords, type filters) and clear messaging

- Q: What should happen when a reference document URL becomes invalid or the source document is removed from the original location? → A: Mark URL as invalid, retain stored content, log change for review

- Q: What should happen when duplicate references are detected during ingestion (same title, type, and effective dates)? → A: Merge metadata, maintain single canonical reference, link versions together

- Q: What should happen when a reference version query with an `as_of` date falls before any version exists, or after all versions have been superseded? → A: Return error (404 or 422) with earliest/latest available version dates and remediation guidance

---

## User Scenarios & Testing

### User Story 1 - Ingest and Store Legal Sources (Priority: P1)

**Developer Story**: A developer needs to ingest authoritative legal and regulatory documents (legislation, ASIC Regulatory Guides, ATO Rulings, case law) into the system so that rules, advice guidance, and client outcome strategies can cite these sources with full traceability.

**Why this priority**: This is foundational - without ingested references, no other module can function. Rules cannot cite sources, provenance chains cannot be built, and compliance verification cannot occur. This must be operational before Compute Engine or Advice Engine can function.

**Independent Test**: A developer can ingest a PDF of the Corporations Act 2001, and the system stores it as a normalized Reference object with metadata (title, type, effective dates), extracts pinpoints (specific sections), and makes it searchable and retrievable.

**Acceptance Scenarios**:

1. **Given** a developer has a legal document (PDF, HTML, or structured format), **When** they submit it to the ingestion pipeline, **Then** the system extracts metadata (title, type, effective dates, source URL), normalizes the content, and stores it as a Reference object with a unique identifier.

2. **Given** a legal document contains multiple sections or clauses, **When** the system ingests it, **Then** it extracts and stores pinpoints (specific sections, paragraphs, clauses) that can be referenced precisely by other modules.

3. **Given** a legal document has been updated or superseded, **When** a new version is ingested, **Then** the system maintains version history, links versions together, and tracks effective date windows for each version.

4. **Given** a developer ingests documents in various formats (PDF, HTML, CSV, YAML), **When** the system processes them, **Then** it automatically classifies document type (Act, Regulation, Guidance, Case), extracts relevant metadata, and normalizes content for consistent storage.

---

### User Story 2 - Search and Retrieve References (Priority: P1)

**User Story**: An adviser, developer, or AI model needs to search for and retrieve specific legal references to verify compliance, cite sources, or understand regulatory requirements.

**Why this priority**: Search and retrieval are core functions that enable all other modules to access authoritative sources. Without this capability, the system cannot provide traceability or compliance verification.

**Independent Test**: An adviser can search for "Corporations Act 2001 section 949A" and receive the exact reference with pinpoint details, version information, and full text of the relevant section, enabling them to verify advice compliance.

**Acceptance Scenarios**:

1. **Given** a user searches for a reference by title, section number, or keyword, **When** they submit a search query, **Then** the system returns matching references ranked by relevance with metadata (type, effective dates, version).

2. **Given** a user needs a specific pinpoint within a reference, **When** they request a reference by ID with a pinpoint identifier, **Then** the system returns the exact text of that section, paragraph, or clause with surrounding context.

3. **Given** a user queries references by type (Act, Regulation, Guidance, Case), **When** they filter search results, **Then** the system returns only references matching the specified type.

4. **Given** an AI model or automated system needs to retrieve references, **When** they request retrieval, **Then** the system returns references in a format suitable for embedding in prompts or citations, with structured metadata and full text.

---

### User Story 3 - Maintain Reference Versions and History (Priority: P2)

**Developer Story**: A developer needs to track changes to legal sources over time, maintain version history, and ensure that rules and advice can reference the correct version applicable at a specific point in time.

**Why this priority**: Financial regulations change over time, and the system must support time-travel queries. Rules need to cite specific versions, and historical advice must reference the versions that were current at that time. This is critical for auditability and compliance.

**Independent Test**: A developer can query for all versions of a specific Act, see the effective date ranges for each version, and retrieve the exact version that was current on a specific date, enabling accurate historical reconstruction of advice.

**Acceptance Scenarios**:

1. **Given** a reference has multiple versions, **When** a user queries version history, **Then** the system returns all versions with effective date ranges, change summaries, and links between versions (supersedes, amends).

2. **Given** a user needs a reference version applicable on a specific date, **When** they query with an `as_of` date parameter, **Then** the system returns the version that was effective on that date, or the most recent version if none existed.

3. **Given** a reference version is superseded or amended, **When** the system stores the new version, **Then** it automatically links versions (supersedes, amends relationships) and updates effective date windows.

4. **Given** a rule or advice references a specific version, **When** that version becomes superseded, **Then** the system maintains the historical link so provenance chains remain accurate even after updates.

---

### User Story 4 - Automated Data Scraping from Online Sources (Priority: P1)

**Developer Story**: A developer adds sources to `Research/human_provided_new_sources.md` with URLs, and the system automatically scrapes, downloads, and organizes these sources into the appropriate folders in the `Research/` directory structure.

**Why this priority**: This is foundational for populating the research database. Without automated scraping, developers must manually download and organize every source, which is time-consuming and error-prone. Automated scraping enables efficient bulk ingestion of regulatory sources.

**Independent Test**: A developer adds a URL for an ASIC Regulatory Guide to `human_provided_new_sources.md`, and the system automatically downloads the document, classifies it, places it in the appropriate folder (`01-primary-authorities/asic/regulatory-guides/`), updates `RESEARCH_PROGRESS.md` and `human_provided_new_sources.md` with status, and makes it available for extraction.

**Acceptance Scenarios**:

1. **Given** a developer adds a source URL to `human_provided_new_sources.md` with status "Pending", **When** the scraping submodule processes it, **Then** it attempts multiple download methods (direct HTTP download, RSS feed discovery, API access), downloads the content, and places it in the appropriate folder based on classification.

2. **Given** a source is a podcast or audio file without transcripts, **When** the scraping submodule processes it, **Then** it attempts to find transcripts via RSS feeds or external sources, and if transcripts are unavailable, it generates transcripts using transcription services and stores both audio and transcript files.

3. **Given** a source URL requires special handling (e.g., requires authentication, uses JavaScript rendering, or has rate limits), **When** the scraping submodule encounters it, **Then** it tries alternative methods (headless browser, API endpoints, manual download instructions) and creates new scraping methods if necessary, logging the approach used for future reference.

4. **Given** scraping fails after all methods are exhausted, **When** the system processes the source, **Then** it updates `human_provided_new_sources.md` with status "Failed", logs the error and methods attempted in the Failed Downloads section, and provides guidance for manual intervention.

5. **Given** a source is successfully scraped, **When** the system processes it, **Then** it updates `RESEARCH_PROGRESS.md` with document counts and `human_provided_new_sources.md` with status "Completed", moving the entry to the Processing History section.

---

### User Story 5 - Data Cleaning and LLM Preparation (Priority: P1)

**Developer Story**: A developer needs scraped or human-provided data to be cleaned, converted to text format, and chunked appropriately for LLM processing across a broad array of potential models via OpenRouter.

**Why this priority**: Raw scraped data (PDFs, HTML, audio transcripts) must be cleaned and prepared before LLM extraction can occur. Proper chunking ensures efficient processing across different model context sizes available through OpenRouter. This is essential for the automated research loop.

**Independent Test**: A developer provides a PDF document, and the system converts it to clean text, removes headers/footers and formatting artifacts, chunks it based on configurable context size parameters compatible with OpenRouter models, and stores cleaned chunks ready for LLM extraction.

**Acceptance Scenarios**:

1. **Given** a scraped PDF document is available, **When** the cleaning submodule processes it, **Then** it converts PDF to text, removes headers, footers, page numbers, and formatting artifacts, preserves document structure (sections, paragraphs), and stores clean text ready for chunking.

2. **Given** cleaned text needs to be chunked for LLM processing, **When** the cleaning submodule processes it, **Then** it only chunks text if it exceeds 60,000 tokens (modern models handle this easily), uses configurable context size parameters (default: 60,000 tokens to avoid unnecessary splitting), ensures chunks respect document boundaries (sections, paragraphs), and stores chunk metadata (chunk ID, position, size, model compatibility) only when chunking occurs.

3. **Given** chunks need to work across multiple OpenRouter models with different context sizes, **When** the cleaning submodule creates chunks (only for documents >60k tokens), **Then** it uses 60,000 tokens as the default chunk size threshold, provides configuration to adjust chunk sizes for specific models, and ensures chunks can be combined or split dynamically based on target model requirements.

4. **Given** a document contains structured data (tables, lists, code), **When** the cleaning submodule processes it, **Then** it preserves structure in a format readable by LLMs (markdown tables, formatted lists), maintains relationships between structured elements, and includes context markers indicating structure type.

5. **Given** cleaning completes successfully, **When** the system processes the document, **Then** it updates `RESEARCH_PROGRESS.md` with extraction-ready status and makes cleaned chunks available for the automated research loop extraction phase.

---

### User Story 6 - Human Source Management Instructions (Priority: P2)

**Developer Story**: A developer needs clear instructions in `human_provided_new_sources.md` for when to store data locally versus linking to online sources, ensuring efficient data management and avoiding unnecessary downloads.

**Why this priority**: Clear guidelines prevent confusion about data storage strategies, reduce redundant downloads, and ensure consistent handling of sources. This supports efficient research database population and maintenance.

**Independent Test**: A developer reads `human_provided_new_sources.md` and understands when to add a URL (for online sources) versus when to place files directly in the Research folder structure (for local files), enabling efficient source management.

**Acceptance Scenarios**:

1. **Given** a developer has a source available online with a stable URL, **When** they want to add it to the system, **Then** they add an entry to `human_provided_new_sources.md` with the URL, and the scraping submodule handles downloading and organization.

2. **Given** a developer has a local file (PDF, transcript, structured data) that is not available online, **When** they want to add it to the system, **Then** they place the file directly in the appropriate Research folder structure, and the system processes it during the next ingestion run without requiring a URL entry.

3. **Given** a developer has a source that changes frequently (e.g., statistical tables updated monthly), **When** they want to track it, **Then** they add it to `human_provided_new_sources.md` with a URL, enabling the system to re-scrape periodically and maintain currency.

4. **Given** a developer has a large file or collection of files, **When** they want to add them efficiently, **Then** they place files directly in the Research folder structure rather than adding individual URLs, reducing scraping overhead and enabling batch processing.

---

### Edge Cases

- What happens when a reference document is corrupted or unparseable? The system MUST flag the document for manual review, log the error, and prevent incomplete or corrupted data from being stored.

- How does the system handle duplicate references? The system MUST detect duplicates based on title, type, and effective dates, merge metadata when appropriate, and maintain a single canonical reference with version history.

- What happens when a search returns no results? The system MUST return an empty result set with clear messaging, and may suggest similar references or alternative search terms.

- How does the system handle references that are not yet effective (future-dated)? The system MUST store future-dated references but clearly mark them as not yet effective, and exclude them from current-date queries unless explicitly requested.

- What happens when a reference URL becomes invalid or the source document is removed? The system MUST maintain the stored reference content, mark the URL as invalid, and log the change for review.

- How does the system handle very large documents (e.g., entire Acts with thousands of sections)? The system MUST process large documents incrementally, store them efficiently, and provide pagination or chunking for retrieval.

- What happens when scraping fails for a source after all methods are exhausted? The system MUST update `human_provided_new_sources.md` with status "Failed", log error details and methods attempted in the Failed Downloads section, and provide guidance for manual intervention or alternative approaches.

- How does the system handle sources that require authentication or special access? The system MUST attempt alternative methods (headless browser, API endpoints), log authentication requirements, and provide instructions for manual download if automated methods fail.

- What happens when a source URL points to a page that requires JavaScript rendering? The system MUST use headless browser rendering, attempt to find direct download links or API endpoints, and create new scraping methods if necessary.

- How does the system determine chunk sizes for different OpenRouter models? The system MUST use the smallest common context size as default, provide configuration for model-specific chunk sizes, and enable dynamic chunk combination or splitting based on target model requirements.

---

## Requirements

### Functional Requirements

#### Reference Storage and Management

- **FR-001**: System MUST store Reference objects with unique identifiers, type (Act, Regulation, Guidance, Case), title, category classification, source URL, version history, and effective date windows.

- **FR-002**: System MUST extract and store pinpoints (specific sections, paragraphs, clauses) for each reference, enabling precise citation and navigation to exact locations within source documents.

- **FR-003**: System MUST maintain version history for references, tracking effective date ranges, change summaries, and relationships between versions (supersedes, amends, replaces).

- **FR-004**: System MUST normalize reference content for consistent storage regardless of source format (PDF, HTML, structured data), preserving original formatting where necessary for legal accuracy.

- **FR-005**: System MUST support time-travel queries, allowing retrieval of reference versions applicable at specific dates via `as_of` date parameters. When an `as_of` date falls before any version exists or after all versions have been superseded, the system MUST return an error (404 Not Found or 422 Unprocessable Entity) with the earliest/latest available version dates and remediation guidance suggesting appropriate dates.

#### Ingestion and Processing

- **FR-006**: System MUST support ingestion of documents in multiple formats: PDF, HTML, CSV, YAML, plain text, and structured data formats.

- **FR-007**: System MUST automatically classify document types (Act, Regulation, Guidance, Case) during ingestion with configurable confidence thresholds.

- **FR-008**: System MUST extract metadata automatically from documents: title, type, effective dates, source URL, publication dates, and regulatory body.

- **FR-009**: System MUST extract pinpoints automatically from structured documents (section numbers, paragraph identifiers, clause references) and support manual pinpoint creation for unstructured documents.

- **FR-010**: System MUST flag documents requiring manual review when classification confidence is low, extraction fails, or data quality issues are detected.

- **FR-011**: System MUST support batch ingestion of multiple documents with progress tracking and error reporting. When batch ingestion fails partially (some documents succeed, others fail), the system MUST return partial success response with detailed error report per document, including success/failure status and specific error messages for failed documents.

#### Data Scraping Submodule

- **FR-027**: System MUST monitor `Research/human_provided_new_sources.md` for sources with status "Pending" and automatically scrape/download them into the appropriate folders in the `Research/` directory structure.

- **FR-028**: System MUST attempt multiple scraping methods for each source: direct HTTP download, RSS feed discovery, API access, headless browser rendering, and other methods as appropriate. If standard methods fail, the system MUST create new scraping methods and log the approach for future reference.

- **FR-029**: System MUST handle audio sources (podcasts, webinars, interviews) by attempting to find transcripts via RSS feeds or external sources. If transcripts are unavailable, the system MUST generate transcripts using transcription services and store both audio and transcript files.

- **FR-030**: System MUST update `RESEARCH_PROGRESS.md` after each scraping operation, updating document counts by folder, type, and regulatory body, and tracking success/failure statistics.

- **FR-031**: System MUST update `human_provided_new_sources.md` after scraping operations, changing status from "Pending" to "Processing", then to "Completed" or "Failed", and moving entries to the Processing History section with processing date and target folder information.

- **FR-032**: System MUST log failed scraping attempts in `human_provided_new_sources.md` Failed Downloads section, including error details, methods attempted, retry count, and last attempt timestamp.

#### Data Cleaning Submodule

- **FR-033**: System MUST clean scraped or human-provided data before LLM extraction, converting PDFs to text, removing headers/footers/page numbers, preserving document structure (sections, paragraphs), and removing formatting artifacts.

- **FR-034**: System MUST only chunk cleaned text if it exceeds 60,000 tokens (modern models handle this easily). Chunk sizes MUST default to 60,000 tokens to avoid unnecessary splitting. Chunking MUST be configurable for specific model requirements.

- **FR-035**: System MUST ensure chunks respect document boundaries (sections, paragraphs) and do not split content mid-sentence or mid-paragraph unless absolutely necessary for size constraints (only when document exceeds 60k token threshold).

- **FR-036**: System MUST store chunk metadata (chunk ID, position in document, size in tokens/characters, model compatibility information) only when chunking occurs, enabling dynamic chunk combination or splitting based on target model requirements for large documents.

- **FR-037**: System MUST preserve structured data (tables, lists, code) in formats readable by LLMs (markdown tables, formatted lists), maintaining relationships between structured elements and including context markers indicating structure type.

- **FR-038**: System MUST update `RESEARCH_PROGRESS.md` after cleaning operations, marking documents as extraction-ready and updating processing statistics.

#### Source Management Instructions

- **FR-039**: System MUST provide clear instructions in `human_provided_new_sources.md` for when to store data locally versus linking to online sources: use URLs for online sources with stable links, use direct file placement for local files not available online, use URLs for frequently changing sources requiring periodic re-scraping, use direct file placement for large files or collections to reduce scraping overhead.

#### Search and Retrieval

- **FR-012**: System MUST provide search capability supporting queries by title, section number, keyword, type, and effective date range. When a search query returns no results, the system MUST return an empty result set with suggestions (similar search terms, alternative keywords, type filters) and clear messaging to help users refine their search.

- **FR-013**: System MUST return search results ranked by relevance with metadata (type, effective dates, version, source URL) and preview text.

- **FR-014**: System MUST provide retrieval capability returning full reference details including metadata, version history, and full text content.

- **FR-015**: System MUST provide pinpoint retrieval capability returning all pinpoints for a reference with section numbers, text excerpts, and navigation paths.

- **FR-016**: System MUST provide retrieval optimized for AI models, returning references in formats suitable for embedding in prompts with structured metadata and citation-ready text.

- **FR-017**: System MUST support filtering search results by type (Act, Regulation, Guidance, Case), effective date range, and regulatory body.

#### Access and Integration

- **FR-018**: System MUST provide access following the master specification's requirements.

- **FR-019**: System MUST support access control with tenant isolation and rate limits as specified in the master specification (see CL-031 and FR-030 for security guarantee that User A can NEVER see User B's data under ANY circumstances).

- **FR-019A**: System MUST include automated security tests that verify cross-tenant data access is impossible for all References & Research Engine endpoints. Tests MUST simulate bugs, misconfigured queries, malicious input, missing tenant context, and other failure scenarios to ensure User A cannot access User B's references, research documents, or extracted data under any conditions (see FR-030A in master specification).

- **FR-020**: System MUST provide reference lookups for provenance chains, enabling Fact → Rule → Reference tracing.

- **FR-021**: System MUST provide reference lookups for regulatory requirements and compliance verification.

- **FR-022**: System MUST provide reference retrieval for citation generation and context enhancement.

#### Data Quality and Governance

- **FR-023**: System MUST maintain data extraction quality standards: completeness (all relevant references ingested), accuracy (exact text from sources), context (narrative summaries), traceability (source URLs), consistency (standardized formats), and currency (effective dates and versions).

- **FR-024**: System MUST validate reference data against schema requirements before storage, ensuring required fields are present and data types are correct.

- **FR-025**: System MUST maintain audit logs tracking all reference ingestion, updates, version changes, and access patterns for compliance and debugging.

- **FR-026**: System MUST detect and prevent duplicate references based on title, type, and effective dates, merging metadata when appropriate. When duplicates are detected during ingestion, the system MUST merge metadata, maintain a single canonical reference, and link versions together, ensuring no duplicate entries exist in the system.

- **FR-026A**: System MUST handle invalid reference URLs: when a reference document URL becomes invalid or the source document is removed, the system MUST mark the URL as invalid, retain the stored reference content, and log the change for review. The reference MUST remain accessible and queryable even with an invalid URL.

- **FR-026B**: System MUST provide instructions in `human_provided_new_sources.md` explaining when to use URLs versus direct file placement: URLs for online sources with stable links, direct file placement for local files not available online, URLs for frequently changing sources requiring periodic re-scraping, direct file placement for large files or collections to reduce scraping overhead.

---

### Key Entities

- **Reference**: Core entity representing an authoritative legal or regulatory source. Attributes include: unique identifier, type (Act, Regulation, Guidance, Case), title, category classification, source URL, version history, effective date windows, regulatory body, publication date, and full text content. Relationships: links to other references (supersedes, amends), linked from Rules via citations, linked from Facts via provenance chains.

- **Pinpoint**: Specific location within a reference document. Attributes include: pinpoint identifier, reference ID, section/paragraph/clause identifier, text excerpt, navigation path (e.g., "Section 949A, subsection (2)"), and context (surrounding text). Relationships: belongs to one Reference, can be cited by Rules or Advice Guidance.

- **Reference Version**: Historical snapshot of a reference at a specific point in time. Attributes include: version identifier, reference ID, effective start date, effective end date (if superseded), change summary, and full content snapshot. Relationships: belongs to one Reference, links to previous/next versions (supersedes, amends).

- **Ingestion Job**: Batch processing job for ingesting documents. Attributes include: job identifier, status (pending, processing, completed, failed), source files, processing start/end times, error logs, and results summary. Relationships: produces multiple References.

- **Scraping Job**: Automated scraping job for downloading sources from `human_provided_new_sources.md`. Attributes include: job identifier, source URL, scraping methods attempted, download status, target folder, processing start/end times, error logs, and retry count. Relationships: produces downloaded files for ingestion.

- **Cleaning Job**: Data cleaning job for preparing documents for LLM extraction. Attributes include: job identifier, source document, cleaning operations performed, chunking configuration, chunk count, processing start/end times, and error logs. Relationships: produces cleaned chunks for extraction.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Developers can ingest a standard legal document (up to 100 pages) and have it stored as a normalized Reference with extracted pinpoints within 5 minutes of submission.

- **SC-002**: Users can search for references and receive relevant results ranked by relevance within 2 seconds for 95% of queries.

- **SC-003**: System maintains 99.9% accuracy in automatic document type classification (Act, Regulation, Guidance, Case) when validated against manually classified test set.

- **SC-004**: System successfully extracts pinpoints from 90% of structured legal documents (Acts, Regulations) without manual intervention.

- **SC-005**: Users can retrieve any reference version applicable on a specific historical date with 100% accuracy for time-travel queries.

- **SC-006**: System supports ingestion of 1,000 reference documents per day through automated batch processing without manual intervention for 95% of documents.

- **SC-007**: Retrieval capability returns references in formats suitable for AI model embedding with structured metadata within 1 second for 90% of requests.

- **SC-008**: System maintains complete version history for all references, enabling accurate historical reconstruction of advice provenance chains.

- **SC-009**: Search capability returns relevant results (precision > 80%) for 90% of queries across different search patterns (title, keyword, section number).

- **SC-010**: System detects and prevents duplicate references with 95% accuracy, reducing data redundancy and ensuring canonical reference storage.

- **SC-011**: System successfully scrapes 90% of sources listed in `human_provided_new_sources.md` without manual intervention, automatically downloading and organizing them into appropriate Research folder structure.

- **SC-012**: System successfully cleans and chunks 95% of scraped documents, converting them to LLM-ready format with appropriate chunk sizes compatible with OpenRouter models.

- **SC-013**: System updates `RESEARCH_PROGRESS.md` and `human_provided_new_sources.md` within 30 seconds of completing scraping or cleaning operations, ensuring accurate tracking of research progress.

---

## Assumptions

### Domain Assumptions

- Australian legal and regulatory sources (Corporations Act, ASIC Regulatory Guides, ATO Rulings) will continue to be published in structured formats (PDF, HTML) that enable automated extraction.

- Legal documents will maintain consistent structure (section numbers, paragraph identifiers) that enables automatic pinpoint extraction.

- Regulatory bodies (ASIC, APRA, ATO) will continue to publish documents with metadata (publication dates, effective dates) that can be extracted automatically.

- Reference documents will be available via stable URLs or can be stored locally with appropriate licensing.

### Technical Assumptions

- Document parsing libraries will be available to extract text and structure from PDF, HTML, and other common formats.

- LLM capabilities can be leveraged for document classification and metadata extraction with acceptable accuracy and cost.

- Storage systems can handle large document collections (thousands of references, millions of pinpoints) with acceptable query performance.

- Search and retrieval systems can scale to support concurrent queries from multiple modules (Compute Engine, Advice Engine, LLM Orchestrator).

### Integration Assumptions

- Other modules will query references via documented interfaces rather than direct database access.

- Reference data will be relatively stable (low update frequency) compared to rule or fact data, enabling caching strategies.

- Interface versioning will be managed to maintain backward compatibility as reference data structures evolve.

---

## Scope Boundaries

### In Scope (MVP)

- Core reference storage with unique identifiers, type, title, metadata, and version history

- Basic ingestion pipeline for PDF and HTML documents with manual classification

- Search capability supporting title and keyword queries

- Retrieval capability for full references and pinpoints

- Version tracking with effective date windows

- Reference lookups for provenance chain construction

### Out of Scope (Future)

- Real-time synchronization with external regulatory databases

- Advanced natural language processing for unstructured document analysis

- Multi-language support (focusing on English/Australian legal documents)

- Collaborative editing or annotation of references

- Advanced analytics on reference usage patterns

- Automated monitoring of regulatory body websites for updates

---

## Dependencies

### External Dependencies

- Document parsing libraries for PDF, HTML, and structured data formats

- LLM services (optional) for automated classification and extraction

- Storage systems (relational database for governance, potentially graph database for relationships)

- Regulatory body websites or document repositories for source material

### Internal Dependencies

- Master specification (`001-master-spec`) for system context and API requirements

- Authentication/authorization system for API access control (from foundational infrastructure)

- Logging and observability infrastructure for audit trails

