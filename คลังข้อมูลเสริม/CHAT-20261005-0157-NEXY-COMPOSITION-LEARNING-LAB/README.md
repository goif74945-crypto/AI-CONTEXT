# NEXY Composition & Learning Auxiliary Lab

Five AI-proposed mechanisms for problems that appear *after* individual components can already be verified.

| ID | System | Core question | Output |
|---|---|---|---|
| C1 | Contract Composition Kernel | Can independently specified components legally compose? | PASS/FREEZE + admitted waves/facts |
| C2 | Emergent Capability Risk Analyzer | Does a safe-looking tool chain create a hazardous capability/dataflow? | PASS/FREEZE + taint trace/findings |
| C3 | Evidence Portability Compiler | Can proof from context A carry to context B without overclaiming? | PORTABLE/REVERIFY/INVALID/FREEZE |
| C4 | Correction-to-Constraint Compiler | Can a verified correction become a narrowly scoped regression contract? | deterministic correction contracts + evaluation |
| C5 | Failure Delta Distiller | What is the 1-minimal reproducer for a stable failure signature? | minimized subsequence + proof of 1-minimality |

## Why this is useful to NEXY
NEXY's existing design already emphasizes deterministic control, evidence, freeze semantics, provider-independent workers, and release gates. These prototypes target second-order failure boundaries:

- correctness can fail when individually valid components are composed;
- capability risk can emerge only across a multi-tool chain;
- old evidence can be accidentally reused in a materially different environment;
- user corrections can be generalized too broadly and become new bugs;
- large failing plans are expensive to understand and regression-test.

## Runtime
- Python 3.11+
- Standard library only at runtime
- No network access
- No provider/model call
- No NEXY.AI import

## Verification command

```text
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src tests
```

Exact executed results are recorded in `VERIFICATION_REPORT.md`; this README does not substitute for runtime evidence.
