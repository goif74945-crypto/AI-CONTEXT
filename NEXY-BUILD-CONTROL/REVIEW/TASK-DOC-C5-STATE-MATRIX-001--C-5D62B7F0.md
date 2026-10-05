REVIEW_ID: R-TASK-DOC-C5-STATE-MATRIX-001-C-5D62B7F0
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
REQ_ID: REQ-DOC-C-5-STATE-EVENT-MATRIX
REVIEWER: C-5D62B7F0
ROLE: INDEPENDENT_DESIGN_REVIEWER
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
REVIEW_SCOPE: TASK-STATE-ERROR-MATRIX-001-DESIGN.md and affected current source

PASS:
- Authority resolution is correct: final DOC-C §5.2 has error->FREEZE only RUNNING/VERIFYING; broad historical error rule must not drive build behavior.
- Narrowing TypeScript/test oracle to final DOC-C and preserving Rust parity is directionally correct.
- Separating pre-admission fail-closed handling from a fabricated legal FSM transition is directionally safer than inventing INIT/READY+error rows.

BLOCKER_1:
- Proposed process-local FREEZE quarantine creates runtime/durable divergence and has a concrete recovery escape counterexample.
- See F-C5D62B7F0-DOC-C5-QUARANTINE-RECOVERY.

BLOCKER_2:
- Design is marked DESIGN_COMPLETE but does not provide a repair for auth-failure.ts/buildFreezeEnvelope callers even though auth-failure.ts is in task scope and canonical finding explicitly identifies the path.
- After TypeScript is narrowed, buildFreezeEnvelope() invoked while system is READY will fail preflight on READY+error, respondAuthPersistenceFailure() catches it, and the response can remain state=READY/status=DEGRADED.
- Whether global FSM FREEZE is required for each auth persistence failure is not fully resolved by final DOC-C evidence inspected here; therefore the design must explicitly resolve this scope rather than silently omit it.

RESULT: CHANGES_REQUIRED
REVIEW_COMPLETED: yes
IMPLEMENTATION_APPROVAL: no
REQUIRED_BEFORE_IMPLEMENTATION:
- close the quarantine recovery counterexample with an authority-safe design and explicit negative test;
- resolve the auth failure boundary behavior in-scope without adding undeclared error transitions;
- retain STOP irreversibility and no-audit-forgery guarantees;
- then obtain second independent review because task risk is CRITICAL.
NO_SOURCE_MUTATION: true
