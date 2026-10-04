# Verification Evidence

Status: isolated prototype evidence only. NEXY.AI runtime integration remains `NOT_VERIFIED`.

## Environment
- Local execution sandbox
- Python: `3.13.5`
- External package dependencies: none
- Network/provider dependency during tests: none

## E1 — static compilation
Command:

```bash
PYTHONPATH=src python -m compileall -q src tests
```

Observed: `PASS`.

## E2 — unit/adversarial tests
Command:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Final observed result:
- tests run: `50`
- failures: `0`
- errors: `0`
- result: `OK`

Coverage focus includes:
- forged authority root and forged promotion receipt rejection;
- authority cycle rejection and deterministic sealing;
- disconnected uncertainty containment;
- cycle/missing/duplicate dependency rejection;
- minimum-cost proof planning, evidence-class preservation and deterministic tie-break;
- exact-planning bounds and safe dominance pruning;
- requirement positive/negative/missing witnesses;
- contradiction detection and malformed/non-finite input rejection;
- untrusted authority digest rejection;
- failed/unknown/cross-claim/stale-version evidence rejection;
- deterministic output digest;
- seeded permutation determinism.

## E3 — isolated integration
`tests/test_integration.py` composes all five modules.

Reference command:

```bash
PYTHONPATH=src python run_reference.py
```

Observed final output:

```text
authority_digest=36e26b6928893c6511f3750d19b977469b7c201824c08383714a1839a60ff46d
proof_probe_ids=unit-check
witness_kinds=positive,negative,missing
compile_status=PASS
compile_digest=91ca5b1b7633caddd7af880c647c47107906961016f1c05174584fe5f28128d2
```

## Optimization evidence
A deterministic benchmark workload with 12 claims, 120 probes, 100 repeated exact plans was used during development.

Before safe dominance pruning / DP tuple optimization:
- observed average: about `73.064 ms/plan`.

After optimization:
- observed average: about `12.431 ms/plan`.
- selected probes remained: `mix-012,mix-025,mix-039,mix-076`.
- total cost remained: `11`.

This benchmark is environment-specific and is not a production latency guarantee.

## Evidence class boundary
- E0: artifacts present locally and later in AI-CONTEXT after publication/readback.
- E1: Python compilation.
- E2: 50 executed unit/adversarial tests.
- E3: isolated package integration test/reference flow.
- E4/E5/E6: not claimed.
- NEXY.AI live/runtime/deployment integration: `NOT_VERIFIED`.
