# FAILURE
FAILURE_ID: NEXY-BUILD-01-CORE-EXACT-HEAD-RUNNER-BLOCKED-20261004
TASK_ID: NEXY-BUILD-01-CORE-20261004
HEAD: cde969ea2d16626a60ad5571e9308ea294289d15
HEAD_TREE: a6ff8287e3f8aea0dbc674b7dc1ff4f271f3cfb1
STATUS: ACTIVE
CLASS: TEST_INFRASTRUCTURE
SEVERITY: S4_RELEASE_BLOCKING

## Attempted recovery
Re-ran the current-HEAD failures:
- 37157315887 — Exact HEAD test evidence
- 37157315899 — Six-system exact HEAD evidence
- 37157315869 — NEXY CI / Deploy Gate

GitHub accepted all rerun requests.

## Attempt-2 observed evidence
Exact-head job:
- job_id=111428000009
- run_attempt=2
- labels=["ubuntu-latest"]
- runner_id=0
- runner_name=""
- steps=[]
- started=2026-10-04T11:39:23Z
- completed=2026-10-04T11:39:25Z
- conclusion=failure

Six-system job:
- job_id=111428006431
- run_attempt=2
- labels=["ubuntu-latest"]
- runner_id=0
- runner_name=""
- steps=[]
- started=2026-10-04T11:39:25Z
- completed=2026-10-04T11:39:28Z
- conclusion=failure

Deploy-gate attempt 2:
- first-wave jobs all conclude failure before exposing steps;
- dependent DOC-C/release/deploy jobs are skipped.

## Classification
PROVEN:
- no workflow step execution is evidenced for attempt 2;
- the jobs were never associated with a runner (runner_id=0);
- therefore these conclusions cannot be classified as source-test failures.

UNKNOWN:
- exact GitHub-side reason runner allocation did not occur. Billing/quota/account/platform policy must not be guessed without evidence.

## Prevention
- never convert this workflow conclusion into VERIFIED_FAIL for source code;
- never claim npm/cargo tests ran for these attempts;
- require a job with runner identity + executed steps + inspectable logs/artifacts before using it as runtime evidence.

RECOVERY:
Restore a runnable exact-HEAD execution environment, then rerun all mandated gates against cde969ea2d16626a60ad5571e9308ea294289d15 or the new exact HEAD after any authorized mutation.

## Current HEAD recurrence
A concurrent out-of-scope Phase-F commit moved NEXY.ai to 568ec8a820abd543b32a42976d2886377b2c47b7.
New push-triggered runs at that exact HEAD also failed before any exposed steps:
- 37199560362 — Exact HEAD test evidence; job 111428255497; steps unavailable/null.
- 37199560363 — Six-system exact HEAD evidence; job 111428255383; steps unavailable/null.
- 37199560350 — NEXY CI / Deploy Gate; completed failure within seconds.

This recurrence strengthens the infrastructure-block classification. It still does not prove the exact GitHub-side cause.
