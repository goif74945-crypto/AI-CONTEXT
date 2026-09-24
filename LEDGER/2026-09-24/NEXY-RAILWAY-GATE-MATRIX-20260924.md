# NEXY Railway gate ledger

Deployment: `aedd277b-38b8-4811-875a-bba1468a0d5f`

| Gate | Result |
|---|---|
| npm_ci | PASS |
| prisma_generate | PASS |
| typecheck | PASS |
| contract | PASS |
| integration | PASS |
| full | PASS |
| coverage | PASS |
| coverage_check | FREEZE/FAIL — authority ambiguity |
| doc_c | PASS |
| web_build | PASS |
| overall | FAIL |

API coverage: lines 82.00%, statements 80.38%, functions 91.26%, branches 71.98%.
Core: lines 95.65%, statements 95.87%, functions 93.75%, branches 93.22% — PASS.
Law: 100% all standard metrics — PASS.
Judge: lines/statements/functions 100%, branches 97.06% — PASS.

Repair status: previous owner-recovery test-harness defect is VERIFIED FIXED because full suite and coverage suite now pass. Remaining blocker is policy/authority ambiguity; no evidence-safe software repair exists without authoritative coverage metric semantics.
