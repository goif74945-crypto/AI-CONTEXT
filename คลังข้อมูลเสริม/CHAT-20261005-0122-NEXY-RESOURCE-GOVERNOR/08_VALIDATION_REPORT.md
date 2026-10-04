# Validation Report — NPRG Reference Lab

Status: PASS for the isolated reference implementation claims listed below.  
Date: 2026-10-05 UTC+7  
Environment: Python 3.13.5 in the current ChatGPT execution container.

## Claim boundary
This report validates only the code/schema/fixtures in this supplemental lab. It does not validate NEXY.AI implementation, real provider metadata, production integration, deployment or real-world model quality.

## E1 — static evidence
Commands executed:

```text
python -m py_compile src/models.py src/governor.py src/serde.py src/__init__.py tests/test_governor.py tests/test_properties.py benchmarks/benchmark_governor.py
python -m json.tool fixtures/scenarios.json
python -m json.tool contracts/resource-governor.schema.json
python - <<PY  # jsonschema Draft202012Validator.check_schema + validate all fixture task/agent payloads
...
PY
```

Observed: PASS. Python sources compiled, both JSON artifacts parsed, the Draft 2020-12 schema passed `check_schema`, all 4 fixture task/agent payloads validated against it using jsonschema 4.26.0, and a negative payload with zero worker input+output tokens was correctly rejected.

## E2 — unit/adversarial evidence
Command executed:

```text
python -m unittest discover -s tests -v
```

Observed: **16 tests PASS / 0 FAIL / 0 ERROR**.

Covered behaviors include:
- lowest-cost selection only among legal plans;
- cost exhaustion freezes instead of downgrading required verification;
- high/critical risk independent-verifier rule;
- data-clearance gating;
- quarantine rejection;
- capability gating;
- evidence-class floor;
- latency and token hard ceilings;
- stable deterministic tie break under input reordering;
- duplicate identity rejection;
- low-evidence verifier-free path under policy;
- self-verification rejection;
- reusable fixture corpus;
- fixed-seed property-style test over **300 generated task/inventory cases**, checking order determinism and selected-plan hard-gate invariants.

## Synthetic scale measurement
Reproducible command:

```text
python benchmarks/benchmark_governor.py --sizes 50 100 250 500 --repeats 5
```

Observed in this environment:

| Workers | Verifiers | Pair space | Median ms | Min ms | Max ms |
|---:|---:|---:|---:|---:|---:|
| 50 | 50 | 2,500 | 4.402 | 4.367 | 4.609 |
| 100 | 100 | 10,000 | 17.575 | 17.278 | 18.669 |
| 250 | 250 | 62,500 | 107.020 | 105.571 | 111.834 |
| 500 | 500 | 250,000 | 423.918 | 419.428 | 435.035 |

This is an environment-specific synthetic measurement, not a production SLA. The reference algorithm remains O(W×V) in time when a verifier is required. It streams the best legal candidate rather than retaining all feasible pairs, keeping feasible-plan storage O(1) beyond inventories and bounded diagnostics.

## Evidence semantics audit
PASS: `PLAN_READY` still returns `verification_status=NOT_VERIFIED`.  
PASS: no unit test treats agent agreement/quality score as E0-E7 proof.  
PASS: hard budget checks occur after verifier requirement is derived, so budget exhaustion cannot suppress a required verifier.  
PASS: high/critical risk cannot use same-provider-domain verification under the reference policy.  
PASS: selected verifier can never be the same agent as the worker.

## Known limitations
- Agent capabilities, prices, quality and latency are trusted inputs in this reference implementation; production provenance/freshness is future work.
- Pair enumeration is exhaustive O(W×V); large production inventories need proven-safe indexing/Pareto pruning before scale claims.
- No E3 integration, E4 E2E, E5 runtime/operational, E6 deployment or E7 physical evidence exists.
- No NEXY.AI-named repository was inspected for implementation or mutated by this lab.
