# NEXY Builder Playbook

## Universal preconditions
1. Pin repository + branch + exact HEAD.
2. Resolve ontology entity, requirements, authority/scope/supersession/conflicts.
3. Resolve dependencies, implementation refs, contracts, FSM, atomic invariants, security/state/event/config.
4. Check failure/recovery library.
5. Do not infer PASS from file presence, build success, or docs.

# Workflow: Add UI Surface

## Required context
- backend truth source;
- role visibility;
- API contracts;
- FREEZE/error/pending states;
- Human Gravity boundary.

## Sequence
1. Define what authoritative backend state the surface renders.
2. Define role visibility without treating it as authorization.
3. Use approved API contracts; never read/write LAW/VAULT directly.
4. Render loading only while backend is pending.
5. Render FREEZE/error/blocking state explicitly.
6. Never display partial/candidate output as released final output.
7. Add mobile/desktop truth-state tests.
8. Add direct-API RBAC tests separately from visibility tests.
9. Update UI ontology/implementation/traceability map.

## Negative tests
- backend FREEZE while UI action is pending;
- unauthorized role deep-links directly;
- backend error after optimistic submit;
- stale cached success;
- missing data/empty state.

## DONE
UI cannot invent authority or success and remains truthful under failure.
