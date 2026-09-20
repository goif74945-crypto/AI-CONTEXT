# TASK

TASK_ID: NEXY-F-RELEASE-001-REPAIR-20260920
title: Fail-closed DOC-E release authorization repair
mode: EXEC/CROSS
scope: goif74945-crypto/NEXY.AI- branch codex/spec-audit-20260919-78df350; F-RELEASE-001 only
inputs_summary: Preserve red-test commit e091fc9c2ab0d963f39d424b732b28254cdc6202, prevent CI-only RELEASE_ELIGIBLE minting, restore branch CI green without merge/deploy.
sources:
- authoritative spec snapshot SHA256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
- DOC-E sections 9.1-9.7: E1-E12 artifacts, signoff, rollback and monitoring requirements
- target HEAD before e091fc9c2ab0d963f39d424b732b28254cdc6202
- implementation commit 39a857fc753405a43671234c10ae306b6f81b551
- PR #8 open/draft/unmerged
- GitHub Actions run 35491343876
skills_tools: GitHub repository Git-data writes, Actions jobs/logs/artifacts, uploaded spec hash/content inspection
actions:
- bumped runtime attestation contract v2 -> v3
- createRuntimeAttestation rejects RELEASE_ELIGIBLE with DOC-E E1-E12 fail-closed error
- deployment verifier checks required gate success before release authorization and independently blocks raw/tampered RELEASE_ELIGIBLE on incomplete DOC-E
- workflow keeps PR VALIDATION_ONLY and main push NON_DEPLOYABLE; no CI path auto-mints RELEASE_ELIGIBLE
- added raw attestation bypass regression and restored gate-specific E9/E10 assertions
- added targeted release-attestation Vitest step before full contract suite
artifacts_paths:
- scripts/evidence-attestation.ts
- .github/workflows/deploy.yml
- tests/contract/release-attestation.test.ts
claims_proofs:
- patch changes exactly 3 authorized files
- targeted release-attestation test: 1 file, 18 passed
- contract: 11 files, 110 passed
- integration: 71 files, 629 passed, 1 skipped
- full suite: 89 files, 766 passed, 1 skipped
- typecheck: SUCCESS
- DOC-C: ALL PASS / STATIC CHECK PASS (NOT RELEASE AUTHORIZATION)
- release-attestation job: SUCCESS
- deploy job on PR: SKIPPED
- source SHA: 39a857fc753405a43671234c10ae306b6f81b551
- tested synthetic merge SHA: 8e9adb697f1c5090184b54fb42a8ee4b5e2e1f63
- source->tested synthetic compare changed files: []
- runtime attestation version: nexy-ci-runtime-v3
- runtime release_status: VALIDATION_ONLY
- runtime deploy_status: NOT_DEPLOYED
- artifact: nexy-runtime-attestation-35491343876 id=10598649511 expired=false
- artifact digest: sha256:80cc230c547976bf209d7664c3de92ba7cc5a4180d2aa0a21afeefaf51351e55
successes: F-RELEASE-001 release/evidence integrity defect repaired in scope; current PR CI green; no deploy/merge occurred.
failures: none in authorized repair execution.
decisions: repository remains NON_DEPLOYABLE; DOC-E E1-E12 is not yet encoded/proven as deployment authorization; PR #8 remains draft/open.
unresolved:
- DOC-E E1-E12 completeness remains unresolved by design
- queue findings remain open
- coverage remains unresolved
- state findings remain open
risks: future release logic must not remove v3 fail-closed DOC-E gate until a real machine-verifiable E1-E12 contract and current proof exist.
limits: local runner unavailable; validation evidence is GitHub Actions execution on synthetic PR merge, proven content-equivalent to source head by empty compare.
rollback: under explicit authorization only, revert 39a857fc753405a43671234c10ae306b6f81b551 on review branch; do not merge/deploy.
final_status: VERIFIED_WITH_LIMITS
next_actions: auditor may proceed to the next independently authorized finding; do not treat this task as release-ready.
dependencies: DOC-E E1-E12 owner/spec implementation required before release eligibility can ever be minted.
version: 1
timestamp_source: GitHub Actions run 35491343876 updated_at=2026-09-20T05:20:16Z
trace_id: GH-ACTIONS-35491343876-PR8
hash: sha256:80cc230c547976bf209d7664c3de92ba7cc5a4180d2aa0a21afeefaf51351e55
