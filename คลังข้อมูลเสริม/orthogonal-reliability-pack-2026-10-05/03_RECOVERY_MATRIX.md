# Failure Taxonomy and Recovery Matrix
F01 INPUT_INVALID: fail fast, no retry.
F02 AUTHN: approved authentication recovery, no blind retry.
F03 AUTHZ: stop mutation and obtain authority.
F04 DEPENDENCY_UNAVAILABLE: bounded retry only if transient.
F05 RATE_LIMIT: server-aware bounded backoff with jitter.
F06 TIMEOUT: retry only idempotent operation or protected by idempotency key.
F07 PARTIAL_WRITE: reconcile observed state before compensation.
F08 STALE_READ: re-read under required consistency/freshness contract.
F09 CONTRACT_DRIFT: freeze dependent path, compare schema/version, update adapter plus regression tests.
F10 DATA_CORRUPTION: quarantine and preserve forensic evidence.
F11 MODEL_UNGROUNDED: downgrade claim and retrieve authority.
F12 TOOL_FALSE_SUCCESS: verify postcondition directly.
F13 RETRIEVAL_MISS: reformulate/broaden retrieval; never invent.
F14 RETRIEVAL_CONTAMINATION: reject namespace/authority/version mismatch.
F15 REGRESSION: smallest safe fix or rollback, then affected full gates.
F16 RESOURCE_EXHAUSTION: degrade only within explicit contract or block.
F17 CONCURRENCY_CONFLICT: use version/compare-and-swap semantics where supported.
F18 IDEMPOTENCY_FAILURE: stop retries and reconcile duplicates.
F19 OBSERVABILITY_GAP: improve evidence capture before guessing root cause.
F20 REQUIREMENT_DRIFT: compare against locked requirement fingerprints.

## Retry law
retry_allowed = transient AND operation_safe. Every retry records attempt, error fingerprint and observed state. No infinite retry.

## Recovery acceptance
Recovery passes only when original postcondition passes and no required regression gate fails.
