# CASE — E11 exact-head validation / release-signoff blocker

CASE_ID: NEXY-CASE-E11-EXACT-HEAD-20260930
related_task: NEXY-E11-HUMAN-APPROVAL-VALIDATION-20260930
implementation_head: d7f824ed7f4b70e5308f3b8bb6a31fbf1ad0a61e
tested_tree: 4cf698ed37f87d68df1c30a3e55bd4bd80a36c5e
severity: S4_RELEASE_BLOCKING
version: 1.0.0
timestamp_source: Railway deployment timestamps

## Cause
Canonical validation carried stale DOC_E_TESTED_SHA / DOC_E_TESTED_TREE, causing exact-head rejection before meaningful validation. After correcting identity metadata, build/typecheck/contract/web-build evidence progressed, but two exact-head deployments still ended FAILED after image build.

## Violation prevented
The E11 verifier correctly prevents an AI-generated/fabricated human approval and requires real engineering/security/migration signoff plus rollback and monitoring verification.

## Impact
- Release remains unauthorized.
- E11 remains BLOCKED_EXTERNAL.
- E12 remains BLOCKED_EXTERNAL for the current exact HEAD.
- E10 also remains BLOCKED_EXTERNAL in the current successful runtime campaign.

## Fix applied
Only canonical Railway exact identity metadata was corrected to:
- SHA d7f824ed7f4b70e5308f3b8bb6a31fbf1ad0a61e
- tree 4cf698ed37f87d68df1c30a3e55bd4bd80a36c5e

No test, schema, workflow, or release-law weakening was performed.

## Evidence
- Contract suite: 97 files / 524 tests PASS.
- E11 fake-approval rejection test PASS.
- Application rollback receipt contract test PASS.
- Production web build produced image digest sha256:e99548f1a24c8c855c2b3ae98fafaf896562b313c67285da0ba1d97ceb137688.
- deployments ce1bf3c1-f3d3-4170-9a7c-46c3aaa929a2 and 69b0c677-2321-4fa0-9b51-22d9ae6a5cbb both FAILED after image build.

## Prevention
- Exact-head identity variables must be refreshed atomically with the target HEAD/tree before validation.
- Human signoff must remain external and evidence-backed.
- E12 application rollback proof must never be replaced with E3 migration rollback proof.
- One reproducibility rerun is sufficient; do not retry until green without diagnosing the blocker.

status: OPEN_BLOCKED
