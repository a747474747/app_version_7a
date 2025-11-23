# System Architect’s Handbook: Veris & Frankie Finance

**Version:** 1.0
**Scope:** High-Level Architecture & Execution Strategy
**Philosophy:** Probabilistic Interface / Deterministic Core

---

## 1. The Core Philosophy
We are solving the "Black Box Problem" of AI in finance. Large Language Models (LLMs) are brilliant translators but terrible calculators. They hallucinate numbers and invent laws.

To solve this, we adhere to **The Separation of Concerns**:

1.  **The Interface is Probabilistic (AI):** It understands intent, nuance, and emotion. It translates human language into structured data.
2.  **The Core is Deterministic (Math):** It operates on strict rules (`CAL-PIT-001`). Given the same inputs, it *always* returns the same outputs.
3.  **The Governance is Explicit (Rules):** Compliance is not a "vibe"; it is a set of logic gates checked by code.

---

## 2. The Four-Engine Architecture
The system is composed of four distinct logical engines. They communicate via structured **State Objects**, never via natural language.

| Engine | Analogy | Responsibility | Input/Output |
| :--- | :--- | :--- | :--- |
| **1. LLM Orchestrator** | **The Translator** | Identifying intent, extracting data, and explaining results. It *never* does math. | Text ↔ JSON |
| **2. Calculation Engine** | **The Physics Engine** | The "Source of Truth." Stateless, amoral financial mathematics. It computes Tax, Wealth, and Cashflow. | State ↔ Projections |
| **3. Strategy Engine** | **The Optimizer** | The "Solver." It iterates on the Physics Engine to find the best outcome (e.g., "Maximize Net Wealth"). | Constraints ↔ Optimal Scenario |
| **4. Advice Engine** | **The Regulator** | The "Building Inspector." It checks specific policies (BID, liquidity, risk) to approve or warn against a strategy. | Scenario ↔ Compliance Flags |

---

## 3. The Data Architecture (The "Spine")

The system relies on a single, unified data structure that flows through all engines.

### 3.1 The `CalculationState` (Year 0)
This is the "DNA" of a client. It is a Pydantic model stored as `JSONB` in PostgreSQL.
* **Global Context:** Tax year, inflation settings.
* **Entity Context:** People (primary, partner), Companies, Trusts.
* **Position Context:** Assets (Property, Super) and Liabilities (Loans).
* **Cashflow Context:** Incomes, Expenses, Contributions.

### 3.2 The Projection Timeline
We do not mutate the State in place for projections. We generate a **Timeline**.
* **Input:** `CalculationState` (Year 0).
* **Process:** The Engine applies growth rates, tax rules, and cashflows year-over-year.
* **Output:** `ProjectionOutput` (A list of Snapshots from Year 0 to Year N).

### 3.3 Traceability
Every number must explain itself.
* **TraceLog:** As the engine runs, it writes to a log: *"Calculated Tax: $25k. Reason: Applied 2025 Resident Rates to $120k income."*
* This log is passed to the LLM so it can explain the "Why" to the user accurately.

---

## 4. Operational Workflows (The "Modes")

The app does not have a single linear flow. The LLM Orchestrator identifies the **User Intent** and selects an **Execution Mode**.

### Tier 1: Factual & Educational
* **Mode 1 (Fact Check):** "What is my balance?" → Calc Engine.
* **Mode 2 (Crystal Ball):** "Will I be okay?" → Calc Engine (Projection).
* **Mode 24 (Conversational):** "What is a franking credit?" → RAG Layer.

### Tier 2: Strategic & Exploratory
* **Mode 3 (Strategy Explorer):** "How do I pay less tax?" → Strategy Engine (Optimization Loop).
* **Mode 4 (Adviser Sandbox):** Manual scenario comparison (A vs B).

### Tier 3: Compliance & Execution
* **Mode 5 (Scaled Advice):** "Top up my super." → Full Compliance Check.
* **Mode 11 (Bulk Auditor):** "Did the new tax law affect my clients?" → Batch run of Advice Engine.

---

## 5. The Tech Stack (Pragmatic Solo-Dev)

We prioritize **Developer Experience** and **Type Safety** to allow a single developer to manage a complex financial system.

### The "Pure Package" Pattern
* **Frontend (Vercel):** Next.js 14 (App Router). Handles UI and State Management.
* **Backend (Render):** FastAPI (Python).
* **Database (Render):** PostgreSQL.

**Crucial Architectural Decision:**
The `calculation_engine` is a **Pure Python Package**. It contains **no database calls** and **no async code**.
* It takes a Pydantic Object (`CalculationState`).
* It returns a Pydantic Object (`ProjectionOutput`).
* **Why?** This makes unit testing trivial ("Golden Tests") and ensures the math is fast and portable.

---

## 6. The Execution Strategy (Phased Build)

We build from the "Core Outwards." We do not build the UI until the Math works.

### Phase 1: The Physics (Weeks 1-2)
* **Focus:** Math & correctness.
* **Actions:**
    * Define Pydantic Models (`state.py`).
    * Write the "Golden Four" CALs (Tax, Super, Debt, Property).
    * Verify against Excel spreadsheets (The "Golden Datasets").
* **Outcome:** A Python script that calculates tax perfectly.

### Phase 2: The Brain (Weeks 3-4)
* **Focus:** Persistence & Logic.
* **Actions:**
    * Set up FastAPI & Postgres on Render.
    * Implement the "Scenario" storage (JSONB).
    * Build the "Strategy Loop" (e.g., iterate salary sacrifice to find the optimum).
* **Outcome:** An API that accepts a client JSON and returns an optimized strategy.

### Phase 3: The Voice (Weeks 5-6)
* **Focus:** Translation.
* **Actions:**
    * Connect OpenRouter/OpenAI.
    * Write the "State Hydration" prompts (Text → JSON).
    * Write the "Narrative" prompts (TraceLog → Explanation).
* **Outcome:** You can chat to the API, and it runs the math.

### Phase 4: The Face (Weeks 7-9)
* **Focus:** User Experience.
* **Actions:**
    * Build the Next.js Dashboard (`/veris`).
    * Build the Dev Console (`/dev`) for debugging rules.
* **Outcome:** A usable product for Advisers.

---

## 7. Directory Map

This structure keeps the "Math" safe from the "Web App".

```text
/backend
  /src
    /engines
      /calc          <-- THE PHYSICS. Pure Python. No DB.
      /strategy      <-- THE OPTIMIZER. Loops over Calc.
      /advice        <-- THE REGULATOR. Checks policies.
    /models          <-- THE VOCABULARY. Shared Pydantic schemas.
    /api             <-- THE GATEWAY. FastAPI routes.
    /llm             <-- THE TRANSLATOR. Prompts & Clients.
  /tests             <-- GOLDEN DATASETS.

```

  ## 8. Summary of Success
Success for this project is defined by:
1.  **Determinism:** If I run the same scenario twice, I get the exact same number.
2.  **Explainability:** If the tax changes, the TraceLog tells me exactly which bracket caused it.
3.  **Safety:** The Advice Engine flags dangerous strategies *before* the user sees them.
4.  **Velocity:** The "Pure Package" structure allows you to write and test complex financial rules without worrying about database migrations or UI state.