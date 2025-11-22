# Feature Specification: Frankie's Finance & Veris Finance Brand Experiences

**Feature Branch**: `003-frankies-finance`
**Created**: November 21, 2025
**Status**: Draft
**Input**: Extracted brand-specific content from 001-four-engine-architecture spec to separate consumer and adviser product experiences

## User Scenarios & Testing *(mandatory)*

### Frankie's Finance Consumer Stories

#### Consumer Fact Check Experience

As a consumer using Frankie's Finance, I want to ask factual questions about my financial situation (like "What's my current net wealth?" or "How much tax will I pay?") and receive accurate, deterministic answers grounded in verified calculations, so I can understand my financial position clearly.

**Acceptance Scenarios**:

1. **Given** a consumer provides their financial data, **When** they ask "What is my current net wealth?", **Then** the system returns a specific dollar amount calculated from their assets minus liabilities
2. **Given** a consumer provides income details, **When** they ask "How much tax will I pay this year?", **Then** the system returns a tax calculation based on current tax rules and their specific situation
3. **Given** a consumer asks a question requiring calculation, **When** the system processes the request, **Then** it provides the answer with clear explanation of how the number was derived

#### Consumer Strategy Exploration Experience

As a consumer using Frankie's Finance, I want to explore "what-if" scenarios (like "What if I paid off my debt faster?" or "How would extra super contributions help?") to understand different financial strategies, so I can make informed decisions about my money.

**Acceptance Scenarios**:

1. **Given** a consumer's baseline financial situation, **When** they explore a strategy like "pay debt faster", **Then** the system shows side-by-side comparison of baseline vs accelerated debt repayment scenarios
2. **Given** multiple strategy options, **When** the consumer compares them, **Then** the system displays clear metrics showing the impact on key financial outcomes (wealth, cashflow, buffers)
3. **Given** a strategy exploration, **When** the system presents results, **Then** it includes educational explanations of why one strategy might perform better than another

#### Consumer Educational Experience

As a consumer seeking general financial education through Frankie's Finance, I want to ask questions about financial concepts and receive accurate, educational responses based on authoritative sources, so I can build my financial knowledge.

**Acceptance Scenarios**:

1. **Given** a general financial question, **When** I ask about concepts like "What is a franking credit?", **Then** the system provides clear educational explanations
2. **Given** an educational query, **When** the system responds, **Then** it avoids giving personal advice and focuses on general information
3. **Given** a user shows interest in specific calculations, **When** they ask educational questions, **Then** the system can transition smoothly to providing personalized calculations

---

### Veris Finance Adviser Stories

#### Adviser Comprehensive Planning Experience

As a financial adviser using Veris Finance, I want to create comprehensive financial plans for clients that include strategy optimization, compliance checking, and regulatory governance, so I can provide professional advice that meets legal standards.

**Acceptance Scenarios**:

1. **Given** a client's complete financial data, **When** I request a holistic plan, **Then** the system optimizes across debt reduction, superannuation, and investment strategies simultaneously
2. **Given** an optimized strategy, **When** the system applies compliance checks, **Then** it validates against Best Interest Duty requirements and regulatory guidelines
3. **Given** a compliant strategy, **When** I proceed to implementation, **Then** the system generates structured action plans and milestone tracking

#### Adviser Collaborative Sessions Experience

As an adviser working with a client in a live session through Veris Finance, I want to explore scenarios together in real-time with the system providing calculations and compliance guidance in the background, so we can have productive planning conversations.

**Acceptance Scenarios**:

1. **Given** a live client session, **When** we modify scenarios together, **Then** the system updates calculations in real-time without interrupting the conversation
2. **Given** strategy changes during a session, **When** compliance issues arise, **Then** the system provides immediate warnings to the adviser while maintaining session flow
3. **Given** a completed session, **When** the adviser requests it, **Then** the system generates structured meeting notes and action items

#### Adviser System Monitoring Experience

As a system administrator or compliance officer using Veris Finance, I want to monitor the system's ongoing performance and compliance with changing regulations, so I can ensure the advice platform remains accurate and legally compliant over time.

**Acceptance Scenarios**:

1. **Given** a change in tax legislation, **When** the system detects the change, **Then** it automatically re-evaluates affected client strategies and alerts advisers
2. **Given** periodic health checks, **When** the system runs compliance audits, **Then** it identifies any strategies that no longer meet regulatory requirements
3. **Given** system monitoring, **When** performance issues occur, **Then** the system provides diagnostic information to help resolve problems

---

### Brand-Specific Edge Cases

- How does Frankie's Finance handle users with limited financial literacy?
- What occurs when multiple advisers attempt to modify the same client scenario simultaneously in Veris Finance?
- How do brand-specific user interfaces differ between Frankie's Finance consumer and Veris Finance adviser experiences?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Frankie's Finance MUST provide consumer-focused interface optimized for individual financial education and decision-making
- **FR-002**: Veris Finance MUST provide adviser-focused interface optimized for professional financial planning and compliance
- **FR-003**: Both brands MUST maintain consistent calculation engines while providing brand-appropriate user experiences
- **FR-004**: System MUST support seamless transitions between Frankie's Finance consumer tools and Veris Finance adviser tools
- **FR-005**: Brand experiences MUST reflect appropriate user roles and permissions (consumer vs professional adviser)

### Key Entities *(include if feature involves data)*

- **ConsumerProfile**: Frankie's Finance user profile with consumer-specific preferences and data access
- **AdviserProfile**: Veris Finance user profile with professional credentials, compliance tracking, and client management permissions
- **BrandConfiguration**: Settings that define brand-specific UI, messaging, and feature availability

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Frankie's Finance consumers achieve 90% task completion rate for personal financial questions and scenario exploration
- **SC-002**: Veris Finance advisers complete comprehensive client plans with 95% compliance check success rate
- **SC-003**: Both brands maintain consistent calculation accuracy while providing differentiated user experiences
- **SC-004**: System supports seamless user transitions between consumer and professional interfaces
- **SC-005**: Brand-specific interfaces load and respond within 2 seconds for optimal user experience
