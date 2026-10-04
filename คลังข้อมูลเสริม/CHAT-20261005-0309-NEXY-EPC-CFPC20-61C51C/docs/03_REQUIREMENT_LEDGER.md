# CFPC-20 Requirement Ledger

| ID | Requirement | Evidence target |
|---|---|---|
| CFPC-R01 | Exactly 20 named mechanisms | architecture + source/tests |
| CFPC-R02 | Checked signed Q64.64 quantitative path | compile + unit/property tests |
| CFPC-R03 | No binary float authoritative path | static scan |
| CFPC-R04 | Explicit i128 overflow failure | E2 tests |
| CFPC-R05 | Bounded symbolic grammar | E2 negative tests |
| CFPC-R06 | Unbound workload variables freeze | E2 |
| CFPC-R07 | Negative monotonic coefficients rejected | E2 |
| CFPC-R08 | Ten required resource surfaces | E2 certificate tests |
| CFPC-R09 | Each resource bound is non-compensatory | E2 |
| CFPC-R10 | Required verification steps cannot disappear | E2 |
| CFPC-R11 | Unsafe degradation contract freezes | E2 |
| CFPC-R12 | Canon/Core/auto-promotion requests freeze | E2 |
| CFPC-R13 | Canonical output insertion-order independent | replay E2/E3 |
| CFPC-R14 | Certificate binds resource policy/assumptions/verification/degradation | E2 |
| CFPC-R15 | Independent compiler validation | g++ + clang++ |
| CFPC-R16 | Sanitizer run | ASan/UBSan |
| CFPC-R17 | Tested bytes get SHA-256 manifest | evidence manifest |
| CFPC-R18 | Published bytes equal tested bytes | GitHub read-back |
| CFPC-R19 | NEXY.AI stays read-only | final head recheck + mutation log |
| CFPC-R20 | No NEXY integration/deployment claim | final audit |
