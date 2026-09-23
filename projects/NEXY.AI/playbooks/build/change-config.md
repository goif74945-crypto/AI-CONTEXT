# PLAYBOOK — Change Configuration

## PRECONDITIONS
- Config key exists or new key is authorized.
- Runtime-mutability class is known.
- Authority owner/version/rollback target are explicit.

## REQUIRED CONTEXT
- Configuration Registry;
- requirements/defaults;
- supersession graph;
- affected contracts/FSMs/invariants;
- current implementation/config sources;
- tests/evidence.

## IMPLEMENTATION SEQUENCE
1. Resolve canonical current value and source.
2. Identify all duplicate/shadow definitions.
3. Define new value/range/type.
4. Define whether change is runtime-mutable or requires rebuild/redeploy.
5. Define config version bump.
6. Define audit actor/reason.
7. Define rollback value/version.
8. Calculate impact on timeouts/quorum/auth/resource/release behavior.
9. Update one canonical source and eliminate/flag illegal drift.
10. Run boundary tests around new range/value.
11. Run impacted regression.
12. Capture exact version/evidence.

## NEGATIVE TESTS
- invalid/out-of-range value;
- environment drift;
- stale node/config version;
- partial rollout;
- rollback;
- incompatible dependent timeout/threshold.

## DONE
No silent config drift remains and the change is versioned, auditable, reversible where required, and regression-tested.
