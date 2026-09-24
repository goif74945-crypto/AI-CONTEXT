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

# Workflow: Add Storage Model

## Required context
- authoritative state owner;
- writer/readers;
- persistence tier;
- lifetime/retention;
- version/migration policy;
- immutability/OCC/idempotency;
- audit/recovery obligations.

## Sequence
1. Add state-ownership entry before schema mutation.
2. Verify dependency tier legality (e.g. no forbidden JUDGE→CORE/VAULT authority).
3. Define keys, relationships, deletion behavior and version semantics.
4. Define immutable vs mutable fields.
5. Define migration and rollback.
6. Define transaction boundary and failure behavior.
7. Implement schema/repository layer.
8. Add migration roundtrip, concurrency, failure-injection and restore/replay tests.
9. Update persistence map and traceability.

## Negative tests
- stale OCC write;
- duplicate idempotency;
- orphan lineage;
- forbidden delete/update;
- transaction partial failure;
- missing blob/content hash;
- rollback failure.

## DONE
State owner, schema, migration, recovery and audit path are explicit and tested.
