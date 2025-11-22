# Specification Reorganization: Frontend Separation

**Date**: November 21, 2025
**Action**: Separated frontend concerns from core engine architecture

## Summary of Changes

The original `001-four-engine-architecture/spec.md` contained a mix of:
- Core computational engine requirements (four engines, calculations, compliance)
- User interaction stories and experiences
- Brand-specific product requirements (Frankie's Finance, Veris Finance)

To improve focus and maintainability, the specification has been reorganized into three separate specs:

### 001-four-engine-architecture (Core Engine)
- **Focus**: Technical architecture of the four computational engines
- **Scope**: LLM Orchestrator, Calculation Engine, Strategy Engine, Advice Engine
- **Content**: System-level requirements, data entities, performance criteria, user stories (for engine capability illustration)
- **Approach**: User stories are retained to show engine capabilities, but with clear scope boundaries - this spec defines WHAT the engines do, not HOW users interact with them

### 002-web-frontend (User Interface)
- **Focus**: Web interface and user interaction patterns
- **Scope**: User experience, interface design, interaction models
- **Content**: All original user stories (consumer fact check, strategy exploration, adviser planning, etc.)
- **File**: `spec_input.md`
- **Purpose**: Define how users interact with the system regardless of brand

### 003-frankies-finance (Brand Products)
- **Focus**: Brand-specific user experiences and product differentiation
- **Scope**: Frankie's Finance consumer experience vs Veris Finance adviser experience
- **Content**: Brand-specific user journeys, interface customization, role-based features
- **File**: `spec_input.md`
- **Purpose**: Define how the same underlying engines present different experiences for different user types

## Content Migration Details

### Retained in 001 with Scope Clarification:
- All 6 User Stories (Consumer Fact Check, Strategy Exploration, Adviser Planning, System Monitoring, Collaborative Sessions, Educational Guidance) - kept to illustrate engine capabilities but with clear boundaries that this spec defines engine behavior, not UI implementation
- Engine-relevant functional requirements (user types for data access, collaborative sessions for concurrency)
- Performance-oriented success criteria (timing, scaling, availability requirements)
- UserProfile entity (for engine-level data access patterns)
- All edge cases (including user-focused ones that affect engine robustness)

### Moved to 002-web-frontend/spec_input.md:
- UI/UX implementation details and interaction patterns
- Brand-agnostic user interface requirements
- Front-end performance and usability metrics

### Moved to 003-frankies-finance/spec_input.md:
- Brand-specific user experiences and journeys
- Frankie's Finance vs Veris Finance differentiation
- Role-based interface customizations

### Removed from 001 and Moved to 003:
- Brand references ("Frankie's Finance", "Veris Finance")
- Brand-specific user experiences and role differentiation
- Consumer vs adviser interface requirements

### Retained in 001:
- Core engine architecture (four engines and their interactions)
- Calculation and compliance requirements
- Data entities (CalculationState, ProjectionTimeline, Scenario, Strategy, AdviceOutcome, TraceLog, ReferenceDocument)
- System performance and reliability criteria
- Technical edge cases (data quality, regulatory conflicts, system outages)

## Development Guidance

### For 002-web-frontend:
- Focus on universal user interaction patterns that work across brands
- Define interface components, user flows, and interaction models
- Consider accessibility, usability, and performance from user perspective
- Test user stories independently of specific brand implementations

### For 003-frankies-finance:
- Define brand-specific customizations and user experiences
- Specify how consumer vs adviser interfaces differ in presentation
- Ensure both brands leverage the same underlying calculation engines
- Maintain compliance and regulatory requirements across both brands

### For 001-four-engine-architecture:
- Focus on technical implementation of computational engines while using user stories to illustrate capabilities
- Ensure engines are brand-agnostic and reusable across different user interfaces
- Maintain separation between deterministic calculations and AI responses
- Provide APIs and interfaces that frontend specs can consume
- Use user stories to define engine behavior requirements, not UI implementation details

## Next Steps

1. **Review Dependencies**: Ensure the separated specs properly define interfaces between layers
2. **Update Plans**: Modify `master_plan.md` and `master_tasks.md` to reflect the new specification structure
3. **Branch Strategy**: Consider creating separate feature branches for `002-web-frontend` and `003-frankies-finance`
4. **Integration Testing**: Define how the three specs integrate together for end-to-end functionality

## Risk Mitigation

- **Consistency**: Ensure calculation results remain identical across brands
- **Compliance**: Maintain regulatory compliance requirements across all user experiences
- **Performance**: Monitor that frontend separation doesn't impact system performance
- **User Experience**: Validate that brand differentiation enhances rather than complicates user journeys
