# LEDGER
LEDGER_ID: NEXY-SPEC-CONVERGENCE-A3E75C76-20261005
HEAD: a3e75c760c1add35c78750203332874f8635b4b4
TREE: 229cd2ac3e0da848c23f23dd11252de2d48cfdfc
SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
STATUS: PARTIAL / RELEASE_BLOCKED

| CONTROL | EVIDENCE | STATUS |
|---|---|---|
| Attached spec identity | SHA-256 rechecked | PASS |
| Current-build authority boundary | DOC-C-only build obligation + 310b experimental scope contract | STATIC_ALIGNED |
| Static repo scan E2E | 5880630d | STATIC_REPAIRED / NOT_EXECUTED |
| Vault determinism traversal | 6f4920e8 | STATIC_REPAIRED / NOT_EXECUTED |
| Canonical text ordering | ae49beb4 + d60946c3 | STATIC_REPAIRED / NOT_EXECUTED |
| Phase-F release-gate scope | a3e75c76 | STATIC_REPAIRED / NOT_EXECUTED |
| Exact-head tests/build | Actions 37222271602 / 37222271654 / 37222271587 / 37222271599 | BLOCKED_INFRA |
| Clock authority scope | Layer-9 TSA-only vs later G19 invariant TSC | CONFLICT/FREEZE |
| Runtime TSA injection | no production caller proven | NOT_VERIFIED |
| Release/deploy | downstream skipped, no attestation | BLOCKED |
| Whole-project completion | runtime evidence unavailable | NOT_PROVEN |

Authored commits in this execution:
- 5880630d30b227b2a7db92056c7e01127a5e2fcd
- 6f4920e8b34751fd7f13010e38e85eda5afadd7b
- a3e75c760c1add35c78750203332874f8635b4b4

Concurrent commits inspected and preserved:
- 88f0b335a06824aed007470ca42bd7312b115684
- ae49beb4f63d0defd3347a2a59d51ebffac05da2
- 310b799f53f31f62e2e2d0d2583d4a7df5d4e919
- d60946c3a9e34dbc51cf7745bcbf1eba3f2e4212
