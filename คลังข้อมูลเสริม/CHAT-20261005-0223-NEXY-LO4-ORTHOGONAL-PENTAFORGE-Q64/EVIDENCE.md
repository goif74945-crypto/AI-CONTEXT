# Verification Evidence

## Evidence classes

- E0 presence: local artifact files exist.
- E1 static: Python compilation + AST static invariant scan.
- E2 unit/property: executable `unittest` suite.
- E3-local composition: the five modules are instantiated and composed in one snapshot test.
- E4/E5/E6/E7: NOT_VERIFIED and not claimed.

## Failure -> repair -> retest history

### Baseline
The first implemented suite passed 26/26 tests. This was not treated as sufficient because the suite had not yet challenged parser and proof-budget edge cases strongly enough.

### Adversarial strengthening
Two additional negative tests exposed two genuine truth-semantics defects:

1. `Q64.parse(".")` was accepted as zero.
   - Risk: malformed numeric input could become a valid value silently.
   - Fix: reject a bare decimal point as `ValueError`.

2. FPSA could label proof-budget exhaustion as `DEADLINE_MISS` even when the response time had not exceeded the deadline.
   - Risk: stronger failure claim than the evidence justified.
   - Fix: track exact failure reason and emit `ITERATION_LIMIT` unless a deadline miss is actually observed.

The raw failing run is preserved in `evidence/01_adversarial_failure.txt`.

### Repair verification
After both repairs: 28/28 tests PASS with compile/static verification.
Raw output: `evidence/02_final_verification.txt`.

### Property/regression strengthening
Five further property/regression tests were added:
- Q64 integer round-trip grid;
- permutation invariance of SQX;
- monotonic clearance as obstacle distance increases;
- reduced WCET does not worsen the known schedulable set;
- OEWC comparison symmetry under the same contract.

Result: 33/33 tests PASS.
Raw output: `evidence/03_property_verification.txt`.

## Static invariants executed

The suite parses every production Python source file and fails if it finds:
- a Python float literal;
- imports rooted at `random`, `time`, `socket`, `subprocess`, `requests`, `urllib`, `http`, or `os`.

This is evidence about the current source code only. It does not prove arbitrary future adapters have no hidden I/O.

## Claim boundaries

PASS:
- current local Python modules compile;
- current test suite behavior passes;
- Q64 raw result range enforcement is tested;
- selected negative paths are tested;
- current source passes the defined no-float-literal/no-banned-import static rule;
- local cross-module composition passes.

NOT_VERIFIED:
- integration with the real NEXY.AI codebase;
- production performance;
- exhaustive finite-state reduction correctness for arbitrary domain semantics;
- causal correctness of externally supplied causal traces;
- real robot safety;
- real OS/RTOS schedulability;
- universal behavioral equivalence;
- deployment/release readiness.

## Final pre-publication regression

After the property suite was locked, the verifier was executed again and then the complete 33-test suite was run in 20 fresh subprocess executions.

- final pre-publication verification: 33/33 PASS; raw output `evidence/04_final_prepublication_verification.txt`;
- repeated regressions: RUN_01 through RUN_20 PASS;
- `python3 -m compileall -q src tests`: PASS;
- raw repeat log: `evidence/05_regression_repeat.txt`;
- artifact SHA-256 list: `evidence/MANIFEST.sha256`.

Repeated local PASS strengthens reproducibility evidence but does not upgrade these results into production/runtime/deployment evidence.
