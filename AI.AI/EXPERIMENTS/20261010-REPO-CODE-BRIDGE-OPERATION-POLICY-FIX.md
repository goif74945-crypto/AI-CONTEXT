# RCB-20261010-CAPABILITY-POLICY-01 — Repo Code Bridge capability and policy repair

## Status

PARTIAL. This records one source-verified repair slice. The broader RCB requirements, independent release acceptance, and remaining delivery phases were not completed or counted as passed.

## Source and deployment provenance

- Site: Repo Code Bridge, project appgprj_6ac56b9353f88191873e731529a5dc6f.
- Active URL: https://repo-code-bridge.nexy-code-me.chatgpt.site.
- Starting deployed Site version: 20, source commit b57991f72e06f341ebebe4a5db0a9be1fac9b38d.
- Ending Site version: 21, source commit 3f95f2ba36abdead61e8b7dd66d7681bc3902772.
- Source branch: main. The remote HEAD was checked at the starting commit before push; a non-force fast-forward push succeeded, and remote readback matched the ending commit.
- Deployment: appgdep_6ac9ff887b608191870a1c07161ddd10, SUCCEEDED; version ID appgprj_6ac56b9353f88191873e731529a5dc6f~appgver_bb870fe121308191944ebbe482e4a512.
- Sites stored archive SHA-256: 7fd1c4439977eca50b2d3230739005e52858aab2c196e312d6eb642b997b59c9.

## Implemented changes

- Made goif74945-crypto/NEXY.AI- an immutable code-level read-only repository. Configuration overrides cannot grant writes or expose branches other than NEXY.ai.
- Changed runtime_status to distinguish DENIED_BY_GATEWAY_POLICY, NOT_READY, and UNVERIFIED_REMOTE_PERMISSION.
- Added separate contents-write, workflow-file-write, and CI-dispatch grant counts. Workflow-file writes require both the contents-write and workflow-write grants.
- Updated the Site UI and README to report those operation-specific states without claiming remote permission probes.

Changed paths: README.md; app/page.tsx; lib/gateway.ts; lib/repository-policy.ts; tests/repository-policy.test.mjs.

## Verification

- npm test: PASS, 40 tests, 0 failures.
- npm run build: PASS.
- ESLint on changed files: PASS.
- git diff --check: PASS.
- Full npm run lint: BLOCKED by Node heap exhaustion at both 2 GB and 4 GB heap limits; no lint result for the full repository.
- Live runtime after deployment: GitHub CONNECTED, D1 READY, 15 configured repositories, 15 read-only. Contents write, workflow write, and CI dispatch each report DENIED_BY_GATEWAY_POLICY with 0 exact grants; remote permission probes remain NOT_PERFORMED.
- Live repo_catalog confirms goif74945-crypto/NEXY.AI- is read-only and exposes only NEXY.ai.

## Unverified and remaining work

- No GitHub Actions workflow was dispatched or verified.
- No remote write-capability probe was performed; the current Site policy grants zero writes and zero CI dispatches.
- No performance benchmark or independent source audit was performed.
- Other proposed RCB capabilities and mandatory deliverables remain unassessed; no completion percentage is claimed.
- The product repository and isolated E2E repository were not modified.