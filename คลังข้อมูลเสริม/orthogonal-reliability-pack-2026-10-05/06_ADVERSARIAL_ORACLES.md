# Adversarial Validation Oracles
Happy-path proves capability. Adversarial validation tests safe failure.

AI/context: prompt injection in retrieved content; stale spec presented as current; forged authority labels; duplicate evidence amplification; contradictions; irrelevant high-similarity chunks; instructions embedded in data; truncation removing prohibitions.
API/data: null-vs-empty; Unicode normalization collisions; duplicate idempotency keys; replay; out-of-order events; concurrent updates; pagination gaps; unknown schema fields; version skew.
Isolation: cross-tenant IDs; predictable IDs; unauthorized export; identity omitted from cache key; secret logs; resource-existence leakage.
Reliability: 429/500; timeout after server commit; crash between write and acknowledgement; stale cache; queue redelivery; clock skew; resource exhaustion.
Verification traps: zero tests discovered but exit success; mocks hiding contract drift; snapshots approving wrong semantics; UI tests ignoring provenance; health green while critical dependency dead.

Each scenario defines observable postcondition, forbidden observation, recovery expectation, telemetry expectation. "No exception" is not a sufficient oracle.
