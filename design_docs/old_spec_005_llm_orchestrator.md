# Feature Specification: LLM Orchestrator

**Feature Branch**: `005-llm-orchestrator`  
**Created**: 2025-01-27  
**Status**: Draft  
**Input**: LLM Orchestrator module - translates human language into structured, auditable requests. Stateless translator and router that performs intent detection, schema validation, safety/PII filtering, prompt templating, and model vendor routing. Never the source of truth.

**Purpose**: This module translates natural language intent into structured compute requests that can be executed by the Compute Engine. It serves as a stateless translator and router, performing intent detection, schema validation, safety/PII filtering, prompt templating, model vendor routing, and RAG (Retrieval-Augmented Generation) capability. The RAG capability retrieves relevant structured data (rules, references, assumptions, advice guidance, client outcome strategies) from the relational database via References & Research Engine APIs to augment LLM prompts, improving intent detection accuracy, parsing quality, and conversational response relevance. Critically, LLMs MUST NEVER determine financial outcomes or replace rule logic—they only structure requests; rules and the deterministic engine determine outcomes. RAG must comply with Principle IV: retrieved data grounds prompts but does not make LLM the source of truth.

**Reference**: This module implements requirements from the master specification (`001-master-spec/spec.md`), specifically FR-004D, FR-013, FR-014, and FR-015.

## Architectural Boundaries

**LLM Orchestrator** is a thin natural-language router and controller. Per Constitution Principle XII:

- **MUST**: Interpret user input and detect intent; build structured requests for the three engines (Compute, References, Advice); call engines in correct sequence; validate and repair schemas; turn structured outputs back into user-facing text; handle PII filtering and safety checks.

- **MUST NOT**: Invent rules, tax formulas, caps, or thresholds; perform calculations or numeric operations; override deterministic outputs from Compute Engine or Advice Engine; store knowledge objects (it queries References & Research Engine); contain business logic or decision-making rules; replace rule logic or calculation logic.

LLM Orchestrator serves as a translation layer between natural language and structured APIs. Keeping it thin ensures that all business logic, calculations, and knowledge remain in their designated components.

---

## Clarifications

This section addresses ambiguous areas in the specification to eliminate implementation uncertainty.

### Session 2025-01-27

- Q: What should happen when an LLM provider (via OpenRouter) is unavailable or returns an error, and how should the system handle retries or fallbacks? → A: Retry with exponential backoff up to 3 times, then return structured error (503 Service Unavailable) with remediation guidance

- Q: What should happen when PII filtering removes critical information needed for intent detection (e.g., user says "My super balance is $450k" but the balance gets filtered)? → A: Preserve filtered PII internally, use anonymized version for LLM (e.g., "super balance is [AMOUNT]"), restore original values for downstream modules

- Q: What should happen when a conversation context exceeds LLM token limits (e.g., very long conversation history)? → A: Summarize or truncate oldest messages, maintain recent context, return warning if truncation occurs

- Q: What should happen when schema validation fails after all retry attempts are exhausted (3 retries with repair logic)? → A: Return 422 Unprocessable Entity with clear user-friendly message suggesting query rephrasing, without exposing internal schema details

- Q: What should happen when a user's query is ambiguous and the system cannot determine intent with sufficient confidence (e.g., query could be interpreted multiple ways)? → A: Return structured response requesting clarification, listing possible interpretations for user to choose

---

## User Scenarios & Testing

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

### Edge Cases

- What happens when an LLM provider is unavailable or returns an error? The system MUST gracefully handle provider failures, potentially routing to alternative providers, and return appropriate error messages to clients.

- How does the system handle queries in languages other than English? The system MUST either support multi-language processing or return clear messages indicating language limitations, focusing on English/Australian English for MVP.

- What happens when an LLM generates a request that would violate system constraints (e.g., requesting calculations with invalid parameters)? The system MUST validate requests against system constraints before forwarding to Compute Engine, preventing invalid operations.

- How does the system handle very long or complex queries that exceed LLM context limits? The system MUST either chunk queries appropriately, summarize context, or return clear messages indicating query complexity limits.

- What happens when an LLM produces inconsistent outputs across multiple attempts? The system MUST handle probabilistic outputs appropriately, using validation and potentially retry logic, while maintaining deterministic outcomes in downstream modules.

- How does the system handle queries that require information not available in the system? The system MUST identify missing information requirements and return structured responses indicating what data is needed, enabling clients to request clarification or provide additional information.

- What happens when RAG retrieval returns no relevant data? The system MUST gracefully handle cases where retrieval returns no results, proceeding with standard LLM processing without RAG augmentation and logging the retrieval failure for monitoring.

- How does the system handle retrieval queries that return too many results? The system MUST limit retrieval results to the most relevant items (e.g., top 5-10 results) and use relevance scoring to select the best matches for prompt augmentation.

- What happens when retrieved data conflicts with LLM-generated content? The system MUST prioritize retrieved authoritative data in prompt augmentation, but all outputs affecting calculations MUST still be validated against deterministic rules in the Compute Engine. LLM remains a translator; retrieved data grounds prompts but does not make LLM the source of truth.

- How does the system handle retrieval latency that exceeds performance requirements? The system MUST implement caching for frequent retrievals in Redis, use cheaper models for retrieval queries, and ensure retrieval adds less than 1 second latency (p95) to maintain acceptable response times.

- What happens when retrieved data contains tenant-specific information? The system MUST ensure retrieved data respects tenant isolation (RLS) and PII redaction, preventing cross-tenant data leakage in RAG-augmented prompts.

- How does the system handle retrieval for queries that span multiple effective dates or ruleset versions? The system MUST retrieve data respecting effective dates and ruleset versions, using the appropriate `as_of` date context from the user query or conversation.

---

## Requirements

### Functional Requirements

#### Intent Detection and Parsing

- **FR-001**: System MUST detect user intent from natural language queries, identifying the type of request (calculation, explanation, comparison, information request) and extracting relevant parameters.

- **FR-002**: System MUST extract structured parameters from natural language queries, identifying client data, scenario parameters, time horizons, and other inputs needed for calculations or advice.

- **FR-003**: System MUST identify missing required parameters in user queries and return structured responses indicating what information is needed, enabling clients to request clarification.

- **FR-004**: System MUST handle ambiguous queries by either requesting clarification or making reasonable inferences based on context, while maintaining transparency about assumptions made. When a user's query is ambiguous and the system cannot determine intent with sufficient confidence, the system MUST return a structured response requesting clarification, listing possible interpretations for the user to choose from.

- **FR-005**: System MUST provide intent parsing capability that accepts natural language queries and returns structured output indicating detected intent, extracted parameters, and the next action to take.

#### Conversational Interface

- **FR-006**: System MUST provide conversational chat capability that accepts message history and returns conversational responses with tool calls and citations.

- **FR-007**: System MUST maintain conversation context across multiple turns, understanding references to previous messages and maintaining coherent dialogue. When conversation context exceeds LLM token limits, the system MUST summarize or truncate oldest messages, maintain recent context, and return a warning if truncation occurs to inform users that older context may not be available.

- **FR-008**: System MUST generate tool calls (structured requests to backend modules) within conversational responses, enabling natural dialogue with structured execution.

- **FR-009**: System MUST include citations to authoritative sources (References) in conversational responses, enabling users to verify information and building trust.

- **FR-010**: System MUST format conversational responses appropriately for different audiences: consumer-friendly language for Frankie's Finance, professional language for Veris Finance.

#### Safety and Privacy

- **FR-011**: System MUST filter PII (personally identifiable information) before sending queries to external LLM providers, maintaining privacy while enabling intent detection.

- **FR-012**: System MUST detect and filter inappropriate or harmful content, preventing safety issues and maintaining professional standards.

- **FR-013**: System MUST preserve filtered PII for internal use (Compute Engine, Advice Engine) while ensuring external LLM providers never receive sensitive information. When PII filtering removes critical information needed for intent detection, the system MUST preserve the filtered PII internally, use an anonymized version for LLM (e.g., replacing "$450k" with "[AMOUNT]" or "super balance is [AMOUNT]"), and restore original values for downstream modules (Compute Engine, Advice Engine).

- **FR-014**: System MUST provide clear, user-friendly messaging when queries are filtered for safety or privacy reasons, without exposing technical filtering details.

#### Schema Validation

- **FR-015**: System MUST validate all LLM outputs against expected schemas before they are used to generate structured requests, ensuring data types, required fields, and constraints are met.

- **FR-016**: System MUST detect schema validation errors (missing fields, invalid types, constraint violations) and handle them gracefully, either requesting regeneration or returning clear error messages.

- **FR-017**: System MUST validate that structured requests conform to calculation service requirements before forwarding them, preventing invalid operations.

- **FR-018**: System MUST provide clear error messages when validation fails, enabling users to understand what went wrong and potentially rephrase their queries.

#### Schema Validation Retry and Repair

- **FR-019**: System MUST retry schema validation failures up to 3 times before failing the request, using exponential backoff with initial delay 1 second, doubling on each retry (1s, 2s, 4s), maximum delay 4 seconds. Reference: `specs/001-master-spec/spec.md` CL-035.

- **FR-020**: System MUST implement repair logic including: type coercion (attempting to coerce invalid types to expected types when safe and unambiguous, e.g., string "123" → number 123), default values (applying default values for optional missing fields when reasonable defaults exist), and field name normalization (attempting to match similar field names with case-insensitive, underscore/hyphen normalization when exact match fails). Reference: `specs/001-master-spec/spec.md` CL-035.

- **FR-021**: System MUST request LLM to regenerate output with explicit error feedback about what failed validation if repair logic cannot fix the error. Reference: `specs/001-master-spec/spec.md` CL-035.

- **FR-022**: System MUST retry transient LLM errors (rate limits, timeouts), schema validation failures that can be repaired, and missing optional fields. System MUST fail fast for structural schema mismatches (completely wrong structure), invalid required fields that cannot be repaired, and security violations (malformed requests, injection attempts). Reference: `specs/001-master-spec/spec.md` CL-035.

- **FR-023**: System MUST return clear error messages to client indicating what validation failed and suggesting how user might rephrase their query when retries are exhausted. Error messages MUST NOT expose internal schema details or LLM provider information. When schema validation fails after all retry attempts are exhausted (3 retries with repair logic), the system MUST return 422 Unprocessable Entity error with clear user-friendly message suggesting query rephrasing, without exposing internal schema details. Reference: `specs/001-master-spec/spec.md` CL-035.

- **FR-024**: System MUST log all validation failures with error patterns, retry counts, and success/failure outcomes. Validation failure patterns MUST be tracked for system improvement. High validation failure rates MUST trigger alerts for investigation. Reference: `specs/001-master-spec/spec.md` CL-035.

#### Model Vendor Routing

- **FR-025**: System MUST use OpenRouter for all LLM interactions, supporting both OpenRouter credits and BYOK (Bring Your Own Key) integration. System MUST support routing to multiple models via OpenRouter's unified API with configurable model selection logic.

- **FR-025A**: System MUST prefer models that do not train on prompts, using OpenRouter's data policy filtering features (see https://openrouter.ai/docs/features/privacy-and-logging). System MAY select models that train on prompts only if such selection would significantly compromise performance metrics (e.g., >20% degradation in accuracy/latency) or increase pricing by more than 50% compared to no-training models.

- **FR-026**: System MUST handle OpenRouter API failures gracefully, leveraging OpenRouter's automatic fallback capabilities or returning appropriate error messages. When an LLM provider (via OpenRouter) is unavailable or returns an error, the system MUST retry with exponential backoff up to 3 times (initial delay: 1s, doubling on each retry: 1s, 2s, 4s), then return structured error (503 Service Unavailable) with remediation guidance if all retries fail.

- **FR-027**: System MUST support prompt templating, enabling consistent prompt structure across different models via OpenRouter while maintaining flexibility.

- **FR-028**: System MUST enforce rate limiting per tenant, preventing abuse and managing costs. Rate limits may be managed by OpenRouter (when using OpenRouter credits) or by the underlying provider (when using BYOK).

#### Stateless Architecture

- **FR-029**: System MUST operate as a stateless translator and router, not maintaining persistent state between requests (conversation context may be maintained by clients).

- **FR-030**: System MUST never determine financial outcomes or replace rule logic; LLMs only structure requests; rules and deterministic engine determine outcomes.

- **FR-031**: System MUST validate all LLM outputs that affect calculations against rules before execution, ensuring LLM outputs are checked before being used.

#### Integration

- **FR-032**: System MUST transform natural language queries into structured calculation requests.

- **FR-033**: System MUST retrieve references for citation generation and context enhancement in conversational responses.

- **FR-034**: System MUST provide natural language processing for consumer queries with consumer-friendly formatting.

- **FR-035**: System MUST provide natural language processing for adviser queries with professional formatting.

#### Access Requirements

- **FR-036**: System MUST provide intent parsing capability returning detected intent, extracted parameters, and next action, and conversational chat capability returning messages, tool calls, and citations.

- **FR-037**: System MUST enforce access control with tenant isolation and rate limits as specified in the master specification (see CL-031 and FR-030 for security guarantee that User A can NEVER see User B's data under ANY circumstances).

- **FR-037A**: System MUST include automated security tests that verify cross-tenant data access is impossible for all LLM Orchestrator endpoints. Tests MUST simulate bugs, misconfigured queries, malicious input, missing tenant context, and other failure scenarios to ensure User A cannot access User B's conversation history, extracted parameters, or LLM-generated content under any conditions (see FR-030A in master specification).

- **FR-038**: System MUST support idempotency for LLM requests where appropriate, enabling safe retries while managing LLM provider costs.

#### RAG (Retrieval-Augmented Generation) Capability

##### RAG Retrieval

- **FR-041**: System MUST retrieve relevant structured data (rules, references, assumptions, advice guidance, client outcome strategies) from the relational database via References & Research Engine APIs (`/references/search`, `/references/{id}`) to augment LLM prompts.

- **FR-042**: System MUST support semantic search or keyword-based queries on the relational database for retrieval, using existing PostgreSQL with JSONB for metadata (no new data stores required).

- **FR-043**: System MUST retrieve data respecting tenant isolation (RLS) and PII redaction, ensuring User A cannot access User B's data through RAG retrieval under any circumstances.

- **FR-044**: System MUST limit retrieval results to the most relevant items (e.g., top 5-10 results) using relevance scoring, preventing prompt bloat from excessive retrieved data.

- **FR-045**: System MUST handle cases where no relevant data is found gracefully, proceeding with standard LLM processing without RAG augmentation and logging retrieval failures for monitoring.

- **FR-046**: System MUST respect effective dates and ruleset versions when retrieving data, using appropriate `as_of` date context from user queries or conversation history.

##### Prompt Augmentation

- **FR-047**: System MUST augment LLM prompts with retrieved structured data, integrating retrieved context into prompts for intent detection, parsing, and conversational responses.

- **FR-048**: System MUST format retrieved data appropriately for prompt augmentation, ensuring retrieved context is clear, relevant, and does not exceed LLM context limits.

- **FR-049**: System MUST prioritize retrieved authoritative data in prompt augmentation, but all outputs affecting calculations MUST still be validated against deterministic rules in the Compute Engine (LLM remains a translator; retrieved data grounds prompts but does not make LLM the source of truth).

- **FR-050**: System MUST include citations to retrieved sources in conversational responses, enabling users to verify information and building trust.

##### RAG API Integration

- **FR-051**: System MUST enhance `/llm/parse` API to optionally include RAG via a `use_rag` flag in requests, enabling clients to opt-in to RAG-enhanced parsing.

- **FR-052**: System MUST enhance `/llm/chat` API to optionally include RAG via a `use_rag` flag in requests, enabling clients to opt-in to RAG-enhanced conversational responses.

- **FR-053**: System MUST add a new internal tool or step for retrieval, integrating RAG retrieval into the LLM Orchestrator workflow without disrupting existing functionality.

- **FR-054**: System MUST maintain backward compatibility: when `use_rag` is not specified or set to false, the system MUST operate without RAG augmentation, preserving existing behavior.

##### RAG Model Routing and Performance

- **FR-055**: System MUST use cheaper models (e.g., gpt-5-mini) for retrieval queries, optimizing cost while maintaining retrieval quality.

- **FR-056**: System MUST switch to higher-capability models (e.g., gpt-5.1) for generation when needed, enabling intelligent model selection based on query complexity and requirements.

- **FR-057**: System MUST ensure retrieval adds less than 1 second latency (p95) to maintain acceptable response times, implementing caching and optimization strategies as needed.

- **FR-058**: System MUST cache frequent retrievals in Redis, reducing latency for common queries and improving performance.

##### RAG Constitution Compliance

- **FR-059**: System MUST comply with Principle IV: LLM remains a translator only; retrieved data grounds prompts but does not make LLM the source of truth.

- **FR-060**: System MUST validate all outputs affecting calculations against deterministic rules in the Compute Engine, ensuring RAG-augmented prompts do not bypass rule validation.

- **FR-061**: System MUST ensure retrieved data is used for prompt augmentation only, not for direct calculation or decision-making, maintaining the separation between LLM translation and deterministic computation.

##### RAG Privacy and Security

- **FR-062**: System MUST ensure retrieved data respects tenant isolation (RLS) at the database level, preventing cross-tenant data access in RAG retrieval.

- **FR-063**: System MUST ensure retrieved data respects PII redaction policies, preventing sensitive information from appearing in RAG-augmented prompts sent to external LLM providers.

- **FR-064**: System MUST log all RAG retrieval operations for audit purposes, including query terms, retrieved items, and relevance scores, while maintaining PII redaction in logs.

##### RAG Testing and Quality

- **FR-065**: System MUST include unit tests for retrieval accuracy, ensuring 95% relevance for retrieved data when validated against manually curated test queries.

- **FR-066**: System MUST include integration tests for RAG functionality, testing end-to-end flows from user query through retrieval, prompt augmentation, and LLM response generation.

- **FR-067**: System MUST include end-to-end tests via Veris/Frankie's UIs, validating RAG functionality in real user scenarios.

- **FR-068**: System MUST include golden dataset validation, testing RAG retrieval against known-good query-result pairs to ensure consistency and accuracy.

- **FR-069**: System MUST include property-based tests for edge cases (e.g., no relevant data found, excessive results, conflicting data), ensuring robust handling of edge conditions.

---

### Key Entities

- **Intent**: Detected purpose or goal of a user query. Attributes include: intent type (calculation, explanation, comparison, information_request), confidence score, extracted parameters, and suggested next actions. Used to route queries to appropriate backend modules.

- **Structured Request**: Transformed natural language query ready for backend module execution. Attributes include: request type (calculation, explanation, compliance_check), target service, parameters (client data, scenario parameters), and validation status. Generated by LLM Orchestrator, consumed by backend modules.

- **Conversation Context**: Maintained dialogue state for multi-turn conversations. Attributes include: conversation identifier, message history, detected intents, extracted parameters, and conversation metadata. May be maintained by clients or temporarily by LLM Orchestrator for conversation continuity.

- **Tool Call**: Structured request to a backend module generated within a conversational response. Attributes include: tool identifier (e.g., "compute_engine.run"), parameters, and expected response format. Enables natural dialogue with structured execution.

- **Citation**: Reference to an authoritative source included in conversational responses. Attributes include: reference identifier, pinpoint (if applicable), excerpt text, and relevance score. Links conversational responses to authoritative sources for verification.

- **PII Filter**: Configuration and rules for identifying and filtering personally identifiable information. Attributes include: filter rules, redaction patterns, and handling policies. Ensures privacy while enabling intent detection.

- **Retrieved Context**: Structured data retrieved from the relational database to augment LLM prompts. Attributes include: retrieved items (rules, references, assumptions, advice guidance, client outcome strategies), relevance scores, source identifiers, effective dates, and retrieval metadata. Used to ground LLM prompts with authoritative financial data.

- **RAG Query**: Search query used to retrieve relevant structured data. Attributes include: query terms (semantic or keyword-based), filters (effective dates, ruleset versions, tenant context), result limits, and relevance thresholds. Used to identify and retrieve relevant data for prompt augmentation.

- **Prompt Augmentation**: Enhanced LLM prompt that includes retrieved context. Attributes include: original prompt, retrieved context, formatting instructions, citation requirements, and augmentation metadata. Used to improve LLM accuracy by grounding prompts with authoritative data.

- **Retrieval Cache**: Cached retrieval results stored in Redis for performance optimization. Attributes include: cache key (based on query terms and filters), cached results, expiration timestamp, and hit/miss statistics. Used to reduce latency for frequent queries.

---

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

---

## Assumptions

### Domain Assumptions

- Users will primarily interact in English/Australian English, enabling focus on English language processing for MVP.

- Natural language queries will follow common patterns (questions, commands, statements) that can be detected and parsed with reasonable accuracy.

- Financial terminology and concepts will be consistent enough to enable reliable intent detection and parameter extraction.

- Users will provide sufficient context in their queries to enable intent detection, or will respond to clarification requests.

### Technical Assumptions

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

### Integration Assumptions

- Calculation services will accept structured requests generated by LLM Orchestrator and execute them deterministically.

- Reference lookup services will provide reference lookups with acceptable performance for citation generation.

- Consumer and adviser applications will maintain conversation context and handle tool calls generated by LLM Orchestrator.

- Backend modules will return structured responses that LLM Orchestrator can format conversationally for users.

- References & Research Engine APIs (`/references/search`, `/references/{id}`) will provide the necessary retrieval capabilities, enabling RAG integration without requiring new APIs or data access patterns.

- Tenant isolation (RLS) will be enforced at the database level, ensuring RAG retrieval respects tenant boundaries without requiring additional application-level filtering.

- PII redaction will be applied consistently across retrieved data, ensuring sensitive information is not included in RAG-augmented prompts sent to external LLM providers.

- Compute Engine will continue to validate all calculation-affecting outputs against deterministic rules, ensuring RAG augmentation does not bypass rule validation.

---

## Scope Boundaries

### In Scope (MVP)

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

### Out of Scope (Future)

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

---

## Dependencies

### External Dependencies

- OpenRouter API for unified LLM provider access (supporting both OpenRouter credits and BYOK integration)

- OpenRouter will maintain acceptable performance, reliability, and API stability

- Network connectivity to OpenRouter API with acceptable latency

- OpenAI API key (via OpenRouter BYOK) for using existing OpenAI credits through OpenRouter's unified interface

- PostgreSQL database with JSONB support for metadata storage and search (for RAG retrieval)

- Redis for caching frequent RAG retrievals

### Internal Dependencies

- Master specification (`001-master-spec`) for system context, requirements, and architectural constraints

- Calculation services for executing structured calculation requests transformed from natural language

- References & Research Engine module (`003-references-research-engine`) for data retrieval APIs (`/references/search`, `/references/{id}`) used by RAG capability

- Compute Engine module for validation of calculation-affecting outputs (ensuring RAG-augmented prompts do not bypass rule validation)

- Authentication/authorization system for access control (from foundational infrastructure)

- Logging and observability infrastructure for monitoring LLM usage, errors, and performance
