# Execution Transaction Model

## Goal
Treat autonomous AI execution as a transaction with explicit authority, side effects, verification, and compensation.

## States
PROPOSED → AUTHORIZED → PRECONDITIONS_OK → EXECUTING → SIDE_EFFECT_RECORDED → VERIFYING → COMMITTED

Failure states:
FREEZE / ROLLBACK_REQUIRED / COMPENSATING / PARTIAL / FAILED / MANUAL_REVIEW

## Transaction envelope
Every consequential action should carry:
- task_id and trace_id
- actor/agent identity
- authority source
- target resource
- expected pre-state fingerprint
- requested mutation
- idempotency key
- reversible? yes/no
- rollback/compensation method
- verification predicate
- evidence destination
- expiry/freshness bound

## Laws
- Re-check pre-state immediately before mutation when state may drift.
- Never retry a non-idempotent action blindly.
- A timeout is UNKNOWN outcome until reconciled.
- “Request failed” does not prove “side effect did not happen”.
- Compensation is not identical to rollback; record residual effects.
- Commit only after postcondition verification.
- If verification cannot distinguish success from partial success, freeze.

## Example failure
External API times out after accepting a write.
Correct state: UNKNOWN_SIDE_EFFECT.
Next action: query by idempotency key/resource identity, reconcile, then either commit or compensate.
Incorrect action: repeat the write and hope civilization survives.

## NEXY relevance
This model supports deterministic execution boundaries, explicit freeze behavior, auditability, and safe orchestration across external tools.
