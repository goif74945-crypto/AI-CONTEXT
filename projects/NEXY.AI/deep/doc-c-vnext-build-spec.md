# NEXY.AI — DOC-C / vNEXT Build Spec Deep Context

## Authority
This file records the narrow **build-spec** architecture. In the source hierarchy:
- DOC-A = Vision Canon
- DOC-B = System Law
- DOC-C = Build Spec
- DOC-D = Product Design Pack
- DOC-E = Deployment Evidence Pack

**Build obligation comes from DOC-C only. Deploy approval comes from DOC-E only.**
Vision/future systems elsewhere in the source do not automatically enter vNEXT.

## 1. vNEXT identity / inclusion
DOC-B identity:
- deterministic AI control hub;
- not chatbot/AGI/friend authority;
- Core hidden, output visible;
- Proof > Speed > Emotion;
- one output / one truth / or freeze.

DOC-C includes:
- directive execution;
- multi-agent debate/verification/consensus;
- release policy;
- Vault revisioning;
- temporary OTAC auth;
- RBAC;
- observability;
- queue + idempotency;
- UI truth layer;
- owner controls;
- auditability.

Explicitly excluded from vNEXT:
- voice orchestration;
- AR/VR/XR;
- holographic UI;
- blockchain;
- IoT;
- quantum-safe cryptography layer;
- self-patch / auto-heal runtime;
- public anonymous write access.

Deferred:
- advanced policy simulation dashboard;
- multi-tenant org hierarchy;
- fine-grained per-project config policy;
- provider marketplace.

Anything outside the include list requires explicit spec extension + dependency/test impact review + version bump.

## 2. Reference implementation target
One implementation-oriented source pack names:
- Frontend: Next.js + TypeScript
- API: Next.js Route Handlers or dedicated Node service
- Validation: Zod
- DB: PostgreSQL
- ORM: Prisma
- Queue: BullMQ + Redis
- Auth: Email OTAC + secure cookie session
- Large payload storage: object/blob storage
- Observability: structured JSON logs + trace IDs
- Tests: Vitest + Playwright + Prisma integration tests

Treat these as build-spec targets, not runtime evidence.

## 3. Canonical state/types
SystemStatus:
- OK
- DEGRADED
- FREEZE
- STOP

SystemState:
- INIT
- READY
- RUNNING
- VERIFYING
- CONSENSUS
- STABLE
- FREEZE
- STOP

Roles:
- OWNER
- OPERATOR
- AUDITOR
- SYSTEM
- PUBLIC_USER

Actor types:
- USER
- SYSTEM
- AGENT

Severity:
- INFO
- WARN
- ERROR
- CRITICAL

## 4. Error taxonomy
Build spec names errors including:
- INVALID_DIRECTIVE
- EMPTY_INPUT
- AMBIGUOUS_INPUT
- UNVERIFIED_OUTPUT
- CONSENSUS_FAILED
- EVIDENCE_MISSING
- SCHEMA_VIOLATION
- STATE_TRANSITION_DENIED
- INVALID_STATE
- AUTH_INVALID / AUTH_EXPIRED
- UNAUTHORIZED / FORBIDDEN
- SESSION_REVOKED
- DEVICE_MISMATCH
- CSRF_INVALID
- OTAC_LOCKED
- RATE_LIMIT_EXCEEDED
- SECURITY_BREACH_DETECTED
- SYSTEM_IN_FREEZE
- DEPENDENCY_FAILURE / DEPENDENCY_UNHEALTHY
- TIMEOUT / AGENT_TIMEOUT
- AGENT_SCHEMA_INVALID
- FREEZE_RECOVERY_DENIED
- VAULT_COMMIT_CONFLICT
- REVISION_NOT_FOUND
- RELEASE_POLICY_FAILED

An earlier execution-pack draft also named PIPELINE_CAP_EXCEEDED. Treat final canonical error unions as authority when exact current contract matters.

## 5. SystemEnvelope
All API responses use a single envelope carrying:
- status/state;
- timestamp;
- request_id;
- trace_id;
- optional correlation_id;
- version;
- optional duration;
- optional actor;
- data;
- structured error;
- optional freeze reason/warnings;
- optional integrity body hash/schema version.

Important: the envelope is part of the truth surface; no endpoint invents its own incompatible success/error shape.

## 6. Directive contract
Directive includes:
- id;
- project id;
- optional artifact id;
- input;
- input type TEXT or STRUCTURED_JSON;
- mode: fast/strict/audit;
- priority: LOW/NORMAL/HIGH/CRITICAL;
- constraints such as token bound, external access and deterministic requirement;
- metadata with created_at, operator, role, schema version and idempotency key.

## 7. Evidence contract
Evidence carries:
- source and source type;
- content;
- hash;
- confidence;
- verified flag;
- collection/verification metadata;
- source anchors;
- contradiction marker;
- normalization version.

This gives evidence a first-class schema rather than treating citations as presentation text.

## 8. Consensus / release policy
ConsensusResult records:
- accepted;
- releaseable;
- output;
- confidence;
- deterministic-match score;
- participating/excluded agents;
- verified evidence;
- threshold snapshot;
- decision reason;
- conflict report.

ReleasePolicyResult records pass/fail plus exact threshold snapshot and reasons.

Release is legal only when all required gates pass:
- accepted=true;
- releaseable=true;
- confidence >= threshold;
- deterministic match >= threshold;
- evidence count >= minimum;
- quorum satisfied;
- no critical-agent blocking failure;
- not frozen;
- integrity hash present;
- LAW pre-release passes.

No averaging/guessing through unresolved conflict.

## 9. Current canonical defaults
The later DOC-C canonical pack supersedes conflicting earlier draft defaults:

### Release
- confidence_min = 0.85
- deterministic_match_min = 0.90
- quorum_min = 2
- evidence_min = 2

### Pipeline
- decompose = 5s
- default agent timeout = 30s
- min/max agent timeout = 10s/60s
- critical-agent timeout = 30s
- cross-verify = 15s
- consensus = 10s
- emit = 5s
- global pipeline cap = 120s

### Auth
- OTAC length = 10
- OTAC TTL = 5 min
- attempts = 5
- resend cooldown = 60s
- lock window = 15 min
- session TTL = 6h
- concurrent sessions/user = 5

### Retention
- event log = 90d
- audit log = 365d
- security incident = 365d
- freeze incident = 365d

### Queue
- stale job TTL = 15 min
- max concurrent pipeline runs = 10

Any config change requires explicit version bump, audit record and rollback target. No per-environment silent drift.

### Important source evolution
An earlier vNEXT.1 draft used a 30-day session TTL. The later canonical DOC-C pack changes this to 6h and adds a 5-session/user cap. Use the later canonical pack unless a newer authority supersedes it.

## 10. Runtime validation law
TypeScript types are not enforcement.
Validation is repeated at boundaries:
- UI → API;
- API → CORE;
- CORE → queue;
- queue consumer;
- SWARM result;
- JUDGE input;
- LAW pre-release;
- VAULT commit.

Stack:
- TypeScript compile-time;
- Zod runtime schemas;
- DB constraints;
- queue payload revalidation;
- hash/FK checks for persistence.

Invalid internal data is not trusted merely because it came from another NEXY module.

## 11. Module architecture
Modules:
- UI — truth rendering only
- API — auth/validation/rate/routing boundary
- CORE — orchestrator/state transitions
- LAW — precheck/pre-release/freeze rules
- SWARM — multi-agent worker execution
- JUDGE — scoring/quorum/deterministic-match evaluation
- VAULT — persistence/versioning/append-only history
- AUTH — OTAC/session/device binding
- OBS — logs/audit/incidents

Allowed dependency shape:
- UI → API
- API → AUTH
- API → CORE
- CORE → LAW (precheck and prerelease)
- CORE → SWARM
- CORE → JUDGE
- CORE → VAULT
- CORE → OBS
- AUTH/VAULT/SWARM/JUDGE/LAW → OBS

Forbidden:
- UI → LAW
- UI → VAULT
- SWARM → VAULT
- JUDGE → CORE
- LAW → UI
- VAULT → CORE
- AUTH → CORE

Dependency violation = build failure, enforced through import/dependency lint + CI.

## 12. Executable FSM
Legal states:
INIT → READY → RUNNING → VERIFYING → CONSENSUS → STABLE
with FREEZE/STOP side paths.

Events:
- boot
- execute
- agents_done
- verified
- accepted
- rejected
- error
- recover
- fatal

Guards:
- system_valid
- directive_valid
- results_exist
- evidence_valid
- quorum_satisfied
- release_policy_passed
- freeze_recovery_allowed
- not_in_stop

Key transitions:
- INIT + boot → READY
- READY + execute → RUNNING
- RUNNING + agents_done → VERIFYING
- VERIFYING + verified → CONSENSUS
- CONSENSUS + accepted → STABLE if quorum/release pass
- CONSENSUS + rejected → FREEZE
- error from any non-STOP state → FREEZE
- FREEZE + recover → READY if allowed
- FREEZE + fatal → STOP

Illegal examples:
READY→CONSENSUS, RUNNING→STABLE, VERIFYING→READY, STOP→ANY, FREEZE→RUNNING, INIT→STABLE.

Event owners:
- CORE: boot/execute
- SWARM: agents_done
- JUDGE: verified/accepted/rejected
- LAW/CORE/AUTH/VAULT/SWARM/API: error
- OWNER or SYSTEM: recover
- LAW or AUTH: fatal

Every transition emits traceable event metadata.

## 13. FREEZE / STOP semantics
FREEZE:
- blocks release;
- blocks new non-owner execution;
- creates/links primary incident;
- invalidates pending release token.

STOP:
- irreversible in this build model;
- cancels all queue jobs;
- requires manual/admin intervention.

Failure priority:
1. security breach
2. schema violation
3. illegal state transition
4. consensus failure
5. timeout

Highest-priority failure becomes primary; others remain secondary.

Recovery:
- only when freeze is marked recoverable;
- actor OWNER or SYSTEM;
- pending output is purged;
- old queue job is never resumed;
- recovery starts a new execution cycle.

## 14. Multi-AI AgentAdapter
Each adapter declares:
- id/provider/schema version;
- supported modes;
- deterministic-capable flag;
- critical flag;
- timeout;
- context capacity;
- execute/cancel/healthcheck.

Health returns HEALTHY / DEGRADED / UNHEALTHY and latency.

This creates provider independence behind a stable worker contract.

## 15. Locked multi-AI pipeline
Stages:
1. Decompose
2. Parallel Execution
3. Adversarial Check
4. Cross Verification
5. Consensus Evaluation
6. Emit OR Freeze

Stage policy:
- decomposition timeout 5s;
- per-agent execution 10–60s;
- adversarial check ~10s;
- cross verify 15s;
- consensus 10s;
- emit 5s.

No automatic retry by default.
Noncritical timeout may exclude the worker if quorum still passes.
Critical timeout freezes.

## 16. API law
All responses use SystemEnvelope.
All mutating routes require secure session + CSRF except OTAC request/verify.
Mutating routes require idempotency key unless explicitly exempt.
Routes declare auth/RBAC/retry/audit/error matrix.

Key routes defined in source:
- POST /api/auth/request-otac
- POST /api/auth/verify-otac
- GET /api/session/me
- POST /api/auth/logout
- POST /api/directives
- GET /api/directives/:id
- GET /api/runs/:id
- POST /api/freeze/recover
- POST /api/vault/commit
- GET /api/artifacts/:id/revisions
- GET /api/incidents/:id
- GET /api/audit-logs

Semantics include explicit response/error codes, RBAC, audit events and retry/idempotency behavior.

## 17. Auth
Session:
- session/user/device ids;
- created/expires;
- revoked flag.

OTAC:
- 10 chars;
- 5-minute TTL in final build spec;
- max 5 attempts;
- 60-second resend cooldown;
- 15-minute lock window.

Cookie:
- HttpOnly;
- Secure;
- SameSite=Strict;
- path=/;
- rotation on successful verify;
- CSRF for mutation.

Controls:
- device binding;
- revoke one/all sessions;
- mismatch/rapid-retry anomaly detection;
- explicit email-provider failure;
- no anonymous mutating session.

## 18. Storage / Vault contract
Primary IDs: ULID.

Entities:
User, Session, Project, Artifact, Revision, Commit, DirectiveRecord, PipelineRun, FreezeIncident, EventLog, AuditLog, SecurityIncident.

Core lineage:
User → Project → Artifact → Revision → Commit.
DirectiveRecord → PipelineRun → optional FreezeIncident.

Storage:
- metadata in PostgreSQL;
- large content in blob/object store;
- content hash + blob path in DB;
- metadata transaction plus pending blob verification;
- soft delete via deleted_at;
- restore only if lineage remains valid;
- hard delete irreversible, OWNER-only, audited.

Revision:
- monotonically increasing revision number;
- no overwrite;
- changed content creates new revision;
- commit must point at existing revision;
- optimistic concurrency uses previous_version.

## 19. RBAC
Permission matrix:
- create directive: OWNER/OPERATOR/SYSTEM
- view directive: OWNER/OPERATOR/AUDITOR/SYSTEM
- recover freeze: OWNER/SYSTEM
- commit Vault: OWNER/SYSTEM
- read revisions/export artifact: OWNER/OPERATOR/AUDITOR/SYSTEM
- view audit logs: OWNER/AUDITOR/SYSTEM
- revoke session: OWNER; OPERATOR self-only; SYSTEM
- revoke all sessions: OWNER/SYSTEM
- manage roles: OWNER only

Frontend may hide controls; backend must enforce regardless of UI.

## 20. Observability / incident graph
Logs are separated:
- Event Log = operational transitions
- Audit Log = accountable actions
- Security Incident = auth/attack/abuse
- Freeze Incident = deterministic blocking failures

All primary incidents have incident_id + request_id + trace_id.
Events/audit records link to incidents.
No orphan incident is allowed when freeze_reason points to one.

Freeze Incident is authoritative for deterministic blocking; Security Incident for auth/abuse/breach.

## 21. Config law
Immutable at runtime:
- schema version;
- dependency rules;
- state machine definition.

Mutable only with audit/version:
- thresholds;
- agent enable/disable;
- timeouts;
- quorum;
- auth limits.

Every change requires config version, actor, audit and rollback target.

## 22. Queue law
Job states:
QUEUED / RUNNING / SUCCEEDED / FAILED / CANCELLED / EXPIRED.

Rules:
- idempotency key suppresses duplicate execution;
- FREEZE cancels pending release jobs;
- STOP cancels all jobs;
- failed job is not automatically retried unless explicitly safe;
- stale queue entries expire;
- payload validates before enqueue and again before consume.

## 23. Retention / redaction
- event logs 90d;
- audit/security/freeze records 365d minimum;
- artifacts/revisions indefinite until deletion by policy.

Redaction may operate on derived/copied views, not rewrite original audit lineage.
Hashes remain for integrity evidence.
Hard delete removes blob/reference and records irreversible audited deletion.

## 24. Test gates
Required suites:
- contract;
- API schema;
- FSM transition;
- forbidden dependencies;
- LAW block;
- release policy;
- freeze;
- auth abuse;
- Vault append-only;
- migration;
- RBAC;
- queue idempotency.

Minimum coverage targets:
- domain/core/law/judge 90%;
- API 85%;
- critical UI flows require E2E.

No merge when contract snapshots change unreviewed or dependency/FSM/release/auth-abuse gates fail.

## 25. UI Truth Contract
UI may format/group/emphasize but cannot:
- invent state;
- mask FREEZE;
- fabricate success;
- expose hidden partial output as released.

Screens:
login/OTAC, session/account, directive create/detail, pipeline detail, freeze incident, artifact/revisions, audit viewer, owner controls.

Frozen state:
- visible global banner;
- non-owner directive submission disabled;
- blocked release/export disabled;
- primary incident visible;
- owner recovery only if recoverable;
- never show success while FREEZE is authoritative.

UI semantics:
- loading = request in flight;
- pending = backend-confirmed queued/running;
- disabled = permission/system lock;
- error = backend-returned failure.
No optimistic fake success for blocking actions.

## 26. Build order
Locked order:
1. Contract Lock
2. Core Engine
3. Law Engine
4. Swarm
5. Judge
6. Vault
7. Auth
8. Observability
9. API
10. UI

Forbidden:
- UI before Core;
- Swarm before Law;
- storage before contracts;
- API without validation;
- deploy before tests.

## 27. Implementation-ready vs deployable
The source calls the spec implementation-ready only when contracts/validation/FSM/module boundaries/release/RBAC/queue-storage-observability/incident/UI truth/non-goal/test gates are defined.

If any required gate is missing in implementation:
**STATUS = NON-DEPLOYABLE.**

A design/spec statement must never be converted into a runtime PASS without DOC-E evidence.
