# PLAYBOOK — Add Capability

## SCOPE WARNING
Capability Registry / NCF admission belongs to future architecture unless explicitly promoted into current build scope. Do not implement into DOC-C merely because the design exists.

## PRECONDITIONS
- Scope registry authorizes capability work.
- Parent/root capability envelope identified.
- No privilege escalation.
- Admission/verifier/governance path selected.

## REQUIRED CONTEXT
- CapabilityNode ontology/registry design;
- G20/G21/G22 governance;
- capability DAG;
- deterministic class;
- resource/permission envelope;
- rejection reason codes;
- chaos/admission tests;
- supersession/version law.

## IMPLEMENTATION SEQUENCE
1. Define immutable capability ID/version/type.
2. Define dependencies and forbidden combinations.
3. Define max depth/resource profile/permission scope.
4. Define deterministic class: STRICT / SANDBOXED / NONDET_RENDER where source-authorized.
5. Canonicalize and hash the node.
6. Run static admission checks:
   schema, dependency closure, cycle, permission escalation, resource cap, syscall/network/dynamic-load rules.
7. For STRICT, run additional deterministic/cross-build checks.
8. Produce VerificationReport.
9. Run policy-risk gate if governance stage requires it.
10. Record ACCEPT/REJECT through governed reason codes.
11. Activate only after the required finalized governance/anchor state in that architecture.
12. Run relevant ChaosUniverse scenarios before promotion where required.

## NEGATIVE TESTS
- dependency cycle;
- undeclared network;
- dynamic code load;
- privilege/resource escalation;
- deterministic-class bypass;
- duplicate rejected hash;
- activation before governance/finalization.

## DONE
Capability is never considered ACTIVE merely because code exists; admission state and required evidence must be proven.
