# Veris Finance Implementation Plan

**Branch**: `007-veris-finance` | **Date**: 2025-01-27 | **Spec**: `specs/007-veris-finance/spec_007_veris_finance.md`  
**Status**: ✅ **Phase 0 Complete**

## Summary

Veris Finance is a professional adviser console with calm, data-centric UI. Provides LLM-powered chat interface, client scenario management, compliant forecasting, comparative analysis, and automated documentation generation.

**Technical Approach**: TypeScript/Next.js App Router web application (desktop-first) with TanStack Query for API caching, Tamagui for shared design tokens, natural language interaction via LLM Orchestrator, financial calculations via Compute Engine, compliance validation via Advice Engine. Sentry for error tracking.

## Technical Context

**Language/Version**: TypeScript/Next.js

**Primary Dependencies**:
- **Framework**: Next.js App Router
- **UI Library**: Tamagui for shared design tokens (mobile + web) - professional, calm design system (graphite, silver, blue accent)
- **Charts**: Professional charting library (e.g., Recharts, D3)
- **State Management**: Zustand (lightweight state management)
- **API Caching**: TanStack Query (React Query) for API caching and synchronization
- **Error Tracking**: Sentry (free tier) for error monitoring
- **Testing**: Jest, React Testing Library

## API Integration

### Backend Service Integration

- **LLM Orchestrator**: 
  - Natural language queries via `POST /llm/chat` and `POST /llm/parse`
  - Receives professional conversational responses with tool calls and citations

- **Compute Engine**: 
  - Structured calculation requests via `POST /run` and `POST /run-batch` (transformed by LLM Orchestrator)
  - Results via `GET /facts`
  - Explanations via `GET /explain/{fact_id}`

- **Advice Engine**: 
  - Compliance checking via `POST /advice/check`
  - Compliance requirements via `GET /advice/requirements`
  - Receives detailed compliance information for professional use

- **References & Research Engine**: 
  - Indirect integration via LLM Orchestrator for citation generation

## Module Dependencies

### Depends On

- **LLM Orchestrator** (`005-llm-orchestrator`): Natural language processing of adviser queries
- **Compute Engine** (`002-compute-engine`): Executing financial calculations and scenario modelling
- **Advice Engine** (`004-advice-engine`): Validating compliance and generating compliance checklists

## Technical Implementation Details

### Professional Interface Design

- **Design System**: Cool neutrals (graphite, silver, blue accent), crisp typography
- **Data-Centric UI**: Optimized for visualizing strategies, forecasts, comparisons
- **Charts**: Professional line charts, bar graphs, comparative dashboards
- **Layout**: Clean two-column layouts for client summaries
- **Audit Log**: Always available, transparent record of all advice logic

### LLM Chat Interface

- **Natural Language**: Understands natural adviser language
- **Structured Replies**: Format responses with clickable commands
- **Context Maintenance**: Conversation context for client scenarios
- **Professional Tone**: Maintain professional tone and accuracy

### Client Management

- **Client Records**: Create and manage client records with demographics, goals, financial data
- **Input Methods**: Natural language input or structured forms
- **Multiple Clients**: Support multiple clients per adviser
- **Data Import**: Import from external sources or enter manually

### Scenario Modelling

- **Multiple Scenarios**: Create and manage multiple scenarios per client
- **Calculation Execution**: Via Compute Engine
- **Forecast Presentation**: Professional line charts, bar graphs, scenario tabs
- **Sensitivity Analysis**: Vary assumptions and see how outcomes change
- **Expandable Tiles**: Show assumptions, inputs, and results

### Strategy Comparison

- **Side-by-Side**: Compare multiple strategies or products
- **Visual Differentiation**: Clear visual differentiation between strategies
- **Best-Interests Evidence**: Provide comparison data demonstrating best-interests duty

### Compliance and Validation

- **Compliance Checking**: Via Advice Engine
- **Status Display**: Show compliance status, warnings, required actions
- **Prevention**: Prevent document generation when compliance validation fails
- **Documentation Integration**: Incorporate compliance results into generated documents

### Documentation Generation

- **SOA/ROA Generation**: Generate Statement of Advice and Record of Advice automatically
- **Traceable Explanations**: Include links to authoritative references, rule versions, calculation assumptions
- **Export Formats**: Suitable for client presentation and regulatory submission
- **Consistency**: Ensure consistency between calculations, compliance results, and documentation

### Audit Trail

- **Transparent Log**: Show all advice logic, calculations, compliance checks, changes
- **Explanation Access**: Access to explanation capabilities for any calculation result
- **Export**: Export audit trails suitable for regulatory review
- **Time-Travel**: Support time-travel queries for historical advice review

## Implementation Phases

### Phase 1: Professional Interface (Weeks 1-2)

**Tasks**:
1. **UI Design**
   - Design professional calm UI (cool neutrals, crisp typography)
   - Implement minimal chrome, clear hierarchy
   - Implement data-centric visualizations (charts, graphs)
   - Implement audit log always available
   - Implement two-column layouts for client summaries

**Deliverables**:
- Professional interface functional
- Data-centric UI operational

### Phase 2: LLM Chat Interface (Week 3)

**Tasks**:
1. **Chat Integration**
   - Integrate with LLM Orchestrator (`POST /llm/chat`, `POST /llm/parse`)
   - Implement natural language input for client data
   - Implement structured replies and clickable commands
   - Implement conversation context for client scenarios
   - Ensure collected comprehensive client PII is used by LLM Orchestrator for enhanced filtering (known client identifiers enable highly effective filtering)
   - Reference: `specs/001-master-spec/spec.md` FR-076

**Deliverables**:
- LLM chat interface working
- Natural language input functional
- Enhanced PII filtering operational (using known client PII)

### Phase 3: Client Management (Week 4)

**Tasks**:
1. **Client Records**
   - Implement client record creation and management
   - Implement natural language and structured input
   - Implement multiple clients per adviser support
   - Implement client data import

2. **Client PII Collection and Privacy Explanation**
   - Collect comprehensive client PII during client setup (name, DOB, address, contact details, account numbers, TFN, etc.)
   - Provide clear labels indicating what information is being collected and why
   - Store collected client PII profile for enhanced filtering (name, DOB, address, contact details, account numbers, TFN, collection timestamp, consent acknowledgment)
   - Display detailed privacy explanation after client setup completion covering:
     - How client PII is handled
     - How the filtering process works
     - How it ensures client identifying information is not sent to external LLMs
     - How this complies with Australian Privacy Act 1988 and professional obligations
   - Provide access to privacy policy (same as Frankie's Finance) through clear link or button
   - Ensure privacy explanation is displayed before processing any client queries
   - Handle cases where advisers enter incomplete client information (still display privacy explanation, filter whatever PII is available)
   - Reference: `specs/001-master-spec/spec.md` User Story 5, FR-072, FR-073, FR-074, FR-075, FR-076, FR-078

3. **Professional Privacy Language**
   - Provide clear, professional language that advisers can use to explain privacy protections to clients
   - Make privacy explanation language accessible for client communication
   - Reference: `specs/001-master-spec/spec.md` FR-077

4. **Privacy Settings Access**
   - Implement privacy settings screen accessible at any time
   - Allow advisers to review what client information has been collected
   - Allow advisers to update privacy preferences
   - Reference: `specs/001-master-spec/spec.md` FR-079

**Deliverables**:
- Client management functional
- Multiple clients supported
- Client PII collection functional with clear labels
- Detailed privacy explanation displayed before first client query
- Privacy policy accessible within 2 clicks/taps
- Professional privacy language available for client communication
- Privacy settings accessible at any time
- Client PII profile stored for enhanced filtering (integrated with LLM Orchestrator)

### Phase 4: Scenario Modelling and Forecasting (Weeks 5-6)

**Tasks**:
1. **Scenario Features**
   - Integrate with Compute Engine (`POST /run`, `POST /run-batch`, `GET /facts`)
   - Implement scenario creation and management
   - Implement professional forecast visualizations (line charts, bar graphs)
   - Implement sensitivity analysis and stress-testing
   - Implement expandable tiles showing assumptions and results

**Deliverables**:
- Scenario modelling working
- Forecast visualizations functional

### Phase 5: Strategy Comparison (Week 7)

**Tasks**:
1. **Comparison Features**
   - Implement side-by-side strategy comparison
   - Implement key difference highlighting
   - Implement evidence-based recommendation support

**Deliverables**:
- Strategy comparison functional

### Phase 6: Compliance and Validation (Week 8)

**Tasks**:
1. **Compliance Integration**
   - Integrate with Advice Engine (`POST /advice/check`, `GET /advice/requirements`)
   - Implement compliance validation display
   - Implement compliance status, warnings, and required actions
   - Prevent non-compliant advice document generation

**Deliverables**:
- Compliance validation integrated
- Compliance status display working

### Phase 7: Documentation Generation (Week 9)

**Tasks**:
1. **Document Generation**
   - Implement Statement of Advice (SOA) generation
   - Implement Record of Advice (ROA) generation
   - Include calculations, compliance results, and traceable explanations
   - Export documents for client presentation and regulatory submission
   - Implement client-side PDF generation using browser print-to-PDF with print-optimized CSS stylesheets
   - Implement print-ready CSS for SOA/ROA templates
   - Implement evidence pack export (JSON and PDF formats) with version information, timestamps, and complete provenance chains
   - Reference: `specs/001-master-spec/spec.md` CL-033

**Deliverables**:
- Document generation working
- Export functionality functional
- Client-side PDF generation operational with print-ready CSS
- Evidence pack export functional (JSON and PDF formats)

### Phase 8: Audit Trail and Explainability (Week 10)

**Tasks**:
1. **Audit Features**
   - Implement transparent audit log
   - Integrate with Compute Engine `/explain/{fact_id}` endpoints
   - Implement audit trail export for regulatory review
   - Implement time-travel queries for historical advice

**Deliverables**:
- Audit trail complete
- Explainability functional

### Phase 9: Testing (Ongoing)

**Tasks**:
1. **Test Implementation**
   - Unit tests for UI components
   - Integration tests with backend modules
   - End-to-end tests (Playwright)
   - **Test Forecasts**: All calculations tested via Veris Finance test forecasts

**Deliverables**:
- Test coverage > 80%
- All calculations validated via Veris Finance test forecasts

