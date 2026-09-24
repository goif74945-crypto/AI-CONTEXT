# NEXY Auditor Playbook

## Universal audit law
1. Pin exact repository/branch/HEAD and observed environment.
2. Resolve source authority and scope before reading code.
3. Separate SOURCE / IMPLEMENTATION / TEST / RUNTIME / DEPLOYMENT / PHYSICAL evidence.
4. Use only: PASS / FAIL / PARTIAL / NOT IMPLEMENTED / NOT VERIFIED / UNKNOWN / BLOCKED / CONFLICT / SCOPE where applicable.
5. File existence, docs, mocks, build success, or comments are never runtime proof.
6. Search failure history and known conflicts before declaring a new root cause.
7. Preserve evidence even when verdict is FAIL.

# Workflow: Audit FSM

## Sequence
1. Identify namespace by FSM ID.
2. Enumerate states/events/event owners.
3. Compare source transition table to implementation table.
4. Verify guards/actions/failure/audit semantics.
5. Enumerate every illegal transition.
6. Test terminal/freeze/recovery behavior.
7. Test wrong actor/event ownership.
8. Test concurrency/race where state is shared.
9. Check same-named states in other FSMs are not conflated.

## Special rule
Implementation-only state models must stay explicitly non-canonical until promoted.

## DONE
Legal transitions pass; every illegal transition fails deterministically with correct evidence.
