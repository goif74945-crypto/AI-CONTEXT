# P4.9 Retry / Backoff

## Deterministic algorithm
`delay = min(cap, base × 2^(attempt-1))`

No RNG and no jitter.

## Retryable
- transient dependency;
- lease lost;
- rate limited.

## Non-retryable by default
Validation failure, authority conflict, security violation, destructive human gate and UNKNOWN.

Attempt budget is hard-bounded. Exhaustion never loops back automatically.

## Files
- `retry.schema.json`
- `retry-policy.json`
- golden + exhausted/authority/security negative examples
- `validation-report.md`
