# Evidence Summary

## Environment
- Isolated container/sandbox
- Python observed via runtime as 3.13-compatible execution environment
- No external network dependency required by prototypes
- No NEXY.AI source mutation

## Static evidence (E1)
Command:
```bash
python3 -m compileall -q .
```
Observed result: exit 0.

## Unit / negative-path evidence (E2)
Command:
```bash
python3 run_all_tests.py
```
Observed result:
- RUC: 4/4 PASS
- AEP: 4/4 PASS
- SNCG: 4/4 PASS
- TICM: 4/4 PASS
- RDRC: 4/4 PASS
- FINAL: PASS

## Stress / determinism evidence
Command:
```bash
python3 stress_checks.py
```
Observed after fixing a Python 3.13 dynamic-import harness issue:
- `check_ruc`: PASS, 200 seeded randomized cases; rechecked irreducible-core property
- `check_aep`: PASS, 100 ordering permutations
- `check_sncg`: PASS, 2,000 clean symbols + one injected collision
- `check_ticm`: PASS, 10,000 trace records + repeat-output equality
- `check_rdrc`: PASS, 2,000 deltas + repeat-output equality
- FINAL: PASS

## Failure found and corrected
First stress-harness attempt failed before engine execution because dynamically imported dataclass modules were not registered in `sys.modules` before `exec_module` under the sandbox's Python 3.13 behavior. The harness was corrected by inserting `sys.modules[name] = mod` before module execution. Unit suites were rerun unchanged and still passed, then stress checks passed.

## Evidence limitations
- No NEXY.AI integration test.
- No production load/SLA claim.
- No CI/CD evidence yet at local-artifact stage.
- No deployment evidence.
- Novelty is repository-search-based, not a formal semantic uniqueness proof.
