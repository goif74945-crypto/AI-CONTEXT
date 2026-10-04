# EOSF Integration Preflight

The integration layer composes all five concepts without granting authority.

## Result states
- `READY`: local contracts allow a new/resumable effect attempt.
- `SUPPRESS_REPLAY`: registry or outbox proves the exact effect already completed/emitted.
- `FREEZE`: one or more blockers exist.

## Cross-store consistency
Registry and outbox state are cross-checked. A registry claiming COMPLETED while a present outbox row is not EMITTED, or a retryable registry row paired with EMITTED outbox state, freezes as `REGISTRY_OUTBOX_STATE_CONFLICT`.

## Independence
The integration gate accumulates multiple blockers rather than hiding later failures behind the first error.
