# models-overview.md

## 0. Purpose & Scope

This document defines the **interaction models** used across:

- **Frankie’s Finance** (consumer app)  
- **Veris Finance** (adviser tooling)  
- **Internal Dev / Compliance / Licensee** workflows  

It sits alongside the **System Architecture: The Four-Engine Model & Operational Workflows** document, which defines **Modes 1–26** (Fact Check, Crystal Ball, Rule Lab, etc.):'workflows_and_modes.md'

- The **Four-Engine document** is *mode-centric* (what happens in each use case).  
- **This document** is *model-centric* (how engines + artifacts combine into reusable patterns).

Each **Model (`MOD-###`)** describes:

- Which **engines** are involved (LLM, Calc, Strategy, Advice, References/RAG).
- Which **actors** use it (consumer, adviser, dev/compliance, partner).
- What **artifacts** it reads/writes (`CalculationState`, `Scenario`, `ProjectionTimeline`, traces, etc.).
- Which **Modes** it typically hosts (from Modes 1–26).

Each model will later get its own file, e.g. `model-MOD-001-conversational-insight.md`.

---

## 0.1 Shared Concepts

### Engines

- **LLM Orchestrator (Interface / Probabilistic Layer)**  
  - Bridges natural language ↔ structured state.  
  - Tasks:  
    - Intent recognition & classification.  
    - State hydration (populate/patch `CalculationState`).  
    - Strategy domain nomination (“Debt vs Super vs Investing”).  
    - Narrative/explanation generation and educational responses.

- **Calculation Engine (Deterministic / Physics Layer)**  
  - Stateless numeric core (“garbage in, garbage out”).  
  - Tasks:  
    - Atomic CALs (tax, super, debt, property, portfolio).  
    - Multi-year projections → `ProjectionTimeline`.  
    - Emitting `TraceLog` entries (rule applications, assumptions).

- **Strategy Engine (Optimization Layer)**  
  - The “solver” that manipulates state to hit goals.  
  - Tasks:  
    - Validate applicability of strategies.  
    - Generate candidate scenarios (vary levers under constraints).  
    - Run optimisation/search loops around Calc.  
    - Produce ranked Candidate Scenarios.

- **Advice Engine (Governance Layer)**  
  - The “regulator” enforcing BID, safety, and licensee rules.  
  - Tasks:  
    - Scenario vs Baseline comparisons.  
    - Suitability checks, buffer thresholds, caps & policy checks.  
    - Output OK/WARN/BLOCK with reasons & references.

- **References / Research Engine (RAG Layer)**  
  - Legal/technical backing store (Acts, RGs, ATO, product docs).  
  - Tasks:  
    - Ingest/version authoritative sources.  
    - Retrieve chunks for rule extraction & explanations.  
    - Support RAG-based educational answers and “why” explanations.



### Actors

- **Consumer / Client (Frankie)** – retail user; gets education, projections, nudges, sometimes scaled advice.  
- **Adviser / Paraplanner (Veris)** – professional user; uses engine outputs + own judgement for advice.  
- **Dev / Compliance / Licensee** – builds rules, tests engines, audits advice, runs QA modes.  
- **Partner / API Consumer** – external platforms consuming engines via APIs.

---

## 0.2 Model IDs

Models are identified as:

- `MOD-###` – where `###` is a 3-digit sequence.

Current catalogue:

- `MOD-001` … `MOD-012`

Each model can host multiple Modes (1–26).

---

## MOD-001 – Conversational Insight Model

**Name:** Conversational Insight  
**ID:** `MOD-001`  
**Status:** Core  
**Primary Users:** Consumers, Advisers  
**Reg Status:** Typically **Factual Information / General Info**, can escalate to advice context when Strategy/Advice engines are invoked.

### Summary

> “Chat → Structured Intent → Deterministic Numbers → Narrative Back.”

Used whenever someone types/speaks a question and expects an answer grounded in the Calculation Engine (or pure education if no calculation needed).

### Engines Involved

- **LLM Orchestrator** – primary:
  - Intent recognition (“fact check” vs “what-if” vs “education”).  
  - State hydration from chat history and user profile.  
  - Decides whether to call Calc / Strategy / Advice or just answer educationally.
- **Calculation Engine** – when a number is needed.
- **Advice Engine** – light guardrails (“don’t accidentally give personal advice when only facts requested”).
- **References/RAG** – for purely educational explanatory answers.

### Key Artifacts

- Updated `CalculationState` (Year 0).  
- Requested intermediates (e.g., `net_tax_payable`, `buffer_months`, `net_wealth_now`).  
- Narrative response (plain language explanation, optionally with charts).  
- Internal classification of Mode (1, 2, 3, 24, etc.).

### Typical Modes

- **Mode 1 – Fact Check** (current net wealth, tax, super, etc.).  
- **Mode 2 – Crystal Ball** (simple projection when user asks “Am I on track?”).  
- **Mode 24 – Conversational Guide** (general education; no compute required).  
- Entry point / shell for many other modes (3, 8, 10, 13), before transferring into other models.

---

## MOD-002 – Scenario & Alternate-Futures Model

**Name:** Scenario & Alternate-Futures  
**ID:** `MOD-002`  
**Status:** Core  
**Primary Users:** Consumers, Advisers  
**Reg Status:** Ranges from educational projections to personal advice (depending on context & Advice Engine usage).

### Summary

> “Baseline vs What-if vs Strategy A/B/C.”

Manages multiple explicit scenarios (Baseline, A, B, “Broken”) and their timelines, enabling comparison of futures.

### Engines Involved

- **LLM Orchestrator:**  
  - Creates & labels scenarios based on user intent (“Do Nothing”, “Strategy A: extra super”, “Strategy B: pay debt”).  
- **Strategy Engine:**  
  - Optionally generates what-ifs (parameter deltas) from Baseline.  
- **Calculation Engine:**  
  - Computes `ProjectionTimeline` per scenario (wealth, tax, cashflow, buffers).  
- **Advice Engine:**  
  - Optional warnings / gating when scenarios imply advice.

### Key Artifacts

- `BaselineScenario` (Do Nothing).  
- `Scenario` objects A, B, etc. with:  
  - Initial `CalculationState`.  
  - `ProjectionTimeline`.  
  - Scenario metadata (short label, description, assumptions).  
- Scenario comparison metrics at key dates (e.g., retirement age, loan end, 10 years).

### Typical Modes

- **Mode 2 – Crystal Ball** (Baseline-only).  
- **Mode 3 – Strategy Explorer** (multiple strategies as scenarios).  
- **Mode 4 – Adviser Sandbox** (manual scenario A/B).  
- **Mode 8 – Stress Tester** (adverse “broken” scenarios).  
- **Mode 10 – Time Traveler** (Past vs Present vs “Projected Past”).  
- **Mode 16 – Collaborative Session** (live edits across scenarios).

---

## MOD-003 – Strategy Optimisation Model

**Name:** Strategy Optimisation  
**ID:** `MOD-003`  
**Status:** Core  
**Primary Users:** Consumers (Frankie, mostly general advice), Advisers (Veris)  
**Reg Status:** Often general advice in Frankie; personal advice in Veris/Scaled Advice contexts.

### Summary

> “Intent → Strategy Domain → Engine Loop → Best Candidate Scenario.”

Defines levers and constraints, then runs optimisation/search around Calc to find mathematically attractive strategies.

### Engines Involved

- **LLM Orchestrator:**  
  - Maps user intent to strategy domains (“super contributions”, “debt reduction”, “investment mix”).  
  - Helps set constraints (“must keep buffer ≥ 3 months”).
- **Strategy Engine:**  
  - Encodes strategy templates and tunable levers.  
  - Filters for applicability (eg, no super strategy if no cap space).  
  - Generates candidate scenarios; runs loops to search for optima or frontiers.  
- **Calculation Engine:**  
  - Scores each candidate (wealth, tax, risk, buffers).  
- **Advice Engine:**  
  - Rejects candidates that break safety or policy envelopes.

### Key Artifacts

- Strategy Domain metadata.  
- Candidate scenario set with metrics & scores.  
- Selected Candidate Scenario or “frontier set” (top N) with rationale.

### Typical Modes

- **Mode 3 – Strategy Explorer** (“How could I pay less tax?”).  
- **Mode 5 – Scaled Advice Loop** (specific issue, narrow domain, full governance check).  
- **Mode 6 – Holistic Plan** (cascade optimisation across domains: Debt → Super → Investment).  
- **Mode 8 – Stress Tester** (inverted optimisation: configure “bad” scenario, not best).  
- **Mode 9 – Value Scout** (lead qualification via “Do Nothing vs Optimised Everything”).  
- **Mode 13 – Behaviour Coach** (micro-strategy changes over short time horizons).  
- **Mode 14 – Implementation Orchestrator** (sequencing actions post-strategy).  

---

## MOD-004 – Compliance & Governance Model

**Name:** Compliance & Governance  
**ID:** `MOD-004`  
**Status:** Core  
**Primary Users:** Advisers, Compliance, Licensee  
**Reg Status:** Personal advice / licensee oversight.

### Summary

> “Scenario → Advice Checks → Compliance Artefacts.”

Wraps Scenario & Strategy output in BID, safety, and licensee policy checks, and produces SoA/RoA-ready compliance content.

### Engines Involved

- **Advice Engine:**  
  - BID checks (s961B equivalence).  
  - Caps, product rules, constraints (e.g., buffer months, max gearing).  
  - Conflict management & vulnerability rules.  
- **Calculation Engine:**  
  - Supplies required metrics (tax, buffers, LVR, exposure, etc.).  
- **References/RAG:**  
  - Links advice rules to official sources.  
- **LLM Orchestrator:**  
  - Converts rule outcomes into humanised rationales, warnings, and compliance wording.

### Key Artifacts

- Advice Outcome per scenario: `OK`, `WARN`, `BLOCK` (+ reasons).  
- Rule hit list (which rules fired, with references).  
- Compliance artefacts: SoA/RoA sections, audit logs.

### Typical Modes

- **Mode 5 – Scaled Advice Loop.**  
- **Mode 6 – Holistic Plan.**  
- **Mode 7 – Proactive Monitor** (when new rules hit existing strategies).  
- **Mode 11 – Bulk Auditor** (portfolio-wide re-checks).  
- **Mode 19 – Advice Harness** (advice behaviour regression).  
- **Mode 25 – Practice Assistant** (email/content audit for compliance tone).

---

## MOD-005 – Onboarding & Data-Quality Model

**Name:** Onboarding & Data Quality  
**ID:** `MOD-005`  
**Status:** Core  
**Primary Users:** Consumers, Advisers, Dev/Compliance  
**Reg Status:** Generally **non-advice**, focused on data integrity and completeness.

### Summary

> “Messy answers → Hardened CalculationState.”

Used before heavy modelling or advice: build a consistent, minimally complete state; detect nonsense; ask for missing info.

### Engines Involved

- **LLM Orchestrator:**  
  - Interviews the user (chat or forms).  
  - Maps responses to structured fields, flags ambiguity.  
- **Calculation Engine:**  
  - Runs **sanity-only** CAL bundles (LVR checks, wealth conservation, cap overflows).  
- **Advice Engine (Data QA mode):**  
  - Flags missing mandatory fields and logically inconsistent combos.  
  - *Does not* make suitability judgements.

### Key Artifacts

- Draft → hardened `CalculationState` (Year 0).  
- Data Quality report (missing, inconsistent, impossible).  
- Follow-up questions or tasks.

### Typical Modes

- **Mode 12 – Progressive Mapper** (onboarding & periodic data clean-up).  
- Pre-step for any Holistic Plan or Scaled Advice run.  

---

## MOD-006 – Privacy, Safety & PII Filtering Model

**Name:** Privacy & Safety Filter  
**ID:** `MOD-006`  
**Status:** Cross-cutting (wraps all LLM access)  
**Primary Users:** All (indirectly)  
**Reg Status:** Privacy, cyber & content safety.

### Summary

> “PII-full World → PII-light LLM Prompts → Safe Outputs.”

Enforces privacy and content-safety constraints around all LLM usage.

### Engines Involved

- **LLM Orchestrator + PII Filter:**  
  - Redacts/masks PII before calls to external LLM endpoints.  
  - Enforces “no raw client identifiers” rules.  
- **Advice Engine (meta-safety rules):**  
  - Blocks clearly harmful or non-compliant prompts.  
- **References/RAG:**  
  - Ensures only allowed content is retrieved for given context.

### Key Artifacts

- Pseudonymised prompts & responses.  
- Safety rejection messages.  
- Internal maps from pseudo IDs to real IDs (never exposed externally).

### Typical Modes

- Wraps all modes that involve external LLM calls (1–6, 8, 10, 13, 16, 24–26).  
- Particularly important in **Mode 24 – Conversational Guide** and **Mode 25 – Practice Assistant** when users free-type content that might include PII.

---

## MOD-007 – Reference & Research Model

**Name:** Reference & Research  
**ID:** `MOD-007`  
**Status:** Core for rule-building & explanations  
**Primary Users:** Dev/Compliance, Advisers, LLMs

### Summary

> “Docs → References → Rules → Explainability.”

Maintains authoritative sources and powers both rule extraction and educational/explanatory responses.

### Engines Involved

- **References/Research Engine:**  
  - Ingests legislation, RGs, rulings, product docs.  
  - Maintains versions & metadata.  
- **LLM Orchestrator (RAG):**  
  - Uses retrieved chunks for:  
    - Rule extraction workflows.  
    - Cited explanations for clients & advisers.  
- **Advice Engine:**  
  - Binds rules to references with IDs & versioning.

### Key Artifacts

- Reference index (sources, sections, versions).  
- Derived rules & strategies with citations.  
- Cited explanations and educational content.

### Typical Modes

- Rule authoring & updates (internal Dev/Compliance processes).  
- **Mode 21 – RAG Auditor** (checking the model uses correct sources).  
- **Mode 24 – Conversational Guide** (general educational queries).  
- **Mode 25 – Practice Assistant** (system help & documentation retrieval).

---

## MOD-008 – Partner & API Integration Model

**Name:** Partner & API Integration  
**ID:** `MOD-008`  
**Status:** Core for externalisation  
**Primary Users:** Partners, Internal Services  
**Reg Status:** Varies by partner; engines remain deterministic & auditable.

### Summary

> “External Platform → Stable Contracts → Embedded Compute & Explainability.”

Exposes engine capabilities via stable APIs for partners and internal services.

### Engines Involved

- **Calculation Engine:** main external compute service.  
- **Advice Engine (optional):** can be enabled/disabled per partner.  
- **LLM Orchestrator (optional):** explanation & narrative endpoints.

### Key Artifacts

- API contracts (OpenAPI + schemas) for:  
  - Scenario submission and result retrieval.  
  - Ruleset selection (`ruleset_id`, `as_of`).  
- Partner configuration (quotas, access level, advice vs facts-only).

### Typical Modes

- Partner-hosted **Mode 1 / Mode 2 / Mode 3** variants via API.  
- Bulk compute services tied to **Mode 11 – Bulk Auditor** for external licensees.

---

## MOD-009 – Monitoring, Health & Review Model

**Name:** Monitoring & Health Check  
**ID:** `MOD-009`  
**Status:** Core for ongoing service  
**Primary Users:** Advisers, Consumers, Licensee  
**Reg Status:** Ongoing advice / review services.

### Summary

> “Background Triggers → Re-run → Alert / Check-in.”

Runs in the background when something changes (time, rules, markets, events).

### Engines Involved

- **Strategy Engine:**  
  - Identifies impacted clients/scenarios when context changes.  
- **Calculation Engine:**  
  - Re-runs relevant scenarios with updated `GlobalContext`.  
- **Advice Engine:**  
  - Re-assesses suitability / compliance.  
- **LLM Orchestrator:**  
  - Generates alerts & health summaries for humans.

### Key Artifacts

- Alerts (client-level, portfolio-level, or system-level).  
- Updated timelines & metrics.  
- Review packs (for advisers) or simple “check-ins” (for consumers).

### Typical Modes

- **Mode 7 – Proactive Monitor** (e.g., new tax rates).  
- **Mode 9 – Value Scout** (used in marketing funnels, triggered periodically).  
- Periodic “portfolio health” passes feeding Frankie & Veris dashboards.

---

## MOD-010 – Dev & Engine QA Model

**Name:** Dev & Engine QA  
**ID:** `MOD-010`  
**Status:** Core for development lifecycle  
**Primary Users:** Dev, Compliance, Licensee Tech Governance  
**Reg Status:** Internal QA / non-advice.

### Summary

> “Rules & CALs & Prompts Under Test.”

Aggregates all QA/testing patterns for rules, calculations, prompts, and RAG behaviour.

### Engines Involved

- **Strategy Engine:** generates synthetic/fuzz test cases and golden grids.  
- **Calculation Engine:** under test (atomic CALs, bundles, projections).  
- **Advice Engine:** under test (policy behaviour, BID logic).  
- **LLM Orchestrator:**  
  - Tested for schema adherence & stability.  
  - Generates QA summaries and diagnostic narratives.  
- **References/RAG:** validated for correct source usage.

### Key Artifacts

- Golden test suites (per CAL, per rule).  
- Regression reports (before/after rule or code changes).  
- Fuzz failure clusters.  
- Prompt contract test logs.  
- RAG source-usage audit logs.

### Typical Modes

- **Mode 11 – Bulk Auditor** (replaying rules against stored scenarios).  
- **Mode 15 – Rule Lab** (regression & golden cases).  
- **Mode 17 – Calculation Harness** (atomic CAL tests).  
- **Mode 18 – Scenario Fuzzer** (robustness & edge case hunting).  
- **Mode 19 – Advice Harness** (advice behaviour audit).  
- **Mode 20 – Prompt Contract Tester** (LLM I/O and schema QA).  
- **Mode 21 – RAG Auditor** (source integrity).  
- **Mode 22 – Load & Latency Bench** (performance & scalability).  
- **Mode 23 – Cross-Engine Consistency Checker** (semantic integrity).  
- **Mode 26 – System Oracle** (LLM + traces answering “why did X happen?” for dev/ops).

---

## MOD-011 – Collaborative Session Model

**Name:** Collaborative Session (Client–Adviser–AI)  
**ID:** `MOD-011`  
**Status:** Core for Veris live UX  
**Primary Users:** Advisers, Clients  
**Reg Status:** Personal advice; high compliance scrutiny.

### Summary

> “Client + Adviser + AI + Engines in the Room.”

Interactive mode for live meetings, letting adviser and client co-explore scenarios with engines running in the background.

### Engines Involved

- **LLM Orchestrator:**  
  - Facilitates dialogue and translates questions into scenario edits.  
  - Drafts meeting notes in real time.  
- **Strategy Engine:**  
  - Applies requested deltas (e.g., more super, less debt, new goal).  
- **Calculation Engine:**  
  - Runs low-latency recalculations for updated scenarios.  
- **Advice Engine:**  
  - Runs in **Warning Mode**; logs all warnings & overrides.

### Key Artifacts

- Revised scenarios generated during the meeting.  
- Live warnings and prompts for adviser.  
- Meeting transcript & structured notes.  
- SoA/RoA skeleton anchored to the actual session.

### Typical Modes

- **Mode 16 – Collaborative Session.**  
- Under the hood uses patterns from MOD-001, MOD-002, MOD-003, MOD-004.

---

## MOD-012 – Implementation & Habit Model

**Name:** Implementation & Habit  
**ID:** `MOD-012`  
**Status:** Core for continuity between reviews  
**Primary Users:** Consumers, Advisers  
**Reg Status:** Implementation support + ongoing general advice/nudges.

### Summary

> “From Strategy → Actions → Behaviour Over Time.”

Turns chosen strategies into concrete actions, monitors adherence, and supports micro-changes.

### Engines Involved

- **Advice Engine:**  
  - Outputs implementation requirements from approved scenarios.  
  - Ensures new actions do not break constraints.  
- **Strategy Engine:**  
  - Sequences tasks and milestones.  
  - Configures small behaviour changes and review checkpoints.  
- **Calculation Engine:**  
  - Runs lightweight checks when user deviates or adds micro-changes.  
- **LLM Orchestrator:**  
  - Converts requirements into to-do lists, nudges, and progress feedback.

### Key Artifacts

- Implementation plans (task lists & timelines).  
- Behavioural nudge definitions and logs.  
- Updated `CalculationState` snapshots at key events.

### Typical Modes

- **Mode 13 – Behaviour Coach** (short-cycle habit changes).  
- **Mode 14 – Implementation Orchestrator** (post-SoA implementation plans).

---

## 1. Mode → Model Mapping (Summary)

High-level mapping of Modes 1–26 to primary Models:

- **MOD-001** – Modes 1, 2, 24 (plus entry shell for others).  
- **MOD-002** – Modes 2, 3, 4, 8, 10, 16.  
- **MOD-003** – Modes 3, 5, 6, 8, 9, 13, 14.  
- **MOD-004** – Modes 5, 6, 7, 11, 19, 25.  
- **MOD-005** – Mode 12.  
- **MOD-006** – Cross-cutting; wraps all LLM-based modes (esp. 1–6, 8, 10, 13, 16, 24–26).  
- **MOD-007** – Modes 21, 24, 25; rule ingestion.  
- **MOD-008** – Partner-facing variants of Modes 1–3, 11.  
- **MOD-009** – Modes 7, 9 + periodic reviews.  
- **MOD-010** – Modes 11, 15, 17, 18, 19, 20, 21, 22, 23, 26.  
- **MOD-011** – Mode 16.  
- **MOD-012** – Modes 13, 14.

This mapping is a **design tool**, not a hard constraint. New features should either:

- Reuse an existing **Model**, or  
- Justify the creation of a new `MOD-###` entry.

