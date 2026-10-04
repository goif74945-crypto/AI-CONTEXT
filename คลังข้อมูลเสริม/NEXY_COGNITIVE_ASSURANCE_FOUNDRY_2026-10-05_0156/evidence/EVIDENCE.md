# Verification Evidence

Status: LOCAL_REFERENCE_IMPLEMENTATION_PASS  
Evidence scope: isolated package only, not NEXY integration/deployment.  
Python: Python 3.13.5

## Executed proofs

### E1 — static/syntax
Command:

`python -m compileall -q nexy_caf tests`

Result: PASS (exit code 0).

### E2 — unit / negative-path behavior
Command:

`python -m unittest discover -s tests -v`

Result: PASS — 23 tests, 0 failures, 0 errors.

Coverage focus:
- ILC valid contract / missing authority / protected-scope collision / deterministic ordering.
- CAG safe adoption / missing rollback / undetectable irreversible risk / scenario-order determinism.
- CDL empty debt / release blocker / age amplification / review threshold.
- PHS fresh graph / transitive invalidation / stale lower-class proof / missing upstream / duplicate ID through generator.
- HTBG low-risk execution / unclear-scope freeze / irreversible confirmation / weak-evidence high-impact freeze.
- Suite FREEZE dominance and input-order invariance.

### Cross-engine smoke
All five engines executed with a low-risk advisory scenario and produced PASS decisions. The suite combined them into PASS.

## Defect discovered and repaired during verification
First implementation materialized proof inputs incorrectly for duplicate-ID validation when supplied a one-shot generator. The implementation was changed to materialize the iterable exactly once before ID validation, then a regression test `test_duplicate_proof_ids_rejected_even_from_generator` was added. Full suite was rerun and passed 23/23.

## Not proven
- E3 NEXY integration: NOT_VERIFIED.
- E4 real NEXY user flow: NOT_VERIFIED.
- E5 operational/load/fault behavior: NOT_VERIFIED.
- E6 deployment: NOT_VERIFIED.
- Canonical NEXY adoption: NOT AUTHORIZED / NOT CLAIMED.
