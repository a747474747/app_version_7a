# Interaction Architecture: Engines, Models, and Modes

**Version:** 1.0
**Context:** Frankie’s Finance (Consumer) / Veris Finance (Adviser)
**Purpose:** Single reference for understanding how engines, models, and modes work together

---

## 1. The Four Engines

The platform utilizes a **Four-Engine Architecture** to solve the core challenge of automated financial advice: the separation of **Probabilistic Intent** (AI) from **Deterministic Rigor** (Math) and **Regulatory Governance** (Compliance).

### 1.1 The LLM Orchestrator (The Interface Layer)
* **Role:** The Translator & Architect.
* **Responsibility:** Bridges the gap between natural language and structured backend requirements.
* **Key Tasks:** Intent recognition, state hydration, strategy nomination, and narrative generation.
* May call the **Reference & Research (RAG) layer** to retrieve authoritative context and citations for explanations, educational answers, and rule/strategy authoring workflows.

### 1.2 The Calculation Engine (The Physics Layer)
* **Role:** The Source of Truth.
* **Responsibility:** Pure, stateless, deterministic calculation. Operates on "Garbage In, Garbage Out."
* **Key Tasks:** Tax/Cashflow math, multi-year projections, and rule traceability (`TraceLog`).

### 1.3 The Strategy Engine (The Optimization Layer)
* **Role:** The Solver.
* **Responsibility:** Finds the *mathematical optimum* for a specific goal (e.g., Max Wealth).
* **Key Tasks:** Applicability filtering, iterative looping (optimization), and candidate scenario selection.

### 1.4 The Advice Engine (The Governance Layer)
* **Role:** The Regulator.
* **Responsibility:** Ensures advice satisfies the **Best Interest Duty (BID)** and suitability constraints.
* **Key Tasks:** Suitability checks, vulnerability logic (buffers/safety), and final gatekeeping (Reject vs. Certify).

### 1.5 Reference & Research Layer (RAG)
**Role:** The system librarian.
**Responsibility:** Provide authoritative, versioned reference material to support rule construction, explanations, and advice governance. Assist in State Hydration by retrieving field definitions and validation rules to guide the LLM in asking precise clarifying questions during onboarding.
**Key tasks:**
- Ingest and version legislation, ASIC Regulatory Guides, ATO rulings, product disclosure statements, and other technical documents.
- Expose a retrieval interface (RAG) so the LLM Orchestrator and Advice Engine can fetch relevant passages for: educational / explanatory answers, rule and strategy authoring, cited justifications for advice and constraint checks.
- Track source, section, and version metadata so every rule and explanation can be traced back to the underlying document.
- Enforce that all RAG results are read-only and never override the deterministic Calculation Engine outputs; they are context, not calculators.

---

## 2. Interaction Models & Modes

### 2.1 Conversational Insight (MOD-001)

* **Architecture:** Used whenever someone types/speaks a question and expects an answer grounded in the Calculation Engine (or pure education if no calculation needed). The LLM Orchestrator handles intent recognition ("fact check" vs "what-if" vs "education"), state hydration from chat history and user profile, and decides whether to call Calc/Strategy/Advice or just answer educationally.

* **Supported Modes:**
    * **Mode 1: Fact Check** (Factual query, e.g., "What is my current net wealth?"). Context: Frankie (App) & Veris (Adviser). Regulatory Status: Factual Information (No Advice). Flow: LLM hydrates CalculationState → requests specific intermediate value → Calc Engine executes relevant CAL → LLM explains naturally.
    * **Mode 2: Crystal Ball** (Linear projection, e.g., "Am I on track for retirement?"). Context: Frankie (App). Regulatory Status: General Advice / Educational Projection. Flow: LLM constructs BaselineScenario → Calc Engine runs 20-year projection → Advice Engine performs Sanity Check → LLM presents trajectory.
    * **Mode 24: Conversational Guide** (General inquiry, vague concepts, or off-topic interaction, e.g., "What is a franking credit?"). Context: Frankie (App - Chat Interface). Regulatory Status: General Information / Non-Financial. Flow: LLM determines input does not require calculation → Advice Engine checks for "Advice Traps" → RAG retrieves general educational content → LLM responds with persona-driven answer.

### 2.2 Strategy & Optimization (MOD-003)

* **Architecture:** Defines levers and constraints, then runs optimisation/search around Calc to find mathematically attractive strategies. The LLM Orchestrator maps user intent to strategy domains, while the Strategy Engine encodes strategy templates, filters for applicability, and generates candidate scenarios through optimization loops.

* **Supported Modes:**
    * **Mode 3: Strategy Explorer** (Exploration of concepts, e.g., "How could I pay less tax?"). Context: Frankie (App). Regulatory Status: General Advice. Flow: LLM suggests Strategy Domain → Strategy Engine finds mathematical winner → Advice Engine checks Generic Safety → LLM presents concept with disclaimers.
    * **Mode 9: Value Scout** (Lead qualification, e.g., "Is it worth paying for an adviser?"). Context: Veris (Funnel). Regulatory Status: Lead Qualification. Flow: Strategy Engine runs "Value Scan" → Calc Engine quantifies financial delta → LLM evaluates delta vs advice cost to score the lead.
    * **Mode 13: Behaviour Coach** (Habits, e.g., "Micro-actions for this week"). Context: Frankie (Momentum). Regulatory Status: General Advice / Nudges. Flow: Strategy Engine proposes micro-moves → Calc Engine quantifies delta → Advice Engine checks Safety Rules → LLM frames as experiment.

### 2.3 Scenarios & Comparison (MOD-002)

* **Architecture:** Manages multiple explicit scenarios (Baseline, A, B, "Broken") and their timelines, enabling comparison of futures. The LLM Orchestrator creates and labels scenarios based on user intent, while the Strategy Engine optionally generates what-ifs and the Calculation Engine computes ProjectionTimelines per scenario.

* **Supported Modes:**
    * **Mode 4: Adviser Sandbox** (Manual modeling, e.g., "Compare Strategy A vs B"). Context: Veris (Adviser). Regulatory Status: Adviser Tooling (Pre-compliance). Flow: Adviser defines scenarios via UI → Calc Engine runs projections instantly → Advice Engine runs in Warning Mode → UI displays side-by-side metrics.
    * **Mode 8: Stress Tester** (Resilience, e.g., "What if I lose my job?"). Context: Frankie (Peace of Mind). Regulatory Status: Risk Analysis. Flow: Strategy Engine configures Adverse Scenario → Calc Engine runs "Broken" projection → Advice Engine checks Survival Policy → LLM reports resilience outcome.
    * **Mode 10: Time Traveler** (Retrospective, e.g., "Why did my balance change?"). Context: Veris (Review). Regulatory Status: Reporting. Flow: Load Snapshot A (Past) and B (Present) → Calc Engine projects A using actual market rates → LLM compares Projected A vs Actual B to explain variance.
    * **Mode 16: Collaborative Session** (Live modeling, e.g., "Client meeting co-pilot"). Context: Veris (Meeting). Regulatory Status: Personal Advice (Human-in-the-loop). Flow: LLM facilitates live questions → Calc updates in near-real-time → Advice Engine runs in Warning Mode → LLM drafts meeting notes/SoA skeleton. (Cross-ref MOD-011)

### 2.4 Comprehensive Advice & Governance (MOD-004)

* **Architecture:** Wraps Scenario & Strategy output in BID, safety, and licensee policy checks, and produces SoA/RoA-ready compliance content. The Advice Engine handles BID checks, caps, and product rules, while the LLM Orchestrator converts rule outcomes into humanised rationales and compliance wording.

* **Supported Modes:**
    * **Mode 5: Scaled Advice Loop** (Single-issue advice, e.g., "Top up super by $20k"). Context: Frankie (Transaction) or Veris (SoA). Regulatory Status: Personal Advice (Limited Scope). Flow: LLM scopes request to domain → Strategy Engine models the specific request → Advice Engine performs Suitability Audit → LLM generates Advice text or Rejection.
    * **Mode 6: Holistic Plan** (Comprehensive plan, e.g., "Fix my finances"). Context: Veris (Adviser). Regulatory Status: Comprehensive Personal Advice (s961B). Flow: LLM aggregates all client data → Strategy Engine runs Cascade Optimization → Calc Engine runs multi-entity projections → Advice Engine runs full Best Interest Duty → LLM drafts Statement of Advice.
    * **Mode 14: Implementation Orchestrator** (Execution, e.g., "Turn strategy into steps"). Context: Veris (Post-SoA). Regulatory Status: Implementation Support. Flow: Advice Engine outputs Implementation Requirements → Strategy Engine sequences dependencies → LLM converts to task lists. (Cross-ref MOD-012)

### 2.5 Data Quality & Onboarding (MOD-005)

* **Architecture:** Used before heavy modelling or advice: build a consistent, minimally complete state; detect nonsense; ask for missing info. The LLM Orchestrator interviews the user and maps responses to structured fields, while the Calculation Engine runs sanity-only CAL bundles and the Advice Engine flags missing or inconsistent data.

* **Supported Modes:**
    * **Mode 12: Progressive Mapper** (Data intake/Quality, e.g., "Does my data look right?"). Context: Frankie (Onboarding). Regulatory Status: Data Quality. Flow: LLM interviews user → Calc Engine runs Data Sanity CALs → Advice Engine flags missing fields or inconsistencies → LLM requests corrections.

### 2.6 Operational Monitoring (MOD-009)

* **Architecture:** Runs in the background when something changes (time, rules, markets, events). The Strategy Engine identifies impacted clients/scenarios when context changes, the Calculation Engine re-runs relevant scenarios with updated GlobalContext, and the LLM Orchestrator generates alerts and health summaries.

* **Supported Modes:**
    * **Mode 7: Proactive Monitor** (System Trigger, e.g., "New Tax Rates Passed"). Context: Veris (Alerts). Regulatory Status: Review Service. Flow: Global Context updated with new rules → Strategy Engine scans client database for impact → Advice Engine checks if current strategies are now non-compliant → LLM generates Adviser Alerts.

### 2.7 QA & Technical Assurance (MOD-010)

* **Architecture:** Aggregates all QA/testing patterns for rules, calculations, prompts, and RAG behaviour. The Strategy Engine generates synthetic test cases, the Calculation Engine is tested for atomic CALs and projections, and the LLM Orchestrator generates QA summaries and diagnostic narratives.

* **Supported Modes:**
    * **Mode 11, 15, 17-23, 26** (Group these succinctly): Bulk Auditor (systemic risk check), Rule Lab (logic regression testing), Calculation Harness (atomic CAL unit testing), Scenario Fuzzer (robustness/edge case testing), Advice Harness (advice policy regression), Prompt Contract Tester (LLM Schema QA), RAG Auditor (reference/source verification), Load & Latency Bench (scalability testing), Cross-Engine Consistency Checker (semantic integrity check), System Oracle (debugging and introspection).

---

## 3. Cross-Cutting Capabilities

* **Privacy (MOD-006)**: Enforces privacy and content-safety constraints around all LLM usage. Redacts/masks PII before external LLM calls and blocks harmful prompts. Wraps all modes involving external LLM calls.

* **Reference/RAG (MOD-007)**: Maintains authoritative sources and powers both rule extraction and educational/explanatory responses. Ingests legislation, RGs, rulings, product docs and enables retrieval for rule construction, explanations, and cited justifications.

* **API Integration (MOD-008)**: Exposes engine capabilities via stable APIs for partners and internal services. Supports partner-hosted variants of core modes with configurable advice levels and quotas.
