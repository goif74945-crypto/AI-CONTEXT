# Formal State Model for Verify-or-Freeze Systems

Status: PROPOSAL

## Purpose
Provide a model-checkable state machine for systems whose terminal behavior is verified output or freeze.

## Abstract states
S0 RECEIVED
S1 NORMALIZED
S2 AUTHORITY_RESOLVED
S3 SCOPE_LOCKED
S4 PLAN_VALID
S5 EXECUTING
S6 VERIFYING
S7 EVIDENCE_CLOSED
S8 OUTPUT_COMMITTED

Side/terminal states:
F1 FREEZE_INPUT
F2 FREEZE_AUTHORITY
F3 FREEZE_SCOPE
F4 FREEZE_SECURITY
F5 FREEZE_EVIDENCE
F6 BLOCKED_DEPENDENCY
F7 FAILED_IMPLEMENTATION
F8 NOT_VERIFIED

## Transition law
A transition is legal only if its guard is proven true from explicit state/evidence.

Examples:
S0 -> S1 iff input normalization succeeds.
S1 -> S2 iff governing authority is unique/sufficient.
S2 -> S3 iff authorized and protected scopes are explicit.
S3 -> S4 iff plan preserves invariants and required evidence path exists.
S4 -> S5 iff mutation/execution capability is authorized.
S5 -> S6 iff execution terminates with inspectable result.
S6 -> S7 iff every required proof obligation has valid evidence.
S7 -> S8 iff no invalidating conflict/blocker exists.

## Safety invariants
I1: OUTPUT_COMMITTED implies EVIDENCE_CLOSED.
I2: EVIDENCE_CLOSED implies all mandatory proof obligations valid.
I3: no FREEZE state has outgoing mutation transition except explicit recovery/re-evaluation.
I4: protected-scope mutation is unreachable without explicit authorization.
I5: advisory context cannot directly transition authority state.
I6: stale evidence cannot satisfy current proof obligations.
I7: execution failure cannot transition directly to OUTPUT_COMMITTED.
I8: missing evidence never coerces to PASS.

## Liveness boundary
A verify-or-freeze system does not promise success for every request.
Desired liveness is:
if inputs are valid, authority is resolvable, dependencies available, execution terminates, and proofs close, then the system eventually reaches OUTPUT_COMMITTED.
Otherwise a defined freeze/block/fail terminal is acceptable.

## Illegal shortcuts
S0 -> S8
S5 -> S8
S6 -> S8 without closure
F* -> S8 without recovery proof

## Model-checking candidates
- TLA+: state transitions, concurrency, stale evidence invalidation.
- Alloy: authority/scope relation consistency and counterexample search.
- PlusCal: executable algorithm sketch for workflow transitions.
- Property-based tests: implementation-level conformance to transition invariants.

Tool choice is PROPOSAL, not current NEXY requirement.

## Concurrency questions
UNKNOWN until project contract specifies:
- Can multiple verifiers close the same proof concurrently?
- What wins if authority changes while execution is running?
- Are evidence seals optimistic, pessimistic, or append-only?
- What is the cancellation law for queued side effects?

Conservative proposal: authority/source identity is snapshotted at execution start; any relevant authority/source mutation before commit invalidates closure and forces re-evaluation.
