# Assumptions, Scope Boundaries & Dependencies - Consolidated

This document contains all assumptions, scope boundaries, and dependencies extracted from the 7 system specification files, organized by source module.

## From Master Specification

### Assumptions

#### Domain Assumptions

- Australian financial regulations (Corporations Act 2001, ASIC Regulatory Guides, ATO Rulings) will continue to operate under hierarchical authority structure (Act > Regulation > Ruling > Guidance > Assumption).

- Financial advisers will continue to be required to demonstrate best interests duty and maintain traceable audit trails under Australian regulations.

- Users (both consumers and advisers) will access the system primarily via mobile devices (consumers) and desktop/web interfaces (advisers).

#### Technical Assumptions

- Relational database technology will be available and capable of supporting the relational-only architecture with required performance characteristics (recursive CTEs, JSONB, temporal tables).

- OpenRouter will continue to offer a unified API suitable for intent detection and natural language translation with acceptable latency and reliability.

- Integration patterns will remain stable enough for partner integrations to rely on documented interfaces.

#### User Behavior Assumptions

- Consumers will prefer conversational, non-technical interactions over complex financial terminology.

- Advisers will prefer efficiency and speed in scenario modelling over extensive configuration options.

- Partners will require stable, versioned interfaces that match internal capabilities rather than custom integrations.

#### Compliance Assumptions

- Australian privacy laws (Privacy Act 1988) will continue to require strict data handling, tenant isolation, and PII protection measures.

- Financial advice regulations will continue to require reproducibility, auditability, and explicit rule-based calculations.

### Scope Boundaries

#### In Scope (MVP)

- Core calculation rules: personal income tax, superannuation contributions and caps, core Capital Gains Tax (CGT)

- Basic scenario support: A/B scenario comparisons, sensitivity basics

- Core calculation capabilities: deterministic calculations and provenance

- Consumer UX: Frankie's Finance with path, front door, living room, study, and garden environments

- Adviser UX: Veris Finance with conversational interface and forecast visualization

- References & Research Engine with basic search and retrieval

- Advice Engine with basic compliance checking

#### Out of Scope (Future)

- Product purchase rails (direct financial product transactions)

- External data aggregation from banks or financial institutions

- Advanced client outcome strategies library beyond basic tax and super strategies

- Comprehensive advice guidance strategies framework beyond core compliance obligations

- Automated trade execution

- Real-time market data integration

### Dependencies

#### External Dependencies

- Australian financial regulatory framework (ASIC, APRA, ATO) maintaining current regulatory structure

- OpenRouter API for unified LLM provider access (supporting both OpenRouter credits and BYOK integration) for natural language processing

- Relational database technology capable of recursive CTEs, JSONB relationships, and temporal queries

- Relational database technology capable of temporal queries and audit logging

#### Internal Dependencies

- Constitution principles must be maintained and validated across all modules

- Rule authoring and publishing workflow must be operational before calculations can execute

- References & Research Engine must be populated with authoritative sources before rules can cite references

- Data extraction pipeline must be operational to populate REFERENCES, RULES, ASSUMPTIONS, ADVICE GUIDANCE, and CLIENT OUTCOME STRATEGIES

---

## From Compute Engine Specification

### Assumptions

#### Domain Assumptions

- Financial calculations will continue to be rule-based and deterministic, enabling algorithmic execution without requiring human judgment during computation.

- Rule definitions will be sufficiently complete and unambiguous to enable automated execution without manual interpretation.

- Calculation inputs (client data, scenario parameters) will be provided in structured formats that can be validated and processed automatically.

- The Australian financial regulatory framework will maintain hierarchical authority (Act > Regulation > Ruling > Guidance > Assumption) enabling precedence-based rule resolution.

#### Technical Assumptions

- PostgreSQL will support efficient traversal of provenance chains (via recursive CTEs) and rule applicability queries with acceptable performance.

- PostgreSQL will provide reliable access to all rule data (definitions, versions, precedence) with acceptable latency.

- Ruleset snapshot creation in PostgreSQL will complete within acceptable time limits (as defined in master spec: 5 minutes) enabling timely ruleset publication.

- Storage systems will scale to support large numbers of Facts (millions) and scenarios (thousands) with acceptable query performance.

- Access infrastructure will support concurrent requests with rate limiting and tenant isolation without performance degradation.

#### Integration Assumptions

- Reference lookup services will be available and operational before Compute Engine can build complete provenance chains.

- Rule authoring and publishing workflow will be operational before Compute Engine can execute calculations.

- Natural language processing services will transform natural language requests into structured calculation requests before calling Compute Engine.

- Compliance evaluation services will query Compute Engine for Fact data when performing compliance evaluation.

### Scope Boundaries

#### In Scope (MVP)

- Core calculation execution with deterministic results

- Scenario support for A/B comparisons and basic sensitivity analysis

- Provenance chain generation linking Facts to Rules, References, and Assumptions

- Explanation capability for human-readable provenance traces

- Facts retrieval with scenario and date filtering

- Time-travel queries using `as_of` dates and ruleset versions

- Batch processing for multiple calculations

- PostgreSQL-only storage: all data storage in single database (computation and rule management)

- Ruleset snapshot creation in PostgreSQL on ruleset publication

#### Out of Scope (Future)

- Real-time streaming calculations or event-driven computation

- Advanced optimization algorithms for complex multi-rule calculations

- Machine learning-based rule inference or pattern detection

- Automated rule conflict resolution beyond precedence-based logic

- Advanced caching strategies beyond basic ruleset projection caching

- Multi-currency or international calculation support (focusing on Australian financial system)

- Real-time market data integration for dynamic calculations

### Dependencies

#### External Dependencies

- PostgreSQL technology capable of recursive CTEs for provenance chain traversal, JSONB for relationship storage, and temporal tables for time-travel queries

- PostgreSQL technology capable of temporal queries, transactions, and audit logging

- Reference lookup services for rule-to-reference lookups in provenance chains

- Authentication/authorization system for access control (from foundational infrastructure)

- Logging and observability infrastructure for audit trails and debugging

#### Internal Dependencies

- Master specification (`001-master-spec`) for system context, requirements, and architectural constraints

- Rule authoring and publishing workflow must be operational before Compute Engine can execute calculations

- Ruleset snapshot mechanism must be functional to create active ruleset snapshots in PostgreSQL

- Data extraction pipeline must populate RULES, ASSUMPTIONS, and CLIENT OUTCOME STRATEGIES before calculations can execute

---

## From References & Research Engine Specification

### Assumptions

#### Domain Assumptions

- Australian legal and regulatory sources (Corporations Act, ASIC Regulatory Guides, ATO Rulings) will continue to be published in structured formats (PDF, HTML) that enable automated extraction.

- Legal documents will maintain consistent structure (section numbers, paragraph identifiers) that enables automatic pinpoint extraction.

- Regulatory bodies (ASIC, APRA, ATO) will continue to publish documents with metadata (publication dates, effective dates) that can be extracted automatically.

- Reference documents will be available via stable URLs or can be stored locally with appropriate licensing.

#### Technical Assumptions

- Document parsing libraries will be available to extract text and structure from PDF, HTML, and other common formats.

- LLM capabilities can be leveraged for document classification and metadata extraction with acceptable accuracy and cost.

- Storage systems can handle large document collections (thousands of references, millions of pinpoints) with acceptable query performance.

- Search and retrieval systems can scale to support concurrent queries from multiple modules (Compute Engine, Advice Engine, LLM Orchestrator).

#### Integration Assumptions

- Other modules will query references via documented interfaces rather than direct database access.

- Reference data will be relatively stable (low update frequency) compared to rule or fact data, enabling caching strategies.

- Interface versioning will be managed to maintain backward compatibility as reference data structures evolve.

### Scope Boundaries

#### In Scope (MVP)

- Core reference storage with unique identifiers, type, title, metadata, and version history

- Basic ingestion pipeline for PDF and HTML documents with manual classification

- Search capability supporting title and keyword queries

- Retrieval capability for full references and pinpoints

- Version tracking with effective date windows

- Reference lookups for provenance chain construction

#### Out of Scope (Future)

- Real-time synchronization with external regulatory databases

- Advanced natural language processing for unstructured document analysis

- Multi-language support (focusing on English/Australian legal documents)

- Collaborative editing or annotation of references

- Advanced analytics on reference usage patterns

- Automated monitoring of regulatory body websites for updates

### Dependencies

#### External Dependencies

- Document parsing libraries for PDF, HTML, and structured data formats

- LLM services (optional) for automated classification and extraction

- Storage systems (relational database for governance, potentially graph database for relationships)

- Regulatory body websites or document repositories for source material

#### Internal Dependencies

- Master specification (`001-master-spec`) for system context and API requirements

- Authentication/authorization system for API access control (from foundational infrastructure)

- Logging and observability infrastructure for audit trails

---

## From Advice Engine Specification

### Assumptions

#### Domain Assumptions

- Australian financial advice regulations (Corporations Act 2001, Code of Ethics, ASIC Regulatory Guides) will continue to require best-interests duty, conflict management, and documentation requirements.

- Compliance obligations can be evaluated deterministically using Advice Guidance and regulatory requirements stored in the system, without requiring subjective human judgment during evaluation.

- Advice Guidance will be sufficiently complete and up-to-date to enable automated compliance evaluation for common advice scenarios.

- Regulatory requirements will maintain consistency in structure (best-interests duty, conflicts, documentation) enabling systematic evaluation.

#### Technical Assumptions

- Advice Guidance data will be available and operational before Advice Engine can perform compliance evaluations.

- Compute Engine will provide Fact data in formats suitable for compliance evaluation.

- References & Research Engine will provide regulatory requirement lookups with acceptable performance for compliance evaluation workflows.

- Storage systems will support efficient querying of Advice Guidance, compliance evaluations, and audit logs.

#### Integration Assumptions

- Consumer and adviser applications will call Advice Engine for compliance validation before presenting advice to users.

- Calculation services will be available to provide Fact data when Advice Engine performs compliance evaluations.

- Reference lookup services will be available to provide regulatory requirement lookups when Advice Engine evaluates compliance.

- Advice Guidance will be stored and versioned in a format that enables efficient querying and evaluation.

### Scope Boundaries

#### In Scope (MVP)

- Core compliance evaluation checking best-interests duty, conflicts, documentation, and product replacement logic

- Compliance requirements retrieval for specific advice contexts

- Warning and required action generation for identified compliance issues

- Basic compliance checklist generation for common advice scenarios

- Fact data retrieval for compliance evaluation

- Regulatory requirement lookups for compliance evaluation

- Consumer-friendly warning formatting for consumer applications

- Deterministic compliance evaluation with reproducibility

#### Out of Scope (Future)

- Advanced conflict detection using machine learning or pattern recognition

- Automated document generation (SOA, ROA) - Advice Engine identifies requirements, but document generation is handled by other modules

- Real-time compliance monitoring or continuous compliance checking

- Multi-jurisdiction compliance evaluation (focusing on Australian regulations)

- Advanced risk assessment or suitability analysis beyond basic best-interests evaluation

- Integration with external compliance databases or regulatory reporting systems

### Dependencies

#### External Dependencies

- Australian financial regulatory framework (Corporations Act 2001, Code of Ethics, ASIC Regulatory Guides) maintaining current compliance structure

- Advice Guidance data must be populated before Advice Engine can perform compliance evaluations

- Storage systems for Advice Guidance, compliance evaluations, and audit logs

#### Internal Dependencies

- Master specification (`001-master-spec`) for system context, requirements, and architectural constraints

- Calculation services for Fact data when evaluating compliance

- Reference lookup services for regulatory requirement lookups

- Authentication/authorization system for access control (from foundational infrastructure)

- Logging and observability infrastructure for audit trails

---

## From LLM Orchestrator Specification

### Assumptions

#### Domain Assumptions

- Users will primarily interact in English/Australian English, enabling focus on English language processing for MVP.

- Natural language queries will follow common patterns (questions, commands, statements) that can be detected and parsed with reasonable accuracy.

- Financial terminology and concepts will be consistent enough to enable reliable intent detection and parameter extraction.

- Users will provide sufficient context in their queries to enable intent detection, or will respond to clarification requests.

#### Technical Assumptions

- OpenRouter will continue to offer a unified API suitable for intent detection and natural language processing with acceptable latency and reliability.

- OpenRouter's BYOK feature will allow seamless integration of existing OpenAI API keys, enabling cost optimization while maintaining unified API access.

- LLM outputs can be validated against schemas with reasonable accuracy, enabling detection of invalid outputs before they reach backend modules.

- Conversation context can be maintained effectively (by clients or temporarily by LLM Orchestrator) to enable coherent multi-turn dialogue.

- PII filtering can be performed effectively without significantly degrading intent detection or parameter extraction capabilities.

- Retrieval queries will primarily use semantic search or keyword-based queries, enabling effective retrieval from PostgreSQL with JSONB metadata without requiring specialized vector databases.

- Relevant structured data (rules, references, assumptions, advice guidance, client outcome strategies) will be available in the relational database via References & Research Engine APIs, enabling RAG retrieval without new data stores.

- Retrieved data will improve LLM accuracy for financial queries by providing authoritative context that may not be present in LLM training data.

- Users will benefit from RAG-enhanced responses even when retrieval adds some latency, as long as total response time remains acceptable (<2 seconds for parsing, <5 seconds for chat).

- PostgreSQL with JSONB will support efficient semantic or keyword-based search for retrieval, enabling RAG without requiring new data stores or specialized search infrastructure.

- Redis caching will effectively reduce latency for frequent retrieval queries, achieving target cache hit rates and performance improvements.

- Cheaper LLM models (e.g., gpt-5-mini) will provide sufficient quality for retrieval queries, enabling cost optimization while maintaining retrieval accuracy.

- Higher-capability models (e.g., gpt-5.1) will be available when needed for complex generation tasks, enabling intelligent model routing based on query complexity.

- Retrieval latency can be optimized to meet p95 <1 second requirement through caching, query optimization, and efficient database queries.

#### Integration Assumptions

- Calculation services will accept structured requests generated by LLM Orchestrator and execute them deterministically.

- Reference lookup services will provide reference lookups with acceptable performance for citation generation.

- Consumer and adviser applications will maintain conversation context and handle tool calls generated by LLM Orchestrator.

- Backend modules will return structured responses that LLM Orchestrator can format conversationally for users.

- References & Research Engine APIs (`/references/search`, `/references/{id}`) will provide the necessary retrieval capabilities, enabling RAG integration without requiring new APIs or data access patterns.

- Tenant isolation (RLS) will be enforced at the database level, ensuring RAG retrieval respects tenant boundaries without requiring additional application-level filtering.

- PII redaction will be applied consistently across retrieved data, ensuring sensitive information is not included in RAG-augmented prompts sent to external LLM providers.

- Compute Engine will continue to validate all calculation-affecting outputs against deterministic rules, ensuring RAG augmentation does not bypass rule validation.

### Scope Boundaries

#### In Scope (MVP)

- Core intent parsing for natural language queries

- Conversational chat interface with tool calls and citations

- Basic PII filtering before sending to external LLM providers

- Schema validation of LLM outputs before forwarding to backend modules

- Structured calculation request generation

- Reference retrieval for citation generation

- Support for English/Australian English language processing

- Basic safety filtering for inappropriate content

- RAG (Retrieval-Augmented Generation) capability for prompt augmentation:
  - RAG retrieval from relational database via References & Research Engine APIs
  - Semantic search or keyword-based queries on PostgreSQL with JSONB metadata
  - Prompt augmentation for `/llm/parse` and `/llm/chat` APIs with optional `use_rag` flag
  - Retrieval of rules, references, assumptions, advice guidance, and client outcome strategies
  - Model routing (cheaper models for retrieval, higher-capability models for generation when needed)
  - Redis caching for frequent retrievals
  - Tenant isolation and PII redaction in retrieval
  - Unit/integration tests for retrieval accuracy (95% relevance target)
  - End-to-end tests via Veris/Frankie's UIs
  - Golden dataset validation
  - Property-based tests for edge cases

#### Out of Scope (Future)

- Advanced multi-language support beyond English

- Complex conversation memory or long-term context retention (focusing on session-based context)

- Advanced reasoning or problem-solving beyond intent detection and parameter extraction

- Direct financial outcome determination (always routes to Compute Engine for deterministic results)

- Advanced PII detection using machine learning (using rule-based filtering for MVP)

- Real-time streaming responses or progressive response generation

- Advanced prompt engineering or fine-tuning of LLM models (using standard models and prompt templating)

- Specialized vector databases or embedding models for semantic search (using PostgreSQL with JSONB for MVP)

- Advanced RAG techniques (re-ranking, multi-hop retrieval, query expansion) beyond basic semantic/keyword search

- RAG for non-structured data (documents, PDFs) - focusing on structured data retrieval for MVP

- Real-time retrieval result streaming or progressive augmentation

- Advanced retrieval optimization (query rewriting, result fusion) beyond basic relevance scoring

- RAG for non-financial domains (focusing on financial rules, references, assumptions, guidance, strategies)

### Dependencies

#### External Dependencies

- OpenRouter API for unified LLM provider access (supporting both OpenRouter credits and BYOK integration)

- OpenRouter will maintain acceptable performance, reliability, and API stability

- Network connectivity to OpenRouter API with acceptable latency

- OpenAI API key (via OpenRouter BYOK) for using existing OpenAI credits through OpenRouter's unified interface

- PostgreSQL database with JSONB support for metadata storage and search (for RAG retrieval)

- Redis for caching frequent RAG retrievals

#### Internal Dependencies

- Master specification (`001-master-spec`) for system context, requirements, and architectural constraints

- Calculation services for executing structured calculation requests transformed from natural language

- References & Research Engine module (`003-references-research-engine`) for data retrieval APIs (`/references/search`, `/references/{id}`) used by RAG capability

- Compute Engine module for validation of calculation-affecting outputs (ensuring RAG-augmented prompts do not bypass rule validation)

- Authentication/authorization system for access control (from foundational infrastructure)

- Logging and observability infrastructure for monitoring LLM usage, errors, and performance

---

## From Frankie's Finance Specification

### Assumptions

#### Domain Assumptions

- Users will primarily access Frankie's Finance via mobile devices (smartphones, tablets) with touch interfaces.

- Users will prefer natural language interaction over structured forms for most queries, enabling conversational interfaces.

- Users will value emotional support and non-judgmental guidance over purely functional financial tools.

- Financial anxiety and shame are common barriers that the app must address through design and interaction patterns.

#### Technical Assumptions

- Mobile devices will have sufficient processing power and connectivity to support real-time calculations and visualizations.

- LLM Orchestrator will provide natural language processing with acceptable latency for conversational interactions.

- Compute Engine will execute calculations within acceptable time limits for real-time scenario exploration.

- Advice Engine will validate compliance within acceptable time limits for seamless user experience.

#### User Behavior Assumptions

- Users will engage with the app non-linearly, jumping between environments based on their current needs rather than following a sequential flow.

- Users will appreciate Frankie's companionship and visual guidance, finding it helpful rather than gimmicky.

- Users will prefer visual representations (charts, metaphors) over text-heavy explanations for financial concepts.

- Users will value transparency and explainability, wanting to understand how advice is calculated even if they don't need technical details.

#### Integration Assumptions

- Natural language processing services will transform natural language queries into structured requests that calculation services can execute.

- Calculation services will return calculation results in formats suitable for visual presentation in the app.

- Compliance validation services will provide compliance validation results formatted appropriately for consumer display.

- Backend services will maintain acceptable performance to support real-time interactions and scenario exploration.

### Scope Boundaries

#### In Scope (MVP)

- Core spatial environments: path, front door, living room, study, garden

- Natural language interaction via natural language processing services

- Financial guidance and advice with compliance validation

- Basic scenario exploration and forecasting

- Goal setting and visual tracking in garden

- Frankie companion with visual navigation cues

- Mobile-first touch interface

- Consumer-friendly explanations and visualizations

#### Out of Scope (Future)

- Advanced goal planning features beyond basic tracking

- Social features or sharing capabilities

- Integration with external financial accounts or bank aggregation

- Advanced analytics or detailed financial reporting

- Multi-user or family account features

- Advanced personalization using machine learning

- Offline-first architecture with full offline capabilities

- Integration with external financial product marketplaces

### Dependencies

#### External Dependencies

- Mobile device capabilities (touch interface, sufficient processing power, connectivity)

- LLM provider APIs (via LLM Orchestrator) for natural language processing

- Mobile app platform (iOS, Android, or cross-platform framework) for app deployment

#### Internal Dependencies

- Master specification (`001-master-spec`) for system context, requirements, and architectural constraints

- Natural language processing services for processing user queries

- Calculation services for executing financial calculations and scenario modelling

- Compliance validation services for validating compliance of financial advice provided to consumers

- Reference lookup services for citation generation and context enhancement

- Authentication/authorization system for user accounts and session management (from foundational infrastructure)

---

## From Veris Finance Specification

### Assumptions

#### Domain Assumptions

- Advisers will primarily access Veris Finance via desktop or web interfaces (not mobile), enabling larger screens and more complex data visualizations.

- Advisers will prefer efficiency and speed over extensive customization options, valuing quick workflows over deep configuration.

- Advisers will work with multiple clients simultaneously, requiring efficient client management and scenario organization.

- Advisers will need to demonstrate compliance and auditability to regulators and clients, requiring comprehensive audit trails and explainability.

#### Technical Assumptions

- Desktop/web interfaces will provide sufficient screen space for complex data visualizations and comparative dashboards.

- LLM Orchestrator will provide natural language processing with acceptable latency for professional workflows.

- Compute Engine will execute calculations within acceptable time limits for real-time scenario exploration.

- Advice Engine will validate compliance within acceptable time limits for seamless workflow integration.

#### User Behavior Assumptions

- Advisers will prefer natural language input for speed, but will also use structured forms when precision is required.

- Advisers will value transparency and auditability, wanting to understand how calculations and recommendations are derived.

- Advisers will need to export documentation frequently for client presentation and regulatory submission.

- Advisers will work in sessions focused on individual clients, requiring efficient context switching between clients.

#### Integration Assumptions

- Natural language processing services will transform natural language queries into structured requests that calculation services can execute.

- Calculation services will return calculation results in formats suitable for professional visualization and analysis.

- Compliance validation services will provide compliance validation results formatted appropriately for professional display and documentation.

- Backend services will maintain acceptable performance to support efficient professional workflows.

### Scope Boundaries

#### In Scope (MVP)

- Core professional interface with LLM chat and data-centric visualizations

- Client record management with natural language and structured input

- Scenario modelling and forecasting with professional charts

- Strategy comparison with side-by-side analysis

- Compliance validation integration

- Basic documentation generation (SOA, ROA) with calculations and compliance results

- Audit log with transparent reasoning trails

- Time-travel queries for historical advice review

#### Out of Scope (Future)

- Advanced client relationship management features beyond basic records

- Integration with external CRM or practice management systems

- Advanced document customization or branding beyond standard templates

- Multi-adviser collaboration or team features

- Advanced analytics or reporting beyond basic audit trails

- Integration with external product databases or marketplaces

- Advanced workflow automation or rule-based triggers

- Integration with external compliance databases or regulatory reporting systems

### Dependencies

#### External Dependencies

- Desktop/web platform capabilities (sufficient screen space, processing power, connectivity)

- LLM provider APIs (via LLM Orchestrator) for natural language processing

- Web application platform or desktop framework for professional interface deployment

#### Internal Dependencies

- Master specification (`001-master-spec`) for system context, requirements, and architectural constraints

- Natural language processing services for processing adviser queries

- Calculation services for executing financial calculations and scenario modelling

- Compliance validation services for validating compliance and generating compliance checklists

- Reference lookup services for citation generation and context enhancement

- Authentication/authorization system for adviser accounts and session management (from foundational infrastructure)
