# Requirement Ledger — Final

| ID | Requirement | Evidence | Status |
|---|---|---|---|
| R1 | Exactly five distinct concepts | design + tested bundle | PASS |
| R2 | AI-proposed/non-canon labels | README/design | PASS |
| R3 | Deterministic equivalent-input behavior | property tests + fingerprints | PASS |
| R4 | Fail closed on malformed/materially insufficient input | unit/adversarial tests | PASS |
| R5 | No hidden external I/O in core | static audit | PASS |
| R6 | No NEXY.AI mutation | scope + executed mutation history | PASS |
| R7 | IDW candidate only | design + tests | PASS |
| R8 | RCTC requires explicit APPROVED authority | design + tests | PASS |
| R9 | AEAP plans evidence only | design + tests | PASS |
| R10 | CDPP does not invent causes/predictions | design + tests | PASS |
| R11 | CRG requires consumer/usage/replacement/rollback/authority evidence | design + tests | PASS |
| R12 | PASS claims backed by executed evidence | 03_EVIDENCE.md | PASS |
| R13 | Design + code + tests + evidence persisted together | repository readback + bundle manifest | PASS |
| R14 | No placeholder implementation | static audit | PASS |
| R15 | NEXY compatibility via adapter contracts only | compatibility design + adapter code | PASS |

## Acceptance
A1 strict TypeScript compile: PASS.
A2 unit/adversarial: PASS 26/26.
A3 integration: PASS 2/2.
A4 order invariance/property: PASS 5/5, including 36-permutation fixtures for AEAP and CDPP.
A5 fail-closed negative paths: PASS.
A6 no protected NEXY source import/write: PASS.
A7 persisted project readback: PASS.
A8 final audit requirement mapping: PASS.

## Evidence ceiling
E0/E1/E2/E3: PASS for this standalone reference package.
E4/E5/E6/E7 for NEXY native runtime/deployment/physical behavior: NOT_VERIFIED and not claimed.
