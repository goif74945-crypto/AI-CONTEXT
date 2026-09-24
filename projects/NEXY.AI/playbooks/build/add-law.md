# NEXY Builder Playbook

## Universal preconditions
1. Pin repository + branch + exact HEAD.
2. Resolve ontology entity, requirements, authority/scope/supersession/conflicts.
3. Resolve dependencies, implementation refs, contracts, FSM, atomic invariants, security/state/event/config.
4. Check failure/recovery library.
5. Do not infer PASS from file presence, build success, or docs.

# Workflow: Add / Modify Law

## Required context
- authority source;
- supersession impact;
- dependent systems;
- atomic invariant decomposition;
- enforcement point(s);
- failure/freeze semantics.

## Sequence
1. Determine whether this is a new law, new version or supersession.
2. Never edit historical law semantics in place.
3. Add/modify governing source and requirement records first.
4. Decompose law into atomic invariants.
5. Identify enforcement boundaries and forbidden bypasses.
6. Implement deterministic enforcement independent of UI.
7. Add negative tests that deliberately violate each invariant.
8. Verify no lower-authority subsystem can bypass the law.
9. Update authority/supersession/invariant/traceability registries.

## DONE
Law is versioned, enforceable, testable, and bypass-negative-tested.
