# LEDGER 20261008-NEXY-EX012-LAW-PRODUCT-REPAIR
| ID | Source | Claim | Proof | Verdict |
|---|---|---|---|---|
| EX012-01 | Local authoritative DOCX | SHA256 exact canonical | container sha256sum | VERIFIED_SOURCE |
| EX012-02 | GitHub NEXY.ai | Initial HEAD 44bcb851, old law blob f0ae1b | live branch/blob read | VERIFIED_PRESTATE |
| EX012-03 | Remote Desktop Commander isolated clone | Original impossible quorum candidate accepted | actual Vitest RED 2 failed / 3 passed | VERIFIED_FAILURE_REPRODUCTION |
| EX012-04 | Local Git patch and GitHub blobs | New law guard byte-match and tests | patched blob 696acae9, test blob 417f3932 | VERIFIED_SOURCE |
| EX012-05 | Remote Windows Vitest | LAW + related contracts | GREEN 58/58 | VERIFIED_LOCAL_TEST |
| EX012-06 | Remote Windows tsc | backend source typecheck | exit0 after Prisma generate | VERIFIED_LOCAL_TEST |
| EX012-07 | Remote Windows broad JSON | 905/911 pass, six failure cases | 2 cargo, 2 tier-depth, 2 attestation | PARTIAL_BROAD_FAILURE |
| EX012-08 | GitHub commit 90fac4835788e867559858fc92d093ded3dcb1eb | Product LAW patch/test committed only on NEXY.ai | expected-head fast-forward and two blob readbacks | VERIFIED_COMMITTED |
| EX012-09 | GitHub current Actions | 4 runs fail on new commit, exact-head steps=[] | GitHub run/job API | CI_FAILURE_CAUSE_UNKNOWN |
| EX012-10 | G3/DOC-E | Real DB Redis test, release approval not provided | no tests or signoffs | NOT_VERIFIED / NOT_AUTHORIZED |
VERSION: 1
