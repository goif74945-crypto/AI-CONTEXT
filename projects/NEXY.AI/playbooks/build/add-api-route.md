# PLAYBOOK — Add API Route

## PRECONDITIONS
- Route is authorized by DOC-C/current scope or explicit extension.
- API boundary owner is resolved.
- Authentication/RBAC/CSRF/idempotency semantics are known.

## REQUIRED CONTEXT
- DOC-C API law;
- Contract Registry API/schema/error records;
- RBAC/security trust map;
- SystemEnvelope contract;
- relevant requirements;
- implementation route map;
- tests/evidence matrix.

## IMPLEMENTATION SEQUENCE
1. Define method/path and owner.
2. Define request schema and runtime validation.
3. Define response through canonical SystemEnvelope.
4. Define auth/RBAC.
5. Define CSRF requirement for mutation.
6. Define idempotency key behavior for mutation unless exempt by authority.
7. Define allowed errors/status codes.
8. Define timeout/retry semantics.
9. Define audit/security incident emission.
10. Implement route → authorized service/core boundary.
11. Prohibit direct UI→LAW/VAULT or other forbidden dependencies.
12. Add contract tests + auth/RBAC negative tests + schema tests.
13. Add integration/E2E if route crosses persistence/queue/UI boundaries.

## NEGATIVE TESTS
- malformed body;
- expired/revoked session;
- wrong role;
- invalid CSRF;
- duplicate idempotency key;
- frozen system;
- downstream dependency failure;
- timeout;
- information leakage in errors.

## DONE
Route contract, auth, runtime validation, idempotency/audit behavior and required evidence must pass.
