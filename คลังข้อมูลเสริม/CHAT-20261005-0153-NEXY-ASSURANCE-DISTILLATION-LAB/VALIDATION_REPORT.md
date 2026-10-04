# Validation Report

## Scope proven
Standalone AI-proposed reference implementation only. No claim of live NEXY integration or deployment.

## Executed evidence

### E1 — Static
- \`python3 -m compileall -q src tests\`: PASS for the modular project.
- publish-layout source/test candidate was also syntax-checked during packaging.

### E2 — Full modular suite
- 24/24 tests PASS.
- raw log: \`evidence/unit-tests-24.txt\`.

Coverage includes:
- canonical JSON and JSON Pointer semantics;
- counterexample baseline/failure preservation and nested protected paths;
- deterministic replay;
- constraint feasibility/minimal unsat core/bounds;
- freshness TTL/version/future timestamp/dependency cycle;
- spec-example contradiction detection;
- safe recovery path/evidence blocking/step bounds;
- CLI malformed-input freeze and unsat-core invocation.

### E2/E3-ish standalone publish-layout conformance
- 21/21 tests PASS against the exact module layout being published.
- includes two subprocess CLI flows via \`python -m nexy_aqt.cli\`.
- raw log: \`evidence/published-package-tests-21.txt\`.

This is standalone package/CLI integration evidence, not NEXY integration evidence.

## Failure/repair history
1. Initial modular implementation reached 19 passing tests.
2. New protected-path adversarial test exposed a sentinel/deep-copy bug.
3. Root cause fixed before publication; regression reached 21/21.
4. Resource/temporal negative tests were added; final modular suite reached 24/24.
5. A first single-file publication harness failed 4/21 because the new harness misread timestamp/example contracts. The implementation was not weakened to satisfy the bad harness.
6. Harness was corrected from the actual contracts and reached 21/21.
7. Git publication attempt through repeated Contents API commits hit a 409 because other chats moved main concurrently. No force update was used; publication switched to an atomic Git-tree strategy.
8. Source blob identities were compared to local tested file Git hashes. One \`freshness.py\` blob differed only by an omitted comment; it was discarded and regenerated until the blob SHA matched exact local bytes.

## Exact tested blob identities
- __init__.py: 9afa1257cc34d411ab275242e6afa4d29f14645f
- common.py: 35030a5f79f1999590b38d63febb823678545233
- predicates.py: 0f5843373e96caec6cfafef617e97f25796f44c7
- counterexample.py: 20b7a7a00550bc457f66769afe601e39b1035593
- unsat_core.py: 861e1d851f60f6a036e2f95425cbc6953659e40b
- freshness.py: e9d5b5cd55119723389d2f89e85097ab0b4e5cfc
- example_linter.py: 2ef9ea0b49793093aa4b481c72b0ffc8e1dcc62e
- recovery.py: e14dfea5bbdfdbf7f5590865162ec227c14f32c8
- cli.py: 8e4f18fb38fde7b9cfb1416126039387145960fc
- test_published_package.py: 056df65114570643232783ad01db7c52e67e1024
- pyproject.toml: d703c439fd58b7309018993e43f8464da9099846
- unit-tests-24.txt: df520ba7a5bb46e3c9a4cbeb1d577cc55977ec9e
- published-package-tests-21.txt: 6f01bb8d764507b39b4fbf700eb85bd22e4e436a

## Status boundary
- Design: PASS for this proposal.
- Standalone implementation: PASS at E1/E2 plus standalone CLI checks.
- NEXY integration: NOT_VERIFIED.
- Runtime/deployment/production safety: NOT_VERIFIED.
