# Verification Evidence

## Environment
- Python: 3.13.5
- pytest: 9.0.2
- execution location: isolated local sandbox copy before persistence to AI-CONTEXT
- network requirement: none
- target under test: standalone MVK package only

## Failure-repair evidence
### Initial run
- Result: **FAIL**
- Observed: 14 failed / 11 passed.
- Root cause: `dataclasses.asdict()` attempted to deepcopy `MappingProxyType`, causing `TypeError: cannot pickle 'mappingproxy' object`.
- Captured initial failure summary: `evidence/pytest-initial.txt`.

### Repair
- Replaced dataclass `asdict()` conversion with direct dataclass field enumeration and recursive canonicalization.
- Preserved mapping immutability rather than weakening the model.
- Added hash-domain separation: `nexy-mvk-canonical-v1\0`.
- Added structured `ERROR` result for uncanonicalizable seed cases.

## Final E1/E2 evidence
Command:

```text
PYTHONPATH=src pytest --cov=nexy_mvk --cov-report=term-missing -q
```

Observed:
- 38 tests passed.
- total line coverage: 97% (324 statements, 9 missed).
- `engine.py`: 100%.
- `model.py`: 100%.
- `report.py`: 100%.
- raw report: `evidence/coverage-final.txt`.

Static compilation:

```text
python -m compileall -q src tests examples
```

Observed: PASS, recorded in `evidence/compileall-final.txt`.

## Local package/entrypoint evidence
Editable install with no dependency/network requirement succeeded using:

```text
python -m pip install --no-build-isolation --no-deps -e .
```

Console entrypoint:

```text
nexy-mvk validate-fixture examples/fixture.json
```

Observed: PASS with deterministic 64-hex case and observation hashes.

## Local multi-component harness
Command:

```text
python examples/integration_harness.py
```

Observed: 4 relations, 4 PASS, 0 FAIL, 0 ERROR.
Relations:
- deterministic replay;
- irrelevant context invariance;
- permission reduction monotonicity;
- evidence removal safety.

Raw output: `evidence/integration-harness-hardening.json`.

## Negative control
Command:

```text
python examples/negative_control.py
```

The adapter intentionally changes output on replay. Observed result:

```text
FAIL: semantic projection changed under an invariance relation
```

This confirms the harness is capable of rejecting drift rather than only producing PASS.

## Evidence boundary
- Standalone implementation: **PASS** for required E1/E2 and local component integration evidence.
- Actual NEXY.AI integration: **NOT_VERIFIED**.
- NEXY runtime/deployment: **NOT_VERIFIED**.
- No claim is made that this project is already part of NEXY.AI.
