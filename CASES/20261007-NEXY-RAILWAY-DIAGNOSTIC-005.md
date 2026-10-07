# Case — NEXY Railway Diagnostic Is Stale

CASE_ID: CASE-20261007-NEXY-RAILWAY-DIAGNOSTIC-005
TASK_ID: 20261007-NEXY-RAILWAY-DIAGNOSTIC-005
STATUS: BLOCKED_WITH_RESUME
OPENED_UTC: 2026-10-07T16:19:21Z

## Request

Run and repair NEXY using GitHub VS Code, Wix, and Railway.

## Observed

Railway has an existing validation project, but the latest failed deployments are not tied to the frozen product HEAD:

| Service | Branch | Deployment | Commit | Result |
|---|---|---|---|---|
| nexy-validation | NEXY.ai | a4e4f0a2-982c-47cd-b1cf-12ba1b120ef0 | 6769b725e46753ce5af58a972c005894065f38da | FAILED |
| nexy-validation-branch | NEXY.AI-Test-AI | e06fbfc7-7a98-4b4f-a383-b820f6b23147 | dd9e691e346e97701877ad6e2e5ff5642ca1b068 | FAILED |

The product gateway's actual `ci_dispatch` operation is still denied with HTTP 403 `REPOSITORY_READ_ONLY`.

## Decision

Use the Railway logs as root-cause leads only. Do not promote them to current evidence and do not trigger a substitute deployment while the locked gateway capability is inconsistent.
