# NEXY.AI — Current Context Status

## Status

**PARTIAL / FREEZE — EXACT-HEAD LOCAL GATES PASS; GITHUB RUNNER BLOCKED / RELEASE NON_DEPLOYABLE**

This is the current-head overlay. It supersedes stale current-looking claims that point to another branch, commit, or CI run. Historical audits remain historical and are not deleted.

## Authority snapshot

- Source: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx.
- Source SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
- DOC-C is the current vNEXT build specification.
- DOC-D is product design only where DOC-C supports it.
- Final Architecture is conceptual architecture.
- DOC-E is evidence/proof only; source prose or file presence is not deployment proof.

## Exact implementation and evidence observation — 2026-09-29

- repository: goif74945-crypto/NEXY.AI-
- branch: NEXY.ai
- tested SHA: ab471d1e2705d6010afdcdbb0a7baf08132de47d
- tested tree: 298468ca539306c2c581248331f082b908400605
- current branch HEAD after evidence commit: ba33c8fdcd0ea56729835bf06b43500ec5b21f4e
- evidence commit: test: add exact-head evidence for ab471d1
- workflow commit: 10985349e33c1aa0fed8ce20be557ee3509b1509
- exact-head evidence directory: evidence/exact-head/ab471d1e2705d6010afdcdbb0a7baf08132de47d/
- the local run checked out the tested SHA in a detached worktree and recorded a clean checkout before dependency setup.
- attestation.json binds the tested SHA/tree, gate results, log paths and SHA-256 manifest; the remote copy reports overall_pass=true.

## Current validation truth

The exact-head local evidence run completed with all recorded gate exit codes equal to 0:

- npm test: 113 test files passed; 835 tests passed.
- typecheck, lint and DOC-C check: PASS.
- coverage run and coverage check: PASS.
- coverage snapshot (lines / statements / functions / branches): API 93.44 / 92.09 / 97.20 / 85.01; core 95.73 / 95.93 / 94.44 / 91.23; law 100 / 94.87 / 100 / 96.83; judge 97.39 / 96.27 / 100 / 94.01.
- web build: PASS; the only recorded caveat is an optional @valkey/valkey-glide resolution warning.
- Phase-F check: PASS, with the recorded release seal remaining NON_DEPLOYABLE.
- experimental suite: 59 files; 574 passed and 1 skipped.
- Rust core-kernel tests: 243 passed, 0 failed, 1 ignored documentation test.
- production dependency audit: 0 vulnerabilities at high-or-higher severity.

The repo-traceable evidence can be independently checked from the evidence directory with sha256sum -c sha256sums.txt. The committed README, exit-codes.tsv, logs/, attestation.json, tested-sha.txt and tested-tree.txt are the proof record for this exact SHA.

## GitHub Actions truth

- workflow: .github/workflows/exact-head-evidence.yml
- run: 36524026445 (https://github.com/goif74945-crypto/NEXY.AI-/actions/runs/36524026445)
- run head/workflow commit: 10985349e33c1aa0fed8ce20be557ee3509b1509
- event/branch: push / NEXY.ai
- conclusion: failure before job start.
- blocker: GitHub account billing/spending-limit guard prevented the runner from starting; this is not a code-level test failure.
- observed steps: 0; GitHub runner logs: none; GitHub artifact: none.

The workflow is intentionally retained and asserts the checkout SHA, tree and clean checkout before running the same gates. It can be rerun after the billing blocker is cleared. Until then, the committed local exact-head evidence is the available reproducible proof, not a GitHub runner attestation.

## Current code changes represented by this validation

- PostgreSQL advisory-lock callers use executeRaw for lock statements, avoiding Prisma result deserialization failures during clean boot.
- The web layout separates server nonce/CSP handling from the client system-state/navigation wrapper; production browser loading was revalidated.
- Directive UI labels and browser route assertions use the canonical directive identifier path.
- A system-state persistence contract test and the required raw-SQL test mocks are included.
- The exact-head workflow and committed evidence package make the tested SHA/tree explicit and independently checkable.

## Specification and release boundary

| Area | Current fact | Status |
|---|---|---|
| Exact-head automated gates | Local checkout of ab471d1e2705d6010afdcdbb0a7baf08132de47d passed every recorded gate. | PASS (local) |
| Repo traceability | Evidence, logs, manifest and attestation are committed on origin/NEXY.ai at ba33c8fdcd0ea56729835bf06b43500ec5b21f4e. | PASS |
| GitHub runner proof | Run 36524026445 was blocked before the first job step by billing; no artifact was produced. | BLOCKED |
| Rollback/database proof | The validation host did not have psql, so rollback was not independently executed or proven. | NOT VERIFIED |
| DOC-C/D full parity | These gates do not constitute a complete design/specification crosswalk. No 100% parity claim is made by this file. | NOT PROVEN |
| Release/deploy authorization | Phase-F records NON_DEPLOYABLE and GitHub attestation is unavailable. | BLOCKED |

Previous static findings and historical DOC-E records are retained as lineage. They must be revalidated against the tested SHA before being called resolved or current. Passing local tests does not, by itself, prove full DOC-C/D design alignment or authorize deployment.

## Decision

Source alignment and release readiness remain PARTIAL/BLOCKED. The exact tested SHA has strong local, repo-traceable gate evidence, but GitHub runner attestation is blocked by account billing, rollback is not verified, and full specification parity is not established. Do not promote or deploy until the billing blocker is cleared and the remaining current-head DOC-C/D, rollback, security and release-authority checks are independently observed.

## Historical boundary

Older branch/head, Railway/browser, coverage and repair-pass claims remain preserved in historical audit and evidence files. They must not be read as proof for the current NEXY.ai head.


## Latest direct repository inspection — 2026-09-29 (Asia/Bangkok)

This addendum records a read-only inspection of the Codespaces checkout after the exact-head evidence commit. It does not replace the exact-head test record above.

- observed repository HEAD: ba33c8fdcd0ea56729835bf06b43500ec5b21f4e
- observed tree: 8a3ae328c1956c661bc2b1561de1a791a7856a7e
- observed branch: NEXY.ai
- observed worktree: CLEAN
- tracked API route files under apps/web/app/api: 37
- DOC-D required component files found: 14/14; grep also found references from the web app/pages/components
- migration rollback files found: 23
- static migration check found event_log_append_only in the up/down migration pair and audit_log_append_only in the up/down migration pair
- the trigger result is static repository evidence only; live database rollback/trigger execution remains NOT VERIFIED because the validation host has no psql

### Open implementation finding

- DOC-D S4 lists a SAVE DRAFT action. In the current apps/web/app/directives/new/page.tsx, the button currently only navigates to /directives; no draft persistence or draft endpoint is implemented. This is an OPEN UI-behavior gap, not a passing claim.
- The current DOC-C/D crosswalk is therefore still NOT PROVEN. The 100% parity claim remains withheld until the open behavior is implemented and re-tested on a new exact target SHA.
- The existing local test/evidence numbers above are bound to tested SHA ab471d1e2705d6010afdcdbb0a7baf08132de47d, not to an untested application-code change at the newer evidence HEAD.
