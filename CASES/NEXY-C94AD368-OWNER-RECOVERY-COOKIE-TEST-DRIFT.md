CASE_ID: NEXY-C94AD368-OWNER-RECOVERY-COOKIE-TEST-DRIFT
classification: TEST_HARNESS_DRIFT
provenance: Railway deployment 2027f4a6-2ab7-467e-a0c2-2cee621efd44
symptom: full and coverage suites each report 2 failures in owner-recovery-control-plane.test.ts.
expected: active non-OWNER session -> 403; session lookup failure -> 500 DEPENDENCY_FAILURE.
observed: handler continued into recovery path and returned 202.
root_cause: tests present cookies under nexy_session; runtime handler reads VNEXT_DEFAULTS.auth.session_cookie_name; canonical value is __Host-nexy-session.
repair: update test harness to use canonical cookie name/value, preferably importing VNEXT_DEFAULTS or exact canonical key without changing production behavior.
