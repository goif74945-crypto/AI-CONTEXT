TASK_ID: NEXY-RAILWAY-VALIDATION-C94AD368-20260924
status: PARTIAL_REPAIR_REQUIRED
source_branch: astra/omega-full-spec-convergence
source_sha: c94ad368773ba57dd9490286e6cca696fc3ec8a1
deployment: 2027f4a6-2ab7-467e-a0c2-2cee621efd44
railway_status: FAILED
verified_gates:
  npm_ci: PASS
  prisma_generate: PASS
  typecheck: PASS
  contract: PASS
  integration: PASS
  full: FAIL
  coverage: FAIL
  coverage_check: FAIL
  doc_c: PASS
  web_build: PASS
root_failure: tests/coverage/owner-recovery-control-plane.test.ts has stale hard-coded cookie key nexy_session while canonical VNEXT_DEFAULTS.auth.session_cookie_name is __Host-nexy-session; handler correctly reads canonical cookie name, so two tests bypass session branch and return 202 instead of expected 403/500.
action: defect isolated; no test/coverage weakening authorized or performed.
