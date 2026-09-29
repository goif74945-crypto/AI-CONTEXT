# CASE-NEXY-DOC-E-2026-09-30-EFC680A

CASE_ID: CASE-NEXY-DOC-E-2026-09-30-EFC680A
cause: GitHub-hosted runner did not start job steps
violation: none proven in application code from this execution plane
impact: DOC-E validation cannot advance beyond environment gate
proof:
- workflow run 36602881913
- job 109524417528
- conclusion=failure
- steps=null
- logs_url=null
- minimal job contained only echo/node --version/uname
fix_attempts:
- repaired source corruption independently before diagnosing runner
- introduced minimal NEXY.ai runner-smoke workflow
prevention:
- preserve separate runner-smoke diagnostic
- do not classify no-step runner failures as test failures
regression_status: NOT_EXECUTED
status: OPEN / BLOCKED_ENVIRONMENT
