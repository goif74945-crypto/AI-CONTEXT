# NEXY Metamorphic Verification Kernel (MVK)

**Status:** standalone reference implementation and verification lab.

**Important:** this project is stored in `AI-CONTEXT` only. It does not modify, patch, import from, or claim runtime proof for the separate NEXY.AI implementation repository.

## Problem
AI/control systems can be difficult to test with a single exact expected output. Metamorphic testing verifies relationships between executions instead. If an input is changed in a way whose semantic effect is known, the output must obey a corresponding invariant.

## High-value relations included
- deterministic replay;
- irrelevant-context noninterference;
- externally asserted semantic-variant invariance;
- permission-reduction monotonicity;
- evidence-removal safety monotonicity.

## Integration model
NEXY.AI or any compatible system supplies a callable adapter:

```python
from nexy_mvk import Case, Observation

def adapter(case: Case) -> Observation:
    ...
```

The kernel owns relation execution, canonical hashing, fail-closed error classification, and structured verification reports. The target system remains the authority for actual execution semantics.

## Verification boundary
Passing this lab's unit tests proves this standalone implementation at E1/E2 classes only. It does **not** prove NEXY.AI integration, runtime behavior, deployment behavior, or production safety. Those require separate E3-E6 evidence against an exact NEXY revision/environment.
