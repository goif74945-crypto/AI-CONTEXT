# Requirement Ledger — Evidence Capsule Lab

| ID | Requirement | Authority | Reference location | Evidence | Status |
|---|---|---|---|---|---|
| EC-001 | Derived disclosure must not rewrite original lineage | NEXY DOC-C context | architecture | design inspection | PASS design |
| EC-002 | Canonical input must be deterministic | AI-proposed | reference_impl.py | unit test key order | PASS E2 |
| EC-003 | Floats/non-string object keys fail closed | AI-proposed | canonical() | negative tests | PASS E2 |
| EC-004 | Field value bound to salted commitment | AI-proposed | leaf() | tamper test | PASS E2 |
| EC-005 | Disclosed fields prove inclusion in capsule root | AI-proposed | proof()/verify_proof() | valid + bad proof tests | PASS E2 |
| EC-006 | Capsule metadata authenticated | AI-proposed | seal()/verify() | header tamper test | PASS E2 |
| EC-007 | Presentation audience authenticated | AI-proposed | present()/verify() | wrong-audience test | PASS E2 |
| EC-008 | Unauthorized role-field disclosure denied | AI-proposed | role policy | policy tests | PASS E2 |
| EC-009 | Expired/stale presentation rejected | AI-proposed | verify() | expiry/stale tests | PASS E2 |
| EC-010 | Replay can be rejected | AI-proposed | replay set hook | replay test | PASS E2 |
| EC-011 | Required fields can be enforced | AI-proposed | verify(required_fields) | negative test | PASS E2 |
| EC-012 | Deterministic fixture produces stable capsule ID | AI-proposed | fixed salt/nonce fixture | deterministic test | PASS E2 |
| EC-013 | Reference code/test Git blobs equal tested local bytes | Verification law | Git object identity | git hash-object vs GitHub blob SHA | PASS E1/E2 linkage |
| EC-014 | Production signer must be asymmetric/governed | adoption gate | future work | not implemented | NOT_VERIFIED |
| EC-015 | Durable distributed replay storage | adoption gate | future work | not implemented | NOT_VERIFIED |
| EC-016 | NEXY runtime integration | protected/out of scope | none | no E3+ evidence | NOT_VERIFIED |

“PASS design” is not a runtime PASS. Rows intentionally preserve evidence class boundaries.