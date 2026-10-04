# Reliability & Failure Engineering
Taxonomy: invalid input, unavailable/slow/malformed dependency, auth denial, concurrency conflict, duplicate, crash, partition, backlog, storage exhaustion, clock skew, stale cache, schema mismatch, partial deploy, rate limit, corrupted state.
Per operation: SLO, timeout, retryable set, attempts, backoff/jitter, idempotency, fallback, compensation, alert, recovery.
Retry only plausibly transient failures when replay-safe, within deadline, and not amplifying overload.
Multi-step mutation: stable operation ID, persisted state, replay-safe steps, compensation, visible partial state, no success before terminal success.
Chaos: 5xx, 429, 10x latency, reset-after-commit, duplicate/out-of-order messages, stale reads, disk full, mid-operation crash, semantically invalid HTTP 200.
