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

# Workflow: Add API Route

## Required context
- route contract and SystemEnvelope;
- auth/RBAC/CSRF/idempotency matrix;
- input/output schemas;
- state/FREEZE behavior;
- audit/event requirements.

## Sequence
1. Add/approve API contract record.
2. Define request schema and response schema before route code.
3. Determine mutating vs read-only.
4. For mutation, enforce session + CSRF + idempotency unless explicitly exempted.
5. Enforce backend RBAC independently of UI.
6. Validate input at API boundary and again at the receiving trust boundary when required.
7. Return canonical SystemEnvelope for success and failure.
8. Emit required event/audit/incident evidence transactionally where critical.
9. Add contract, auth, negative, rate-limit, freeze and idempotency tests.
10. Update route traceability.

## Negative tests
- no session;
- wrong role;
- missing/invalid CSRF;
- duplicate idempotency key;
- malformed body;
- system FREEZE;
- dependency unavailable;
- audit persistence failure.

## DONE
Route cannot bypass auth/LAW/FSM/traceability and all error paths remain structured.
