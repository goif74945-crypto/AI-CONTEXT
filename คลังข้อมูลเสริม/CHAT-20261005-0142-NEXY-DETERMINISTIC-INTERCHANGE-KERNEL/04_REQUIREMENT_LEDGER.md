# Requirement Ledger

| ID | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|
| NDIK-R01 | Same allowed logical object yields same canonical text independent of insertion order | `canonical.py` object sorting | `test_key_order_is_irrelevant`, 120-permutation grid | PASS_EXECUTED |
| NDIK-R02 | Repeated execution has no hidden nondeterminism | no clock/random/env access | 1,000-repeat property test | PASS_EXECUTED |
| NDIK-R03 | Unicode-equivalent strings normalize consistently | NFC normalization | Unicode composed/decomposed test | PASS_EXECUTED |
| NDIK-R04 | Normalization key collision fails closed | collision detector | negative test | PASS_EXECUTED |
| NDIK-R05 | Floating-point ambiguity fails closed | exact float rejection | parse/runtime negative tests | PASS_EXECUTED |
| NDIK-R06 | Cross-JS unsafe integers fail by default | ±(2^53−1) limits | boundary tests | PASS_EXECUTED |
| NDIK-R07 | Duplicate raw JSON keys fail closed | `object_pairs_hook` | negative test | PASS_EXECUTED |
| NDIK-R08 | Cyclic runtime structures fail closed | active-container identity set | list/dict cycle tests | PASS_EXECUTED |
| NDIK-R09 | Resource bombs are bounded | depth/node/output-byte limits | limit tests | PASS_EXECUTED |
| NDIK-R10 | Hash purposes cannot collide by accidental reuse of same bytes | domain separation | domain test | PASS_EXECUTED |
| NDIK-R11 | Envelope payload tampering is detected | payload hash verify | tamper test | PASS_EXECUTED |
| NDIK-R12 | Envelope metadata/provenance tampering is detected | envelope hash verify | provenance tamper test | PASS_EXECUTED |
| NDIK-R13 | Envelope does not hide implicit current time | required caller `observed_at` | empty-time negative test + code inspection | PASS_EXECUTED |
| NDIK-R14 | Project is not presented as production NEXY integration | explicit non-goals/status | README/proposal audit | PASS_STATIC |
