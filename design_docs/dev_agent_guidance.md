# Dev Agent Guidance – Context & Automation Framework

> Goal: Ensure every AI-assisted coding session gets **just enough context** –
> never too little to be dangerous, never so much it blows the context window –
> while staying faithful to **Spec-Driven Development (SDD)** and the
> **Probabilistic Interface / Deterministic Core** philosophy.

This document tells automation scripts **what** to assemble for the AI and
**how** to wire specs, plans, and tasks into small, coherent context bundles.

---

## 1. Mental Model: “Context Bundles”, Not “Throw Everything In”

Every time an AI agent writes code, it should be operating under a **Context Bundle**:

1. **Core Invariants** – the unchanging “laws of the project”.
2. **Engine Slice** – a focused view for the specific engine or layer.
3. **Task Slice** – the spec/plan/tasks relevant to the concrete change.

Think of it as three concentric circles:

- **Inner circle**: Pydantic models + calculation engine contracts.
- **Middle circle**: The engine-specific view (Calc / Strategy / Advice / LLM / UI).
- **Outer circle**: The exact feature spec + plan + file manifest + checklist.

Scripts are responsible for assembling this bundle; the agent never sees random,
unstructured project files unless they are explicitly part of the bundle.

---

## 2. The Three Layers of Context

### 2.1 Layer 1 – Core Invariants (Always Included, Small)

These are **short, stable** documents that must be present in *every* coding
session, regardless of engine or feature:

1. **System Architect’s Handbook** (this document, or a trimmed version).
2. **Canonical State & CAL Overview**:
   - `canonical_calc_engine_parameters.md` (or a short “view” version).
   - List of CAL domains and IDs (e.g. PIT, CGT, SUP, PRP, PFL, FND).
3. **Project Rules / Constitution Extract**:
   - A 1–2 page extract containing:
     - “LLM doesn’t do math; Calc Engine is source of truth.”
     - “No DB calls inside `engines/calc`.”
     - “CALs are atomic, pure functions with traces.”
     - “Specs → Plans → Tasks → Code” sequence.

**Key constraint**:  
Core invariants must be **short enough** to fit into every context bundle
without dominating the token budget. If they get too long, create a
`core_invariants_view.md` with only the essentials.

---

### 2.2 Layer 2 – Engine Slice (Per-Engine Views)

For each engine, maintain a short “view” that explains:

- What this engine is allowed to do.
- What it must never do.
- Its inputs/outputs and its relationship to other engines.

Examples:

- `views/calc_engine_view.md`
- `views/strategy_engine_view.md`
- `views/advice_engine_view.md`
- `views/llm_orchestrator_view.md`
- `views/ui_veris_view.md`
- `views/ui_dev_dashboard_view.md`

Each view should be:

- 1–4 pages max.
- No global philosophy rehash – just:
  - The **responsibility** of this engine.
  - The **contracts** (Pydantic models, CAL IDs, ProjectionOutput).
  - **Examples** of allowed interactions (e.g. “Calc Engine can only read its
    input state, cannot touch DB, cannot call LLM”).

**Script rule**:  
When a task is tagged with `engine: calc`, the automation must always include:

- Core invariants (Layer 1).
- `views/calc_engine_view.md`.

If `engine: ui-veris`, then include `views/ui_veris_view.md` instead.

---

### 2.3 Layer 3 – Task Slice (Spec / Plan / Tasks / Files)

This is the **workbench** for the agent: what actual change is requested?

Each feature/change should have:

- A **feature spec**: `specs/features/<feature-id>/spec.md`
- A **feature plan**: `specs/features/<feature-id>/plan.md`
- A **task list**: `specs/features/<feature-id>/tasks.md`
- A **file manifest**: `specs/features/<feature-id>/file-manifest.md`
- Optional: `checklist.md`, `agent-file.md`

The task list is what your scripts operate on. It should be machine-friendly.

Example `tasks.md` row:

| Task ID     | Engine | Feature ID     | CAL IDs                  | Files (hint)                                      | Phase |
|------------|--------|----------------|--------------------------|---------------------------------------------------|-------|
| T-CAL-001  | calc   | SPEC-CALC-001  | CAL-PIT-001, CAL-PIT-005 | `engines/calc/pit.py`, `tests/unit/test_pit.py`   | 1     |
| T-UIV-002  | ui-veris | SPEC-UIV-001 | –                        | `frontend/web/app/veris/results/page.tsx`         | 4     |

**Script rule**:  
When launching an agent for a given Task ID, the script should:

1. Look up the row in `tasks.md`.
2. Load:
   - Feature `spec.md`
   - Feature `plan.md`
   - The specific task description from `tasks.md`.
   - The file manifest for that feature (so Cursor can navigate files properly).

---

## 3. How Scripts Should Build Agent Context

### 3.1 High-Level Algorithm (for `update-agent-context`)

Given a `Task ID`, the script should:

1. **Resolve metadata from tasks**
   - Engine (`calc`, `strategy`, `advice`, `llm`, `ui-veris`, `ui-dev`).
   - Feature ID (e.g. `SPEC-CALC-001`).
   - CAL IDs touched (optional, helpful).
   - Candidate file paths.

2. **Assemble Context Bundle:**

   **Always:**
   - Core invariants (short).
   - System Architect’s Handbook (or trimmed view).

   **Per Engine:**
   - `views/<engine>_view.md`.

   **Per Feature:**
   - `specs/features/<feature-id>/spec.md`
   - `specs/features/<feature-id>/plan.md`
   - The relevant row from `tasks.md`.
   - `file-manifest.md` for that feature.

   **Optionally, per CAL:**
   - If CAL IDs are listed, include relevant section(s) from
     `canonical_calc_engine_parameters.md` or a CAL-specific view file
     (`views/cal_pit_view.md`, etc.).

3. **Inject a Small, Stable System Prompt**

   At the top of the agent chat, the script should prepend a short instruction like:

   > You are working on Task `T-CAL-001` in a Spec-Driven Development project.  
   > 1. Read the feature spec and plan first.  
   > 2. Obey the Calc Engine and State model contracts.  
   > 3. Only modify files listed in the file manifest, unless the plan explicitly says otherwise.  
   > 4. Keep the Calculation Engine pure (no DB, no network, no LLM calls).  

4. **Optionally: include relevant code files**

   - Use the file manifest and task metadata to pre-open:
     - Existing implementation files.
     - Tests that need updating.
   - Do **not** open the entire repo; stay within the feature’s footprint.

---

## 4. Automation Script Roles

You can structure scripts loosely like this (names are illustrative):

### 4.1 `create-new-feature.ps1`

- Creates folder: `specs/features/<feature-id>/`.
- Seeds:
  - `spec.md` from `spec-template.md`.
  - `plan.md` from `plan-template.md`.
  - `tasks.md` from `tasks-template.md`.
  - `file-manifest.md` from `file-manifest-template.md`.
  - `checklist.md`, `agent-file.md` if needed.
- Ensures Spec ID, Plan ID, and Feature ID are consistent.

### 4.2 `setup-plan.ps1`

- Given a feature, ensures:
  - Spec & plan are filled.
  - Tasks have IDs, engine tags, CAL tags, file hints.
- Might call an LLM to:
  - Expand tasks based on spec.
  - Propose a file manifest.

### 4.3 `update-agent-context.ps1`

- **Key script** used in Cursor / dev flow.
- Given:
  - `Task ID`
  - (Optionally) Engine override or Feature ID
- Assembles the context bundle:
  - Core invariants.
  - Engine view.
  - Feature spec + plan.
  - Task row + file manifest.
  - Any CAL / mode references.
- Writes a single **agent context markdown file** (or environment variable) that Cursor uses as the “preloaded” context for that Chat/Session.

---

## 5. How an Agent Should Use the Context (Expected Behaviour)

Every agent run should be implicitly guided to follow this mental sequence:

1. **Understand the world (Core Invariants).**
   - “This is a deterministic core / probabilistic interface app.”
   - “Calc Engine is pure. Advice Engine checks policies.”

2. **Understand the engine (Engine View).**
   - “I am in the Calc Engine; I may not touch DB or LLM.”
   - “I must work with CalculationState and ProjectionOutput only.”

3. **Understand the feature (Spec & Plan).**
   - “What change is being requested?”
   - “What CALs and modes are involved?”
   - “What is the definition of done for this feature?”

4. **Understand the task (Task row + file manifest).**
   - “What is my exact sub-piece of work?”
   - “Which files should I edit or create?”

5. **Only then, write code and tests.**

The spec-driven loop becomes:

> **Spec → Plan → Tasks → Context Bundle → Code + Tests → PR**

---

## 6. Example: Implementing CAL-PIT-001

**Task row:**

| Task ID     | Engine | Feature ID     | CAL IDs     | Files (hint)                               | Phase |
|------------|--------|----------------|-------------|--------------------------------------------|-------|
| T-CAL-001  | calc   | SPEC-CALC-001  | CAL-PIT-001 | `engines/calc/pit.py`, `tests/unit/test_pit.py` | 1     |

**Context bundle for T-CAL-001:**

- Core:
  - System Architect’s Handbook (trimmed).
  - Calc engine state & CAL overview view.
- Engine:
  - `views/calc_engine_view.md`
- Feature:
  - `specs/features/SPEC-CALC-001/spec.md`
  - `specs/features/SPEC-CALC-001/plan.md`
  - `specs/features/SPEC-CALC-001/tasks.md` (filtered to T-CAL-001 row)
  - `specs/features/SPEC-CALC-001/file-manifest.md`
- CAL-specific:
  - CAL-PIT-001 section from `canonical_calc_engine_parameters.md`.
- Files:
  - Open `engines/calc/pit.py` (existing or empty).
  - Open `tests/unit/test_pit.py`.

The agent now has everything it needs to:

- Implement `CAL-PIT-001` as a pure function.
- Write tests that match “Golden Dataset” examples.
- Respect the architecture, without seeing unrelated UI or LLM code.

---

## 7. Guardrails in Agent Prompts

Your Cursor project rules (or per-task agent prompts) should always reinforce:

- “Never invent new CAL IDs; always use existing IDs from the canonical list.”
- “Do not modify master files from a feature task unless explicitly authorised.”
- “For Calc Engine tasks, **do not** import database, HTTP clients, or LLM clients.”
- “Every CAL change must include/update unit tests or golden tests.”
- “Prefer extending existing modules over creating new top-level scripts.”

---

## 8. Summary

- Specs & plans remain your **source of truth**, but the AI never gets them all at once.
- Instead, scripts assemble **small, purposeful Context Bundles**:
  - Core Invariants → Engine Slice → Task Slice.
- This lets you:
  - Maintain your ambitious architecture.
  - Keep each agent run constrained and productive.
  - Avoid the two failure modes: “LLM has no idea what project it’s in” vs
    “LLM is drowning in 200 pages of context.”

As you evolve the project, you only need to:

- Keep Core Invariants short and stable.
- Keep engine views accurate.
- Tag tasks well (Engine, CAL IDs, files).
- Improve scripts to stitch the right bundle every time.
