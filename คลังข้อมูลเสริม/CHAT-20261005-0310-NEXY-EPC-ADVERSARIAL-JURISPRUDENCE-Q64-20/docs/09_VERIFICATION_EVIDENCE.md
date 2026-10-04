# Verification Evidence

## Local reference implementation
STATUS: PASS

Evidence files:
- `evidence/VERIFY.log` — `npm run verify`; two complete suites, 40/40 PASS normal and 40/40 PASS production-mode rerun.
- `evidence/REPLAY_PROOF.log` — 1,000 identical canonical replays; stable SHA-256.
- `evidence/INTEGRATION_EXAMPLE.log` — twenty organs all PASS, output `READY_FOR_EXTERNAL_JUDGE`, mutation/promotion capabilities false.
- `evidence/NPM_PACK_DRY_RUN.log` — package composition dry-run.
- `evidence/TOOLCHAIN.txt` — actual toolchain observed.
- `evidence/SECRET_SCAN.log` — bounded common credential-pattern scan of authored package files.
- `evidence/METRICS.txt` — implementation/test size metrics.
- `MANIFEST.sha256` — source/test/doc/evidence content hashes generated after final local verification.

## Claims and evidence classes
- Compiles under strict TypeScript: E1 PASS.
- Authoritative source contains no scanned float/random/wall-clock tokens: E1 PASS.
- Court/Q64 behaviors represented by tests: E2 PASS for tested cases.
- Standalone end-to-end library/example boundary: local integration-reference PASS.
- Exact NEXY runtime integration: NOT_VERIFIED.
- Production deployment: NOT_VERIFIED / OUT OF SCOPE.
- Canon promotion: NOT AUTHORIZED.

## Regression discovered and repaired
Initial Q64 ratio helper incorrectly bounded the temporary `numerator * Q64_ONE` to i128 before division. This would falsely reject valid ratios of accumulated Q64 quantities. The repair uses exact arbitrary-precision bigint for the temporary product and applies signed-i128 validation to the represented final Q64.64 result. A dedicated regression test now covers `(5*ONE)/(10*ONE) = 0.5`.
