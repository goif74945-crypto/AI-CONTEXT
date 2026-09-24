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

# Workflow: Build New System

## Required context
- parent ontology entity and entity type;
- scope class and authority;
- requirement IDs or explicit spec extension;
- dependency DAG predecessors;
- trust/state/event/config boundaries;
- definition of proof required.

## Sequence
1. Confirm the system is CURRENT-required; if FUTURE/DEFERRED/EXPERIMENTAL, do not silently promote it.
2. Create/approve ontology entity before code when the object is not already registered.
3. Add or link testable requirements.
4. Define contracts before implementation.
5. Define state ownership/persistence and FSM namespace if stateful.
6. Define atomic invariants and failure behavior.
7. Define security boundary and permissions.
8. Implement in dependency order.
9. Add tests for normal, negative, boundary, failure and recovery behavior.
10. Update implementation map, traceability and evidence only after observed artifacts exist.

## Negative tests
- bypass LAW/JUDGE;
- hidden fallback;
- missing validation;
- stale/ambiguous state;
- unauthorized mutation;
- nondeterministic mutation;
- retry/idempotency duplication;
- missing audit/incident path.

## Rollback
Remove or disable the new implementation without rewriting prior source/history; preserve failure evidence and revert only through legal repository/version path.

## DONE
Not DONE until requirement→code→test→evidence path is explicit and all unresolved blockers are reported.
