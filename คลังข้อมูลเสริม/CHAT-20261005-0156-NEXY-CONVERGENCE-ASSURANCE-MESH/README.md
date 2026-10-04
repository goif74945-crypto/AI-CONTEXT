# NEXY Convergence Assurance Mesh (CAM)

Status: **REFERENCE IMPLEMENTATION VERIFIED LOCALLY / NEXY INTEGRATION NOT VERIFIED**

CAM is an AI-proposed five-system research pack for making a deterministic control hub more autonomous *without* relaxing zero-guess or evidence rules.

## Five concepts

| ID | System | Core question | Safe outcome |
|---|---|---|---|
| C1 | Interpretation Convergence Gate | Can all admissible meanings lead to one identical legal action? | RELEASE only on convergence, else FREEZE |
| C2 | Context Noninterference Sentinel | Can excluded/untrusted context alter the decision? | PASS only across declared mutation evidence |
| C3 | Evidence Acquisition Planner | What minimum-cost probes satisfy exact evidence obligations? | PLAN or FREEZE if no complete proof plan |
| C4 | Resumption Equivalence Capsule | Will a resumed worker reconstruct the same next legal action? | VERIFIED or FREEZE on critical drift |
| C5 | Independent Evidence Quorum Engine | Are multiple proofs truly independent after ancestry expansion? | PASS only with disjoint producer/failure domains |

## Why the composition matters
A user request can be ambiguous without being decision-relevant. Context can be present without being allowed to influence authority. Verification can be correct but wasteful. A handoff can be syntactically valid while changing what happens next. Two proofs can look independent while sharing one common failure source. CAM treats those as separate failure classes and composes them without claiming authority over NEXY::LAW or NEXY::JUDGE.

## Run

```bash
python3 -m compileall -q .
PYTHONHASHSEED=1 python3 run_all_tests.py
PYTHONHASHSEED=777 python3 run_all_tests.py
```

No third-party Python packages are required.

## Evidence summary
- Static compile: PASS on Python 3.13.5 in the local sandbox.
- Test suite: 34 tests PASS with hash seed 1.
- Regression repeat: same 34 tests PASS with hash seed 777.
- Property checks include exact EAP comparison against brute force for 160 random small instances, 120 ICG permutations, 150 IEQE random pairwise cases, and 100 REC map-order permutations.
- Secret-pattern scan: 0 findings.
- NEXY implementation/runtime/deployment: **NOT VERIFIED and not claimed**.
