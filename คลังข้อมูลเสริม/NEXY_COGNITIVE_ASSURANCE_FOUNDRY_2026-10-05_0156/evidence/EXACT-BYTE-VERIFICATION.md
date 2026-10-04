# Exact-Byte Verification Record

## Tested code revision
Branch: `caf-20261005-0156`
Code/test head before evidence-only commits: `127946a569c11cbb5d10eff3daaff0b292345d89`

The local files used for the final compile/test run were compared using Git's blob identity formula:

`SHA1("blob " + byte_length + NUL + exact_bytes)`

All 9 code/test files matched the blob SHA reported by GitHub for the branch.

| File | Git blob SHA-1 | Bytes | Match |
|---|---|---:|---|
| nexy_caf/__init__.py | 78ae27c3379e6568e11669e55fc0ea40afec65ff | 587 | PASS |
| nexy_caf/cognitive_debt.py | 8c036ca946737b79fa2ae4faf1eecc7101e2708d | 3673 | PASS |
| nexy_caf/contracts.py | c1a9c264e255881270b827f60b79e576edd594e5 | 2186 | PASS |
| nexy_caf/counterfactual_gate.py | b37eedb6ac1f7e8cd9259fe4127eb415560d1dc6 | 3849 | PASS |
| nexy_caf/intent_lattice.py | 2b15fc8a77ad22a27054cfa5782896ca9d297d3b | 4105 | PASS |
| nexy_caf/proof_horizon.py | 7e3fda94cdf1166230d278bd7eb455dca1fa8da5 | 3874 | PASS |
| nexy_caf/suite.py | 4ef4ee528248e7a099544adf5206ea6d202302e2 | 1078 | PASS |
| nexy_caf/trust_budget.py | f93485e6264b910afa0729c7ed8776c1f743b741 | 2866 | PASS |
| tests/test_foundry.py | 96184b212b8b852df178d94f0729b7649a664338 | 9291 | PASS |

## Executed against those exact bytes
- `python -m compileall -q nexy_caf tests` => PASS.
- `python -m unittest discover -s tests -v` => PASS, 23/23, 0 failures, 0 errors.
- Cross-engine smoke => PASS; all five advisory engines returned PASS for the low-risk smoke case and suite composition returned PASS.

This proves E1/E2 behavior for the isolated reference implementation only. It does not prove NEXY integration or deployment.
