# NEIK Verification Evidence

Status: PASS for the standalone reference implementation claims below.
No NEXY.AI runtime, deployment, or production-integration claim is made.

## Exact code identities
Local source SHA-256 before Git object creation:
292c81b7567ac1b69a373c9664f65bd0f1d2fd0ed8a25bce57bbd2b583d47993  src/neik.py

Git blob identity after upload:
3ba7ac900936af6c66f5cb1a6d21516c39e55074  src/neik.py

Local test SHA-256 before Git object creation:
cd104e812d1108d617a1959036b85a6d9ba1c9d3af04e6295fdcb5fd15e3677d  tests/test_neik.py

Git blob identity after upload:
16f104d0014dafb842301de71051da23ecf88efd  tests/test_neik.py

The returned Git blob identities exactly matched locally computed git hash-object identities before branch mutation.

## E1 static evidence
- python -m compileall -q src tests -> PASS
- input schema JSON parsed successfully -> PASS
- AST import audit of src/neik.py found only Python standard-library modules:
  __future__, argparse, dataclasses, enum, hashlib, json, pathlib, sys, typing
- no clock/random/network library is imported by the core

## E2 executed behavior evidence
Command:
PYTHONPATH=src python -m unittest discover -s tests -v

Observed:
24 tests executed
24 passed
0 failed
0 errors

Test surface includes:
- independent quorum PASS
- shared source NOT_VERIFIED
- source/producer/oracle correlation
- derived-lineage inheritance
- dependency cycle FREEZE
- stale target exclusion
- evidence-class gate
- blind-policy gate
- self-verification gate
- missing configured lineage
- duplicate artifact correlation
- PASS/FAIL contradiction FREEZE
- exact non-greedy witness selection
- order-invariant deterministic decision
- deterministic solver-budget FREEZE
- strict unknown field/dependency and duplicate-lineage rejection
- producer identity lineage invariant
- CLI exit semantics
- exhaustive exact-solver comparison against brute force for every simple graph topology through 5 vertices

## Deterministic replay
A valid three-confirmation input was executed through the CLI in 25 separate subprocesses.
Result: 25/25 stdout byte sequences identical.
stdout SHA-256:
816fa91d511f35ad5e73a8da6700b68e5679cecbeabd0b5998156918a5660868
decision_sha256:
b0455dcbc21527ebb7107a83e65f7837c7c13ca6f1072590b3072c7d92bfa36e
decision: PASS

## Bounded solver stress
Configured max_solver_states = 1,000,000.
16 nodes -> witness 3, states 297
24 nodes -> witness 3, states 759
32 nodes -> witness 3, states 1,593
48 nodes -> witness 3, states 4,809
64 nodes -> witness 3, states 10,515
All completed under budget without approximation.

## Failure/recovery record
Design re-audit found two genuine missing protections after the first passing suite:
- empty configured lineage could be counted as independent;
- exact solver had no explicit deterministic state budget.

Both were repaired and tests expanded. A fixture regression caused by the stronger producer-lineage contract was then fixed without weakening the invariant.

Two final ad-hoc validation harness mistakes were also exposed and corrected:
- schema was typed instead of schema_version in a hand-authored replay payload;
- a stress script read a non-existent nested result key.
The product test suite remained green; the corrected replay/stress runs produced the results above.

## Proven / not proven
PASS:
- exact tested standalone semantics;
- strict parser behavior covered by tests;
- exact solver correctness over the exhaustive checked graph domain;
- tested deterministic replay;
- tested bounded-search behavior.

NOT VERIFIED / OUT OF SCOPE:
- production performance;
- NEXY.AI integration;
- deployment;
- authenticity of lineage metadata;
- truth of the underlying claim;
- cryptographic producer/oracle/source attestation.