FAILURE_ID: NEXY-C94AD368-FULL-COVERAGE
status: OPEN
severity: validation-blocker
failed_gates: full, coverage, coverage_check
passing_gates: npm_ci, prisma_generate, typecheck, contract, integration, doc_c, web_build
failed_file: tests/coverage/owner-recovery-control-plane.test.ts
failed_tests:
  - rejects active non-OWNER and active OWNER sessions
  - fails closed when active-session lookup fails
counts: 2 failed / 670 passed / 672 total; 1 failed file / 88 passed files / 89 total
cause: stale test cookie key, not a proven production handler defect.
