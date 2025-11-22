# System Architecture: The Four-Engine Model & Operational Workflows

**Version:** 2.0
**Context:** Frankie’s Finance (Consumer) / Veris Finance (Adviser)

---

## 1. Executive Summary

The platform utilizes a **Four-Engine Architecture** to solve the core challenge of automated financial advice: the separation of **Probabilistic Intent** (AI) from **Deterministic Rigor** (Math) and **Regulatory Governance** (Compliance).

This architecture ensures that while the user interface is conversational and adaptive (LLM), the underlying advice is mathematically reproducible, technically optimized, and legally compliant.

In addition to these four decision engines, the system also relies on a
**Reference & Research layer (RAG)** that stores and retrieves authoritative
sources (legislation, ASIC regulatory guides, ATO rulings, product documents).
The RAG layer does not perform calculations or make advice decisions; instead
it supplies context and citations to the LLM Orchestrator and Advice Engine.

---

## 2. The Four Engines

### 2.1 The LLM Orchestrator (The Interface Layer)
* **Role:** The Translator & Architect.
* **Responsibility:** Bridges the gap between natural language and structured backend requirements.
* **Key Tasks:** Intent recognition, state hydration, strategy nomination, and narrative generation.
- May call the **Reference & Research (RAG) layer** (see 2.5) to retrieve
  authoritative context and citations for explanations, educational answers,
  and rule/strategy authoring workflows.


### 2.2 The Calculation Engine (The Physics Layer)
* **Role:** The Source of Truth.
* **Responsibility:** Pure, stateless, deterministic calculation. Operates on "Garbage In, Garbage Out."
* **Key Tasks:** Tax/Cashflow math, multi-year projections, and rule traceability (`TraceLog`).

### 2.3 The Strategy Engine (The Optimization Layer)
* **Role:** The Solver.
* **Responsibility:** Finds the *mathematical optimum* for a specific goal (e.g., Max Wealth).
* **Key Tasks:** Applicability filtering, iterative looping (optimization), and candidate scenario selection.

### 2.4 The Advice Engine (The Governance Layer)
* **Role:** The Regulator.
* **Responsibility:** Ensures advice satisfies the **Best Interest Duty (BID)** and suitability constraints.
* **Key Tasks:** Suitability checks, vulnerability logic (buffers/safety), and final gatekeeping (Reject vs. Certify).

### 2.5 Reference & Research Layer (RAG)

**Role:** The system librarian.

**Responsibility:** Provide authoritative, versioned reference material to
support rule construction, explanations, and advice governance.

**Key tasks:**

- Ingest and version legislation, ASIC Regulatory Guides, ATO rulings,
  product disclosure statements, and other technical documents.
- Expose a retrieval interface (RAG) so the LLM Orchestrator and Advice Engine
  can fetch relevant passages for:
  - educational / explanatory answers,
  - rule and strategy authoring,
  - cited justifications for advice and constraint checks.
- Track source, section, and version metadata so every rule and explanation can
  be traced back to the underlying document.
- Enforce that all RAG results are read-only and never override the
  deterministic Calculation Engine outputs; they are context, not calculators.


---

## 3. Core Advice Workflows (Standard User Journeys)

These modes represent the most common interactions for both consumers and advisers.

### Mode 1: The "Fact Check"
* **Intent:** Factual query (e.g., "What is my current net wealth?").
* **Context:** Frankie (App) & Veris (Adviser).
* **Regulatory Status:** Factual Information (No Advice).
* **Engines:** `LLM` → `Calc`.
* **Flow:**
    1.  **LLM** hydrates `CalculationState` (Year 0).
    2.  **LLM** requests a specific intermediate value.
    3.  **Calc Engine** executes the relevant CAL.
    4.  **LLM** retrieves the number and explains it naturally.

### Mode 2: The "Crystal Ball"
* **Intent:** Linear projection (e.g., "Am I on track for retirement?").
* **Context:** Frankie (App).
* **Regulatory Status:** General Advice / Educational Projection.
* **Engines:** `LLM` → `Calc` → `Advice (Observer)`.
* **Flow:**
    1.  **LLM** constructs `BaselineScenario` (Status Quo).
    2.  **Calc Engine** runs 20-year projection.
    3.  **Advice Engine** performs Sanity Check (Data integrity only).
    4.  **LLM** presents the trajectory.

### Mode 3: The "Strategy Explorer"
* **Intent:** Exploration of concepts (e.g., "How could I pay less tax?").
* **Context:** Frankie (App).
* **Regulatory Status:** General Advice (Strategy suggestions without product recommendation).
* **Engines:** `LLM` → `Strategy` → `Calc` → `Advice (Safety)`.
* **Flow:**
    1.  **LLM** suggests Strategy Domain.
    2.  **Strategy Engine** finds mathematical winner (Optimization Loop).
    3.  **Advice Engine** checks Generic Safety (Risk warnings).
    4.  **LLM** presents the concept with disclaimers.

### Mode 4: The "Adviser Sandbox"
* **Intent:** Manual modeling (e.g., "Compare Strategy A vs B").
* **Context:** Veris (Adviser).
* **Regulatory Status:** Adviser Tooling (Pre-compliance).
* **Engines:** `LLM` → `Calc` → `Advice (Warning)`.
* **Flow:**
    1.  **Adviser** defines scenarios via UI.
    2.  **Calc Engine** runs projections instantly.
    3.  **Advice Engine** runs in **Warning Mode** (Flags breaches but does not block).
    4.  **UI** displays side-by-side metrics for Adviser judgment.

### Mode 5: The "Scaled Advice" Loop
* **Intent:** Single-issue advice (e.g., "Top up super by $20k").
* **Context:** Frankie (Transaction) or Veris (SoA).
* **Regulatory Status:** Personal Advice (Limited Scope).
* **Engines:** `Full Four-Engine Stack` (Narrow Scope).
* **Flow:**
    1.  **LLM** scopes request to domain.
    2.  **Strategy Engine** models the specific request.
    3.  **Advice Engine** performs Suitability Audit on that specific action.
    4.  **LLM** generates Advice text or Rejection.

### Mode 6: The "Holistic Plan"
* **Intent:** Comprehensive plan (e.g., "Fix my finances").
* **Context:** Veris (Adviser).
* **Regulatory Status:** Comprehensive Personal Advice (s961B).
* **Engines:** `Full Four-Engine Stack` (Iterative/Multi-Goal).
* **Flow:**
    1.  **LLM** aggregates all client data.
    2.  **Strategy Engine** runs Cascade Optimization (Debt -> Super -> Investment).
    3.  **Calc Engine** runs multi-entity projections.
    4.  **Advice Engine** runs full Best Interest Duty (BID) comparisons.
    5.  **LLM** drafts Statement of Advice (SoA).

---

## 4. Operational & Business Workflows

Modes supporting business logic, lead generation, and ongoing monitoring.

### Mode 7: The "Proactive Monitor"
* **Intent:** System Trigger (e.g., "New Tax Rates Passed").
* **Context:** Veris (Alerts).
* **Regulatory Status:** Review Service.
* **Engines:** `Strategy` → `Calc` → `Advice`.
* **Flow:**
    1.  Global Context updated with new rules.
    2.  **Strategy Engine** scans client database for impact.
    3.  **Advice Engine** checks if current strategies are now non-compliant.
    4.  **LLM** generates Adviser Alerts.

### Mode 9: The "Value Scout"
* **Intent:** Lead qualification (e.g., "Is it worth paying for an adviser?").
* **Context:** Veris (Funnel).
* **Regulatory Status:** Lead Qualification.
* **Engines:** `LLM` → `Strategy` → `Calc`.
* **Flow:**
    1.  **Strategy Engine** runs "Value Scan" (Optimizes everything vs Do Nothing).
    2.  **Calc Engine** quantifies financial delta (e.g., +$200k).
    3.  **LLM** evaluates delta vs advice cost to score the lead.

### Mode 12: The "Progressive Mapper"
* **Intent:** Data intake/Quality (e.g., "Does my data look right?").
* **Context:** Frankie (Onboarding).
* **Regulatory Status:** Data Quality.
* **Engines:** `LLM` ⇄ `Calc` → `Advice (Data QA)`.
* **Flow:**
    1.  **LLM** interviews user.
    2.  **Calc Engine** runs Data Sanity CALs (LVR checks, Wealth balancing).
    3.  **Advice Engine** flags missing fields or inconsistencies.
    4.  **LLM** requests corrections.

### Mode 14: The "Implementation Orchestrator"
* **Intent:** Execution (e.g., "Turn strategy into steps").
* **Context:** Veris (Post-SoA).
* **Regulatory Status:** Implementation Support.
* **Engines:** `Advice` → `Strategy` → `LLM`.
* **Flow:**
    1.  **Advice Engine** outputs Implementation Requirements.
    2.  **Strategy Engine** sequences dependencies (Forms -> Budget -> Transfer).
    3.  **LLM** converts to task lists.
    4.  **Calc/Advice** re-run if user deviates during execution.

---

## 5. Specialized & Advanced Advice Modes

Modes dealing with risk, behavior, and retrospective analysis.

### Mode 8: The "Stress Tester"
* **Intent:** Resilience (e.g., "What if I lose my job?").
* **Context:** Frankie (Peace of Mind).
* **Regulatory Status:** Risk Analysis.
* **Engines:** `LLM` → `Strategy (Chaos)` → `Calc` → `Advice (Survival)`.
* **Flow:**
    1.  **Strategy Engine** configures Adverse Scenario (Income=0, Market -20%).
    2.  **Calc Engine** runs "Broken" projection.
    3.  **Advice Engine** checks Survival Policy (Cash Buffer > 0).
    4.  **LLM** reports resilience outcome.

### Mode 10: The "Time Traveler"
* **Intent:** Retrospective (e.g., "Why did my balance change?").
* **Context:** Veris (Review).
* **Regulatory Status:** Reporting.
* **Engines:** `Calc` → `LLM`.
* **Flow:**
    1.  Load Snapshot A (Past) and Snapshot B (Present).
    2.  **Calc Engine** projects A using *actual* market rates.
    3.  **LLM** compares Projected A vs Actual B to explain variance.

### Mode 13: The "Behaviour Coach"
* **Intent:** Habits (e.g., "Micro-actions for this week").
* **Context:** Frankie (Momentum).
* **Regulatory Status:** General Advice / Nudges.
* **Engines:** `LLM` → `Strategy` → `Calc` → `Advice (Behaviour Safety)`.
* **Flow:**
    1.  **Strategy Engine** proposes micro-moves (e.g., +$50/wk savings).
    2.  **Calc Engine** quantifies delta.
    3.  **Advice Engine** checks Safety Rules (Don't reduce buffers below min).
    4.  **LLM** frames as an experiment.

### Mode 16: The "Collaborative Session"
* **Intent:** Live modeling (e.g., "Client meeting co-pilot").
* **Context:** Veris (Meeting).
* **Regulatory Status:** Personal Advice (Human-in-the-loop).
* **Engines:** `LLM` ⇄ `Calc` ⇄ `Strategy` ⇄ `Advice`.
* **Flow:**
    1.  **LLM** facilitates live questions to Strategy deltas.
    2.  **Calc** updates in near-real-time.
    3.  **Advice Engine** runs in **Warning Mode** (Adviser override).
    4.  **LLM** drafts meeting notes/SoA skeleton.

---

## 6. Technical Assurance Modes (QA & Dev)

Internal modes for testing, audit, and robustness.

### Mode 11: The "Bulk Auditor"
* **Intent:** Systemic risk check.
* **Context:** Licensee Compliance.
* **Flow:** **Strategy** loads all client scenarios -> **Advice Engine** re-runs new rules -> **LLM** generates Risk Report.

### Mode 15: The "Rule Lab"
* **Intent:** Logic regression testing.
* **Context:** Dev / Model Governance.
* **Flow:** **Strategy** generates golden cases -> **Calc** runs Baseline vs Candidate rules -> **Advice** checks invariants -> **LLM** generates Diff Report.

### Mode 17: The "Calculation Harness"
* **Intent:** Atomic CAL unit testing.
* **Context:** Engine QA.
* **Flow:** **Calc Harness** runs target CAL against golden inputs -> Compares Actual vs Expected -> **LLM** summarises failures.

### Mode 18: The "Scenario Fuzzer"
* **Intent:** Robustness/Edge case testing.
* **Context:** Dev.
* **Flow:** **Strategy** generates pseudo-random inputs -> **Calc** runs bundles -> **Advice** checks for NaN/Negatives -> **LLM** reports failure clusters.

### Mode 19: The "Advice Harness"
* **Intent:** Advice policy regression.
* **Context:** Licensee QA.
* **Flow:** Synthetic client catalogue -> **Advice Engine** runs -> Output compared to expected labels -> **LLM** explains mismatches.

### Mode 20: The "Prompt Contract Tester"
* **Intent:** LLM Schema QA.
* **Context:** Dev / Integration.
* **Flow:** Canonical prompts -> **LLM** -> Parse to Pydantic -> **Calc** validates structure -> Log regression.

### Mode 21: The "RAG Auditor"
* **Intent:** Reference/Source verification.
* **Context:** Legal QA.
* **Flow:** Reference tasks -> **RAG/LLM** -> **Advice** checks cited authorities vs expected sources.

### Mode 22: The "Load & Latency Bench"
* **Intent:** Scalability testing.
* **Context:** DevOps.
* **Flow:** **Strategy** generates workload -> **Perf Harness** runs batch Calc -> **LLM** summarises bottlenecks.

### Mode 23: The "Cross-Engine Consistency Checker"
* **Intent:** Semantic integrity check.
* **Context:** System Integration.
* **Flow:** **Calc** computes numbers -> **LLM** explains -> **Strategy/Advice** classify -> Flag if LLM text contradicts Calc numbers or Advice logic.

## 7. General Interaction & System Modes

These modes handle fallback interactions, operational assistance, and system introspection where a specific financial calculation strategy is not the primary trigger.

### Mode 24: The "Conversational Guide"
* **Intent:** General inquiry, vague concepts, or off-topic interaction (e.g., *"What is a franking credit?"* or *"Thanks!"*).
* **Context:** Frankie (App - Chat Interface).
* **Regulatory Status:** General Information / Non-Financial.
* **Engines:** `LLM` → `RAG` → `Advice (Guardrails)`.
* **Flow:**
    1.  **LLM** determines input does *not* require calculation or strategy.
    2.  **Advice Engine** checks for "Advice Traps" (ensures no inadvertent personal recommendations).
    3.  **RAG (Optional)** retrieves general educational content (e.g., definitions).
    4.  **LLM** responds with persona-driven, educational answer.
    5.  **Pivot Check:** If user provides specific numbers, LLM suggests transitioning to **Mode 1** or **Mode 3**.

### Mode 25: The "Practice Assistant"
* **Intent:** Operational support or content generation (e.g., *"Draft an email to Client X"* or *"How do I update inflation settings?"*).
* **Context:** Veris (Adviser Chat).
* **Regulatory Status:** Operational Support / Content Generation.
* **Engines:** `LLM` → `RAG` → `Advice (Content Audit)`.
* **Flow:**
    1.  **LLM** identifies intent: **Operational** (System help) or **Creative** (Drafting).
    2.  *Operational:* **RAG** retrieves system docs; LLM explains feature.
    3.  *Creative:* **LLM** generates draft using client context variables.
    4.  **Advice Engine** scans draft for compliance risks (e.g., promissory language).
    5.  **LLM** presents draft for Adviser review.

### Mode 26: The "System Oracle"
* **Intent:** Debugging and introspection (e.g., *"Why did the Strategy Engine reject that scenario?"*).
* **Context:** Admin Dashboard / Dev Console.
* **Regulatory Status:** System Administration.
* **Engines:** `LLM` → `Trace Logs` → `DB (Read-Only)`.
* **Flow:**
    1.  **LLM** identifies technical query.
    2.  **LLM** converts language to safe query for **Trace Logs** or **Metadata**.
    3.  Retrieves specific error stack, rule trigger, or metric.
    4.  **LLM** synthesizes root cause: *"Strategy loop timed out due to non-convergence of Taxable Income."*
    5.  Provides links to specific `trace_id` for deep dive.