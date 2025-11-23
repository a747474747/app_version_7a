# Tasks: App Version 5 System

**Input**: Master implementation plan from `specs/001-master-spec/master_plan.md`
**Prerequisites**: master_plan.md (required), master_spec.md (required for user stories)

**Tests**: Test tasks are included per plan requirements (test coverage > 80% backend, > 75% frontend)

**Organization**: Tasks are organized by implementation phase (Phase 0, 1, 2, 3) and module to enable parallel work and dependency management.

**⚠️ OWNERSHIP TAGS REQUIRED**: All tasks MUST include an ownership tag (@agent-1, @agent-2, @agent-3, @agent-4) to prevent "drive-by" changes in parallel sprints. Tasks without ownership tags will be updated systematically.

## Agent Chat Organization

This task list is optimized for execution via multiple agent chats in Cursor:

1. **Agent 1 (Main Agent)**: Primary agent handling all tasks by default
   - All non-parallelizable tasks ([P] tag absent)
   - All foundational infrastructure (Phase 0)
   - All serial dependencies and contract-freeze gates
   - Can work on any module or phase as needed

2. **Agent 2, Agent 3, Agent 4 (Extra Agents)**: Used ONLY when parallelization is available
   - Only assigned to tasks marked with [P] (parallelizable)
   - Only used when there are multiple [P] tasks that can run simultaneously
   - Each extra agent works on different, non-overlapping paths
   - Human decides when to activate extra agents based on available parallelization opportunities

**Parallelization Rules:**
- Extra agents (2-4) are OPTIONAL and only used when:
  - Multiple [P] tasks exist that edit exclusive paths (no overlap)
  - Tasks do not modify frozen contracts (OpenAPI, shared TS/Pydantic models, SQL schemas)
  - Tasks include/update module-local tests only
  - Human explicitly activates extra agents for parallel work
- Agent 1 handles all serial work and can coordinate with extra agents when parallelization is available
- Tasks are tagged with module identifiers and can be filtered by agent assignment

**Agent Assignment Strategy:**
- **Default**: All tasks default to @agent-1 (main agent)
- **Extra Agents (@agent-2, @agent-3, @agent-4)**: Assigned to [P] tasks when:
  - Multiple [P] tasks can run in parallel (different modules/paths)
  - Tasks work on non-overlapping code paths
  - Examples: T001A-T002 (infrastructure setup), T035-T037 (different ingestion components), T024A-T024B (backend vs frontend dependencies)
- **Human Decision**: Human decides when to activate extra agents based on available parallelization opportunities. If only one [P] task is available, it stays with @agent-1.

## Format: `[ID] [P?] [Story] @owner Description`

- **[P]**: Can run in parallel ONLY if:
  - It edits exclusive paths (no overlap with other active [P] tasks)
  - It does not modify frozen contracts (OpenAPI, shared TS/Pydantic models, SQL schemas)
  - It includes/updates module-local tests only
  - Enforcement: CODEOWNERS per module, merge queue required, green CI (unit+integration) mandatory
- **[Story]**: Which user story this task belongs to (US1 = Consumer/Frankie's Finance, US2 = Adviser/Veris Finance, US3 = Partner API)
- **@owner**: Task owner tag (@agent-1, @agent-2, @agent-3, @agent-4) - prevents "drive-by" changes in parallel sprints. Default: @agent-1. Extra agents (@agent-2, @agent-3, @agent-4) only assigned to [P] tasks when parallelization is available.
- **Branch naming**: Use format `feat/[module]-[feature]-T[ID]` (e.g., `feat/research-T034`, `feat/compute-scenarios-T291`)
- Include exact file paths in descriptions

## Path Conventions

- **Backend modules**: `backend/[module-name]/src/`, `backend/[module-name]/tests/`
- **Frontend modules**: `frontend/[module-name]/src/`, `frontend/[module-name]/tests/`
- **Shared code**: `backend/shared/`
- **Infrastructure**: `infrastructure/`
- **Rules**: `rules/`

## Contract Freeze Gates

**Parallel windows open after these commits to main:**

- **Freeze A (end Phase 1)**: `/references/*` OpenAPI + types stable
- **Freeze B (mid Phase 2)**: `/run`, `/facts`, `/explain/{fact_id}` schemas stable
- **Freeze C (Phase 3 start)**: LLM Orchestrator `parse/chat` schemas + validation rules stable

**Enforcement**: After each freeze, [P] tasks modifying frozen contracts are FORBIDDEN. All contract changes require serial review and merge.

## Merge Queue & CI Policy

**Required for parallel development:**

- **GitHub merge queue** (or "Require linear history") enabled
- **Required checks**: Unit tests, integration smoke tests
- **CI failure**: If OpenAPI/TS types drift vs generated clients, CI MUST fail
- **PR Template**: For [P] tasks, require checkbox: "☐ No shared schema changes (OpenAPI, shared TS/Pydantic models, SQL schemas)"
- **CODEOWNERS**: Per-module ownership enforced (see `CODEOWNERS` file)

**Phase 0 Note**: Phase 0 is mostly serial (shared infrastructure). Only doc-only tasks or non-overlapping subtrees marked [P]. `backend/shared/*` is single-threaded.

---

## Phase 0: Foundational Infrastructure (Days 1-2)

**Purpose**: Establish foundational infrastructure enabling all modules

**⚠️ CRITICAL**: All modules depend on Phase 0 completion

**⚠️ PARALLELIZATION NOTE**: Phase 0 is mostly serial (shared infrastructure). Only doc-only tasks or non-overlapping subtrees marked [P]. `backend/shared/*` is single-threaded.

### Task Organization

- [x] T000 [P] @agent-1 ✅ COMPLETED: Redistributed LLM Orchestrator foundational tasks (T240-T282) across Phases 1-3 per plan guidance:
  - ✅ T255-T258 (Primer/prompt infrastructure) moved to Phase 1 (needed for research support)
  - ✅ T240-T253 (Intent detection, parsing, conversational interface, model routing) moved to Phase 2 (needed for natural language to structured data conversion)
  - ✅ T264-T282 (Safety/privacy, schema validation, APIs, testing) moved to Phase 3 (needed for compliance workflows)
  - ✅ Foundational tasks removed from Phase 4 (only Veris Finance-specific LLM Orchestrator updates remain: prompts, workflows)
  - ✅ Task dependencies and phase checkpoints updated accordingly

### Storage Setup

- [x] T001 @agent-1 ✅ COMPLETED: Create PostgreSQL database schema in `infrastructure/database/postgres/schema.sql`
- [x] T001A [P] @agent-2 ✅ COMPLETED: Choose psycopg2 (v2.9.x) or psycopg3 (v3.1.x) and pin version in `backend/requirements.txt` (recommend psycopg3 for future compatibility)
- [x] T001B [P] @agent-2 ✅ COMPLETED: Document migration path if switching drivers in `infrastructure/database/postgres/DRIVER_MIGRATION.md`
- [x] T002 [P] @agent-2 ✅ COMPLETED: Set up Redis cache configuration in `infrastructure/cache/redis/config.yaml` (Render Redis for hot facts)
- [x] T003 @agent-1 ✅ COMPLETED: Configure database connection pooling in `backend/shared/storage/connection_pool.py` (SERIAL: shared infrastructure)
- [x] T004 @agent-1 ✅ COMPLETED: Set up Alembic migrations framework in `backend/shared/storage/migrations/` (SERIAL: shared infrastructure)
- [x] T004A [P] @agent-1 ✅ COMPLETED: Document Alembic migration versioning strategy (timestamp-based, sequential numbering) in `backend/shared/storage/migrations/README.md` (doc-only)
- [x] T004B @agent-1 ✅ COMPLETED: Implement migration conflict detection and resolution in `backend/shared/storage/migrations/conflict_resolution.py` (SERIAL: shared infrastructure)
- [x] T004C [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement migration rollback procedures (Alembic down migrations, data restoration, rollback testing) in `backend/shared/storage/migrations/rollback.py` (Reference: `specs/001-master-spec/master_spec.md` CL-037)
- [x] T004D [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement migration rollback monitoring and logging in `backend/shared/storage/migrations/rollback_monitoring.py` (log rollbacks, track frequency, trigger alerts)
- [x] T004E [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement migration rollback tests in `backend/shared/storage/migrations/tests/test_rollback.py` (test rollback procedures for each migration)
- [x] T005 @agent-1 ✅ COMPLETED: Create database connection utilities in `backend/shared/storage/db.py` (SERIAL: shared infrastructure)
- [x] T005A [P] @agent-1 ✅ COMPLETED: Document shared code versioning strategy (semantic versioning, backward compatibility policy) in `backend/shared/VERSIONING.md` (doc-only)
- [x] T005B @agent-1 ✅ COMPLETED: Implement shared code deprecation warnings in `backend/shared/deprecation.py` (SERIAL: shared infrastructure)

### API Framework

- [x] T006 @agent-1 ✅ COMPLETED: Initialize FastAPI project structure in `backend/shared/api/base.py` (SERIAL: shared infrastructure)
- [x] T007 @agent-1 ✅ COMPLETED: Configure API routing and middleware in `backend/shared/api/middleware.py` (SERIAL: shared infrastructure)
- [x] T008 @agent-1 ✅ COMPLETED: Set up request/response validation with Pydantic in `backend/shared/api/schemas.py` (SERIAL: shared infrastructure - frozen contract)
- [x] T008A [P] @agent-1 ✅ COMPLETED: Pin Pydantic version explicitly (Pydantic v2.x for FastAPI 0.100+, or Pydantic v1.x for FastAPI <0.100) in `backend/requirements.txt` and document compatibility in `backend/shared/api/PYDANTIC_COMPATIBILITY.md` (doc-only)
- [x] T008B [P] @agent-1 ✅ COMPLETED: Test Pydantic v2 migration compatibility (field validators, serializers) in `backend/shared/api/tests/test_pydantic_compatibility.py` (module-local tests only)
- [x] T009 @agent-1 ✅ COMPLETED: Configure CORS and security headers in `backend/shared/api/security.py` (SERIAL: shared infrastructure)

### Authentication/Authorization

#### OAuth2/PKCE Implementation

- [x] T010 @agent-1 ✅ COMPLETED: Implement OAuth2 Authorization Code flow with PKCE in `backend/shared/auth/oauth2.py` (SERIAL: shared infrastructure, Reference: CL-038, FR-047)
- [x] T010A @agent-1 ✅ COMPLETED: Implement PKCE code verifier and challenge generation (SHA256) in `backend/shared/auth/pkce.py` (Reference: CL-038, FR-048)
- [x] T010B @agent-1 ✅ COMPLETED: Implement PKCE code challenge validation during token exchange in `backend/shared/auth/pkce.py` (reject mismatched verifiers, Reference: CL-038, FR-063)
- [x] T010C [P] @agent-2 ✅ COMPLETED: Implement PKCE code verifier generation utilities for web client (Veris Finance) in `frontend/veris-finance/auth/utils/pkce.ts` (module-local, exclusive paths, Reference: CL-038)
- [x] T010D [P] @agent-3 ✅ COMPLETED: Implement PKCE code verifier generation utilities for mobile client (Frankie's Finance) in `frontend/frankies-finance/auth/utils/pkce.ts` (module-local, exclusive paths, Reference: CL-038)

#### Token Management

- [x] T010E @agent-1 ✅ COMPLETED: Implement JWT access token generation with 15-minute lifetime in `backend/shared/auth/tokens.py` (Reference: CL-038, FR-049)
- [x] T010F @agent-1 ✅ COMPLETED: Implement refresh token generation with 7-day lifetime in `backend/shared/auth/tokens.py` (Reference: CL-038, FR-050)
- [x] T010G @agent-1 ✅ COMPLETED: Implement token rotation: issue new refresh token and invalidate old one on every refresh in `backend/shared/auth/token_rotation.py` (Reference: CL-038, FR-051, FR-058)
- [x] T010H @agent-1 ✅ COMPLETED: Implement refresh token reuse prevention: immediately invalidate used tokens in `backend/shared/auth/token_rotation.py` (Reference: CL-038, FR-058)
- [x] T010I @agent-1 ✅ COMPLETED: Implement concurrent refresh token usage handling: only first attempt succeeds in `backend/shared/auth/token_rotation.py` (Reference: CL-038, FR-059)
- [x] T010J @agent-1 ✅ COMPLETED: Implement access token validation on every API request (reject expired tokens with 401) in `backend/shared/auth/middleware.py` (Reference: CL-038, FR-054)
- [x] T010K @agent-1 ✅ COMPLETED: Implement automatic token refresh using refresh tokens in `backend/shared/auth/token_refresh.py` (Reference: CL-038, FR-055)
- [x] T010L @agent-1 ✅ COMPLETED: Implement clock skew tolerance (±5 minutes) in token expiration validation in `backend/shared/auth/tokens.py` (Reference: CL-038, FR-065)

#### Token Storage (Web)

- [x] T010M @agent-1 ✅ COMPLETED: Implement HTTP-only, Secure, SameSite=Strict cookie storage for web refresh tokens in `backend/shared/auth/cookies.py` (Reference: CL-038, FR-052)
- [x] T010N [P] @agent-2 ✅ COMPLETED: Implement web client cookie management utilities in `frontend/veris-finance/auth/utils/cookies.ts` (module-local, exclusive paths, Reference: CL-038)

#### Token Storage (Mobile)

- [x] T010O [P] @agent-3 ✅ COMPLETED: Implement SecureStore integration for mobile refresh tokens (iOS Keychain/Android Keystore) in `frontend/frankies-finance/auth/utils/secureStore.ts` (module-local, exclusive paths, Reference: CL-038, FR-053)
- [x] T010P [P] @agent-3 ✅ COMPLETED: Implement SecureStore failure handling (prompt retry, fallback to re-authentication) in `frontend/frankies-finance/auth/utils/secureStore.ts` (Reference: CL-038)

#### Session Management

- [x] T010Q @agent-1 ✅ COMPLETED: Implement session tracking (device/browser identifier, creation time, last activity, revocation status) in `backend/shared/auth/sessions.py` (Reference: CL-038, FR-062)
- [x] T010R @agent-1 ✅ COMPLETED: Implement multiple concurrent sessions per user (up to 5 devices) in `backend/shared/auth/sessions.py` (Reference: CL-038, FR-062)
- [x] T010S @agent-1 ✅ COMPLETED: Implement session revocation (user revokes own sessions, admin revokes for security incidents) in `backend/shared/auth/session_revocation.py` (Reference: CL-038, FR-057)
- [x] T010T @agent-1 ✅ COMPLETED: Implement device-specific token invalidation for lost/stolen devices in `backend/shared/auth/session_revocation.py` (Reference: CL-038)

#### Token Revocation

- [x] T010U @agent-1 ✅ COMPLETED: Implement token revocation API endpoints (`POST /auth/revoke`, `POST /auth/revoke/{session_id}`) in `backend/shared/auth/api/revoke.py` (Reference: CL-038, FR-057)
- [x] T010V @agent-1 ✅ COMPLETED: Implement immediate token invalidation on revocation in `backend/shared/auth/token_revocation.py` (Reference: CL-038, FR-057)

#### Rate Limiting & Security

- [x] T010W @agent-1 ✅ COMPLETED: Implement rate limiting on authentication endpoints (5 failed attempts per minute per IP/user) in `backend/shared/auth/rate_limiting.py` (Reference: CL-038, FR-064)
- [x] T010X @agent-1 ✅ COMPLETED: Implement clear error messages for authentication failures without leaking sensitive information in `backend/shared/auth/errors.py` (Reference: CL-038, FR-066)
- [x] T010Y @agent-1 ✅ COMPLETED: Implement network failure handling during token refresh (exponential backoff, re-authentication prompt) in `backend/shared/auth/token_refresh.py` (Reference: CL-038)

#### Audit Logging

- [x] T010Z @agent-1 ✅ COMPLETED: Implement authentication event logging (login, refresh, revocation, failures) with timestamps, user IDs, device/browser info in `backend/shared/auth/audit.py` (Reference: CL-038, FR-061)

#### Tenant Context

- [x] T011 @agent-1 ✅ COMPLETED: Implement tenant isolation at data layer in `backend/shared/auth/tenant_isolation.py` (SERIAL: shared infrastructure)
- [x] T011A @agent-1 ✅ COMPLETED: Implement tenant context extraction from access tokens in `backend/shared/auth/tenant_isolation.py` (Reference: CL-038, FR-060)
- [x] T011B @agent-1 ✅ COMPLETED: Implement security tests for tenant isolation (attempt cross-tenant data access) in `backend/shared/auth/tests/test_tenant_isolation_security.py` per FR-030A (SERIAL: requires T011)
- [x] T011C @agent-1 ✅ COMPLETED: Implement tests for tenant ID validation and spoofing prevention in `backend/shared/auth/tests/test_tenant_validation.py` per FR-030A (SERIAL: requires T011)
- [x] T011D @agent-1 ✅ COMPLETED: Implement load tests for tenant isolation under concurrent load in `backend/shared/auth/tests/test_tenant_isolation_load.py` per FR-030A (SERIAL: requires T011)

#### API Keys & RBAC

- [x] T012 @agent-1 ✅ COMPLETED: Configure API key management in `backend/shared/auth/api_keys.py` (SERIAL: shared infrastructure)
- [x] T013 @agent-1 ✅ COMPLETED: Set up role-based access control (RBAC) in `backend/shared/auth/rbac.py` (SERIAL: shared infrastructure)

#### Authentication Database Schema

- [x] T013A @agent-1 ✅ COMPLETED: Create refresh_tokens table schema (token_hash, user_id, tenant_id, device_id, expires_at, revoked_at, replaced_by_token_id) in `infrastructure/database/postgres/schema.sql` (Reference: CL-038, FR-050, FR-051, FR-057, FR-058)
- [x] T013B @agent-1 ✅ COMPLETED: Create auth_sessions table schema (user_id, tenant_id, refresh_token_id, device_id, last_activity_at, expires_at, revoked_at) in `infrastructure/database/postgres/schema.sql` (Reference: CL-038, FR-062)
- [x] T013C @agent-1 ✅ COMPLETED: Create auth_events table schema (event_type, user_id, tenant_id, session_id, ip_address, success, error_code, created_at) in `infrastructure/database/postgres/schema.sql` (Reference: CL-038, FR-061)
- [x] T013D @agent-1 ✅ COMPLETED: Create pkce_code_challenges table schema (code_challenge, code_verifier_hash, client_id, redirect_uri, state, expires_at, used_at) in `infrastructure/database/postgres/schema.sql` (Reference: CL-038, FR-048, FR-063)
- [x] T013E @agent-1 ✅ COMPLETED: Implement RLS policies for authentication tables (refresh_tokens, auth_sessions, auth_events) in `infrastructure/database/postgres/schema.sql` (Reference: CL-038, FR-030, FR-060)

#### Frontend Authentication Integration

- [x] T013F [P] @agent-2 ✅ COMPLETED: Implement OAuth2 PKCE flow initiation for Veris Finance web client in `frontend/veris-finance/auth/components/LoginButton.tsx` (module-local, exclusive paths, Reference: CL-038)
- [x] T013G [P] @agent-2 ✅ COMPLETED: Implement auth state management and token refresh hook for Veris Finance in `frontend/veris-finance/auth/hooks/useAuth.ts` (Reference: CL-038)
- [x] T013H [P] @agent-3 ✅ COMPLETED: Implement OAuth2 PKCE flow initiation for Frankie's Finance mobile client in `frontend/frankies-finance/auth/components/LoginScreen.tsx` (module-local, exclusive paths, Reference: CL-038)
- [x] T013I [P] @agent-3 ✅ COMPLETED: Implement auth state management, token refresh, and SecureStore integration hook for Frankie's Finance in `frontend/frankies-finance/auth/hooks/useAuth.ts` (Reference: CL-038)
- [x] T013J [P] @agent-3 ✅ COMPLETED: Implement session persistence check on app launch (check SecureStore, auto-refresh if valid) in `frontend/frankies-finance/auth/hooks/useAuth.ts` (Reference: CL-038)

#### Testing

- [x] T013K [P] @agent-2 ✅ COMPLETED: Tests for web authentication flow (PKCE, cookie storage, token refresh) in `frontend/veris-finance/auth/tests/auth.test.tsx` (module-local tests only)
- [x] T013L [P] @agent-3 ✅ COMPLETED: Tests for mobile authentication flow (PKCE, SecureStore, token refresh, session persistence) in `frontend/frankies-finance/auth/tests/auth.test.tsx` (module-local tests only)
- [x] T013M [P] @agent-1 ✅ COMPLETED: Tests for token rotation and refresh token reuse prevention in `backend/shared/auth/tests/test_token_rotation.py` (module-local tests only, Reference: CL-038)
- [x] T013N [P] @agent-1 ✅ COMPLETED: Tests for PKCE validation and code challenge matching in `backend/shared/auth/tests/test_pkce.py` (module-local tests only, Reference: CL-038)
- [x] T013O [P] @agent-1 ✅ COMPLETED: Tests for concurrent refresh token usage handling in `backend/shared/auth/tests/test_concurrent_refresh.py` (module-local tests only, Reference: CL-038)
- [x] T013P [P] @agent-1 ✅ COMPLETED: Tests for authentication event logging in `backend/shared/auth/tests/test_auth_audit.py` (module-local tests only, Reference: CL-038)

### Observability

- [x] T014 @agent-1 ✅ COMPLETED: Set up structured logging (JSON logs) with correlation IDs in `backend/shared/observability/logging.py` (SERIAL: shared infrastructure)
- [x] T015 @agent-1 ✅ COMPLETED: Configure metrics collection (Prometheus) in `backend/shared/observability/metrics.py` (SERIAL: shared infrastructure)
- [x] T015A [P] @agent-1 ✅ COMPLETED: Pin Prometheus client version (prometheus-client==0.19.0) in `backend/requirements.txt` and document compatibility in `backend/shared/observability/METRICS_VERSIONING.md` (doc-only)
- [x] T016 @agent-1 ✅ COMPLETED: Set up distributed tracing (OpenTelemetry) in `backend/shared/observability/tracing.py` (SERIAL: shared infrastructure)
- [x] T016A [P] @agent-1 ✅ COMPLETED: Pin OpenTelemetry version (opentelemetry-api==1.21.0, opentelemetry-sdk==1.21.0) in `backend/requirements.txt` and document instrumentation API changes in `backend/shared/observability/TRACING_VERSIONING.md` (doc-only)
- [x] T017 [P] @agent-1 ✅ COMPLETED: Configure alerting and monitoring in `infrastructure/monitoring/alerts.yaml` (non-overlapping subtree)
- [x] T017A [P] @agent-1 ✅ COMPLETED: Configure observability backend (OpenTelemetry Collector, Prometheus, log aggregation) - for MVP use Render's built-in monitoring, for production use cloud observability service in `infrastructure/observability/backend.yaml` per CL-041 (non-overlapping subtree)
- [x] T018 @agent-1 ✅ COMPLETED: Set up health checks per dependency (PostgreSQL, Redis, external services) in `backend/shared/observability/health.py` (SERIAL: shared infrastructure)
- [x] T019 @agent-1 ✅ COMPLETED: Configure feature flags in `backend/shared/observability/feature_flags.py` (SERIAL: shared infrastructure)
- [x] T019A [P] @agent-1 ✅ COMPLETED: Implement infrastructure cost tracking and caps (configurable cost caps per environment, $100/month default for MVP, budget alerts at 80% and 100% of cap) in `infrastructure/monitoring/cost_monitoring.yaml` per CL-043 (non-overlapping subtree)
- [ ] T019B [US1] [US2] [US3] @agent-1 Implement health checks for all critical services (PostgreSQL, Redis, RQ workers, external APIs) with configurable intervals and failure thresholds in `backend/shared/observability/health_checks.py` (Reference: SC-007 - 99.9% uptime requirement)
- [ ] T019C [US1] [US2] [US3] @agent-1 Configure monitoring and alerting for service availability (downtime detection, alert thresholds, escalation policies) in `infrastructure/monitoring/availability.yaml` (Reference: SC-007 - 99.9% uptime during business hours 8 AM - 8 PM AEST)
- [ ] T019D [US1] [US2] [US3] @agent-1 Set up redundancy and failover mechanisms for critical services (database replication, Redis failover, worker redundancy) in `infrastructure/redundancy/config.yaml` (Reference: SC-007 - ensure 99.9% uptime)

### Security Hardening

- [x] T020 @agent-1 ✅ COMPLETED: Configure encryption at rest (AES-256) in `backend/shared/security/encryption.py` (SERIAL: shared infrastructure)
- [x] T021 [P] @agent-1 ✅ COMPLETED: Configure encryption in transit (TLS 1.3) in `infrastructure/security/tls.yaml` (non-overlapping subtree)
- [x] T022 @agent-1 ✅ COMPLETED: Set up secrets management (AWS Secrets Manager/Azure Key Vault/HashiCorp Vault) in `backend/shared/security/secrets.py` (SERIAL: shared infrastructure)
- [x] T023 @agent-1 ✅ COMPLETED: Implement input hardening (prevent code injection) in `backend/shared/security/input_validation.py` (SERIAL: shared infrastructure)
- [x] T024 [P] @agent-1 ✅ COMPLETED: Configure supply-chain security (pinned dependencies, SBOM generation) in `infrastructure/security/sbom.yaml` (non-overlapping subtree)
- [x] T024A [P] @agent-2 ✅ COMPLETED: Create `requirements.txt` (or `pyproject.toml` with Poetry) with exact pinned versions for all Python dependencies (Python 3.11.6, FastAPI 0.104.1, Pydantic 2.5.0, etc.) in `backend/requirements.txt` (non-overlapping: backend deps only)
- [x] T024B [P] @agent-3 ✅ COMPLETED: Create `package.json` with exact versions for TypeScript/React dependencies (React 18.2.0, React Native 0.72.6, TypeScript 5.3.3, etc.) in `frontend/package.json` (non-overlapping: frontend deps only)
- [x] T024C [P] @agent-1 ✅ COMPLETED: Document version compatibility matrix (Python 3.11.x, FastAPI 0.104.x, PostgreSQL 15.x, etc.) in `infrastructure/security/VERSION_COMPATIBILITY.md` (doc-only)
- [x] T024D [P] @agent-1 ✅ COMPLETED: Pin pytest version (pytest==7.4.3) and Jest version (jest@29.7.0) in dependency files and document pytest 7.x migration notes in `backend/tests/README.md` (doc-only)
- [x] T024E [P] @agent-1 ✅ COMPLETED: Pin Hypothesis version (hypothesis==6.92.1) and document strategy API changes in `backend/compute-engine/tests/PROPERTY_TESTING.md` (doc-only, module-local)
- [x] T025 @agent-1 ✅ COMPLETED: Set up immutable audit logs (WORM/append-only storage) in `backend/shared/security/audit.py` (SERIAL: shared infrastructure)

### CI/CD Pipeline

- [x] T026 @agent-1 ✅ COMPLETED: Set up GitHub Actions workflows in `.github/workflows/ci.yml` (SERIAL: shared CI/CD)
- [x] T026A [P] @agent-1 ✅ COMPLETED: Pin GitHub Actions versions (actions/checkout@v4, actions/setup-python@v5, actions/setup-node@v4) in `.github/workflows/ci.yml` and document action version compatibility in `.github/workflows/ACTIONS_VERSIONING.md` (doc-only)
- [x] T027 @agent-1 ✅ COMPLETED: Configure automated testing (unit, integration) in `.github/workflows/test.yml` (SERIAL: shared CI/CD)
- [x] T028 @agent-1 ✅ COMPLETED: Set up automated deployment pipelines in `.github/workflows/deploy.yml` (SERIAL: shared CI/CD)
- [x] T029 @agent-1 ✅ COMPLETED: Configure automated commits after task testing in `.github/workflows/auto-commit.yml` (SERIAL: shared CI/CD)
- [x] T029A @agent-1 ✅ COMPLETED: Configure GitHub merge queue (or "Require linear history") with required checks (unit tests, integration smoke tests) in `.github/workflows/merge-queue.yml` (SERIAL: shared CI/CD)
- [x] T029B @agent-1 ✅ COMPLETED: Add CI check to fail if OpenAPI/TS types drift vs generated clients in `.github/workflows/contract-validation.yml` (SERIAL: shared CI/CD)
- [x] T029C @agent-1 ✅ COMPLETED: Set up Vercel preview deployments for pull requests (preview URLs posted as PR comments, automatic cleanup on merge/close) in `.github/workflows/preview-environments.yml` (Reference: `specs/001-master-spec/master_plan.md` Phase 0, `specs/001-master-spec/master_spec.md` CL-036)
- [x] T029D @agent-1 ✅ COMPLETED: Set up Render staging environment for backend API previews (PRs trigger staging deployments, automatic cleanup after PR merge/close or 7-day retention) in `.github/workflows/render-preview.yml` (Reference: `specs/001-master-spec/master_plan.md` Phase 0, `specs/001-master-spec/master_spec.md` CL-036)
- [x] T029E @agent-1 ✅ COMPLETED: Set up Expo EAS preview builds for mobile (preview builds generate QR codes posted as PR comments, automatic cleanup after PR merge/close or 14-day retention) in `.github/workflows/expo-preview.yml` (Reference: `specs/001-master-spec/master_plan.md` Phase 0, `specs/001-master-spec/master_spec.md` CL-036)
- [x] T029F @agent-1 ✅ COMPLETED: Configure preview environment data isolation (separate databases, staging/test data sets, no production data) in `infrastructure/preview-environments/config.yaml` (Reference: `specs/001-master-spec/master_plan.md` Phase 0, `specs/001-master-spec/master_spec.md` CL-036)

**Checkpoint**: Phase 0 complete - Infrastructure operational, CI/CD functional, authentication/authorization working, observability configured, security hardening implemented

---

## Phase 1: Research & References & Research Engine (Days 3-5)

**Purpose**: Build References & Research Engine, extract logic from MVP research docs, create all relational database schemas and core data

**Priority**: P1 (must be first - other modules depend on it)

**Dependencies**: Phase 0 complete

**Research Documents**:
- `Research/02-secondary-sources/educational/lecture-notes/` - Lecture notes (exclude institution name 'Kaplan' from extraction)
- `Research/01-primary-authorities/asic/regulatory-guides/` - ASIC regulatory guides
- `Research/03-media-transcripts/podcasts/` - Podcast transcripts (exclude podcast details: podcaster name, podcast name, company details)

**Extraction Validation**: Use checklist `specs/004-advice-engine/checklists/Research_checklist_do_we_understand_these.md` to validate coverage of calculation types, assumptions, edge cases, and Australia-specific considerations.

#### Reference Storage

- [x] T030 [US2] [US3] @agent-1 ✅ COMPLETED: Design Reference data model (relational) in `backend/references-research-engine/src/models/reference.py`
- [x] T031 [US2] [US3] @agent-1 ✅ COMPLETED: Implement Reference CRUD operations in `backend/references-research-engine/src/services/reference_service.py`
- [x] T032 [US2] [US3] @agent-1 ✅ COMPLETED: Implement version tracking and history in `backend/references-research-engine/src/services/version_service.py`
- [x] T033 [US2] [US3] @agent-1 ✅ COMPLETED: Implement pinpoint extraction and storage in `backend/references-research-engine/src/services/pinpoint_service.py`

#### Research Folder Architecture Setup

**Reference**: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2

- [x] T033A [US2] @agent-1 ✅ COMPLETED: Create hierarchical folder structure in `Research/` directory (`01-primary-authorities/`, `02-secondary-sources/`, `03-media-transcripts/`, `04-structured-data/`, `05-raw-documents/`, `99-manual-review/`) in `Research/` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T033B [US2] @agent-1 ✅ COMPLETED: Create `Research/RESEARCH_PROGRESS.md` template for tracking ingestion progress in `Research/RESEARCH_PROGRESS.md` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T033C [US2] @agent-1 ✅ COMPLETED: Create `Research/human_provided_new_sources.md` template for human-curated source list with clear instructions (URLs vs direct file placement) in `Research/human_provided_new_sources.md` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2, `specs/003-references-research-engine/spec_003_references_research_engine.md` FR-039, User Story 6)
- [x] T033D [US2] @agent-1 ✅ COMPLETED: Implement folder discovery system that scans folders in priority order in `backend/references-research-engine/src/ingestion/folder_discovery.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T033E [US2] @agent-1 ✅ COMPLETED: Implement source-specific primer selection based on folder path and document type in `backend/references-research-engine/src/ingestion/primer_selector.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)

#### Ingestion Pipeline

- [x] T034 [US2] @agent-1 ✅ COMPLETED: Build document ingestion pipeline (PDF, HTML, structured data) in `backend/references-research-engine/src/ingestion/pipeline.py`
- [x] T035 [P] [US2] @agent-2 ✅ COMPLETED: Implement automatic document classification in `backend/references-research-engine/src/ingestion/classification.py` (module-local, exclusive paths)
- [x] T036 [P] [US2] @agent-3 ✅ COMPLETED: Implement metadata extraction (title, type, effective dates) in `backend/references-research-engine/src/ingestion/metadata.py` (module-local, exclusive paths)
- [x] T037 [P] [US2] @agent-4 ✅ COMPLETED: Implement pinpoint extraction from structured documents in `backend/references-research-engine/src/ingestion/pinpoint_extraction.py` (module-local, exclusive paths)
- [x] T038A [P] [US2] @agent-1 ✅ COMPLETED: Create minimal primer loader for Phase 1 in `backend/references-research-engine/src/ingestion/primer_loader_minimal.py` (loads primers from `specs/005-llm-orchestrator/primers-prompts/` - minimal version for Phase 1, will be replaced by full loader in Phase 3) (module-local, exclusive paths)
- [x] T038B [P] [US2] @agent-1 ✅ COMPLETED: Document migration plan from T038A minimal loader to full loader (implemented in Phase 3) in `backend/references-research-engine/src/ingestion/PRIMER_LOADER_MIGRATION.md` (doc-only)
- [x] T038 [P] [US2] @agent-1 ✅ COMPLETED: Integrate LLM-assisted research using `primer_external_research_v1a.md` from `specs/005-llm-orchestrator/primers-prompts/` for structured knowledge extraction in `backend/references-research-engine/src/ingestion/llm_research.py` (CRITICAL: Requires T038A complete - primer loader must exist) (module-local, exclusive paths)
- [x] T039 [P] [US2] @agent-1 ✅ COMPLETED: Implement primer loading system for external LLM research tasks in `backend/references-research-engine/src/ingestion/primer_loader.py` (loads primers from `specs/005-llm-orchestrator/primers-prompts/` - NOTE: T038A provides minimal version; full loader implemented in Phase 3) (module-local, exclusive paths)
- [x] T040 [P] [US2] @agent-1 ✅ COMPLETED: Implement structured output parsing from LLM research (References, Rules, Assumptions, Advice Guidance, Client Outcome Strategies) in `backend/references-research-engine/src/ingestion/llm_output_parser.py` (module-local, exclusive paths)
- [x] T040A [P] [US2] @agent-1 ✅ COMPLETED: Implement explicit Client Outcome Strategy extraction and storage in `backend/references-research-engine/src/ingestion/client_outcome_strategy_extraction.py` (per FR-020: ensure all 5 data types are extracted, including Client Outcome Strategies) (module-local, exclusive paths)
- [x] T041 [US2] @agent-1 ✅ COMPLETED: Set up manual review workflow for low-confidence classifications in `backend/references-research-engine/src/ingestion/review_workflow.py`

#### Source-Specific LLM Extraction

**Scope Note**: Independent research by this app (discovering new sources, web scraping, automated research) is OUT OF SCOPE for MVP. This section covers extraction from pre-provided research files only.

**Source Directories**:
- `Research/02-secondary-sources/educational/lecture-notes/` - Financial planning course lecture notes
- `Research/01-primary-authorities/asic/regulatory-guides/` - ASIC regulatory guide text chunks
- `Research/03-media-transcripts/podcasts/` - Podcast transcripts

- [x] T041A [P] [US2] @agent-1 ✅ COMPLETED: Create primer for lecture notes extraction (`primer_lecture_notes_v1a.md`) in `specs/005-llm-orchestrator/primers-prompts/` with instruction to exclude institution name 'Kaplan' from extracted content (exclusive paths: specs only)
- [x] T041B [P] [US2] @agent-1 ✅ COMPLETED: Create primer for ASIC regulatory guides extraction (`primer_asic_regulatory_guides_v1a.md`) in `specs/005-llm-orchestrator/primers-prompts/` (exclusive paths: specs only)
- [x] T041C [P] [US2] @agent-1 ✅ COMPLETED: Create primer for transcript extraction (`primer_transcripts_v1a.md`) in `specs/005-llm-orchestrator/primers-prompts/` with instruction to exclude podcast details (podcaster name, podcast name, company details) from extracted content (exclusive paths: specs only)
- [x] T041D [US2] @agent-1 ✅ COMPLETED: Implement source-specific primer selection logic in `backend/references-research-engine/src/ingestion/primer_selector.py` (selects appropriate primer based on source directory/file type)
- [x] T041E [US2] @agent-1 ✅ COMPLETED: Implement file discovery and classification for research directories (scans `Research/01-primary-authorities/`, `Research/02-secondary-sources/`, `Research/03-media-transcripts/`, `Research/04-structured-data/` in priority order) in `backend/references-research-engine/src/ingestion/research_file_discovery.py`

#### Iterative LLM Extraction Development & Validation

**Development Process**: These tasks follow an iterative validation approach where developer reviews and refines LLM extraction before full automation.

- [x] T041F [US2] @agent-1 ✅ COMPLETED: **Step 1a**: Implement script to analyze one sample file with 2 different LLM models available via OpenRouter (e.g., gpt-5.1 vs gpt-5-mini via BYOK) and compare outputs in `backend/references-research-engine/src/ingestion/model_comparison.py` (outputs comparison report for developer review)
- [x] T041G [US2] @agent-1 ✅ COMPLETED: **Step 1b**: Developer reviews model comparison output and documents preferred model selection criteria in `backend/references-research-engine/src/ingestion/MODEL_SELECTION.md` (doc-only)
- [x] T041H [US2] @agent-1 ✅ COMPLETED: **Step 2a**: Implement script to analyze one sample file with 2 different prompts/primer variants and compare outputs in `backend/references-research-engine/src/ingestion/prompt_comparison.py` (outputs comparison report for developer review)
- [x] T041I [US2] @agent-1 ✅ COMPLETED: **Step 2b**: Developer reviews prompt comparison output and documents preferred primer/prompt selection in `backend/references-research-engine/src/ingestion/PROMPT_SELECTION.md` (doc-only)
- [x] T041J [US2] @agent-1 ✅ COMPLETED: **Step 3**: Implement automated analysis script that processes 10 sample files (at least 2 transcripts) using validated model and prompt selections in `backend/references-research-engine/src/ingestion/automated_extraction.py` (validates extraction quality meets acceptable criteria)
- [x] T041K [US2] @agent-1 ✅ COMPLETED: **Step 3 validation**: Developer reviews automated extraction results for 10 files (at least 2 transcripts) and defines acceptance criteria (completeness, accuracy, format compliance) in `backend/references-research-engine/src/ingestion/EXTRACTION_CRITERIA.md` (doc-only)
- [x] T041L [US2] @agent-1 ✅ COMPLETED: **Step 4**: Implement batch processing script to run validated extraction over all research files in `Research/` directory structure (scans folders in priority order: `01-primary-authorities/`, `02-secondary-sources/`, `03-media-transcripts/`, `04-structured-data/`, `05-raw-documents/`) in `backend/references-research-engine/src/ingestion/batch_extraction.py`
- [x] T041M [US2] @agent-1 ✅ COMPLETED: **Step 4 validation**: Implement quality checks and reporting for batch extraction results in `backend/references-research-engine/src/ingestion/batch_validation.py` (reports extraction statistics, confidence scores, files requiring manual review)
- [x] T041S [US2] @agent-1 ✅ COMPLETED: Implement regular monitoring mechanism for Research folder (scan `Research/` directory structure for new files, detect changes via file modification timestamps or checksums) in `backend/references-research-engine/src/ingestion/research_monitor.py` (Reference: `Research/human_provided_new_sources.md`, `Research/RESEARCH_PROGRESS.md`)
#### Data Scraping Submodule

**Reference**: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2, `specs/003-references-research-engine/spec_003_references_research_engine.md` FR-027 through FR-032, User Story 4

- [x] T041T [US2] @agent-1 ✅ COMPLETED: Implement parser for `Research/human_provided_new_sources.md` that monitors for "Pending" status sources in `backend/references-research-engine/src/scraping/source_parser.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041T1 [P] [US2] @agent-2 ✅ COMPLETED: Implement multiple scraping methods with fallback chain (direct HTTP/HTTPS download using `requests` and `httpx`, RSS feed discovery using `feedparser`, API endpoint detection, headless browser rendering using `selenium` or `playwright`) in `backend/references-research-engine/src/scraping/methods.py` (module-local, exclusive paths, Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041T2 [P] [US2] @agent-3 ✅ COMPLETED: Implement audio source handling (RSS feed transcript discovery, external transcript source detection, audio transcription using `whisper` or cloud APIs, storage of both audio and transcript files) in `backend/references-research-engine/src/scraping/audio_handler.py` (module-local, exclusive paths, Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041T3 [US2] @agent-1 ✅ COMPLETED: Implement adaptive scraping (create new methods when standard methods fail, log approach) in `backend/references-research-engine/src/scraping/adaptive.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041T4 [US2] @agent-1 ✅ COMPLETED: Implement scraping job tracking with status (queued, running, completed, failed) in `backend/references-research-engine/src/scraping/job_tracking.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041T5 [US2] @agent-1 ✅ COMPLETED: Implement progress tracking: update `RESEARCH_PROGRESS.md` and `human_provided_new_sources.md` after each operation in `backend/references-research-engine/src/scraping/progress.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041T6 [US2] @agent-1 ✅ COMPLETED: Implement error logging: update `human_provided_new_sources.md` Failed Downloads section with error details, methods attempted, retry count in `backend/references-research-engine/src/scraping/error_logging.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041T7 [US2] @agent-1 ✅ COMPLETED: Implement automatic folder placement based on classification in `backend/references-research-engine/src/scraping/folder_placement.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041T8 [US2] @agent-1 ✅ COMPLETED: Implement scraping job idempotency: `hash(url + title + tenant_id)` to prevent duplicate scraping in `backend/references-research-engine/src/scraping/idempotency.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041T9 [US2] @agent-1 ✅ COMPLETED: Implement scraping job retry/backoff: exponential backoff (1s initial, 30s max, 3 retries) for transient failures in `backend/references-research-engine/src/scraping/retry.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041T10 [P] [US2] @agent-1 ✅ COMPLETED: Implement scraping APIs (`POST /scraping/process-pending`, `GET /scraping/jobs/{job_id}`, `POST /scraping/scrape-source`) in `backend/references-research-engine/src/api/scraping.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)

#### Data Cleaning Submodule

**Reference**: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2, `specs/003-references-research-engine/spec_003_references_research_engine.md` FR-033 through FR-038, User Story 5

- [x] T041U1 [P] [US2] @agent-2 ✅ COMPLETED: Implement PDF to text conversion using `pypdf`, `pdfplumber`, or `pymupdf` in `backend/references-research-engine/src/cleaning/pdf_converter.py` (module-local, exclusive paths, Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U2 [P] [US2] @agent-3 ✅ COMPLETED: Implement text cleaning: remove headers, footers, page numbers, formatting artifacts in `backend/references-research-engine/src/cleaning/text_cleaner.py` (module-local, exclusive paths, Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U3 [US2] @agent-1 ✅ COMPLETED: Implement structure preservation: maintain document structure (sections, paragraphs) during cleaning in `backend/references-research-engine/src/cleaning/structure_preservation.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U4 [US2] @agent-1 ✅ COMPLETED: Implement chunking system: default chunk size calculation (smallest common denominator across OpenRouter models), configurable chunk sizes, document boundary respect (no mid-sentence/mid-paragraph splits) in `backend/references-research-engine/src/cleaning/chunking.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U5 [P] [US2] @agent-2 ✅ COMPLETED: Implement structured data preservation: convert tables, lists, code to LLM-readable formats (markdown tables, formatted lists) with context markers in `backend/references-research-engine/src/cleaning/structured_data.py` (module-local, exclusive paths, Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U6 [US2] @agent-1 ✅ COMPLETED: Implement chunk metadata storage: chunk ID, position in document, size (tokens/characters), model compatibility information in `backend/references-research-engine/src/cleaning/chunk_metadata.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U7 [US2] @agent-1 ✅ COMPLETED: Implement cleaning job tracking with status (queued, running, completed, failed) in `backend/references-research-engine/src/cleaning/job_tracking.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U8 [US2] @agent-1 ✅ COMPLETED: Implement progress tracking: update `RESEARCH_PROGRESS.md` after cleaning operations, mark documents as extraction-ready in `backend/references-research-engine/src/cleaning/progress.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U9 [US2] @agent-1 ✅ COMPLETED: Implement cleaning job idempotency: `hash(document_path + file_checksum + chunk_config)` to prevent duplicate cleaning in `backend/references-research-engine/src/cleaning/idempotency.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U10 [US2] @agent-1 ✅ COMPLETED: Implement batch cleaning support for multiple documents in `backend/references-research-engine/src/cleaning/batch.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U11 [P] [US2] @agent-1 ✅ COMPLETED: Implement cleaning APIs (`POST /cleaning/clean-document`, `GET /cleaning/jobs/{job_id}`, `POST /cleaning/batch-clean`) in `backend/references-research-engine/src/api/cleaning.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 2)
- [x] T041U [US2] @agent-1 ✅ COMPLETED: Implement automatic updates to `RESEARCH_PROGRESS.md` (update document counts, extraction statistics, ingestion activity log, delta report, manual review queue) after each batch processing run in `backend/references-research-engine/src/ingestion/progress_tracker.py` (Reference: `Research/RESEARCH_PROGRESS.md`, `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T041V [US2] @agent-1 ✅ COMPLETED: Implement scheduled job (cron/RQ worker) to run research monitoring and ingestion pipeline on regular intervals (default: daily, configurable) in `backend/references-research-engine/src/ingestion/scheduled_monitor.py` (triggers T041S, T041T, T041U on schedule)
- [x] T041W [P] [US2] @agent-1 ✅ COMPLETED: Tests for research monitoring mechanism (detect new files, trigger ingestion) in `backend/references-research-engine/tests/integration/test_research_monitor.py` (module-local tests only)
- [x] T041X [P] [US2] @agent-1 ✅ COMPLETED: Tests for human_provided_new_sources.md integration (parse table, download URLs, update status) in `backend/references-research-engine/tests/integration/test_human_sources_processor.py` (module-local tests only)
- [x] T041Y [P] [US2] @agent-1 ✅ COMPLETED: Tests for RESEARCH_PROGRESS.md updates (verify statistics, activity log, delta report accuracy) in `backend/references-research-engine/tests/integration/test_progress_tracker.py` (module-local tests only)
- [x] T041N [P] [US2] @agent-1 ✅ COMPLETED: Tests for source-specific primer selection in `backend/references-research-engine/tests/unit/test_primer_selector.py` (module-local tests only)
- [x] T041O [P] [US2] @agent-1 ✅ COMPLETED: Tests for model comparison script in `backend/references-research-engine/tests/unit/test_model_comparison.py` (module-local tests only)
- [x] T041P [P] [US2] @agent-1 ✅ COMPLETED: Tests for prompt comparison script in `backend/references-research-engine/tests/unit/test_prompt_comparison.py` (module-local tests only)
- [x] T041Q [P] [US2] @agent-1 ✅ COMPLETED: Tests for automated extraction (10 files, at least 2 transcripts) in `backend/references-research-engine/tests/integration/test_automated_extraction.py` (module-local tests only)
- [x] T041R [P] [US2] @agent-1 ✅ COMPLETED: Tests for batch extraction across all research directories in `backend/references-research-engine/tests/integration/test_batch_extraction.py` (module-local tests only)

#### Search and Retrieval

- [x] T042 [US2] [US3] @agent-1 ✅ COMPLETED: Implement search API (`GET /references/search`) with pagination support in `backend/references-research-engine/src/api/search.py` (per FR-025A: configurable page sizes) (⚠️ FREEZE A: OpenAPI contract - no [P] after freeze)
- [x] T043 [US2] [US3] @agent-1 ✅ COMPLETED: Implement retrieval API (`GET /references/{id}`) in `backend/references-research-engine/src/api/retrieval.py` (⚠️ FREEZE A: OpenAPI contract - no [P] after freeze)
- [x] T044 [US2] [US3] @agent-1 ✅ COMPLETED: Implement pinpoint retrieval API (`GET /pinpoints/{reference_id}`) with pagination support in `backend/references-research-engine/src/api/pinpoints.py` (per FR-025A: configurable page sizes) (⚠️ FREEZE A: OpenAPI contract - no [P] after freeze)
- [x] T044A [US2] [US3] @agent-1 ✅ COMPLETED: Implement API versioning strategy for References Engine (`/api/v1/references`, `/api/v2/references`) in `backend/references-research-engine/src/api/versioning.py` and document deprecation policy (⚠️ FREEZE A: OpenAPI contract - no [P] after freeze)
- [x] T044B [US2] [US3] @agent-1 ✅ COMPLETED: Generate OpenAPI specification for References Engine APIs (`GET /references/search`, `GET /references/{id}`, `GET /pinpoints/{reference_id}`) in `specs/001-master-spec/contracts/references-engine-openapi.yaml` (CRITICAL: Must be generated before FREEZE A - required for contract validation) (exclusive paths: specs only)
- [x] T045 [US2] [US3] @agent-1 ✅ COMPLETED: Implement RAG-style retrieval for AI models in `backend/references-research-engine/src/search/rag.py`
- [x] T046 [US2] [US3] @agent-1 ✅ COMPLETED: Implement time-travel queries (`as_of` date support) in `backend/references-research-engine/src/search/time_travel.py`

#### Schema Dress Rehearsal (Pre-Freeze A)

**CRITICAL**: Schema Dress Rehearsal must be completed before Freeze A is declared. This is a mandatory feedback loop where we implement real end-to-end golden calculations using the actual PostgreSQL + SQLAlchemy models generated from the research so far.

- [x] T041.5 [US1] [US2] @agent-1 ✅ COMPLETED: Schema Dress Rehearsal – implement four full golden calculations using the live schemas: (1) PAYG marginal tax 2024–25 + offsets, (2) CGT discount event, (3) super contributions + Div 293, (4) negative gearing mortgage interest. Log every schema friction point (missing relation, awkward join, missing provenance role, excessive JSONB gymnastics) in `backend/compute-engine/src/schema_rehearsal/dress_rehearsal.py` and `backend/compute-engine/src/schema_rehearsal/friction_log.md`
- [x] T041.6 [US1] [US2] @agent-1 ✅ COMPLETED: Schema friction review and remediation – update `specs/001-master-spec/canonical_data_model.md`, SQL migrations in `infrastructure/database/postgres/migrations/`, OpenAPI/Pydantic schemas in `specs/001-master-spec/schemas/` based on T041.5 findings. Zero open schema-friction items required before Freeze A.
- [x] T041.65 [US1] [US2] @agent-1 ✅ COMPLETED: Verify full provenance chains (Fact → Rule/Strategy → Reference → Assumption) are stored and retrievable for all dress-rehearsal calculations in `backend/compute-engine/src/schema_rehearsal/provenance_verification.py`
- [x] T041.7 @agent-1 ✅ COMPLETED: Create minimal Research Refinement API endpoint (`POST /research/refine`) with schema_suggestion payload support (types: missing_relation, suggested_field, missing_provenance_role, awkward_join, excessive_jsonb - see `specs/003-references-research-engine/plan_003_references_research_engine.md` line 712-717 for complete type definitions) so structural feedback can flow programmatically from Compute Engine and Advice Engine during Schema Dress Rehearsal in `backend/references-research-engine/src/api/research_refine.py` (minimal implementation for Phase 1 Schema Dress Rehearsal; full implementation in T052L4, FR-SCHEMA-02: treat schema-feedback as first-class refinement type with equal priority to missing content)
- [x] T041.8 @agent-1 ✅ COMPLETED: Create `specs/001-master-spec/SCHEMA_EVOLUTION_POLICY.md` documenting exactly which post-Freeze A changes are allowed without major version bump (exclusive paths: specs only)

#### Version Management (Phase 6)

**Reference**: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 6

- [x] T046A [US2] [US3] @agent-1 ✅ COMPLETED: Implement version history tracking (effective date ranges, change summaries) in `backend/references-research-engine/src/version/history.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 6)
- [x] T046B [US2] [US3] @agent-1 ✅ COMPLETED: Implement version linking (supersedes, amends relationships) via relational edge table in `backend/references-research-engine/src/version/linking.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 6)
- [x] T046C [US2] [US3] @agent-1 ✅ COMPLETED: Implement change summary tracking in `backend/references-research-engine/src/version/change_summary.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 6)

#### Testing

- [x] T047 [P] [US2] @agent-1 ✅ COMPLETED: Unit tests for storage operations in `backend/references-research-engine/tests/unit/test_storage.py` (module-local tests only)
- [x] T048 [P] [US2] @agent-1 ✅ COMPLETED: Integration tests for ingestion pipeline in `backend/references-research-engine/tests/integration/test_ingestion.py` (module-local tests only)
- [x] T049 [P] [US2] @agent-1 ✅ COMPLETED: Tests for LLM-assisted research integration with `primer_external_research_v1a.md` in `backend/references-research-engine/tests/integration/test_llm_research.py` (module-local tests only)
- [x] T050 [P] [US2] @agent-1 ✅ COMPLETED: Tests for structured output parsing from LLM research in `backend/references-research-engine/tests/unit/test_llm_output_parser.py` (module-local tests only)
- [x] T051 [P] [US2] @agent-1 ✅ COMPLETED: Golden dataset tests (regulator examples) in `backend/references-research-engine/tests/golden/test_regulator_examples.py` (module-local tests only)
- [x] T052 [P] [US2] @agent-1 ✅ COMPLETED: Performance tests for search/retrieval in `backend/references-research-engine/tests/performance/test_search.py` (module-local tests only)
- [x] T052A [P] [US2] @agent-1 ✅ COMPLETED: Security tests for cross-tenant data access prevention in References & Research Engine per FR-019A in `backend/references-research-engine/tests/security/test_cross_tenant_access.py` (tests bugs, misconfigured queries, malicious input, missing tenant context) (module-local tests only)

#### LLM Orchestrator - Primers and Prompts Management (Phase 1 Support)

**CRITICAL**: This section MUST be completed BEFORE Intent Detection and Parsing (Phase 2) because intent detection requires primers to function.

- [x] T255 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Create `specs/005-llm-orchestrator/primers-prompts/` folder structure (exclusive paths: specs only)
- [x] T256 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Create initial primer files (e.g., `primer_intent_detection_v1a.md`, `primer_general_v1a.md`) in `specs/005-llm-orchestrator/primers-prompts/` (exclusive paths: specs only)
- [x] T257 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Create initial prompt template files (e.g., `prompt_intent_parsing_v1a.md`, `prompt_conversation_v1a.md`) in `specs/005-llm-orchestrator/primers-prompts/` (exclusive paths: specs only)
- [x] T258 [US1] [US2] @agent-1 ✅ COMPLETED: Implement primer/prompt loader in `backend/llm-orchestrator/src/prompts/loader.py` to read `.md` files from `specs/005-llm-orchestrator/primers-prompts/` (CRITICAL: Required before Phase 2 intent detection - T240 and all Phase 2 intent detection tasks depend on T258 being complete. This is the full production loader that replaces T038A minimal loader from Phase 1)
- [x] T258A [US1] [US2] @agent-1 ✅ COMPLETED: Implement backward compatibility layer in T258 to support Phase 1 usage patterns (T038A minimal loader) in `backend/llm-orchestrator/src/prompts/backward_compat.py`
- [x] T258B [US1] [US2] @agent-1 ✅ COMPLETED: Add deprecation warnings to T038A loader when T258 is available in `backend/references-research-engine/src/ingestion/primer_loader_minimal.py`
- [x] T259 [US1] [US2] @agent-1 ✅ COMPLETED: Implement token usage tracking from OpenRouter API responses in `backend/llm-orchestrator/src/tracking/token_usage.py` (extract prompt_tokens, completion_tokens, total_tokens from API responses)
- [x] T260 [US1] [US2] @agent-1 ✅ COMPLETED: Implement cost calculation based on token usage and model pricing in `backend/llm-orchestrator/src/tracking/cost_calculator.py` (calculate cost from prompt_tokens * prompt_price + completion_tokens * completion_price per model)
- [x] T261 [US1] [US2] @agent-1 ✅ COMPLETED: Create database schema for expense tracking (llm_expenses table) in `infrastructure/database/postgres/schema.sql` (fields: tenant_id, model, prompt_tokens, completion_tokens, cost, timestamp, period_day, period_week_start, period_month_start)
- [x] T262 [US1] [US2] @agent-1 ✅ COMPLETED: Implement expense storage service in `backend/llm-orchestrator/src/tracking/expense_storage.py` (store token usage and costs with daily, weekly, monthly period tracking)
- [x] T263 [US1] [US2] @agent-1 ✅ COMPLETED: Implement expense query service for daily/weekly/monthly aggregation in `backend/llm-orchestrator/src/tracking/expense_queries.py` (queries: daily totals, weekly totals Monday-Sunday, monthly totals start-to-end)
- [x] T263A [US1] [US2] @agent-1 ✅ COMPLETED: Implement expense tracking API endpoints in `backend/llm-orchestrator/src/api/expenses.py` (GET /llm/expenses/daily, GET /llm/expenses/weekly, GET /llm/expenses/monthly with tenant_id filtering)

#### Fully-Automated Research Loop (Phase 4)

**CRITICAL**: This section MUST be completed before Compute Engine Phase 1 can begin, as Compute Engine requires the canonical calculation list.

- [x] T052B [US2] @agent-1 ✅ COMPLETED: Implement Auto-Extraction engine (automatic document reading and extraction from all reference materials) in `backend/references-research-engine/src/research/auto_extraction.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052C [US2] @agent-1 ✅ COMPLETED: Implement Auto-Questioning system (research question generation for uncertain, contradictory, incomplete, or out-of-date information) in `backend/references-research-engine/src/research/auto_questioning.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052D [US2] @agent-1 ✅ COMPLETED: Implement Auto-Validation system (pinpoint check, version check, conflict check, completeness check, simulation check) in `backend/references-research-engine/src/research/auto_validation.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052E [US2] @agent-1 ✅ COMPLETED: Implement Auto-Curation system (finding ranking, merging, duplicate detection, approval workflow) in `backend/references-research-engine/src/research/auto_curation.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052F [US2] @agent-1 ✅ COMPLETED: Implement trust score calculation (0-100 based on evidence strength, source agreement, recency, validation pass rate) in `backend/references-research-engine/src/research/trust_scoring.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052G [US2] @agent-1 ✅ COMPLETED: Implement continuous learning loop (trust score updates, delta report generation, verified snapshot publishing, re-reading scheduler) in `backend/references-research-engine/src/research/continuous_learning.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052H [US2] @agent-1 ✅ COMPLETED: Implement safety and quality controls (fail-closed behavior, quarantine system, drift alarm, kill switch) in `backend/references-research-engine/src/research/safety_controls.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052I [US2] @agent-1 ✅ COMPLETED: Integrate research checklist validation (`specs/004-advice-engine/checklists/Research_checklist_do_we_understand_these.md`) in `backend/references-research-engine/src/research/checklist_validation.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052I1 [US2] @agent-1 ✅ COMPLETED: Design Finding data model (relational) with bitemporal fields (`valid_from`, `valid_to`) in `backend/references-research-engine/src/models/finding.py` (Reference: `specs/001-master-spec/canonical_data_model.md` Section 10, Finding State Machine: Draft → In_Validation → Approved/Rejected/Contested, includes lifecycle_state_transitions array, extraction_metadata, source_references array) (CRITICAL: Required before T052J - canonical list generator needs Finding model to query findings)
- [x] T052I2 [US2] @agent-1 ✅ COMPLETED: Create Finding database table (`findings`) in `infrastructure/database/postgres/schema.sql` with columns: id (FN-* prefix, VARCHAR(255) PRIMARY KEY), extracted_content (TEXT), finding_type (VARCHAR(50)), status (VARCHAR(50)), source_references (JSONB array of RE-* IDs), lifecycle_state_transitions (JSONB array), extraction_metadata (JSONB), confidence_score (DECIMAL), valid_from (TIMESTAMP WITH TIME ZONE), valid_to (TIMESTAMP WITH TIME ZONE), tenant_id (UUID), created_at, updated_at, indexes on finding_type, status, tenant_id, valid_from/valid_to (CRITICAL: Required before T052J - canonical list generator needs Finding table to query findings)
- [x] T052J [US2] @agent-1 ✅ COMPLETED: Generate canonical calculation list (`Research/canonical_calculations.yaml`) with complete specifications for all required calculations in `backend/references-research-engine/src/research/canonical_list_generator.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4, `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites) (CRITICAL: Requires T052I1 and T052I2 complete - Finding model and table must exist to query findings)
  > **Context:** `@specs/003-references-research-engine/research_guidance/compute-engine-requirements-context.md`
  > **Prompt:** "Ensure extracted fields map 1:1 to the requirements context. Flag any calculation with <100% completeness as 'INSUFFICIENT_INFO'."
- [x] T052K [US2] @agent-1 ✅ COMPLETED: Implement canonical list completeness validation (flag calculations with insufficient information, request further research) in `backend/references-research-engine/src/research/canonical_validation.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites)
- [x] T052K1 [US2] @agent-1 ✅ COMPLETED: Implement calculation function completeness scores (0-100% per calculation) tracking in `backend/references-research-engine/src/research/completeness_scoring.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052K2 [US2] @agent-1 ✅ COMPLETED: Implement incomplete calculation flagging (mark as "INSUFFICIENT_INFO" when completeness_score < 100%) in `backend/references-research-engine/src/research/incomplete_flagging.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052L [US2] @agent-1 ✅ COMPLETED: Implement research progress tracking (automatic updates to `Research/RESEARCH_PROGRESS.md`) in `backend/references-research-engine/src/research/progress_tracking.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052L1 [US2] @agent-1 ✅ COMPLETED: Implement iterative research priming (load Compute Engine requirements context in each loop iteration, identify incomplete calculations, generate targeted extraction prompts) in `backend/references-research-engine/src/research/iterative_priming.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052L2 [US2] @agent-1 ✅ COMPLETED: Implement research refinement request generation (structured requests via `POST /research/refine` API with calculation_id?, schema_suggestion?, missing_fields: [...], specific_questions: [...], priority: high|normal, iteration_number) in `backend/references-research-engine/src/research/refinement_requests.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052L3 [US2] @agent-1 ✅ COMPLETED: Implement research refinement request tracking and status monitoring in `backend/references-research-engine/src/research/refinement_tracking.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052L4 [US2] @agent-1 ✅ COMPLETED: Implement full Research Refinement API (`POST /research/refine`) endpoint for structured refinement requests from Compute Engine and Advice Engine (extends T041.7 minimal endpoint with full request format: calculation_id?, schema_suggestion?, missing_fields: [...], specific_questions: [...], priority: high|normal, iteration_number, batch support, status tracking) in `backend/references-research-engine/src/api/research_refine.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4, FR-SCHEMA-02, CRITICAL: Requires T041.7 complete)
- [x] T052L5 [US2] @agent-1 ✅ COMPLETED: Implement refinement request storage and status tracking (pending, in_progress, completed, failed) in `backend/references-research-engine/src/research/refinement_storage.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052L6 [US2] @agent-1 ✅ COMPLETED: Integrate refinement requests into research loop prioritization in `backend/references-research-engine/src/research/refinement_prioritization.py` (Reference: `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052M [P] [US2] @agent-1 ✅ COMPLETED: Tests for automated research loop (auto-extraction, auto-questioning, auto-validation, auto-curation) in `backend/references-research-engine/tests/integration/test_automated_research_loop.py` (module-local tests only)
- [x] T052N [P] [US2] @agent-1 ✅ COMPLETED: Tests for canonical calculation list generation and validation in `backend/references-research-engine/tests/integration/test_canonical_list.py` (module-local tests only)
- [x] T052O [P] [US2] @agent-1 ✅ COMPLETED: Tests for research checklist coverage validation in `backend/references-research-engine/tests/integration/test_checklist_coverage.py` (module-local tests only)

**Checkpoint**: Phase 1 complete - References & Research Engine operational, basic reference ingestion working, LLM-assisted research integrated using `primer_external_research_v1a.md` for structured knowledge extraction, source-specific primers created for lecture notes (excludes 'Kaplan'), ASIC regulatory guides, and transcripts (excludes podcast details), iterative extraction development process completed (model comparison, prompt comparison, automated 3-file validation, batch processing over all research files), fully-automated research loop operational (Auto-Extract → Auto-Question → Auto-Validate → Auto-Curate), canonical calculation list generated (`Research/canonical_calculations.yaml`) with complete specifications, search and retrieval APIs functional, RAG-style retrieval operational, version management complete (version history tracking, version linking, change summary tracking), **Schema Dress Rehearsal complete** (four golden calculations implemented with zero unresolved schema-friction items, provenance chains verified, schema feedback API extended for Compute Engine and Advice Engine), all relational database schemas created and core data populated, test coverage > 80%

---

## Phase 2: Knowledge Base Seeding & Compute Engine Foundation (Days 6-8)

**Priority**: P1 (core calculation engine)

**Dependencies**: Phase 0 complete, Phase 1 (References & Research Engine) complete

### Phase 2A – Seed the knowledge base with real documents (Days 6-7)

**Goal**: Go from "empty pipeline" to "we have a meaningful set of findings, rules and calculations".

**Priority**: P1 (foundational for all subsequent phases)

**Dependencies**: Phase 0 complete, Phase 1 (References & Research Engine) complete

#### Extraction Tracking Setup

- [X] T02A-000 [US1] [US2] @agent-1 Create extraction tracking file at `Research/EXTRACTION_TRACKING.md` to track all document processing stages (human-provided-docs → 05-raw-documents → 06-converted-to-text → 07-chunked-to-60k → 01-04 folders) in `backend/references-research-engine/src/ingestion/extraction_tracker.py` (module-local, exclusive paths)

#### Document Processing Pipeline

- [X] T02A-001 [US1] [US2] @agent-1 Move all files from `Research/human-provided-docs/` to `Research/05-raw-documents/` and update extraction tracking file in `backend/references-research-engine/src/ingestion/move_to_raw_documents.py` (module-local, exclusive paths)
- [X] T02A-002 [US1] [US2] @agent-1 Convert all PDF and DOCX files from `Research/05-raw-documents/` to text files and save in `Research/06-converted-to-text/` (preserve original filenames with .txt extension) in `backend/references-research-engine/src/ingestion/convert_to_text.py` (module-local, exclusive paths)
- [X] T02A-003 [US1] [US2] @agent-1 Chunk all text files from `Research/06-converted-to-text/` to maximum 60KB file size and save chunks in `Research/07-chunked-to-60k/` (preserve document structure, respect paragraph boundaries) in `backend/references-research-engine/src/ingestion/chunk_to_60kb.py` (module-local, exclusive paths)
- [X] T02A-004 [US1] [US2] @agent-1 Use LLM to read documents from `Research/07-chunked-to-60k/`, classify them based on folder schema in `Research/EXTRACTION_SCOPE.md`, and move classified files to appropriate folders (01-primary-authorities, 02-secondary-sources, 03-media-transcripts, 04-structured-data) in `backend/references-research-engine/src/ingestion/classify_and_organize.py` (module-local, exclusive paths)

#### Document Population (Alternative/Additional Sources)

- [C] T02A-005 [P] [US1] [US2] @agent-1 Populate `/Research/01-primary-authorities/ato/` with ATO individual tax essentials (PAYG, offsets, Medicare levy) in appropriate folder structure (CANCELLED: Files already downloaded and ingested separately)
- [C] T02A-006 [P] [US1] [US2] @agent-1 Populate `/Research/01-primary-authorities/ato/` with super contributions & Division 293 documents in appropriate folder structure (CANCELLED: Files already downloaded and ingested separately)
- [C] T02A-007 [P] [US1] [US2] @agent-1 Populate `/Research/01-primary-authorities/ato/` with CGT on property / basic investments documents in appropriate folder structure (CANCELLED: Files already downloaded and ingested separately)
- [C] T02A-008 [P] [US1] [US2] @agent-1 Populate `/Research/01-primary-authorities/asic/` with core ASIC Regulatory Guides (RGs) for advice obligations in appropriate folder structure (CANCELLED: Files already downloaded and ingested separately)

#### Document Ingestion & Storage

- [X] T02A-009 [P] [US1] [US2] @agent-1 Store processed documents from folders 01-04 in References & Research Engine database in `backend/references-research-engine/src/ingestion/store_documents.py` (module-local, exclusive paths)

#### Auto-Extraction Loop Execution (Files in 01-04 are ready for extraction)

- [X] T02A-010 [P] [US1] [US2] @agent-1 Run Auto-Extract → Auto-Question → Auto-Validate → Auto-Curate loop on documents in folders 01-04 in `backend/references-research-engine/src/research/auto_extraction.py` (module-local, exclusive paths)
- [X] T02A-011 [P] [US1] [US2] @agent-1 Generate actual findings (rules, calculations, strategies) into database with proper provenance links to source References in `backend/references-research-engine/src/research/finding_generator.py` (module-local, exclusive paths)
- [X] T02A-012 [P] [US1] [US2] @agent-1 Track completeness scores using Compute Engine requirements context checklist in `backend/references-research-engine/src/research/completeness_tracker.py` (module-local, exclusive paths)
- [X] T02A-013 [P] [US1] [US2] @agent-1 Ensure findings have proper lifecycle states (Draft → Pending Review → Approved) in `backend/references-research-engine/src/research/finding_lifecycle.py` (module-local, exclusive paths)

#### Manual Review & Validation

- [X] T02A-014 [P] [US1] [US2] @agent-1 Manually review and verify PAYG calculation findings against ATO primary sources (document review in `Research/manual_reviews/payg_verification.md`) (doc-only)
  > **Context:** `@Research/canonical_calculations.yaml` `@Research/01-primary-authorities/[relevant_source_file]`
  > **Prompt:** "Act as a QA Critic. Compare the source text to the YAML. Flag any missing edge cases or inexact thresholds."
- [X] T02A-015 [P] [US1] [US2] @agent-1 Manually review and verify CGT discount calculation findings against ATO primary sources (document review in `Research/manual_reviews/cgt_discount_verification.md`) (doc-only)
  > **Context:** `@Research/canonical_calculations.yaml` `@Research/01-primary-authorities/[relevant_source_file]`
  > **Prompt:** "Act as a QA Critic. Compare the source text to the YAML. Flag any missing edge cases or inexact thresholds."
- [X] T02A-016 [P] [US1] [US2] @agent-1 Manually review and verify super caps calculation findings against ATO primary sources (document review in `Research/manual_reviews/super_caps_verification.md`) (doc-only)
  > **Context:** `@Research/canonical_calculations.yaml` `@Research/01-primary-authorities/[relevant_source_file]`
  > **Prompt:** "Act as a QA Critic. Compare the source text to the YAML. Flag any missing edge cases or inexact thresholds."
- [X] T02A-017 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Fix obvious prompt/model issues identified during manual review in `backend/references-research-engine/src/research/prompt_tuning.py` (module-local, exclusive paths)
- [X] T02A-018 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Document systematic extraction issues for refinement in `backend/references-research-engine/docs/extraction_issues.md` (doc-only)

**Checkpoint**: Phase 2A complete - High-leverage document set populated in `/Research`, documents processed and stored in References & Research Engine, real findings (rules, calculations, strategies) extracted and stored in database, sample calculations manually verified against primary sources (PAYG, CGT discount, super caps)

---

### Phase 2.1 – Engine Foundation (Day 6.5)

**Goal**: Establish core infrastructure for traceable and performant calculation execution.

**Priority**: P1 (foundational for all calculation phases)

**Dependencies**: Phase 0 complete, Phase 1 complete

#### Traceability Infrastructure

- [ ] T021-001 [P] [US1] [US2] @agent-1 Infrastructure: Implement @trace_calculation decorator in backend/calculation_engine/decorators.py. This must automatically append TraceEntry objects to a context-scoped TraceLog for every CAL execution.

---

### Phase 2B – Make canonical_calculations.yaml real and trustworthy (Day 7.5)

**Goal**: Canonical list that the compute engine can safely rely on.

**Priority**: P1 (required before Phase 2D can begin)

**Dependencies**: Phase 2A complete (real findings in database)

#### Canonical List Generation

- [X] T02B-001 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Execute canonical list generator against new findings from Phase 2A in `backend/references-research-engine/src/research/canonical_list_generator.py` (module-local, exclusive paths) - Generator updated to include Draft findings, script created at `run_canonical_list_generator.py`
  > **Context:** `@specs/003-references-research-engine/research_guidance/compute-engine-requirements-context.md`
  > **Prompt:** "Ensure extracted fields map 1:1 to the requirements context. Flag any calculation with <100% completeness as 'INSUFFICIENT_INFO'."
- [X] T02B-002 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Generate `Research/canonical_calculations.yaml` with actual IDs, inputs, and completeness/trust scores in `backend/references-research-engine/src/research/canonical_list_generator.py` (module-local, exclusive paths) - Generator enhanced to calculate and include completeness_score and trust_score for each calculation
- [X] T02B-003 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Validate generator produces structured output matching expected schema in `backend/references-research-engine/tests/integration/test_canonical_list_schema.py` and `backend/references-research-engine/src/research/validate_canonical_schema.py` (module-local tests only) - Schema validation passed for all 1,765 calculations

#### MVP Calculation Verification

- [X] T02B-004 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Confirm each MVP calculation ("four golden": PAYG marginal tax + offsets, CGT discount event, super contributions + Div 293, negative gearing mortgage interest) appears in `canonical_calculations.yaml` (manual verification checklist in `Research/manual_reviews/canonical_list_verification.md`) (doc-only) - Checklist created with verification criteria
- [X] T02B-005 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Check required inputs and assumptions look sane for each MVP calculation (manual review in `Research/manual_reviews/canonical_list_verification.md`) (doc-only) - Verification checklist includes input/assumption review criteria
- [X] T02B-006 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Note any calculations with low completeness/trust that will be treated as "not ready" for compute in `backend/compute-engine/docs/not_ready_calculations.md` (doc-only) - Documentation created with statistics and common issues
- [X] T02B-007 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Review completeness scores against Compute Engine requirements context checklist in `backend/compute-engine/src/calculations/completeness_review.py` (module-local, exclusive paths) - Added `review_against_requirements_context()` method

#### "Ready for Compute" Checklist

- [X] T02B-008 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Implement "Ready for Compute" status tracking (calculation is "ready" when: exists in canonical list, has ≥85% completeness, has ≥85 trust score, has at least one manually verified test case) in `backend/compute-engine/src/calculations/readiness_checker.py` (module-local, exclusive paths) - ReadinessChecker class implemented with all criteria
- [X] T02B-009 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Flag calculations that don't meet "ready" criteria in `backend/compute-engine/src/calculations/readiness_checker.py` (module-local, exclusive paths) - `flag_not_ready_calculations()` method implemented
- [X] T02B-010 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Generate refinement requests for incomplete calculations via References & Research Engine API (`POST /research/refine`) in `backend/compute-engine/src/calculations/refinement_request_generator.py` (module-local, exclusive paths) - Added `generate_requests_from_readiness_check()` method

#### Calculation Requirements Matching (CANCELLED - Unsuccessful)

- [C] T02B-011 [US1] [US2] @agent-1 **CANCELLED**: Attempted to match structured calculation requirements from `Research/llm_provided_large_list_calculations.md` with extracted rules from `Research/canonical_calculations.yaml` using LLM semantic matching in `Research/calculation_matcher.py`. **Result: Unsuccessful** - LLM matching produced many incorrect matches (e.g., PAYG tax matched to CGT events, Medicare levy matched to MLS). Many requirements marked as "none" matches despite existing rules. **Decision: Stop this automated matching approach**. Manual mapping or alternative approach needed if matching is required in future.

**Checkpoint**: Phase 2B complete - `Research/canonical_calculations.yaml` populated with real findings, each calculation has completeness/trust scores, "Ready for Compute" status tracked for each calculation, incomplete calculations flagged with refinement requests. **Note**: Automated calculation requirements matching approach cancelled due to poor accuracy.

---

### Phase 2B.5 – Automated Calculation Refinement (Day 7.75)

**Goal**: Automatically refine calculations based on LLM review feedback to achieve correctness and completeness.

**Priority**: P1 (required to ensure calculation accuracy before Compute Engine implementation)

**Dependencies**: Phase 2B complete (populated canonical list), LLM review results available

#### Automated Refinement Module Implementation

- [X] T02B5-001 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Create calculation refinement module structure in `backend/references-research-engine/src/research/calculation_refinement/` with components: `review_extractor.py`, `fix_generator.py`, `fix_applier.py`, `fix_validator.py`, `iteration_tracker.py`, `refinement_orchestrator.py`, `schemas.py` (module-local, exclusive paths)
  > **Context:** `@Research/mvp_calculations_review_results.yaml` `@Research/MVP_canonical_calculations.yaml`
  > **Reference:** Architecture design from conversation - iterative refinement pipeline

- [X] T02B5-002 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Implement `review_extractor.py` to parse LLM review text into structured `RefinementIssues` object (extracts overall assessment, issues by category, missing elements, recommendations) in `backend/references-research-engine/src/research/calculation_refinement/review_extractor.py` (module-local, exclusive paths)

- [X] T02B5-003 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Implement `fix_generator.py` to generate fix prompts and produce corrected calculation YAML from `RefinementIssues` in `backend/references-research-engine/src/research/calculation_refinement/fix_generator.py` (module-local, exclusive paths)

- [X] T02B5-004 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Implement `fix_applier.py` to merge fixes into original calculations while preserving metadata (version, iteration tracking) in `backend/references-research-engine/src/research/calculation_refinement/fix_applier.py` (module-local, exclusive paths)

- [X] T02B5-005 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Implement `fix_validator.py` to re-review fixed calculations and verify issues were addressed (compares before/after assessments) in `backend/references-research-engine/src/research/calculation_refinement/fix_validator.py` (module-local, exclusive paths)

- [X] T02B5-006 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Implement `iteration_tracker.py` to track refinement iterations per calculation (stores iteration number, issues found, fixes applied, validation results, assessment progression) with max iteration limits in `backend/references-research-engine/src/research/calculation_refinement/iteration_tracker.py` (module-local, exclusive paths)

- [X] T02B5-007 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Implement `refinement_orchestrator.py` main orchestration class with methods: `refine_calculation()`, `refine_all_calculations()`, `refine_all_from_review()`, `get_refinement_status()` in `backend/references-research-engine/src/research/calculation_refinement/refinement_orchestrator.py` (module-local, exclusive paths)

- [X] T02B5-008 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Implement `schemas.py` with data models: `RefinementIssue`, `RefinementIssues`, `RefinementIteration` in `backend/references-research-engine/src/research/calculation_refinement/schemas.py` (module-local, exclusive paths)

#### Refinement Execution

- [X] T02B5-009 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Create script to run automated refinement on MVP calculations from review results in `backend/references-research-engine/src/research/run_calculation_refinement.py` (module-local, exclusive paths)
  > **Context:** `@Research/mvp_calculations_review_results.yaml` `@Research/MVP_canonical_calculations.yaml`

- [X] T02B5-010 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Execute refinement on all 14 MVP calculations with max_iterations=3, save updated calculations to `Research/MVP_canonical_calculations.yaml` in `backend/references-research-engine/src/research/run_calculation_refinement.py` (module-local, exclusive paths) - Refinement executed on 2025-11-20, 12/14 calculations marked as CORRECT (85.7% success rate)

- [X] T02B5-011 [P] [US1] [US2] @agent-1 ✅ COMPLETED: Verify refinement results: check that calculations marked as CORRECT or improved from NEEDS MAJOR/MINOR CORRECTIONS in `Research/mvp_calculations_refinement_results.yaml` (doc-only verification) - Verification document created, 12/14 calculations CORRECT, 2 improved from MAJOR to MINOR corrections

**Validation Considerations** (Deferred to Phase 4):
- Independent verification mechanisms were considered but not implemented:
  - Test case execution validation (execute calculations and verify outputs)
  - Golden dataset validation (compare against ATO official examples)
  - Independent LLM review (cross-check with different model)
  - Mathematical formula verification (syntax and logic checks)
  - Change diff analysis (detailed before/after comparison)
- Current validation relies on LLM self-assessment (same model validates its own fixes)
- Future enhancement: Implement comprehensive validation mechanisms in Phase 4

**Checkpoint**: ✅ Phase 2B.5 complete - Automated refinement module implemented, MVP calculations refined based on LLM review feedback, iteration tracking and validation in place, updated `MVP_canonical_calculations.yaml` with corrections. **Results**: 12/14 calculations (85.7%) marked as CORRECT, 2 calculations improved from MAJOR to MINOR corrections. Verification document created at `Research/mvp_calculations_refinement_results.yaml`. **Note**: Independent verification mechanisms deferred to Phase 4.

---

### Phase 2.3 – Calculation Expansion (Day 7.75)

**Goal**: Expand calculation capabilities with performance-optimized strategy execution.

**Priority**: P1 (enables efficient strategy optimization)

**Dependencies**: Phase 2B.5 complete (refined calculations)

#### Strategy Engine Implementation

- [ ] T023-001 [P] [US1] [US2] @agent-1 Implement Strategy Engine with optimization loops
  **Constraint**: Strategy Engine loops must use ProjectionSummary (in-memory) rather than full ProjectionOutput serialization to ensure <30s optimization times.

---

### Phase 2C – Build test harness around research output (Day 8)

**Goal**: Makes the whole thing safe enough to base advice on.

**Priority**: P1 (required before Phase 2D can begin)

**Dependencies**: Phase 2A complete (real findings in database), Phase 2B complete (populated canonical list)

#### Golden Examples Set Creation

- [X] ✅ T02C-001 [P] [US1] [US2] @agent-1 Create golden examples set from ATO/ASIC worked examples in `tests/golden-datasets/ato_examples/` (module-local, exclusive paths)
- [X] ✅ T02C-002 [P] [US1] [US2] @agent-1 Store PAYG marginal tax + offsets golden example (official inputs + outputs + citations) in `tests/golden-datasets/ato_examples/payg_marginal_tax_offsets.yaml` (module-local, exclusive paths)
- [X] ✅ T02C-003 [P] [US1] [US2] @agent-1 Store CGT discount event golden example (official inputs + outputs + citations) in `tests/golden-datasets/ato_examples/cgt_discount_event.yaml` (module-local, exclusive paths)
- [X] ✅ T02C-004 [P] [US1] [US2] @agent-1 Store super contributions + Div 293 golden example (official inputs + outputs + citations) in `tests/golden-datasets/ato_examples/super_contributions_div293.yaml` (module-local, exclusive paths)
- [X] ✅ T02C-005 [P] [US1] [US2] @agent-1 Store negative gearing mortgage interest golden example (official inputs + outputs + citations) in `tests/golden-datasets/ato_examples/negative_gearing_mortgage_interest.yaml` (module-local, exclusive paths)
- [X] ✅ T02C-006 [P] [US1] [US2] @agent-1 Document exact expected outputs with rounding rules for each golden example in golden example YAML files (module-local, exclusive paths)

#### Tests That Pull Rules/Findings from DB

- [X] ✅ T02C-007 [P] [US1] [US2] @agent-1 Write tests that pull relevant rules/findings from database for each golden example in `backend/references-research-engine/tests/integration/test_golden_examples_integration.py` (module-local tests only)
- [X] ✅ T02C-008 [P] [US1] [US2] @agent-1 Assert that extracted logic matches official behaviour (or at least doesn't contradict it in obvious ways) in `backend/references-research-engine/tests/integration/test_golden_examples_integration.py` (module-local tests only)
- [X] ✅ T02C-009 [P] [US1] [US2] @agent-1 Test findings → canonical list → calculation logic chain in `backend/references-research-engine/tests/integration/test_findings_chain.py` (module-local tests only)
- [X] ✅ T02C-010 [P] [US1] [US2] @agent-1 Validate provenance chains are complete for test cases in `backend/references-research-engine/tests/integration/test_provenance_chains.py` (module-local tests only)

#### Research Integrity Tests

- [ ] T02C-011 [P] [US1] [US2] @agent-1 Add tests that validate no rules without references (every rule must cite at least one Reference) in `backend/references-research-engine/tests/integration/test_research_integrity.py` (module-local tests only)
- [ ] T02C-012 [P] [US1] [US2] @agent-1 Add tests that validate no orphan strategies without linked calculations in `backend/references-research-engine/tests/integration/test_research_integrity.py` (module-local tests only)
- [ ] T02C-013 [P] [US1] [US2] @agent-1 Add tests that validate provenance is complete for each finding (Finding → Reference → Assumptions chain) in `backend/references-research-engine/tests/integration/test_provenance_chains.py` (module-local tests only)
- [ ] T02C-014 [P] [US1] [US2] @agent-1 Add tests that validate References exist and are accessible in `backend/references-research-engine/tests/integration/test_reference_accessibility.py` (module-local tests only)
- [ ] T02C-015 [P] [US1] [US2] @agent-1 Add tests that validate findings have proper lifecycle states in `backend/references-research-engine/tests/integration/test_finding_lifecycle.py` (module-local tests only)

#### Research Drift Detection Tests

- [ ] T02C-016 [P] [US1] [US2] @agent-1 Add tests that catch when canonical list drifts from findings in `backend/references-research-engine/tests/integration/test_research_drift.py` (module-local tests only)
- [ ] T02C-017 [P] [US1] [US2] @agent-1 Add tests that validate findings remain linked to valid References after updates in `backend/references-research-engine/tests/integration/test_research_drift.py` (module-local tests only)
- [ ] T02C-018 [P] [US1] [US2] @agent-1 Add tests that ensure completeness scores remain accurate after research updates in `backend/references-research-engine/tests/integration/test_completeness_drift.py` (module-local tests only)

**Checkpoint**: Phase 2C complete - Golden examples set created from ATO/ASIC worked examples, tests validate extracted logic against official examples, tests validate research integrity (no orphaned rules, complete provenance), research drift detection tests operational

---

### Phase 2D – Compute Engine "Phase 2 proper" (Days 7.5-8)

**Goal**: Build Compute Engine consuming real canonical data rather than theoretical stubs.

**Priority**: P1 (core calculation engine)

**Dependencies**: Phase 0 complete, Phase 1 (References & Research Engine) complete, **CRITICAL**: Phase 2A complete (real findings in database), Phase 2B complete (populated `canonical_calculations.yaml`), Phase 2C complete (verified golden examples)

#### Entity ID Generation System

- [x] T053AA [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement entity ID generation utility using Python `ulid` library in `backend/shared/storage/entity_id.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1, `Design_docs/final_design_questions.md` Section 4)
- [x] T053AB [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement prefix validation (RU-, RE-, AS-, AG-, ST-, SC-, EV-, IN-, FA-, FN-, RQ-, VD-, RS-, PL-) in `backend/shared/storage/entity_id.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1)
- [ ] T053AC [P] [US1] [US2] [US3] @agent-2 Implement ID format validation and parsing in `backend/shared/storage/entity_id_validator.py` (module-local, exclusive paths)
- [x] T053AD [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Add database unique constraints on entity ID columns for defense-in-depth collision prevention in `infrastructure/database/postgres/schema.sql` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1)

#### Canonical Calculation List Dependency

**CRITICAL**: Compute Engine Phase 1 CANNOT begin until References & Research Engine Phase 4 canonical calculation list is complete.

- [x] T052P [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Load canonical calculation list from References & Research Engine (`Research/canonical_calculations.yaml`) in `backend/compute-engine/src/calculations/canonical_loader.py` (CRITICAL: Requires T052J complete - canonical list must exist) (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites)
- [x] T052O1 [US2] @agent-1 ✅ COMPLETED: Create Compute Engine requirements context file (`specs/003-references-research-engine/research_guidance/compute-engine-requirements-context.md`) with checklist of required information for calculation implementation (CRITICAL: Must be created before T052P1 can load it) (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites, `specs/003-references-research-engine/plan_003_references_research_engine.md` Phase 4)
- [x] T052P1 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Load Compute Engine requirements context (`specs/003-references-research-engine/research_guidance/compute-engine-requirements-context.md`) before starting implementation in `backend/compute-engine/src/calculations/requirements_context_loader.py` (CRITICAL: Requires T052O1 complete - requirements context file must exist) (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites)
- [x] T052Q [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Validate calculation completeness (verify all calculations have sufficient information for implementation using Compute Engine requirements context checklist) in `backend/compute-engine/src/calculations/completeness_check.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites)
- [x] T052Q1 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Check completeness scores: review completeness_score (0-100%) for each calculation from canonical list in `backend/compute-engine/src/calculations/completeness_review.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites)
- [x] T052R [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Flag incomplete calculations (mark as "INSUFFICIENT_INFO" when completeness_score < 100% or missing required fields) in `backend/compute-engine/src/calculations/incomplete_tracker.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites)
- [x] T052R1 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Generate structured refinement requests via References & Research Engine API (`POST /research/refine`) with calculation_id, missing_fields, specific_questions, priority, iteration_number, and schema_suggestion (when schema issues block implementation) in `backend/compute-engine/src/calculations/refinement_request_generator.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites, FR-SCHEMA-01, CRITICAL: Requires T041.7 complete - Research Refinement API must exist)
- [x] T052R2 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Track refinement request status and resume implementation when research completes in `backend/compute-engine/src/calculations/refinement_tracker.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites)
- [x] T052S [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Document research gaps in `backend/compute-engine/docs/research_gaps.md` for tracking incomplete calculations (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1 prerequisites)
- [x] T052T [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Generate calculation function stubs from canonical list specifications (one Python function per calculation with CAL-* identifier) - ONLY for complete calculations (completeness_score = 100%) in `backend/compute-engine/src/calculations/stub_generator.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1)

#### Rule Execution

- [x] T053 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Design Fact data model with bitemporal fields (`valid_from`, `valid_to`) in `backend/compute-engine/src/models/fact.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1, `Design_docs/final_design_questions.md` Section 4)
- [x] T053A [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement default filter for current rows (`WHERE valid_to IS NULL`) in `backend/compute-engine/src/models/fact.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1)
- [ ] T053B [P] [US1] [US2] [US3] @agent-2 Create partial indexes on current data (`WHERE valid_to IS NULL`) for performance in `infrastructure/database/postgres/indexes.sql` (module-local, exclusive paths)
- [x] T054 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement rule resolution (precedence, effective dates) with temporal logic using bitemporal fields in `backend/compute-engine/src/rules/resolution.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1)
- [x] T055 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement calculation execution engine in `backend/compute-engine/src/calculation/engine.py`
- [x] T056 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement deterministic calculation logic in `backend/compute-engine/src/calculation/deterministic.py`
- [x] T057 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement numeric tolerance and rounding standards in `backend/compute-engine/src/calculation/rounding.py`

#### Scenario Management

- [x] T058 [US1] [US2] @agent-1 ✅ COMPLETED: Implement scenario creation and tagging in `backend/compute-engine/src/scenarios/creation.py`
- [x] T059 [US1] [US2] @agent-1 ✅ COMPLETED: Implement scenario comparison queries in `backend/compute-engine/src/scenarios/comparison.py`
- [x] T060 [US1] [US2] @agent-1 ✅ COMPLETED: Implement sensitivity analysis support in `backend/compute-engine/src/scenarios/sensitivity.py`
- [x] T061 [US1] [US2] @agent-1 ✅ COMPLETED: Ensure scenarios never overwrite base reality in `backend/compute-engine/src/scenarios/isolation.py`

#### Provenance Storage Implementation

- [x] T061A [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement `provenance_edges` table schema (src_id, dst_id, relation_type, created_at, tenant_id) in `infrastructure/database/postgres/schema.sql` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1, `Design_docs/final_design_questions.md` Section 4) - Already exists in schema.sql
- [x] T061B [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement JSONB metadata columns on entity tables for attributes in `infrastructure/database/postgres/schema.sql` (relationships stored as rows, attributes stored as JSONB) (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1) - Documentation and patterns added to schema.sql
- [x] T061C [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement provenance link creation and querying utilities in `backend/compute-engine/src/provenance/storage.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1)
- [ ] T061D [P] [US1] [US2] [US3] @agent-2 Tests for provenance storage (relational edge table + JSONB) in `backend/compute-engine/tests/unit/test_provenance_storage.py` (module-local tests only)

#### Bitemporal Fields & Time-Travel

- [x] T061E [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement bitemporal fields (`valid_from`, `valid_to`) on all temporal entities (Rules, References, Assumptions, Advice Guidance, Client Outcome Strategies, Scenarios, Facts, Provenance Links) in `infrastructure/database/postgres/schema.sql` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1, `Design_docs/final_design_questions.md` Section 4) - Documentation and patterns added to schema.sql (Facts already implemented in T053, Provenance Links already in provenance_edges table)
- [x] T061F [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement time-travel query utilities with `as_of` date support (query pattern: `WHERE valid_from <= as_of AND (valid_to IS NULL OR valid_to > as_of)`) in `backend/compute-engine/src/storage/time_travel.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 1)
- [ ] T061G [P] [US1] [US2] [US3] @agent-3 Create partial indexes on current data for performance optimization (`WHERE valid_to IS NULL`) in `infrastructure/database/postgres/indexes.sql` (module-local, exclusive paths)

#### Provenance and Explainability

- [x] T062 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement provenance chain building (Fact → Rule(s)/Client Outcome Strategy → Reference(s) → Assumptions) using relational edge table in `backend/compute-engine/src/provenance/chain.py` (CRITICAL: Requires Phase 1 References & Research Engine checkpoint complete - References must exist before provenance chains can reference them, requires T061A-T061C complete)
  > **Context:** `@infrastructure/database/postgres/schema.sql` `@backend/compute-engine/src/provenance`
  > **Prompt:** "Use a Recursive CTE for graph traversal. Do not loop in Python. Ensure JSONB queries use specific keys."
- [x] T063 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement `/explain/{fact_id}` endpoint in `backend/compute-engine/src/api/explain.py` (⚠️ FREEZE B: OpenAPI contract - no [P] after freeze)
  > **Context:** `@infrastructure/database/postgres/schema.sql` `@backend/compute-engine/src/provenance`
  > **Prompt:** "Use a Recursive CTE for graph traversal. Do not loop in Python. Ensure JSONB queries use specific keys."
- [x] T064 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement time-travel queries (`as_of` date support) in `backend/compute-engine/src/provenance/time_travel.py`
- [x] T065 [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement provenance export for compliance packs in `backend/compute-engine/src/provenance/export.py`
- [x] T065A [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement fallback handling when References are missing from provenance chain in `backend/compute-engine/src/provenance/reference_fallback.py` (handle missing References gracefully)
- [x] T065B [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement validation that all References in provenance chain exist in `backend/compute-engine/src/provenance/reference_validation.py` (validate References exist before building chain)
- [x] T065C [US1] [US2] [US3] @agent-1 ✅ COMPLETED: Implement materialized view with CONCURRENT refresh strategy for instant `/explain` chains in `infrastructure/database/postgres/materialized_views.sql` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 3, `specs/001-master-spec/master_plan.md`)
  > **Context:** `@infrastructure/database/postgres/schema.sql` `@backend/compute-engine/src/provenance`
  > **Prompt:** "Use a Recursive CTE for graph traversal. Do not loop in Python. Ensure JSONB queries use specific keys."
- [ ] T065D [US1] [US2] [US3] @agent-1 Configure read replicas for explain query distribution and read scaling in `infrastructure/database/postgres/replicas.sql` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Performance & Scalability, `specs/001-master-spec/master_plan.md`)
- [ ] T065E [US1] [US2] [US3] @agent-1 Set up connection pooling (PgBouncer) for efficient connection management in `infrastructure/database/postgres/connection_pooling.sql` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Performance & Scalability, `specs/001-master-spec/master_plan.md`)
- [ ] T065F [US1] [US2] [US3] @agent-1 Implement Redis caching for hot explain chains in `backend/compute-engine/src/explanations/cache.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 3)

#### Calculation Function Explanation Repository

**CRITICAL**: This section MUST be completed BEFORE Calculation Types Implementation (T132+) because all calculation functions MUST reference explanation entries.


- [ ] T066 [P] [US1] [US2] [US3] @agent-1 Create `explanations/` directory structure with `index.yaml` and `functions/` subdirectory at repository root (exclusive paths: explanations/ only)
- [ ] T067 [P] [US1] [US2] [US3] @agent-1 Define explanation file schema (function ID, comprehensive explanation, implementation rationale, rule references, testing approach, creation date, version tracking, canonical_source, canonical_calculation_id) in `explanations/functions/SCHEMA.md` (doc-only) (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 7)
- [ ] T068 [US1] [US2] [US3] @agent-1 Implement explanation repository loader in `backend/compute-engine/src/explanations/loader.py` to load explanation files from `explanations/functions/` directory
- [ ] T069 [US1] [US2] [US3] @agent-1 Implement explanation index builder in `backend/compute-engine/src/explanations/index_builder.py` to scan `explanations/functions/` and build/update `explanations/index.yaml` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 7)
- [ ] T069A [US1] [US2] [US3] @agent-1 Implement canonical list bootstrap process (auto-populate explanation templates from canonical list data) in `backend/compute-engine/src/explanations/canonical_bootstrap.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 7)
- [ ] T069B [US1] [US2] [US3] @agent-1 Implement canonical sync mechanism (detect canonical list updates and flag explanations for review) in `backend/compute-engine/src/explanations/canonical_sync.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 7)
- [ ] T070 [US1] [US2] [US3] @agent-1 Implement explanation file validator in `backend/compute-engine/src/explanations/validator.py` to ensure all required fields are present and schema-compliant
- [ ] T071 [P] [US1] [US2] [US3] @agent-1 Create explanation template generator in `backend/compute-engine/src/explanations/template_generator.py` for new calculation functions (module-local, exclusive paths)
- [ ] T072 [US1] [US2] [US3] @agent-1 Implement explanation lookup system in `backend/compute-engine/src/explanations/lookup.py` that every Python calculation function must use to reference its explanation entry
- [ ] T073 [US1] [US2] [US3] @agent-1 Create explanation repository documentation in `explanations/README.md` describing structure, schema, and usage (doc-only)
- [ ] T074 [P] [US1] [US2] [US3] @agent-1 Tests for explanation repository loader and index builder in `backend/compute-engine/tests/unit/test_explanations_repository.py` (module-local tests only)
- [ ] T075 [P] [US1] [US2] [US3] @agent-1 Tests to verify all calculation functions have corresponding explanation entries in `backend/compute-engine/tests/integration/test_explanations_coverage.py` (module-local tests only)

#### PostgreSQL Storage Integration

- [ ] T097 [US1] [US2] [US3] @agent-1 Implement Publish → Validate → Activate workflow in `backend/compute-engine/src/storage/publish_validate_activate.py` (CRITICAL: Requires T001 complete - PostgreSQL schema must exist)
- [ ] T097A [US1] [US2] [US3] @agent-1 Implement ruleset snapshot creation in PostgreSQL in `backend/compute-engine/src/storage/ruleset_snapshot.py`
- [ ] T097B [US1] [US2] [US3] @agent-1 Implement ruleset validation (integrity, consistency, referential checks) in `backend/compute-engine/src/storage/ruleset_validation.py`
- [ ] T097C [US1] [US2] [US3] @agent-1 Implement ruleset activation in `backend/compute-engine/src/storage/ruleset_activation.py` (activate validated ruleset snapshots)
- [ ] T097D [US1] [US2] [US3] @agent-1 Implement workflow timing monitoring and performance tracking for Publish → Validate → Activate workflow in `backend/compute-engine/src/storage/workflow_timing.py` (Reference: SC-008 - 5-minute workflow completion requirement)
- [ ] T097E [US1] [US2] [US3] @agent-1 Add performance optimization for ruleset publication workflow (parallel validation, optimized database operations, caching) to ensure 5-minute completion time in `backend/compute-engine/src/storage/workflow_optimization.py` (Reference: SC-008)
- [ ] T098 [US1] [US2] [US3] @agent-1 Forbid direct database edits outside of versioned artifacts (enforce via code review) in `backend/compute-engine/src/storage/database_access.py`
- [ ] T099 [US1] [US2] [US3] @agent-1 Implement ruleset snapshot monitoring and alerting in `backend/compute-engine/src/storage/snapshot_monitoring.py` (monitor snapshot creation and validation)
- [ ] T100 [US1] [US2] [US3] @agent-1 Implement snapshot rollback on validation failure in `backend/compute-engine/src/storage/snapshot_rollback.py` (rollback snapshot creation if validation fails)
- [ ] T100A [US1] [US2] [US3] @agent-1 Implement snapshot retry logic in `backend/compute-engine/src/storage/snapshot_retry.py` (retry failed snapshot creation with exponential backoff)
- [ ] T100B [US1] [US2] [US3] @agent-1 Implement activated ruleset rollback API (`POST /api/v1/rulesets/{ruleset_id}/rollback`) with deactivation/reactivation logic, time-travel query support, and audit logging in `backend/compute-engine/src/api/ruleset_rollback.py` (Reference: `specs/001-master-spec/master_spec.md` CL-037)
- [ ] T100C [US1] [US2] [US3] @agent-1 Implement rollback testing scenarios in `backend/compute-engine/tests/integration/test_ruleset_rollback.py` (test rollback procedures before production deployment)

#### APIs

- [ ] T101 [US1] [US2] [US3] @agent-1 Implement `POST /run` (calculation API) in `backend/compute-engine/src/api/run.py` (⚠️ FREEZE B: OpenAPI contract - no [P] after freeze)
  > **Context:** `@specs/001-master-spec/contracts/compute-engine.openapi.yaml` `@backend/shared/api/schemas.py`
  > **Prompt:** "Ensure implementation matches the OpenAPI contract exactly (Freeze B). Use Pydantic v2 models."
- [ ] T101A [US1] [US2] [US3] @agent-1 Implement API versioning strategy for Compute Engine (`/api/v1/run`, `/api/v2/run`) in `backend/compute-engine/src/api/versioning.py` (⚠️ FREEZE B: OpenAPI contract - no [P] after freeze)
- [ ] T101B [US1] [US2] [US3] @agent-1 Document deprecation policy for Compute Engine APIs (e.g., "v1 deprecated 6 months after v2 release") in `backend/compute-engine/src/api/DEPRECATION_POLICY.md` (doc-only)
- [ ] T102 [US1] [US2] [US3] @agent-1 Implement `POST /run-batch` (batch calculations) with async job handling (return `202 Accepted` with `job_id` for requests exceeding time threshold, default: 15 seconds) and partial-result semantics (return successful results alongside errors for failed items) in `backend/compute-engine/src/api/run_batch.py` (⚠️ FREEZE B: OpenAPI contract - no [P] after freeze, Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Background Jobs, per FR-025C: partial-result semantics)
- [ ] T102A [US1] [US2] [US3] @agent-1 Set up RQ (Redis Queue) workers on Render for background job processing in `backend/compute-engine/src/jobs/rq_setup.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 5, `Design_docs/final_design_questions.md` Section 6)
- [ ] T102B [US1] [US2] [US3] @agent-1 Configure Redis connection for job queue in `backend/compute-engine/src/jobs/redis_config.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 5)
- [ ] T102C [US1] [US2] [US3] @agent-1 Implement job queue management (enqueue, dequeue, status tracking) in `backend/compute-engine/src/jobs/queue.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 5)
- [ ] T102D [US1] [US2] [US3] @agent-1 Set up job monitoring and health checks for RQ workers in `backend/compute-engine/src/jobs/monitoring.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 5)
- [ ] T102E [US1] [US2] [US3] @agent-1 Implement `GET /jobs/{job_id}` (job status polling endpoint) with status (`queued`, `running`, `completed`, `failed`), progress percentage, result data, error details in `backend/compute-engine/src/api/jobs.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 5, `Design_docs/final_design_questions.md` Section 6)
- [ ] T102F [US1] [US2] [US3] @agent-1 Implement job result storage and retrieval (minimum 7 days retention) in `backend/compute-engine/src/jobs/storage.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 5)
- [ ] T102G [US1] [US2] [US3] @agent-1 Implement job idempotency with job key format: `hash(inputs_hash + ruleset_id + as_of_date + scenario_id + tenant_id)` in `backend/compute-engine/src/jobs/idempotency.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Background Jobs, `Design_docs/final_design_questions.md` Section 6)
- [ ] T102H [US1] [US2] [US3] @agent-1 Implement job timeout handling (default: 15 minutes for Render limits) - jobs exceeding timeout marked as failed in `backend/compute-engine/src/jobs/timeout.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Background Jobs)
- [ ] T103 [US1] [US2] [US3] @agent-1 Implement `GET /facts` (Facts retrieval) in `backend/compute-engine/src/api/facts.py` (⚠️ FREEZE B: OpenAPI contract - no [P] after freeze)
  > **Context:** `@specs/001-master-spec/contracts/compute-engine.openapi.yaml` `@backend/shared/api/schemas.py`
  > **Prompt:** "Ensure implementation matches the OpenAPI contract exactly (Freeze B). Use Pydantic v2 models."
- [ ] T104 [US1] [US2] [US3] @agent-1 Implement `GET /explain/{fact_id}` (explanation API) in `backend/compute-engine/src/api/explain.py` (⚠️ FREEZE B: OpenAPI contract - no [P] after freeze)
  > **Context:** `@specs/001-master-spec/contracts/compute-engine.openapi.yaml` `@backend/shared/api/schemas.py`
  > **Prompt:** "Ensure implementation matches the OpenAPI contract exactly (Freeze B). Use Pydantic v2 models."
- [ ] T104A [US1] [US2] [US3] @agent-1 Implement `GET /explain/batch` (batch explain endpoint) for multiple Facts with query parameters `fact_ids=...&scenario_id=...` returning array of explain chains in `backend/compute-engine/src/api/explain_batch.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Phase 3, `specs/002-compute-engine/spec_002_compute_engine.md` FR-020D) (⚠️ FREEZE B: OpenAPI contract - no [P] after freeze)
- [ ] T105 [US1] [US2] [US3] @agent-1 Implement idempotency support with job key format: `hash(inputs_hash + ruleset_id + as_of_date + scenario_id + tenant_id)` in `backend/compute-engine/src/api/idempotency.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Background Jobs, `Design_docs/final_design_questions.md` Section 6)
- [ ] T106 [US3] @agent-1 Implement `GET /rulesets` API (rulesets listing) in `backend/compute-engine/src/api/rulesets.py` returning all published rulesets with metadata (identifiers, publication dates, effective date ranges, status, rule counts) per FR-030
- [ ] T107 [US3] @agent-1 Implement `GET /rules?active=true&as_of=...` API (rules query) in `backend/compute-engine/src/api/rules.py` returning rule metadata (identifiers, effective dates, precedence, references, applicability conditions) for rules active at specified date per FR-031
- [ ] T108 [US3] @agent-1 Ensure rule metadata APIs return data without exposing internal implementation details (calculation expressions, code, proprietary logic) per FR-032
- [ ] T109 [P] [US3] @agent-1 Tests for rules intelligence APIs (`GET /rulesets`, `GET /rules`) in `backend/compute-engine/tests/unit/test_rules_intelligence.py` (module-local tests only)

#### LLM Orchestrator - Intent Detection, Parsing, and Conversational Interface (Phase 2)

**CRITICAL**: All intent detection tasks require Phase 1 primer loader (T258) complete.

**Key Architectural Clarifications** (from `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md`):
- **Extraction vs Translation**: LLM Orchestrator does NOT extract advice directly. It translates natural language into structured requests. The extraction process includes: (1) Intent detection, (2) Parameter extraction, (3) Optional RAG retrieval, (4) PII filtering, (5) Schema validation.
- **Advice Provision Flow**: LLM Orchestrator does NOT generate advice. It structures requests executed by backend engines: User Query → LLM Orchestrator (Intent Detection + Parameter Extraction) → Structured Request → Compute Engine (Deterministic Calculations) → Facts → Advice Engine (Compliance Validation) → LLM Orchestrator (Format Response) → User-Facing Text.
- **User Communication**: Two main APIs handle user communication: `POST /llm/parse` (intent parsing) and `POST /llm/chat` (conversational interface). Both support optional RAG via `use_rag` flag.
- **Never Determines Outcomes**: All calculations and compliance checks happen in deterministic engines. LLM Orchestrator only structures requests and formats responses.

#### Intent Detection and Parsing

- [ ] T240 [US1] [US2] @agent-1 Implement intent detection from natural language in `backend/llm-orchestrator/src/intent/detection.py` (CRITICAL: Requires T258 complete - primer loader must exist)
- [ ] T241 [US1] [US2] @agent-1 Implement parameter extraction in `backend/llm-orchestrator/src/intent/parameter_extraction.py`
- [ ] T242 [US1] [US2] @agent-1 Implement missing parameter identification in `backend/llm-orchestrator/src/intent/missing_params.py`
- [ ] T243 [US1] [US2] @agent-1 Implement ambiguous query handling in `backend/llm-orchestrator/src/intent/ambiguity.py`

#### Conversational Interface

- [ ] T244 [US1] [US2] @agent-1 Implement multi-turn conversation support in `backend/llm-orchestrator/src/conversation/multi_turn.py`
- [ ] T245 [US1] [US2] @agent-1 Implement conversation context management in `backend/llm-orchestrator/src/conversation/context.py`
- [ ] T246 [US1] [US2] @agent-1 Implement tool call generation in `backend/llm-orchestrator/src/conversation/tool_calls.py`
- [ ] T246A [US1] [US2] @agent-1 Implement schema validation for LLM-generated tool calls before forwarding to Compute Engine in `backend/llm-orchestrator/src/conversation/tool_call_validation.py` (validate tool call schema matches Compute Engine API)
- [ ] T246B [US1] [US2] @agent-1 Implement schema versioning for tool calls in `backend/llm-orchestrator/src/conversation/tool_call_versioning.py` (handle API schema changes)
- [ ] T246C [US1] [US2] @agent-1 Implement schema version detection and deprecation warnings in `backend/llm-orchestrator/src/conversation/schema_deprecation.py`
- [ ] T246D [US1] [US2] @agent-1 Document schema migration path (v1 → v2) in `backend/llm-orchestrator/src/conversation/SCHEMA_MIGRATION.md` (doc-only)
- [ ] T247 [US1] [US2] @agent-1 Implement citation generation (References) in `backend/llm-orchestrator/src/conversation/citations.py`

#### LLM Model Routing

- [ ] T248 [US1] [US2] @agent-1 **Research Task**: Evaluate models available via OpenRouter for different tasks (MVP: OpenAI models via BYOK - gpt-5.1, gpt-5, gpt-5-mini, gpt-5-nano), prioritizing models that do not train on prompts, in `backend/llm-orchestrator/model-config/model_evaluation.md` (doc-only)
- [ ] T247A [US1] [US2] @agent-1 Implement model selection method for selecting models for different tasks based on OpenRouter model data schema (performance quality, developer preferences, pricing, speed) in `backend/llm-orchestrator/src/models/selector.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 1)
- [ ] T247B [US1] [US2] @agent-1 Implement model metadata fetching from OpenRouter API (`/api/v1/models` endpoint) in `backend/llm-orchestrator/src/models/metadata_fetcher.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 1)
- [ ] T247C [US1] [US2] @agent-1 Implement performance tracking and storage system (task-specific performance metrics, historical analysis) in `backend/llm-orchestrator/src/models/performance_tracking.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 1)
- [ ] T247D [US1] [US2] @agent-1 Implement configuration system for developer preferences per task type in `backend/llm-orchestrator/src/models/preferences.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 1)
- [ ] T247E [US1] [US2] @agent-1 Implement selection algorithm with weighted factors (performance quality, developer preferences, pricing, speed) in `backend/llm-orchestrator/src/models/selection_algorithm.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 1)
- [ ] T248A [US1] [US2] @agent-1 Implement OpenRouter API integration using OpenRouter SDK or direct API calls in `backend/llm-orchestrator/src/routing/openrouter_client.py` (see https://openrouter.ai/docs/quickstart)
- [ ] T248B [US1] [US2] @agent-1 Implement BYOK (Bring Your Own Key) configuration for OpenAI API keys via OpenRouter in `backend/llm-orchestrator/src/routing/byok_config.py` (see https://openrouter.ai/docs/use-cases/byok)
- [ ] T248E [US1] [US2] @agent-1 Implement data policy filtering to prefer models that do not train on prompts using OpenRouter's data policy filtering features in `backend/llm-orchestrator/src/routing/data_policy_filter.py` (see https://openrouter.ai/docs/features/privacy-and-logging). Allow models that train on prompts only if performance degradation >20% or pricing increase >50%.
- [ ] T248C [US1] [US2] @agent-1 Document OpenRouter API changes and model deprecation handling in `backend/llm-orchestrator/src/routing/OPENROUTER_API_CHANGES.md` (doc-only)
- [ ] T248D [US1] [US2] @agent-1 Monitor OpenRouter API changes and model availability, update integration as needed in `backend/llm-orchestrator/src/routing/api_monitor.py`
- [ ] T249 [US1] [US2] @agent-1 Implement intelligent model switching based on task type (MVP: within models available via OpenRouter) in `backend/llm-orchestrator/src/routing/model_switching.py`
- [ ] T250 [US1] [US2] @agent-1 Implement preference for cheaper models with performance fallback via OpenRouter in `backend/llm-orchestrator/src/routing/cost_optimization.py`
- [ ] T251 [US1] [US2] @agent-1 Implement prompt templating compatible with OpenRouter API in `backend/llm-orchestrator/src/routing/prompt_templates.py`
- [ ] T252 [US1] [US2] @agent-1 Implement token tracking (input/output/cached tokens per request) in `backend/llm-orchestrator/src/routing/token_tracking.py`
- [ ] T253 [US1] [US2] @agent-1 Implement cost calculation based on token usage and model pricing in `backend/llm-orchestrator/src/routing/cost_calculation.py`
- [ ] T253A [US1] [US2] @agent-1 Implement cost tracking database schema (store cost data per tenant, per model, per time period) in `infrastructure/database/postgres/schema.sql` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 3, `specs/001-master-spec/master_spec.md` CL-042)
- [ ] T253B [US1] [US2] @agent-1 Implement cost storage and retrieval in `backend/llm-orchestrator/src/costs/storage.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 3)

#### Numerical Fidelity

- [ ] T110 [US1] [US2] [US3] @agent-1 Implement fixed-point Decimal (Python `decimal.Decimal`) for all monetary values in `backend/compute-engine/src/calculation/decimal.py` (CRITICAL: Binary floating-point arithmetic is FORBIDDEN - use `decimal.Decimal` or integer cents only, per FR-007A)
- [ ] T111 [US1] [US2] [US3] @agent-1 Enforce explicit units and dimensional checks (% vs bps vs dollars vs years) in `backend/compute-engine/src/calculation/units.py`
- [ ] T112 [US1] [US2] [US3] @agent-1 Implement rounding policy per field (ATO rules, bankers rounding vs away-from-zero) in `backend/compute-engine/src/calculation/rounding_policy.py`
- [ ] T113 [US1] [US2] [US3] @agent-1 Specify when rounding occurs (step vs end) in rule definitions in `backend/compute-engine/src/rules/rounding_spec.py`
- [ ] T114 [US1] [US2] [US3] @agent-1 Guard against precision loss for long horizons (50+ years) and large totals in `backend/compute-engine/src/calculation/precision.py`

#### Error Handling and Resilience

- [ ] T115 [US1] [US2] [US3] @agent-1 Implement structured error responses with remediation guidance in `backend/compute-engine/src/api/errors.py` (per FR-025B: error taxonomy - 4xx for validation errors, 409 for conflicts, 5xx for compute failures, structured error responses with remediation guidance)
- [ ] T115A [US1] [US2] [US3] @agent-1 Implement error taxonomy system (4xx validation errors, 409 conflicts, 5xx compute failures) with structured error responses including error codes and remediation guidance in `backend/shared/api/error_taxonomy.py` (per FR-025B) (SERIAL: shared infrastructure)
- [ ] T116 [US1] [US2] [US3] @agent-1 Implement timeouts (default 30s) around database and external service lookups in `backend/compute-engine/src/resilience/timeouts.py`
- [ ] T117 [US1] [US2] [US3] @agent-1 Implement circuit breakers around external dependencies in `backend/compute-engine/src/resilience/circuit_breaker.py`
- [ ] T118 [US1] [US2] [US3] @agent-1 Implement retry policies with exponential backoff (1s initial, 30s max, 3 retries) for transient failures in `backend/compute-engine/src/resilience/retry.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Background Jobs, `Design_docs/final_design_questions.md` Section 6)
- [ ] T119 [US1] [US2] [US3] @agent-1 Implement dead-letter queue for failed calculation jobs with replay capability, error analysis, and operator notifications in `backend/compute-engine/src/resilience/dlq.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Background Jobs, `Design_docs/final_design_questions.md` Section 6)
- [ ] T119A [US1] [US2] [US3] @agent-1 Implement idempotency enforcement: all retries use same job idempotency key for exactly-once semantics in `backend/compute-engine/src/jobs/idempotency_enforcement.py` (Reference: `specs/002-compute-engine/plan_002_compute_engine.md` Background Jobs)

#### Validation and Reconciliation

- [ ] T120 [US1] [US2] [US3] @agent-1 Implement cross-checks (sum of components = totals, cash conservation) in `backend/compute-engine/src/validation/cross_checks.py`
- [ ] T121 [US1] [US2] [US3] @agent-1 Implement tax reconciliation (taxable income → tax → offsets → net tax) in `backend/compute-engine/src/validation/tax_reconciliation.py`
- [ ] T122 [US1] [US2] [US3] @agent-1 Implement super caps reconciliation (concessional + non-concessional = total, TBC/TSB roll-forward) in `backend/compute-engine/src/validation/super_reconciliation.py`
- [ ] T123 [US1] [US2] [US3] @agent-1 Implement amortisation reconciliation (opening + interest - repayments = closing) in `backend/compute-engine/src/validation/amortisation_reconciliation.py`
- [ ] T124 [US1] [US2] [US3] @agent-1 Implement rounding drift detection (tolerance: 0.01 cents per period) in `backend/compute-engine/src/validation/rounding_drift.py`

#### Concurrency and Consistency

- [ ] T125 [US1] [US2] @agent-1 Implement optimistic concurrency control (version numbers) or pessimistic locking for scenario updates in `backend/compute-engine/src/concurrency/locking.py`
- [ ] T126 [US1] [US2] [US3] @agent-1 Specify isolation levels (read-committed for fact writes, snapshot for time-travel) in `backend/compute-engine/src/concurrency/isolation.py`
- [ ] T127 [US1] [US2] [US3] @agent-1 Document consistency guarantees per endpoint (strong for `/run`, eventual for `/facts`) in `backend/compute-engine/src/api/consistency.py`

#### Ruleset Consistency

- [ ] T128 [US1] [US2] [US3] @agent-1 Implement consistency checks after ruleset publication (counts, checksums, referential integrity) in `backend/compute-engine/src/storage/consistency_checks.py`
- [ ] T129 [US1] [US2] [US3] @agent-1 Validate rule count matches in ruleset snapshot in `backend/compute-engine/src/storage/rule_count_validation.py`
- [ ] T130 [US1] [US2] [US3] @agent-1 Validate rule content hash matches in `backend/compute-engine/src/storage/hash_validation.py`
- [ ] T131 [US1] [US2] [US3] @agent-1 Validate all referenced rules exist in ruleset in `backend/compute-engine/src/storage/reference_validation.py`
- [ ] T131A [US1] [US2] [US3] @agent-1 Implement pre-snapshot validation (before T097A) in `backend/compute-engine/src/storage/pre_snapshot_validation.py` (validate ruleset consistency before snapshot creation)
- [ ] T131B [US1] [US2] [US3] @agent-1 Implement consistency check failure handling (rollback snapshot) in `backend/compute-engine/src/storage/consistency_failure_handling.py` (rollback snapshot if consistency checks fail)
- [ ] T131C [US1] [US2] [US3] @agent-1 Validate provenance link integrity (JSONB relationships) in `backend/compute-engine/src/storage/provenance_link_validation.py`

#### Calculation Types Implementation (per Advice_engine_calc_guidance.md)

**CRITICAL**: All calculation functions (T132+) MUST reference explanation entries created in T066-T075 above.

**Foundation Calculations**
- [ ] T132 [P] [US1] [US2] [US3] @agent-1 Implement CAL-FND-001: Time axis & periodization (FY/quarter/month, pro-rata, as_of pinning) in `backend/compute-engine/src/calculations/foundation/time_axis.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."
- [ ] T133 [P] [US1] [US2] [US3] @agent-1 Implement CAL-FND-002: Compounding & discounting (nominal/real, CPI/WPI, NPV/IRR) in `backend/compute-engine/src/calculations/foundation/compounding.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."
- [ ] T134 [P] [US1] [US2] [US3] @agent-1 Implement CAL-FND-003: Rounding standards (ATO rules, cents vs dollars, tolerances) in `backend/compute-engine/src/calculations/foundation/rounding.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."
- [ ] T135 [P] [US1] [US2] [US3] @agent-1 Implement CAL-FND-004: Scenario mechanics (A/B, sensitivities, Monte Carlo opt-in) in `backend/compute-engine/src/calculations/foundation/scenarios.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."
- [ ] T136 [P] [US1] [US2] [US3] @agent-1 Implement CAL-FND-005: Assumptions snapshotting & version pinning in `backend/compute-engine/src/calculations/foundation/assumptions.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Personal Income Tax Calculations**
- [ ] T137 [P] [US1] [US2] [US3] @agent-1 Implement CAL-PIT-001 through CAL-PIT-009: Personal income tax calculations (taxable income aggregation, PAYG, marginal tax, Medicare Levy, offsets, HELP/HECS, foreign income, deductions, bracket indexation) in `backend/compute-engine/src/calculations/tax/personal_income_tax.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Capital Gains Tax Calculations**
- [ ] T138 [P] [US1] [US2] [US3] @agent-1 Implement CAL-CGT-001 through CAL-CGT-007: CGT calculations (event detection, cost base adjustments, discounts, main residence exemption, managed fund components, losses, small business concessions) in `backend/compute-engine/src/calculations/tax/capital_gains_tax.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Investment Income & Entities Calculations**
- [ ] T139 [P] [US1] [US2] [US3] @agent-1 Implement CAL-INV-001 through CAL-INV-005: Investment income calculations (dividend gross-up, interest accrual, trust/partnership distributions, company tax, withholding tax) in `backend/compute-engine/src/calculations/investment/income.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Property Calculations - Growth & Ownership**
- [ ] T140 [P] [US1] [US2] [US3] @agent-1 Implement CAL-PRP-001 through CAL-PRP-008: Property growth and ownership calculations (capital growth, rental income, operating expenses, interest expense, depreciation, land tax, negative gearing, apportionment) in `backend/compute-engine/src/calculations/property/growth_ownership.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Property Calculations - Purchase & Sale**
- [ ] T141 [P] [US1] [US2] [US3] @agent-1 Implement CAL-PRX-001 through CAL-PRX-007: Property purchase and sale calculations (borrowing capacity, upfront costs, LMI, settlement adjustments, refinancing, sale costs, CGT on sale) in `backend/compute-engine/src/calculations/property/purchase_sale.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Debt & Cashflow Calculations**
- [ ] T142 [P] [US1] [US2] [US3] @agent-1 Implement CAL-DBT-001 through CAL-DBX-004: Debt and cashflow calculations (amortisation schedules, extra repayments, offset modelling, debt recycling, effective interest rates, credit-card payoff, split-loan, HELP/HECS, cash-buffer optimization) in `backend/compute-engine/src/calculations/debt/cashflow.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Superannuation - Contributions Calculations**
- [ ] T143 [P] [US1] [US2] [US3] @agent-1 Implement CAL-SUP-001 through CAL-SUP-008: Superannuation contribution calculations (SG accruals, concessional caps, non-concessional caps, government co-contribution, spouse offset, Division 293, LISTO, excess contributions) in `backend/compute-engine/src/calculations/superannuation/contributions.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Superannuation - Earnings & Benefits Calculations**
- [ ] T144 [P] [US1] [US2] [US3] @agent-1 Implement CAL-SUE-001 through CAL-SUE-007: Superannuation earnings and benefits calculations (fund earnings tax, account growth, preservation, TTR pensions, retirement phase, minimum drawdowns, lump sum vs income stream) in `backend/compute-engine/src/calculations/superannuation/earnings_benefits.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Reporting & Year-End Aggregation**
- [ ] T145 [P] [US1] [US2] [US3] @agent-1 Implement CAL-RPT-001 through CAL-RPT-004: Reporting calculations (FY roll-up, contributions summary, TBC/TSB trackers, cashflow vs tax timing reconciliation) in `backend/compute-engine/src/calculations/reporting/year_end.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Social Security & Aged Care Calculations**
- [ ] T146 [P] [US1] [US2] [US3] @agent-1 Implement CAL-SSC-001 through CAL-SSC-004: Social security and aged care calculations (Age Pension means tests, gifting/deprivation rules, Rent Assistance, aged care fees) in `backend/compute-engine/src/calculations/social_security/aged_care.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Superannuation - Advanced & SMSF Calculations**
- [ ] T147 [P] [US1] [US2] [US3] @agent-1 Implement CAL-SMS-001 through CAL-SMS-008: SMSF and advanced super calculations (ECPI, TBC tracking, death benefits taxation, defined benefit schemes, LRBA, in-house asset test, NALI/NALE, contribution reserving) in `backend/compute-engine/src/calculations/superannuation/smsf_advanced.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Entities & Business/Practice Tax Calculations**
- [ ] T148 [P] [US1] [US2] [US3] @agent-1 Implement CAL-ENT-001 through CAL-ENT-006: Entity and business tax calculations (trust streaming, Division 7A, PSI, GST basics, FBT, small business offsets) in `backend/compute-engine/src/calculations/entities/business_tax.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Insurance & Risk Calculations**
- [ ] T149 [P] [US1] [US2] [US3] @agent-1 Implement CAL-INS-001 through CAL-INS-003: Insurance calculations (premium projections, tax treatment, waiting/benefit period impacts) in `backend/compute-engine/src/calculations/insurance/risk.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Investment Portfolio Mechanics**
- [ ] T150 [P] [US1] [US2] [US3] @agent-1 Implement CAL-PFL-001 through CAL-PFL-004: Portfolio mechanics (rebalancing logic, tax-lot selection, sequence-of-returns, fee drag modelling) in `backend/compute-engine/src/calculations/investment/portfolio.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Property - Extended Calculations**
- [ ] T151 [P] [US1] [US2] [US3] @agent-1 Implement CAL-PRE-001 through CAL-PRE-005: Extended property calculations (surcharges, first-home concessions, GST on builds, PPOR exemptions, capex vs repairs) in `backend/compute-engine/src/calculations/property/extended.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**International & Residency Calculations**
- [ ] T152 [P] [US1] [US2] [US3] @agent-1 Implement CAL-INT-001 through CAL-INT-003: International and residency calculations (residency tests, non-resident tax scales, CGT main-residence limits) in `backend/compute-engine/src/calculations/international/residency.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Estate & Transfers Calculations**
- [ ] T153 [P] [US1] [US2] [US3] @agent-1 Implement CAL-EST-001 through CAL-EST-003: Estate and transfer calculations (death-related roll-overs, testamentary trusts, super death-benefit processing) in `backend/compute-engine/src/calculations/estate/transfers.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

**Reporting & Governance - Extras**
- [ ] T154 [P] [US1] [US2] [US3] @agent-1 Implement CAL-RGX-001 through CAL-RGX-004: Reporting and governance extras (ETP caps, PAYG instalments, indexation calendars, per-fact provenance enrichment) in `backend/compute-engine/src/calculations/reporting/governance.py` (module-local, exclusive paths)
  > **Context:** `@Research/canonical_calculations.yaml` `@backend/compute-engine/src/calculation/decimal.py`
  > **Prompt:** "Implement using `decimal.Decimal` only (precision 28, ROUND_HALF_UP). NO FLOATS. strictly follow the logic defined in the canonical yaml."

#### Assumptions Management (per Advice_engine_calc_guidance.md)

- [ ] T155 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue system for Foundation & Macro assumptions (ASM-FND-001 through ASM-FND-011) in `backend/compute-engine/src/assumptions/foundation.py` (module-local, exclusive paths)
- [ ] T156 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Personal Income & Deductions (ASM-PIT-001 through ASM-PIT-009) in `backend/compute-engine/src/assumptions/personal_income_tax.py` (module-local, exclusive paths)
- [ ] T157 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Capital Gains Tax (ASM-CGT-001 through ASM-CGT-008) in `backend/compute-engine/src/assumptions/capital_gains_tax.py` (module-local, exclusive paths)
- [ ] T158 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Investment & Portfolio (ASM-PFL-001 through ASM-PFL-013) in `backend/compute-engine/src/assumptions/investment_portfolio.py` (module-local, exclusive paths)
- [ ] T159 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Property - Market & Ownership (ASM-PRP-001 through ASM-PRP-010) in `backend/compute-engine/src/assumptions/property_market.py` (module-local, exclusive paths)
- [ ] T160 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Property - Purchase & Sale (ASM-PRX-001 through ASM-PRX-008) in `backend/compute-engine/src/assumptions/property_purchase_sale.py` (module-local, exclusive paths)
- [ ] T161 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Debt & Credit (ASM-DBT-001 through ASM-DBT-008) in `backend/compute-engine/src/assumptions/debt_credit.py` (module-local, exclusive paths)
- [ ] T162 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Superannuation - Contributions (ASM-SUP-001 through ASM-SUP-010) in `backend/compute-engine/src/assumptions/superannuation_contributions.py` (module-local, exclusive paths)
- [ ] T163 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Superannuation - Earnings & Benefits (ASM-SUE-001 through ASM-SUE-010) in `backend/compute-engine/src/assumptions/superannuation_earnings.py` (module-local, exclusive paths)
- [ ] T164 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Social Security & Aged Care (ASM-SSC-001 through ASM-SSC-008) in `backend/compute-engine/src/assumptions/social_security.py` (module-local, exclusive paths)
- [ ] T165 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Entities & Business/Practice Tax (ASM-ENT-001 through ASM-ENT-008) in `backend/compute-engine/src/assumptions/entities_business.py` (module-local, exclusive paths)
- [ ] T166 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Insurance & Risk (ASM-INS-001 through ASM-INS-004) in `backend/compute-engine/src/assumptions/insurance_risk.py` (module-local, exclusive paths)
- [ ] T167 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for International & Residency (ASM-INT-001 through ASM-INT-005) in `backend/compute-engine/src/assumptions/international_residency.py` (module-local, exclusive paths)
- [ ] T168 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Estate & Transfers (ASM-EST-001 through ASM-EST-004) in `backend/compute-engine/src/assumptions/estate_transfers.py` (module-local, exclusive paths)
- [ ] T169 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Behaviour & Planning (ASM-BHV-001 through ASM-BHV-007) in `backend/compute-engine/src/assumptions/behaviour_planning.py` (module-local, exclusive paths)
- [ ] T170 [P] [US1] [US2] [US3] @agent-1 Implement assumptions catalogue for Reporting & Governance (ASM-RGX-001 through ASM-RGX-008) in `backend/compute-engine/src/assumptions/reporting_governance.py` (module-local, exclusive paths)

#### Edge Case Handling (per Advice_engine_calc_guidance.md)

- [ ] T171 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Foundation & Temporal Logic (EDGE-FND-001 through EDGE-FND-014) in `backend/compute-engine/src/edge_cases/foundation.py` (module-local, exclusive paths)
- [ ] T172 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Personal Income Tax (EDGE-PIT-001 through EDGE-PIT-013) in `backend/compute-engine/src/edge_cases/personal_income_tax.py` (module-local, exclusive paths)
- [ ] T173 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Capital Gains Tax (EDGE-CGT-001 through EDGE-CGT-012) in `backend/compute-engine/src/edge_cases/capital_gains_tax.py` (module-local, exclusive paths)
- [ ] T174 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Investment Portfolio Mechanics (EDGE-PFL-001 through EDGE-PFL-010) in `backend/compute-engine/src/edge_cases/investment_portfolio.py` (module-local, exclusive paths)
- [ ] T175 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Property - Growth & Ownership (EDGE-PRP-001 through EDGE-PRP-010) in `backend/compute-engine/src/edge_cases/property_growth.py` (module-local, exclusive paths)
- [ ] T176 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Property - Purchase & Sale (EDGE-PRX-001 through EDGE-PRX-010) in `backend/compute-engine/src/edge_cases/property_purchase_sale.py` (module-local, exclusive paths)
- [ ] T177 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Debt & Cashflow (EDGE-DBT-001 through EDGE-DBT-009) in `backend/compute-engine/src/edge_cases/debt_cashflow.py` (module-local, exclusive paths)
- [ ] T178 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Superannuation - Contributions (EDGE-SUP-001 through EDGE-SUP-008) in `backend/compute-engine/src/edge_cases/superannuation_contributions.py` (module-local, exclusive paths)
- [ ] T179 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Superannuation - Earnings & Benefits (EDGE-SUE-001 through EDGE-SUE-008) in `backend/compute-engine/src/edge_cases/superannuation_earnings.py` (module-local, exclusive paths)
- [ ] T180 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for SMSF / Advanced Super (EDGE-SMS-001 through EDGE-SMS-006) in `backend/compute-engine/src/edge_cases/smsf_advanced.py` (module-local, exclusive paths)
- [ ] T181 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Social Security & Aged Care (EDGE-SSC-001 through EDGE-SSC-008) in `backend/compute-engine/src/edge_cases/social_security.py` (module-local, exclusive paths)
- [ ] T182 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Entities & Business/Trusts/Companies (EDGE-ENT-001 through EDGE-ENT-009) in `backend/compute-engine/src/edge_cases/entities_business.py` (module-local, exclusive paths)
- [ ] T183 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Insurance & Risk (EDGE-INS-001 through EDGE-INS-005) in `backend/compute-engine/src/edge_cases/insurance_risk.py` (module-local, exclusive paths)
- [ ] T184 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for International & Residency (EDGE-INT-001 through EDGE-INT-005) in `backend/compute-engine/src/edge_cases/international_residency.py` (module-local, exclusive paths)
- [ ] T185 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Estate & Transfers (EDGE-EST-001 through EDGE-EST-005) in `backend/compute-engine/src/edge_cases/estate_transfers.py` (module-local, exclusive paths)
- [ ] T186 [P] [US1] [US2] [US3] @agent-1 Implement edge case handling for Reporting, Governance & Provenance (EDGE-RGX-001 through EDGE-RGX-010) in `backend/compute-engine/src/edge_cases/reporting_governance.py` (module-local, exclusive paths)

#### Australia-Specific Design Considerations (per Advice_engine_calc_guidance.md)

- [ ] T187 [P] [US1] [US2] [US3] @agent-1 Implement calendar and period handling (FY 1 July-30 June, FBT year 1 April-31 March, BAS/GST cycles, PAYG instalments, super contribution counting, SG due dates, HECS/HELP timing, social security indexation, state revenue calendars) in `backend/compute-engine/src/australia/calendars.py` (module-local, exclusive paths)
- [ ] T188 [P] [US1] [US2] [US3] @agent-1 Implement multi-regulator environment support (ATO, ASIC, APRA, RBA, Council of Financial Regulators, AFCA) in `backend/compute-engine/src/australia/regulators.py` (module-local, exclusive paths)
- [ ] T189 [P] [US1] [US2] [US3] @agent-1 Implement tax system peculiarities (progressive scales, Medicare Levy, MLS, refundable dividend imputation, CGT discounts, main residence exemption, negative gearing, zone/SAPTO/PHI rebates, PSI rules, Division 7A, trust streaming, AMIT/managed fund tax, withholding for non-residents, tax residency tests, prepayment deduction spreading, ETPs) in `backend/compute-engine/src/australia/tax_system.py` (module-local, exclusive paths)
- [ ] T190 [P] [US1] [US2] [US3] @agent-1 Implement GST/Indirect tax handling (GST 10%, margin scheme, input-taxed supplies, FBT) in `backend/compute-engine/src/australia/gst_indirect.py` (module-local, exclusive paths)
- [ ] T191 [P] [US1] [US2] [US3] @agent-1 Implement superannuation system specifics (compulsory SG, concessional/non-concessional caps, carry-forward, bring-forward, Division 293, LISTO, government co-contribution, spouse contribution offset, preservation, TTR, retirement phase tax-free, TBC, minimum pension drawdowns, ECPI, SMSF LRBA, NALI/NALE, death-benefit taxes) in `backend/compute-engine/src/australia/superannuation.py` (module-local, exclusive paths)
- [ ] T192 [P] [US1] [US2] [US3] @agent-1 Implement social security and aged care specifics (Age Pension means tests, principal residence exemption, gifting/deprivation, Work Bonus, Rent Assistance, residential aged-care fees with RAD/DAP/MPIR, granny flat interests) in `backend/compute-engine/src/australia/social_security.py` (module-local, exclusive paths)
- [ ] T193 [P] [US1] [US2] [US3] @agent-1 Implement property and state/territory variation handling (stamp/transfer duty by state, land tax thresholds/surcharges, first-home buyer schemes, foreign buyer surcharge duties, capital works/plant depreciation, council rates, PPOR vs investment apportionment) in `backend/compute-engine/src/australia/property_state.py` (module-local, exclusive paths)
- [ ] T194 [P] [US1] [US2] [US3] @agent-1 Implement loans and credit specifics (purpose-based interest deductibility, offset vs redraw, LMI premiums, fixed-rate break costs, serviceability buffers) in `backend/compute-engine/src/australia/loans_credit.py` (module-local, exclusive paths)
- [ ] T195 [P] [US1] [US2] [US3] @agent-1 Implement investment market specifics (DRP participation, ETF/CDIs, buy/sell spreads, performance fees, rebalancing conventions, tax-lot selection) in `backend/compute-engine/src/australia/investment_markets.py` (module-local, exclusive paths)
- [ ] T196 [P] [US1] [US2] [US3] @agent-1 Implement international/residency specifics (franking credits WHT, non-resident scales, CGT main residence restrictions, double-tax agreements) in `backend/compute-engine/src/australia/international_residency.py` (module-local, exclusive paths)
- [ ] T197 [P] [US1] [US2] [US3] @agent-1 Implement admin, compliance and advice requirements (SOA/ROA/FSG, Code of Ethics, commission bans, record-keeping, ID verification/AML-CTF, AFSL authorisations) in `backend/compute-engine/src/australia/compliance_advice.py` (module-local, exclusive paths)
- [ ] T198 [P] [US1] [US2] [US3] @agent-1 Implement indexation and versioning (mixed indexation bases, different indexation dates, frequent threshold shifts, as-of pinning, ATO safe-harbour benchmark rates) in `backend/compute-engine/src/australia/indexation_versioning.py` (module-local, exclusive paths)
- [ ] T199 [P] [US1] [US2] [US3] @agent-1 Implement data and UX implications (state of residence, property location, as-of date requirements, separate calendars, provenance chains, explainability, June/July processing lag, residency/couple status validation, PPOR/investment use toggle) in `backend/compute-engine/src/australia/data_ux.py` (module-local, exclusive paths)

#### Testing

- [ ] T200 [P] [US1] [US2] [US3] @agent-1 Unit tests for calculation logic in `backend/compute-engine/tests/unit/test_calculation.py` (module-local tests only)
- [ ] T201 [P] [US1] [US2] [US3] @agent-1 Property-based tests (Hypothesis) for edge cases in `backend/compute-engine/tests/property/test_edge_cases.py` (module-local tests only)
- [ ] T202 [P] [US1] [US2] [US3] @agent-1 Metamorphic tests (scaling inputs scales outputs appropriately) in `backend/compute-engine/tests/property/test_metamorphic.py` (module-local tests only)
- [ ] T203 [P] [US1] [US2] [US3] @agent-1 Snapshot tests for `/explain` chains in `backend/compute-engine/tests/integration/test_explain_snapshots.py` (module-local tests only)
- [ ] T204 [P] [US1] [US2] [US3] @agent-1 Golden dataset tests (ATO examples) in `backend/compute-engine/tests/golden/test_ato_examples.py` (module-local tests only)
- [ ] T204A [US1] [US2] [US3] @agent-1 **CRITICAL - Minimum Validation Suite**: Collect and validate at least 10 ATO tax calculation examples (taxable income, tax offsets, deductions, CGT) in `backend/compute-engine/tests/golden/test_ato_minimum_validation.py` - must match ATO examples exactly (within rounding tolerance) (module-local tests only)
- [ ] T205 [P] [US1] [US2] [US3] @agent-1 Deterministic reproducibility tests (same inputs = same outputs) in `backend/compute-engine/tests/integration/test_determinism.py` (module-local tests only)
- [ ] T205A [US1] [US2] [US3] @agent-1 **CRITICAL - Minimum Validation Suite**: Run 1000+ iterations of same calculation (same inputs + ruleset + date) and verify 100% identical outputs across all iterations in `backend/compute-engine/tests/integration/test_deterministic_reproducibility_validation.py` - test across different execution times, servers, and environments (module-local tests only)
- [ ] T206 [US1] [US2] [US3] @agent-1 Integration tests with References & Research Engine in `backend/compute-engine/tests/integration/test_references_integration.py`
- [ ] T207 [P] [US1] [US2] [US3] @agent-1 Tests for all calculation types (CAL-* items) in `backend/compute-engine/tests/unit/test_calculation_types.py` (module-local tests only)
- [ ] T208 [P] [US1] [US2] [US3] @agent-1 Tests for all assumptions (ASM-* items) in `backend/compute-engine/tests/unit/test_assumptions.py` (module-local tests only)
- [ ] T209 [P] [US1] [US2] [US3] @agent-1 Tests for all edge cases (EDGE-* items) in `backend/compute-engine/tests/unit/test_edge_cases_comprehensive.py` (module-local tests only)
- [ ] T210 [P] [US1] [US2] [US3] @agent-1 Tests for Australia-specific design considerations in `backend/compute-engine/tests/integration/test_australia_specific.py` (module-local tests only)
- [ ] T210A [P] [US1] [US2] [US3] @agent-1 Security tests for cross-tenant data access prevention in Compute Engine per FR-028A in `backend/compute-engine/tests/security/test_cross_tenant_access.py` (tests bugs, misconfigured queries, malicious input, missing tenant context to ensure User A cannot access User B's calculation results, scenarios, or facts) (module-local tests only)
- [ ] T211 [US2] @agent-1 **Veris Finance Test Forecasts**: Create test forecast suite in `frontend/veris-finance/tests/test_forecasts/` (per user guidance)

**Checkpoint**: Phase 2D complete - Compute Engine operational, deterministic calculations working, fixed-point Decimal arithmetic enforced, all calculation types implemented (per Advice_engine_calc_guidance.md), all assumptions catalogue implemented, all edge cases handled, Australia-specific design considerations implemented, error handling and resilience patterns implemented, reconciliation checks implemented, concurrency control implemented, ruleset consistency checks implemented, PostgreSQL data structures created and populated, ruleset snapshots created, provenance chains complete (via recursive CTEs), test coverage > 85%, all calculations validated against golden examples from Phase 2C (100% match for golden examples), all calculations validated via Veris Finance test forecasts

**Overall Phase 2 Checkpoint** (Phase 2A-2D complete):
- Phase 2A complete: High-leverage document set populated, real findings extracted and stored, sample calculations manually verified
- Phase 2B complete: `canonical_calculations.yaml` populated with real findings, "Ready for Compute" status tracked
- Phase 2C complete: Golden examples set created, tests validate extracted logic, research integrity tests operational
- Phase 2D complete: Compute Engine operational, all calculations validated against golden examples

---

### Phase 2.4 – LLM Integration (Day 8.5)

**Goal**: Integrate LLM capabilities with secure, design-time logic generation.

**Priority**: P1 (enables automated calculation development)

**Dependencies**: Phase 2D complete (Compute Engine operational)

#### Logic Factory Implementation

- [ ] T024-001 [P] [US1] [US2] @agent-1 Implement Design-Time Logic Factory: LLM generates draft CAL-*.py files locally.
  **Constraint**: Runtime code generation is strictly prohibited. All logic must be human-reviewed, tested via Golden Tests, and committed to the repo before deployment.

---

## Phase 3: Advice Engine (Days 9-10)

**Purpose**: Build Advice Engine and progress LLM Orchestrator for compliance checking workflows

**Priority**: P1 (compliance validation)

**Dependencies**: Phase 0 complete, Phase 1 (References & Research Engine) complete, Phase 2 complete (Phase 2A-2D: Knowledge base seeded, canonical list populated, test harness built, Compute Engine operational)

#### Compliance Evaluation

- [ ] T212 [US1] [US2] @agent-1 Design Advice Guidance data model in `backend/advice-engine/src/models/advice_guidance.py`
- [ ] T213 [US1] [US2] @agent-1 Implement best-interests duty checks in `backend/advice-engine/src/compliance/best_interests.py`
- [ ] T214 [US1] [US2] @agent-1 Implement conflict detection in `backend/advice-engine/src/compliance/conflict_detection.py`
- [ ] T215 [US1] [US2] @agent-1 Implement documentation requirement checks in `backend/advice-engine/src/compliance/documentation.py`
- [ ] T216 [US1] [US2] @agent-1 Implement product replacement logic evaluation in `backend/advice-engine/src/compliance/product_replacement.py`

#### Compliance APIs

- [ ] T217 [US1] [US2] @agent-1 Implement `POST /advice/check` (compliance checking) in `backend/advice-engine/src/api/check.py` (⚠️ FREEZE C: OpenAPI contract - no [P] after freeze)
- [ ] T218 [US1] [US2] @agent-1 Implement `GET /advice/requirements?context=...` (requirement retrieval) in `backend/advice-engine/src/api/requirements.py` (⚠️ FREEZE C: OpenAPI contract - no [P] after freeze)
- [ ] T218A [US1] [US2] @agent-1 Generate OpenAPI specification for Advice Engine APIs (`POST /advice/check`, `GET /advice/requirements`, `GET /advice-guidance`, `GET /client-outcome-strategies`) in `specs/001-master-spec/contracts/advice-engine-openapi.yaml` (CRITICAL: Must be generated before FREEZE C - required for contract validation) (exclusive paths: specs only)
- [ ] T219 [US1] [US2] [US3] @agent-1 Implement `GET /advice-guidance` API (advice guidance retrieval) in `backend/advice-engine/src/api/advice_guidance.py` per FR-024
- [ ] T220 [US1] [US2] [US3] @agent-1 Implement `GET /client-outcome-strategies` API (client outcome strategies retrieval) in `backend/advice-engine/src/api/client_outcome_strategies.py` per FR-024
- [ ] T221 [US1] [US2] @agent-1 Implement warning and required action generation in `backend/advice-engine/src/compliance/warnings.py`
- [ ] T222 [US1] [US2] @agent-1 Implement consumer-friendly vs professional warning formatting in `backend/advice-engine/src/compliance/formatting.py`

#### Integration

- [ ] T223 [US1] [US2] @agent-1 Integrate with Compute Engine (Fact data retrieval) in `backend/advice-engine/src/integration/compute_engine.py`
- [ ] T223A [US1] [US2] @agent-1 Define API contract tests for Compute Engine integration in `backend/advice-engine/tests/contracts/test_compute_engine_contract.py` (validate API compatibility) (module-local tests only)
- [ ] T223B [US1] [US2] @agent-1 Implement API versioning strategy for Compute Engine integration in `backend/advice-engine/src/integration/api_versioning.py` (handle API version changes)
- [ ] T223C [US1] [US2] @agent-1 Implement contract schema versioning (contract-v1.json, contract-v2.json) in `backend/advice-engine/tests/contracts/schemas/` (module-local, exclusive paths)
- [ ] T223D [US1] [US2] @agent-1 Document contract deprecation policy (support v1 for 6 months after v2 release) in `backend/advice-engine/tests/contracts/DEPRECATION_POLICY.md` (doc-only)
- [ ] T224 [US1] [US2] @agent-1 Integrate with References & Research Engine (regulatory requirements) in `backend/advice-engine/src/integration/references_engine.py`
- [ ] T224A [US1] [US2] @agent-1 Define API contract tests for References Engine integration in `backend/advice-engine/tests/contracts/test_references_engine_contract.py` (validate API compatibility) (module-local tests only)
- [ ] T225 [US1] [US2] @agent-1 Implement deterministic compliance evaluation in `backend/advice-engine/src/compliance/deterministic.py`
- [ ] T225A1 [US1] [US2] @agent-1 Implement schema feedback emission capability in Advice Engine (when missing field, relationship, or canonical mapping blocks compliance evaluation, emit structured schema-feedback requests via `POST /research/refine` API with schema_suggestion payload) in `backend/advice-engine/src/compliance/schema_feedback.py` (Reference: `specs/001-master-spec/master_spec.md` FR-SCHEMA-01, `specs/004-advice-engine/plan_004_advice_engine.md` - Schema Feedback section, CRITICAL: Requires T041.7 complete - Research Refinement API must exist)

#### Compliance Documentation (Phase 4)

**Reference**: `specs/004-advice-engine/plan_004_advice_engine.md` Phase 4

- [ ] T225A [US1] [US2] @agent-1 Implement compliance checklist generation in `backend/advice-engine/src/compliance/checklist_generation.py` (Reference: `specs/004-advice-engine/plan_004_advice_engine.md` Phase 4)
- [ ] T225B [US1] [US2] @agent-1 Implement completion tracking for checklist items in `backend/advice-engine/src/compliance/checklist_tracking.py` (Reference: `specs/004-advice-engine/plan_004_advice_engine.md` Phase 4)
- [ ] T225C [US1] [US2] @agent-1 Implement export functionality (JSON, PDF) for compliance checklists in `backend/advice-engine/src/compliance/checklist_export.py` (Reference: `specs/004-advice-engine/plan_004_advice_engine.md` Phase 4)
- [ ] T225D [US1] [US2] @agent-1 Link checklists to specific advice scenarios in `backend/advice-engine/src/compliance/checklist_linking.py` (Reference: `specs/004-advice-engine/plan_004_advice_engine.md` Phase 4)

#### Audit and Reporting (Phase 5)

**Reference**: `specs/004-advice-engine/plan_004_advice_engine.md` Phase 5

- [ ] T225E [US1] [US2] @agent-1 Implement comprehensive audit logging (track all compliance evaluations with timestamps and reasoning trails) in `backend/advice-engine/src/audit/logging.py` (Reference: `specs/004-advice-engine/plan_004_advice_engine.md` Phase 5)
- [ ] T225F [US1] [US2] @agent-1 Implement audit trail export (complete audit trails suitable for regulatory review) in `backend/advice-engine/src/audit/export.py` (Reference: `specs/004-advice-engine/plan_004_advice_engine.md` Phase 5)
- [ ] T225G [US1] [US2] @agent-1 Implement historical reconstruction using Advice Guidance versions applicable at that time in `backend/advice-engine/src/audit/historical_reconstruction.py` (Reference: `specs/004-advice-engine/plan_004_advice_engine.md` Phase 5)
- [ ] T225H [US1] [US2] @agent-1 Support time-travel queries for audit trail review in `backend/advice-engine/src/audit/time_travel.py` (Reference: `specs/004-advice-engine/plan_004_advice_engine.md` Phase 5)

#### LLM Orchestrator - Safety, Privacy, Schema Validation, APIs, and Testing (Phase 3)

#### Cost Management & Budget Controls

- [ ] T253C [US1] [US2] @agent-1 Implement configurable LLM cost caps per tenant and per time period (daily, weekly, monthly, default $100/month) in `backend/llm-orchestrator/src/costs/caps.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 3A, `specs/001-master-spec/master_spec.md` CL-042)
- [ ] T253D [US1] [US2] @agent-1 Implement budget alert system (80% warning, 100% critical) in `backend/llm-orchestrator/src/costs/alerts.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 3A)
- [ ] T253E [US1] [US2] @agent-1 Implement cost rejection mechanism (reject requests when cap reached) in `backend/llm-orchestrator/src/costs/rejection.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 3A)
- [ ] T253F [US1] [US2] @agent-1 Implement cost reporting API (`GET /llm/costs`, `GET /llm/costs/caps`, `PUT /llm/costs/caps`) in `backend/llm-orchestrator/src/api/costs.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 3A)
- [ ] T253G [US1] [US2] @agent-1 Integrate cost cap checking into `POST /llm/parse` and `POST /llm/chat` endpoints in `backend/llm-orchestrator/src/api/parse.py` and `backend/llm-orchestrator/src/api/chat.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 3A)
- [ ] T253H [US1] [US2] @agent-1 Implement daily query tracking for rate-limited models (track queries per model per day, enforce 1k/day limit for `alibaba/tongyi-deepresearch-30b-a3b:free`, reject requests when limit exceeded) in `backend/llm-orchestrator/src/routing/query_tracking.py` (Reference: `backend/llm-orchestrator/model-config/openrouter_models_list.md` - Alibaba model has 1k queries/day limit on free tier)

#### Primers and Prompts Management (continued)

**NOTE**: Initial primer/prompt setup (T255-T258) was completed in Phase 1. This section continues with A/B versioning and performance tracking.

- [ ] T259 [US1] [US2] @agent-1 Implement A/B versioning system for primers and prompts in `backend/llm-orchestrator/src/prompts/versioning.py` (supports `_v1a.md`, `_v1b.md` naming)
- [ ] T260 [US1] [US2] @agent-1 Implement performance measurement system for A/B variants in `backend/llm-orchestrator/src/prompts/performance_tracking.py`
- [ ] T261 [US1] [US2] @agent-1 Implement metrics tracking (accuracy, latency, cost, user satisfaction) per variant in `backend/llm-orchestrator/src/prompts/metrics.py`
- [ ] T262 [US1] [US2] @agent-1 Implement variant selection logic based on performance data in `backend/llm-orchestrator/src/prompts/variant_selection.py`
- [ ] T263 [US1] [US2] @agent-1 Document primer/prompt versioning and performance tracking in `specs/005-llm-orchestrator/PRIMERS_PROMPTS.md` (doc-only)

#### Safety and Privacy

- [ ] T264 [US1] [US2] @agent-1 Implement PII profile storage system (receive known PII from Frankie's Finance and Veris Finance) in `backend/llm-orchestrator/src/safety/pii_profiles.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 5)
- [ ] T264A [US1] [US2] @agent-1 Implement PII detection using known PII profiles (check queries against known names, addresses, account numbers) in `backend/llm-orchestrator/src/safety/pii_detection.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 5)
- [ ] T264B [US1] [US2] @agent-1 Implement pattern-based PII detection (regex patterns for structured PII) in `backend/llm-orchestrator/src/safety/pii_patterns.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 5)
- [ ] T264C [US1] [US2] @agent-1 Implement PII filtering before sending to OpenRouter API (MANDATORY pre-processing step) in `backend/llm-orchestrator/src/safety/pii_filtering.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 5)
- [ ] T264D [US1] [US2] @agent-1 Implement PII redaction with placeholder replacement in `backend/llm-orchestrator/src/safety/pii_redaction.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 5)
- [ ] T264E [US1] [US2] @agent-1 Implement audit logging to verify no PII in LLM API request payloads in `backend/llm-orchestrator/src/safety/pii_audit.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 5)
- [ ] T265 [US1] [US2] @agent-1 Implement safety content filtering in `backend/llm-orchestrator/src/safety/content_filtering.py`
- [ ] T266 [US1] [US2] @agent-1 Implement PII preservation for internal use (separate storage, mapping system) in `backend/llm-orchestrator/src/safety/pii_preservation.py` (Reference: `specs/005-llm-orchestrator/plan.md` Phase 5)
- [ ] T267 [US1] [US2] @agent-1 Implement user-friendly error messaging in `backend/llm-orchestrator/src/safety/error_messaging.py`
- [ ] T267A [P] [US1] [US2] @agent-1 Tests for PII filtering (verify PII is filtered before LLM calls, verify filtered queries don't contain original PII) in `backend/llm-orchestrator/tests/unit/test_pii_filtering.py` (module-local tests only) (Reference: `specs/005-llm-orchestrator/plan.md` Phase 5)

#### Schema Validation

- [ ] T268 [US1] [US2] @agent-1 Implement LLM output validation against schemas with retry/repair loop (max 3 retries, exponential backoff, type coercion, defaults, normalization, LLM regeneration) in `backend/llm-orchestrator/src/validation/schema_validation.py` (⚠️ FREEZE C: validation rules - no [P] after freeze) (Reference: `specs/005-llm-orchestrator/plan.md` Phase 1, `specs/001-master-spec/master_spec.md` CL-035)
- [ ] T269 [US1] [US2] @agent-1 Implement validation error handling in `backend/llm-orchestrator/src/validation/error_handling.py`
- [ ] T270 [US1] [US2] @agent-1 Implement request validation before forwarding to Compute Engine in `backend/llm-orchestrator/src/validation/request_validation.py`

#### APIs

- [ ] T271 [US1] [US2] @agent-1 Implement `POST /llm/parse` (intent parsing) in `backend/llm-orchestrator/src/api/parse.py` (⚠️ FREEZE C: OpenAPI contract - no [P] after freeze)
- [ ] T272 [US1] [US2] @agent-1 Implement `POST /llm/chat` (conversational interface) in `backend/llm-orchestrator/src/api/chat.py` (⚠️ FREEZE C: OpenAPI contract - no [P] after freeze)
- [ ] T272C [US1] [US2] @agent-1 Generate OpenAPI specification for LLM Orchestrator APIs (`POST /llm/parse`, `POST /llm/chat`, `GET /llm/costs`, `GET /llm/costs/caps`, `PUT /llm/costs/caps`) in `specs/001-master-spec/contracts/llm-orchestrator-openapi.yaml` (CRITICAL: Must be generated before FREEZE C - required for contract validation) (exclusive paths: specs only)
- [ ] T272A [US1] [US2] @agent-1 Implement circuit breaker for Compute Engine calls from LLM Orchestrator in `backend/llm-orchestrator/src/api/compute_engine_circuit_breaker.py` (prevent blocking on Compute Engine failures)
- [ ] T272B [US1] [US2] @agent-1 Implement timeout handling for LLM→Compute Engine calls in `backend/llm-orchestrator/src/api/compute_engine_timeout.py` (handle Compute Engine timeouts)
- [ ] T273 [US1] [US2] @agent-1 Implement rate limiting per vendor and tenant in `backend/llm-orchestrator/src/api/rate_limiting.py`

#### Testing

- [ ] T274 [P] [US1] [US2] @agent-1 Unit tests for intent detection in `backend/llm-orchestrator/tests/unit/test_intent.py` (module-local tests only)
- [ ] T275 [P] [US1] [US2] @agent-1 Integration tests with Compute Engine in `backend/llm-orchestrator/tests/integration/test_compute_engine.py` (module-local tests only)
- [ ] T276 [P] [US1] [US2] @agent-1 LLM output validation tests in `backend/llm-orchestrator/tests/unit/test_validation.py` (module-local tests only)
- [ ] T277 [P] [US1] [US2] @agent-1 PII filtering tests in `backend/llm-orchestrator/tests/unit/test_pii_filtering.py` (module-local tests only)
- [ ] T278 [P] [US1] [US2] @agent-1 Performance tests (latency, cost) in `backend/llm-orchestrator/tests/performance/test_performance.py` (module-local tests only)
- [ ] T279 [P] [US1] [US2] @agent-1 Tests for token tracking (input/output/cached tokens) in `backend/llm-orchestrator/tests/unit/test_token_tracking.py` (module-local tests only)
- [ ] T280 [P] [US1] [US2] @agent-1 Tests for cost calculation based on token usage in `backend/llm-orchestrator/tests/unit/test_cost_calculation.py` (module-local tests only)
- [ ] T281 [P] [US1] [US2] @agent-1 Tests for primer/prompt A/B versioning system in `backend/llm-orchestrator/tests/unit/test_prompts_versioning.py` (module-local tests only)
- [ ] T282 [P] [US1] [US2] @agent-1 Tests for performance measurement and variant selection in `backend/llm-orchestrator/tests/unit/test_prompts_performance.py` (module-local tests only)
- [ ] T282A [P] [US1] [US2] @agent-1 Security tests for cross-tenant data access prevention in LLM Orchestrator per FR-031A in `backend/llm-orchestrator/tests/security/test_cross_tenant_access.py` (tests bugs, misconfigured queries, malicious input, missing tenant context to ensure User A cannot access User B's conversation history, extracted parameters, or LLM-generated content) (module-local tests only)

#### RAG Capability Integration (Phase 7, Days 9-12)

**NOTE**: Plan describes this as "Phase 7" but implementation occurs during Phase 3 (Days 9-12) to enable RAG functionality for Advice Engine workflows. The plan's Phase 7 designation refers to the feature's maturity/completeness level, not the implementation phase.

**Reference**: `specs/005-llm-orchestrator/spec_005_llm_orchestrator.md` and `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7

**RAG Key Points** (from `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md`):
- **Retrieval**: PostgreSQL JSONB + Redis caching (80% hit rate target, <1s latency p95, 95% relevance target)
- **Model Routing**: gpt-5-mini for retrieval queries, gpt-5.1 for generation when needed
- **Compliance**: Principle IV compliant (LLM remains translator only; retrieved data grounds prompts but does not make LLM the source of truth)
- **Security**: Tenant isolation (RLS) and PII redaction enforced in all RAG operations
- **Integration**: References & Research Engine APIs (`/references/search`, `/references/{id}`) for data retrieval

- [ ] T282B [US1] [US2] @agent-1 Implement RAGRetriever class for retrieving relevant structured data (rules, references, assumptions, advice guidance, client outcome strategies) from relational database in `backend/llm-orchestrator/src/rag/retriever.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7, `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282B1 [US1] [US2] @agent-1 Integrate RAG retrieval with References & Research Engine APIs (`/references/search`, `/references/{id}`) in `backend/llm-orchestrator/src/rag/references_integration.py` (Reference: `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282C [US1] [US2] @agent-1 Implement query builder for semantic/keyword search on PostgreSQL JSONB metadata (no new data stores) in `backend/llm-orchestrator/src/rag/query_builder.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7, `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282D [US1] [US2] @agent-1 Implement Redis caching for frequent RAG retrievals (cache key: `rag:{query_hash}:{filters_hash}:{tenant_id}`, TTL: 1 hour, target: 80% cache hit rate, <1s latency p95) in `backend/llm-orchestrator/src/rag/cache.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7, `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282E [US1] [US2] @agent-1 Implement formatter for prompt augmentation with citation generation in `backend/llm-orchestrator/src/rag/formatter.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7)
- [ ] T282F [US1] [US2] @agent-1 Enhance intent detection with RAG retrieval (augment prompts, include citations) in `backend/llm-orchestrator/src/intent/rag_enhancement.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7)
- [ ] T282G [US1] [US2] @agent-1 Enhance conversational interface with RAG retrieval (augment prompts, include citations) in `backend/llm-orchestrator/src/conversation/rag_enhancement.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7)
- [ ] T282H [US1] [US2] @agent-1 Add optional `use_rag` flag to `/llm/parse` and `/llm/chat` APIs for RAG-enhanced processing in `backend/llm-orchestrator/src/api/parse.py` and `backend/llm-orchestrator/src/api/chat.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7, `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282I [US1] [US2] @agent-1 Implement model routing for RAG (use cheaper models gpt-5-mini for retrieval queries, switch to higher-capability models gpt-5.1 for generation when needed) in `backend/llm-orchestrator/src/rag/model_routing.py` (Reference: `specs/005-llm-orchestrator/plan_005_llm_orchestrator.md` Phase 7, `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282I1 [US1] [US2] @agent-1 Ensure RAG complies with Principle IV: LLM remains translator only; retrieved data grounds prompts but does not make LLM the source of truth in `backend/llm-orchestrator/src/rag/compliance.py` (Reference: `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282I2 [US1] [US2] @agent-1 Ensure retrieved data respects tenant isolation (RLS) and PII redaction in `backend/llm-orchestrator/src/rag/tenant_isolation.py` (Reference: `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282J [P] [US1] [US2] @agent-1 Tests for RAG retrieval (95% relevance target, <1s latency p95, tenant isolation) in `backend/llm-orchestrator/tests/integration/test_rag.py` (module-local tests only, Reference: `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282K [P] [US1] [US2] @agent-1 Tests for RAG constitution compliance (Principle IV validation, tenant isolation, PII redaction) in `backend/llm-orchestrator/tests/integration/test_rag_compliance.py` (module-local tests only, Reference: `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282L [P] [US1] [US2] @agent-1 End-to-end tests for RAG via Veris/Frankie's UIs in `backend/llm-orchestrator/tests/e2e/test_rag_ui_integration.py` (module-local tests only, Reference: `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282M [P] [US1] [US2] @agent-1 Golden dataset validation for RAG retrieval accuracy in `backend/llm-orchestrator/tests/golden/test_rag_golden.py` (module-local tests only, Reference: `specs/001-master-spec/master_plan.md` Phase 3)
- [ ] T282N [P] [US1] [US2] @agent-1 Property-based tests for RAG edge cases in `backend/llm-orchestrator/tests/property/test_rag_edge_cases.py` (module-local tests only, Reference: `specs/001-master-spec/master_plan.md` Phase 3)

#### Testing

- [ ] T226 [P] [US1] [US2] @agent-1 Unit tests for compliance logic in `backend/advice-engine/tests/unit/test_compliance.py` (module-local tests only)
- [ ] T227 [P] [US1] [US2] @agent-1 Integration tests with Compute Engine in `backend/advice-engine/tests/integration/test_compute_engine.py` (module-local tests only)
- [ ] T228 [P] [US1] [US2] @agent-1 Golden dataset tests (ASIC compliance examples) in `backend/advice-engine/tests/golden/test_asic_examples.py` (module-local tests only)
- [ ] T228A [US1] [US2] @agent-1 **CRITICAL - Minimum Validation Suite**: Collect and validate at least 5 ASIC compliance examples (best interests duty checks, conflict detection, advice documentation requirements) in `backend/advice-engine/tests/golden/test_asic_minimum_validation.py` - must match ASIC examples exactly (module-local tests only)
- [ ] T229 [P] [US1] [US2] @agent-1 Deterministic reproducibility tests in `backend/advice-engine/tests/integration/test_determinism.py` (module-local tests only)
- [ ] T229A [P] [US1] [US2] @agent-1 Security tests for cross-tenant data access prevention in Advice Engine per FR-014A in `backend/advice-engine/tests/security/test_cross_tenant_access.py` (tests bugs, misconfigured queries, malicious input, missing tenant context to ensure User A cannot access User B's compliance evaluations, advice guidance, or client outcome strategies) (module-local tests only)

**Checkpoint**: Phase 3 complete - Advice Engine operational, compliance checking functional, compliance documentation complete (checklist generation, completion tracking, export functionality, scenario linking), audit and reporting complete (comprehensive audit logging, audit trail export, historical reconstruction, time-travel queries), integration with Compute Engine working, LLM Orchestrator progress for compliance workflows, RAG capability implemented (RAGRetriever, References & Research Engine integration, semantic/keyword search on PostgreSQL JSONB, Redis caching, model routing, Principle IV compliance, tenant isolation, PII redaction, comprehensive test coverage), test coverage > 80%

---

## Phase 4: Veris Finance (Days 11-12)

**Purpose**: Build Veris Finance and update LLM Orchestrator to deliver this app

**Priority**: P1 (adviser UX - developed before Frankie's Finance per user guidance)

**Dependencies**: Phase 0 complete, Phase 1 (References & Research Engine) complete, Phase 2 complete (Phase 2A-2D: Knowledge base seeded, canonical list populated, test harness built, Compute Engine operational), Phase 3 (Advice Engine) complete

---

## Phase 4: Veris Finance (Days 11-12)

**Priority**: P1 (adviser UX - developed before Frankie's Finance per user guidance)

**Dependencies**: Phase 0 complete, Phase 1 (References & Research Engine) complete, Phase 2 complete (Phase 2A-2D: Knowledge base seeded, canonical list populated, test harness built, Compute Engine operational), Phase 3 (Advice Engine) complete

#### Frontend Dependency Versioning

- [ ] T283 [P] [US2] @agent-1 Document React version compatibility matrix (React 18.2.0 for Veris Finance) in `frontend/veris-finance/VERSION_COMPATIBILITY.md` (doc-only)
- [ ] T284 [P] [US2] @agent-1 Create shared component library with version constraints in `frontend/shared/components/` and pin React/TypeScript versions (exclusive paths: frontend/shared only)
- [ ] T285 [P] [US2] @agent-1 Pin TypeScript version (typescript@5.3.3) and document compatibility with React in `frontend/veris-finance/package.json` (exclusive paths: frontend/veris-finance only)

#### Professional Interface

- [ ] T337 [US2] @agent-1 Design professional calm UI (cool neutrals, crisp typography) in `frontend/veris-finance/src/styles/theme.ts`
- [ ] T338 [US2] @agent-1 Implement minimal chrome, clear hierarchy in `frontend/veris-finance/src/components/layout/AppLayout.tsx`
- [ ] T339 [US2] @agent-1 Implement data-centric visualizations (charts, graphs) in `frontend/veris-finance/src/components/visualizations/`
- [ ] T340 [US2] @agent-1 Implement audit log always available in `frontend/veris-finance/src/components/audit/AuditLog.tsx`
- [ ] T341 [US2] @agent-1 Implement two-column layouts for client summaries in `frontend/veris-finance/src/components/client/ClientSummary.tsx`

#### LLM Chat Interface

- [ ] T342 [US2] @agent-1 Integrate with LLM Orchestrator (`POST /llm/chat`, `POST /llm/parse`) in `frontend/veris-finance/src/services/llmService.ts`
- [ ] T343 [US2] @agent-1 Implement natural language input for client data in `frontend/veris-finance/src/components/chat/ChatInput.tsx`
- [ ] T344 [US2] @agent-1 Implement structured replies and clickable commands in `frontend/veris-finance/src/components/chat/ChatResponse.tsx`
- [ ] T345 [US2] @agent-1 Implement conversation context for client scenarios in `frontend/veris-finance/src/hooks/useConversationContext.ts`

#### Client Management

- [ ] T346 [US2] @agent-1 Implement client record creation and management in `frontend/veris-finance/src/services/clientService.ts`
- [ ] T347 [US2] @agent-1 Implement natural language and structured input in `frontend/veris-finance/src/components/client/ClientForm.tsx`
- [ ] T348 [US2] @agent-1 Implement multiple clients per adviser support in `frontend/veris-finance/src/components/client/ClientList.tsx`
- [ ] T349 [US2] @agent-1 Implement client data import in `frontend/veris-finance/src/services/importService.ts`

#### Client PII Collection and Privacy Explanation (User Story 5 from Master Spec)

**Goal**: Implement client PII collection during client setup with detailed privacy explanation. Advisers must see privacy explanation before processing any client queries.

**Independent Test**: Adviser can complete client setup, see detailed privacy explanation covering PII handling, filtering process, compliance with Australian Privacy Act 1988, access privacy policy, and view privacy settings. Client PII profile is stored and integrated with LLM Orchestrator.

**Reference**: `specs/001-master-spec/master_spec.md` User Story 5, FR-072, FR-073, FR-074, FR-075, FR-076, FR-077, FR-078, FR-079, `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3

- [ ] T349A [P] [US2] [US5] @agent-1 Create client setup form component with comprehensive PII collection (name, DOB, address, contact details, account numbers, TFN, etc.) in `frontend/veris-finance/src/components/client/ClientSetupForm.tsx` (Reference: `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)
- [ ] T349B [US2] [US5] @agent-1 Create ClientPIIProfile type and storage in `frontend/veris-finance/src/types/client-pii-profile.ts` (Reference: `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)
- [ ] T349C [US2] [US5] @agent-1 Implement client PII profile storage service in `frontend/veris-finance/src/services/client-pii-profile.ts` (Reference: `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)
- [ ] T349D [US2] [US5] @agent-1 Create detailed privacy explanation screen component covering PII handling, filtering process, Australian Privacy Act 1988 compliance in `frontend/veris-finance/src/screens/ClientPrivacyExplanationScreen.tsx` (Reference: `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)
- [ ] T349E [US2] [US5] @agent-1 Implement privacy policy access (link/button) in `frontend/veris-finance/src/components/PrivacyPolicyLink.tsx` (Reference: `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)
- [ ] T349F [US2] [US5] @agent-1 Create professional privacy language component for client communication in `frontend/veris-finance/src/components/ProfessionalPrivacyLanguage.tsx` (Reference: `specs/001-master-spec/master_spec.md` FR-077, `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)
- [ ] T349G [US2] [US5] @agent-1 Create privacy settings screen accessible at any time in `frontend/veris-finance/src/screens/PrivacySettingsScreen.tsx` (Reference: `specs/001-master-spec/master_spec.md` FR-079, `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)
- [ ] T349H [US2] [US5] @agent-1 Implement privacy settings navigation and access from any screen (Reference: `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)
- [ ] T349I [US2] [US5] @agent-1 Integrate client PII profile with LLM Orchestrator API client for enhanced filtering (comprehensive known client identifiers enable highly effective filtering) (Reference: `specs/001-master-spec/master_spec.md` FR-076, `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)
- [ ] T349J [US2] [US5] @agent-1 Implement client setup completion check: block client queries until privacy explanation viewed (Reference: `specs/001-master-spec/master_spec.md` FR-078, `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)
- [ ] T349K [US2] [US5] @agent-1 Handle incomplete client information: still display privacy explanation, filter whatever PII is available (Reference: `specs/007-veris-finance/plan_007_veris_finance.md` Phase 3)

#### Scenario Modelling and Forecasting

- [ ] T350 [US2] @agent-1 Integrate with Compute Engine (`POST /run`, `POST /run-batch`, `GET /facts`) in `frontend/veris-finance/src/services/computeService.ts`
- [ ] T351 [US2] @agent-1 Implement scenario creation and management in `frontend/veris-finance/src/components/scenarios/ScenarioManager.tsx`
- [ ] T352 [US2] @agent-1 Implement professional forecast visualizations (line charts, bar graphs) in `frontend/veris-finance/src/components/scenarios/ForecastCharts.tsx`
- [ ] T353 [US2] @agent-1 Implement sensitivity analysis and stress-testing in `frontend/veris-finance/src/components/scenarios/SensitivityAnalysis.tsx`
- [ ] T354 [US2] @agent-1 Implement expandable tiles showing assumptions and results in `frontend/veris-finance/src/components/scenarios/ScenarioTile.tsx`

#### Strategy Comparison

- [ ] T355 [US2] @agent-1 Implement side-by-side strategy comparison in `frontend/veris-finance/src/components/comparison/StrategyComparison.tsx`
- [ ] T356 [US2] @agent-1 Implement key difference highlighting in `frontend/veris-finance/src/components/comparison/DifferenceHighlight.tsx`
- [ ] T357 [US2] @agent-1 Implement evidence-based recommendation support in `frontend/veris-finance/src/components/comparison/Recommendations.tsx`

#### Compliance and Validation

- [ ] T358 [US2] @agent-1 Integrate with Advice Engine (`POST /advice/check`, `GET /advice/requirements`) in `frontend/veris-finance/src/services/adviceService.ts`
- [ ] T359 [US2] @agent-1 Implement compliance validation display in `frontend/veris-finance/src/components/compliance/ComplianceStatus.tsx`
- [ ] T360 [US2] @agent-1 Implement compliance status, warnings, and required actions in `frontend/veris-finance/src/components/compliance/ComplianceWarnings.tsx`
- [ ] T361 [US2] @agent-1 Prevent non-compliant advice document generation in `frontend/veris-finance/src/components/compliance/ComplianceGate.tsx`

#### Documentation Generation

- [ ] T362 [US2] @agent-1 Implement Statement of Advice (SOA) generation in `frontend/veris-finance/src/services/documentGeneration/soa.ts`
- [ ] T363 [US2] @agent-1 Implement Record of Advice (ROA) generation in `frontend/veris-finance/src/services/documentGeneration/roa.ts`
- [ ] T364 [US2] @agent-1 Include calculations, compliance results, and traceable explanations in `frontend/veris-finance/src/services/documentGeneration/content.ts`
- [ ] T365 [US2] @agent-1 Implement client-side PDF generation using browser print-to-PDF with print-optimized CSS stylesheets in `frontend/veris-finance/src/services/documentGeneration/pdf.ts` (Reference: `specs/007-veris-finance/plan.md` Phase 7, `specs/001-master-spec/master_spec.md` CL-033)
- [ ] T365A [US2] @agent-1 Implement print-ready CSS for SOA/ROA templates in `frontend/veris-finance/src/styles/print.css` (Reference: `specs/007-veris-finance/plan.md` Phase 7)
- [ ] T365B [US2] @agent-1 Implement evidence pack export (JSON and PDF formats) with version information, timestamps, and complete provenance chains in `frontend/veris-finance/src/services/documentGeneration/evidencePack.ts` (Reference: `specs/007-veris-finance/plan.md` Phase 7, `specs/001-master-spec/master_spec.md` CL-033)
- [ ] T365C [US2] @agent-1 Export documents for client presentation and regulatory submission in `frontend/veris-finance/src/services/documentGeneration/export.ts`

#### Audit Trail and Explainability

- [ ] T366 [US2] @agent-1 Implement transparent audit log in `frontend/veris-finance/src/components/audit/AuditTrail.tsx`
- [ ] T367 [US2] @agent-1 Integrate with Compute Engine `/explain/{fact_id}` endpoints in `frontend/veris-finance/src/services/explainService.ts`
- [ ] T368 [US2] @agent-1 Implement audit trail export for regulatory review in `frontend/veris-finance/src/services/auditExport.ts`
- [ ] T369 [US2] @agent-1 Implement time-travel queries for historical advice in `frontend/veris-finance/src/services/timeTravel.ts`

#### Testing

- [ ] T370 [P] [US2] @agent-1 Unit tests for UI components in `frontend/veris-finance/tests/unit/` (module-local tests only)
- [ ] T371 [P] [US2] @agent-1 Integration tests with backend modules in `frontend/veris-finance/tests/integration/` (module-local tests only)
- [ ] T372 [P] [US2] @agent-1 End-to-end tests (Playwright) in `frontend/veris-finance/tests/e2e/` (module-local tests only)
- [ ] T373 [US2] @agent-1 **Test Forecasts**: All calculations tested via Veris Finance test forecasts (per user guidance) in `frontend/veris-finance/tests/test_forecasts/`

**Checkpoint**: Phase 4 complete - Veris Finance operational, professional interface functional, scenario modelling working, compliance validation integrated, document generation working, LLM Orchestrator updated for Veris Finance workflows, test coverage > 80%, all calculations validated via Veris Finance test forecasts

---

### Phase 5: Frankie's Finance (Days 13-14)

**Priority**: P1 (consumer UX - developed after Veris Finance per user guidance)

**Dependencies**: Phase 0 complete, Phase 1 (References & Research Engine) complete, Phase 2 complete (Phase 2A-2D: Knowledge base seeded, canonical list populated, test harness built, Compute Engine operational), Phase 3 (Advice Engine) complete, Phase 4 (Veris Finance) complete

#### Frontend Dependency Versioning

- [ ] T286 [P] [US1] @agent-1 Document React Native version compatibility matrix (React Native 0.72.6, React 18.2.0 for Frankie's Finance) in `frontend/frankies-finance/VERSION_COMPATIBILITY.md` (doc-only)
- [ ] T287 [P] [US1] @agent-1 Ensure shared component library compatibility with React Native in `frontend/shared/components/` (test React Native 0.72.6 compatibility) (exclusive paths: frontend/shared only)
- [ ] T288 [P] [US1] @agent-1 Pin Playwright version (playwright==1.40.1) or Cypress version (cypress@13.6.0) for E2E tests in `frontend/frankies-finance/package.json` (exclusive paths: frontend/frankies-finance only)

#### Project Setup (React Native/Expo)

- [ ] T412 [US1] @agent-1 Create Expo project structure in `frontend/frankies-finance/`
- [ ] T413 [US1] @agent-1 Configure package.json with dependencies: expo, react-native, react-navigation, zustand, @tanstack/react-query, @tamagui/core, @tamagui/config, sentry-expo
- [ ] T414 [US1] @agent-1 Set up TypeScript configuration in `frontend/frankies-finance/tsconfig.json`
- [ ] T415 [P] [US1] @agent-1 Configure Tamagui design tokens in `frontend/frankies-finance/src/theme/`
- [ ] T416 [P] [US1] @agent-1 Set up Sentry error tracking in `frontend/frankies-finance/src/services/error-tracking.ts`
- [ ] T417 [P] [US1] @agent-1 Create project folder structure: `src/components/`, `src/screens/`, `src/services/`, `src/hooks/`, `src/navigation/`, `src/stores/`, `src/types/`
- [ ] T418 [US1] @agent-1 Configure environment variables for API endpoints in `frontend/frankies-finance/.env.example`
- [ ] T419 [US1] @agent-1 Set up Jest and React Native Testing Library in `frontend/frankies-finance/`
- [ ] T420 [US1] @agent-1 Configure Expo EAS build settings in `frontend/frankies-finance/eas.json`

#### Foundational Infrastructure

- [ ] T421 [P] [US1] @agent-1 Implement React Navigation setup in `frontend/frankies-finance/src/navigation/AppNavigator.tsx`
- [ ] T422 [P] [US1] @agent-1 Create Zustand store structure in `frontend/frankies-finance/src/stores/`
- [ ] T423 [P] [US1] @agent-1 Implement TanStack Query setup with API client in `frontend/frankies-finance/src/services/api-client.ts`
- [ ] T424 [P] [US1] @agent-1 Create API service interfaces for LLM Orchestrator in `frontend/frankies-finance/src/services/llm-orchestrator.ts`
- [ ] T425 [P] [US1] @agent-1 Create API service interfaces for Compute Engine in `frontend/frankies-finance/src/services/compute-engine.ts`
- [ ] T426 [P] [US1] @agent-1 Create API service interfaces for Advice Engine in `frontend/frankies-finance/src/services/advice-engine.ts`
- [ ] T427 [US1] @agent-1 Implement authentication flow integration in `frontend/frankies-finance/src/services/auth.ts`
- [ ] T428 [US1] @agent-1 Implement AsyncStorage persistence utilities in `frontend/frankies-finance/src/services/storage.ts`
- [ ] T429 [US1] @agent-1 Create shared types and interfaces in `frontend/frankies-finance/src/types/`
- [ ] T430 [US1] @agent-1 Implement offline detection and connectivity handling in `frontend/frankies-finance/src/hooks/useConnectivity.ts`

#### Initial Setup & PII Filtering Transparency (User Story 4 from Master Spec)

**Goal**: Implement initial setup flow with PII collection and privacy explanation. Users must complete setup and see privacy explanation before asking financial questions.

**Independent Test**: New user can complete initial setup, see privacy explanation, access privacy policy, and view privacy settings. PII profile is stored and integrated with LLM Orchestrator.

**Reference**: `specs/001-master-spec/master_spec.md` User Story 4, FR-067, FR-068, FR-069, FR-070, FR-071, FR-078, FR-079

- [ ] T431 [P] [US1] [US4] @agent-1 Create initial setup screen component in `frontend/frankies-finance/src/screens/SetupScreen.tsx`
- [ ] T432 [P] [US1] [US4] @agent-1 Implement PII collection form (name, DOB, suburb) in `frontend/frankies-finance/src/components/SetupForm.tsx`
- [ ] T433 [US1] [US4] @agent-1 Create UserPIIProfile type and storage in `frontend/frankies-finance/src/types/user-pii-profile.ts`
- [ ] T434 [US1] [US4] @agent-1 Implement PII profile storage service in `frontend/frankies-finance/src/services/pii-profile.ts`
- [ ] T435 [US1] [US4] @agent-1 Create privacy explanation screen component in `frontend/frankies-finance/src/screens/PrivacyExplanationScreen.tsx`
- [ ] T436 [US1] [US4] @agent-1 Implement privacy policy access (link/button) in `frontend/frankies-finance/src/components/PrivacyPolicyLink.tsx`
- [ ] T437 [US1] [US4] @agent-1 Create privacy settings screen in `frontend/frankies-finance/src/screens/PrivacySettingsScreen.tsx`
- [ ] T438 [US1] [US4] @agent-1 Implement privacy settings navigation and access from any screen
- [ ] T439 [US1] [US4] @agent-1 Integrate PII profile with LLM Orchestrator API client for enhanced filtering (Reference: FR-071)
- [ ] T440 [US1] [US4] @agent-1 Implement setup completion check: block financial questions until privacy explanation viewed (Reference: FR-078)
- [ ] T441 [US1] [US4] @agent-1 Handle setup skip/cancel: still display privacy info before allowing queries (Reference: FR-078)

#### Spatial Navigation and Environments (Polish & Cross-Cutting)

- [ ] T380 [US1] @agent-1 Design five environments (path, front door, living room, study, garden) in `frontend/frankies-finance/src/designs/environments.md` (doc-only)
- [ ] T475 [P] [US1] @agent-1 Implement Path environment screen in `frontend/frankies-finance/src/screens/PathScreen.tsx`
- [ ] T476 [P] [US1] @agent-1 Implement Front Door environment screen in `frontend/frankies-finance/src/screens/FrontDoorScreen.tsx`
- [ ] T381 [US1] @agent-1 Implement non-linear navigation in `frontend/frankies-finance/src/navigation/SpatialNavigation.tsx`
- [ ] T383 [US1] @agent-1 Implement smooth transitions between environments in `frontend/frankies-finance/src/navigation/Transitions.tsx`
- [ ] T384 [US1] @agent-1 Implement persistent state per environment in `frontend/frankies-finance/src/stores/environment-state.ts`
- [ ] T477 [US1] @agent-1 Implement alternative navigation (menu/tabs) for accessibility

#### Frankie Companion (Polish & Cross-Cutting)

- [ ] T478 [P] [US1] @agent-1 Create Frankie component with behaviors in `frontend/frankies-finance/src/components/Frankie.tsx`
- [ ] T479 [P] [US1] @agent-1 Implement Frankie animations (wagging, running, sitting, lying, soft bark) in `frontend/frankies-finance/src/components/FrankieAnimations.tsx`
- [ ] T382 [US1] @agent-1 Implement visual navigation cues (wagging ahead, looking expectantly) in `frontend/frankies-finance/src/components/frankie/FrankieCompanion.tsx`
- [ ] T480 [US1] @agent-1 Implement Frankie in all environments (continuity)

#### User Story 1 - "What should I do?" Decision Guidance (Priority: P1)

**Goal**: Users can ask financial questions and receive personalized guidance with visual forecasts, compliance validation, and explainable insights.

**Independent Test**: User can ask "Should I contribute more to super?" in living room, receive conversational response with visual forecasts, see compliance validation, and understand recommendation through explainable insights.

- [ ] T443 [P] [US1] @agent-1 Create LivingRoomScreen component in `frontend/frankies-finance/src/screens/LivingRoomScreen.tsx`
- [ ] T444 [P] [US1] @agent-1 Implement natural language input component (text/voice) in `frontend/frankies-finance/src/components/QueryInput.tsx`
- [ ] T385 [US1] @agent-1 Integrate with LLM Orchestrator (`POST /llm/chat`, `POST /llm/parse`) in `frontend/frankies-finance/src/services/llmService.ts`
- [ ] T386 [US1] @agent-1 Implement text and voice input in `frontend/frankies-finance/src/components/chat/InputMethods.tsx`
- [ ] T387 [US1] @agent-1 Implement conversation context maintenance in `frontend/frankies-finance/src/hooks/useConversationContext.ts`
- [ ] T481 [US1] @agent-1 Implement LLM Orchestrator integration for query processing in `frontend/frankies-finance/src/hooks/useLLMQuery.ts`
- [ ] T388 [US1] @agent-1 Implement consumer-friendly response formatting in `frontend/frankies-finance/src/components/chat/ResponseFormatter.tsx`
- [ ] T442 [US1] @agent-1 Ensure collected user name is used by LLM Orchestrator for enhanced PII filtering (known name enables more accurate detection of name references in queries) (Reference: `specs/001-master-spec/master_spec.md` FR-071)
- [ ] T373A [US1] @agent-1 Integrate with Compute Engine (`POST /run`, `GET /facts`, `GET /explain/{fact_id}`) in `frontend/frankies-finance/src/services/computeService.ts`
- [ ] T482 [US1] @agent-1 Implement Compute Engine integration for calculation execution in `frontend/frankies-finance/src/hooks/useCalculation.ts`
- [ ] T445 [US1] @agent-1 Create conversation display component in `frontend/frankies-finance/src/components/ConversationDisplay.tsx`
- [ ] T376 [US1] @agent-1 Implement visual forecast component (charts/graphs) in `frontend/frankies-finance/src/components/guidance/ForecastVisualization.tsx`
- [ ] T374 [US1] @agent-1 Integrate with Advice Engine (`POST /advice/check`) in `frontend/frankies-finance/src/services/adviceService.ts` (per FR-039: connect Frankie's Finance to compliance validation)
- [ ] T377 [US1] @agent-1 Implement compliance validation integration (connect to Advice Engine, validate all financial advice) in `frontend/frankies-finance/src/services/complianceIntegration.ts` (per FR-039: ensure all financial advice provided to consumers is validated for compliance)
- [ ] T483 [US1] @agent-1 Implement Advice Engine integration for compliance validation in `frontend/frankies-finance/src/hooks/useComplianceCheck.ts`
- [ ] T378 [US1] @agent-1 Create compliance validation display component (consumer-friendly) in `frontend/frankies-finance/src/components/compliance/ConsumerCompliance.tsx` (per FR-040: display compliance validation results in consumer-friendly, non-technical manner)
- [ ] T379 [US1] @agent-1 Implement explainable insights component linking to rules/references in `frontend/frankies-finance/src/components/guidance/ExplainableInsights.tsx`
- [ ] T446 [US1] @agent-1 Create pros/cons display component in `frontend/frankies-finance/src/components/ProsConsDisplay.tsx`
- [ ] T447 [US1] @agent-1 Implement error handling for questions outside rule coverage (supportive message)
- [ ] T448 [US1] @agent-1 Implement error handling for compliance failures (consumer-friendly message)

#### User Story 2 - "Explain this to me." Financial Literacy Companion (Priority: P1)

**Goal**: Users can ask about financial terms/concepts and receive clear, jargon-free explanations with visual analogies and citations.

**Independent Test**: User can ask "What's capital gains tax?" and receive clear, jargon-free explanation with visual analogies, links to authoritative sources, and ability to ask follow-up questions.

- [ ] T449 [P] [US1] @agent-1 Create financial explanation display component in `frontend/frankies-finance/src/components/FinancialExplanation.tsx`
- [ ] T450 [P] [US1] @agent-1 Implement visual analogies and metaphors component in `frontend/frankies-finance/src/components/VisualAnalogies.tsx`
- [ ] T451 [US1] @agent-1 Create citation display component for authoritative sources in `frontend/frankies-finance/src/components/CitationDisplay.tsx`
- [ ] T452 [US1] @agent-1 Implement follow-up question handling (maintain conversation context) - extends T387
- [ ] T453 [US1] @agent-1 Create interactive explanation elements component in `frontend/frankies-finance/src/components/InteractiveExplanation.tsx`
- [ ] T454 [US1] @agent-1 Implement progressive explanation depth (deeper explanations on follow-up)

#### User Story 3 - "Run the numbers." Scenario Simulation (Priority: P1)

**Goal**: Users can test different financial scenarios, compare outcomes, and adjust parameters in real-time with visual charts.

**Independent Test**: User can ask "What happens if I retire at 58 instead of 65?" in study, view comparative forecasts with visual charts, adjust parameters using sliders, and see outcomes update in real-time.

- [ ] T455 [P] [US1] @agent-1 Create StudyScreen component in `frontend/frankies-finance/src/screens/StudyScreen.tsx`
- [ ] T456 [P] [US1] @agent-1 Implement scenario input component (chat-driven prompts) in `frontend/frankies-finance/src/components/ScenarioInput.tsx`
- [ ] T457 [US1] @agent-1 Create interactive slider components for parameter adjustment in `frontend/frankies-finance/src/components/ParameterSliders.tsx`
- [ ] T392 [US1] @agent-1 Implement real-time calculation updates on parameter change in `frontend/frankies-finance/src/components/scenarios/ParameterAdjustment.tsx`
- [ ] T484 [US1] @agent-1 Implement real-time calculation updates on parameter change in `frontend/frankies-finance/src/hooks/useRealTimeCalculation.ts`
- [ ] T458 [US1] @agent-1 Create scenario comparison component (side-by-side) in `frontend/frankies-finance/src/components/ScenarioComparison.tsx`
- [ ] T459 [US1] @agent-1 Implement scenario storage and tagging in `frontend/frankies-finance/src/services/scenario-storage.ts`
- [ ] T391 [US1] @agent-1 Create scenario visualization component (charts, graphs) in `frontend/frankies-finance/src/components/scenarios/VisualCharts.tsx`
- [ ] T460 [US1] @agent-1 Implement scenario history and retrieval in `frontend/frankies-finance/src/components/ScenarioHistory.tsx`

#### User Story 4 - "Help me plan." Goal Setting & Tracking (Priority: P2)

**Goal**: Users can set financial goals, track progress visually in garden, and receive milestone celebrations.

**Independent Test**: User can set goal "Save $50k for house deposit", track progress in garden, receive milestone reminders, and see how decisions affect goal achievement through visual metaphors.

- [ ] T461 [P] [US1] @agent-1 Create GardenScreen component in `frontend/frankies-finance/src/screens/GardenScreen.tsx`
- [ ] T393 [US1] @agent-1 Implement goal setting component (natural language and structured input) in `frontend/frankies-finance/src/components/goals/GoalSetting.tsx`
- [ ] T462 [US1] @agent-1 Create Goal type and storage in `frontend/frankies-finance/src/types/goal.ts`
- [ ] T463 [US1] @agent-1 Implement goal storage service in `frontend/frankies-finance/src/services/goal-storage.ts`
- [ ] T394 [US1] @agent-1 Create visual goal representation component (trees, flowers) in `frontend/frankies-finance/src/components/goals/GardenVisualization.tsx`
- [ ] T395 [US1] @agent-1 Implement goal progress tracking logic in `frontend/frankies-finance/src/components/goals/ProgressTracking.tsx`
- [ ] T485 [US1] @agent-1 Implement goal progress tracking logic in `frontend/frankies-finance/src/hooks/useGoalProgress.ts`
- [ ] T464 [US1] @agent-1 Create milestone celebration component (Frankie animations) in `frontend/frankies-finance/src/components/MilestoneCelebration.tsx`
- [ ] T465 [US1] @agent-1 Implement goal modification and deletion in `frontend/frankies-finance/src/components/GoalManagement.tsx`
- [ ] T466 [US1] @agent-1 Create goal history tracking component

#### User Story 5 - "Am I on the right track?" Health & Progress Reports (Priority: P2)

**Goal**: Users receive periodic check-ins showing financial health evolution, progress, and risk indicators with supportive messaging.

**Independent Test**: User receives monthly check-in showing financial health evolution, visual indicators of progress, risk identification, and supportive messaging.

- [ ] T467 [P] [US1] @agent-1 Create ProgressReport type and generation logic in `frontend/frankies-finance/src/types/progress-report.ts`
- [ ] T397 [US1] @agent-1 Implement periodic report generation (monthly/quarterly) in `frontend/frankies-finance/src/services/reportService.ts`
- [ ] T398 [US1] @agent-1 Create progress report display component in `frontend/frankies-finance/src/components/reports/ProgressReport.tsx`
- [ ] T468 [US1] @agent-1 Implement on-demand report generation in `frontend/frankies-finance/src/hooks/useProgressReport.ts`
- [ ] T469 [US1] @agent-1 Create risk indicator display component (supportive language) in `frontend/frankies-finance/src/components/RiskIndicators.tsx`
- [ ] T399 [US1] @agent-1 Implement supportive, non-alarming language in `frontend/frankies-finance/src/components/reports/ReportLanguage.tsx`
- [ ] T400 [US1] @agent-1 Implement achievement celebration in reports (Frankie animations)

#### User Story 6 - "See My Future." Easy-to-Use Forecasting (Priority: P2)

**Goal**: Users can easily create forecasts of financial future with chat-driven prompts or sliders, seeing forecasts adjust live.

**Independent Test**: User can ask "What will my super look like at 65?" using chat-driven prompts or sliders, see forecasts adjust live as parameters change, with Frankie narrating what's happening.

- [ ] T470 [P] [US1] @agent-1 Create forecasting input component (chat-driven prompts) in `frontend/frankies-finance/src/components/ForecastingInput.tsx`
- [ ] T471 [P] [US1] @agent-1 Implement live forecast updates on parameter change in `frontend/frankies-finance/src/hooks/useLiveForecast.ts`
- [ ] T472 [US1] @agent-1 Create forecast visualization component (intuitive charts) in `frontend/frankies-finance/src/components/ForecastDisplay.tsx`
- [ ] T473 [US1] @agent-1 Implement assumption explanation component in `frontend/frankies-finance/src/components/ForecastAssumptions.tsx`
- [ ] T474 [US1] @agent-1 Create Frankie narration component for forecast changes

#### Visual Design and Emotion

- [ ] T401 [US1] @agent-1 Implement emotion-first design in `frontend/frankies-finance/src/styles/emotionTheme.ts`
- [ ] T402 [US1] @agent-1 Implement responsive visual elements (lighting, sound, motion) in `frontend/frankies-finance/src/components/visual/ResponsiveElements.tsx`
- [ ] T403 [US1] @agent-1 Implement organic presentation (notes opening, sketches forming) in `frontend/frankies-finance/src/components/visual/OrganicPresentation.tsx`
- [ ] T404 [US1] @agent-1 Implement warm, welcoming visual language in `frontend/frankies-finance/src/styles/warmTheme.ts`

#### Mobile-First Experience

- [ ] T405 [US1] @agent-1 Implement touch-optimized interface in `frontend/frankies-finance/src/components/mobile/TouchOptimized.tsx`
- [ ] T406 [US1] @agent-1 Implement offline capabilities with AsyncStorage persistence (environment state, conversations, scenarios, goals) in `frontend/frankies-finance/src/services/offlineService.ts` (Reference: `specs/006-frankies-finance/plan_006_frankies_finance.md` Phase 8, `specs/001-master-spec/master_spec.md` CL-034)
- [ ] T406A [US1] @agent-1 Implement TanStack Query cache management for offline API response access in `frontend/frankies-finance/src/services/offlineCache.ts` (Reference: `specs/006-frankies-finance/plan_006_frankies_finance.md` Phase 8)
- [ ] T406B [US1] @agent-1 Implement sync on reconnect (automatic sync of cached changes, refetch stale data) in `frontend/frankies-finance/src/services/syncService.ts` (Reference: `specs/006-frankies-finance/plan_006_frankies_finance.md` Phase 8)
- [ ] T406C [US1] @agent-1 Implement request queue for failed requests (retry on reconnect) in `frontend/frankies-finance/src/services/requestQueue.ts` (Reference: `specs/006-frankies-finance/plan_006_frankies_finance.md` Phase 8)
- [ ] T406D [US1] @agent-1 Implement offline UI indicators and messaging in `frontend/frankies-finance/src/components/mobile/OfflineIndicator.tsx` (Reference: `specs/006-frankies-finance/plan_006_frankies_finance.md` Phase 8)
- [ ] T407 [US1] @agent-1 Implement graceful connectivity handling in `frontend/frankies-finance/src/services/connectivityService.ts`

#### Testing

- [ ] T408 [P] [US1] @agent-1 Unit tests for UI components in `frontend/frankies-finance/tests/unit/` (module-local tests only)
- [ ] T409 [P] [US1] @agent-1 Integration tests with backend modules in `frontend/frankies-finance/tests/integration/` (module-local tests only)
- [ ] T410 [P] [US1] @agent-1 End-to-end tests (React Native Testing Library, Detox) in `frontend/frankies-finance/tests/e2e/` (module-local tests only)
- [ ] T411 [US1] @agent-1 User acceptance tests (emotion-first design validation) in `frontend/frankies-finance/tests/acceptance/`

**Checkpoint**: Phase 5 complete - Frankie's Finance operational, spatial navigation functional, natural language interaction working, financial guidance and advice working, scenario exploration functional, goal tracking working, LLM Orchestrator updated for Frankie's Finance workflows, test coverage > 75%

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple modules and user stories

### Documentation

- [ ] T314 [P] @agent-1 Update API documentation in `specs/001-master-spec/contracts/` (doc-only, exclusive paths: specs only)
- [ ] T315 [P] @agent-1 Update developer quickstart guide in `specs/001-master-spec/quickstart.md` (doc-only, exclusive paths: specs only)
- [ ] T316 [P] @agent-1 Update data model documentation in `specs/001-master-spec/data-model.md` (doc-only, exclusive paths: specs only)

### Performance Optimization

- [ ] T317 [P] @agent-1 Performance optimization across all backend modules (module-local, exclusive paths per module)
- [ ] T318 [P] @agent-1 Performance optimization across all frontend modules (module-local, exclusive paths per module)
- [ ] T319 [P] @agent-1 Caching strategy implementation in `backend/shared/cache/` (SERIAL: shared infrastructure)

### Security Hardening

- [ ] T320 [P] @agent-1 Security audit and penetration testing (exclusive paths: tests/security/ only)
- [ ] T321 [P] @agent-1 Additional security hardening based on audit findings (module-local, exclusive paths per module)

### Testing

- [ ] T322 [P] @agent-1 Additional unit tests for edge cases in all modules (module-local tests only, exclusive paths per module)
- [ ] T323 [P] @agent-1 Load testing for all APIs in `tests/performance/` (exclusive paths: tests/performance/ only)
- [ ] T324 [P] @agent-1 End-to-end integration tests across all modules in `tests/integration/e2e/` (exclusive paths: tests/integration/e2e/ only). Tests MUST validate: (1) Complete user workflows from frontend through all backend modules, (2) API contract compatibility between all module pairs, (3) Error propagation and handling across module boundaries, (4) Data format consistency (request/response schemas), (5) Performance requirements met across module boundaries, (6) Tenant isolation maintained across module boundaries. Reference: `specs/001-master-spec/master_spec.md` FR-025E for cross-module integration test requirements.

### Minimum Validation Suite (CRITICAL - Required Before Shipping)

**Purpose**: Ensure system meets minimum validation requirements before production deployment.

- [ ] T331 [US1] [US2] [US3] @agent-1 **CRITICAL**: Validate at least 10 ATO tax calculation examples (taxable income, tax offsets, deductions, CGT calculations) - all must match ATO examples exactly (within rounding tolerance) in `backend/compute-engine/tests/golden/test_ato_minimum_validation.py` (module-local tests only)
- [ ] T332 [US1] [US2] [US3] @agent-1 **CRITICAL**: Validate at least 5 ASIC compliance examples (best interests duty checks, conflict detection, advice documentation requirements) - all must match ASIC examples exactly in `backend/advice-engine/tests/golden/test_asic_minimum_validation.py` (module-local tests only)
- [ ] T333 [US1] [US2] [US3] @agent-1 **CRITICAL**: Verify 100% deterministic reproducibility (run 1000+ iterations of same calculation, verify 100% identical outputs) across different execution times, servers, and environments in `backend/compute-engine/tests/integration/test_deterministic_reproducibility_validation.py` (module-local tests only)
- [ ] T334 [US1] [US2] [US3] @agent-1 **CRITICAL**: Validate all calculations via Veris Finance test forecasts (test forecasts validate calculation accuracy, provenance chains, and compliance validation) in `frontend/veris-finance/tests/test_forecasts/validation_suite.py` (module-local tests only)
- [ ] T335 @agent-1 **CRITICAL**: Create validation suite report documenting all minimum validation suite results (expected vs actual for ATO/ASIC examples, deterministic reproducibility results, Veris Finance test forecast results) in `tests/validation/MINIMUM_VALIDATION_SUITE_REPORT.md` (doc-only, exclusive paths: tests/validation/ only)
- [ ] T336 @agent-1 **CRITICAL**: Add CI/CD check to fail if minimum validation suite is not complete (must pass before production deployment) in `.github/workflows/minimum-validation-suite.yml` (exclusive paths: .github/workflows/ only)

**CRITICAL**: System MUST NOT ship without minimum validation suite complete (T331-T336 all passing).

### Code Quality

- [ ] T325 [P] @agent-1 Code cleanup and refactoring across all modules (module-local, exclusive paths per module)
- [ ] T326 [P] @agent-1 Linting and formatting standardization (exclusive paths: config files only)
- [ ] T327 [P] @agent-1 Technical debt reduction (module-local, exclusive paths per module)

### Validation

- [ ] T328 @agent-1 Run quickstart.md validation
- [ ] T329 @agent-1 Validate all integration checkpoints
- [ ] T330 @agent-1 Final system integration testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 0 (Foundational Infrastructure, Days 1-2)**: No dependencies - can start immediately
- **Phase 1 (References & Research Engine, Days 3-5)**: Depends on Phase 0 completion - BLOCKS Phase 2
- **Phase 2 (Compute Engine, Days 6-8)**: Depends on Phase 0 and Phase 1 completion - BLOCKS Phase 3
- **Phase 3 (Advice Engine, Days 9-10)**: Depends on Phase 0, Phase 1, and Phase 2 completion - BLOCKS Phase 4
- **Phase 4 (Veris Finance, Days 11-12)**: Depends on Phase 0, Phase 1, Phase 2, and Phase 3 completion - BLOCKS Phase 5
- **Phase 5 (Frankie's Finance, Days 13-14)**: Depends on Phase 0, Phase 1, Phase 2, Phase 3, and Phase 4 completion
- **Phase 6 (Polish)**: Depends on all desired phases being complete

### User Story Dependencies

- **User Story 1 (Consumer/Frankie's Finance)**: Depends on Phase 2 (Compute Engine), Phase 3 (Advice Engine), and Phase 4 (Veris Finance for backend validation)
- **User Story 2 (Adviser/Veris Finance)**: Depends on Phase 2 (Compute Engine) and Phase 3 (Advice Engine)
- **User Story 3 (Partner API)**: Depends on Phase 1 (References & Research Engine) and Phase 2 (Compute Engine) - Can be implemented after Phase 2

### Module Dependencies

- **References & Research Engine**: No module dependencies (foundational)
- **Compute Engine**: Depends on References & Research Engine
- **Advice Engine**: Depends on Compute Engine and References & Research Engine
- **LLM Orchestrator**: Depends on Compute Engine and References & Research Engine
- **Veris Finance**: Depends on all backend modules (Advice Engine, LLM Orchestrator, Compute Engine, References & Research Engine)
- **Frankie's Finance**: Depends on all backend modules (Advice Engine, LLM Orchestrator, Compute Engine, References & Research Engine)

### Parallel Opportunities

- **Phase 0**: All tasks marked [P] can run in parallel
- **Phase 1**: Tasks marked [P] can run in parallel
- **Phase 2**: Tasks marked [P] can run in parallel
- **Phase 3**: Tasks marked [P] can run in parallel
- **Phase 4**: Tasks marked [P] can run in parallel
- **Phase 5**: Tasks marked [P] can run in parallel
- **Phase 6**: All tasks marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (Phase 1 + Phase 2 Only)

1. Complete Phase 0: Foundational Infrastructure (Days 1-2)
2. Complete Phase 1: References & Research Engine (Days 3-5)
3. Complete Phase 2: Compute Engine (Days 6-8)
4. **STOP and VALIDATE**: Test core backend modules independently
5. Deploy/demo if ready

### Incremental Delivery (2-Week Compressed Timeline)

1. Complete Phase 0 (Days 1-2) → Foundation ready
2. Add Phase 1 (References & Research Engine, Days 3-5) → Test independently → Deploy/Demo
3. Add Phase 2 (Compute Engine, Days 6-8) → Test independently → Deploy/Demo
4. Add Phase 3 (Advice Engine, Days 9-10) → Test independently → Deploy/Demo
5. Add Phase 4 (Veris Finance, Days 11-12) → Test independently → Deploy/Demo (Adviser MVP!)
6. Add Phase 5 (Frankie's Finance, Days 13-14) → Test independently → Deploy/Demo (Consumer MVP!)
7. Each phase adds value without breaking previous phases

### Parallel Team Strategy (AI-Assisted Development with Cursor Agents)

With Cursor AI agents (Backend, Frontend, Infrastructure/DevOps):

1. **Days 1-2**: Infrastructure/DevOps Agent completes Phase 0 (Foundational Infrastructure)
2. **Days 3-5**: Backend Agent completes Phase 1 (References & Research Engine)
3. **Days 6-8**: Backend Agent completes Phase 2 (Compute Engine)
4. **Days 9-10**: Backend Agent completes Phase 3 (Advice Engine)
5. **Days 11-12**: Frontend Agent completes Phase 4 (Veris Finance)
6. **Days 13-14**: Frontend Agent completes Phase 5 (Frankie's Finance)

**Note**: LLM Orchestrator progresses incrementally through each phase as needed for module functionality.

### Version Control Strategy

**Per User Guidance**: Automated commits after each task has been tested.

**Workflow**:
1. Complete task implementation
2. Write/update tests for task
3. Run tests locally (unit, integration)
4. Commit with descriptive message: `feat(module): task description`
5. Push to feature branch
6. CI/CD runs automated tests
7. If tests pass, merge to main branch

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability (US1 = Consumer/Frankie's Finance, US2 = Adviser/Veris Finance, US3 = Partner API)
- Each phase should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group (per user guidance)
- Stop at any checkpoint to validate phase independently
- Avoid: vague tasks, same file conflicts, cross-phase dependencies that break independence
- **Veris Finance Test Forecasts**: Each calculation in Compute Engine must be tested via Veris Finance test forecasts (per user guidance)
- **LLM Model Selection**: Different LLM models for different tasks with intelligent switching, preference for cheaper models based on performance requirements
- **Minimum Validation Suite (CRITICAL)**: System MUST NOT ship without minimum validation suite complete:
  - At least 10 ATO tax calculation examples validated (T204A, T331)
  - At least 5 ASIC compliance examples validated (T228A, T332)
  - 100% deterministic reproducibility verified (T205A, T333)
  - All calculations validated via Veris Finance test forecasts (T334)
  - Validation suite report created (T335)
  - CI/CD check configured to fail if validation suite incomplete (T336)


  - At least 10 ATO tax calculation examples validated (T204A, T331)
  - At least 5 ASIC compliance examples validated (T228A, T332)
  - 100% deterministic reproducibility verified (T205A, T333)
  - All calculations validated via Veris Finance test forecasts (T334)
  - Validation suite report created (T335)
  - CI/CD check configured to fail if validation suite incomplete (T336)

