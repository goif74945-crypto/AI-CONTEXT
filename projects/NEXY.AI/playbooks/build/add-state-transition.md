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

# Workflow: Add State Transition

## Required context
- exact FSM namespace;
- FROM/EVENT/GUARD/ACTION/TO;
- event owner;
- invalid-transition behavior;
- incident/audit semantics;
- all same-named states in other FSMs to avoid conflation.

## Sequence
1. Identify the FSM by ID + namespace; never use state name alone.
2. Confirm transition is source-authorized. If absent, require source/governance change first.
3. Define event owner and guard.
4. Define action side effects and persistence transaction.
5. Define failure/timeout behavior.
6. Define audit event and incident linkage.
7. Add transition; do not mutate another FSM with similar state labels.
8. Add legal and illegal transition tests.
9. Add concurrency/race tests if state is shared.
10. Refresh FSM registry and traceability.

## Negative tests
- wrong event owner;
- wrong FROM state;
- direct state jump;
- STOP/terminal escape;
- recovery without recoverable flag;
- duplicated transition under race.

## DONE
Transition is source-bound, namespace-safe, testable and auditable.
