# CASES 20261008-NEXY-QUEUE-CAGE-EXECUTION-007-CROSS
Product HEAD at source audit: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
Control PREWRITE HEAD: b8b11254dc1c5a4091de883ec35fbd7a4d70df85
DOCX SHA256 locally computed: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

## QUEUE-CANCEL-RACE-006
Reproduction: current dispatch.ts @ blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29 reads PENDING, awaits enqueueDirective(); OWNER cancel sets CANCELLED; unconditional ID-only update overwrites ENQUEUED. Failure path similarly overwrites FAILED. Node harness executed five deterministic model tests with two RED-behavior observables; model is not source-integrated validation.
REQUIRED PATCH: narrow try/catch around only enqueue call; retain durable optimistic status+attempt counter; on success and failure perform updateMany with id,status,attempts predicate. On zero, read durable status for truthful CANCELLED/COMPLETED/PROCESSING/FAILED response. Must not count an unsafely enqueued Redis job as an accepted delivery. Worker guard prevents PROCESSING transition from CANCELLED (source check), but provider cancellation/release must be integration tested.
REGRESSION MATRIX: success/cancel, failure/cancel, Redis publish-DB conflict, duplicate reconciler, failed retry policy QUEUE_UNAVAILABLE only, allowlist/maxAttempts, stale worker claim, STOP while processing, crash after DB commit, DB outage. Test real pg+Redis before product commit.
## CAGE-ISOLATION-006
cage.ts source: Linux bwrapAvailable false triggers trusted direct spawn without namespaces; seccomp JSON not used in Linux spawn path. Reject silent production fallback; add real negative test; if production isolation unavailable, explicit safe failure. No product patch until runtime test and valid policy fence.
