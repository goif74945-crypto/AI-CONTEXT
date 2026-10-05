# Independent Authority Challenge — DOC-C §4.2 verify-otac success wire

REVIEW_ID: RV-DOC-C4-AUTH-VERIFY-C-2CFA8A5D
CHAT_ID: C-2CFA8A5D
TASK_ID: TASK-DOC-C4-AUTH-VERIFY-SUCCESS-WIRE-001
REQ_ID: REQ-DOC-C-4-2-AUTH-VERIFY-SUCCESS-WIRE-001
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
ROLE: INDEPENDENT_RED_TEAM / SPEC_PROSECUTOR
RESULT: AUTHORITY_CHALLENGE
SOURCE_MUTATION: NONE

FACT:
1. Primary final DOC-C paragraphs 10027-10037 establish Global API Law. They require SystemEnvelope<T>, secure session + CSRF for mutating routes except OTAC request/verify, idempotency unless exempt, and declared auth/RBAC/retry/audit/error policies.
2. Primary final DOC-C paragraphs 10071-10105 declare POST /api/auth/verify-otac and show success data members session_id, expires_at, role.
3. A full scan of final DOC-C paragraphs 9886-10499 found no occurrence of `exact`, `additional`, `extra`, or `closed`; the only `strict` occurrence is directive mode `"strict"`, not object-shape semantics.
4. The five `only` occurrences in final DOC-C concern AUDITOR audit emission, OWNER RBAC, or STABLE-before-emission state law; none closes response objects against additional members.
5. Runtime packages/api/auth.ts@608426cb returns additional email_hash and csrf_token in verify success data. This is a verified source fact.
6. tests/coverage/auth-decision-paths.test.ts@608426cb expects csrf_token and the login flow uses CSRF issuance as an active security mechanism.

CHALLENGE:
The derived requirement adds the statement "exactly session_id, expires_at, role" and forbids extra response members, but primary final DOC-C does not explicitly establish closed/exact response-object semantics. Absence from the displayed TypeScript shape is not, by itself, an explicit prohibition under V8 NO GUESSING / AUTHORITY LAW.

SECURITY RISK:
Removing csrf_token or changing its transport solely to satisfy an unproven exactness interpretation can break CSRF bootstrap or force a new security design not required by primary build authority.

SAFE VERDICT:
- Required declared members remain active obligations.
- No source field-removal repair should be authorized solely by the unproven closed-shape inference.
- First prove an active final-DOC-C clause establishing closed response objects, or amend/reclassify the derived requirement.
- Preserve CSRF issuance/session/device-binding behavior unless separately proven defective.

RELATED_FINDING:
F-2CFA8A5D-DOC-C4-EXACTNESS-AUTHORITY

CI:
Exact integration SHA has workflow run 37240273646, but all nine failed jobs inspected executed zero steps; classification remains EXECUTION_INFRA_FAILURE, not PASS or CODE_FAIL.
