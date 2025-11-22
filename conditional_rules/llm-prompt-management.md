# LLM Prompt Management Rules

## Location Requirements
When creating LLM prompts and context primers for API calls to external LLMs:

- **ALL prompt files MUST be placed in the `/specs/001-four-engine-architecture/llm-prompts/` folder**
- Use appropriate subfolders to organize prompts by function:
  - `/specs/001-four-engine-architecture/llm-prompts/core-orchestrator/` - Core LLM Orchestrator function prompts (intent recognition, state hydration, strategy nomination, narrative generation)
  - `/specs/001-four-engine-architecture/llm-prompts/mode-prompts/` - All 26 mode-specific prompts aligned with workflows_and_modes.md
  - `/specs/001-four-engine-architecture/llm-prompts/shared-utilities/` - Cross-cutting prompt utilities (privacy, RAG, error handling, conversation context)

## Source Materials Requirements
Internal knowledge base materials for prompt development (NEVER sent to external LLMs):

- **ALL source material files MUST be placed in the `/specs/001-four-engine-architecture/llm-source-materials/` folder**
- Use appropriate subfolders:
  - `/specs/001-four-engine-architecture/llm-source-materials/` - Core system primers (Australian financial system, advice process, regulatory environment, interaction patterns)
  - `/specs/001-four-engine-architecture/llm-source-materials/domain-knowledge/` - Domain-specific knowledge bases (tax, superannuation, property, retirement, insurance)

## Separation Principle
**CRITICAL**: Do not write inside a script the text that will be passed to an LLM - it should always be called by the script from a separate file.

- Scripts must load prompts from files, never embed prompt text directly
- Each unique primer and prompt must have its own file
- Prompts must be in a format suitable for LLMs (markdown with clear sections)
- Source materials are for internal reference only (used by developers to create prompts, never sent to external LLMs)

## Tracking File Requirements
Each prompt file creation MUST be accompanied by an entry in the tracking file:

**Location**: `/specs/001-four-engine-architecture/llm-prompts/catalog.json`

**Entry Format** (JSON):
```json
{
  "prompt_id": "mode-01-fact-check",
  "title": "Mode 1: Fact Check Prompt",
  "description": "Handles factual queries about current financial state",
  "mode_id": 1,
  "category": "mode_prompt",
  "created_date": "2025-11-21",
  "created_timezone": "Australia/Brisbane",
  "last_updated": "2025-11-21",
  "version": "1.0",
  "file_path": "mode-prompts/mode-01-fact-check.md",
  "related_files": [
    "001-four-engine-architecture/design/workflows_and_modes.md"
  ]
}
```

**Required Fields**:
- `prompt_id`: Unique identifier (e.g., "mode-01-fact-check", "intent-recognition")
- `title`: Human-readable title
- `description`: Short description (max 150 characters)
- `mode_id`: Associated mode number (1-26) or null for core/shared prompts
- `category`: One of ["core_orchestrator", "mode_prompt", "shared_utility"]
- `created_date`: ISO format (YYYY-MM-DD)
- `created_timezone`: "Australia/Brisbane" (UTC+10)
- `last_updated`: ISO format (YYYY-MM-DD)
- `version`: Version string (e.g., "1.0")
- `file_path`: Relative path from `/specs/001-four-engine-architecture/llm-prompts/` folder
- `related_files`: Array of related spec/documentation files (can be empty array)

## Source Materials Tracking
Each source material file creation MUST be accompanied by an entry in the tracking file:

**Location**: `/specs/001-four-engine-architecture/llm-source-materials/catalog.json`

**Entry Format** (JSON):
```json
{
  "material_id": "australian-financial-system",
  "title": "Australian Financial System Primer",
  "description": "Overview of Australian financial institutions and products",
  "category": "system_primer",
  "created_date": "2025-11-21",
  "created_timezone": "Australia/Brisbane",
  "last_updated": "2025-11-21",
  "version": "1.0",
  "file_path": "australian-financial-system.md",
  "purpose": "Internal reference for developers creating prompts. Provides comprehensive context about Australian financial system without exposing sensitive knowledge to external LLMs."
}
```

**Required Fields**:
- `material_id`: Unique identifier
- `title`: Human-readable title
- `description`: Short description (max 150 characters)
- `category`: One of ["system_primer", "domain_knowledge", "regulatory", "process"]
- `created_date`: ISO format (YYYY-MM-DD)
- `created_timezone`: "Australia/Brisbane" (UTC+10)
- `last_updated`: ISO format (YYYY-MM-DD)
- `version`: Version string (e.g., "1.0")
- `file_path`: Relative path from `/specs/001-four-engine-architecture/llm-source-materials/` folder
- `purpose`: Detailed purpose (internal reference for prompt developers)

## Process Requirements
1. **Read the catalog file** (`/specs/001-four-engine-architecture/llm-prompts/catalog.json` or `/specs/001-four-engine-architecture/llm-source-materials/catalog.json`) to understand what prompts/materials already exist and avoid duplication
2. **Create the prompt/material file first** in the appropriate subfolder
3. **Update the catalog file** immediately after file creation
4. **Validate the catalog entry** matches the actual file location and content
5. **Ensure prompts align with mode IDs** from `specs/001-four-engine-architecture/design/workflows_and_modes.md` (modes 1-26)
6. **Commit both files together** in the same git commit

## Validation Rules
- No prompt text may exist in Python scripts - all prompts must be in separate files
- Every prompt file in `/specs/001-four-engine-architecture/llm-prompts/` must have a corresponding catalog entry
- Every source material file in `/specs/001-four-engine-architecture/llm-source-materials/` must have a corresponding catalog entry
- Catalog files must be valid JSON with no duplicate prompt_id/material_id entries
- All `related_files` paths must be valid relative paths from `/specs` folder
- Prompt file paths in catalog must match actual file locations
- Mode IDs must correspond to modes defined in workflows_and_modes.md (1-26)
- Source materials are NEVER sent to external LLMs - they are internal reference only
