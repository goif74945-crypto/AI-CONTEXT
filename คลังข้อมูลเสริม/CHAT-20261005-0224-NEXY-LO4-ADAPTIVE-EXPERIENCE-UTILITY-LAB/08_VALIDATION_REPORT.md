# Validation Report

**Work code:** `CHAT-20261005-0224-NEXY-LO4-ADAPTIVE-EXPERIENCE-UTILITY-LAB`  
**Final research identity:** NEXY Lo4 Innovation Capital Fabric  
**Classification:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_GOVERNING / NOT_CANON`  
**Environment:** Python 3.13.5, isolated Linux container  
**Standalone status before repository publication:** PASS

## Evidence matrix

| Gate | Class | Command | Observed | Status |
|---|---|---|---|---|
| Syntax/import compilation | E1 | `python3 -m compileall -f -q aeul tests` | exit 0 | PASS |
| Full suite seed 1 | E2/E3-lab | `PYTHONHASHSEED=1 python3 -m unittest discover -v tests` | 53 tests, OK | PASS |
| Full suite seed 777 | E2/E3-lab | `PYTHONHASHSEED=777 python3 -m unittest discover -v tests` | 53 tests, OK | PASS |
| Replay comparison | E2 support | normalize timing, byte compare reports | identical | PASS |
| Deterministic stress | E2 | `PYTHONPATH=. python3 tests/stress.py` | 10,000 IURS + 3,000 DCPX cases PASS | PASS |
| Binary-float exclusion | E1/E2 | AST adversarial test | no float literals / `float()` in decision modules | PASS |
| Q64 differential arithmetic | E2 | Fraction-backed randomized tests | multiply/divide exact half-even oracle matches | PASS |
| NEXY runtime integration | E3 target | not executed by design | NOT RUN | NOT_VERIFIED |
| Product E2E | E4 | not in scope | NOT RUN | NOT_VERIFIED |
| Deployment | E6 | not in scope | NOT RUN | NOT_VERIFIED |

## Final test inventory
- Q64.64 core + boundary tests.
- IURS selection/protected-minimum/determinism tests.
- COMET missing/conflicting/high-overlap/determinism tests.
- SCTE total/single-surface/duplicate/order tests.
- DCPX budgets/dependencies/conflicts/overlap/diversity/reference-limit/order tests.
- RIVP risk/blast/rollback/sample/holdout/option-value tests.
- Cross-system integration tests.
- Adversarial randomized Q64 differential tests.
- **Total unittest cases: 53.**

## Stress inventory
Fixed seed `202610050224`:
- IURS: 10,000 generated cases, 10,000 selected outcomes completed without assertion failure.
- DCPX: 3,000 generated six-candidate portfolio cases, 3,000 selected outcomes completed without assertion failure.

## Failure -> repair -> re-verification
1. Early pre-pivot Q64 test oracle compared a multi-step `0.1` arithmetic result to a separately parsed decimal. The raw values differed by 2 because Q64.64 rounds at defined operation boundaries. The test oracle was corrected; engine arithmetic was not weakened.
2. Final SCTE test repeated the same oracle mistake at 1 raw-unit difference. It was corrected to calculate the expected value through the defined Q64.64 operation sequence. Full 53-test suite then passed.
3. First stress invocation `python3 tests/stress.py` failed with `ModuleNotFoundError: aeul` because direct script execution changed import-root semantics. Runtime contract corrected to `PYTHONPATH=. python3 tests/stress.py`; no engine code change was required. The corrected stress run passed.

## Evidence files
- `evidence_final/environment.txt`
- `evidence_final/compileall.txt`
- `evidence_final/unittest-seed1.txt`
- `evidence_final/unittest-seed777.txt`
- `evidence_final/replay-compare.txt`
- `evidence_final/stress-initial-failure.txt`
- `evidence_final/stress.txt`
- `evidence_final/local-file-hashes.txt`

## Truth boundary
The results prove only the isolated reference implementation on the tested local bytes. Publication readback/blob-equivalence is a separate final gate. No result here proves that NEXY.AI currently implements or has adopted ICF.
