# Feature Specification: Frankie's Finance

**Feature Branch**: `006-frankies-finance`  
**Created**: 2025-01-27  
**Status**: Draft  
**Input**: Frankie's Finance module - consumer mobile UX with emotion-first design. Provides non-linear navigation through spatial metaphors (path, front door, living room, study, garden), guided by Frankie the companion dog. Enables natural language queries, financial guidance, scenario exploration, and goal tracking.

**Purpose**: Frankie's Finance is a personal finance companion that helps everyday Australians feel confident, informed, and emotionally supported when making financial decisions. The app translates complex Australian financial rules into understandable, auditable advice without jargon or judgment. Frankie, a friendly dog companion, guides users through a warm, spatial environment where questions drive navigation and every interaction reduces anxiety and builds understanding.

**Reference**: This module implements requirements from the master specification (`001-master-spec/spec.md`), specifically FR-027, FR-029, FR-039, and FR-040.

## Architectural Boundaries

**Frankie's Finance** is a consumer UX module that consumes backend services. Per Constitution Principle XII:

- **MUST**: Call backend APIs (LLM Orchestrator for natural language processing, Compute Engine for calculations, Advice Engine for compliance validation, References & Research Engine for knowledge retrieval); display results and visualizations; provide user-friendly interfaces.

- **MUST NOT**: Perform calculations (it calls Compute Engine APIs); store knowledge objects (it queries References & Research Engine APIs); contain business logic or decision-making rules (it calls Advice Engine APIs).

All calculations, knowledge storage, and business logic are handled by backend modules. Frankie's Finance focuses on user experience and presentation.

---

## Clarifications

This section addresses ambiguous areas in the specification to eliminate implementation uncertainty.

### Session 2025-01-27

- Q: What should happen when a user's financial question cannot be answered by existing rules or calculations (e.g., question falls outside current rule coverage)? → A: Display supportive message explaining limitation, suggest consulting licensed adviser, maintain warm tone

- Q: What should happen when a user loses connectivity during an active calculation or scenario exploration? → A: Save progress, queue request for retry, display clear offline indicator with what's available offline

- Q: What should happen when compliance validation fails and advice cannot be provided to a consumer (e.g., BLOCK violation detected)? → A: Display consumer-friendly message explaining advice cannot be provided, suggest consulting licensed adviser, maintain supportive tone

- Q: What should happen when a user wants to navigate between environments (e.g., from living room to study) but Frankie's visual cues aren't clear or the user doesn't understand the navigation? → A: Provide alternative navigation (menu/tabs), make Frankie cues optional, support both methods

- Q: What should happen when a user sets a goal but later wants to modify or delete it (e.g., change target amount or timeline)? → A: Allow goal modification/deletion, maintain history, update visual representation in garden

---

## User Scenarios & Testing

### User Story 1 - "What should I do?" Decision Guidance (Priority: P1)

**Consumer Story**: A user wants to ask Frankie questions like "Should I buy this property or keep renting?" or "Should I salary sacrifice more into super?" and receive clear, personalized guidance in plain English with simple visuals showing pros, cons, and long-term impacts.

**Why this priority**: This is the primary consumer value proposition. Users need personalized financial guidance that helps them make decisions. Without this capability, the app cannot deliver its core value of reducing financial anxiety and enabling informed decisions.

**Independent Test**: A user can ask "Should I contribute more to super?" in the living room, receive a conversational response with visual forecasts, see compliance validation, and understand the recommendation through explainable insights—all without feeling judged or overwhelmed.

**Acceptance Scenarios**:

1. **Given** a user opens Frankie's Finance and asks a financial question in the living room, **When** they submit the query, **Then** they receive a conversational response from the app (not Frankie) with personalized guidance, visual forecasts, and compliance validation results displayed in consumer-friendly language.

2. **Given** a user asks "Should I buy this property or keep renting?", **When** the system processes the question, **Then** it executes calculations, validates compliance, and presents pros, cons, and long-term impacts in simple visuals with plain English explanations.

3. **Given** a user receives financial advice, **When** they want to understand why a recommendation was made, **Then** they can access explainable insights tracing the recommendation back to rules and references, presented in consumer-friendly language without technical jargon.

4. **Given** compliance validation identifies issues with advice, **When** warnings are displayed, **Then** they appear in consumer-friendly language, explaining what the issue means and what actions might be needed, without exposing technical compliance details.

---

### User Story 2 - "Explain this to me." Financial Literacy Companion (Priority: P1)

**Consumer Story**: A user wants to ask Frankie to explain complex financial terms or rules ("What's capital gains tax?" or "How does negative gearing work?") so they can build their understanding of the financial system in simple, relatable language.

**Why this priority**: Financial literacy is essential for empowering users. Many users feel overwhelmed by financial jargon. This capability reduces anxiety, builds confidence, and enables users to make better-informed decisions.

**Independent Test**: A user can ask "What's capital gains tax?" and receive a clear, jargon-free explanation with visual analogies, links to authoritative sources, and the ability to ask follow-up questions naturally.

**Acceptance Scenarios**:

1. **Given** a user asks "What's capital gains tax?" in the living room, **When** the system processes the question, **Then** it provides a clear, jargon-free explanation using simple analogies and relatable language, with citations to authoritative sources for verification.

2. **Given** a user asks about a complex financial concept, **When** the explanation is provided, **Then** it uses visual metaphors, analogies, and interactive elements to make the concept understandable without requiring financial expertise.

3. **Given** a user wants to learn more after an explanation, **When** they ask follow-up questions, **Then** the system maintains conversation context and provides deeper explanations, building understanding progressively.

4. **Given** a user asks about a financial rule or regulation, **When** the explanation is provided, **Then** it includes citations to authoritative sources (References) that users can explore if they want more detail, building trust through transparency.

---

### User Story 3 - "Run the numbers." Scenario Simulation (Priority: P1)

**Consumer Story**: A user wants to test different financial scenarios ("What happens if I retire at 58 instead of 65?" or "If I invest $20k a year, how much will I have by 2040?") so they can make better-informed decisions using concrete projections and see long-term trade-offs.

**Why this priority**: Scenario exploration is essential for financial planning. Users need to see "what-if" outcomes to make informed decisions. This capability enables experimentation without fear and builds confidence through understanding.

**Independent Test**: A user can ask "What happens if I retire at 58 instead of 65?" in the study, view comparative forecasts with visual charts, adjust parameters using sliders, and see how outcomes change in real-time—all presented in an intuitive, playful way.

**Acceptance Scenarios**:

1. **Given** a user asks about a financial scenario in the study, **When** they submit the query, **Then** Frankie guides them to the study environment, and the system executes calculations, presenting results as visual forecasts with charts and projections.

2. **Given** a user wants to compare scenarios (e.g., retirement at 58 vs 65), **When** they request comparison, **Then** the system executes multiple scenario calculations and presents side-by-side comparisons with visual charts showing differences and trade-offs.

3. **Given** a user wants to adjust scenario parameters, **When** they use sliders or chat-driven prompts in the study, **Then** the system updates calculations in real-time, showing how outcomes change as parameters adjust, with Frankie narrating what's happening.

4. **Given** a user explores scenarios, **When** they view results, **Then** each scenario is tagged and stored, enabling them to return to previous experiments and compare outcomes over time.

---

### User Story 4 - "Help me plan." Goal Setting & Tracking (Priority: P2)

**Consumer Story**: A user wants to log goals such as buying a house, paying off debt, or building super so that Frankie can help them stay intentional—reminding them of milestones, showing progress, and adjusting advice as their circumstances change.

**Why this priority**: Goal tracking provides motivation and accountability. Users need to see progress and feel supported in achieving their financial goals. This capability builds long-term engagement and helps users stay focused.

**Independent Test**: A user can set a goal (e.g., "Save $50k for a house deposit"), track progress in the garden, receive milestone reminders, and see how their financial decisions affect goal achievement through visual metaphors (trees growing, flowers blooming).

**Acceptance Scenarios**:

1. **Given** a user wants to set a financial goal, **When** they express the goal naturally (e.g., "I want to save for a house"), **Then** the system helps them define the goal with specific parameters (amount, timeline) and stores it for tracking.

2. **Given** a user has set goals, **When** they visit the garden, **Then** they see visual representations of their goals (trees, flowers) showing progress, with Frankie celebrating milestones and providing encouragement.

3. **Given** a user's financial circumstances change, **When** they update their situation, **Then** the system adjusts advice and goal projections accordingly, showing how changes affect goal achievement.

4. **Given** a user reaches a milestone, **When** progress is updated, **Then** Frankie celebrates visibly (running, wagging tail), the garden environment brightens, and the user receives positive reinforcement for their achievement.

---

### User Story 5 - "Am I on the right track?" Health & Progress Reports (Priority: P2)

**Consumer Story**: A user wants to receive periodic check-ins (monthly or quarterly) showing how their financial situation is evolving so they can see whether they're improving, identify risks early, and feel supported in achieving their long-term goals.

**Why this priority**: Regular check-ins provide ongoing support and help users stay engaged. Users need to see progress and feel supported over time. This capability builds long-term relationships and helps users maintain financial health.

**Independent Test**: A user receives a monthly check-in showing their financial health evolution, with visual indicators of progress, risk identification, and supportive messaging that helps them feel confident and motivated.

**Acceptance Scenarios**:

1. **Given** a user has been using the app, **When** a periodic check-in is triggered (monthly or quarterly), **Then** the system generates a progress report showing financial health evolution, goal progress, and risk indicators.

2. **Given** a progress report identifies risks or concerns, **When** it is presented, **Then** it uses supportive, non-alarming language, explains what the risks mean, and suggests actions users can take, maintaining an encouraging tone.

3. **Given** a progress report shows improvement, **When** it is presented, **Then** it celebrates achievements, reinforces positive behaviors, and provides motivation to continue, with Frankie visibly celebrating in the garden.

4. **Given** a user wants to review their financial health, **When** they request a progress report, **Then** the system generates it on-demand, showing current status, trends over time, and recommendations for improvement.

---

### User Story 6 - "See My Future." Easy-to-Use Forecasting (Priority: P2)

**Consumer Story**: A user wants to easily create forecasts of their financial future—like "What will my super look like at 65?" or "If I buy this house, how much will I have left each month?"—so they can understand where their money is heading without needing financial or technical expertise.

**Why this priority**: Forecasting helps users understand long-term implications of financial decisions. Users need simple, visual forecasts that feel playful and intuitive, not intimidating. This capability enables informed decision-making through understanding.

**Independent Test**: A user can ask "What will my super look like at 65?" using chat-driven prompts or sliders, see forecasts adjust live as parameters change, with Frankie narrating what's happening, and understand outcomes through simple charts and visualizations.

**Acceptance Scenarios**:

1. **Given** a user wants to forecast their financial future, **When** they ask a forecasting question or use chat-driven prompts ("Let's peek 10 years ahead"), **Then** the system executes calculations and presents forecasts as visual charts that adjust live as parameters change.

2. **Given** a user adjusts forecast parameters using sliders, **When** they change values, **Then** the system updates calculations in real-time, showing how outcomes change, with Frankie narrating what's happening in a playful, engaging way.

3. **Given** forecasting feels playful and visual, **When** forecasts are presented, **Then** they use intuitive charts, simple visualizations, and engaging interactions that make financial planning feel approachable rather than intimidating.

4. **Given** a user wants to understand forecast assumptions, **When** they explore deeper, **Then** the system provides explanations of assumptions used, enabling users to understand how forecasts are calculated without requiring technical knowledge.

---

### Edge Cases

- What happens when a user's question cannot be answered by existing rules or calculations? The system MUST gracefully indicate when questions fall outside current coverage, suggest consulting a human adviser, and maintain a supportive, non-judgmental tone.

- How does the system handle users who feel overwhelmed or anxious during interactions? The system MUST provide calming visual elements, allow users to pause or exit, and offer gentle encouragement through Frankie's behavior and environmental cues.

- What happens when compliance validation fails and advice cannot be provided? The system MUST gracefully handle validation failures, inform users that advice cannot be provided, suggest consulting a licensed financial adviser, and maintain a supportive tone without causing additional anxiety.

- How does the system handle users who want to skip onboarding or jump directly to specific features? The system MUST support non-linear navigation, allowing users to enter any environment (living room, study, garden) based on their intent, without forcing sequential progression.

- What happens when a user's device loses connectivity during an interaction? The system MUST handle connectivity issues gracefully, save progress where possible, and provide clear messaging about connectivity requirements without disrupting the emotional experience.

- How does the system handle users who prefer text over voice interaction or vice versa? The system MUST support both text and voice interaction modes, allowing users to choose their preferred method and switch between modes seamlessly.

---

## Requirements

### Functional Requirements

#### Spatial Navigation and Environments

- **FR-001**: System MUST provide five distinct environments: Path to the House (entry/onboarding), Front Door (transition), Living Room (conversation/reflection), Study (forecasting/scenarios), and Garden (goals/progress).

- **FR-002**: System MUST enable non-linear navigation where user questions dictate movement between environments, with Frankie guiding transitions through visual cues (wagging, running ahead, looking expectantly). When Frankie's visual cues aren't clear or users don't understand the navigation, the system MUST provide alternative navigation methods (menu/tabs), make Frankie cues optional, and support both navigation methods to ensure accessibility and usability.

- **FR-003**: System MUST support navigation by intent: when users ask questions about numbers or strategy, Frankie guides to the study; when users ask about goals or progress, Frankie guides to the garden; general questions remain in the living room.

- **FR-004**: System MUST provide smooth, fluid transitions between environments that feel natural and calming, avoiding abrupt scene cuts or jarring changes.

- **FR-005**: System MUST maintain persistent state in each environment: living room retains conversations and reflections, study remembers experiments and models, garden visually represents ongoing goals.

- **FR-006**: System MUST allow users to stay in an environment and reflect, or follow Frankie's lead to explore, giving users control over pace and depth of interaction.

#### Frankie Companion

- **FR-007**: System MUST present Frankie as a companion guide (not the adviser) who provides emotional support, visual navigation cues, and warmth, while the app itself provides the advice voice.

- **FR-008**: System MUST provide Frankie behaviors that communicate meaning: wagging and running ahead ("Follow me"), tilting head or sitting ("I'm listening"), lying beside user ("You're safe here"), soft bark ("I found something interesting"), running in garden (celebration).

- **FR-009**: System MUST make Frankie's cues non-intrusive invitations rather than demands, allowing users to control when to follow Frankie's lead.

- **FR-010**: System MUST display Frankie in every environment, providing continuity and emotional grounding throughout the user's journey.

#### Natural Language Interaction

- **FR-011**: System MUST support natural language queries via text or voice input, enabling users to ask questions conversationally without learning specific commands or syntax.

- **FR-012**: System MUST integrate with natural language processing services to process natural language queries and receive conversational responses with tool calls and citations.

- **FR-013**: System MUST maintain conversation context across multiple turns, understanding references to previous messages and maintaining coherent dialogue.

- **FR-014**: System MUST format conversational responses appropriately for consumers, using plain English, avoiding jargon, and explaining financial concepts in relatable language.

- **FR-015**: System MUST support both text and voice interaction modes, allowing users to choose their preferred method and switch seamlessly between modes.

#### Financial Guidance and Advice

- **FR-016**: System MUST provide personalized financial guidance based on user questions, executing calculations and presenting results with visual forecasts, pros/cons, and long-term impacts.

- **FR-017**: System MUST validate all financial advice before presenting it to users, ensuring compliance with best-interests duty and regulatory requirements.

- **FR-018**: System MUST display compliance validation results in consumer-friendly, non-technical language, explaining what validation means and any warnings or required actions without exposing technical details.

- **FR-019**: System MUST provide explainable insights for all recommendations, enabling users to understand why advice was given through traces linking to rules and references, presented in consumer-friendly language.

- **FR-020**: System MUST handle advice that cannot be provided (due to compliance failures or rule coverage gaps) gracefully, informing users supportively and suggesting consulting a licensed financial adviser when appropriate. When a user's financial question cannot be answered by existing rules or calculations (question falls outside current rule coverage), the system MUST display a supportive message explaining the limitation, suggest consulting a licensed adviser, and maintain a warm, non-judgmental tone throughout the interaction. When compliance validation fails and advice cannot be provided to a consumer (e.g., BLOCK violation detected), the system MUST display a consumer-friendly message explaining that advice cannot be provided, suggest consulting a licensed adviser, and maintain a supportive, non-alarming tone throughout the interaction.

#### Scenario Exploration and Forecasting

- **FR-021**: System MUST enable scenario simulation ("what-if" analysis) allowing users to test different financial scenarios and compare outcomes side-by-side.

- **FR-022**: System MUST provide interactive forecasting tools (sliders, chat-driven prompts) that allow users to adjust parameters and see outcomes update in real-time.

- **FR-023**: System MUST present forecasts and scenarios visually with charts, graphs, and simple visualizations that make financial projections understandable without requiring technical expertise.

- **FR-024**: System MUST execute scenario calculations, retrieving results and explanations for display.

- **FR-025**: System MUST tag and store scenarios for future reference, enabling users to return to previous experiments and compare outcomes over time.

#### Goal Setting and Tracking

- **FR-026**: System MUST enable users to set financial goals (buying a house, paying off debt, building super) with specific parameters (amount, timeline) through natural language or structured input. Users MUST be able to modify or delete goals after creation. When a goal is modified or deleted, the system MUST maintain history of the original goal, update the visual representation in the garden accordingly, and preserve progress tracking data for audit purposes.

- **FR-027**: System MUST display goals visually in the garden environment using metaphors (trees, flowers) that show progress and growth.

- **FR-028**: System MUST track goal progress over time, updating visual representations as users make progress toward their goals.

- **FR-029**: System MUST provide milestone reminders and celebrations, with Frankie visibly celebrating achievements and the garden environment brightening to reinforce progress.

- **FR-030**: System MUST adjust advice and goal projections when user circumstances change, showing how changes affect goal achievement.

#### Progress Reports and Health Checks

- **FR-031**: System MUST generate periodic progress reports (monthly or quarterly) showing financial health evolution, goal progress, and risk indicators.

- **FR-032**: System MUST present progress reports using supportive, non-alarming language, explaining risks and improvements in ways that motivate rather than discourage users.

- **FR-033**: System MUST enable on-demand progress reports, allowing users to request financial health reviews at any time.

- **FR-034**: System MUST celebrate improvements and achievements in progress reports, reinforcing positive behaviors and providing motivation to continue.

#### Visual Design and Emotion

- **FR-035**: System MUST use emotion-first design that calms, reassures, and empowers users, reducing shame and replacing fear with curiosity.

- **FR-036**: System MUST provide visual elements (lighting, sound, motion) that adjust to user tone and emotional state, creating a responsive, supportive environment.

- **FR-037**: System MUST present forecasts and explanations in organic ways (notes opening, sketches forming, charts glowing) that feel natural rather than mechanical.

- **FR-038**: System MUST maintain a warm, welcoming visual language throughout all environments, using colors, typography, and imagery that create a sense of safety and comfort.

#### Mobile-First Experience

- **FR-039**: System MUST provide a mobile-first experience optimized for touch interaction, with Frankie's behaviors triggered by tapping when he becomes animated.

- **FR-040**: System MUST support offline capabilities where possible, allowing users to access previously loaded content and view progress even without connectivity.

- **FR-041**: System MUST handle connectivity issues gracefully, saving progress where possible and providing clear messaging about connectivity requirements. When a user loses connectivity during an active calculation or scenario exploration, the system MUST save progress, queue the request for retry when connectivity is restored, and display a clear offline indicator explaining what functionality is available offline versus what requires connectivity.

#### Offline Capabilities and Sync

- **FR-042**: System MUST support offline access to previously loaded content (conversations, scenarios, goals, visualizations), view progress and goal tracking, access to cached API responses (via TanStack Query cache), and environment state persistence (path, front door, living room, study, garden). Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-043**: System MUST require connectivity for new calculations (`POST /run`, `POST /run-batch`), new natural language queries (`POST /llm/chat`), real-time scenario updates, and fresh compliance validation. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-044**: System MUST persist state using AsyncStorage for local state persistence, including environment state, conversations, scenarios, and goals. Backend is source of truth; AsyncStorage used for caching and offline access. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-045**: System MUST implement online-first architecture with offline caching, handling connectivity issues gracefully, saving progress where possible, and providing clear messaging about connectivity requirements. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-046**: System MUST automatically sync cached changes and refetch stale data when connectivity is restored, using TanStack Query automatic cache management and background refetching. Failed requests MUST be queued and retried on reconnect. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-047**: System MUST implement conflict resolution using last-write-wins strategy for simple state updates. For critical data (scenarios, calculations), system MUST validate with backend before applying local changes. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-048**: System MUST invalidate cache based on data freshness requirements: critical data (calculations, compliance) invalidated immediately; less critical data (conversations, goals) cached longer. Reference: `specs/001-master-spec/spec.md` CL-034.

- **FR-049**: System MUST display clear offline indicators and messaging when connectivity is unavailable, informing users about what functionality is available offline vs. requires connectivity. Reference: `specs/001-master-spec/spec.md` CL-034.

---

### Key Entities

- **User Session**: Active user interaction session within Frankie's Finance. Attributes include: session identifier, current environment (path, front door, living room, study, garden), conversation history, active goals, scenario experiments, and user preferences. Maintains state across interactions.

- **Goal**: User-defined financial objective. Attributes include: goal identifier, description, target amount, target date, current progress, milestones, and visual representation (tree/flower in garden). Linked to user session and tracked over time.

- **Conversation**: Multi-turn dialogue between user and the app. Attributes include: conversation identifier, message history, detected intents, extracted parameters, tool calls generated, and citations included. Maintained for context and continuity.

- **Scenario Experiment**: User's "what-if" scenario exploration. Attributes include: experiment identifier, scenario parameters, calculation results (Facts), visualizations generated, and timestamp. Stored for future reference and comparison.

- **Progress Report**: Periodic or on-demand financial health assessment. Attributes include: report identifier, report date, financial health metrics, goal progress summary, risk indicators, achievements, and recommendations. Generated from user data and calculations.

- **Visualization**: Chart, graph, or visual representation of financial data. Attributes include: visualization type (forecast chart, comparison graph, progress indicator), data source (Facts from Compute Engine), parameters used, and presentation format. Generated for display in study or garden environments.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can ask financial questions and receive personalized guidance within 5 seconds from query submission to displayed response (excluding complex multi-scenario calculations).

- **SC-002**: 90% of users successfully navigate between environments (living room, study, garden) using Frankie's visual cues without requiring instructions or help text.

- **SC-003**: 85% of users successfully complete their intended task (get advice, explore scenarios, set goals) when interacting via natural language without requiring multiple clarification rounds.

- **SC-004**: 90% of users understand financial explanations provided by the app without requiring additional clarification or external resources.

- **SC-005**: 80% of users feel less anxious about financial decisions after using the app, as measured by user satisfaction surveys and self-reported anxiety levels.

- **SC-006**: Users can create and view forecasts with parameter adjustments, seeing results update in real-time within 3 seconds for 90% of parameter changes.

- **SC-007**: 75% of users who set goals return to track progress within 30 days, demonstrating engagement and value from goal tracking features.

- **SC-008**: 100% of financial advice presented to users is validated by Advice Engine before display, ensuring compliance with regulatory requirements.

- **SC-009**: 90% of users can access explainable insights for recommendations and understand why advice was given without requiring technical or financial expertise.

- **SC-010**: System maintains conversation context across up to 10 message turns, enabling natural multi-turn dialogue for 85% of conversations.

---

## Assumptions

### Domain Assumptions

- Users will primarily access Frankie's Finance via mobile devices (smartphones, tablets) with touch interfaces.

- Users will prefer natural language interaction over structured forms for most queries, enabling conversational interfaces.

- Users will value emotional support and non-judgmental guidance over purely functional financial tools.

- Financial anxiety and shame are common barriers that the app must address through design and interaction patterns.

### Technical Assumptions

- Mobile devices will have sufficient processing power and connectivity to support real-time calculations and visualizations.

- LLM Orchestrator will provide natural language processing with acceptable latency for conversational interactions.

- Compute Engine will execute calculations within acceptable time limits for real-time scenario exploration.

- Advice Engine will validate compliance within acceptable time limits for seamless user experience.

### User Behavior Assumptions

- Users will engage with the app non-linearly, jumping between environments based on their current needs rather than following a sequential flow.

- Users will appreciate Frankie's companionship and visual guidance, finding it helpful rather than gimmicky.

- Users will prefer visual representations (charts, metaphors) over text-heavy explanations for financial concepts.

- Users will value transparency and explainability, wanting to understand how advice is calculated even if they don't need technical details.

### Integration Assumptions

- Natural language processing services will transform natural language queries into structured requests that calculation services can execute.

- Calculation services will return calculation results in formats suitable for visual presentation in the app.

- Compliance validation services will provide compliance validation results formatted appropriately for consumer display.

- Backend services will maintain acceptable performance to support real-time interactions and scenario exploration.

---

## Scope Boundaries

### In Scope (MVP)

- Core spatial environments: path, front door, living room, study, garden

- Natural language interaction via natural language processing services

- Financial guidance and advice with compliance validation

- Basic scenario exploration and forecasting

- Goal setting and visual tracking in garden

- Frankie companion with visual navigation cues

- Mobile-first touch interface

- Consumer-friendly explanations and visualizations

### Out of Scope (Future)

- Advanced goal planning features beyond basic tracking

- Social features or sharing capabilities

- Integration with external financial accounts or bank aggregation

- Advanced analytics or detailed financial reporting

- Multi-user or family account features

- Advanced personalization using machine learning

- Offline-first architecture with full offline capabilities

- Integration with external financial product marketplaces

---

## Dependencies

### External Dependencies

- Mobile device capabilities (touch interface, sufficient processing power, connectivity)

- LLM provider APIs (via LLM Orchestrator) for natural language processing

- Mobile app platform (iOS, Android, or cross-platform framework) for app deployment

### Internal Dependencies

- Master specification (`001-master-spec`) for system context, requirements, and architectural constraints

- Natural language processing services for processing user queries

- Calculation services for executing financial calculations and scenario modelling

- Compliance validation services for validating compliance of financial advice provided to consumers

- Reference lookup services for citation generation and context enhancement

- Authentication/authorization system for user accounts and session management (from foundational infrastructure)
