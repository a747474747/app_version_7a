# Frankie's Finance Implementation Plan

**Branch**: `006-frankies-finance` | **Date**: 2025-01-27 | **Spec**: `specs/006-frankies-finance/spec_006_frankies_finance.md`  
**Status**: ✅ **Phase 0 Complete**

## Summary

Frankie's Finance is a consumer mobile UX with emotion-first design. Provides non-linear navigation through spatial metaphors (path, front door, living room, study, garden), guided by Frankie the companion dog.

**Technical Approach**: React Native mobile application (iOS/Android) with Expo, TanStack Query for API caching, Tamagui for shared design tokens, natural language interaction via LLM Orchestrator, financial calculations via Compute Engine, compliance validation via Advice Engine. Sentry for error tracking.

## Technical Context

**Language/Version**: TypeScript/React Native

**Primary Dependencies**:
- **Framework**: React Native with Expo
- **Navigation**: React Navigation v6 (custom spatial navigation system)
- **State Management**: Zustand (lightweight state management)
- **API Caching**: TanStack Query (React Query) for API caching and synchronization
- **Design System**: Tamagui for shared design tokens (mobile + web)
- **Error Tracking**: Sentry (free tier) for error monitoring
- **Testing**: Jest, React Native Testing Library

## API Integration

### Backend Service Integration

- **LLM Orchestrator**: 
  - Natural language queries via `POST /llm/chat` and `POST /llm/parse`
  - Receives conversational responses with tool calls and citations

- **Compute Engine**: 
  - Structured calculation requests via `POST /run` and `POST /run-batch` (transformed by LLM Orchestrator)
  - Results via `GET /facts`
  - Explanations via `GET /explain/{fact_id}`

- **Advice Engine**: 
  - Compliance checking via `POST /advice/check` for all financial advice
  - Receives validation results formatted for consumer-friendly display

- **References & Research Engine**: 
  - Indirect integration via LLM Orchestrator for citation generation

## Module Dependencies

### Depends On

- **LLM Orchestrator** (`005-llm-orchestrator`): Natural language processing of consumer queries
- **Compute Engine** (`002-compute-engine`): Executing financial calculations and scenario modelling
- **Advice Engine** (`004-advice-engine`): Validating compliance of financial advice provided to consumers
- **References & Research Engine** (`003-references-research-engine`): Citation generation (via LLM Orchestrator)

## Technical Implementation Details

### Spatial Navigation

- **Environments**: Path, Front Door, Living Room, Study, Garden
- **Non-Linear Navigation**: User questions dictate movement between environments
- **Frankie Guidance**: Visual cues (wagging, running ahead, looking expectantly) guide transitions
- **State Persistence**: Maintain persistent state in each environment

### Frankie Companion

- **Behaviors**: Wagging, running ahead, tilting head, sitting, lying beside user, soft bark, running in garden
- **Non-Intrusive**: Invitations rather than demands
- **Continuity**: Displayed in every environment

### Natural Language Interaction

- **Input Methods**: Text or voice input
- **LLM Integration**: Via LLM Orchestrator for processing
- **Context Maintenance**: Conversation context across multiple turns
- **Formatting**: Consumer-friendly language, plain English, avoiding jargon

### Financial Guidance

- **Calculation Execution**: Via Compute Engine
- **Compliance Validation**: Via Advice Engine before presentation
- **Explainable Insights**: Trace recommendations back to rules and references
- **Visual Forecasts**: Charts, graphs, simple visualizations

### Scenario Exploration

- **Interactive Tools**: Sliders, chat-driven prompts
- **Real-Time Updates**: Calculations update as parameters change
- **Visual Presentation**: Charts, graphs, visualizations
- **Scenario Storage**: Tag and store scenarios for future reference

### Goal Tracking

- **Visual Representation**: Garden metaphors (trees, flowers) showing progress
- **Milestone Celebrations**: Frankie celebrates achievements visibly
- **Progress Updates**: Update visual representations as users make progress

## Implementation Phases

### Phase 1: Initial Setup, PII Filtering Transparency, and Spatial Navigation (Weeks 1-2)

**Tasks**:
1. **Initial Setup Flow**
   - Implement initial setup screen for new users
   - Collect user name, date of birth, and suburb during setup
   - Explain that this information helps personalize the experience
   - Store collected PII profile for enhanced filtering (name, DOB, suburb, collection timestamp, consent acknowledgment)
   - Reference: `specs/001-master-spec/spec.md` User Story 4, FR-067, FR-068, FR-069, FR-070, FR-071

2. **Privacy Explanation Screen**
   - Display privacy explanation screen after initial setup completion
   - Clearly state: "Your name and any identifying information about you will be filtered out of requests to external AIs so that your information is not connected to you and you cannot be identified from your information."
   - Provide access to privacy policy through clear link or button
   - Ensure privacy explanation is displayed before users can ask financial questions
   - Handle cases where users skip or cancel setup (still display privacy info before queries)
   - Reference: `specs/001-master-spec/spec.md` User Story 4, FR-067, FR-069, FR-070, FR-078

3. **Privacy Settings Access**
   - Implement privacy settings screen accessible at any time
   - Allow users to review what information has been collected
   - Allow users to update privacy preferences
   - Reference: `specs/001-master-spec/spec.md` FR-079

4. **Environment Design**
   - Design five environments (path, front door, living room, study, garden)
   - Implement non-linear navigation
   - Implement smooth transitions between environments
   - Implement persistent state in each environment

5. **Frankie Companion**
   - Implement Frankie companion behaviors (wagging, running, sitting, lying, soft bark)
   - Implement visual navigation cues
   - Implement non-intrusive invitations

**Deliverables**:
- Initial setup flow functional
- Privacy explanation displayed before first financial question
- Privacy policy accessible within 2 clicks/taps
- Privacy settings accessible at any time
- PII profile stored for enhanced filtering (integrated with LLM Orchestrator)
- Five environments functional
- Frankie companion behaviors working
- Non-linear navigation operational

### Phase 2: Natural Language Interaction (Week 3)

**Tasks**:
1. **LLM Integration**
   - Integrate with LLM Orchestrator (`POST /llm/chat`, `POST /llm/parse`)
   - Implement text and voice input
   - Implement conversation context maintenance
   - Implement consumer-friendly response formatting
   - Ensure collected user name is used by LLM Orchestrator for enhanced PII filtering (known name enables more accurate detection of name references in queries)
   - Reference: `specs/001-master-spec/spec.md` FR-071

**Deliverables**:
- Natural language interaction working
- Conversation context maintained
- Enhanced PII filtering operational (using known user name)

### Phase 3: Financial Guidance and Advice (Week 4)

**Tasks**:
1. **Backend Integration**
   - Integrate with Compute Engine (`POST /run`, `GET /facts`, `GET /explain/{fact_id}`)
   - Integrate with Advice Engine (`POST /advice/check`)
   - Implement personalized financial guidance
   - Implement visual forecasts and pros/cons
   - Implement compliance validation display (consumer-friendly)
   - Implement explainable insights (consumer-friendly language)

**Deliverables**:
- Financial guidance functional
- Compliance validation integrated
- Explainable insights working

### Phase 4: Scenario Exploration and Forecasting (Week 5)

**Tasks**:
1. **Scenario Features**
   - Implement scenario simulation ("what-if" analysis)
   - Implement interactive forecasting tools (sliders, chat-driven prompts)
   - Implement visual charts and graphs
   - Implement real-time parameter adjustment

**Deliverables**:
- Scenario exploration functional
- Real-time forecasting working

### Phase 5: Goal Setting and Tracking (Week 6)

**Tasks**:
1. **Goal Management**
   - Implement goal setting (natural language and structured input)
   - Implement visual goal representation in garden (trees, flowers)
   - Implement goal progress tracking
   - Implement milestone reminders and celebrations

**Deliverables**:
- Goal tracking functional
- Visual representation working

### Phase 6: Progress Reports and Health Checks (Week 7)

**Tasks**:
1. **Reporting**
   - Implement periodic progress reports (monthly/quarterly)
   - Implement on-demand progress reports
   - Implement supportive, non-alarming language
   - Implement achievement celebration

**Deliverables**:
- Progress reports functional
- Health checks working

### Phase 7: Visual Design and Emotion (Week 8)

**Tasks**:
1. **Emotion-First Design**
   - Implement emotion-first design
   - Implement responsive visual elements (lighting, sound, motion)
   - Implement organic presentation (notes opening, sketches forming)
   - Implement warm, welcoming visual language

**Deliverables**:
- Emotion-first design implemented
- Visual elements responsive

### Phase 8: Mobile-First Experience (Week 9)

**Tasks**:
1. **Mobile Optimization**
   - Implement touch-optimized interface
   - Implement offline capabilities (where possible)
   - Implement graceful connectivity handling

2. **Offline Capabilities Implementation**
   - Implement AsyncStorage persistence for environment state, conversations, scenarios, goals
   - Implement TanStack Query cache management for offline API response access
   - Implement offline UI indicators and messaging
   - Implement sync on reconnect (automatic sync of cached changes, refetch stale data)
   - Implement request queue for failed requests (retry on reconnect)
   - Implement conflict resolution (last-write-wins for simple updates, backend validation for critical data)
   - Implement cache invalidation strategy (immediate for critical data, longer cache for less critical data)
   - Reference: `specs/001-master-spec/spec.md` CL-034

**Deliverables**:
- Mobile-first experience functional
- Offline capabilities working
- Offline state persistence operational (AsyncStorage)
- Sync on reconnect functional
- Offline UI indicators and messaging implemented

### Phase 9: Testing (Ongoing)

**Tasks**:
1. **Test Implementation**
   - Unit tests for UI components
   - Integration tests with backend modules
   - End-to-end tests (React Native Testing Library, Detox)
   - User acceptance tests (emotion-first design validation)

**Deliverables**:
- Test coverage > 75%

