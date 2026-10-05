# Requirement Ledger

All requirements below are **lab requirements**, not canonical NEXY requirements.

| ID | Requirement | Authority | Implementation / Evidence | Status target |
|---|---|---|---|---|
| PF-001 | Same normalized input + policy yields same structural result | Lab contract | deterministic unit/property replay | E2 |
| PF-002 | Purpose mismatch cannot release datum | Lab contract + minimization rationale | evaluator + tests | E2 |
| PF-003 | Recipient mismatch cannot release datum | Lab contract | evaluator + tests | E2 |
| PF-004 | Sensitive+ data requires explicit recipient binding by default | Lab contract | metadata validation + wildcard regression | E2 |
| PF-005 | Sensitive+ external release requires bounded grant by default | Lab contract | consent evaluator + tests | E2 |
| PF-006 | Grant binds item + purpose + recipient + expiry + revocation state | Lab contract | `ConsentGrant.is_valid_for` + tests | E2 |
| PF-007 | Secret data cannot leave to non-local recipients under default policy | Lab contract | hard egress rule + property audit | E2 |
| PF-008 | Optional disallowed data may be removed without blocking legal remainder | Lab contract | `REDACT` path + tests | E2 |
| PF-009 | Required disallowed data blocks the release | Lab contract | `BLOCK` path + tests | E2 |
| PF-010 | Missing required grant asks rather than guessing consent | NEXY-compatible proposal | `ASK` path + tests | E2 |
| PF-011 | Terminal ASK/BLOCK/FREEZE contains zero payload | Lab invariant | property audit | E2 |
| PF-012 | Field-purpose rules remove unrelated top-level fields | Lab contract | minimizer + tests | E2 |
| PF-013 | Missing field rule fails closed for that field when field rules are active | Lab contract | minimizer behavior | E2 |
| PF-014 | Raw values never appear in receipt | AI-CONTEXT security direction | non-echo test/property audit | E2 bounded |
| PF-015 | Duplicate item IDs freeze | Integrity invariant | request validation test | E2 |
| PF-016 | Invalid purpose/recipient/expiry/field metadata freezes | Integrity invariant | validation paths + tests/compile | E1/E2 |
| PF-017 | Evaluator has no network/persistence side effect | Lab architecture | code inspection; runtime sandbox not exhaustively proven | E0/E1 limited |
| PF-018 | AI proposal remains non-governing until explicit adoption | AI-CONTEXT authority law | docs/adoption gates | E0 |
| PF-019 | No NEXY.AI repository mutation is required by this lab | User scope | GitHub mutation ledger | E0 scoped |
| PF-020 | External standards are rationale, not project authority | Authority separation | research record | E0 |
| PF-021 | A batch consent grant binds one exact request ID, purpose, recipient, expiry/revocation state, and exact set of at least two consent-requiring item IDs | Wave 07 lab contract | `ConsentBundleGrant` + focused tests | E2 |
| PF-022 | An active bundle whose item scope differs from the request's full consent-requiring item set freezes instead of broadening or partially guessing consent | Least-authority invariant | exact-scope validation + under/over-scope tests | E2 |
| PF-023 | Expired, revoked, request-mismatched, purpose-mismatched, or recipient-mismatched bundles are inert and cannot authorize release | Consent integrity invariant | negative tests + bounded audit | E2 |
| PF-024 | Duplicate grant IDs and overlapping active single/bundle or multiple-bundle authority freeze as ambiguous | Integrity invariant | ambiguity validation + adversarial tests | E2 |
| PF-025 | Bundle item ordering and request item ordering do not change the decision, payload, or receipt digest | Determinism invariant | order test + bounded permutations | E2 |
| PF-026 | Batch-consent verification records never echo raw payload marker values | Security boundary | marker non-echo bounded audit | E2 bounded |
| PF-027 | Batch consent remains AI-PROPOSED/NON-GOVERNING and cannot claim upstream human authorization authenticity | Authority boundary | docs + claim limitations | E0 |
| PF-028 | Every external request supplies explicit recipient-resolution metadata under the default reference policy | Wave 09 lab contract | `RecipientRouteProof` requirement + missing-proof test | E2 |
| PF-029 | Requested and resolved recipient identities must both equal the request's exact policy/grant recipient binding | Recipient integrity invariant | route validation + alias/substitution tests | E2 |
| PF-030 | Any observed redirect hop freezes because this lab has no adopted alias/redirect authority registry | Least-authority invariant | redirect-chain tests | E2 |
| PF-031 | Route proof metadata is strictly typed, nonblank, and bounded to at most eight reported hops | Fail-closed metadata boundary | malformed/blank/overlong tests | E2 |
| PF-032 | Existing consent grants cannot override a recipient-route mismatch | Consent integrity invariant | grant-plus-substitution negative test | E2 |
| PF-033 | Recipient-route aliases and payload markers are not echoed into receipts | Metadata minimization boundary | focused test + bounded audit | E2 bounded |
| PF-034 | Route metadata remains AI-PROPOSED/NON-GOVERNING and is not claimed as authenticated transport evidence | Authority/truth boundary | docs + limitations | E0 |

## Deliberately NOT VERIFIED by this prototype

Nested-object minimization; streaming/token-by-token egress; derived/inferred sensitive-data classification; real identity/authorization for grant issuers; revocation propagation; cryptographic receipt authenticity; distributed policy consistency; legal compliance; connector retention/deletion behavior; runtime bypass resistance in NEXY.AI; production latency/load behavior. Wave 07 proves only local exact-scope bundle semantics; it does not prove that a human validly granted consent. Wave 09 validates caller-supplied route metadata only; it does not authenticate a resolver, observe a network path, establish canonical alias equivalence, or prove dispatch-time destination integrity.
