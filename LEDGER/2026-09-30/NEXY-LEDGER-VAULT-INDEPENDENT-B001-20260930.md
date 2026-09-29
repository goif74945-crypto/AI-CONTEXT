# LEDGER — VAULT Independent Batch 001

LEDGER_ID: NEXY-LEDGER-VAULT-INDEPENDENT-B001-20260930

| Requirement | Claim | Proof | Status |
|---|---|---|---|
| REQ-0378 | revision allocation is serialized per artifact | packages/vault/versioning.ts advisory transaction lock + durable max allocator | FIXED_PENDING_RUNTIME_VALIDATION |
| REQ-0374 | vault commit no longer claims blob verification before provider proof | vault/repository.ts BLOB_VERIFICATION_PENDING + provider verifyHash paths | FIXED_PENDING_RUNTIME_VALIDATION |
| Non-conflict constraint | no shared validator/boundary/observability file modified | changed-file set limited to 4 VAULT/test files | PASS |

checkpoint_head: 0f9c8c65e2ab7b959f03264569430afc256f268a
checkpoint_tree: 7d035b597f905878d879abb779fe549762be3f24
verdict: PARTIAL
