<!--
Sync Impact Report:
Version: 2.6.1 (Canonical Concepts simplification and data model separation)
Ratified: 2025-01-27
Last Amended: 2025-01-27

Changes:
- Simplified Canonical Concepts section: removed detailed attribute lists and state machines, replaced with concise prose summaries
- Created canonical_data_model.md: extracted detailed schemas, fields, and lifecycle definitions to separate file
- Added note in Canonical Concepts section pointing to canonical_data_model.md for detailed schemas

Added sections:
- canonical_data_model.md (NEW): Detailed data model documentation for all 14 canonical concepts

Modified sections:
- Canonical Concepts: Simplified descriptions while preserving all 14 concepts and their meaning
  - Rule: Condensed to prose summary of attributes
  - Reference: Condensed to prose summary of attributes
  - Assumptions: Condensed to prose summary of attributes
  - Advice Guidance: Added brief attribute summary
  - Client Outcome Strategy: Added brief attribute summary
  - Scenario: Added brief attribute summary
  - Client Event: Condensed to prose summary of attributes
  - Input: Added brief attribute summary
  - Fact: Condensed to prose summary of attributes
  - Finding: Added lifecycle reference, condensed to prose summary
  - Research Question: Added brief attribute summary
  - Verdict: Removed explicit state machine, added lifecycle reference
  - Provenance Link: Condensed to prose summary of attributes
  - Ruleset Snapshot: Added brief attribute summary

Templates requiring updates:
- ✅ plan-template.md (Constitution Check section references constitution)
- ✅ spec-template.md (should align with canonical concepts and principles)
- ✅ tasks-template.md (should align with principles and workflow and document three-agent chat structure)
- ⚠️ Note: canonical_data_model.md is new and should be referenced by specs/plans that need detailed schema information

Follow-up TODOs: None
-->

# App Version 5 Constitution

**Status**: ✅ **Ready for Implementation**

---

## Mission Statement

Convert the Australian financial system into **auditable rules** and a **deterministic calculation engine**, surfaced through human-centred experiences. The system replaces the technical work of a human adviser while preserving judgement, transparency, and auditability.

**One-Sentence Charter**: App Version 5 is an *explainable*, *deterministic*, *spec-driven* system that turns Australian financial sources into governed rules and reproducible forecasts—delivered through a humane consumer world (Frankie's Finance), a calm professional console (Veris Advice), and a partner API—with provenance you can trust and outcomes you can audit.

---

## Core Principles

### I. Deterministic, Rule-Based Forecasting (NON-NEGOTIABLE)

All financial calculations MUST be deterministic and reproducible. **Compute Engine** is the single source of truth for all deterministic financial logic, including tax formulas, caps, thresholds, eligibility tests, and projections. The calculation engine MUST use explicit rules with pinned versions (`ruleset_id`, `as_of` date). Same inputs + same ruleset/date MUST produce identical outputs.

All numeric tolerances and rounding standards MUST be explicit. Facts are immutable with full provenance (rule versions, inputs hash, scenario id, units, rounding). No other component may perform numeric calculations or override deterministic outputs from Compute Engine.

**Rationale**: Financial advice requires absolute accuracy and auditability. Non-deterministic calculations undermine trust and compliance. Reproducibility enables verification, debugging, and regulatory compliance. The Australian financial system is built on precise legal and regulatory requirements that demand algorithmic precision. Centralizing all calculation logic in Compute Engine ensures consistency, testability, and auditability.

### II. Transparent, Auditable Advice (NON-NEGOTIABLE)

Every computed result (Fact) MUST have end-to-end provenance traceable through `/explain` endpoints. Provenance chains MUST link:

**Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions**

All chains MUST include versions and dates. All recommendations MUST be exportable for compliance packs. The system MUST support time-travel queries using effective dates and ruleset versions.

**Rationale**: Australian financial advice regulations (Corporations Act 2001, Code of Ethics) require advisers to demonstrate best interests duty and traceability. Clients and regulators must be able to audit why advice was given, how calculations were performed, and what authoritative sources were used. Every number must be traceable to its legal or regulatory foundation.

### III. Relational Database Architecture (MANDATORY)

The system MUST use a relational database-only storage model (no graph databases):

- **Relational Database**: All data storage including canonical governance (rule definitions, effective windows, precedence, review workflow, assumptions snapshots, change logs), execution data (scenarios, facts, provenance links), and explainability (provenance chains, relationship storage, time-travel queries).

Rules MUST be authored directly in the relational database. All execution, explainability, and provenance queries MUST use relational database capabilities:
- Efficient provenance chain traversal for `/explain` queries
- Flexible relationship storage and querying
- Built-in or implemented `as_of` time-travel query support
- Indexes optimized for explain path queries and fact lookups

**Rationale**: Relational database-only architecture provides faster `/explain` queries compared to graph databases, full auditability via relational query capabilities, built-in or implemented temporal query support for time-travel queries, and significantly lower operational costs. Relational databases' mature ecosystem, strong ACID guarantees, and rich query capabilities fully support deterministic calculations, provenance chains, and explainability requirements without the complexity and performance overhead of a hybrid architecture.

### IV. LLM as Translator, Not Source of Truth

LLM orchestration MUST translate natural language intent into structured compute requests. LLMs MUST NEVER determine financial outcomes or replace rule logic. The LLM structures requests; **rules + deterministic engine** determine outcomes.

The **LLM Orchestrator** is a thin, stateless translator and router that serves as:
- Intent detection and schema validation
- Safety/PII filtering
- Prompt templating and model vendor routing
- Natural language to structured request translation
- Coordination of calls to Compute Engine, References & Research Engine, and Advice Engine

The LLM Orchestrator MUST NOT invent rules, perform calculations, override deterministic outputs, store knowledge objects, or contain business logic. It is **never the source of truth** and does not replace rule logic or calculation logic.

All LLM outputs that affect calculations MUST be validated against rules before execution. The LLM Orchestrator builds structured requests and calls the appropriate engines; it does not make business decisions or perform computations.

**LLM Provider Integration**: The MVP MUST use OpenRouter for all LLM interactions. The system MUST support both OpenRouter credits and BYOK (Bring Your Own Key) integration, allowing use of existing OpenAI API keys via OpenRouter's unified interface. This enables cost optimization, unified rate limit management, and provider fallback capabilities while maintaining a single integration point.

**Rationale**: LLMs are probabilistic and cannot guarantee accuracy. Financial advice requires deterministic, rule-based outcomes traceable to authoritative sources. LLMs serve as a user-friendly interface layer, not a calculation layer or business logic layer. The Australian financial system demands precision that probabilistic systems cannot provide. Keeping the Orchestrator thin ensures that all business logic, calculations, and knowledge remain in their designated components. OpenRouter provides a unified API that simplifies provider management, enables cost optimization through BYOK, and provides automatic fallback capabilities while maintaining a single integration point.

### V. Specification-Driven Development

All rules, references, assumptions, advice guidance, and client outcome strategies MUST be authored as structured artifacts (Markdown/YAML) with:

- Schema validation
- Tests, examples, and edge cases
- Narrative summaries explaining purpose and application
- Version tags and effective date windows
- Two-person review before publication (four-eyes principle)

Repository hygiene MUST maintain versioned artifacts with effective-date time travel and signed bundles. Rules MUST be published directly to the relational database; all rule changes originate from versioned artifacts.

**Rationale**: Specification-driven development ensures consistency, testability, and maintainability. Human-readable artifacts enable review, audit, and collaboration. Versioning enables reproducibility and change tracking. The Australian financial system's complexity requires systematic, traceable rule management.

### VI. Frontend-Agnostic Backend

The backend MUST be frontend-agnostic and accessible only through documented APIs. Direct end-user backend access is FORBIDDEN. All access MUST be mediated by:

- **Frankie's Finance** (consumer mobile UX)
- **Veris Advice** (adviser professional console)
- **Partner API** (third-party integrations)

The Partner API MUST match internal capabilities with no logic forks. Different auth scopes and UI tones are handled by client applications; backend logic remains consistent.

**Rationale**: Frontend-agnostic design enables multiple client experiences (consumer, adviser, partner) while maintaining a single source of truth. API-first design supports integration and future clients. This separation allows UI evolution without affecting core calculation logic.

### VII. Experience Principles

**For Consumers (Frankie's Finance)**:
- Emotion-first design with non-linear navigation
- Frankie is a **companion** (not the adviser); the app provides the advice voice
- Intent drives movement through spatial metaphors (path → front door → living room/study/garden)
- Questions drive where the user goes; no rigid phases
- Human-centred, non-judgemental onboarding

**For Advisers (Veris Advice)**:
- Professional calm with minimal chrome, clear hierarchy
- Comparative dashboards and audit log always available
- LLM chat interface for natural language input
- Data-centric UI for visualizing strategies and forecasts
- Fast, compliant forecasting, comparisons, and documentation

**Universal**: Navigation by intent—the user's question dictates the next view; the system brings the right module to them.

**Rationale**: Different user segments have different emotional and functional needs. Consumer experience must reduce anxiety and shame around financial decisions. Adviser experience must prioritize speed, clarity, and compliance. Both must enable natural interaction while maintaining deterministic outcomes.

### VIII. Reproducibility Over Convenience

Every compute operation MUST pin `ruleset_id` and `as_of` date. Convenience features that sacrifice reproducibility are FORBIDDEN. All runs MUST be idempotent with explicit idempotency keys.

Scenarios represent tagged alternative futures that never overwrite base reality. Historical queries MUST use time-travel capabilities. Facts are immutable; new calculations create new facts.

**Rationale**: Financial advice requires auditability and verification. Reproducibility enables debugging, compliance verification, and client confidence. The Australian regulatory environment demands that advice can be reconstructed and verified. Convenience cannot compromise accuracy or traceability.

### IX. Precedence and Temporal Logic

Rule resolution MUST respect authority rank:

**Act > Regulation > Ruling > Guidance > Assumption**

Effective date windows MUST be strictly enforced. Temporal queries MUST use `as_of` dates to determine applicable rules. Conflicts between rules at the same precedence level MUST be explicitly documented and resolved through review workflow.

All rules MUST include:
- Effective dates (when they start/end)
- Precedence level
- Status (Published, Draft, Superseded)
- Version numbers

**Rationale**: Australian financial regulation has hierarchical authority (Corporations Act, ASIC Regulatory Guides, ATO Rulings). Temporal logic ensures advice uses correct rules for the relevant time period. Precedence prevents ambiguity in rule application. The system must accurately reflect the legal hierarchy of Australian financial regulation.

### X. Privacy, Tenancy, and Compliance

Per-tenant isolation MUST be enforced at the data layer. PII-minimal logging with field-level redaction. Data retention and erasure policies MUST align with Australian Privacy Act 1988 obligations.

All access MUST use API keys/OAuth with rate limits. Audit logs MUST track:
- All rule changes
- Compute operations
- Data access
- Document generation

The system MUST support compliance with:
- Corporations Act 2001
- Privacy Act 1988
- Anti-Money Laundering and Counter-Terrorism Financing Act 2006
- Code of Ethics for financial advisers

**Rationale**: Financial data is highly sensitive. Australian privacy law requires strict data handling. Multi-tenant architecture requires isolation. Compliance requires comprehensive audit trails. The system must support advisers in meeting their regulatory obligations.

### XI. Data Extraction and Quality Standards

The system transforms unstructured financial documents (regulatory guides, legislation, rulings, case law) into structured data. Extraction MUST maintain:

**Completeness**: Extract all relevant instances of each data type  
**Accuracy**: Preserve exact values, dates, and text from source documents  
**Context**: Include narrative summaries that explain purpose and application  
**Traceability**: Link all extracted items to their source references  
**Consistency**: Use standardized identifiers, formats, and terminology  
**Currency**: Track effective dates and versions to ensure data remains current

The five core data types extracted are:
1. **REFERENCES**: Legal and regulatory sources with pinpoints and versions
2. **RULES**: Calculation and taxation rules
3. **ASSUMPTIONS**: Financial parameters and constants (market-based, economic, actuarial)
4. **ADVICE GUIDANCE**: Mandatory obligations and professional standards
5. **CLIENT OUTCOME STRATEGIES**: Actionable financial planning approaches producing measurable results

**Rationale**: Structured data enables automated compliance checking, rule-based calculations, strategic recommendations, and knowledge management. The Australian financial system's complexity requires systematic data extraction that preserves accuracy while enabling computation. Quality standards ensure extracted data remains authoritative and useful.

### XII. Architectural Component Boundaries (NON-NEGOTIABLE)

The system MUST maintain crisp, non-overlapping boundaries between four core backend components. Each component has a single, well-defined responsibility with explicit forbidden activities.

#### Single Source of Truth for Calculations

**Compute Engine** is the single home for all deterministic financial logic. It MUST own:
- Tax formulas, caps, thresholds, eligibility tests, projections
- All numeric calculations and arithmetic operations
- Rule execution and deterministic computation
- Structured Facts with provenance

**Compute Engine MUST NOT**:
- Perform judgement, advice, or free-text reasoning
- Define its own tax formulas, caps, or thresholds (these come from Rules)
- Override deterministic outputs based on business logic
- Store or serve knowledge objects (References, Rules, Assumptions, Advice Guidance, Strategies)

**Rationale**: Financial calculations require absolute precision and reproducibility. Centralizing all numeric logic in Compute Engine ensures consistency, testability, and auditability. Separating calculation from judgement enables independent verification and compliance.

#### Single Source of Truth for Regulatory Knowledge

**References & Research Engine** is the single home for knowledge storage and retrieval. It MUST own:
- REFERENCES: Legal and regulatory sources with pinpoints and versions
- RULES: Calculation and taxation rule definitions (stored, not executed)
- ASSUMPTIONS: Financial parameters and constants
- ADVICE GUIDANCE: Mandatory obligations and professional standards
- CLIENT OUTCOME STRATEGIES: Actionable financial planning approaches
- FINDINGS: Provisional knowledge discovered during research
- RESEARCH QUESTIONS: Uncertainty and ambiguity records
- VERDICTS: Validation decisions on Findings

**References & Research Engine MUST NOT**:
- Perform numeric calculations or execute rules
- Generate personalised advice or recommendations
- Define tax formulas, caps, or thresholds (it stores them as Rules)
- Scrape raw documents (it stores processed, structured knowledge)

**Rationale**: Knowledge management requires systematic organization, versioning, and traceability. Centralizing all knowledge objects in References & Research Engine ensures consistency, prevents duplication, and enables efficient retrieval. Separating knowledge storage from calculation and advice enables independent evolution and compliance verification.

#### Advice Engine: Judgement and Compliance Brain

**Advice Engine** is the judgement and compliance brain. It MUST:
- Consume Facts from Compute Engine (never calculate them)
- Consume knowledge objects from References & Research Engine (never store them)
- Select and sequence Client Outcome Strategies
- Weigh trade-offs and test suitability
- Evaluate compliance obligations and best-interests duty
- Emit structured advice outputs (recommendations, risks, violations, required artefacts)

**Advice Engine MUST NOT**:
- Define its own tax formulas, caps, or raw system rules
- Perform numeric calculations (it consumes Facts from Compute Engine)
- Scrape raw documents (it consumes knowledge from References & Research Engine)
- Store knowledge objects (it queries References & Research Engine)
- Override deterministic outputs from Compute Engine

**Rationale**: Advice requires judgement, trade-off analysis, and compliance evaluation. Separating advice logic from calculation and knowledge storage enables independent evolution, testing, and compliance verification. Advice Engine focuses on reasoning, suitability, and compliance while delegating calculation and knowledge retrieval to specialized components.

#### Orchestrator is Thin: Natural-Language Router Only

**LLM Orchestrator** is a thin natural-language router and controller. It MUST:
- Interpret user input and detect intent
- Build structured requests for the three engines (Compute, References, Advice)
- Call engines in correct sequence
- Validate and repair schemas
- Turn structured outputs back into user-facing text
- Handle PII filtering and safety checks

**LLM Orchestrator MUST NOT**:
- Invent rules, tax formulas, caps, or thresholds
- Perform calculations or numeric operations
- Override deterministic outputs from Compute Engine or Advice Engine
- Store knowledge objects (it queries References & Research Engine)
- Contain business logic or decision-making rules
- Replace rule logic or calculation logic

**Rationale**: LLM Orchestrator serves as a translation layer between natural language and structured APIs. Keeping it thin ensures that all business logic, calculations, and knowledge remain in their designated components. This separation enables independent testing, evolution, and compliance verification of each component.

**Enforcement**: All specifications and implementation tasks MUST clearly assign responsibilities to the correct component. Tasks that violate these boundaries MUST be flagged during Constitution Check and redirected to the appropriate component.

---

## Architecture Constraints

### Module Boundaries

The system MUST maintain clear module boundaries with API-based interactions:

#### 1. Frankie's Finance (Consumer UX)
- **Purpose**: Mobile-first experience for everyday users
- **Responsibilities**: Collect user goals and scenarios; display outputs, charts, and explainable insights
- **Interfaces**: Calls `/llm/chat` or `/llm/parse` for user intent; calls backend APIs for computations

#### 2. Veris Finance (Adviser UX)
- **Purpose**: Professional console for financial advisers and paraplanners
- **Responsibilities**: Scenario management, client records, compliance documentation; access to audit logs and `/explain` chains
- **Interfaces**: Same APIs as Frankie's Finance; different auth scopes and UI tone

#### 3. LLM Orchestrator
- **Purpose**: Translate human language into structured, auditable requests
- **Nature**: Thin stateless translator and router; never the source of truth
- **Structure**: Orchestrator Layer (intent detection, schema validation, tool routing) + OpenRouter Integration Layer (unified API for all LLM providers via OpenRouter, supporting both OpenRouter credits and BYOK)
- **Responsibilities**:
  - Interpret user input and detect intent
  - Build structured requests for Compute Engine, References & Research Engine, and Advice Engine
  - Call engines in correct sequence
  - Validate and repair schemas
  - Turn structured outputs back into user-facing text
  - Handle PII filtering and safety checks
- **APIs**: `POST /llm/parse`, `POST /llm/chat`
- **FORBIDDEN**: Must not invent rules, perform calculations, override deterministic outputs, store knowledge objects, or contain business logic

#### 4. Compute Engine (Calculation Core)
- **Purpose**: Perform deterministic financial computations and projections
- **Nature**: Calculation engine with relational database data plane
- **Responsibilities**:
  - Execute all tax formulas, caps, thresholds, eligibility tests, and projections
  - Execute rulesets, scenarios, and simulations
  - Maintain provenance and reproducibility
  - Return structured Facts with full provenance
- **Storage**: Relational database (governance, execution, explain paths, time-travel queries)
- **APIs**: `POST /run`, `POST /run-batch`, `GET /facts`, `GET /explain/{fact_id}`
- **Invariants**: Every run pins `ruleset_id`, `as_of`, and `scenario_id`; facts are immutable, versioned, and fully traceable
- **FORBIDDEN**: Must not perform judgement, advice, or free-text reasoning; must not define its own tax formulas or store knowledge objects

#### 5. References & Research Engine
- **Purpose**: Manage authoritative legal and regulatory sources
- **Nature**: Research and ingestion pipeline for legislation, RGs, rulings, and case law
- **Responsibilities**:
  - Store and serve REFERENCES, RULES, ASSUMPTIONS, ADVICE GUIDANCE, CLIENT OUTCOME STRATEGIES, FINDINGS, RESEARCH QUESTIONS, VERDICTS
  - Maintain normalized Reference objects with pinpoints, versions, and metadata
  - Provide RAG-style retrieval for AI models and other consumers
- **APIs**: `GET /references/search`, `GET /references/{id}`, `GET /pinpoints/{reference_id}`
- **FORBIDDEN**: Must not perform numeric calculations, execute rules, generate personalised advice, or scrape raw documents

#### 6. Advice Engine (Compliance & Best-Interest Checks)
- **Purpose**: Enforce professional and regulatory standards
- **Nature**: Deterministic policy engine that evaluates compliance obligations
- **Responsibilities**:
  - Consume Facts from Compute Engine (never calculate them)
  - Consume knowledge objects from References & Research Engine (never store them)
  - Select and sequence Client Outcome Strategies
  - Weigh trade-offs and test suitability
  - Check best-interests duty, conflicts, documentation, and product replacement logic
  - Generate warnings, required actions, and artifact checklists
  - Emit structured advice outputs (recommendations, risks, violations, required artefacts)
- **APIs**: `POST /advice/check`, `GET /advice/requirements`
- **FORBIDDEN**: Must not define tax formulas, perform numeric calculations, scrape raw documents, store knowledge objects, or override deterministic outputs from Compute Engine

### Storage Requirements

- **Relational Database**: MUST support:
  - **Transactions and ACID guarantees**: For rule governance, version tracking, and audit logging
  - **Efficient provenance chain traversal**: For `/explain` queries
  - **Flexible relationship storage and querying**: For provenance links, rule metadata
  - **Time-travel query support**: For built-in or implemented `as_of` queries
  - **Indexes**: Optimized for explain path queries, fact lookups, and scenario queries
  - **Foreign keys and constraints**: For data integrity and referential integrity
- **Cache Layer**: Optional but recommended for hot facts and frequently accessed data
- **Object Storage**: For reference documents (PDFs, HTML), rule artifacts (Markdown/YAML)

### API Requirements

Core compute endpoints MUST include:
- `POST /run` and `POST /run-batch` (idempotent; accepts `ruleset_id`, `as_of`, `scenario_id`)
- `GET /facts?scenario=...&as_of=...`
- `GET /explain/{fact_id}`
- `GET /rulesets`, `GET /rules?active=true&as_of=...`, `GET /references/{id}`, `GET /advice-guidance`, `GET /client-outcome-strategies`

All APIs MUST support API keys/OAuth, tenant isolation, and rate limits.

### Canonical Schemas

All modules MUST use canonical schemas stored in `specs/001-master-spec/schemas/`. This master folder is the single source of truth for:

- **Data Model Schemas**: All fourteen Canonical Concepts (Rule, Reference, Assumptions, Advice Guidance, Client Outcome Strategy, Scenario, Client Event, Input, Fact, Finding, Research Question, Verdict, Provenance Link, Ruleset Snapshot) defined as YAML/JSON Schema
- **API Schemas**: Request/response schemas for all module APIs (OpenAPI/Pydantic)
- **Database Schemas**: Relational database schema definitions (migrations, version control)

**Requirements**:
- All modules MUST import schemas from the master folder (no local copies)
- Schema changes require PR review and coordination across affected modules
- Schema versioning ensures backward compatibility
- Backend modules load schemas into `backend/shared/models/` (Python Pydantic)
- Frontend modules load schemas into `frontend/shared/types/` (TypeScript)

**Rationale**: Canonical schemas ensure consistency across modules, prevent schema drift, enable type safety, and provide a single source of truth for all data structures. This is critical for a multi-module system where modules must interoperate seamlessly.

### Canonical Concepts

These concepts are applicable across all six modules (Frankie's Finance, Veris Finance, LLM Orchestrator, Compute Engine, References & Research Engine, and Advice Engine). Every specification MUST include these concepts to ensure determinism, traceability, and explainability across the system.

#### 1. Rule

A formal, deterministic statement that defines how a calculation, condition, or logical test must operate within the system. Rules encode financial and regulatory principles as executable, auditable logic.

Rules are the backbone of deterministic forecasting. They transform complex legal obligations into reproducible algorithms with version control and temporal logic. Each Rule includes identifiers, effective windows, precedence levels, parameters, tests and edge cases, linked References, status and versioning, and supersedes relationships.

#### 2. Reference

An authoritative legal or regulatory source (Act, Regulation, ASIC Regulatory Guide, ATO Ruling, Case, or Standard) that anchors every Rule, Assumption, or Strategy in verifiable legal evidence.

References ensure all computations and advice can be traced back to an immutable, validated source. They enable long-term citation stability and protection from URL or document drift. Each Reference includes full citation details, reference type and pinpoint classifications, stable pinpoint identifiers, version metadata, and source text checksums.

#### 3. Assumptions

Non-authoritative constants required for modelling (e.g., inflation, CPI, earnings growth, discount rate) that fill legislative gaps with explicit, reviewable parameters.

Assumptions make forecasting possible without hidden defaults. Scoped snapshots ensure reproducibility across tenants and time. Each Assumption includes versioning, effective windows, scope (global, tenant, or scenario), source/rationale tagging, and change logs.

#### 4. Advice Guidance

Codified professional obligations and ethical or procedural standards (ASIC RG 175, RG 244, FASEA Code, licensee policies) that embed compliance and ethical obligations within the Advice Engine.

Advice Guidance ensures every recommendation satisfies the best-interests duty and other statutory obligations. It provides a compliance link between strategy and law, including identifiers, versioning, effective windows, and links to authoritative sources.

#### 5. Client Outcome Strategy

An actionable plan that orchestrates multiple **Rules** under relevant **Advice Guidance** to achieve measurable financial outcomes. Examples: *Salary-sacrifice super contribution*, *Debt-recycling plan*.

Client Outcome Strategies connect calculation logic (Rules) with human-meaningful goals, providing repeatable, outcome-based pathways that remain compliant and deterministic. Strategies must not contain calculation logic; all arithmetic occurs in Rules. Strategies orchestrate Rules, eligibility tests, sequencing, and trade-offs, and reference Advice Guidance by ID. Each Strategy includes identifiers, versioning, effective windows, linked Rules and Advice Guidance, and outcome definitions.

#### 6. Scenario

A tagged, versioned set of Facts, Inputs, and Assumptions representing a possible financial future (baseline, what-if, or historical). Scenarios model alternate futures without overwriting the base state.

Scenarios preserve reproducibility across simulations and allow safe experimentation. They include references to **Client Events** but do not own them. Each Scenario includes identifiers, versioning, tags, linked Facts, Inputs, Assumptions, and Client Event references.

#### 7. Client Event

A discrete financial or life action affecting a client (income change, purchase, policy start, marriage, retirement) that represents real-world triggers updating client circumstances.

Client Events are time-anchored evidence for scenario modelling, improving temporal accuracy. Each Event includes identifiers, timestamps, descriptions, financial impact details, affected entities, and links to Rules, Assumptions, or References.

#### 8. Input

Immutable, versioned client-supplied or imported data (balances, income, holdings, contributions) captured at an `as_of` date that distinguishes raw client data from Assumptions or derived Facts.

Inputs prevent hidden dependencies on mutable or inferred values and enable deterministic re-execution using the exact same inputs. Each Input includes identifiers, versioning, `as_of` dates, data values, units, and source metadata.

#### 9. Fact

An immutable computed result produced by applying Rules and Assumptions to Inputs within a Scenario. Facts record verified outcomes that can be replayed and audited.

Facts make every number explainable and reproducible, forming the foundation of transparency and compliance. Each Fact includes identifiers, units, rounding policies and stages, rounding plan and inputs hashes, linked Rules, References, Assumptions, and Provenance Links, scenario identifiers, `as_of` dates, and tolerance and computation method metadata.

#### 10. Finding

A provisional rule, assumption, or principle extracted automatically from reference material. Findings exist before validation and capture candidate knowledge discovered by automated research pipelines.

Findings separate unverified knowledge from governance-approved logic and prevent unvalidated extractions from influencing advice or calculations. Finding and Verdict form a validation lifecycle for candidate rules, recorded in the data model. Each Finding includes identifiers, extracted content, source references, status, and lifecycle state transitions.

#### 11. Research Question

A structured record of uncertainty, ambiguity, or conflict identified during extraction or validation that logs what the system does not yet know and drives iterative re-reading.

Research Questions transform uncertainty into actionable research tasks and maintain visible traceability of open issues. Each Research Question includes identifiers, topic, source references, priority, reason, and status tracking.

#### 12. Verdict

A formal decision outcome attached to a Finding after validation that creates an immutable audit record for each Finding.

Verdicts show the lineage of every Rule from discovery to publication and support explainable governance. Finding and Verdict form a validation lifecycle for candidate rules, recorded in the data model. Each Verdict includes identifiers, decision outcome (Approved, Rejected, Needs Revision), validator summary, timestamps, reason, and actor metadata.

#### 13. Provenance Link

A first-class relationship object connecting **Facts ↔ Rules/Strategies ↔ References ↔ Assumptions ↔ Inputs** that embeds explainability directly into the data model.

Provenance Links enable deterministic `/explain` queries, cached explain chains, and complete audit reconstruction. Each Provenance Link includes identifiers, role tags, effective windows per link, evidence metadata, and version stamps.

#### 14. Ruleset Snapshot

A frozen, versioned collection of validated Rules, References, and Assumptions identified by a unique `ruleset_id` and `as_of` date that defines the exact knowledge state used by deterministic computations.

Ruleset Snapshots guarantee reproducibility and time-travel, allowing both retrospective and prospective analyses under the correct legal regime. Snapshots may be composed into **domain bundles** (e.g., tax-2025-07-01 + super-2025-10-01) under one published bundle id. Each Ruleset Snapshot includes identifiers, `as_of` dates, bundle composition, linked Rules, References, and Assumptions, and version metadata.

**Note**: Detailed schemas, fields, and lifecycle/state-machine definitions for each canonical concept are documented in `specs/001-master-spec/canonical_data_model.md`.

### Canonical ID Prefix Reference

All canonical entities use **structured IDs** with a short **two-letter prefix** followed by a **ULID or deterministic hash**. This ensures uniqueness, readability, and auditability across modules.

**ID Format**: Example: `RU-01HFSZ2R2Y1G2M5D8C9QWJ7K4T`

| Prefix | Entity Name | Meaning and Purpose |
|--------|-------------|---------------------|
| **RU-** | **Rule** | Deterministic calculation/condition used by the Compute Engine. |
| **RE-** | **Reference** | Authoritative source: legislation, regulations, rulings, guides. |
| **AS-** | **Assumption** | Non-authoritative modelling constants (economic/actuarial). |
| **AG-** | **Advice Guidance** | Professional/regulatory obligations (ASIC/FASEA/licensee). |
| **ST-** | **Client Outcome Strategy** | Goal-oriented plan orchestrating Rules toward outcomes. |
| **SC-** | **Scenario** | Alternate future/modelling context grouping Inputs, Assumptions, Facts. |
| **EV-** | **Client Event** | Discrete life/financial event impacting the client state. |
| **IN-** | **Input** | Immutable client-supplied data captured at an `as_of` date. |
| **FA-** | **Fact** | Immutable computed result with full provenance. |
| **FN-** | **Finding** | Provisional rule or concept discovered during automated research. |
| **RQ-** | **Research Question** | Uncertainty/contradiction requiring clarification. |
| **VD-** | **Verdict** | Decision on a Finding (Approved/Rejected/Needs Revision). |
| **RS-** | **Ruleset Snapshot** | Frozen, versioned bundle used in deterministic computation. |
| **PL-** | **Provenance Link** | Connects Facts ↔ Rules ↔ References ↔ Assumptions ↔ Inputs. |

**ID Requirements**:
- **Global uniqueness**: ULID/hash ensures collision-free IDs across tenants/modules.
- **Immutability**: IDs are never reused or reassigned.
- **Cross-module consistency**: Prefix semantics are identical in every module.
- **Traceability**: IDs appear in logs, audit trails, and provenance chains.
- **Human readability**: Short, stable prefixes aid debugging and compliance reviews.

**Example Provenance Chain with IDs**:
```
FA-01HFSZ2R2Y1... ← produced by
RU-01HFSWXYZ8... ← justified by
RE-01HFSPQRT9... ← interpreted from
AS-01HFSNJKL5... ← under assumptions
IN-01HFSLMNO3... ← using client inputs
PL-01HFSTUVW2... ← recorded as provenance link
RS-01HFSGHIJ7... ← within ruleset snapshot
```

### Governance, Identity, and Security Clarifications

#### Tenant Isolation

Findings, Assumptions, Strategies, Scenarios, Events, and Inputs may include optional `tenant_id`. References and Rules are global. Provenance Links MUST never cross tenants.

#### Publishing Discipline

Four-eyes rule applies to governance artifacts (Rules, References, Assumptions, Guidance, Strategies). Execution artifacts (Facts, Events, Inputs) are write-only via the deterministic engine.

#### Explain-Chain Performance

Explain paths can grow large. The system caches materialized explain chains per `(fact_id, ruleset_id)`; invalidates caches on new Ruleset publication.

#### PII Containment

Provenance Links and References MUST NOT store personally identifiable information. All PII resides in Inputs; downstream logs must mask PII fields.

### Quality and Validation Rules

- Every Finding must pass **pinpoint validation** (anchored offsets or DOM markers).
- Contradiction check required for same-precedence sources.
- All Assumptions resolved deterministically via scope cascade (`scenario` → `tenant` → `global`).
- Equal-precedence conflicts produce `Contested` status; no publication allowed.
- Explain cache, rounding plan, and tolerance metadata required on every Fact.

---

## Specification and Planning Structure

The project uses a hierarchical specification and planning structure optimized for parallel development and multi-agent collaboration:

### Master Specification and Subspecifications

**Master Specification**: `specs/001-master-spec/spec.md`
- Coordinates all six modules
- Defines system-wide requirements and user stories
- Contains clarifications and edge cases applicable across modules

**Subspecifications** (module-specific user requirements):
- `specs/002-compute-engine/spec.md` - Compute Engine module
- `specs/003-references-research-engine/spec.md` - References & Research Engine module
- `specs/004-advice-engine/spec.md` - Advice Engine module
- `specs/005-llm-orchestrator/spec.md` - LLM Orchestrator module
- `specs/006-frankies-finance/spec.md` - Frankie's Finance consumer UX module
- `specs/007-veris-finance/spec.md` - Veris Finance adviser UX module

Each subspecification focuses exclusively on user requirements (user stories, acceptance scenarios, success criteria) and is readable by non-technical stakeholders. Technical implementation details are excluded from specifications.

### Master Plan and Subplans

**Master Plan**: `specs/001-master-spec/plan.md`
- Overall system architecture and cross-module coordination
- Shared infrastructure (databases, auth, observability)
- Technology stack decisions affecting all modules
- Development workflow and governance
- API contracts between modules
- Phase 0 foundational infrastructure
- Module sequencing and dependencies

**Subplans** (module-specific technical implementation):
- `specs/002-compute-engine/plan.md` - Compute Engine implementation
- `specs/003-references-research-engine/plan.md` - References & Research Engine implementation
- `specs/004-advice-engine/plan.md` - Advice Engine implementation
- `specs/005-llm-orchestrator/plan.md` - LLM Orchestrator implementation
- `specs/006-frankies-finance/plan.md` - Frankie's Finance implementation
- `specs/007-veris-finance/plan.md` - Veris Finance implementation

Each subplan contains module-specific technical decisions, internal architecture, dependencies, implementation phases, testing strategies, and performance goals.

### Task List Structure

**Single Task List**: `specs/001-master-spec/tasks.md`
- Contains all development tasks across all modules
- Organized by phases and user stories
- Optimized for execution via three separate agent chats in Cursor:
  1. **Backend Agent Chat**: Tasks for backend modules (Compute Engine, References & Research Engine, Advice Engine, LLM Orchestrator)
  2. **Frontend Agent Chat**: Tasks for UX modules (Frankie's Finance, Veris Finance)
  3. **Infrastructure/DevOps Agent Chat**: Tasks for foundational infrastructure, CI/CD, deployment, and cross-cutting concerns

Tasks are tagged with module identifiers and can be filtered by agent chat focus area. This structure enables parallel development while maintaining a single source of truth for all tasks.

**Rationale**: The hierarchical structure (master + subspecs/plans) enables:
- Clear separation between user requirements (specs) and technical implementation (plans)
- Parallel development across modules with clear boundaries
- Single task list prevents duplication and ensures consistency
- Multi-agent chat optimization enables focused, efficient development workflows

## Development Workflow

### Rule Authoring Process

1. **Author**: Create rule as Markdown/YAML with schema validation
2. **Test**: Include tests, examples, and edge cases
3. **Review**: Two-person review (four-eyes principle)
4. **Publish**: Creates `ruleset-YYYYMMDD` snapshot in relational database
5. **Validate**: Validate rule integrity and consistency
6. **Activate**: Make available in Compute Engine for execution

### Quality Gates

- **Constitution Check**: All PRs/reviews MUST verify compliance with constitution principles
- **Testing**: Deterministic functions with explicit units/rounding; golden datasets (regulator examples); property-based tests for brackets, monotonicity, and boundaries
- **Observability**: Idempotency keys, job tracking, change logs; `/explain` and per-Fact provenance always on
- **Documentation**: All rules, references, and strategies MUST have narrative summaries explaining purpose and application
- **Data Extraction Quality**: Maintain completeness, accuracy, context, traceability, consistency, and currency

### Complexity Justification

Any architecture decision that violates constitution principles (e.g., adding a graph database, bypassing rule engine, direct database edits outside of versioned artifacts) MUST be documented with:

- Why the violation is needed
- Simpler alternative considered and rejected
- Migration plan to return to compliance

---

## Governance

This constitution supersedes all other practices, coding standards, and architectural decisions. Amendments require:

1. **Documentation**: Explicit rationale for change
2. **Approval**: Review and approval process (TBD based on team structure)
3. **Migration Plan**: If amendment affects existing code, a migration plan MUST be provided
4. **Version Bump**: Constitution version MUST increment per semantic versioning:
   - **MAJOR**: Backward incompatible governance/principle removals or redefinitions
   - **MINOR**: New principle/section added or materially expanded guidance
   - **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

All PRs and reviews MUST verify compliance with the constitution. Complexity that violates principles MUST be justified in the Complexity Tracking section of implementation plans.

**Version**: 2.6.1 | **Ratified**: 2025-01-27 | **Last Amended**: 2025-01-27
