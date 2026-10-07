# Task — NEXY VS Code and Railway Diagnostic

TASK_ID: 20261007-NEXY-RAILWAY-DIAGNOSTIC-005
MODE: EXECUTE_NOW / ENGINEERING / EVIDENCE_DRIVEN / FAIL_CLOSED
STATUS: BLOCKED_WITH_RESUME
DATE_UTC: 2026-10-07T16:19:21Z

## User action

The user instructed execution through GitHub VS Code and Railway to run tests and repair NEXY to the authoritative specification.

## Authority

- Product repository: `goif74945-crypto/NEXY.AI-`
- Product branch: `NEXY.ai`
- Product HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- AI-CONTEXT branch: `main`
- AI-CONTEXT parent HEAD: `8b9e258b2356ed7d07ecea66cc48a5e2bf4d1c40`
- DOCX SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`

## Read-only tools used

- GitHub VS Code URL was returned for `github.dev` at the exact product HEAD. It returned a browser URL, not a desktop process; authentication is required in the VS Code browser session.
- WixREADME was read because the Wix plugin was selected. No Wix site or Wix app execution target was provided; no Wix mutation was performed.
- Railway read-only inventory and logs were inspected for the existing project `NEXY Validation R2`.

## Railway evidence

- Project ID: `01537473-6a6d-42a0-856f-40d8a4e6a712`.
- `nexy-validation` is connected to `NEXY.ai), but its latest failed deployment `a4e4f0a2-982c-47cd-b1cf-12ba1b120ef0` used commit `6769b725e46753ce5af58a972c005894065f38da`, not the current target HEAD.
- That deployment failed at image build during `npm run test:contract`: 2 test files failed and 112 passed; the reported contract failure was `tests/integration/game-canonical-order.spec.ts imports Phase F but is not isolated`.
- `nexy-validation-branch` is connected to the old `NEXY.AI-Test-AI` branch. Its latest failed deployment used commit `dd9e691e346e97701877ad6e2e5ff5642ca1b068`; coverage reported 3 failed tests, 179/180 files passed, and 1232/1235 tests passed.

## Result

These Railway logs are historical diagnostics, not exact-head proof for `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`. No new Railway deployment was triggered because the authorized product gateway's actual CI operation returned `REPOSITORY_READ_ONLY`; triggering Railway as a substitute would bypass the locked CI boundary.

No Product source, test, workflow, commit, or exact-head CI result was changed or created.

## Resume

After the Repo Code Bridge operation gate is consistent and permits authorized write plus CI dispatch, freeze a new product HEAD, open VS Code for that branch, write a regression test first, run RED, implement the minimal fix, run GREEN and the full suite, then run exact-head CI. Railway may be used for a fresh exact-head deployment only after that gate is cleared.
