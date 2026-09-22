# CASE RECORD

CASE_ID: NEXY-ASTRA-CLOSE-REMAINING-GAPS-20260922-CLOSE-CI-RUNNER
cause: GitHub Actions jobs terminate before step creation on authorized NEXY branch
violation: required executable validation evidence unavailable
impact: typecheck, contract, integration, full suite, coverage, build, browser E2E, E7, rollback, auth-abuse and incident drill cannot be accepted as PASS
proof:
- push run 35693191309 attempt 2: primary jobs conclusion=failure, steps=null
- PR run 35693196053 attempt 2: primary jobs conclusion=failure, steps=null
- E7 run 35692777192 attempt 2: critical jobs conclusion=failure, steps=null
- job-log fetches returned BlobNotFound on affected attempts
fix: application/source repair completed where defects were proven; no CI-infrastructure fix available through repository source
prevention: fail closed on missing steps/logs; never equate workflow dispatch or conclusion metadata with executed tests
regression: unknown until runnable CI exists
status: OPEN_EXTERNAL_ENVIRONMENT_BLOCKER
protected_branch_touched: false
