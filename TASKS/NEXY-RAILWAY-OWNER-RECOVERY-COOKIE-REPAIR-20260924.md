TASK_ID: NEXY-RAILWAY-OWNER-RECOVERY-COOKIE-REPAIR-20260924
scope: goif74945-crypto/NEXY.AI- branch astra/omega-full-spec-convergence
source_failure_deployment: 2027f4a6-2ab7-467e-a0c2-2cee621efd44
source_failure_sha: c94ad368773ba57dd9490286e6cca696fc3ec8a1
head_drift_before_repair: NONE
proven_defect: tests/coverage/owner-recovery-control-plane.test.ts used stale cookie key nexy_session while production reads VNEXT_DEFAULTS.auth.session_cookie_name and canonical value is __Host-nexy-session.
repair: imported VNEXT_DEFAULTS in the test and replaced all three stale session-cookie literals with computed canonical key.
production_semantics_changed: NO
test_assertions_weakened: NO
coverage_thresholds_changed: NO
repair_commit: 84484d8108fe1dee186450c0d36c26d360b2596e
railway_revalidation_deployment: aedd277b-38b8-4811-875a-bba1468a0d5f
railway_revalidation_status_at_record: BUILDING
status: REPAIR_COMMITTED_REVALIDATION_PENDING
