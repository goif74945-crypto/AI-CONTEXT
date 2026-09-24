# NEXY Auditor Playbook

## Universal audit law
1. Pin exact repository/branch/HEAD and observed environment.
2. Resolve source authority/scope before implementation.
3. Separate SOURCE / IMPLEMENTATION / TEST / RUNTIME / DEPLOYMENT / PHYSICAL evidence.
4. Never infer PASS from code/docs/build alone.
5. Preserve failure evidence and unresolved UNKNOWN explicitly.

# Workflow: Audit Determinism

## Sequence
1. Identify authoritative vs presentation/nondeterministic domain.
2. Enumerate all mutation points.
3. Verify single canonical mutator where required.
4. Verify event ordering, counters and tie-breaks.
5. Scan authoritative math for float/RNG/system-clock/unordered iteration.
6. Verify environment/toolchain/target identity inputs.
7. Rebuild/replay same inputs across repeated runs/architectures where required.
8. Compare state hash after each canonical replay step.
9. Inject overflow, timing, ordering and crash faults.
10. Verify divergence freezes rather than self-heals silently.

## DONE
Same authorized inputs/environment produce the required identical authoritative state/hash, with divergence handled by law.
