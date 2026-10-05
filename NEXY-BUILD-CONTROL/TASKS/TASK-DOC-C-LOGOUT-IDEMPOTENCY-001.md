# TASK-DOC-C-LOGOUT-IDEMPOTENCY-001

STATUS: SUPERSEDED_BY_PARALLEL_INTEGRATION
OWNER_CHAT: C-SOL-20261006-0202-0700-LOGOUT-IDEMPOTENCY
PRODUCT_REPO: goif74945-crypto/NEXY.AI-
BASE_BRANCH: NEXY.AI-Test-AI
BASE_SHA: 59b4d88e482d965e2a5554a0645dada5b827fa36
WORKER_BRANCH: work/C-SOL-20261006-0202-0700-logout-idempotency
AUTHORITATIVE_SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

## Requirement / product truth
FINAL DOC-C §4.2: POST /api/auth/logout revokes current or all sessions; idempotency is required and retry is safe with the same idempotency key.

## Proven gap
Current replay lookup is global by AuditLog.requestId=idempotency_key plus logout action set, before binding the replay to the authenticated session/action. A different valid session reusing an existing key can receive revoked=true without its session being revoked.

## Mutation scope
- packages/api/auth.ts
- tests/integration/auth/logout.spec.ts

## Constraints
Bind idempotent replay to the authenticated session and exact logout action. Preserve valid exact replay semantics. Do not widen error codes or touch unrelated auth behavior.


## Independent review result
- Parallel integration commit: c2a833cde90a51d7fd709937d66a4abea132739e
- Parallel regression evidence commit immediately before it: 77519350b839fe9371d2f80655495ab13d3b90a7
- Reviewed implementation binds replay to requestId=idempotency_key, exact action, actor=session.emailHash, resourceId=session.id, outcome=ACCEPTED.
- Replay lookup occurs after canonical session/device-binding resolution and before revoked-session rejection, preserving exact retry semantics while preventing cross-session/cross-action replay.
- Our worker implementation is intentionally NOT integrated because target already contains a stricter equivalent repair.
- GitHub Actions validation infrastructure remained unavailable: worker run 37360770351 / job 111934514447 failed before any workflow step executed.
