# NEXY Builder Playbook

## Universal preconditions
1. Pin repository + branch + exact HEAD.
2. Abort/freeze if the requested target branch/HEAD differs from task authority.
3. Resolve target entity in `ontology/entities.jsonl`.
4. Resolve governing requirements in `requirements/requirements.jsonl`.
5. Resolve authority/scope/supersession/conflicts before implementation.
6. Resolve `REQUIRES` predecessors from `graphs/dependency-graph.json`.
7. Resolve code only through `implementation/system-to-code.jsonl`; CANDIDATE refs must be opened before use.
8. Load linked contracts, FSM namespace, atomic invariants, trust boundaries, state ownership, events and config.
9. Check `failures/failures.jsonl` for known failure classes.
10. Never interpret file presence, build success, or prose as runtime/evidence PASS.

# Workflow: Modify Existing System

## Required context
- exact target entity;
- all dependents from Ontology/Dependency Graph;
- linked atomic invariants;
- contracts/FSM/state ownership;
- historical failures and supersession records.

## Sequence
1. Calculate impact set: target + dependents + linked requirements + contracts + invariants + tests.
2. Read every EXACT mapping and all relevant GROUP/CANDIDATE files before edit.
3. Record intended semantic change: behavior, contract, authority, state or implementation-only.
4. If behavior/contract/authority changes, update source/governance first; do not hide semantic change inside code.
5. Apply smallest dependency-safe patch.
6. Re-run required negative/regression tests.
7. Compare semantic before/after, not only git diff.
8. Refresh implementation map/snapshot/traceability.

## Stop conditions
- unresolved authority conflict;
- stale HEAD;
- invariant impact cannot be bounded;
- migration/rollback unspecified for persisted state;
- source and requested behavior disagree without explicit supersession.

## DONE
No unresolved invariant/contract/FSM regression attributable to the patch; evidence class stated honestly.
