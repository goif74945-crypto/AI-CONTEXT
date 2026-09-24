# NEXY Auditor Playbook

## Universal audit law
1. Pin exact repository/branch/HEAD and observed environment.
2. Resolve source authority/scope before implementation.
3. Separate SOURCE / IMPLEMENTATION / TEST / RUNTIME / DEPLOYMENT / PHYSICAL evidence.
4. Never infer PASS from code/docs/build alone.
5. Preserve failure evidence and unresolved UNKNOWN explicitly.

# Workflow: Audit Failure / Recovery

## Sequence
1. Identify failure code/layer and primary failure priority.
2. Confirm containment/freeze occurs before unsafe continuation.
3. Verify incident + event + audit linkage.
4. Confirm recoverable flag and actor authorization.
5. Confirm pending output is invalidated.
6. Confirm failed/old job is not silently resumed when source requires a new cycle.
7. Verify rollback/replay/snapshot/WAL checks where applicable.
8. Inject repeated recovery failure/crash loops.
9. Confirm nonrecoverable failures remain blocked.
10. Record proven root cause/recovery into Failure Library only after evidence exists.

## DONE
Recovery cannot fabricate history, bypass authority or report success without proof.
