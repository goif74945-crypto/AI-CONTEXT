# Evidence — Direct GitHub/Railway Exact-Head Run Blocked

EVIDENCE_ID: EVIDENCE-20261007-NEXY-DIRECT-RUN-BILLING-BLOCK-006
MODE: EXECUTE_NOW / ENGINEERING / EVIDENCE_DRIVEN / FAIL_CLOSED
STATUS: BLOCKED_WITH_RESUME
OBSERVED_UTC: 2026-10-07T17:07:00Z

## Authority

- Product repository: `goif74945-crypto/NEXY.AI-`
- Product branch: `NEXY.ai`
- Product target HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- Authoritative DOCX SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- Coordination repository: `goif74945-crypto/AI-CONTEXT`
- Coordination branch at observation: `main`
- Prior AI-CONTEXT HEAD: `d84860222078feea3ee02887ffc6d0cfd3ef39ca`

## Direct execution attempted

The current user explicitly requested execution without Repo Code Bridge. The following direct, authorized surfaces were used:

1. GitHub repository API/read access for the exact product HEAD.
2. GitHub Actions rerun of failed jobs for the existing exact-head workflow runs:
   - `37222997743`, latest rerun attempt `6`
   - `37222997798`, latest rerun attempt `5`
   - `37222997784`, latest available attempt `4`
   - `37222997736`, latest rerun attempt `6`
3. Railway validation service `nexy-validation` was pinned to product commit `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43` and a deployment was triggered:
   - Deployment: `68471115-106e-4576-ac43-232c0b69f453`
4. GitHub VS Code Web opened the product repository at `github.dev`/`vscode.dev`; it was a restricted browser workspace and exposed no verified runnable local terminal.
5. Shell clone through GitHub HTTPS was attempted and failed because the environment had no GitHub credential:
   `fatal: could not read Username for 'https://github.com'`.

## Observed results

### GitHub Actions

The rerun attempts completed as failures in seconds. The GitHub Actions run page annotations state that jobs were not started because recent account payments failed or the spending limit needs to be increased. Therefore these are infrastructure/account failures, not test assertions and not code-root-cause evidence.

### Railway

The exact-head Railway deployment `68471115-106e-4576-ac43-232c0b69f453` ended `SKIPPED`. It produced no deploy log and no test output. The deployment diagnosis retained a generic image-build failure context but did not provide executable test evidence. The existing service configuration contains the validation commands, but no command reached a verifiable result in this attempt.

## Integrity

- Product files changed: NO
- Product commit created: NO
- Regression test added: NO
- Production code changed: NO
- Exact-head RED result: NOT_OBTAINED
- Exact-head GREEN result: NOT_OBTAINED
- Full-suite result: NOT_OBTAINED
- Backend bypass through Repo Code Bridge: NO
- Fake pass or stale failure promoted to current proof: NO

## Ruling

Do not patch Product from the historical Railway failures or from the failed GitHub job conclusions. A valid TDD repair requires a runnable exact-head environment that produces a real failing assertion or type/build error first.

## Resume conditions

1. Restore GitHub Actions billing/spending capacity, or provide an authorized runnable exact-head runner.
2. Make Railway produce a non-SKIPPED deployment with readable build logs, or provide a credentialed local checkout.
3. Freeze the resulting product HEAD.
4. Add a regression test, observe RED, implement the minimal fix, run GREEN, then run all applicable gates.
5. Re-read the result into AI-CONTEXT/main with source blobs, commit SHA, workflow/deployment IDs, logs, and timestamps.
