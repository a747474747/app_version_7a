# Feature Specification: Four-Engine System Architecture

**Feature Branch**: `001-four-engine-architecture`
**Created**: November 21, 2025
**Status**: Draft
**Input**: User description: "create the spec from this:@design/interaction_architecture.md"

## Scope and Focus

### What This Specification Covers
This specification defines the **core computational architecture** of the four-engine system that powers financial advice and calculations. It focuses on:

- **Engine Design**: Technical implementation of the four computational engines (LLM Orchestrator, Calculation Engine, Strategy Engine, Advice Engine)
- **Engine Interactions**: How the engines work together to process queries and generate results
- **Data Processing**: How financial data flows through the system and is transformed
- **Compliance & Quality**: Regulatory compliance checking, audit trails, and calculation accuracy
- **Performance & Reliability**: System performance requirements and operational constraints

### What This Specification Does NOT Cover
This specification intentionally does NOT define:

- **User Interface**: Front-end web interfaces, mobile apps, or user interaction patterns
- **Brand Experiences**: Frankie's Finance consumer experience or Veris Finance adviser interfaces
- **User Roles & Permissions**: Consumer vs adviser access controls or user management
- **Product Features**: Brand-specific features, marketing, or product positioning
- **Deployment**: Hosting, scaling, or operational deployment concerns

**Note**: User stories are included below to illustrate how the engines are used and what capabilities they provide, but the implementation details of user interfaces are specified separately in `002-web-frontend` and brand experiences in `003-frankies-finance`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consumer Fact Check (Priority: P1)

As a consumer using Frankie's Finance, I want to ask factual questions about my financial situation (like "What's my current net wealth?" or "How much tax will I pay?") and receive accurate, deterministic answers grounded in verified calculations, so I can understand my financial position clearly.

**Why this priority**: This represents the most fundamental interaction - consumers need reliable answers to basic financial questions. It's the entry point for all financial education and decision-making.

**Independent Test**: Can be fully tested by asking factual questions and verifying answers match expected calculations based on provided financial data.

**Acceptance Scenarios**:

1. **Given** a consumer provides their financial data, **When** they ask "What is my current net wealth?", **Then** the system returns a specific dollar amount calculated from their assets minus liabilities
2. **Given** a consumer provides income details, **When** they ask "How much tax will I pay this year?", **Then** the system returns a tax calculation based on current tax rules and their specific situation
3. **Given** a consumer asks a question requiring calculation, **When** the system processes the request, **Then** it provides the answer with clear explanation of how the number was derived

---

### User Story 2 - Consumer Strategy Exploration (Priority: P1)

As a consumer using Frankie's Finance, I want to explore "what-if" scenarios (like "What if I paid off my debt faster?" or "How would extra super contributions help?") to understand different financial strategies, so I can make informed decisions about my money.

**Why this priority**: Strategy exploration enables consumers to understand the impact of different financial choices, which is core to financial planning and education.

**Independent Test**: Can be fully tested by comparing baseline scenarios against alternative strategies and verifying the projected outcomes are mathematically consistent.

**Acceptance Scenarios**:

1. **Given** a consumer's baseline financial situation, **When** they explore a strategy like "pay debt faster", **Then** the system shows side-by-side comparison of baseline vs accelerated debt repayment scenarios
2. **Given** multiple strategy options, **When** the consumer compares them, **Then** the system displays clear metrics showing the impact on key financial outcomes (wealth, cashflow, buffers)
3. **Given** a strategy exploration, **When** the system presents results, **Then** it includes educational explanations of why one strategy might perform better than another

---

### User Story 3 - Adviser Comprehensive Planning (Priority: P1)

As a financial adviser using Veris Finance, I want to create comprehensive financial plans for clients that include strategy optimization, compliance checking, and regulatory governance, so I can provide professional advice that meets legal standards.

**Why this priority**: This enables the core business value of providing compliant financial advice, which is the primary use case for professional advisers.

**Independent Test**: Can be fully tested by running a complete planning workflow and verifying all governance checks pass for approved strategies.

**Acceptance Scenarios**:

1. **Given** a client's complete financial data, **When** I request a holistic plan, **Then** the system optimizes across debt reduction, superannuation, and investment strategies simultaneously
2. **Given** an optimized strategy, **When** the system applies compliance checks, **Then** it validates against Best Interest Duty requirements and regulatory guidelines
3. **Given** a compliant strategy, **When** I proceed to implementation, **Then** the system generates structured action plans and milestone tracking

---

### User Story 4 - System Health Monitoring (Priority: P2)

As a system administrator or compliance officer, I want to monitor the system's ongoing performance and compliance with changing regulations, so I can ensure the advice platform remains accurate and legally compliant over time.

**Why this priority**: This supports the operational reliability and regulatory compliance of the platform, which is essential for business continuity.

**Independent Test**: Can be fully tested by triggering rule changes and verifying the system correctly identifies impacted clients and re-evaluates their strategies.

**Acceptance Scenarios**:

1. **Given** a change in tax legislation, **When** the system detects the change, **Then** it automatically re-evaluates affected client strategies and alerts advisers
2. **Given** periodic health checks, **When** the system runs compliance audits, **Then** it identifies any strategies that no longer meet regulatory requirements
3. **Given** system monitoring, **When** performance issues occur, **Then** the system provides diagnostic information to help resolve problems

---

### User Story 5 - Collaborative Client Sessions (Priority: P2)

As an adviser working with a client in a live session, I want to explore scenarios together in real-time with the system providing calculations and compliance guidance in the background, so we can have productive planning conversations.

**Why this priority**: Live collaboration enhances the adviser-client relationship and enables more effective planning sessions.

**Independent Test**: Can be fully tested by simulating a live session with scenario changes and verifying real-time updates and compliance warnings.

**Acceptance Scenarios**:

1. **Given** a live client session, **When** we modify scenarios together, **Then** the system updates calculations in real-time without interrupting the conversation
2. **Given** strategy changes during a session, **When** compliance issues arise, **Then** the system provides immediate warnings to the adviser while maintaining session flow
3. **Given** a completed session, **When** the adviser requests it, **Then** the system generates structured meeting notes and action items

---

### User Story 6 - Educational Guidance (Priority: P3)

As a consumer or adviser seeking general financial education, I want to ask questions about financial concepts and receive accurate, educational responses based on authoritative sources, so I can build my financial knowledge.

**Why this priority**: Financial education supports all other interactions and helps users make better decisions.

**Independent Test**: Can be fully tested by asking educational questions and verifying responses are based on authoritative financial sources.

**Acceptance Scenarios**:

1. **Given** a general financial question, **When** I ask about concepts like "What is a franking credit?", **Then** the system provides clear educational explanations
2. **Given** an educational query, **When** the system responds, **Then** it avoids giving personal advice and focuses on general information
3. **Given** a user shows interest in specific calculations, **When** they ask educational questions, **Then** the system can transition smoothly to providing personalized calculations

---

## Edge Cases

- What happens when financial data is incomplete or inconsistent?
- How does system handle extremely complex financial situations with multiple entities?
- What occurs when regulatory rules conflict with optimized strategies?
- How does system behave when calculation engines encounter mathematical impossibilities?
- What happens during system outages or when external data sources are unavailable?
- How does system handle users with limited financial literacy? (engine robustness requirement)
- What occurs when multiple users attempt to modify the same scenario simultaneously? (concurrency requirement)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide four distinct computational engines (LLM Orchestrator, Calculation Engine, Strategy Engine, Advice Engine) that work together to process financial queries and generate advice
- **FR-002**: System MUST support 12 interaction models that define how engines combine for different use cases (from conversational insight to comprehensive planning)
- **FR-003**: System MUST implement 26 operational modes representing specific user journeys and workflows
- **FR-004**: System MUST maintain separation between probabilistic AI responses and deterministic mathematical calculations
- **FR-005**: System MUST enforce regulatory compliance checks including Best Interest Duty (BID) requirements
- **FR-006**: System MUST provide real-time calculation capabilities for interactive scenario exploration
- **FR-007**: System MUST maintain authoritative reference materials for educational responses and rule validation
- **FR-008**: System MUST support multiple user types (consumers, advisers, compliance officers, partners) with appropriate data access patterns (engine-level requirement)
- **FR-009**: System MUST generate comprehensive audit trails and traceability for all calculations and advice decisions
- **FR-010**: System MUST handle data quality assessment and progressive onboarding for incomplete financial information
- **FR-011**: System MUST provide privacy and safety filtering for all inputs and AI-generated responses
- **FR-012**: System MUST support background monitoring and proactive alerts for regulatory changes or client situation changes
- **FR-013**: System MUST enable collaborative sessions between advisers and clients with real-time scenario updates (engine concurrency requirement)
- **FR-014**: System MUST provide implementation orchestration capabilities to turn strategies into actionable steps
- **FR-015**: System MUST maintain comprehensive testing and QA capabilities across all engines and modes
- **FR-016**: System MUST support an automated "Logic Factory" workflow where calculation logic is hypothesized by LLMs, audited against provided reference text, and compiled into executable Python code

### Key Entities *(include if feature involves data)*

- **CalculationState**: Represents a user's complete financial position at a point in time, including assets, liabilities, income, expenses, and demographic information
- **ProjectionTimeline**: Time-series data showing how financial metrics evolve over future periods based on different scenarios
- **Scenario**: A specific set of financial assumptions and strategy choices that produce different projected outcomes
- **Strategy**: A reusable optimization template that defines tunable parameters and constraints for achieving financial goals
- **AdviceOutcome**: The result of regulatory compliance checking, including approval status, reasons, and referenced rules
- **TraceLog**: Detailed audit trail of all calculation steps, rule applications, and decision points
- **ReferenceDocument**: Authoritative source materials (legislation, rulings, guidelines) with versioning and metadata
- **UserProfile**: Information about system users including their role (consumer/adviser/compliance) and data access permissions (engine-level entity)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Consumers can receive accurate answers to factual financial questions within 5 seconds of asking (engine performance requirement)
- **SC-002**: System processes complex strategy optimizations involving multiple financial domains within 30 seconds
- **SC-003**: 95% of generated advice passes automated regulatory compliance checks without human intervention
- **SC-004**: Advisers can explore and compare 5 different financial scenarios simultaneously without performance degradation (engine scaling requirement)
- **SC-005**: System maintains 99.9% availability for critical financial calculations during business hours
- **SC-006**: All calculation results include complete audit trails that can be independently verified
- **SC-007**: System correctly identifies and alerts on 100% of regulatory changes that impact existing strategies
- **SC-008**: Collaborative sessions support real-time updates for up to 10 concurrent scenario modifications (engine concurrency requirement)
- **SC-009**: Educational responses are grounded in authoritative sources with proper citations in 100% of cases (content quality requirement)
