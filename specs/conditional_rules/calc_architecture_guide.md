# Calculation Engine Architecture Guide



**Purpose**: Define the modular structure for the deterministic Calculation Engine to ensure auditability, testability, and scalability.

**Applies to**: `backend/src/engines/calculation/`



## 1. Core Philosophy

The Calculation Engine is a **deterministic** system. It must never contain AI/LLM logic.

* **Input**: `CalculationState` (Pydantic Model)

* **Output**: `CalculationResult` (Value + Trace Log)

* **Structure**: Domain-Driven Modules (not one giant file)



## 2. Directory Structure



The engine MUST follow this strict hierarchy:



```text

backend/src/engines/calculation/

├── __init__.py            # Public API (exposes `run_calculation`)

├── core.py                # Shared mathematical utilities (tax scales, rounding)

├── registry.py            # Maps "CAL-ID" strings to functions

├── domains/               # ⚠️ Domain Logic Lives Here

│   ├── __init__.py

│   ├── tax_personal.py    # CAL-PIT-* (PAYG, Medicare)

│   ├── tax_company.py     # CAL-CIT-* (Company Tax)

│   ├── superannuation.py  # CAL-SUP-* (Concessional Caps, Div293)

│   ├── cgt.py             # CAL-CGT-* (Capital Gains)

│   ├── property.py        # CAL-PRP-* (Negative Gearing)

│   └── retirement.py      # CAL-RPT-* (Age Pension)

└── projection.py          # Orchestrator for multi-year loops



3. The Registry Pattern

We use a Registry to decouple the Orchestrator from specific functions. The Orchestrator requests "CAL-PIT-001", and the Registry finds the function.



registry.py pattern:



Python



from .domains import tax_personal, superannuation



CALCULATION_REGISTRY = {

    "CAL-PIT-001": tax_personal.run_CAL_PIT_001,

    "CAL-SUP-002": superannuation.run_CAL_SUP_002,

}



def get_calculation(cal_id: str):

    return CALCULATION_REGISTRY[cal_id]



4. Implementation Rules



One Function Per CAL-ID: run_CAL_PIT_001 handles only CAL-PIT-001.



No Hardcoded Rates: All rates (tax brackets, caps) must come from the RuleLoader service, not hardcoded constants.



Traceability: Every function MUST return a TraceEntry linking the result to the specific CAL-ID.



Isolation: A calculation function should generally not call other calculation functions directly; it should rely on the CalculationState having the necessary intermediate data (dependency injection via state).





---



### 2. Update to `plan.md`

We need to insert the refactoring phase into your plan. Since you are partway through Phase 2, we will add a **"Phase 2.1: Refactor"** checkpoint.



**Add this section to `plan.md` just before "Phase 2.3: Calculation Expansion":**



```markdown

### Phase 2.1: Calculation Engine Refactor (Critical Tech Debt)

**Goal**: Move from monolithic `__init__.py` to domain-driven module structure to support Extended Tier growth.



**Implementation Tasks**:

1.  **Create Directory Structure**: Set up `backend/src/engines/calculation/domains/`.

2.  **Implement RuleLoader**: Build service to read `specs/rules/*.yaml` instead of hardcoding values (Completes T009b).

3.  **Migrate Core Calculations**: Move existing CAL-PIT/SUP/CGT functions from `__init__.py` to their respective domain files (`tax_personal.py`, etc.).

4.  **Build Registry**: Implement `registry.py` to map string IDs to functions.

5.  **Update Consumers**: Refactor `projection.py` and API routers to use the Regis
