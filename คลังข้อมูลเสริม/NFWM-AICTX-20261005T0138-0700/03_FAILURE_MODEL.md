# NFWM Failure Model

## Parser failures

- malformed JSON;
- wrong trace/profile schema version;
- unknown top-level fields;
- missing required event identity;
- invalid event sequence type;
- invalid profile transition shape.

Behavior: fail closed, emit `NFWM_ERROR`, exit `64`. No partial trace analysis.

## Analyzer failures represented as deterministic violations

- `INV_SEQUENCE_STRICT_INCREASE`
- `INV_TRANSITION_SHAPE`
- `INV_FSM_TRANSITION`
- `INV_FREEZE_INCIDENT_LINK`
- `INV_STOP_TERMINAL`
- `INV_RELEASE_AFTER_FREEZE`
- `INV_IDEMPOTENCY_REUSE`

Behavior: valid analysis result with `status=FAIL`, exit `2` in CLI analyze mode.

## Minimizer failure

If the requested violation code is not present in the source event set, minimization raises an explicit error. It does not fabricate a witness.

## Replay failure

Witness verification fails when:

- stored witness hash differs from canonical hash;
- selected violation no longer reproduces;
- re-minimization can remove additional events.

Behavior: `status=FAIL`, exit `3`.

## Known semantic limits

1. Violation targeting is by **violation code**, not by exact original event fingerprint. If multiple violations share one code, minimization may return a different reproducer of the same violation class.
2. `INV_RELEASE_AFTER_FREEZE` scopes by `(trace_id, run_id)`. A real implementation may require a richer execution-cycle identifier.
3. The profile is a derived external profile, not proof of the current NEXY event schema.
4. NFWM does not inspect application payloads under `metadata` for secrets.
5. 1-minimality is local to single-event deletion and the configured predicate. It is not a mathematical proof of globally smallest cardinality.

These limits are preserved rather than hidden because a useful debugger that lies about its guarantees is just an incident generator wearing glasses.
