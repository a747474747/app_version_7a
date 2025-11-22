# Research Findings: Four-Engine System Architecture

**Research Date**: November 21, 2025
**Status**: Complete
**Researcher**: AI Assistant

This document consolidates research findings for all technical unknowns identified in the implementation plan. Each research task includes the decision made, rationale, and alternatives considered.

---

## 1. Multi-User Architecture

### 1.1 Authentication Patterns

**Decision**: Clerk (SaaS) authentication with role-based access control (RBAC) managed via Clerk metadata.

**Rationale**:
- Offloads auth complexity (MFA, session management, security) to a managed provider
- Clerk metadata handles RBAC for the four user types: consumers, advisers, compliance officers, partners
- Focuses development velocity on core Engine logic instead of auth infrastructure
- Aligns with solo-developer MVP constraints and plan.md technology choices

**Alternatives Considered**:
- Custom FastAPI JWT: Too complex for MVP, massive time sink for auth infrastructure
- OAuth 2.0 + OpenID Connect: Overkill for MVP scope, requires external identity provider management
- API Key authentication: Insufficient for user-specific permissions and session management
- Session-based auth with cookies: Less suitable for API-first architecture

### 1.2 Role-Based Access Control

**Decision**: Four-tier role system: `consumer`, `adviser`, `compliance`, `partner` with hierarchical permissions managed via Clerk metadata.

**Rationale**:
- Maps directly to user stories (US-3 Adviser Comprehensive Planning, US-4 System Health Monitoring)
- Hierarchical permissions: compliance > adviser > consumer > partner
- Clerk metadata handles RBAC instead of custom database tables
- Supports the functional requirement FR-008 (multiple user types with appropriate access controls)
- Simple to implement and maintain with managed auth provider

**Permission Matrix**:
```
consumer: read_own_scenarios, create_scenarios, run_calculations
adviser: consumer_permissions + read_client_scenarios, create_advice, compliance_warnings
compliance: adviser_permissions + system_monitoring, rule_management, audit_logs
partner: limited_api_access, read_public_scenarios
```

**Alternatives Considered**:
- Attribute-based access control (ABAC): Overkill for MVP, complex permission logic
- Flat permission system: Doesn't support the hierarchical adviser-client relationship
- Custom database role tables: Unnecessary complexity when Clerk metadata suffices

### 1.3 Session Management

**Decision**: Clerk-managed sessions with automatic token refresh and session persistence.

**Rationale**:
- Clerk handles all session management complexity (MFA, refresh tokens, security)
- Automatic token refresh prevents user friction during collaborative sessions
- Offloads session security concerns to managed provider
- Focuses development on core Engine logic instead of session infrastructure

**Alternatives Considered**:
- Custom JWT with 24-hour expiration: Unnecessary complexity for MVP
- Long-lived tokens (7 days): Security risk for financial data, but Clerk handles this better
- Session storage in database: Adds complexity when Clerk provides session management

---

## 2. Real-time Collaboration

### 2.1 Optimistic UI Implementation

**Decision**: Optimistic UI (TanStack Query) for perceived real-time scenario updates without WebSocket complexity.

**Rationale**:
- WebSockets are overkill and operationally complex for 100 users on Render
- Optimistic updates provide the "feeling" of real-time without stateful server management
- Aligns with success criteria SC-009 (optimistic UI updates < 100ms per plan.md)
- Simplifies deployment and reduces operational complexity for solo-developer MVP

**Implementation Approach**:
- TanStack Query for client-side caching and optimistic updates
- Background sync for scenario modifications
- Conflict detection with user notifications
- Last-write-wins strategy for concurrent edits

**Alternatives Considered**:
- WebSockets: Too complex for MVP, operational overhead on Render
- Server-Sent Events (SSE): One-way only, insufficient for collaborative editing
- Polling only: Poor user experience for real-time collaboration
- WebRTC: Overkill for data collaboration, better suited for video/audio

### 2.2 Conflict Resolution

**Decision**: Last-write-wins with conflict detection and user notifications.

**Rationale**:
- Financial scenarios typically have clear ownership (adviser-led sessions)
- Last-write-wins prevents data loss in collaborative editing
- Conflict detection alerts users to simultaneous changes
- Simpler than complex merge algorithms for financial data

**Conflict Detection**:
- Version numbers on scenario objects
- Timestamp-based conflict detection
- User notifications for overwritten changes
- Optional change history for reconciliation

**Alternatives Considered**:
- Operational Transformation: Complex for financial data structures
- Manual conflict resolution UI: Poor user experience, increases session friction
- Single-user locking: Prevents true collaboration

### 2.3 Performance Implications

**Decision**: Optimize for 10 concurrent scenario modifications per session with horizontal scaling.

**Rationale**:
- Success criteria SC-009 specifies support for 10 concurrent modifications
- Horizontal scaling (multiple Render instances) handles load
- Calculation results cached to reduce redundant computations
- TanStack Query handles optimistic updates efficiently

**Performance Optimizations**:
- Calculation result caching (Redis optional for MVP)
- Debounced updates (500ms delay for rapid changes)
- Background processing for heavy calculations
- Optimistic UI updates (< 100ms perceived latency)

**Alternatives Considered**:
- Vertical scaling only: Limited by Render's instance sizes
- No caching: Poor performance for repeated calculations
- Synchronous updates: Blocks UI during calculations

---

## 3. External Data Integration

### 3.1 Bank Feed APIs

**Decision**: DEFERRED / OUT OF SCOPE - Manual data entry and LLM chat parsing only for MVP.

**Rationale**:
- Open Banking (CDR) integration is too heavy for solo-developer MVP
- Manual entry or LLM parsing of shared financial statements suffices for initial use cases
- Aligns with plan.md technology constraints (external data integration excluded)
- Focuses development velocity on core Engine logic

**Integration Points** (Future):
- Account balances for position context
- Transaction history for cashflow validation
- Investment holdings for portfolio context
- Loan details for debt context

**Alternatives Considered**:
- Open Banking APIs: Too complex for MVP scope, regulatory overhead
- Screen scraping: Fragile, unreliable, potential legal issues
- Third-party aggregation services: Additional cost and complexity
- Manual data entry only: Acceptable for MVP with LLM assistance for parsing

### 3.2 Regulatory Data Sources

**Decision**: File-based regulatory data with automated update notifications.

**Rationale**:
- Regulatory changes drive Mode 7 (Proactive Monitor)
- File-based storage aligns with constitution (Phase 1-3 knowledge storage)
- Automated notifications ensure timely updates
- Supports success criteria SC-008 (100% regulatory change detection)

**Implementation**:
- Markdown/YAML files for tax rules, thresholds, rates
- Version control with change detection
- Webhook notifications for rule updates
- Audit trail for regulatory changes

**Alternatives Considered**:
- Direct API integration: Limited availability of regulatory APIs
- Manual rule updates: Error-prone, doesn't meet automation requirements
- Database storage only: Constitution prefers file-based for phases 1-3

### 3.3 Data Synchronization

**Decision**: Event-driven synchronization with idempotent operations.

**Rationale**:
- Event-driven approach handles intermittent connectivity
- Idempotent operations prevent duplicate data processing
- Supports both push (webhooks) and pull (scheduled) patterns
- Reliable for financial data integrity

**Synchronization Patterns**:
- Webhook receivers for real-time updates
- Scheduled sync jobs for batch processing
- Conflict resolution with source system priority
- Data quality validation before storage

**Alternatives Considered**:
- Real-time polling: Resource intensive, potential rate limiting
- Batch-only sync: Poor real-time user experience
- Manual synchronization: Error-prone and unreliable

---

## 4. Scale and Performance

### 4.1 Concurrent User Load

**Decision**: Design for 100 concurrent users with 10-second average response times.

**Rationale**:
- Balances MVP scope with realistic business requirements
- 100 concurrent users supports small-to-medium advisory practice
- 10-second target provides good UX while allowing complex calculations
- Horizontal scaling path available on Render

**Capacity Planning**:
- 100 concurrent users = ~50 active calculations
- 10-second average response time for complex scenarios
- Peak load handling with request queuing
- Database connection pooling for PostgreSQL

**Alternatives Considered**:
- 1000+ concurrent users: Overkill for MVP, premature optimization
- 10 concurrent users: Too limiting for multi-adviser firms
- No concurrency limits: Risk of system overload

### 4.2 Calculation Engine Optimization

**Decision**: Implement calculation result caching and parallel processing for independent entities.

**Rationale**:
- Success criteria SC-001/SC-002 require fast responses
- Caching reduces redundant calculations for similar scenarios
- Parallel processing leverages multi-core instances
- Memory-efficient data structures for large projections

**Optimization Techniques**:
- LRU cache for calculation results (TTL-based expiration)
- Parallel entity processing (household members, companies)
- Incremental calculations for scenario variations
- Pre-computed tax tables and rule lookups

**Alternatives Considered**:
- No caching: Poor performance for repeated calculations
- Single-threaded processing: Underutilizes server resources
- External calculation service: Adds complexity and latency

### 4.3 Database Optimization

**Decision**: PostgreSQL with JSONB storage, read replicas, and query optimization.

**Rationale**:
- JSONB storage aligns with flexible CalculationState requirements
- Read replicas support high-read workloads (scenario comparisons)
- Query optimization ensures fast scenario retrieval
- ACID compliance critical for financial data

**Database Architecture**:
- Primary write instance for scenario creation/updates
- Read replicas for calculation runs and comparisons
- JSONB indexes for state queries
- Partitioning for large scenario tables

**Alternatives Considered**:
- MongoDB: No ACID guarantees for financial calculations
- MySQL: Less flexible JSON handling than PostgreSQL
- In-memory only: No persistence for production use

---

## 5. Security Implementation

### 5.1 Authentication Implementation

**Decision**: Clerk-managed authentication with secure token handling.

**Rationale**:
- Clerk provides enterprise-grade auth security (MFA, session management, token refresh)
- Offloads token security complexity to managed provider
- Secure token storage and CSRF protection handled automatically
- Focuses development on core Engine logic instead of auth infrastructure

**Security Measures**:
- Clerk handles token expiration and refresh mechanisms
- Secure token storage (httpOnly cookies for web clients)
- CSRF protection for web endpoints
- Rate limiting on authentication endpoints via Clerk

**Alternatives Considered**:
- Custom JWT with RS256 signatures: Unnecessary complexity for MVP
- HS256 symmetric signing: Less secure than Clerk's implementation
- API key authentication: Insufficient for user-specific sessions
- OAuth 2.0 full flow: Overkill when Clerk provides auth as a service

### 5.2 Data Encryption

**Decision**: TLS 1.3 for transit, AES-256 for sensitive data at rest.

**Rationale**:
- TLS 1.3 provides modern transport security
- AES-256 is industry standard for data encryption
- Balances security with performance requirements
- Compliant with financial data protection standards

**Encryption Scope**:
- All API communications use TLS 1.3
- Sensitive PII encrypted in database
- Backup files encrypted
- End-to-end encryption for collaborative sessions

**Alternatives Considered**:
- TLS 1.2: Outdated security standards
- Database-level encryption only: Transit security gaps
- Client-side encryption: Complex key management

### 5.3 PII Handling and Anonymization

**Decision**: Minimal PII collection with pseudonymization for LLM interactions.

**Rationale**:
- Constitution principle: minimize PII sent to LLM
- Pseudonymization protects privacy while maintaining functionality
- GDPR/privacy regulation compliance
- Balances utility with privacy protection

**PII Handling**:
- Pseudonymized identifiers for LLM context
- Encrypted storage for sensitive personal data
- Data minimization (collect only necessary fields)
- Clear data retention policies

**Alternatives Considered**:
- No PII anonymization: Privacy regulation violations
- Full client-side processing: Complex and unreliable
- External anonymization service: Additional cost and complexity

---

## 6. Monitoring & Observability

### 6.1 Health Check Endpoints

**Decision**: Simple health checks with dependency validation per plan.md requirements.

**Rationale**:
- Success criteria SC-005 requires 99.9% availability
- Simple /health endpoint aligns with plan.md monitoring approach
- Dependency validation ensures system reliability
- Supports Render's health check requirements

**Health Check Components**:
- Database connectivity validation
- LLM provider availability
- Calculation engine responsiveness
- Clerk authentication service availability
- Disk space and memory monitoring

**Alternatives Considered**:
- Comprehensive health checks: Overkill for MVP per plan.md
- External monitoring only: No internal health validation
- No health checks: Poor operational visibility

### 6.2 Performance Monitoring

**Decision**: Sentry + Axiom/BetterStack integration with essential metrics per plan.md.

**Rationale**:
- Simple yet effective monitoring aligns with solo-developer constraints
- Sentry provides error tracking and performance insights
- Axiom/BetterStack handles log aggregation and alerting
- Minimal setup for full visibility per plan.md requirements

**Monitoring Stack**:
- Response time percentiles (p50, p95, p99)
- Error rates by endpoint and user type
- Calculation engine performance metrics
- Database query performance
- Memory and CPU utilization

**Alternatives Considered**:
- Full APM integration: Overkill for MVP scope
- External monitoring only: No application-specific metrics
- No performance monitoring: Blind operation

### 6.3 Audit Logging

**Decision**: Structured audit logs with compliance-focused retention.

**Rationale**:
- Success criteria SC-006 requires complete audit trails
- Regulatory compliance requires detailed logging
- Structured logs enable automated analysis
- Long retention periods for financial records

**Audit Log Scope**:
- All calculation executions with inputs/outputs
- User actions and scenario modifications
- Regulatory compliance checks and results
- System configuration changes
- Authentication and authorization events

**Alternatives Considered**:
- Minimal logging: Doesn't meet audit requirements
- External audit service: Additional complexity
- Short retention: Regulatory non-compliance risk

---

## 7. Data Quality Framework

### 7.1 Progressive Onboarding

**Decision**: Multi-stage onboarding with data quality scoring and guided completion.

**Rationale**:
- Functional requirement FR-010 requires progressive onboarding
- Data quality scoring provides clear completion indicators
- Guided completion improves user experience
- Supports incomplete data handling

**Onboarding Stages**:
1. Basic profile (name, age, residency)
2. Essential finances (income, major assets/liabilities)
3. Detailed breakdown (complete cashflow, all holdings)
4. Optimization ready (complete data for strategy analysis)

**Alternatives Considered**:
- All-or-nothing onboarding: Poor user experience
- No data quality indicators: Users unsure of completion status
- Mandatory complete data: High abandonment rates

### 7.2 Data Validation Rules

**Decision**: Pydantic models with business logic validation and contextual rules.

**Rationale**:
- Constitution requires validated inputs with Pydantic schemas
- Business logic validation catches domain-specific errors
- Contextual rules adapt to user type and jurisdiction
- Clear error messages guide data correction

**Validation Types**:
- Schema validation (required fields, data types)
- Business rules (income vs expense consistency)
- Cross-field validation (asset/liability balancing)
- Regulatory compliance checks

**Alternatives Considered**:
- Database constraints only: Limited validation expressiveness
- Application-level validation only: No data integrity guarantees
- No validation: Data quality and calculation errors

### 7.3 Missing Data Handling

**Decision**: Default values with transparency flags and sensitivity analysis.

**Rationale**:
- Supports progressive onboarding with incomplete data
- Transparency flags indicate estimated vs actual values
- Sensitivity analysis shows impact of missing data
- Maintains calculation accuracy where possible

**Missing Data Strategies**:
- Industry averages for missing rates/returns
- Conservative estimates for risk parameters
- Transparency flags in all outputs
- Sensitivity analysis for key metrics

**Alternatives Considered**:
- Require complete data: Poor user experience
- Skip calculations with missing data: Limited functionality
- No transparency: Users unaware of data quality issues

---

## 8. Educational Content Management

### 8.1 RAG Implementation

**Decision**: File-based RAG with simple vector search for MVP, pgvector for future scaling.

**Rationale**:
- Constitution specifies file-based knowledge storage for phases 1-3
- Simple implementation aligns with solo-developer constraints
- pgvector upgrade path for advanced RAG features
- Supports educational response requirements

**RAG Architecture**:
- Markdown files for legislation summaries and examples
- Simple keyword/tag-based retrieval for MVP
- Optional embedding generation for semantic search
- Citation tracking with source attribution

**Alternatives Considered**:
- Full pgvector from start: Overkill for MVP scope
- External RAG service: Additional cost and complexity
- No RAG: Poor educational response quality

### 8.2 Content Versioning

**Decision**: Git-based versioning with semantic versioning for regulatory content.

**Rationale**:
- Regulatory content requires strict version control
- Semantic versioning supports compliance tracking
- Git provides audit trail and rollback capabilities
- Aligns with constitution's specification-driven approach

**Versioning Strategy**:
- Major versions for regulatory changes
- Minor versions for content updates
- Patch versions for corrections
- Version metadata in all citations

**Alternatives Considered**:
- Database versioning: Complex schema management
- No versioning: Regulatory compliance issues
- Manual versioning: Error-prone process

### 8.3 Citation Tracking

**Decision**: Structured citation metadata with source validation.

**Rationale**:
- Success criteria SC-010 requires authoritative citations
- Structured metadata enables automated validation
- Source validation ensures citation accuracy
- Supports audit trail requirements

**Citation Structure**:
```json
{
  "source": "ATO",
  "document": "ITR 2025",
  "section": "4.2",
  "version": "2025-01-01",
  "url": "https://ato.gov.au/itrr",
  "last_verified": "2025-11-21"
}
```

**Alternatives Considered**:
- Free-text citations: Difficult to validate automatically
- No citation tracking: Doesn't meet authoritative requirements
- External citation service: Unnecessary complexity

---

## Implementation Recommendations

### Priority Implementation Order

1. **High Priority** (Week 1-2):
   - Clerk integration and RBAC setup
   - Core data models and validation
   - Basic calculation engine with audit trails

2. **Medium Priority** (Week 3-4):
   - TanStack Query optimistic UI setup
   - Manual data entry workflows (no bank feeds)
   - Sentry + Axiom/BetterStack monitoring

3. **Lower Priority** (Week 5-6):
   - Advanced RAG features
   - Full regulatory data integration
   - Enhanced monitoring capabilities

### Risk Mitigation

- **Security First**: Implement authentication and encryption early
- **Performance Testing**: Continuous performance validation during development
- **Compliance Focus**: Audit trails and regulatory checks built into core architecture
- **Scalability Planning**: Design for horizontal scaling from day one

### Success Metrics

- All NEEDS CLARIFICATION items resolved with documented decisions
- Architecture supports all success criteria
- Implementation complexity manageable for solo developer
- Regulatory compliance requirements met
- Performance targets achievable with chosen architecture
