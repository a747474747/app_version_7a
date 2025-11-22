# Consolidated User Scenarios

This document contains all unique user scenarios extracted from the system specifications. Each scenario represents a distinct user need or workflow in the financial advice system.

## From Master Specification

### User Story 1 - Consumer Financial Guidance (Priority: P1)

**Consumer Story**: An everyday Australian user opens Frankie's Finance on their mobile device seeking guidance on a financial question. They feel anxious about money decisions and need a safe, non-judgmental environment to explore options and understand recommendations.

**Why this priority**: This represents the primary consumer value proposition. The system must provide emotionally supportive, transparent financial guidance accessible to non-experts. Without this capability, the consumer-facing product cannot deliver value.

**Independent Test**: A user can ask "Should I contribute more to super?" and receive:
- A clear, jargon-free explanation
- A visual forecast showing different contribution scenarios
- Transparency on how the recommendation was calculated
- Compliance validation ensuring the advice meets professional standards
- The ability to explore follow-up questions without judgment

**Acceptance Scenarios**:

1. **Given** a user opens Frankie's Finance for the first time, **When** they interact with Frankie on the path, **Then** they are welcomed into the home environment (path → front door → living room/study/garden) and can ask questions naturally.

2. **Given** a user asks a financial question in the living room, **When** the system processes their intent, **Then** they receive a conversational response with underlying calculations executed, traceable explanations, and compliance validation ensuring the advice meets professional standards.

3. **Given** a user wants to explore "what-if" scenarios, **When** they follow Frankie to the study, **Then** they can view comparative forecasts, charts, and sensitivity analyses with full provenance linking back to rules and references, with compliance checks performed for each scenario.

4. **Given** a user receives financial advice, **When** they want to understand why a recommendation was made, **Then** they can access a human-readable explanation tracing Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions with versions and dates, and see compliance validation results indicating whether the advice meets best interests duty and regulatory requirements.

5. **Given** a user receives financial advice through Frankie's Finance, **When** the system evaluates the recommendation for compliance, **Then** any compliance warnings or required actions are displayed in a user-friendly, non-technical manner appropriate for consumers.

---

### User Story 2 - Adviser Professional Workflow (Priority: P1)

**Adviser Story**: A licensed financial adviser needs to quickly model client strategies, compare scenarios, and generate compliant documentation. They require professional tools that reduce administrative burden while maintaining auditability and compliance standards.

**Why this priority**: This represents the primary adviser value proposition. The system must enable efficient, compliant advice generation while preserving transparency and regulatory compliance. This is critical for professional adoption.

**Independent Test**: An adviser can enter client data via natural language ("Add client aged 42 with $450k super") or structured input, request strategy comparisons ("Compare debt-recycling vs offset-strategy over 10 years"), and export compliance documentation with full audit trails.

**Acceptance Scenarios**:

1. **Given** an adviser opens Veris Finance, **When** they input client information via chat or structured forms, **Then** the system stores client data and makes it available for scenario modelling and future advice sessions.

2. **Given** an adviser requests a strategy comparison, **When** they specify scenarios and assumptions, **Then** the system executes deterministic calculations, returns comparative forecasts, and maintains full provenance for audit purposes.

3. **Given** an adviser generates advice documentation, **When** they export compliance packs, **Then** all recommendations include traceable explanations linking to authoritative references, rule versions, and calculation assumptions.

4. **Given** an adviser needs to review past advice, **When** they query historical calculations, **Then** the system uses time-travel capabilities with `as_of` dates to reconstruct exact recommendations using the ruleset versions applicable at that time.

---

### User Story 3 - Partner Integration (Priority: P2)

**Partner Story**: A third-party financial services provider wants to integrate App Version 5's calculation engine and rule intelligence into their own platform. They need stable, well-documented interfaces that match internal capabilities.

**Why this priority**: Partner integrations expand the system's reach and create additional revenue streams. However, core consumer and adviser functionality must be stable before partner integrations can be reliably delivered.

**Independent Test**: A partner can submit calculation requests with client payloads, receive forecasts and comparisons, query active rules, and embed explainability traces in their own UI for transparency.

**Acceptance Scenarios**:

1. **Given** a partner has valid credentials, **When** they submit a calculation request with client data, scenario parameters, and pin `ruleset_id` and `as_of`, **Then** they receive deterministic calculation results identical to internal system calls with no logic forks.

2. **Given** a partner needs to understand which rules apply to a client situation, **When** they query active rules, **Then** they receive rule metadata including effective dates, precedence, and references without exposing internal implementation details.

3. **Given** a partner wants to surface explainability to their users, **When** they request explanation for a calculation result, **Then** they receive human-readable provenance chains suitable for embedding in their own interfaces.

---

### User Story 4 - Consumer PII Filtering Transparency (Frankie's Finance) (Priority: P1)

**Consumer Story**: A user opens Frankie's Finance for the first time and is asked to provide basic identifying information (name, date of birth, suburb) during initial setup. The app explains that this information will be used to personalize their experience, but that their name and any identifying information will be filtered out of requests sent to external AI services so that the information cannot be connected to them and they cannot be identified from their information. The app references its privacy policy for more details.

**Why this priority**: Privacy transparency is essential for building consumer trust, especially when dealing with financial information. Users need to understand how their data is protected before they feel comfortable using the service. This is a foundational trust-building element that must be present from the first interaction.

**Independent Test**: A new user can complete the initial setup flow, see a clear explanation of PII filtering, understand that their identifying information will not be sent to external AIs, and access the privacy policy—all before asking their first financial question.

**Acceptance Scenarios**:

1. **Given** a user opens Frankie's Finance for the first time, **When** they reach the initial setup screen, **Then** they are prompted to enter their name, date of birth, and suburb, with a clear explanation that this information helps personalize their experience.

2. **Given** a user enters their name, date of birth, and suburb during setup, **When** they submit this information, **Then** they see a privacy explanation screen that clearly states: "Your name and any identifying information about you will be filtered out of requests to external AIs so that your information is not connected to you and you cannot be identified from your information."

3. **Given** a user views the privacy explanation, **When** they want more details, **Then** they can access the app's privacy policy through a clear link or button, which explains the full privacy practices and compliance with Australian Privacy Act 1988.

4. **Given** the app has collected the user's full name during setup, **When** the user asks financial questions that might reference their name or other identifying information, **Then** the system uses the known name to more effectively filter PII from queries before sending to external LLM providers.

5. **Given** a user has completed setup and understands PII filtering, **When** they ask a financial question like "Should I contribute more to super?", **Then** they can use the service with confidence that their identifying information is protected, even if their query contains references to personal details.

---

### User Story 5 - Adviser PII Filtering Transparency (Veris Finance) (Priority: P1)

**Adviser Story**: A licensed financial adviser opens Veris Finance and enters client personal information during initial client setup. The system explains in detail how client PII is handled, how it complies with privacy regulations, and how the filtering process ensures that client identifying information is not sent to external LLM providers. The explanation is more detailed than the consumer version, appropriate for professional users who need to understand compliance requirements. The system references the same privacy policy used by Frankie's Finance.

**Why this priority**: Professional advisers have legal and ethical obligations to protect client information. They need detailed understanding of how the system handles PII to ensure compliance and to explain privacy practices to clients. This transparency is essential for professional adoption and regulatory compliance.

**Independent Test**: An adviser can complete client setup, view a detailed explanation of PII filtering and compliance, understand how client information is protected, and access the privacy policy—all before processing any client queries through the LLM system.

**Acceptance Scenarios**:

1. **Given** an adviser opens Veris Finance and begins setting up a new client, **When** they enter client personal information (name, date of birth, address, contact details, financial account numbers, TFN, etc.), **Then** the system collects this information with clear labels indicating what information is being collected and why.

2. **Given** an adviser enters comprehensive client PII during setup, **When** they complete the client setup, **Then** they see a detailed privacy explanation that covers: how client PII is handled, how the filtering process works, how it ensures client identifying information is not sent to external LLMs, and how this complies with Australian Privacy Act 1988 and professional obligations.

3. **Given** an adviser views the detailed privacy explanation, **When** they want more information, **Then** they can access the full privacy policy (same as Frankie's Finance) which provides comprehensive details about data handling, retention, security, and compliance.

4. **Given** the system has collected comprehensive client PII during setup, **When** the adviser processes client queries or scenarios, **Then** the system uses the known client information to more effectively filter PII from all queries before sending to external LLM providers, ensuring no client identifying information reaches external services.

5. **Given** an adviser understands the PII filtering process, **When** they process client scenarios or ask questions about client situations, **Then** they can use the service with confidence that client information is protected, and they can explain the privacy protections to clients if asked.

6. **Given** an adviser needs to explain privacy practices to a client, **When** they reference the system's privacy handling, **Then** they have access to clear, professional language they can use to explain how client information is protected when using the system.

---

## From Compute Engine Specification

### User Story 1 - Execute Deterministic Financial Calculations (Priority: P1)

**User Story**: An adviser, consumer, or partner needs to execute financial calculations (e.g., tax calculations, superannuation contributions, retirement projections) and receive deterministic, reproducible results that can be verified and audited.

**Why this priority**: This is the core function of the Compute Engine. Without deterministic calculations, the system cannot provide reliable financial advice. All other capabilities depend on this foundational requirement.

**Independent Test**: A user can submit a calculation request with client data, scenario parameters, `ruleset_id`, and `as_of` date, and receive computed Facts with full provenance. Repeating the same request with identical parameters produces identical results.

**Acceptance Scenarios**:

1. **Given** a user submits a calculation request with client data, scenario parameters, `ruleset_id`, and `as_of` date, **When** the system processes it, **Then** it executes applicable rules from the specified ruleset, produces Facts with full provenance, and returns results within acceptable time limits.

2. **Given** a user submits the same calculation request twice with identical parameters, **When** both requests are processed, **Then** both produce identical Fact values, units, rounding, and provenance chains, demonstrating deterministic reproducibility.

3. **Given** a user submits a calculation request with an `as_of` date in the past, **When** the system processes it, **Then** it uses the ruleset version and rules applicable on that date, enabling time-travel queries for historical reconstruction.

4. **Given** a calculation requires multiple rules to be applied in sequence, **When** the system executes them, **Then** it respects rule precedence (Act > Regulation > Ruling > Guidance > Assumption) and effective date windows, applying the correct rules in the correct order.

---

### User Story 2 - Scenario Modelling and Comparisons (Priority: P1)

**User Story**: An adviser or consumer needs to model different financial scenarios (e.g., "What if I retire at 58 vs 65?" or "Compare debt-recycling vs offset-strategy") and compare outcomes side-by-side to make informed decisions.

**Why this priority**: Scenario modelling is essential for financial planning. Users need to explore "what-if" scenarios and compare alternatives. This capability enables informed decision-making and is a core value proposition.

**Independent Test**: A user can create multiple scenarios (A, B, C) with different parameters, execute calculations for each scenario, and retrieve comparative results showing how outcomes differ across scenarios.

**Acceptance Scenarios**:

1. **Given** a user creates multiple scenarios with different parameters (e.g., retirement age, contribution amounts), **When** they execute calculations for each scenario, **Then** the system produces separate Facts for each scenario, tagged with unique scenario IDs, enabling side-by-side comparison.

2. **Given** a user requests scenario comparison, **When** they query with scenario parameters, **Then** the system returns Facts for all requested scenarios with consistent structure, enabling comparative analysis.

3. **Given** scenarios are created as alternative futures, **When** calculations are executed, **Then** scenario Facts never overwrite base reality Facts, maintaining clear separation between actual and hypothetical outcomes.

4. **Given** a user wants to perform sensitivity analysis, **When** they vary a single parameter across multiple scenarios, **Then** the system executes calculations efficiently, showing how outcomes change with parameter variations.

---

### User Story 3 - Provenance and Explainability (Priority: P1)

**User Story**: An adviser, consumer, or regulator needs to understand how a calculation result was derived, tracing it back through rules, references, and assumptions to verify accuracy and compliance.

**Why this priority**: Provenance and explainability are non-negotiable requirements for financial advice. Users must be able to audit calculations, and regulators must be able to verify compliance. This capability builds trust and enables regulatory compliance.

**Independent Test**: A user can retrieve any computed Fact and request its explanation, receiving a human-readable trace showing Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions with versions and dates.

**Acceptance Scenarios**:

1. **Given** a Fact has been computed, **When** a user requests explanation, **Then** the system builds a provenance chain linking the Fact to the rules that produced it, the references those rules cite, and the assumptions used.

2. **Given** a Fact was computed using multiple rules, **When** the explanation is generated, **Then** it shows all applicable rules, their precedence relationships, and how they combined to produce the result.

3. **Given** a Fact references a Client Outcome Strategy, **When** the explanation is generated, **Then** it shows how the strategy combines rules, assumptions, and advice guidance, providing context for why the strategy was applied.

4. **Given** a user needs to export provenance for compliance, **When** they request explanation, **Then** the system provides a format suitable for inclusion in compliance packs, with all references, versions, and dates clearly documented.

---

### User Story 4 - Batch Processing and Performance (Priority: P2)

**User Story**: An adviser or partner needs to execute multiple calculations efficiently, either as part of a single request (batch) or as multiple sequential requests, without performance degradation.

**Why this priority**: Advisers often need to model multiple scenarios or process multiple clients. Performance is critical for user experience. Batch processing enables efficiency gains and reduces API call overhead.

**Independent Test**: A user can submit a batch of calculation requests and receive results for all calculations within acceptable time limits, with performance scaling linearly with batch size up to reasonable limits.

**Acceptance Scenarios**:

1. **Given** a user submits a batch of calculation requests, **When** the system processes them, **Then** it executes calculations efficiently, potentially in parallel where safe, and returns results for all requests with consistent structure.

2. **Given** multiple users submit calculation requests concurrently, **When** the system processes them, **Then** it maintains performance and accuracy, ensuring tenant isolation and preventing one user's requests from affecting another's results.

3. **Given** a calculation request requires complex rule resolution or large data processing, **When** the system processes it, **Then** it completes within acceptable time limits (as defined in success criteria) while maintaining accuracy and provenance.

4. **Given** a user queries historical Facts with scenario and date parameters, **When** the system retrieves them, **Then** it returns results efficiently, supporting time-travel queries without performance degradation.

---

## From References & Research Engine Specification

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

## From Advice Engine Specification

### User Story 1 - Validate Advice Compliance (Priority: P1)

**Adviser Story**: An adviser wants to validate their recommendations against the Code of Ethics and regulatory obligations so they can ensure every piece of advice is compliant, traceable, and ready for audit.

**Why this priority**: Compliance is non-negotiable for professional advisers. Every recommendation must meet regulatory requirements. This capability ensures advisers can confidently provide advice knowing it meets professional standards.

**Independent Test**: An adviser can submit advice recommendations for compliance checking, receive validation results with warnings and required actions, and see compliance status clearly displayed with links to regulatory requirements.

**Acceptance Scenarios**:

1. **Given** an adviser prepares advice recommendations, **When** they request compliance checking, **Then** the system validates best-interests duty, conflicts, documentation requirements, and product replacement logic, returning compliance outcomes.

2. **Given** compliance validation identifies issues, **When** warnings and required actions are generated, **Then** they are specific, actionable, and reference relevant regulatory requirements and professional standards.

3. **Given** an adviser needs to understand compliance requirements, **When** they query with context parameters, **Then** the system returns required actions, documentation, and professional standards applicable to their advice context.

4. **Given** compliance validation passes, **When** advice is approved, **Then** the system clearly indicates compliance status, enabling advisers to proceed with confidence.

---

### User Story 2 - Consumer Advice Compliance Validation (Priority: P1)

**Consumer Story**: A consumer receives financial advice through Frankie's Finance, and the system must validate that advice meets professional standards and regulatory requirements before presenting it to the consumer.

**Why this priority**: Consumers must receive compliant advice even when accessing it through a consumer-facing application. The Advice Engine must validate all advice provided to consumers, ensuring it meets best-interests duty and regulatory requirements, with results displayed in consumer-friendly language.

**Independent Test**: When Frankie's Finance provides financial advice to a consumer, the Advice Engine validates it, and any compliance warnings or required actions are displayed in user-friendly, non-technical language appropriate for consumers.

**Acceptance Scenarios**:

1. **Given** Frankie's Finance provides financial advice to a consumer, **When** the Advice Engine evaluates it, **Then** it performs the same compliance checks as for adviser advice, ensuring consumer advice meets professional standards.

2. **Given** compliance validation identifies issues with consumer advice, **When** warnings are generated, **Then** they are displayed in consumer-friendly language, avoiding technical jargon while maintaining accuracy.

3. **Given** consumer advice cannot meet compliance requirements, **When** validation fails, **Then** the system prevents presentation of non-compliant advice and suggests consulting a licensed financial adviser.

4. **Given** consumer advice passes compliance validation, **When** results are returned, **Then** consumers can see that their advice has been validated against professional standards, building trust and confidence.

---

### User Story 3 - Retrieve Compliance Requirements (Priority: P2)

**Adviser Story**: An adviser needs to understand what compliance obligations apply in a specific context (e.g., "giving personal advice" or "recommending a product replacement") so they can prepare appropriate documentation and follow required processes.

**Why this priority**: Advisers need proactive guidance on compliance requirements before providing advice. This enables them to prepare documentation, follow processes, and avoid compliance issues. This is valuable for workflow efficiency and risk management.

**Independent Test**: An adviser can query compliance requirements for a specific context (e.g., "giving_personal_advice") and receive a list of required actions, documentation, and professional standards that apply.

**Acceptance Scenarios**:

1. **Given** an adviser queries compliance requirements for a specific context, **When** they submit a query with context parameters, **Then** the system returns required actions (e.g., provide FSG, assess client circumstances), required documentation (e.g., Statement of Advice), and relevant professional standards.

2. **Given** compliance requirements reference regulatory sources, **When** requirements are returned, **Then** they include links to relevant References (legislation, regulatory guides) enabling advisers to verify requirements.

3. **Given** compliance requirements vary by advice type or client circumstances, **When** requirements are queried, **Then** the system returns context-specific requirements, filtering out irrelevant obligations.

4. **Given** compliance requirements change over time, **When** requirements are queried with an `as_of` date, **Then** the system returns requirements applicable at that time, supporting historical reconstruction.

---

### User Story 4 - Generate Compliance Documentation Checklists (Priority: P2)

**Adviser Story**: An adviser needs automated checklists of required documentation and actions for compliance, ensuring nothing is missed when preparing advice and reducing administrative burden.

**Why this priority**: Compliance documentation is complex and error-prone. Automated checklists reduce the risk of missing required documents or actions, improve efficiency, and ensure consistency. This supports the value proposition of reducing adviser administrative burden.

**Independent Test**: An adviser can request a compliance checklist for their advice scenario, and receive a structured list of required documents (FSG, SOA, ROA), required actions (client assessment, conflict checks), and professional standards, with checkboxes for tracking completion.

**Acceptance Scenarios**:

1. **Given** an adviser requests a compliance checklist, **When** the Advice Engine generates it, **Then** it includes all required documents, actions, and professional standards applicable to the advice context.

2. **Given** compliance checklists reference specific regulatory requirements, **When** checklists are generated, **Then** they include citations to relevant References, enabling advisers to verify requirements and demonstrate compliance.

3. **Given** compliance requirements have been completed, **When** checklists are updated, **Then** the system tracks completion status, enabling advisers to see what remains to be done.

4. **Given** compliance checklists are used for audit purposes, **When** they are exported, **Then** they include timestamps, completion status, and references to regulatory sources, suitable for inclusion in compliance packs.

---

## From LLM Orchestrator Specification

### User Story 1 - Parse Natural Language Intent (Priority: P1)

**User Story**: A consumer or adviser asks a financial question in natural language (e.g., "Should I contribute more to super?" or "Compare debt-recycling vs offset-strategy over 10 years"), and the system needs to understand the intent and transform it into a structured request that can be executed.

**Why this priority**: This is the core function of the LLM Orchestrator. Without intent parsing, users cannot interact with the system using natural language. This capability enables the conversational interfaces in both Frankie's Finance and Veris Finance.

**Independent Test**: A user can submit a natural language query and receive structured output indicating intent, extracted parameters, and the next action to take, enabling the client application to proceed with execution.

**Acceptance Scenarios**:

1. **Given** a user asks "Should I contribute more to super?", **When** the system processes it (optionally with RAG enabled), **Then** it retrieves relevant rules and references about superannuation contribution caps (if RAG enabled), augments the LLM prompt with this context, detects the intent (e.g., "superannuation_contribution_advice"), extracts parameters (current super balance, contribution amounts, age), and returns structured request for calculation with higher accuracy than without RAG.

2. **Given** a user asks "Compare debt-recycling vs offset-strategy over 10 years", **When** the system processes it, **Then** it detects the intent (scenario comparison), extracts parameters (mortgage details, investment capacity, time horizon), and structures a request for multiple scenario calculations.

3. **Given** a user's query is ambiguous or missing required information, **When** the system processes it, **Then** it identifies missing parameters and returns a structured response indicating what information is needed, enabling the client to request clarification.

4. **Given** a user's query contains PII or sensitive information, **When** the system processes it, **Then** it filters or redacts sensitive data before sending to LLM providers, maintaining privacy while enabling intent detection.

---

### User Story 2 - Conversational Chat Interface (Priority: P1)

**User Story**: A consumer or adviser engages in a multi-turn conversation with the system, asking follow-up questions, refining their queries, and receiving conversational responses that guide them toward actionable outcomes.

**Why this priority**: Conversational interfaces are essential for both consumer and adviser experiences. Users expect natural dialogue, not rigid forms. This capability enables the emotion-first experience in Frankie's Finance and the professional chat interface in Veris Finance.

**Independent Test**: A user can engage in a multi-turn conversation, receiving conversational responses with tool calls (structured requests to backend modules) and citations (references to authoritative sources), enabling natural interaction while maintaining structured execution.

**Acceptance Scenarios**:

1. **Given** a user starts a conversation asking "What's capital gains tax?", **When** they engage in conversation (optionally with RAG enabled), **Then** the system retrieves relevant references, rules, and guidance about capital gains tax (if RAG enabled), augments the prompt with this context, generates a conversational explanation with citations to relevant References, and can handle follow-up questions in context with improved accuracy.

2. **Given** a user asks a financial question that requires calculation, **When** the conversation proceeds, **Then** the system generates tool calls (structured requests for calculations) while maintaining conversational context, enabling natural dialogue with structured execution.

3. **Given** a user asks follow-up questions that refine their original query, **When** the conversation continues, **Then** the system maintains conversation context, understands references to previous messages, and structures requests accordingly.

4. **Given** a user receives a calculation result and asks "Why did you recommend that?", **When** they continue the conversation, **Then** the system generates a tool call to retrieve provenance, then formats the explanation conversationally with citations.

---

### User Story 3 - Safety and PII Filtering (Priority: P1)

**User Story**: The system must protect user privacy and prevent exposure of sensitive information while enabling natural language processing. PII must be filtered before sending to external LLM providers, and safety checks must prevent inappropriate or harmful content.

**Why this priority**: Privacy and safety are non-negotiable requirements. Financial data is highly sensitive, and Australian privacy laws require strict data handling. Safety filtering prevents inappropriate content and maintains professional standards.

**Independent Test**: A user submits a query containing PII (e.g., "My super balance is $450,000"), and the system filters or redacts sensitive information before sending to LLM providers, while still enabling intent detection and parameter extraction.

**Acceptance Scenarios**:

1. **Given** a user's query contains PII (names, account numbers, exact balances), **When** the system processes it, **Then** it identifies and filters sensitive data before sending to external LLM providers, maintaining privacy while enabling intent detection.

2. **Given** a user's query contains inappropriate or harmful content, **When** the system processes it, **Then** it detects safety issues and either filters the content or returns an appropriate error response, preventing inappropriate interactions.

3. **Given** filtered PII is needed for calculations, **When** the system structures requests, **Then** it preserves the original data for internal use while ensuring external LLM providers never receive sensitive information.

4. **Given** a user's query is filtered for safety or privacy reasons, **When** the system responds, **Then** it provides clear, user-friendly messaging explaining why the query cannot be processed, without exposing technical filtering details.

---

### User Story 4 - Schema Validation and Error Handling (Priority: P2)

**User Story**: The system must validate that LLM outputs conform to expected schemas before they are used to generate structured requests. Invalid outputs must be caught and handled gracefully, preventing errors in downstream modules.

**Why this priority**: LLMs are probabilistic and can produce invalid outputs. Schema validation ensures that only valid structured requests reach Compute Engine and other backend modules. This prevents errors and maintains system reliability.

**Independent Test**: An LLM produces an output that doesn't conform to the expected schema (e.g., missing required fields, invalid data types), and the system validates it, detects the error, and either requests regeneration or returns a clear error to the client.

**Acceptance Scenarios**:

1. **Given** an LLM generates a structured request with missing required parameters, **When** the system validates it, **Then** it detects the missing fields and either requests the LLM to regenerate with corrections or returns a validation error to the client.

2. **Given** an LLM generates a structured request with invalid data types (e.g., text where a number is expected), **When** the system validates it, **Then** it detects the type mismatch and handles it appropriately, either correcting the type or requesting regeneration.

3. **Given** schema validation fails, **When** the system handles the error, **Then** it provides clear error messages to the client, enabling users to understand what went wrong and potentially rephrase their query.

4. **Given** validation errors occur frequently for a specific query pattern, **When** the system detects this, **Then** it may log the pattern for improvement while maintaining graceful error handling for users.

---

## From Frankie's Finance Specification

### User Story 1 - "What should I do?" Decision Guidance (Priority: P1)

**Consumer Story**: A user wants to ask Frankie questions like "Should I buy this property or keep renting?" or "Should I salary sacrifice more into super?" and receive clear, personalized guidance in plain English with simple visuals showing pros, cons, and long-term impacts.

**Why this priority**: This is the primary consumer value proposition. Users need personalized financial guidance that helps them make decisions. Without this capability, the app cannot deliver its core value of reducing financial anxiety and enabling informed decisions.

**Independent Test**: A user can ask "Should I contribute more to super?" in the living room, receive a conversational response with visual forecasts, see compliance validation, and understand the recommendation through explainable insights—all without feeling judged or overwhelmed.

**Acceptance Scenarios**:

1. **Given** a user opens Frankie's Finance and asks a financial question in the living room, **When** they submit the query, **Then** they receive a conversational response from the app (not Frankie) with personalized guidance, visual forecasts, and compliance validation results displayed in consumer-friendly language.

2. **Given** a user asks "Should I buy this property or keep renting?", **When** the system processes the question, **Then** it executes calculations, validates compliance, and presents pros, cons, and long-term impacts in simple visuals with plain English explanations.

3. **Given** a user receives financial advice, **When** they want to understand why a recommendation was made, **Then** they can access explainable insights tracing the recommendation back to rules and references, presented in consumer-friendly language without technical jargon.

4. **Given** compliance validation identifies issues with advice, **When** warnings are displayed, **Then** they appear in consumer-friendly language, explaining what the issue means and what actions might be needed, without exposing technical compliance details.

---

### User Story 2 - "Explain this to me." Financial Literacy Companion (Priority: P1)

**Consumer Story**: A user wants to ask Frankie to explain complex financial terms or rules ("What's capital gains tax?" or "How does negative gearing work?") so they can build their understanding of the financial system in simple, relatable language.

**Why this priority**: Financial literacy is essential for empowering users. Many users feel overwhelmed by financial jargon. This capability reduces anxiety, builds confidence, and enables users to make better-informed decisions.

**Independent Test**: A user can ask "What's capital gains tax?" and receive a clear, jargon-free explanation with visual analogies, links to authoritative sources, and the ability to ask follow-up questions naturally.

**Acceptance Scenarios**:

1. **Given** a user asks "What's capital gains tax?" in the living room, **When** the system processes the question, **Then** it provides a clear, jargon-free explanation using simple analogies and relatable language, with citations to authoritative sources for verification.

2. **Given** a user asks about a complex financial concept, **When** the explanation is provided, **Then** it uses visual metaphors, analogies, and interactive elements to make the concept understandable without requiring financial expertise.

3. **Given** a user wants to learn more after an explanation, **When** they ask follow-up questions, **Then** the system maintains conversation context and provides deeper explanations, building understanding progressively.

4. **Given** a user asks about a financial rule or regulation, **When** the explanation is provided, **Then** it includes citations to authoritative sources (References) that users can explore if they want more detail, building trust through transparency.

---

### User Story 3 - "Run the numbers." Scenario Simulation (Priority: P1)

**Consumer Story**: A user wants to test different financial scenarios ("What happens if I retire at 58 instead of 65?" or "If I invest $20k a year, how much will I have by 2040?") so they can make better-informed decisions using concrete projections and see long-term trade-offs.

**Why this priority**: Scenario exploration is essential for financial planning. Users need to see "what-if" outcomes to make informed decisions. This capability enables experimentation without fear and builds confidence through understanding.

**Independent Test**: A user can ask "What happens if I retire at 58 instead of 65?" in the study, view comparative forecasts with visual charts, adjust parameters using sliders, and see how outcomes change in real-time—all presented in an intuitive, playful way.

**Acceptance Scenarios**:

1. **Given** a user asks about a financial scenario in the study, **When** they submit the query, **Then** Frankie guides them to the study environment, and the system executes calculations, presenting results as visual forecasts with charts and projections.

2. **Given** a user wants to compare scenarios (e.g., retirement at 58 vs 65), **When** they request comparison, **Then** the system executes multiple scenario calculations and presents side-by-side comparisons with visual charts showing differences and trade-offs.

3. **Given** a user wants to adjust scenario parameters, **When** they use sliders or chat-driven prompts in the study, **Then** the system updates calculations in real-time, showing how outcomes change, with Frankie narrating what's happening.

4. **Given** a user explores scenarios, **When** they view results, **Then** each scenario is tagged and stored, enabling them to return to previous experiments and compare outcomes over time.

---

### User Story 4 - "Help me plan." Goal Setting & Tracking (Priority: P2)

**Consumer Story**: A user wants to log goals such as buying a house, paying off debt, or building super so that Frankie can help them stay intentional—reminding them of milestones, showing progress, and adjusting advice as their circumstances change.

**Why this priority**: Goal tracking provides motivation and accountability. Users need to see progress and feel supported in achieving their financial goals. This capability builds long-term engagement and helps users stay focused.

**Independent Test**: A user can set a goal (e.g., "Save $50k for a house deposit"), track progress in the garden, receive milestone reminders, and see how their financial decisions affect goal achievement through visual metaphors (trees growing, flowers blooming).

**Acceptance Scenarios**:

1. **Given** a user wants to set a financial goal, **When** they express the goal naturally (e.g., "I want to save for a house"), **Then** the system helps them define the goal with specific parameters (amount, timeline) and stores it for tracking.

2. **Given** a user has set goals, **When** they visit the garden, **Then** they see visual representations of their goals (trees, flowers) showing progress, with Frankie celebrating milestones and providing encouragement.

3. **Given** a user's financial circumstances change, **When** they update their situation, **Then** the system adjusts advice and goal projections accordingly, showing how changes affect goal achievement.

4. **Given** a user reaches a milestone, **When** progress is updated, **Then** Frankie celebrates visibly (running, wagging tail), the garden environment brightens, and the user receives positive reinforcement for their achievement.

---

### User Story 5 - "Am I on the right track?" Health & Progress Reports (Priority: P2)

**Consumer Story**: A user wants to receive periodic check-ins (monthly or quarterly) showing how their financial situation is evolving so they can see whether they're improving, identify risks early, and feel supported in achieving their long-term goals.

**Why this priority**: Regular check-ins provide ongoing support and help users stay engaged. Users need to see progress and feel supported over time. This capability builds long-term relationships and helps users maintain financial health.

**Independent Test**: A user receives a monthly check-in showing their financial health evolution, with visual indicators of progress, risk identification, and supportive messaging that helps them feel confident and motivated.

**Acceptance Scenarios**:

1. **Given** a user has been using the app, **When** a periodic check-in is triggered (monthly or quarterly), **Then** the system generates a progress report showing financial health evolution, goal progress, and risk indicators.

2. **Given** a progress report identifies risks or concerns, **When** it is presented, **Then** it uses supportive, non-alarming language, explains what the risks mean, and suggests actions users can take, maintaining an encouraging tone.

3. **Given** a progress report shows improvement, **When** it is presented, **Then** it celebrates achievements, reinforces positive behaviors, and provides motivation to continue, with Frankie visibly celebrating in the garden.

4. **Given** a user wants to review their financial health, **When** they request a progress report, **Then** the system generates it on-demand, showing current status, trends over time, and recommendations for improvement.

---

### User Story 6 - "See My Future." Easy-to-Use Forecasting (Priority: P2)

**Consumer Story**: A user wants to easily create forecasts of their financial future—like "What will my super look like at 65?" or "If I buy this house, how much will I have left each month?"—so they can understand where their money is heading without needing financial or technical expertise.

**Why this priority**: Forecasting helps users understand long-term implications of financial decisions. Users need simple, visual forecasts that feel playful and intuitive, not intimidating. This capability enables informed decision-making through understanding.

**Independent Test**: A user can ask "What will my super look like at 65?" using chat-driven prompts or sliders, see forecasts adjust live as parameters change, with Frankie narrating what's happening, and understand outcomes through simple charts and visualizations.

**Acceptance Scenarios**:

1. **Given** a user wants to forecast their financial future, **When** they ask a forecasting question or use chat-driven prompts ("Let's peek 10 years ahead"), **Then** the system executes calculations and presents forecasts as visual charts that adjust live as parameters change.

2. **Given** a user adjusts forecast parameters using sliders, **When** they change values, **Then** the system updates calculations in real-time, showing how outcomes change, with Frankie narrating what's happening in a playful, engaging way.

3. **Given** forecasting feels playful and visual, **When** forecasts are presented, **Then** they use intuitive charts, simple visualizations, and engaging interactions that make financial planning feel approachable rather than intimidating.

4. **Given** a user wants to understand forecast assumptions, **When** they explore deeper, **Then** the system provides explanations of assumptions used, enabling users to understand how forecasts are calculated without requiring technical knowledge.

---

## From Veris Finance Specification

### User Story 1 - "Model my client's scenario." Data-Driven Forecasting (Priority: P1)

**Adviser Story**: An adviser wants to enter or import a client's financial profile and run multiple scenarios so they can compare outcomes (e.g., retirement age, investment mix, contribution strategy) and produce deterministic forecasts backed by explainable rules.

**Why this priority**: This is the core professional workflow. Advisers need to model client scenarios quickly and accurately. Without this capability, advisers cannot provide value to clients or generate compliant advice.

**Independent Test**: An adviser can enter client data via natural language ("Add client aged 42 with $450k super") or structured input, create multiple scenarios, execute calculations, and view comparative forecasts with full provenance—all within a professional, efficient interface.

**Acceptance Scenarios**:

1. **Given** an adviser opens Veris Finance, **When** they input client information via natural language chat ("Add new client aged 42 with $450k super") or structured forms, **Then** the system stores client data and makes it available for scenario modelling and future advice sessions.

2. **Given** an adviser creates a client scenario, **When** they specify parameters (retirement age, investment mix, contribution strategy), **Then** the system executes deterministic calculations and presents forecasts with professional charts and visualizations.

3. **Given** an adviser wants to compare multiple scenarios, **When** they create scenario A, B, and C with different parameters, **Then** the system executes calculations for each scenario and presents side-by-side comparisons with clear visual differentiation.

4. **Given** an adviser views forecast results, **When** they examine the data, **Then** all calculations are traceable through explanation capabilities, with provenance chains linking to rules, references, and assumptions clearly displayed in the audit log.

---

### User Story 2 - "Check my advice for compliance." Best-Interests & Conduct Verification (Priority: P1)

**Adviser Story**: An adviser wants to validate their recommendations against the Code of Ethics and regulatory obligations so they can ensure every piece of advice is compliant, traceable, and ready for audit.

**Why this priority**: Compliance is non-negotiable for professional advisers. Every recommendation must meet regulatory requirements. This capability ensures advisers can confidently provide advice knowing it meets professional standards.

**Independent Test**: An adviser can submit advice recommendations for compliance checking, receive validation results with warnings and required actions, and see compliance status clearly displayed with links to regulatory requirements.

**Acceptance Scenarios**:

1. **Given** an adviser prepares advice recommendations, **When** they request compliance checking, **Then** the system validates best-interests duty, conflicts, documentation requirements, and product replacement logic, returning compliance outcomes.

2. **Given** compliance validation identifies issues, **When** warnings and required actions are generated, **Then** they are displayed clearly with specific guidance on what needs to be addressed, linked to relevant regulatory requirements.

3. **Given** an adviser needs to understand compliance requirements, **When** they query with context parameters, **Then** the system returns required actions, documentation, and professional standards applicable to their advice context.

4. **Given** compliance validation passes, **When** advice is approved, **Then** the system clearly indicates compliance status, enabling advisers to proceed with confidence.

---

### User Story 3 - "Generate the advice documents." Automated SOA/ROA Creation (Priority: P1)

**Adviser Story**: An adviser wants to produce a Statement or Record of Advice automatically from the client scenario so they can save time and guarantee consistency with their calculations and compliance results.

**Why this priority**: Document generation is a major time burden for advisers. Automated generation reduces administrative work while ensuring consistency between calculations, compliance results, and documentation. This directly supports the value proposition of reducing adviser burden.

**Independent Test**: An adviser can generate a Statement of Advice from a client scenario, and the document includes all calculations, compliance results, recommendations, and required disclosures, formatted consistently and ready for client presentation.

**Acceptance Scenarios**:

1. **Given** an adviser has completed client scenario modelling and compliance checking, **When** they request document generation, **Then** the system generates a Statement or Record of Advice including all calculations, compliance results, recommendations, and required disclosures.

2. **Given** a document is generated, **When** it is created, **Then** it includes traceable explanations linking to authoritative references, rule versions, and calculation assumptions, suitable for compliance packs.

3. **Given** a document includes compliance information, **When** it is generated, **Then** it incorporates compliance validation results, warnings, and required actions, ensuring documentation matches compliance status.

4. **Given** an adviser needs to export documentation, **When** they request export, **Then** the system provides documents in formats suitable for client presentation and regulatory submission, with full audit trails.

---

### User Story 4 - "Compare products and strategies." Evidence-Based Recommendations (Priority: P1)

**Adviser Story**: An adviser wants to test alternative products or strategies side-by-side so they can demonstrate to clients—and auditors—that their recommendation represents the client's best interest.

**Why this priority**: Advisers must demonstrate best-interests duty by comparing alternatives. This capability enables evidence-based recommendations and supports regulatory compliance. It's essential for professional practice.

**Independent Test**: An adviser can compare multiple strategies (e.g., "Compare debt-recycling vs offset-strategy over 10 years"), view side-by-side forecasts, and export comparison results showing how the recommended strategy serves the client's best interests.

**Acceptance Scenarios**:

1. **Given** an adviser wants to compare strategies, **When** they request comparison ("Compare debt-recycling vs offset-strategy over 10 years"), **Then** the system executes calculations for each strategy and presents comparative forecasts with professional charts showing differences and trade-offs.

2. **Given** strategy comparison results are displayed, **When** an adviser reviews them, **Then** they can see clear visual differentiation between strategies, with key differences highlighted and explained.

3. **Given** an adviser selects a recommended strategy, **When** they document the recommendation, **Then** the system enables them to explain why this strategy serves the client's best interests, with evidence from the comparison.

4. **Given** comparison results are used for client presentation, **When** they are exported, **Then** they include all calculations, assumptions, and visualizations needed to demonstrate best-interests duty to clients and auditors.

---

### User Story 5 - "Explain and justify my advice." Transparent Audit Trail (Priority: P1)

**Adviser Story**: An adviser wants to show regulators or clients why a recommendation was made so they can demonstrate transparency, ethical reasoning, and adherence to professional standards.

**Why this priority**: Auditability is essential for professional practice. Advisers must be able to justify recommendations to regulators and clients. This capability builds trust and ensures regulatory compliance.

**Independent Test**: An adviser can access the audit log for any recommendation, see the complete reasoning chain (Fact → Rule → Reference → Assumptions), and export audit trails suitable for regulatory review or client explanation.

**Acceptance Scenarios**:

1. **Given** an adviser has generated advice, **When** they access the audit log, **Then** they see a transparent record of all advice logic, calculations, compliance checks, and changes, with timestamps and reasoning trails.

2. **Given** an adviser needs to explain a recommendation, **When** they request explanation via `/explain/{fact_id}`, **Then** the system provides a human-readable trace showing Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions with versions and dates.

3. **Given** an adviser needs to justify advice to regulators, **When** they export audit trails, **Then** the system provides complete provenance chains with all calculations, compliance results, and regulatory references, suitable for regulatory submission.

4. **Given** an adviser needs to explain advice to clients, **When** they access explanations, **Then** the system provides client-friendly versions that explain recommendations clearly while maintaining technical accuracy for professional use.

---

### User Story 6 - "Forecast with Precision." Professional Forecasting Engine (Priority: P2)

**Adviser Story**: An adviser wants to build accurate financial forecasts for clients quickly and confidently so they can model outcomes, stress-test strategies, and present compliant projections backed by deterministic rules and assumptions.

**Why this priority**: Forecasting is essential for financial planning. Advisers need precise, reliable forecasts that can be stress-tested and validated. This capability enables confident client presentations and strategy evaluation.

**Independent Test**: An adviser can create financial forecasts quickly, adjust assumptions, stress-test scenarios, and present projections with confidence that they are backed by deterministic rules and can be explained and validated.

**Acceptance Scenarios**:

1. **Given** an adviser wants to create a financial forecast, **When** they specify client data and assumptions, **Then** the system executes calculations and presents professional forecasts with clear visualizations and key metrics.

2. **Given** an adviser wants to stress-test a strategy, **When** they vary assumptions (e.g., different return rates, contribution amounts), **Then** the system executes sensitivity analysis, showing how outcomes change with assumption variations.

3. **Given** forecasts are presented to clients, **When** they are displayed, **Then** they use professional charts and visualizations with consistent formatting, clear legends, and appropriate detail levels for client understanding.

4. **Given** forecasts are based on deterministic rules, **When** they are generated, **Then** all assumptions and rule versions are clearly documented, enabling advisers to explain forecasts and demonstrate compliance.
