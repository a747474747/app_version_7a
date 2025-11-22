### 3. Document Topology & Task-Oriented Context

This project uses a **single canonical set of design documents**, plus **derived per-feature plans** and a **master task index** that the automation scripts use to feed context to AI agents.

#### 3.1 Canonical design files

There is exactly **one** canonical copy of each core design file:

- `models_overview.md`
- `workflows_and_modes.md`
- `calculation_engine_state_plan.md`
- `canonical_calc_engine_parameters.md`
- `functional_requirements_consolidated.md`
- `example_calculation.md` / other worked examples
- `master_plan.md` (high-level phases & milestones)
- `spec_guidance.md` (this file)

These files are the **single source of truth**. All feature-level plans and tasks are derived from them; they must never be forked or duplicated.

#### 3.2 Per-feature plan views

- Each **feature** (or engine sub-feature) gets its own plan file, e.g.  
  `plans/plan_calc_engine_pit.md`, `plans/plan_llm_orchestrator_modes.md`, etc.
- These plans are **generated or updated by a script**, not hand-written from scratch.
- A feature plan is a *view* over the canonical design files:
  - It references specific sections / line ranges in the master specs.
  - It may add local implementation notes, but must not redefine global rules.

The source of truth for behaviour remains the canonical design docs; feature plans are curated slices that make it easier for agents to work in bounded context.

#### 3.3 master_tasks.md as the task index

- There is exactly one `master_tasks.md`.
- Each task in `master_tasks.md` includes metadata that tells an agent **where to look for context**, for example:

  - `feature_id`
  - `phase_id`
  - `engine` (calc / strategy / advice / llm / frontend / backend)
  - `spec_refs` – list of `(file, line_start, line_end)` tuples
  - `plan_refs` – list of `(file, line_start, line_end)` tuples
  - `status` – `todo | in_progress | done | blocked`

- `master_tasks.md` is the **main entry point** for automated work: scripts and agents always start from a task row, never from free-form browsing of the repo.

#### 3.4 Scripts: creating tasks from specs

There will be a **task-generation script**, e.g. `scripts/generate_tasks_from_specs.py`, which:

1. Reads the canonical design files (specs, plans, models, workflows).
2. Identifies logical work units (features, sub-features, CALs, endpoints, screens, etc.).
3. Locates the relevant sections in those files (by heading and/or line numbers).
4. Writes/updates entries in `master_tasks.md`, including:
   - task id and title
   - engine / phase / feature tags
   - `spec_refs` + `plan_refs` with concrete file + line ranges

This script is responsible for keeping `master_tasks.md` in sync with the evolving design documents.

#### 3.5 Scripts: feeding context to AI agents

There will be a **task-runner / context-builder script**, e.g. `scripts/hydrate_task_context.py`, which:

1. Reads `master_tasks.md` to:
   - Find the **next** `todo` task for a given phase/engine, or
   - Load a specific task by `task_id`.
2. For that task, reads the referenced sections from:
   - Canonical design files (`spec_refs`)
   - Feature plan views (`plan_refs`)
3. Assembles a **compact context bundle** for the agent, e.g.:

   - A short task summary (from `master_tasks.md`)
   - The exact snippets from the relevant specs & plans
   - Optional links to example calculations or tests

4. Emits this bundle in a format usable in prompts (e.g. a `.md` block or JSON blob) so that Cursor/LLM agents always get:
   - Just enough context to implement the task correctly
   - Without loading the entire master spec/plan into the context window.

#### 3.6 Agent workflow (high-level)

- Human/dev chooses a task (or phase/engine).
- `hydrate_task_context.py`:
  - Looks up the task in `master_tasks.md`
  - Reads only the referenced lines from the relevant files
  - Produces a “task context” payload
- The AI agent is invoked with:
  - The task description
  - The task context payload
  - The relevant coding constraints (constitution, style, etc.)
- The agent:
  - Modifies only the intended files (as per task)
  - Updates status/comments back into `master_tasks.md` or a per-feature checklist.

This pattern preserves **spec-driven development** while keeping per-task context small enough for LLMs, and it provides a clear path to fully automating task selection and context assembly later.
