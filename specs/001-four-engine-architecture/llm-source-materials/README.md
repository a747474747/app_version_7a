# LLM Source Materials Directory

This directory contains comprehensive internal reference materials used by developers when creating and maintaining LLM prompts.

## Important: Internal Use Only

**CRITICAL**: These source materials are **NEVER** sent to external LLMs. They are for internal reference only, providing developers with comprehensive context about:
- Australian financial system
- Financial advice process
- Regulatory environment
- Domain-specific knowledge

## Directory Structure

- **Root level** - Core system primers
  - `australian-financial-system.md` - Overview of financial institutions, products, tax system, investment structures
  - `financial-advice-process.md` - Stages of advice, adviser responsibilities, client communication, documentation
  - `regulatory-environment.md` - ASIC framework, BID requirements, licensing, consumer protection, privacy
  - `interaction-patterns.md` - User question types, educational delivery, risk communication, conversation flows

- **`domain-knowledge/`** - Domain-specific knowledge bases
  - `tax-regime.md` - Detailed tax rules and thresholds
  - `superannuation.md` - Super contribution strategies and rules
  - `property-investment.md` - Property investment considerations
  - `retirement-planning.md` - Retirement income strategies
  - `insurance.md` - Insurance product types and suitability

## Catalog Tracking

All source materials are tracked in `catalog.json` with the following metadata:
- `material_id`: Unique identifier
- `title`: Human-readable title
- `description`: Short description
- `category`: "system_primer", "domain_knowledge", "regulatory", or "process"
- `version`: Version string
- `file_path`: Relative path to source material file
- `purpose`: Detailed purpose (internal reference for prompt developers)

## How to Use Source Materials

1. **When creating prompts**: Reference these materials to ensure accurate understanding of:
   - Australian financial system concepts
   - Regulatory requirements
   - Industry terminology
   - Best practices

2. **When updating prompts**: Review relevant source materials to ensure prompts reflect current:
   - Regulatory requirements
   - Industry standards
   - Best practices

3. **Never send to LLMs**: These materials are comprehensive internal references. Extract only the specific information needed for prompts, not the entire documents.

## How to Maintain Source Materials

1. **Read the catalog file** (`catalog.json`) to understand what materials exist

2. **Update materials** when:
   - Regulatory requirements change
   - Industry standards evolve
   - New concepts need documentation
   - Errors are discovered

3. **Update the catalog** (`catalog.json`) when:
   - Creating new source materials
   - Updating existing materials (update `last_updated` and `version`)
   - Deprecating materials (set `status` to "deprecated")

4. **Version control**: Track versions in catalog.json and update `last_updated` when modifying

5. **Commit changes**: Commit catalog updates together with material file changes

## Purpose

These source materials provide developers with comprehensive domain knowledge to:
- Create accurate and compliant prompts
- Understand regulatory requirements
- Use correct terminology
- Follow best practices
- Ensure consistency across prompts

Without exposing sensitive internal knowledge to external LLMs.

## Related Documentation

- Prompt files: `/specs/001-four-engine-architecture/llm-prompts/` (actual prompts sent to LLMs)
- Workflows and modes: `specs/001-four-engine-architecture/design/workflows_and_modes.md`
- LLM Orchestrator contract: `specs/001-four-engine-architecture/contracts/llm-orchestrator.yaml`

