# LEDGER
LEDGER_ID: NEXY-SPEC-CONVERGENCE-6F4920E8-20261005
TASK_ID: NEXY-SPEC-CONVERGENCE-6F4920E8-20261005
HEAD: 6f4920e8b34751fd7f13010e38e85eda5afadd7b
TREE: 47828e6ddd31614425d456d5da051c09beaca97d
SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
STATUS: PARTIAL / RELEASE_BLOCKED

| ITEM | EVIDENCE | STATUS | NOTE |
|---|---|---|---|
| SPEC-IDENTITY | uploaded DOCX SHA-256 = canonical SHA-256 | PASS | exact identity |
| TIME-ELAPSED-SEMANTICS | 88f0b335; core TSA accessor + LO2/I/O consumers + tests | STATIC_REPAIRED / NOT_EXECUTED | runtime gates unavailable |
| WORKFLOW-BRANCH-GOVERNANCE | 88f0b335; NEXY.ai-only inspected triggers | STATIC_REPAIRED | no branch created |
| STATIC-SCAN-E2E | 5880630d; tests/contract/static-determinism-gate.test.ts | STATIC_REPAIRED / NOT_EXECUTED | invokes scanRepository on fixture |
| CANONICAL-ORDERING | ae49beb4; packages/core/canonical-order.ts + authoritative call sites | STATIC_REPAIRED / NOT_EXECUTED | current blobs no localeCompare in inspected repaired paths |
| VAULT-SCAN-ROOT | 6f4920e8; scripts/check-static-determinism.ts | STATIC_REPAIRED / NOT_EXECUTED | root corrected vault -> packages/vault |
| EXACT-HEAD-TESTS | Actions runs 37221827962 / 37221827961 / 37221827979 / 37221827950 | BLOCKED_INFRA | steps/logs unavailable; no command execution proof |
| CLOCK-AUTHORITY | spec Layer-9 vs later hardware lock | CONFLICT/FREEZE | no silent precedence choice |
| PRODUCTION-TSA-INJECTION | 9c full-repo negative proof + delta review to 6f | NOT_VERIFIED | no production caller proven |
| RELEASE/DEPLOY | dependent CI jobs skipped | BLOCKED | no release attestation/deploy proof |
| WHOLE-PROJECT-COMPLETION | evidence denominator invalid without runtime gates | NOT_PROVEN | no percentage claim |

## Mutations authored by this execution
- 5880630d30b227b2a7db92056c7e01127a5e2fcd — test(determinism): verify repository scan end-to-end
- 6f4920e8b34751fd7f13010e38e85eda5afadd7b — fix(determinism): scan canonical Vault package

## Concurrent mutations preserved
- 88f0b335a06824aed007470ca42bd7312b115684
- ae49beb4f63d0defd3347a2a59d51ebffac05da2

A non-fast-forward update collision occurred while another writer advanced NEXY.ai. The attempted update was rejected by GitHub and was not force-pushed. The patch was rebased onto the new HEAD before 6f4920e8 was created.
