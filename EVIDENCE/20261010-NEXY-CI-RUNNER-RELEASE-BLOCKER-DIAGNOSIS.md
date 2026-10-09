# NEXY.AI CI diagnostic: runner-stage failures and release-lock blockers (2026-10-10)
 
Status: READ-ONLY PRODUCT INVESTIGATION / ROOT_CAUSE_INFRA_NOT_PROVEN / RELEASE_LOCK_VERIFIED_STATIC
Product: goif74945-crypto/NEXY.AI-; branch NEXY.ai
Product HEAD observed: 58b1200bd61b867e917057d0019eea78ea9f6b2a
AI-CONTEXT main HEAD observed before this report: 0139db74e7311516875630c1a479b811a9c3c5b0
No product writes, CI dispatches, GitHub settings changes or secret reads.

## FACT: historical live GitHub Actions
- NEXY CI / Deploy Gate, run 37741650343, on historical product SHA 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08: completed/failure. Nine independent jobs failed with no reported failed steps, three downstream jobs skipped. https://github.com/goif74945-crypto/NEXY.AI-/actions/runs/37741650343
- NEXY DOC-E E7 Queue and Rollback, run 37741650376 attempt 2, same historical SHA: six jobs completed/failure; job step summaries were empty (steps=[]), including Redis E7, auth abuse, rollback, incident/alarm, npm audit, deterministic lint. https://github.com/goif74945-crypto/NEXY.AI-/actions/runs/37741650376
- Downloading raw job logs (E7 job 113320413296, lint job 113320415374) returned HTTP 404 BlobNotFound; E7 step API returned steps=[].
- HEAD as observed on 2026-10-10: 58b1200bd61b867e917057d0019eea78ea9f6b2a. Combined commit statuses returned [] and PR-filtered workflow-runs endpoint returned []; neither establishes status of push CI at current HEAD.
- Repo Code Bridge showed 24 active workflows and write/ci backend READY; this does **not** prove GitHub-hosted runner allocation is healthy.

## ANALYSIS / HYPOTHESES (not proven)
- Multi-job failures with no step traces are consistent with a GitHub Actions runner provisioning or account/billing/quota/permissions restriction. Current account billing, Actions budgets, runner availability and UI banners were not independently readable. Do NOT label billing as verified root cause.
- Diagnose by inspecting run annotations/UI, repository Settings > Actions > General and account Settings > Billing & licensing > Budgets and usage. Check usage limit, stop-usage budget, payment issues and GitHub Actions allow settings without making unapproved chargeable changes.
- A minimal existing workflow .github/workflows/omega-runner-diagnostic.yml runs a single ubuntu-latest echo/node/uname step and has workflow_dispatch. If the owner authorizes one dispatch and this fails before a first step, prioritize GitHub infrastructure/account controls and escalate with run/job IDs; if smoke passes, diagnose tests using exact current HEAD and logs.

## FACT: separate deterministic release block in product source
At product HEAD 58b1200b...:
- .github/workflows/deploy.yml constructs push attestation with release_status=NON_DEPLOYABLE, and then Deploy invokes verification with --purpose deployment. https://github.com/goif74945-crypto/NEXY.AI-/blob/58b1200bd61b867e917057d0019eea78ea9f6b2a/.github/workflows/deploy.yml
- scripts/evidence-attestation.ts createRuntimeAttestation throws when release_status === RELEASE_ELIGIBLE; verifyRuntimeAttestation(..., purpose=deployment) requires attestation.release_status === RELEASE_ELIGIBLE. Therefore with the current producer/verifier semantics the Deploy authorization step cannot pass, even if upstream tests pass. This is a deliberate fail-closed release design, not permission to weaken it. https://github.com/goif74945-crypto/NEXY.AI-/blob/58b1200bd61b867e917057d0019eea78ea9f6b2a/scripts/evidence-attestation.ts
- deploy.yml additionally requires NEXY_DEPLOY_PROVIDER and scripts/deployment-provider-contract.ts requires provider/project/token; workflow does not explicitly bind a configured provider to that step. Runtime secret/variable values are UNKNOWN. Do not bypass the provider or invent credentials.
- .github/workflows/doc-e-exact-head.yml enforces DOC-E E1-E12 release verdict and can return BLOCKED_EXTERNAL when genuine external receipts/signoffs are unavailable. A blocked release is not a test PASS.

## Recommended non-regressive closure order
1. Fix **job-start prerequisites**, not application source, once UI evidence isolates runner/account cause. Avoid changes to billing without owner consent.
2. Run an existing isolated runner smoke test once (authorized workflow dispatch), pin recorded SHA/run ID, inspect actual steps/logs.
3. On a working runner, resolve real npm ci/typecheck/lint/contract/integration/coverage/web/E7/E2E failures one at a time with evidence and re-run at exact SHA. Keep real Postgres/Redis, negative/security coverage and deterministic gates.
4. Keep CI validation and deployment authorization logically distinct. Preserve fail-closed DOC-E release, enable RELEASE_ELIGIBLE only with authoritative specification and actual external authorization evidence, provider adapter and real credentials. No artificial green, skipped gates, fabricated attestations or forced deploy.
5. Re-run independent audit and maintain separate labels: TEST_CI, RUNNER_SMOKE, DOC_E_RELEASE, DEPLOY_PROOF.

Result: historical multi-job runner-stage failure observed; exact upstream reason UNKNOWN. Static deployment-auth contradiction VERIFIED. Current HEAD full-CI verdict NOT_VERIFIED.
