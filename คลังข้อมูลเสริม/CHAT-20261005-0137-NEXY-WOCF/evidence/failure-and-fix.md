# Failure and Fix Record

## Failure F-001

During the first full verification run, E2 unit/adversarial verification failed 1 of 16 tests.

Failing test: `test_moderate_overlap_warns`.

Observed behavior:
- designed overlap score: `0.24144736842105263`;
- test-local warning threshold: `0.30`;
- actual decision: `ALLOW`;
- test expected: `WARN`.

## Root cause

The engine scoring formula was behaving as designed. The test fixture did not actually satisfy the warning boundary it claimed to exercise. Lowering a production threshold merely to make the test green would have changed semantics to satisfy a faulty test, so that option was rejected.

## Smallest safe correction

The fixture was changed to represent genuinely moderate overlap under the default policy by sharing more concept tags and objective vocabulary while remaining below the freeze threshold.

Corrected observed overlap: `0.4614285714285714` under default warning threshold `0.45` and freeze threshold `0.72`.

## Re-verification

The complete suite was rerun after the fixture correction and expansion. Final result: 18/18 unit/adversarial tests PASS, plus CLI allow/freeze scenario gates PASS.

This record demonstrates `failure -> diagnose -> smallest safe fix -> full rerun`. It does not claim production NEXY behavior.
