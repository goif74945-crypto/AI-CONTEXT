# NEXY Auditor Playbook

## Universal audit law
1. Pin exact repository/branch/HEAD and observed environment.
2. Resolve source authority and scope before reading code.
3. Separate SOURCE / IMPLEMENTATION / TEST / RUNTIME / DEPLOYMENT / PHYSICAL evidence.
4. Use only: PASS / FAIL / PARTIAL / NOT IMPLEMENTED / NOT VERIFIED / UNKNOWN / BLOCKED / CONFLICT / SCOPE where applicable.
5. File existence, docs, mocks, build success, or comments are never runtime proof.
6. Search failure history and known conflicts before declaring a new root cause.
7. Preserve evidence even when verdict is FAIL.

# Workflow: Audit Security / Trust Boundaries

## Sequence
1. Load trust-boundary and permission matrices.
2. Enumerate external inputs, secrets, roles, sessions, cross-plane calls.
3. Verify validation and authorization at each receiver.
4. Attack auth replay, OTAC abuse, CSRF, rate-limit bypass and session misuse.
5. Attack prompt/model injection and authority escalation.
6. Attack sandbox/tenant/universe escape where in scope.
7. Verify security incidents/audit evidence are fail-closed.
8. Confirm UI visibility is never the authorization layer.
9. Confirm secrets are absent from client/source/log surfaces where forbidden.

## DONE
No untrusted path crosses into authority without the required proof/control.
