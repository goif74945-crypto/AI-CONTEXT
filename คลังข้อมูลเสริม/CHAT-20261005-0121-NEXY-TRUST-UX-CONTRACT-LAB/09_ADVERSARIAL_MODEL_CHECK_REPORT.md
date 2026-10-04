# Adversarial Model Check Report

Status: **PASS for the local proposal checker claims described below**.

## Static proof

Executed:

```text
python -m py_compile \
  conformance/truth_surface_checker.py \
  conformance_tests/test_truth_surface_checker.py \
  tools/exhaustive_conformance_selfcheck.py
```

Observed: success, no syntax error.

Evidence class: E1.

## Unit/negative behavior

Executed:

```text
python -m unittest discover -s conformance_tests -p 'test_*.py' -v
```

Observed:
- 32 tests run;
- 32 passed;
- 0 failed;
- 0 errors.

Evidence class: E2.

## Exhaustive bounded self-check

Executed:

```text
python tools/exhaustive_conformance_selfcheck.py
```

Observed result:

```text
clean_cases = 45
injected_defects = 150
caught = 150
failures = 0
```

The bounded state set covers 9 status/state scenarios across 5 roles. It injects identity, state, result-leak, semantic-copy, STOP mutation, FREEZE result and missing-release-proof defects where applicable.

This is an exhaustive check over the generated bounded matrix, **not** an exhaustive proof over every possible UI or string.

Evidence class: E2 for generated checker behavior.

## Combined executed test count in this session

- Initial exploratory Trust Card compiler: 20/20 PASS.
- Distinct Truth Surface Checker: 32/32 PASS.
- Total unit tests executed: 52/52 PASS.
- Additional generated adversarial defects: 150/150 detected.

Do not interpret those counts as NEXY production coverage.

## Remaining evidence gap

NOT_VERIFIED:
- integration with actual NEXY frontend/backend;
- browser DOM behavior;
- accessibility tree equivalence;
- localization equivalence beyond token rules;
- deployed behavior;
- current NEXY implementation adoption.
