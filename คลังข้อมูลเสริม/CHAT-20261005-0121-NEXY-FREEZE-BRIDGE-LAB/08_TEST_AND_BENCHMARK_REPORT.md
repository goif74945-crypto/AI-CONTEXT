> **HISTORICAL / SUPERSEDED v1.0**
>
> This file records the initial design before the concurrent `NEXY Trust UX Contract Lab` was discovered. Its UI/action-oriented portions are **not current**. The current Freeze Bridge contract is v1.1 and is defined by `README.md`, `10_V1_1_PIVOT_AND_SIBLING_BOUNDARY.md`, and `11_PROTOCOL_V1_1.md`. Historical text is retained for provenance only.

# Test and Benchmark Report

Classification: **EXECUTED LOCAL EVIDENCE FOR THIS REFERENCE IMPLEMENTATION ONLY**

## Environment boundary

Executed in the current isolated tool/container environment during session:
`NEXY-FREEZE-BRIDGE-20261005-0121-ICT`

This does not prove behavior in NEXY production/runtime/deployment.

## Failure history

Initial test run:
- total: 15
- passed: 14
- failed: 1

Root cause:
- defective test assertion searched for substring `script`;
- serialized JSON legitimately contained key `description`;
- the engine had not reflected the malicious `<script>alert(1)</script>` context label.

Correction:
- assertion changed to test actual payload markers `<script>` and `alert(1)`.

Re-run:
- 15/15 PASS.

## Expanded negative-path suite

Additional validation tests were added for:
- non-object input;
- required text type/empty/length paths;
- optional context label type/empty/control-char/length paths;
- null/list/size/item-length list paths;
- enum invalid/non-string paths;
- retryable type validation;
- authorized-action collection type/size/dedup paths.

Final unit/negative suite:
- **21/21 PASS**

## Coverage

Command shape:
```bash
PYTHONPATH=. python -m coverage run --branch -m unittest discover -s tests -v
python -m coverage report -m
```

Observed production library coverage:
- `freeze_bridge/__init__.py`: 100%
- `freeze_bridge/compiler.py`: 100%
- `freeze_bridge/model.py`: 100%
- `freeze_bridge/policy.py`: 100%

Combined report including tests:
- 99% because the `if __name__ == "__main__": unittest.main()` line in the test module is not executed by discovery.

Interpretation:
**production reference library reached 100% line + branch coverage in this run.**

## Static/syntax proof

```bash
python -m compileall -q freeze_bridge tests
```

Observed: **PASS**

## CLI round-trip

Executed:
- sample Thai fixture through `python -m freeze_bridge ... --compact`;
- output parsed through `python -m json.tool`.

Observed: **PASS**

Example output properties:
- reason = MISSING_REQUIRED_INPUT;
- Thai title/summary;
- needed fields sorted;
- unauthorized CONTACT_OPERATOR not emitted;
- deterministic fingerprint present.

## Policy matrix self-check

Dimensions:
- 11 reasons;
- 2 locales;
- 3 disclosures;
- 5 statuses.

Total generated cases:
**330**

Checks per case:
- repeat determinism;
- action subset invariant;
- restricted security evidence suppression;
- restricted security non-retryability;
- unknown-reason non-retryability.

Observed:
`PASS policy_matrix_cases=330`

## Microbenchmark

Command:
```bash
PYTHONPATH=. python tools/benchmark.py --iterations 50000
```

Observed:
- iterations: 50,000
- elapsed_seconds: 1.735162
- rate: 28,815.76 ops/s
- stable sample fingerprint emitted

Interpretation:
This is a local microbenchmark of the Python reference engine only. It is **not** a production SLA, not an E5 load test, and not evidence about a future integrated service.

## Evidence status

- E0 presence in local sandbox: PASS
- E1 syntax/static/coverage instrumentation: PASS
- E2 unit/negative behavior: PASS
- E3 integration with NEXY: NOT_VERIFIED
- E4 real user flow: NOT_VERIFIED
- E5 target runtime/fault/load: NOT_VERIFIED
- E6 deployment: NOT_VERIFIED
- E7 physical: not applicable
