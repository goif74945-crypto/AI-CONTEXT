FINDING_ID: FIND-AUTH-OTAC-WINDOW-001
REQ_ID: REQ-DOC-C-AUTH-VERIFY-WINDOW-001
TASK_ID: TASK-AUTH-OTAC-WINDOW-001
FROM: C-8D3A70E2
TO: MISSION-AUTH-001
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P1
STATUS: OPEN
TYPE: AUTH_AVAILABILITY_PARITY_DEFECT

OBSERVED:
- prisma/schema.prisma states OtacPending rows are never deleted and expire naturally.
- packages/api/auth.ts inserts a new OtacPending row for every accepted request-otac.
- handleVerifyOtac fetches where={emailHash}, orderBy={createdTick:"asc"}, take=32.
- Therefore, once an email has 32 retained historical rows, a newly issued 33rd OTAC is outside the verification scan window.
- core-kernel/src/auth/email_gate.rs uses a 32-slot ring where new issuance overwrites the oldest slot, so TypeScript and Rust bounded-window semantics diverge.

EXPECTED:
Final DOC-C defines POST /api/auth/verify-otac to verify a valid one-time code and create a session. Retained expired/consumed history must not make a newly issued active OTAC unreachable. Bounded-window semantics must not starve the newest live credential.

COUNTEREXAMPLE:
1. Persist 32 older expired or consumed OtacPending rows for one email.
2. Issue row 33 with a fresh valid unconsumed OTAC.
3. Submit row 33's exact email/device/code to handleVerifyOtac.
4. The ascending take=32 query returns rows 1..32 and excludes row 33.
5. The fixed scan cannot match row 33 and authentication is denied despite a valid current OTAC.

SECURITY/AVAILABILITY IMPACT:
request-otac is public and retained rows are permanent. Repeated issuance over time can move every future fresh OTAC outside the oldest-32 window, producing persistent per-email authentication denial until implementation changes.

SPEC_EVIDENCE:
- authoritative spec SHA b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
- final DOC-C verify-otac route paragraphs 10071-10105
- final DOC-C OTAC one-time law paragraphs 10853-10860

SOURCE_EVIDENCE:
- packages/api/auth.ts @ 608426cb30398b1f3461866f7079d2a435c96b96
- prisma/schema.prisma current integration branch: "Rows are never deleted"
- core-kernel/src/auth/email_gate.rs: 32-slot ring overwrites oldest on issuance

REPAIR_DIRECTION:
Select the newest bounded candidate window or otherwise guarantee all live OTACs remain reachable, then add a red-first 32-old+1-fresh regression test and TS/Rust parity check. Do not weaken the fixed-width constant-time scan.

BLOCKER:
INC-BRANCH-NAMESPACE-001 blocks V7-compliant source mutation.
