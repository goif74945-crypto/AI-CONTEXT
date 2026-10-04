# REQUIREMENT LEDGER

| ID | Requirement | Implementation | Evidence | Final status |
|---|---|---|---|---|
| R1 | Never silently promote authority through transform | `derive()` minimum authority floor | unit + property tests | PASS |
| R2 | Prevent assurance inflation | intersection + preservation allowlist | unit + property tests | PASS |
| R3 | Preserve taints across transforms | taint union + 64-step chain | unit + property tests | PASS |
| R4 | Bind verification to exact artifact | content-addressed receipt + artifact ID check | negative unit tests | PASS |
| R5 | Detect receipt content tamper | receipt SHA-256 identity revalidation | unit + wire tests | PASS |
| R6 | Prevent generic clearing of protected taints | `PROTECTED_TAINTS` guard | negative unit tests | PASS |
| R7 | Deterministic release result | immutable inputs + sorted reasons | repeatability tests + duplicate demo | PASS |
| R8 | Freeze on stale/future artifacts when policy requires freshness | epoch checks | unit tests | PASS |
| R9 | Do not treat E0–E7 as universal rank | exact assurance tags | unit test | PASS |
| R10 | Tamper-evident artifact identity | canonical SHA-256 identity | unit + wire tests | PASS |
| R11 | Strict future adapter boundary | versioned fail-closed wire v1 | 12 wire tests | PASS |
| R12 | No third-party runtime dependency | stdlib-only implementation | compile/import/test | PASS |
| R13 | Runnable proof path | `examples/demo.py` | executed twice, outputs identical | PASS |
| R14 | Performance smoke/stress path | `bench/stress.py` | 20k transforms + 50k decisions | PASS |
| R15 | No placeholder implementation | source audit | grep audit | PASS |
| R16 | No NEXY.AI mutation | isolated AI-CONTEXT lab | action-scope audit | PASS |
| R17 | Actual NEXY.AI integration/deployment | explicitly forbidden/out of scope | none | NOT_VERIFIED |
