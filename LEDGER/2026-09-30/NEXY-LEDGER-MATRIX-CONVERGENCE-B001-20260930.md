# LEDGER — NEXY Matrix Convergence Batch 001

LEDGER_ID: NEXY-LEDGER-MATRIX-CONVERGENCE-B001-20260930

| Claim | Proof | Status | Risk |
|---|---|---|---|
| Current source denominator is 837 normalized rows | CURRENT-SYSTEM-FEATURE-BUILD-MATRIX + workbook Build Matrix 837 data rows | PASS | low |
| Legacy 215 registry is not current truth | AI-CONTEXT current matrix policy | PASS | high if violated |
| Current NEXY.ai HEAD is fb4f0f064ffe03d032f160f397a515538b4a86bd | GitHub branch latest commit observation | PASS | low |
| Exact HEAD Railway validation reached terminal SUCCESS | deployment 8ecc0830-d1c4-442f-a282-491a79d166e2 | PASS | low |
| Full test suite passes current HEAD | Railway logs: 117/117 files, 859/859 tests | PASS | low |
| Coverage gates pass | Railway coverage_check metrics recorded in task | PASS | low |
| DOC-C static gate passes | Railway doc_c exit=0 | PASS_WITH_LIMIT | does not equal release authorization |
| Web build passes | Railway web_build exit=0 | PASS | low |
| Migration forward/rollback/reapply/status roundtrip passes | Railway E3 hashes + exit=0 | PASS | low |
| All 837 matrix rows implemented and evidenced | exhaustive row-level mapping not completed | NOT_VERIFIED | critical |
| REQ-0005,0007,0008,0012 have exact behavior-level evidence | currently insufficient | NOT_VERIFIED | medium |

VERDICT: PARTIAL
