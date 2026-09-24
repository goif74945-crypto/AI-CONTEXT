# NEXY Builder Playbook

## Universal preconditions
1. Pin repository + branch + exact HEAD.
2. Resolve ontology entity, requirements, authority/scope/supersession/conflicts.
3. Resolve dependencies, implementation refs, contracts, FSM, atomic invariants, security/state/event/config.
4. Check failure/recovery library.
5. Do not infer PASS from file presence, build success, or docs.

# Workflow: Add Capability

## Required context
- CapabilityNode schema/version;
- deterministic class;
- dependency closure;
- forbidden combinations;
- resource/permission caps;
- static verifier;
- policy review/quorum;
- registry FSM and public projection.

## Sequence
1. Create a new immutable version; never mutate an ACTIVE historical node.
2. Canonicalize/hash node.
3. Resolve dependency closure and conflicts.
4. Assign deterministic class.
5. Run static verification.
6. Run human/policy review and required quorum.
7. Advance only through legal registry FSM.
8. Anchor/activate only when all gates pass.
9. Add rejection reason code on failure.
10. Run chaos/adversarial catalog applicable to the change.

## DONE
Capability is versioned, dependency-closed, policy-approved, chaos-tested and traceable.
