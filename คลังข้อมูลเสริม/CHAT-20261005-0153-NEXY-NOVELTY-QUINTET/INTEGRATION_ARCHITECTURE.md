# Integration Architecture — Release Evolution Guard Composition

**Status:** AI-PROPOSED COMPOSITION / NOT A NEXY REQUIREMENT

A future NEXY-compatible adapter could compose the quintet as follows:

1. **SMW**: reject/hold migrations that lose witness state.
2. **DDB**: compare pre/post or replay traces to localize deterministic drift.
3. **ARIG**: ensure the requirement/test/evidence graph has no broken proof links or stale hashes.
4. **MCH**: exercise invariant properties that ordinary example tests may miss.
5. **AMS**: mutate the final acceptance gate and ensure critical corruption is rejected.

## Monotonic status rule
A downstream stage cannot upgrade a stronger upstream failure state. Suggested aggregation:

`FAIL/BLOCKED > NOT_VERIFIED > PARTIAL > PASS`

The aggregate output is releasable only if every required stage for that action is PASS under the authoritative integration policy.

## Why this composition is efficient
The stages fail at different semantic layers, so expensive checks can be scheduled after cheap deterministic blockers. ARIG and static migration checks can run early; deeper metamorphic/mutation suites run only after structural prerequisites hold.

## Non-goals
- no direct NEXY mutation
- no automatic deployment
- no claim that these five tools cover all NEXY proof obligations
- no replacement for DOC-B/DOC-C/DOC-E authority
