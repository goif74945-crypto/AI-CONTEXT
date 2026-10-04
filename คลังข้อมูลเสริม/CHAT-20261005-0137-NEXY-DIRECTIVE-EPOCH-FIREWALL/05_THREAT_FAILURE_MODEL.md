# 05 — Threat and Failure Model

## T1 — Stale worker commits after replacement
**Risk:** worker prepared under epoch N writes after epoch N+1.
**Control:** prepared epoch + directive/lineage binding checked at commit.
**Failure behavior:** FREEZE `STALE_DIRECTIVE_EPOCH`.

## T2 — Scope narrowed while queued writer remains alive
**Risk:** action kind was permitted earlier but no longer is.
**Control:** NARROW advances epoch and commit rejects stale epoch before mutation.
**Failure behavior:** FREEZE.

## T3 — Revoked directive still has queued work
**Risk:** revoked task mutates after cancellation.
**Control:** REVOKE advances epoch and changes engine status.
**Failure behavior:** no stale action may ALLOW.

## T4 — Prepared payload altered after approval
**Risk:** approval/gate applies to one action while executor receives another.
**Control:** recompute domain-separated action digest at commit.
**Failure behavior:** FREEZE `ACTION_DIGEST_MISMATCH`.

## T5 — Irreversible approval copied to a different action
**Risk:** approval token is reused across payloads/actions.
**Control:** exact binding includes action ID + epoch + action digest + lineage.
**Failure behavior:** REJECT.

## T6 — Duplicate event ID carries different directive
**Risk:** idempotency key collision becomes authority substitution.
**Control:** event ID maps to exact event digest.
**Failure behavior:** FREEZE.

## T7 — Replay log tampering
**Risk:** restart reconstructs a false authority history.
**Control:** hash chain + outcome/state replay checks.
**Failure behavior:** `ProtocolError`; no trusted replay result.

## T8 — Failed commit attempt omitted from recovery history
**Risk:** original run freezes, replay does not, creating state divergence.
**Control:** journal directive, commit and recovery attempts, not only accepted directives.
**Evidence:** this defect was found during self-audit of the first implementation and fixed before publication.

## T9 — Race after gate decision
**Risk:** epoch changes after `ALLOW` but before external write.
**Reference status:** NOT SOLVED by an in-memory precheck alone.
**Required integration control:** transaction/lease/CAS/outbox mechanism that couples epoch validity with durable mutation dispatch.

## T10 — Forged approval binding
**Risk:** deterministic hash is computable by an attacker.
**Reference status:** intentionally NOT authentication.
**Required integration control:** AUTH-verified signature/MAC/capability, then bind its authenticated grant to the DEF tuple.

## T11 — Malicious/incorrect natural-language supersession classification
**Risk:** model labels a change REPLACE/NARROW incorrectly.
**Reference status:** outside deterministic core.
**Required integration control:** only an authoritative structured control layer may emit directive operations.

## T12 — Distributed split brain
**Risk:** two nodes believe different epochs are current.
**Reference status:** NOT VERIFIED / out of reference scope.
**Required integration control:** single writer or consensus-backed monotonic authority register.
