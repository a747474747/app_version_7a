# LLM Prompts Directory

This directory contains all LLM prompts and context primers used for API calls to external LLMs.

## Directory Structure

- **`core-orchestrator/`** - Core LLM Orchestrator function prompts
  - `intent-recognition.md` - Intent recognition and mode selection
  - `state-hydration.md` - Converting natural language to structured state
  - `strategy-nomination.md` - Strategy suggestion and nomination
  - `narrative-generation.md` - Generating human-readable narratives

- **`mode-prompts/`** - Mode-specific prompts aligned with workflows_and_modes.md
  - `mode-01-fact-check.md` through `mode-26-system-oracle.md`
  - Each mode has its own prompt file following the naming pattern `mode-XX-[mode-name].md`

- **`shared-utilities/`** - Cross-cutting prompt utilities
  - `privacy-filter.md` - PII filtering and redaction
  - `rag-retrieval.md` - Reference retrieval and citation
  - `error-handling.md` - Error handling and user communication
  - `conversation-context.md` - Multi-turn conversation management

## Catalog Tracking

All prompts are tracked in `catalog.json` with the following metadata:
- `prompt_id`: Unique identifier
- `title`: Human-readable title
- `description`: Short description
- `mode_id`: Associated mode number (1-26) or null for core/shared prompts
- `category`: "core_orchestrator", "mode_prompt", or "shared_utility"
- `version`: Version string
- `file_path`: Relative path to prompt file
- `related_files`: Array of related specification files

## How to Create New Prompts

1. **Read the catalog file** (`catalog.json`) to understand what prompts already exist and avoid duplication

2. **Create the prompt file** in the appropriate subfolder:
   - Core orchestrator functions → `core-orchestrator/`
   - Mode-specific prompts → `mode-prompts/`
   - Shared utilities → `shared-utilities/`

3. **Follow the prompt file template**:
   - Include prompt ID, category, mode ID (if applicable), version, and last updated date
   - Structure with sections: Primary Prompt, Context Primers, Error Handling, Result Formatting

4. **Update the catalog** (`catalog.json`) immediately after file creation:
   - Add entry with all required fields
   - Link to related specification files (especially `workflows_and_modes.md`)

5. **Validate the catalog entry** matches the actual file location and content

6. **Commit both files together** in the same git commit

## How to Reference Prompts in Scripts

**CRITICAL**: Scripts must load prompts from files, never embed prompt text directly.

Example pattern:
```python
import json
from pathlib import Path

def load_prompt(prompt_id: str) -> str:
    """Load prompt text from file."""
    catalog_path = Path("specs/001-four-engine-architecture/llm-prompts/catalog.json")
    with open(catalog_path) as f:
        catalog = json.load(f)
    
    prompt_entry = next(p for p in catalog if p["prompt_id"] == prompt_id)
    prompt_path = Path("specs/001-four-engine-architecture/llm-prompts") / prompt_entry["file_path"]
    
    with open(prompt_path) as f:
        return f.read()
```

## Alignment with Modes

All mode prompts must align with the 26 operational modes defined in:
- `specs/001-four-engine-architecture/design/workflows_and_modes.md`

Each mode prompt file should reference the corresponding mode description and flow from that document.

## Best Practices for Prompt Design

1. **Separation**: Never embed prompt text in scripts - always load from files
2. **Reusability**: Create specific files for each unique primer and prompt
3. **Versioning**: Track versions in catalog.json and update `last_updated` when modifying
4. **Documentation**: Include clear descriptions of what each prompt does
5. **Testing**: Test prompts independently before integrating into scripts
6. **Consistency**: Follow the established template structure for all prompts

## Related Documentation

- Source materials: `/specs/001-four-engine-architecture/llm-source-materials/` (internal reference only, never sent to LLMs)
- Workflows and modes: `specs/001-four-engine-architecture/design/workflows_and_modes.md`
- LLM Orchestrator contract: `specs/001-four-engine-architecture/contracts/llm-orchestrator.yaml`

