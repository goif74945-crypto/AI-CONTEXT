CASE_ID: CASE-NEXY-SANDBOX-IMPORT-CORRUPTION-80FB8FB0
TASK_ID: NEXY-FULL-AUDIT-80fb8fb0-20261002
mode: AUDIT/CROSS
target_head: 80fb8fb0c85f142635212d3864664bafc50a8919
path: tests/integration/sandbox-tier1-runc.spec.ts
cause: latest commit replaced the valid module specifier "vitest" with "viteหำดำst"
proof: exact current/parent source comparison plus repository search
impact: current runc integration test cannot resolve its intended Vitest import; Sandbox exact-head validation is invalid/blocking
fix: restore only the module specifier to "vitest"; commit on NEXY.ai; rerun full exact-head validation for the new SHA
prevention: add static forbidden-nonASCII/dependency-resolution validation for import specifiers in test/source files where package names must be ASCII package identifiers
severity: S3 correctness failure; release-blocking under exact-head gate
status: OPEN
sanitization: no secrets or personal data
