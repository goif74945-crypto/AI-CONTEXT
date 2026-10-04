# Failure / Fix / Re-verify Log

## Hardening finding 1 — replay poisoning risk
Initial code created shallow `dict()` copies for replay request/state. Nested mutable values could be shared with the original capsule, allowing an executor to mutate later replay input.

Correction:
- deep canonicalize request/state on each replay;
- add a test where a mutating executor appends to a nested list;
- assert the later executor still observes the original list and the original capsule remains unchanged.

Re-verification: full suite PASS, 27/27.

## Hardening finding 2 — cyclic proof dependency
Initial EDEL dependency validation rejected unknown nodes but did not reject cycles. Cycles can obscure proof-root authority and create ambiguous evidence repair semantics.

Correction:
- deterministic DFS cycle detection added before debt analysis;
- explicit `DEPENDENCY_CYCLE` structural failure;
- negative test added.

Re-verification: full suite PASS, 27/27; stress PASS 40,000 checks.

These were design-review findings discovered before publication, not production incidents.
