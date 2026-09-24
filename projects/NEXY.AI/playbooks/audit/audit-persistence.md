# NEXY Auditor Playbook

## Universal audit law
1. Pin exact repository/branch/HEAD and observed environment.
2. Resolve source authority/scope before implementation.
3. Separate SOURCE / IMPLEMENTATION / TEST / RUNTIME / DEPLOYMENT / PHYSICAL evidence.
4. Never infer PASS from code/docs/build alone.
5. Preserve failure evidence and unresolved UNKNOWN explicitly.

# Workflow: Audit Persistence / State Ownership

## Sequence
1. Resolve authoritative owner for every state object.
2. Compare declared owner with observed writers/readers.
3. Check forbidden tier dependencies.
4. Verify immutability/soft-delete/OCC/idempotency rules.
5. Verify transaction boundaries and partial-failure behavior.
6. Check append-only Event/Audit enforcement.
7. Validate blob/content hashes and lineage.
8. Run migration + rollback roundtrip.
9. Inject DB/blob/write-barrier failures.
10. Verify retention/redaction does not rewrite immutable lineage.

## DONE
No unauthorized writer, orphan state, silent overwrite or untraceable persistence path remains.
