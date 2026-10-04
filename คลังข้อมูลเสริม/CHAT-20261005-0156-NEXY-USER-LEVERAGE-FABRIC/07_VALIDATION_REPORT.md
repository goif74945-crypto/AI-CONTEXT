# Validation Report

## Environment

- execution environment: isolated local container without GitHub network resolution;
- Python: `3.13.5`;
- pytest: `9.0.2`;
- runtime dependency model: Python standard library only;
- test dependency: pytest.

## Validation sequence

### E1 — static compilation

Command:

```bash
PYTHONPATH=src python -m compileall -q src tests
```

Observed result: `PASS` with no emitted compilation errors.

### E2 — unit / negative / determinism tests

Command:

```bash
PYTHONPATH=src pytest -q
```

Observed final result:

```text
...............................                                          [100%]
31 passed in 0.05s
```

The suite covers positive behavior plus negative paths including:
- orphan work;
- forbidden scope;
- dependency cycles;
- unknown acceptance criteria;
- unavailable/disallowed capabilities;
- cost budget failure;
- artifact hash mismatch;
- forbidden artifact classification;
- missing/empty metadata / oversize package;
- unpinned dependency;
- permission/network policy violations;
- invalid dependency digest/source;
- unknown mastery goal;
- prerequisite cycle;
- mastery step-budget overflow;
- input-order permutation stability across all five engines.

### Local package integration demo

Command:

```bash
PYTHONPATH=src python -m nulf.demo
```

Observed summary:

```text
artifact_consumer_fitness_gate PASS []
goal_contribution_graph PASS []
mastery_path_compiler PASS []
supply_chain_trust_gate PASS []
verified_capability_composer PASS []
```

This is package integration evidence only. It is **not** NEXY.AI integration evidence.

### Deterministic replay

Two independent demo invocations were compared byte-for-byte with `cmp`.

Both outputs SHA-256:

`83560e83819e37695f043d831e5186feb4a0b44abdd235af3f4c4ec85d9dc35c`

Result: PASS.

## Defect discovered and repaired during verification

Initial implementation canonicalized most result fields but fingerprints for capability, supply-chain and mastery engines still included input tuples in caller-provided order. That meant semantically identical permutations could produce different fingerprints.

Correction:
- sort capability manifests by capability ID before fingerprinting;
- sort dependencies by name before fingerprinting;
- sort mastery nodes by skill ID before fingerprinting;
- add permutation tests for all five engines.

Re-verification after correction: `31 passed`.

## Evidence limitations

- No production runtime was exercised.
- No NEXY.AI code was integrated or modified.
- No browser/E2E product flow was run.
- No external vulnerability feed or package signature service was queried.
- No real user study was run.
- Therefore NEXY integration, deployment and product-value claims remain `NOT_VERIFIED`.
