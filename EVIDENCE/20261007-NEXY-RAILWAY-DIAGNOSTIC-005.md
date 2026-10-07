# Evidence — NEXY VS Code and Railway Diagnostic

EVIDENCE_ID: EVIDENCE-20261007-NEXY-RAILWAY-DIAGNOSTIC-005
TASK_ID: 20261007-NEXY-RAILWAY-DIAGNOSTIC-005
MODE: EXECUTE_NOW / ENGINEERING / EVIDENCE_DRIVEN / FAIL_CLOSED
STATUS: BLOCKED_WITH_RESUME
OBSERVED_UTC: 2026-10-07T16:19:21Z

## Target

- Product repository: `goif74945-crypto/NEXY.AI-`
- Branch: `NEXY.ai`
- Target HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- AI-CONTEXT parent: `8b9e258b2356ed7d07ecea66cc48a5e2bf4d1c40`
- Spec SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`

## GitHub VS Code

- github.dev URL returned: `https://github.dev/goif74945-crypto/NEXY.AI-`
- vscode.dev URL returned: `https://vscode.dev/github/goif74945-crypto/NEXY.AI-`
- Result: URL returned; browser authentication/session required; no product mutation performed.

## Wix

Wix plugin context was loaded. The request did not specify a Wix site ID or a Wix app project. No Wix API mutation or deployment was made. Wix was not treated as a substitute for the repository's exact-head test runner.

## Railway

- Project: `NEXY Validation R2` (`01537473-6a6d-42a0-856f-40d8a4e6a712`)
- `nexy-validation`: branch `NEXY.ai`, failed deployment commit `6769b725e46753ce5af58a972c005894065f38da`
- Failure: contract gate; 2 failed files and 112 passed; Phase-F isolation assertion failed.
- `nexy-validation-branch`: branch `NEXY.AI-Test-AI`, failed deployment commit `dd9e691e346e97701877ad6e2e5ff5642ca1b068`
- Failure: coverage/auth decision paths; 3 failed tests, 179/180 files, 1232/1235 tests.

Neither is evidence for target HEAD `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.

## Integrity

- Product files changed: NO
- Product commit: NO
- New CI run: NO
- New Railway deployment: NO
- Backend bypass: NO
- PASS_100: NO

## Resume

After actual authorized write and CI dispatch succeed, freeze new HEAD, use TDD RED → GREEN, and create fresh exact-head evidence.
