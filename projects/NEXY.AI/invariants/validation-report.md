# Invariant Registry Validation

## Result
**PASS**

- invariants: **40**
- invalid entity refs: **0**
- S5 invariants: **39**
- S4 invariants: **1**

## Semantics
These records are **change-preservation obligations**, not implementation PASS claims.

Before modifying a mapped system, a builder should:
1. resolve invariants whose `system_ids` intersect the change;
2. include their verification obligations in regression scope;
3. preserve domain distinctions;
4. freeze/stop if an S5 invariant cannot be proven preserved.

## Domain distinctions retained
- Core overflow FREEZE vs Game numeric saturation/clamping are not merged.
- final one-output vs internal Top-K candidates are not merged.
- runtime/system memory classes are not equated with uncontrolled model memory.
- physical safety invariants require physical/HIL proof.
