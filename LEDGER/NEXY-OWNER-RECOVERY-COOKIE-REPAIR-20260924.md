LEDGER_ID: NEXY-OWNER-RECOVERY-COOKIE-REPAIR-20260924
claim: The c94ad368 Railway failure reached application validation and isolated a test-harness defect rather than a production OWNER-recovery semantic defect.
status: VERIFIED
claim: Production reads VNEXT_DEFAULTS.auth.session_cookie_name and canonical configuration is __Host-nexy-session.
status: VERIFIED_FROM_SOURCE
claim: The failing coverage test used stale nexy_session literals on all three active-session scenarios.
status: VERIFIED_FROM_SOURCE
claim: Repair commit 84484d8108fe1dee186450c0d36c26d360b2596e changes only the test harness to consume canonical VNEXT_DEFAULTS auth cookie configuration.
status: VERIFIED_FROM_COMMIT_WRITE
claim: Full validation passes after repair.
status: NOT_YET_VERIFIED
pending_evidence: Railway deployment aedd277b-38b8-4811-875a-bba1468a0d5f gate exit markers.
