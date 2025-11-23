# Architecture & Implementation Integration Map

**Date:** 2025-11-23
**References:** - `workflows_and_modes.md` (Architecture Definition)
- `interaction_architecture.md` (Interaction Models)
- `tasks.md` (Implementation Plan)

## 1. Executive Summary

This document maps the **Four-Engine Architecture** and **26 Operational Modes** defined in the design specifications to the specific execution phases in the implementation plan. It serves as a verification traceability matrix to ensure every architectural component has a corresponding build task.

---

## 2. The Four Engines Implementation Mapping

The plan implements the engines in dependency order (Physics → Interface → Optimization → Governance), matching the definitions in `workflows_and_modes.md` Section 2.

| Engine | Role (Spec) | Implementation Phase | Key Tasks |
| :--- | :--- | :--- | :--- |
| **Calculation Engine** | The Physics Layer (Deterministic) | **Phase 2 (Foundational)** | `T009` (Core Build)<br>`T017d-g` (Refactor & Domain Logic) |
| **LLM Orchestrator** | The Interface Layer (Translator) | **Phase 2.5 (Connectivity)** | `T036` (Orchestrator Base)<br>`T040` (Intent Recognition)<br>`T037` (State Hydration) |
| **Strategy Engine** | The Optimization Layer (Solver) | **Phase 4 (User Story 2)** | `T057` (Optimization Loops)<br>`T055` (Strategy Schemas) |
| **Advice Engine** | The Governance Layer (Regulator) | **Phase 5 (User Story 3)** | `T065` (Compliance Checking)<br>`T067` (BID Validation Rules) |

---

## 3. Core Advice Workflows (Mode Mapping)

Specific user journeys defined in `workflows_and_modes.md` Section 3 are mapped to User Stories.

### Mode 1: The "Fact Check"
* **Spec Flow:** `LLM` → `Calc` (Hydrate → Request Value → Explain).
* **Implementation:** **Phase 3 (User Story 1)**.
* **Traceability:**
    * `T047`: Fact Check Endpoint.
    * `T048`: Intent Recognition (Fact queries).
    * `T050`: Connect Calc Engine to Endpoint.

### Mode 3: The "Strategy Explorer"
* **Spec Flow:** `LLM` → `Strategy` → `Calc` → `Advice`.
* **Implementation:** **Phase 4 (User Story 2)**.
* **Traceability:**
    * `T056`: Scenario Comparison Endpoint.
    * `T057`: Strategy Engine Build.
    * `T061`: Comparison Narratives.

### Mode 6: The "Holistic Plan"
* **Spec Flow:** Full Stack (Cascade Optimization → Multi-Entity Projections → BID Check).
* **Implementation:** **Phase 5 (User Story 3)**.
* **Traceability:**
    * `T066`: Comprehensive Plan Endpoint.
    * `T068`: Multi-domain Optimization.
    * `T069`: Compliance Integration.

---

## 4. Operational Workflows

Backend and business logic modes defined in `workflows_and_modes.md` Section 4.

### Mode 7: The "Proactive Monitor"
* **Spec Flow:** New Rules → Strategy Scan → Compliance Check → Alert.
* **Implementation:** **Phase 6 (User Story 4)**.
* **Traceability:**
    * `T074`: Rule Monitoring System.
    * `T077`: Automated Change Detection.
    * `T084`: Bulk Scenario Re-evaluation.

### Mode 16: The "Collaborative Session"
* **Spec Flow:** Live Q&A → Real-time Calc Update → Warning Mode Advice.
* **Implementation:** **Phase 7 (User Story 5)**.
* **Traceability:**
    * `T087`: Optimistic UI / Sync.
    * `T089`: Real-time Scenario Updates.
    * `T092`: Immediate Compliance Warnings.

---

## 5. Interaction Model Alignment (MOD-*)

Mapping the architectural groupings from `interaction_architecture.md` to the plan.

| Interaction Model | Description | Plan Integration |
| :--- | :--- | :--- |
| **MOD-001** | **Conversational Insight**<br>(Fact Check, Education) | **Phase 3 & 8**<br>Implemented via US1 (Fact Check) and US6 (RAG/Education). |
| **MOD-002** | **Scenarios & Comparison**<br>(Sandbox, Collaboration) | **Phase 4**<br>Implemented via US2 (Scenario Management APIs). |
| **MOD-003** | **Strategy & Optimization**<br>(Solver Loops) | **Phase 4**<br>Implemented via US2 (Strategy Engine). |
| **MOD-004** | **Comprehensive Advice**<br>(Governance, BID) | **Phase 5**<br>Implemented via US3 (Advice Engine & SoA Generation). |
| **MOD-007** | **Reference/RAG**<br>(Source of Truth) | **Phase 8**<br>Implemented via US6 (Reference Material System `T080-T086`). |
| **MOD-009** | **Operational Monitoring**<br>(System Triggers) | **Phase 6**<br>Implemented via US4 (Health Monitoring). |

---

## 6. Key Technical Enablers

These technical decisions in the plan enable the architectural strictures defined in the specs.

### A. Tiered LLM Routing (Phase 2.5)
* **Enables:** The "Translator" role of the Orchestrator.
* **Mapping:**
    * **Router (Tier 1)** handles Intent Recognition for **all modes**.
    * **Narrator (Tier 2)** handles fluency for **Mode 1** and **Mode 24**.
    * **Thinker (Tier 3)** handles reasoning for **Mode 6** (Holistic Plan).
* **Tasks:** `T041c` - `T041f`.

### B. Shared Schemas (Phase 1 & 2.35)
* **Enables:** The seamless data flow between engines (e.g., `LLM` hydrating `CalculationState` for `Calc Engine`).
* **Mapping:** Ensures `CalculationState`, `Scenario`, and `AdviceOutcome` are consistent across Python (Backend) and TypeScript (Frontend).
* **Tasks:** `T002`, `T017d`.

### C. TraceLog (Phase 2)
* **Enables:** System introspection and audit.
* **Mapping:** Required for **Mode 26 (System Oracle)** and **Mode 11 (Bulk Auditor)** to function.
* **Tasks:** `T008`.