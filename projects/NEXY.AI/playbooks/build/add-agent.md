# NEXY Builder Playbook

## Universal preconditions
1. Pin repository + branch + exact HEAD.
2. Resolve ontology entity, requirements, authority/scope/supersession/conflicts.
3. Resolve dependencies, implementation refs, contracts, FSM, atomic invariants, security/state/event/config.
4. Check failure/recovery library.
5. Do not infer PASS from file presence, build success, or docs.

# Workflow: Add Agent / Model Adapter

## Required context
- provider/model identity;
- schema version;
- supported modes;
- deterministic capability flag;
- criticality;
- timeout/context capacity;
- health interface;
- security/Cage rules;
- cost/trust routing policy.

## Sequence
1. Register adapter metadata and stable ID.
2. Define execute/cancel/health contracts.
3. Treat all model output as untrusted proposal.
4. Enforce timeout bounds and cancellation.
5. Define critical vs noncritical failure semantics.
6. Route through Swarm→verification→Judge; never direct-release.
7. Apply prompt-law/security boundary.
8. Add malformed output, timeout, provider error, injection and disagreement tests.
9. Update trust/cost metrics only from governed outcomes.

## DONE
Adapter cannot bypass verification/release authority and all failure modes are explicit.
