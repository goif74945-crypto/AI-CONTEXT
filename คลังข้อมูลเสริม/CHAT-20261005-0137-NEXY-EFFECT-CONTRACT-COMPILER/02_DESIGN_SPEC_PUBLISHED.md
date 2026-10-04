# NECC Design Specification — Published Summary

**Authority:** AI-PROPOSED research design only. It is not current NEXY canon.

## Objective
Transform a proposed external side effect into a deterministic Effect Contract that can be validated, gated, reconciled and verified before being treated as committed.

Pipeline:
`EffectIntent -> validate -> canonicalize -> EffectContract -> preflight -> dispatch -> reconcile/verify -> receipt`

## Contract semantics
Each consequential intent describes target identity, authority, preconditions, expected postconditions, reversibility R0-R5, idempotency/reconciliation semantics, compensation where required, timestamps/expiry, and explicit high-impact authorization flags.

### Reversibility
- R0: read-only only.
- R1-R2: reversible under known state.
- R3: requires compensation/rollback material by default.
- R4: requires compensation plus explicit confirmation.
- R5: requires compensation, confirmation, and explicit irreversible authorization.

## Execution FSM
Primary:
`PROPOSED -> READY -> DISPATCHED -> VERIFYING -> COMMITTED`

Safety paths:
- failed/expired preflight -> `FROZEN`;
- timeout after dispatch -> `UNKNOWN_SIDE_EFFECT`;
- no blind redispatch from ambiguous outcome;
- reconcile true -> `VERIFYING`;
- reconcile false -> `READY`;
- indeterminate reconcile -> `FROZEN`;
- failed postcondition -> `FROZEN`.

## Determinism
Canonical JSON drives SHA-256 contract identity. Timestamps normalize to UTC Z, mapping keys must be strings, non-finite numbers are rejected, and nested metadata is detached/deep-frozen after compilation.

## Planning and ledger
Multi-action plans reject duplicate IDs, missing/unknown dependencies and cycles, then produce deterministic topological order/waves.

The receipt ledger uses an append-only hash chain and detects idempotency-key conflicts. It is **tamper-evident, not non-repudiation**.

## Integration boundary
NECC does not call external providers. A future NEXY adapter would need authoritative current-state snapshotting, preflight immediately before dispatch, independent provider authorization, receipt/timeout mapping, reconciliation/readback, postcondition verification and durable evidence storage.

The full design and implementation plan are inside the exact encoded bundle.
