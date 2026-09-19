# CASE

TASK_ID: NEXY-AI-VALIDATION-RECOVERY-API002-STATE003-20260919
title: Validation recovery + API002 + STATE003
mode: EXEC
scope: goif74945-crypto/NEXY.AI- branch codex/spec-audit-20260919-78df350
inputs_summary: Re-audit F-CI-001, F-API-002, F-STATE-003; retest F-API-001/F-STATE-001/F-STATE-002; no queue/outbox mutation.
sources:
- authoritative NEXY DOC-C/DOC-B supplied in project
- target git baseline e950f1131baeb450537c1c44a6a83034a101f088
- GitHub Actions baseline run 34740944733
- GitHub Actions validation run 35448899862
skills_tools: GitHub repository reads/writes, GitHub Actions logs, source/diff audit
artifacts_paths:
- target commit ce0e490f83b2e8d7ce56b2546e0cfc8d8bbbcc25
- draft PR #8
actions:
- repaired Vitest 4.1.6 discovery scripts using positional path filters
- fail-closed session-store read failures into canonical DEPENDENCY_FAILURE envelope
- one-shot process hydration latch prevents implicit FREEZE/STOP recovery
- added/reworked targeted regression tests
claims_proofs:
- Contract CI: 10 test files, 91 passed, 0 failed
- Integration CI: 71 test files, 623 passed, 1 skipped, 0 failed
- DOC-C gate: success
- Typecheck: failure with error set unchanged from baseline
- Evidence seal: failure; not repaired in this scope
- Deploy: skipped
tests_results:
- F-CI-001 targeted discovery: PASS
- F-API-002 targeted integration tests: PASS
- F-STATE-003 targeted contract tests S1-S10: PASS
- F-API-001 retest: PASS
- F-STATE-001 retest: PASS
- F-STATE-002 retest: PASS
changes:
- package.json
- packages/api/bootstrap.ts
- packages/api/directives.ts
- packages/orch-core/system-state.ts
- tests/contract/hydration-fail-closed.test.ts
- tests/integration/directives/read-auth.spec.ts
successes: authorized findings have executable targeted evidence
failures: full workflow remains failure due pre-existing typecheck errors and evidence seal failure
decisions: branch remains NON_DEPLOYABLE; no merge/deploy; queue finding untouched
unresolved:
- pre-existing typecheck blocker
- evidence seal verification failure
- queue/outbox issue reported by another worker remains untrusted/not audited here
risks: draft PR is validation-only and must not be merged until gate release
limits: no full-project compliance claim; PR validation uses GitHub pull_request environment
rollback: revert target commit ce0e490f83b2e8d7ce56b2546e0cfc8d8bbbcc25 or move review branch to its parent only under explicit authorization
final_status: PARTIAL
next_actions: separately scope typecheck/evidence/queue remediation; retain draft PR as non-deployable validation evidence
dependencies: none for the three authorized targeted findings; project release still blocked
version: 1
timestamp_source: GitHub Actions run 35448899862 updated_at=2026-09-19T14:31:07Z
trace_id: GH-ACTIONS-35448899862-PR8

case_cause: CI test discovery regression plus two source-proven fail-closed/state-rehydration defects.
case_impact: critical suites previously executed zero tests; auth dependency errors escaped envelope; repeated hydration could overwrite live freeze/stop semantics.
case_fix: positional Vitest filters; canonical dependency failure envelope; one-shot hydration semantics.
case_prevention: retain >0 suite discovery in CI and S1-S10 hydration regressions.
regression_status: targeted contract/integration suites green; project-wide release gate not green.
