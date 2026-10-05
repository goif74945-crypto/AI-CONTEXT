TASK_ID: TASK-AUTH-OTAC-WINDOW-001
REQ_ID: REQ-DOC-C-AUTH-VERIFY-WINDOW-001
REVIEWER_CHAT: C-9B6A4E27
STATUS: PREIMPLEMENTATION_REVIEW
REVIEW_RESULT: AUTHORITY_CORRECTION_REQUIRED
BASE_SHA_REVIEWED: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

FACT:
- packages/api/auth.ts selects the oldest rows using createdTick ascending with take=32.
- Retained historical rows can therefore exclude a newly issued valid OTAC.
- Final DOC-C requires verify-otac to verify a one-time code and create a session.
- Final DOC-C does not define session_slots or a 32-slot scan.
- packages/api/vnext-config.ts labels session_slots=32 as an internal parameter not part of DOC-C canonical config.

RESULT:
The valid-code reachability gap is real, but the requirement must not attribute the exact number 32 to DOC-C.

SAFE DIRECTION:
After the worker-branch incident is resolved, prefer newer relevant candidates over oldest history while preserving existing constant-width security hardening unless separate evidence requires a change. Use deterministic ordering appropriate to the persisted model.

UNKNOWN:
Rust/TypeScript same-contract parity for this exact auth path requires separate proof; similar implementation names are not enough.

SOURCE_MUTATION: NONE
BLOCKER: INC-BRANCH-NAMESPACE-001
FINDING: F-9B6A4E27-AUTH-WINDOW-AUTHORITY
