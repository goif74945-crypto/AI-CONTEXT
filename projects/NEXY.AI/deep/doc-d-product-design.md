# NEXY.AI — DOC-D Final Product Design Pack

## Authority
SOURCE-PRODUCT-DESIGN. DOC-D defines concrete product surfaces and UX contracts. It does not override DOC-B System Law or DOC-C Build Spec and is not deployment evidence.

# 1. Screen inventory

### S1 — Front Door
Primary: Start / Enter Directive  
Secondary: View Mode

### S2 — OTAC Verify
Primary: Verify Code  
Secondary: Resend Code

### S3 — Home / Front
Primary: RUN  
Secondary: VIEW / FORGE

### S4 — Directive Create
Primary: Submit Directive  
Secondary: Save Draft

### S5 — Directive Detail
Primary: View Result  
Secondary: Export

### S6 — Pipeline Run Detail
Primary: Inspect Run  
Secondary: Open Incident

### S7 — Freeze Incident
Primary for OWNER: Recover  
Secondary: View Trace

### S8 — Artifact List
Primary: Open Artifact  
Secondary: New Artifact

### S9 — Revision History
Primary: Compare Revision  
Secondary: Restore

### S10 — Audit Viewer
Primary: Filter Logs  
Secondary: Export Logs

### S11 — Owner Control Panel
Primary controls: Recover / Revoke / Config  
Secondary: View System

### S12 — I-Don’t-Know Mode
Primary: Show Examples  
Secondary: Ask One Guided Question

The last screen is a usability surface and must not become permission to invent missing material facts.

# 2. Key per-screen layout contracts

## S1 Front Door
- top: status chip;
- center: one large input;
- bottom: VIEW/RUN/FORGE selector;
- no dangerous controls;
- no telemetry clutter.

Intent: minimal first contact despite the large backend.

## S4 Directive Create
Fields:
- input;
- mode;
- priority;
- allow_external;
- deterministic_required.

Submit remains disabled until schema-valid.

## S7 Freeze Incident
Must expose:
- FREEZE banner;
- primary incident code;
- trigger;
- blocking layer;
- recoverable true/false.

OWNER may see recovery CTA.
Other roles receive read-only explanation.

The UI may not hide/mask the authoritative frozen state.

# 3. Component inventory
Named product components:
- StatusChip
- ModeTabs
- DirectiveInput
- ConstraintPanel
- SubmitButton
- FreezeBanner
- IncidentCard
- RevisionTable
- AuditTable
- EmptyStateCard
- PermissionGate
- OwnerActionBar
- LoadingSkeleton
- TrustExplainer

These are product/UI components, not new authority modules.

# 4. Table contracts

## RevisionTable
Columns:
- revision_no
- created_at
- created_by
- content_hash
- commit_count
- status
- actions

## AuditTable
Columns:
- timestamp
- actor
- role
- action
- target_type
- target_id
- success
- incident_link

# 5. Form contract

Directive creation:
- input: textarea, required, non-empty;
- mode: fast/strict/audit;
- priority: low/normal/high/critical;
- allow_external: explicit boolean;
- deterministic_required: explicit boolean.

Auth:
- email: syntactically valid;
- OTAC: exact current configured length, source pack uses 10.

The product is intentionally explicit about external-model use and deterministic requirement rather than hiding those decisions.

# 6. Validation-copy law
Blocked paths should use direct deterministic wording.

Examples:
- Input required
- Schema invalid
- Permission denied
- System frozen
- Recovery not allowed

Avoid ambiguous language such as “maybe” and avoid “try again?” when law says the path is blocked.

# 7. Permission visibility
UI visibility follows role, but UI hiding is never backend authorization.

Examples:
- Recover: OWNER only.
- Hard delete: OWNER only.
- Config panel: OWNER only.
- Audit export: OWNER and AUDITOR.
- Submit directive: OWNER/OPERATOR.

System role exists at backend level and is not necessarily a human-visible UI role.

# 8. Mobile / desktop law

### Mobile
- single column;
- dangerous controls behind owner drawer;
- tables collapse to cards;
- freeze banner remains sticky.

### Desktop
- at most two main panels;
- directive/result split view allowed;
- audit/revision tables may use full width.

The source intentionally limits dashboard sprawl.

# 9. Loading/pending truth
Skeletons are permitted only while waiting for backend truth.

Rules:
- skeleton must not imply success;
- pending run shows only backend-confirmed state;
- loading animation is not evidence that execution succeeded.

This extends UI Truth Law into concrete component behavior.

# 10. Empty states
Named wording:
- No directive yet
- No revisions yet
- No incidents recorded
- No active run
- You can start in VIEW, RUN, or FORGE

Empty state is explicit rather than fabricated content.

# 11. First-session walkthrough
Source flow:
1. explain one-output rule;
2. explain FREEZE = integrity;
3. let user choose VIEW/RUN/FORGE;
4. show one safe example;
5. show where dangerous controls are hidden.

The onboarding goal is to teach NEXY’s control model, not internal jargon.

# 12. Trust-building loop
Repeated explanations should make clear:
- why one answer is released;
- why FREEZE exists;
- why partial/unverified truth may be blocked;
- why controls are role-hidden;
- what happens after a blocked action.

This is the product bridge between strict backend semantics and user trust.

# 13. Storage Law — migration-ready supplement

DOC-D-adjacent product pack also specifies database behavior more concretely.

Enums:
- Role = OWNER | OPERATOR | AUDITOR | SYSTEM
- SystemState = INIT | READY | RUNNING | VERIFYING | CONSENSUS | STABLE | FREEZE | STOP
- IncidentType = FREEZE | SECURITY | AUDIT_RELEVANT
- RunOutcome = SUCCESS | FAILURE

Unique constraints include:
- User.email
- Session.id
- DirectiveRecord.idempotency_key
- Commit.idempotency_key
- Revision(artifact_id, revision_no)
- PipelineRun.id
- FreezeIncident.pipeline_run_id

## Deletion/FK semantics
Production relations are largely RESTRICT to preserve lineage:
- User→Session;
- User→Project;
- Project→Artifact;
- Artifact→Revision;
- Revision→Commit;
- PipelineRun→FreezeIncident.

DirectiveRecord→PipelineRun may cascade only in test fixtures; production is RESTRICT.

## Soft delete semantics
- User: deactivate, no soft delete.
- Project/Artifact: soft delete, lineage retained.
- Revision/Commit/Directive/Pipeline/logs/incidents: immutable historical records, not soft-deleted as ordinary UI data.

## Version rules
- every content mutation = new Revision;
- Commit points to exactly one Revision;
- previous_version required for write-after-read flows;
- no overwrite;
- committed revision body immutable.

## Commit atomicity
1. validate request;
2. verify revision;
3. verify previous_version;
4. verify content hash;
5. metadata transaction;
6. blob-verification marker;
7. audit log.

Failure rolls back the metadata transaction.

## Restore
Artifact may restore only when:
- it was soft-deleted;
- parent project is active;
- lineage is intact;
- referenced blob was not hard-deleted.

## Blob retention
Blob remains while active revisions reference it.
Hard delete destroys blob + link and emits irreversible audit evidence.

## Archival
- hot store: recent active;
- warm: older closed artifacts;
- cold: audit/export snapshots.

No archive path may break traceability.

# 14. Auth-hardening product pack

Classification:
**TEMPORARY PRODUCTION MINIMUM — not final enterprise auth.**

### Session invalidation
- logout revokes current session only;
- revoke-all revokes every session;
- successful passwordless verification rotates to a new session id;
- revoked session cannot reactivate.

### Concurrent sessions
Maximum = 5/user in this pack.
If exceeded, oldest non-owner session is revoked first.
OWNER session removal needs explicit confirmation.

### OTAC replay
- one-time;
- consumed flag after success;
- hash may remain;
- raw code discarded;
- reuse → AUTH_INVALID + security audit.

### Brute-force lock
5 failed attempts in TTL:
lock email + device + IP window for 15 min.
Repeated lock cycles create a SecurityIncident.

### Metadata minimization
Store only required security metadata such as:
- device_id;
- IP hash;
- user-agent fingerprint summary;
- created_at;
- last_seen_at.

Source explicitly says not to store unnecessary personal profiling.

### Cookie/renewal
- HttpOnly;
- Secure;
- SameSite=Strict;
- Path=/;
- rotate on verification;
- renewal only via explicit refresh endpoint;
- no silent perpetual extension.

### Audit emission
Auth events are auditable:
- OTAC request;
- verify success/failure;
- logout;
- revoke-all;
- suspicious login.

### Owner recovery
Lost/suspiciously locked OWNER session requires manual recovery path, security incident and audit trail.
No hidden bypass.

### Suspicious login signals
- device mismatch;
- impossible rapid retries;
- reused OTAC;
- revoked-session reuse.

Response:
- deny session;
- emit SecurityIncident;
- optionally revoke all active user sessions.

# 15. Product-design principle

DOC-D translates NEXY’s system laws into visible behavior:
**the interface should make truth, authority, failure and next legal action obvious without exposing the entire machinery.**

It cannot invent state, bypass backend permission, hide FREEZE, or substitute attractive UX for verified system truth.
