# Verification Plan

- E1: compile all Python sources/tests; AST scan for float literals.
- E2: unit tests for Q64 core + five systems; negative/freeze paths; seeded properties.
- E3: isolated integration pipeline.

Required negative paths include mutating prefetch rejection, impossible SLO freeze, unknown/cyclic proof dependency freeze, pinned-context budget freeze, mandatory notice surfacing, Q64 divide-by-zero and overflow.

Repro:
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests
```
