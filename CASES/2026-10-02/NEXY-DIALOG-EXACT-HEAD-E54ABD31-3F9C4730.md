# CASE — NEXY DIALOG exact-head convergence E54ABD31

- CASE_ID: NEXY-DIALOG-EXACT-HEAD-E54ABD31-3F9C4730
- trace_id: NEXY-E54ABD31-3F9C4730-20261002
- status: OPEN_EXTERNAL_BLOCKER

## Cause
Adding DIALOG exposed three real release-gate defects in sequence: UI type narrowing, forbidden active→experimental dependency, and API branch coverage regression. After those were repaired, stale E10 provider identity prevented promotion until a real current-head deploy/rollback receipt chain was rebuilt.

## Proven state
Exact-head deployment `3f9c4730-0681-454f-bba8-0fde2484bdfe` executed `e54abd3122427dcfc27f81cc725ec0f43ff00837` / `0ad78e8f8fcdbbeb3141e483fa31e70172e2a08c` and completed SUCCESS. Software gates pass. DOC-E E1-E10 and E12 pass. E11 alone is BLOCKED_EXTERNAL.

## Rollback proof
Railway rollback deployment `0f710de0-a24f-4331-b976-f0e2f871c96c` was created with reason=rollback, status=SUCCESS, targeting `8ec411af-170b-412f-8647-4c75e4515cf3`. The rollback runtime campaign verified E1-E10/E12 and emitted all six required alarm classes.

## Prevention
- retain strict TypeScript and boundary tests;
- do not weaken coverage thresholds;
- bind provider receipts to exact SHA/tree;
- never reuse stale provider receipts across HEAD changes;
- never synthesize E11 human authorization.
