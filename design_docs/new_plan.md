# Technical Plan & Tech Stack (Veris MVP – Solo Dev, Render + Vercel)

> This plan defines the **initial technical scope** and **stack** for the
> Veris/Calc Engine MVP. Frankie (consumer app) is explicitly **out of scope**
> for this phase.

---

## 1. Scope Boundaries

### 1.1 In Scope (MVP)

- **Core Calculation Engine** implementing canonical `CAL-*` calculations:
  - Personal income tax, CGT, basic property & debt, super contributions.
- **Backend API** on **Render**:
  - FastAPI service exposing calculation and scenario endpoints.
- **Single database (PostgreSQL)**:
  - Store scenarios, snapshots, references and QA metadata.
- **Projection Engine**:
  - Year-over-year projection loop producing `ProjectionOutput`.
- **TraceLog**:
  - Unified mechanism for recording *why* each numeric result was produced.
- **Strategy Engine: Foundational Framework**:
  - Implement the full Optimization Loop architecture (Solvers, Objectives, Constraints) capable of multi-variable solving. Initial implementation will focus on single-variable strategies (e.g., Salary Sacrifice) to prove the architecture, with multi-goal cascades added iteratively.
- **Advice Engine: Policy Logic Core**:
  - Implement the full Policy Evaluation structure (Conditions, Triggers, Actions). V1 will enforce 'Safety & Buffers', establishing the pattern for future 'Best Interest Duty' complex logic.
- **Simple RAG/knowledge base**:
  - File-first (`/knowledge_base`) + optional DB index, used for explanations and dev/compliance work.
- **Web UI on Vercel (Next.js)** with two spaces:
  - `/veris` – adviser-style Scenario Builder + Results + simple comparison + chat sidebar later.
  - `/dev` – dev/compliance dashboard (Rule Lab, Golden Cases, QA views, System Oracle).

### 1.2 Out of Scope (For Now / Future Phases)

These are **explicitly not included** in the Veris MVP build:

- **Frankie consumer app**:
  - No React Native / Expo mobile app.
  - No `/frankie` web space or consumer onboarding flows.
- **Comprehensive Advice Engine**:
  - No full BID/SoA generator.
  - No holistic multi-goal optimisation with full suitability proofs.
- **Full Strategy Engine**:
  - No large-scale cascade optimisation (“Holistic Plan” mode) beyond small targeted loops.
- **Deep RAG infrastructure**:
  - No pgvector, heavy ingestion pipeline, or complex retrieval ranking.
- **Production-grade auth & multi-tenancy**:
  - No full user management, roles, or licensee-level isolation.
- **Mobile deployment & app store concerns**:
  - No iOS/Android builds, push notifications, or offline sync.

---

## 2. Tech Stack Overview

### 2.1 Backend (Render)

- **Language**: Python 3.11
- **Web Framework**: FastAPI
- **Data Models**: Pydantic v2
- **Database**: PostgreSQL (Render managed DB)
  - Use **JSONB** for flexible storage of:
    - `state_json` (CalculationState snapshot).
    - `results_json` (ProjectionOutput + intermediaries).
- **ORM**: SQLAlchemy 2.0 + Alembic migrations.
- **Core Components**:

  - `engines/calc` (**Physics Engine**)
    - Pydantic state models (`CalculationState`, `ProjectionOutput`, etc.).
    - CAL functions per domain (`pit.py`, `cgt.py`, `super.py`, `property.py`, `portfolio.py`, `debt.py`, etc.).
    - `trace.py` helper with `add_trace(...)`.
    - **No DB or network calls** – pure math + state transitions.

  - `engines/strategy` (**Optimizer-lite**)
    - Small, targeted optimisation routines:
      - e.g. `optimize(target="net_wealth", variable="salary_sacrifice")` using a simple search loop calling the Projection Engine.
    - Keeps loops small and traceable (no black-box AI).

  - `engines/advice` (**Governance-lite**)
    - Simple `Policy` model and policy checks.
    - Example: `RULE-RISK-005` (Cash Buffer check using CAL-FND emergency fund metrics).
    - Produces warnings/flags; does **not** generate full SoA.

  - `llm` (**Orchestrator helpers**)
    - `client.py` – wrapper over OpenAI/OpenRouter.
    - `orchestrator.py` – maps:
      - Chat text → Intent → Execution Mode (Fact Check, Strategy Explorer, Adviser Sandbox, etc.).
      - Chat text → partial `CalculationState` snippets (State Hydration).
      - Trace + Projection → human-readable explanation.

  - `knowledge_base`
    - Markdown/YAML documents (legislation notes, worked examples, internal rules).
    - Light index (DB table or JSON) with `id`, `path`, `tags`, `description`, optional `embedding`.

### 2.2 Frontend (Vercel – Next.js)

- **Framework**: Next.js (App Router) + TypeScript
- **Styling**: Tailwind CSS (and optionally shadcn/ui later).
- **Data Layer**: TanStack Query for API calls & caching.
- **Spaces** (route groups):

  1. **Veris Space – `/veris`**
     - Scenario Builder.
     - Results view (year-by-year net wealth, tax, buffers).
     - Basic A/B scenario comparison.
     - Chat sidebar (later) hooked into LLM “Fact Check” and “Strategy Explorer”.

  2. **Dev/Compliance Space – `/dev`**
     - Mode 26 “System Oracle”:
       - View raw JSON state.
       - View TraceLog per scenario/year.
       - Run manual calculation tests.
     - Rule Lab – per-CAL golden case runner.
     - Golden Cases status dashboard.
     - Basic Bulk Audit / QA & perf view (later).

- **Auth (MVP)**:
  - Simple environment guard or basic auth for `/dev`.
  - Adviser UI can initially assume a trusted, single-user environment.

### 2.3 LLM & RAG

- **LLM Provider**:
  - OpenAI or OpenRouter, configurable via env vars on Render.
- **Responsibilities**:
  - **Intent Classification**:
    - Map free text → Execution Mode (Fact Check, Crystal Ball, Strategy Explorer, Adviser Sandbox, etc.).
  - **State Hydration**:
    - Extract JSON fragments for `EntityContext`, `CashflowContext`, etc. from chat or notes.
  - **Narrative Generation**:
    - Convert `TraceLog + ProjectionOutput` into friendly explanations.
  - **Citations** (with RAG):
    - Pull 1–3 relevant snippets from `/knowledge_base` when needed.

- **RAG (Minimal, file-first)**:
  - Folder: `/knowledge_base` with md/YAML docs.
  - Small index: `references` table or `references_index.json`.
  - Flow:
    - Orchestrator chooses a small set of reference IDs.
    - Backend loads those snippets only.
    - Snippets are added to the LLM prompt to support explanation or dev/compliance.

---

## 3. Repo Structure

```text
/my-finance-app
  /backend
    /core
      main.py          # FastAPI app entry, routing
      config.py        # env, settings
      database.py      # SQLAlchemy + Postgres connection
    /engines
      /calc            # PURE MATH + state models
        state_models.py
        projection_engine.py
        pit.py
        cgt.py
        super.py
        property.py
        portfolio.py
        debt.py
        trace.py
      /strategy        # small optimisation loops (MVP)
        optimize_salary_sacrifice.py
      /advice          # light governance rules (MVP)
        policies.py
    /llm
      client.py        # OpenAI/OpenRouter wrapper
      orchestrator.py  # Intent → Mode → Engine calls
    /knowledge_base    # md/YAML docs, simple index
    /tests
      /golden          # ATO-style test cases (Excel parity)
      /unit
  /frontend
    /web               # Next.js app deployed to Vercel
      /veris           # adviser space
      /dev             # dev/compliance dashboard
      /components
      /lib
  /specs               # spec-kit master spec/plan + views
    master_spec.md
    master_plan.md
    /views
      calc_engine_view.md
      llm_view.md
      ui_view_veris.md
      ui_view_dev.md

```

## 4. Backend Architecture (High-Level)

### 4.1 Core Principles

- **Pure Calculation Engine ("Physics Engine")**
  - `engines/calc` has **no DB or network dependencies**.
  - CAL functions take structured inputs and return deterministic outputs + trace entries.
- **Projection Engine**
  - Lives in `projection_engine.py`.
  - Loops over years 0–N:
    - Updates balances, debts, super, and cash buffer each year.
    - Records annual results into `ProjectionOutput`.
- **State & Projection Models**
  - `CalculationState` – Year 0 snapshot of:
    - GlobalContext, EntityContext, PositionContext, CashflowContext.
  - `ProjectionOutput` – list of `YearSnapshot`s with:
    - balances, net wealth, tax paid, cash buffers, etc.
  - `CalculatedIntermediariesContext` – per-entity results namespaced by domain.

### 4.2 Core Endpoints (MVP, `/api/v1/...`)

- `POST /api/v1/calc/run`
  - Input: `CalculationState` + projection config.
  - Output: `ProjectionOutput` + summary metrics.
- `POST /api/v1/scenarios`
  - Create a new scenario with `state_payload` (JSONB).
- `GET /api/v1/scenarios/{id}`
  - Fetch scenario + latest snapshot/summary.
- `POST /api/v1/scenarios/{id}/run`
  - Run calc and persist a new `ScenarioSnapshot`.
- `POST /api/v1/scenarios/compare`
  - Compare scenarios A vs B; return key metric deltas.
- `GET /api/v1/trace/{scenario_id}`
  - Retrieve TraceLog entries for dev/compliance.
- `/api/v1/qa/*`
  - Internal QA routes for `/dev`:
    - `POST /api/v1/qa/run-golden-suite`
    - `POST /api/v1/qa/run-single-cal`
    - `POST /api/v1/qa/bulk-audit` (later).

---

## 5. Frontend Architecture (Next.js on Vercel)

### 5.1 Veris Space (`/veris`)

Goal: Adviser-style sandbox & internal demo environment.

- **Pages/Routes (MVP)**:
  - `/veris/scenario`
    - Scenario Builder form:
      - Income, property, debts, contributions, buffers.
    - Saves `CalculationState` to backend as a `Scenario`.
  - `/veris/results`
    - Calls `/api/v1/scenarios/{id}/run`.
    - Shows:
      - Tax summary.
      - Net wealth timeline.
      - Debt profiles and buffers.
  - `/veris/compare`
    - Select base scenario + variant.
    - Show side-by-side metrics and simple charts.
  - `/veris/chat` (later)
    - Chat wrapper around `Fact Check` and `Crystal Ball` modes.

### 5.2 Dev/Compliance Space (`/dev`)

Goal: Internal cockpit for development, testing, and compliance checks.

- **Pages/Routes (MVP)**:
  - `/dev`
    - Overview dashboard:
      - Health (ping backend).
      - Last golden test run status.
      - Counts of scenarios, snapshots.
  - `/dev/rule-lab`
    - Mode 15/17:
      - Choose a `CAL-*`.
      - Select a golden case from list.
      - Call `/api/v1/qa/run-single-cal`.
      - Show inputs, outputs, and trace.
  - `/dev/golden`
    - List all golden cases and their PASS/FAIL status.
    - Button: `Run Golden Suite` → calls `/api/v1/qa/run-golden-suite`.
  - `/dev/trace`
    - Select scenario + year index.
    - Show TraceLog entries (with filter by severity/tags).
  - `/dev/perf` (later)
    - Simple latency stats from metrics endpoint.

---

## 6. Phased Implementation Plan

### Phase 1 – The Physics Engine (Weeks ~1–2)

**Goal:** A Pydantic-powered math engine that passes ATO “Golden Tests”.  
**No API/DB yet. Run everything via `pytest` / REPL.**

- [ ] **Task 1.1 – Define `CalculationState` Pydantic models**
  - Implement:
    - `GlobalContext`
    - `EntityContext`
    - `PositionContext`
    - `CashflowContext`
    - `CalculatedIntermediariesContext`
    - `ProjectionOutput` / `YearSnapshot`
- [ ] **Task 1.2 – Create TraceLog mechanism**
  - Implement `trace.py` with a helper:
    - `add_trace(state, calc_id, entity_id, field, severity, explanation, metadata)`
  - Ensure every CAL can log decisions (“why this number?”).

- [ ] **Task 1.3 – Implement “Golden Four” CALs**
  - `CAL-PIT-001` – PAYG tax (2024/25 resident scales).
  - `CAL-SUP-007` – Super contributions tax (15% on concessional).
  - `CAL-PRP-005` – Net rental cashflow / yield for an investment property.
  - `CAL-DEBT-001` – P&I loan amortisation schedule (loan repayment & interest).

- [ ] **Task 1.4 – Implement Projection Engine (Year-over-Year loop)**
  - Single function in `projection_engine.py`:
    - Input: `CalculationState`, projection config.
    - Output: `ProjectionOutput` with Y0–YN snapshots.
    - Uses Golden Four CALs along the path.

- [ ] **Task 1.5 – Golden tests vs Excel**
  - Build Excel or CSV “Golden Datasets” for:
    - PAYG examples from ATO.
    - Super contribution + tax examples.
    - Simple property & mortgage scenarios.
  - Write `tests/golden/test_core_calcs.py` verifying parity to the cent.

---

### Phase 2 – The Brain & Persistence (Weeks ~3–4)

**Goal:** Persist state to Postgres and run targeted optimisation loops.  
**Now running as a FastAPI service on Render.**

- [ ] **Task 2.1 – Set up Postgres (local dev + Render)**
  - Local: Dockerised Postgres or a local instance.
  - Render: Managed Postgres instance.
  - Configure SQLAlchemy connection in `database.py`.

- [ ] **Task 2.2 – Implement DB models**
  - SQLAlchemy models:
    - `User` (simple/optional at first).
    - `Scenario`:
      - `id`, `owner_id`, `name`, timestamps.
      - `state_payload` (JSONB) storing `CalculationState`.
    - `ScenarioSnapshot`:
      - `scenario_id`, `year_index`, `state_json`, `results_json`.
    - Optional `AssumptionSet` (for later base vs stress cases).

- [ ] **Task 2.3 – Strategy Engine (Empty but Capable)**
  - Build Abstract Optimization Interface. Implement the Optimizer class that accepts generic variables and constraints. Prove it with the 'Salary Sacrifice' strategy.

- [ ] **Task 2.4 – Advice Engine (Empty but Capable)**
  - Build Policy Evaluation Pipeline. Implement the generic evaluate_policies(scenario) function. Prove it with 'Cash Buffer' and 'LVR' rules.

- [ ] **Task 2.5 – Expose first API endpoints**
  - `POST /api/v1/calc/run`
  - `POST /api/v1/scenarios`
  - `GET /api/v1/scenarios/{id}`
  - `POST /api/v1/scenarios/{id}/run`
  - Deploy backend to **Render**.

---

### Phase 3 – The Orchestrator (Weeks ~5–6)

**Goal:** Connect natural language to the engine via a thin LLM layer.**

- [ ] **Task 3.1 – Build LLMClient**
  - `llm/client.py`:
    - Wrap OpenAI/OpenRouter calls.
    - Config via env vars (Render secrets).
- [ ] **Task 3.2 – Implement Intent Classification**
  - Map user text → Execution Mode:
    - Fact Check
    - Crystal Ball
    - Strategy Explorer
    - Adviser Sandbox
    - (Others later).
- [ ] **Task 3.3 – Implement State Hydration**
  - Prompt templates that:
    - Extract `EntityContext` and basic `CashflowContext` JSON from free text.
  - Structured output validated by Pydantic before use.
- [ ] **Task 3.4 – Narrative Generation**
  - Prompt templates to convert:
    - `TraceLog + ProjectionOutput (+ optional KB snippets)`
    - → human explanation paragraphs for `/veris` UI or logs.

---

### Phase 4 – The Interface (Weeks ~7–9, Vercel)

**Goal:** Usable web UI for Devs and Advisers (Frankie remains out-of-scope).**

- [ ] **Task 4.1 – Setup Next.js app on Vercel**
  - Create `/frontend/web`:
    - App Router.
    - Tailwind CSS.
    - Basic layout and navigation.
  - Configure deployment to **Vercel**.

- [ ] **Task 4.2 – Build Mode 26: "System Oracle" (/dev dashboard)**
  - `/dev`:
    - Display raw JSON state for a selected scenario.
    - Display TraceLog for scenario/year.
    - Strategy Debugging: Build visualization for Optimization Loops (see the engine iterating towards a solution).
    - Buttons to run:
      - Single CAL evaluation (Rule Lab).
      - Golden Suite tests via `/api/v1/qa/run-golden-suite`.

- [ ] **Task 4.3 – Build Veris Finance (/veris)**
  - `/veris/scenario`:
    - Form that builds `CalculationState`.
    - Save scenario via API.
  - `/veris/results`:
    - Runs scenario via API.
    - Renders charts for net wealth, tax, buffers, debt.
  - `/veris/compare`:
    - Side-by-side comparison of two scenarios.
  - `/veris/chat` (later extension):
    - Simple chat sidebar calling “Fact Check” and “Crystal Ball” modes.

- [ ] **Task 4.4 – Frankie’s Finance (/frankie) – FUTURE, OUT OF SCOPE**
  - **Not part of this MVP.** When in scope, will include:
    - Mobile-responsive consumer chat interface.
    - Simple “Net Wealth” trajectory view for consumers.
  - For now, this remains documented but **deferred**.

---

### Phase 5 – Capability Expansion (Weeks ~10–12)

**Goal:** Turn on the "Big Brain" features - multi-goal optimization and complex compliance.**

- [ ] **Task 5.1 – Implement Multi-Goal Optimization**
  - Solve for Debt Paydown AND Super Contribution simultaneously.

- [ ] **Task 5.2 – Implement Complex Compliance**
  - Advice Engine checks 'Better Off' test by running comparative simulations automatically.

- [ ] **Task 5.3 – RAG Manual Authoring**
  - Keep the source simple for now, but let the rules be complex.

---

## 7. Core Execution Modes (Reference)

The backend will respond differently based on **Execution Mode** (some fully supported in MVP, others partial/future):

1. **Fact Check**  
   - Flow: **LLM → Calc (Single Point)**  
   - Example: “What is my current net wealth / tax / buffer?”

2. **Crystal Ball**  
   - Flow: **LLM → Calc (Projection) → Advice (Observer)**  
   - Example: “Will I have enough to retire at 60?”  
   - Advice Engine here only performs sanity checks (not full suitability).

3. **Strategy Explorer**  
   - Flow: **LLM → Strategy (Optimize small lever) → Calc → Advice (Safety)**  
   - Example: “How could I pay less tax using super?”  
   - Strategy Engine varies one or two levers (e.g. salary sacrifice) within caps.

4. **Adviser Sandbox**  
   - Flow: **User Inputs → Calc → Advice (Warning)**  
   - Implemented in `/veris`: advisers directly build scenarios and see warnings.

5. **Scaled Advice** (Future / partial)  
   - Flow: **LLM → Strategy (Narrow) → Advice (Suitability)**  
   - Single-issue recommendations (e.g. “Top up super by $X”) with stronger checks.

6. **Holistic Plan** (Future, out of MVP)  
   - Flow: **LLM → Strategy (Cascade) → Advice (BID)**  
   - Full multi-goal optimisation and BID-style comparison of multiple strategies.

7. **Proactive Monitor** (Future)  
   - Flow: **Trigger → Strategy (Scan) → Advice**  
   - Example: new tax rules → rescan clients → flag those impacted.

> MVP will **fully support** modes 1, 2 (simplified), and 4 inside `/veris` and `/dev`,  
> will experiment with 3 in limited form, and will **only scaffold** 5–7 for later.

---

## 8. Explicit Out-of-Scope Summary

To be absolutely clear, the **Veris MVP** delivered via **Render (backend)** + **Vercel (frontend)** does **not** include:

- A Frankie mobile/consumer app or `/frankie` web experience.
- Full BID-compliant, licensee-ready Advice Engine.
- Large-scale optimisation across many variables/goals.
- Advanced RAG (vector DB, full legislation ingestion).
- Rich auth, tenancy, integrations, or outsourced product feeds.

The focus is a **fast, deterministic calculation engine**, a **clean API**, and a **two-space web UI** that supports:

- Real adviser-style experimentation (`/veris`), and
- Deep dev/compliance testing and inspection (`/dev`).

---

## 9. Success Metrics (Revised)

- **Golden Test Pass Rate: 100%**
- **SC-002**: System processes multi-variable strategy optimizations within 30 seconds.
- **Advice Engine successfully blocks 100% of unsafe scenarios defined in the test suite.**
