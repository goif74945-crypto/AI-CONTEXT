# DEFECT-001 — CLEAR severity incorrectly influenced MANIPGATE64

## Detection
Found during post-first-pass architecture review after the initial 24-test suite had passed.

## Root cause
Several mechanisms expose useful raw metrics even when policy state is `CLEAR` (for example merge coverage, clone count ratio, or provenance concentration). `MANIPGATE64` originally computed maximum severity across all findings, so a high raw metric on a `CLEAR` finding could trigger `DEFER_REVIEW`.

## Why this was wrong
The gate's decision semantics are state-based: only a `FLAGGED` finding represents manipulation risk. `CLEAR` raw metrics are diagnostic context, not violations.

## Repair
`MANIPGATE64` now computes `maxSeverityQ64` only from findings whose state is `FLAGGED`. `UNKNOWN` remains separately fail-deferred; hard flagged findings remain non-compensatory blockers.

## Regression proof
Added property/regression test: `MANIPGATE ignores raw severity on CLEAR findings`. The test supplies all 19 required findings as `CLEAR` with severity `Q64_ONE` and requires `ALLOW_REVIEW` plus `maxSeverityQ64 == 0`.

## Re-verification
Final suite: 28 tests passed, 0 failed. Static compile and deterministic replay also passed.
