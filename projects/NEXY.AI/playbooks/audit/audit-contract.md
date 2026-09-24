# NEXY Auditor Playbook

## Universal audit law
1. Pin exact repository/branch/HEAD and observed environment.
2. Resolve source authority and scope before reading code.
3. Separate SOURCE / IMPLEMENTATION / TEST / RUNTIME / DEPLOYMENT / PHYSICAL evidence.
4. Use only: PASS / FAIL / PARTIAL / NOT IMPLEMENTED / NOT VERIFIED / UNKNOWN / BLOCKED / CONFLICT / SCOPE where applicable.
5. File existence, docs, mocks, build success, or comments are never runtime proof.
6. Search failure history and known conflicts before declaring a new root cause.
7. Preserve evidence even when verdict is FAIL.

# Workflow: Audit Contract

## Sequence
1. Identify exact producer/consumer and version.
2. Compare source contract vs implementation schema field-by-field.
3. Check preconditions/postconditions/error contract/timeout/idempotency/auth.
4. Check runtime validation at both sides of trust boundary.
5. Test malformed, missing, extra, boundary and version-drift payloads.
6. Inspect compatibility and migration impact.
7. Check downstream code does not rely on undocumented fields.

## Verdict rule
Schema parse success is insufficient if semantics/authority/failure behavior differ.

## DONE
All contract fields and negative behaviors are traceable and version-safe.
