# Requirement Ledger

| ID | Requirement | Evidence | Status |
|---|---|---|---|
| R1 | Exactly five distinct concepts AEAP/RCTC/IDW/CDPP/CRG | design + bundle | PASS |
| R2 | Explicit AI-proposed/non-canon labels | README/design | PASS |
| R3 | Deterministic equivalent-input behavior | property tests + fingerprints | PASS |
| R4 | Fail closed on malformed/materially insufficient input | unit/adversarial tests | PASS |
| R5 | No hidden external I/O in core | static audit | PASS |
| R6 | No NEXY.AI mutation | mutation boundary + connector history for this mission | PASS |
| R7 | IDW candidate only | design + tests | PASS |
| R8 | RCTC requires explicit APPROVED authority | design + tests | PASS |
| R9 | AEAP plans evidence only | design + tests | PASS |
| R10 | CDPP does not invent causes/predictions | design + tests | PASS |
| R11 | CRG requires consumer/usage/replacement/rollback/authority evidence | design + tests | PASS |
| R12 | PASS claims backed by executed evidence | 03_EVIDENCE.md | PASS |
| R13 | Design + code + tests + evidence persisted together | docs + bundle parts | PASS once commit/readback is recorded in final audit |
| R14 | No placeholder implementation | static audit | PASS |
| R15 | NEXY compatibility via adapter contracts only | compatibility record + adapters | PASS |

## Acceptance criteria
A1 strict TypeScript compile: PASS.
A2 unit/adversarial tests: PASS 26/26.
A3 integration tests: PASS 2/2.
A4 input-order invariance: PASS 5 property suites, including exhaustive 36-permutation checks for AEAP and CDPP small fixtures.
A5 negative paths each concept: PASS.
A6 no NEXY.AI source import/write: PASS for static import audit and mission mutation boundary.
A7 persisted project readback: to be finalized by 06_FINAL_AUDIT.md after commit.
A8 final audit maps all requirements: this ledger plus 06_FINAL_AUDIT.md.

If A7 readback fails, final task status must not be COMPLETE.
