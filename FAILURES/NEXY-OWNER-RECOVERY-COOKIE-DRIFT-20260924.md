FAILURE_ID: NEXY-OWNER-RECOVERY-COOKIE-DRIFT-20260924
status: REPAIRED_PENDING_RUNTIME_REVALIDATION
failed_sha: c94ad368773ba57dd9490286e6cca696fc3ec8a1
failed_deployment: 2027f4a6-2ab7-467e-a0c2-2cee621efd44
failed_gates: full, coverage, coverage_check
passing_gates: npm_ci, prisma_generate, typecheck, contract, integration, doc_c, web_build
root_cause: stale test-only session cookie key prevented active-session lookup branches from executing.
repair_sha: 84484d8108fe1dee186450c0d36c26d360b2596e
revalidation_deployment: aedd277b-38b8-4811-875a-bba1468a0d5f
revalidation_status: BUILDING
