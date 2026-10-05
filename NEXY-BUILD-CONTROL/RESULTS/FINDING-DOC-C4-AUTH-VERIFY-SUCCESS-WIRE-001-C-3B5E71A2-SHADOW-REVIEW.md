# Shadow Review — Verify-OTAC Canonical Success Wire

CHAT_ID: C-3B5E71A2
FINDING_ID: FINDING-DOC-C4-AUTH-VERIFY-SUCCESS-WIRE-001
REQ_ID: REQ-DOC-C-4-2-AUTH-VERIFY-SUCCESS-WIRE-001
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
AUTH_BLOB: 0f8c8e21ce39f36b850c0db93ceadaa886088e6b
CSRF_BLOB: 3444b32561d8b5a11951822810381da66c3c8f92
WEB_CSRF_BLOB: 2e9974a1e99db18f7c51057906094ec1ff975dd6
VERIFY_TEST_BLOB: b81b1a963c932aa942d19cca8b9b776d0aeb6031
DECISION_PATH_TEST_BLOB: 3cefe463642b43735c5e61cd018dcd9fae3d6967
ROLE: SHADOW_REVIEWER
VERDICT: FINDING_CONFIRMED_P1

## Exact-head observations

- Final DOC-C canonical success data is exactly session_id, expires_at, role.
- handleVerifyOtac currently returns session_id, email_hash, expires_at, role, csrf_token.
- issueCsrfToken(res) already sets __Host-nexy-csrf as Secure, SameSite=Strict, httpOnly=false.
- apps/web/lib/csrf.ts reads that cookie through document.cookie and derives the x-csrf-token header from it.
- apps/web/components/OtacLoginForm.tsx does not read csrf_token or email_hash from the verify response; on success it only redirects.
- Repository search found no application consumer that requires verify-OTAC response-body email_hash.
- The existing auth decision-path oracle explicitly expects csrf_token, so that expectation is part of the test-oracle drift.

## Minimal repair design

1. Keep session cookie issuance unchanged.
2. Keep device-binding cookie issuance unchanged.
3. Keep csrfModule.issueCsrfToken(res) on every successful verify-OTAC so the readable CSRF cookie continues to exist.
4. Do not place the returned CSRF token into canonical response data.
5. Remove email_hash from canonical response data.
6. Return exactly:
   data: { session_id, expires_at, role }
7. Change tests to assert exact equality of canonical data and separately assert that the CSRF cookie is issued.
8. Preserve owner-session-cap confirmation behavior and all failure envelopes.

## Security review

Removing csrf_token from response data does not remove CSRF issuance or validation because the production web client reads the non-httpOnly CSRF cookie directly. The repair therefore narrows the canonical wire contract without weakening the double-submit mechanism.

## Required regression cases

- successful verify returns exactly session_id/expires_at/role
- successful verify still sets __Host-nexy-session
- successful verify still sets __Host-nexy-csrf
- successful verify still sets device-binding cookie
- apps/web/lib/csrf.ts can derive x-csrf-token from the issued cookie
- no verify success response contains email_hash or csrf_token
- failure paths remain unchanged

SOURCE_MUTATION: NONE
UPSTREAM_MUTATION: NONE
MUTATION_BLOCKER: INC-BRANCH-NAMESPACE-001
