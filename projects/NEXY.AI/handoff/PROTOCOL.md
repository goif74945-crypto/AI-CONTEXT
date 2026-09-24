# NEXY Handoff Protocol v2

1. **CREATE** — sender emits a schema-valid package with exact target identity and scope.
2. **VALIDATE** — receiver validates schema, package type, references, supersession and forbidden secret-bearing content.
3. **REFRESH** — receiver reads current target branch/HEAD.
4. **STALE GUARD** — if current HEAD differs from `expected_head`, mark the package STALE; do not execute it.
5. **REVALIDATE** — run semantic diff + change impact and refresh affected claims/evidence.
6. **SUPERSEDE OR BLOCK** — issue a new package referencing the old ID, or stop with an evidence-backed blocker.
7. **EXECUTE** — Builder acts only within `allowed_scope`, respecting `forbidden_scope`, stop conditions and human gates.
8. **RETURN** — Builder emits `BUILDER_TO_AUDITOR` with exact START_HEAD/END_HEAD, commits, actions, tests and evidence.
9. **AUDIT** — Auditor reads back the END_HEAD and checks acceptance, regression, evidence freshness and residual risk.
10. **RESUME** — receiving worker follows `resume.next_action` only after required refreshes.

No package may silently rewrite historical expected-head, scope, claims or evidence.
No handoff may bypass destructive-operation, credential, production, authority-conflict or security-expansion human gates.
