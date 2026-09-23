CASE_ID: NEXY-ASTRA-20260923-5c3cad
cause: Cross-chat branch advanced 30 commits while audit was in progress; executor revalidated and continued from current HEAD.
violation_or_finding: dead-source OWNER recovery route; recovery CSRF deadlock; vault previousVersion semantic verifier bug; Prisma migration mapping drift.
impact: active requirements remained PARTIAL and could not be truthfully promoted to PASS.
fix: see TASKS/NEXY-ASTRA-20260923-5c3cad.md
prevention: always re-read HEAD before mutation; run semantic source re-audit after each commit; never infer runtime PASS from source existence.
regression: runtime regression execution remains BLOCKED_ENVIRONMENT.
status: OPEN_PARTIAL
trace_id: NEXY-ASTRA-20260923-5c3cad
