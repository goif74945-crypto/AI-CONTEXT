# PLAYBOOK — Audit Security

## PURPOSE
Audit trust boundaries, authorization, input isolation, secret handling and containment without claiming security from design prose.

## PROCEDURE
1. Load trust-boundaries, permission matrix, threat model.
2. Identify assets/actors/trust transitions.
3. Inspect every external/untrusted input boundary.
4. Inspect auth/session/role/CSRF/rate/idempotency where applicable.
5. Inspect external model/tool/provider isolation.
6. Inspect secrets handling and frontend exposure.
7. Inspect sandbox/execution permissions.
8. Inspect tenant/session/project isolation.
9. Inspect security incident emission and freeze/containment.
10. Test abuse paths appropriate to the target.
11. Search for hidden admin/debug/force routes.
12. Check current deployment evidence before making operational security claims.

## ATTACK CLASSES
- prompt/instruction injection;
- replay/reuse;
- privilege escalation;
- IDOR/cross-project access;
- session fixation/revoked-session reuse;
- CSRF;
- rate-limit bypass;
- secret leakage;
- unsafe RCE/tool invocation;
- sandbox escape;
- model output injection;
- tenant/universe escape;
- audit suppression.

## PASS
Requires matching evidence; static code alone cannot prove runtime containment/security.
