FINDING_ID: FIND-AUTH-OTAC-WINDOW-001
REQ_ID: REQ-DOC-C-AUTH-VERIFY-WINDOW-001
TASK_ID: TASK-AUTH-OTAC-WINDOW-001
FROM: C-8D3A70E2
TO: MISSION-AUTH-001
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P1
STATUS: OPEN
TYPE: AUTH_AVAILABILITY_DEFECT_WITH_CONDITIONAL_PARITY

OBSERVED:
- prisma/schema.prisma states OtacPending rows are never deleted and expire naturally.
- packages/api/auth.ts inserts a new OtacPending row for every accepted request-otac.
- handleVerifyOtac fetches where={emailHash}, orderBy={createdTick:"asc"}, take=32.
- Therefore, once an email has at least 32 retained historical rows, a newly issued later OTAC can fall outside the current verification query window.
- core-kernel/src/auth/email_gate.rs uses a 32-slot ring where new issuance overwrites the oldest slot. This is source-level semantic divergence evidence, but cross-runtime parity is only a required closure item after the two implementations are proven to carry the same active auth contract.

EXPECTED:
Final DOC-C defines POST /api/auth/verify-otac to verify a one-time code and create a session. Retained historical rows must not make a newly issued active valid credential unreachable. Final DOC-C does not prescribe a 32-slot scan.

COUNTEREXAMPLE:
1. Persist 32 older retained OtacPending rows for one email.
2. Issue row 33 with a fresh valid unconsumed OTAC.
3. Submit row 33's exact email/device/code to handleVerifyOtac.
4. The current ascending take=32 query returns rows 1..32 and excludes row 33.
5. The fixed scan cannot match row 33 and authentication is denied despite a valid current OTAC.

SECURITY/AVAILABILITY IMPACT:
request-otac is public and OtacPending history is retained. Under the current oldest-first bounded query, accumulated history can starve later valid credentials and create persistent per-email authentication denial until implementation changes.

SPEC_EVIDENCE:
- authoritative spec SHA b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
- FINAL VERDICT paragraphs 9834-9845 establishes DOC-C as sole build obligation.
- final DOC-C auth defaults paragraphs 9910-9949 define OTAC/session parameters but no session_slots.
- final DOC-C verify-otac paragraphs 10071-10105 defines the route purpose, audit behavior, response and canonical errors.
- paragraphs 10853-10860 describe replay prevention outside final DOC-C and MUST NOT be cited as final-DOC-C build authority.

SOURCE_EVIDENCE:
- packages/api/auth.ts @ 608426cb30398b1f3461866f7079d2a435c96b96.
- prisma/schema.prisma current integration branch: retained OtacPending rows.
- core-kernel/src/auth/email_gate.rs: source-level 32-slot ring behavior.

REPAIR_DIRECTION:
Select a candidate set that guarantees newer valid active OTAC reachability, such as a newest-first bounded window if compatible with all verified semantics. Preserve constant-width comparison/no early return as justified hardening unless separately disproven. Add a red-first retained-history regression. Add cross-runtime parity testing only after active-contract equivalence is established.

BLOCKER:
INC-BRANCH-NAMESPACE-001 blocks V8-compliant worker source mutation because V8 retains NEXY.AI-Test-AI/work/<TASK_ID>, which conflicts with the existing integration ref.
