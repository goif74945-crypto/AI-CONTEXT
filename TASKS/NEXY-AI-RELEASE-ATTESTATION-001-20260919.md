# TASK\n\nTASK_ID: NEXY-AI-RELEASE-ATTESTATION-001-20260919
title: Release attestation integrity repair
mode: EXEC
scope: goif74945-crypto/NEXY.AI- branch codex/spec-audit-20260919-78df350
inputs_summary: Repair F-EVID-001/F-GATE-001/F-DEPLOY-001 only; no build/queue/state/api/dependency remediation.
sources:
- target baseline ce0e490f83b2e8d7ce56b2546e0cfc8d8bbbcc25
- target patch ef89492327dbe55acfaa417e5e228a603eb49266
- PR #8 draft validation runner
- GitHub Actions run 35454093303
skills_tools: GitHub repository reads/writes, Actions logs, diff audit
artifacts_paths:
- scripts/evidence-attestation.ts
- scripts/seal-evidence.ts
- scripts/check-doc-c.ts
- .github/workflows/deploy.yml
- tests/contract/release-attestation.test.ts
- package.json
claims_proofs:
- contract suite: 11 files, 106 passed, 0 failed
- integration suite: 71 files, 623 passed, 1 skipped, 0 failed
- E1-E12 runtime attestation contract tests all executed and passed
- tested PR merge SHA: ea48f56ed0637f5e9bf1afb9297a6780c1ac12ee
- source head SHA: ef89492327dbe55acfaa417e5e228a603eb49266
- DOC-C output: STATIC CHECK PASS (NOT RELEASE AUTHORIZATION)
- typecheck failure diagnostic set unchanged from previous validation run
- release attestation job skipped because typecheck failed
- deploy job skipped; no deployment executed
- workflow artifacts list empty because attestation job was correctly blocked
tests_results:
- F-EVID-001 mechanism tests: PASS; end-to-end release chain blocked by F-BUILD-001
- F-GATE-001: PASS
- F-DEPLOY-001 false-claim path: PASS; actual deployment capability BLOCKED_PROVIDER_NOT_CONFIGURED
changes:
- runtime non-self-referential attestation helper added
- historical seal generation disabled; historical verify is integrity-only
- release attestation binds tested/source SHA, branch, run ID, context, actor, commands/results, evidence root/list, release/deploy status
- release attestation job depends on typecheck+contract+integration+DOC-C
- deploy consumes same-run artifact then fails closed when provider absent
successes: stale seal cannot authorize release; DOC-C cannot declare deployability; placeholder deploy claim removed
failures: end-to-end runtime attestation did not execute because typecheck blocker correctly prevented it
decisions: repository remains NON_DEPLOYABLE; PR #8 stays draft/unmerged
unresolved:
- F-BUILD-001
- F-QUEUE-001 untouched
- F-STATE-004 untouched
- F-API-003 untouched
- authoritative deployment provider/runbook absent
risks: full release chain remains blocked until typecheck succeeds and provider/runbook is established
limits: runtime attestation CLI generate/verify was not exercised in workflow because upstream typecheck correctly blocked job; helper/verifier behavior is contract-tested
rollback: revert ef89492327dbe55acfaa417e5e228a603eb49266 on review branch only under explicit authorization
final_status: PARTIAL
next_actions: separately remediate F-BUILD-001, then rerun PR/main validation to execute runtime attestation end-to-end; provider remains separate owner/runbook decision
dependencies: F-BUILD-001 blocks release-attestation execution
version: 1
timestamp_source: GitHub Actions run 35454093303 updated_at=2026-09-19T16:11:01Z
trace_id: GH-ACTIONS-35454093303-PR8
