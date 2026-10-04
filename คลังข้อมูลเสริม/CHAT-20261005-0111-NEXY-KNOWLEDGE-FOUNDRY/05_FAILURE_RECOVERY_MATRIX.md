# Failure and Recovery Matrix

| Failure | Detection | Safe response | Evidence before resume |
|---|---|---|---|
| Requirement drift | output differs from authoritative spec | freeze expansion, restore scope | requirement diff |
| Hallucinated dependency | referenced API/file absent | mark UNKNOWN, inspect source | direct source result |
| Stale context | source exceeds freshness policy | refresh or isolate claim | timestamped evidence |
| Partial tool mutation | write only partly succeeds | inspect post-state, reconcile minimally | post-write read |
| Retry amplification | retries duplicate side effects | require idempotency/state check | side-effect ledger |
| Schema drift | producer/consumer mismatch | stop rollout, negotiate migration | contract tests |
| Silent data corruption | valid-shaped but wrong values | quarantine and compare authority | integrity checks |
| Agent loop | repeated action without information gain | stop and record exhausted hypotheses | attempt history |
| Verification illusion | test misses claimed behavior | redesign test from acceptance criterion | test mapping |
| Secret exposure | sensitive data enters logs/context | stop propagation and rotate where authorized | sanitized audit |

## Recovery law
Apply the smallest safe correction. Re-run the failed gate, then dependent regression gates. Never declare recovery merely because a corrective action executed.
