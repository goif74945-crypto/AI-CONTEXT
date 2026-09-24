# Semantic Diff + Change Impact Validation

## Result
**PASS — derived impact index**

- entity impact records: **518**
- each record includes direct prerequisites/dependents;
- transitive REQUIRES dependents derived from acyclic dependency DAG;
- requirement/contract/invariant/failure/test/evidence links attached where available;
- implementation paths retain blob SHA.

## Rule
This index is predictive context, not proof that every dependent actually breaks.

AI must use it to determine **what must be inspected/regressed**, not to invent a FAIL.

## Semantic Diff
The semantic diff spec covers behavior, contracts, authority, invariants, FSM, persistence, security, determinism, errors, observability, performance, scope and evidence freshness.
