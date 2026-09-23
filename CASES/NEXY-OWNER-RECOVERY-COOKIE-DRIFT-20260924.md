CASE_ID: NEXY-OWNER-RECOVERY-COOKIE-DRIFT-20260924
classification: TEST_HARNESS_DRIFT
failure_evidence: Railway deployment 2027f4a6-2ab7-467e-a0c2-2cee621efd44 completed with full/coverage/coverage_check failures caused by two OWNER recovery tests.
production_authority: packages/api/owner-recovery.ts indexes req.cookies[VNEXT_DEFAULTS.auth.session_cookie_name].
canonical_config: packages/api/vnext-config.ts sets session_cookie_name to __Host-nexy-session.
stale_test_behavior: tests/coverage/owner-recovery-control-plane.test.ts supplied nexy_session for active-session paths.
repair_sha: 84484d8108fe1dee186450c0d36c26d360b2596e
verification: Railway deployment aedd277b-38b8-4811-875a-bba1468a0d5f BUILDING; final gate result pending.
