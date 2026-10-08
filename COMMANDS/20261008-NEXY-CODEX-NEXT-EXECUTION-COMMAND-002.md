# NEXY — Codex Next Execution Command

SYSTEM: NEXY::REMOTE-WRITE-EVIDENCE-INTEGRITY-CONTINUOUS-REPAIR-V1
MODEL TARGET: Codex / GPT-5.6-class engineering executor

MODE:
EXECUTE_NOW
ENGINEERING
EVIDENCE_DRIVEN
FAIL_CLOSED
NO_GUESS
NO_FAKE_PASS
CURRENT_HEAD_AWARE
MULTI_CHAT_SAFE
REMOTE_WRITE_ALLOWED
CONTINUOUS_CLOSURE

## 0. CONTINUE FROM YOUR LAST REPORT

Your last reported state was:

- TARGET_BRANCH: `NEXY.ai`
- START_HEAD = END_HEAD = `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- MATRIX: 98 rows = 71 VERIFIED / 15 PARTIAL / 5 MISMATCH / 7 NOT_VERIFIED
- AUDIT_COVERAGE: 100%
- COMPLETION: 78.0%
- CHANGED_FILES: none
- TESTS_EXECUTED: none
- LOCAL_BLOCKER: product repo not locally mounted / no authorized runner surface

Do NOT repeat that report and stop.

This command exists specifically to advance beyond that local-only blocker.

## 1. CORRECT THE STATE MODEL FIRST

Your prior output contains a contradiction:

- `INFRA_BLOCKED: 0`
- while also stating `no authorized runner surface was available`.

These cannot be treated as simultaneously equivalent states.

Immediately separate capability state into:

- `WRITE_CAPABILITY`
- `RUNNER_CAPABILITY`
- `BROWSER_E2E_CAPABILITY`
- `DEPLOY_CAPABILITY`
- `AI_CONTEXT_WRITE_CAPABILITY`

If no executable runner exists, set `RUNNER_CAPABILITY=UNAVAILABLE` or `BLOCKED` and classify only the rows that actually require executable proof as `INFRA_BLOCKED` or `CURRENT_NOT_VERIFIED` as justified by evidence.

Do not use `INFRA_BLOCKED=0` while simultaneously claiming runner unavailability unless you explicitly prove that no controlled row depends on that runner.

## 2. LIVE AUTHORITY / REPOSITORY FACTS TO RE-QUERY

Product repository:
`goif74945-crypto/NEXY.AI-`

Observed live branch topology at command creation:
- only branch: `NEXY.ai`

Observed HEAD:
`9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

Observed current GitHub repository permission from the connected GitHub surface:
- `pull=true`
- `push=true`

These are observations, not permanent assumptions.

Before every mutation:
1. re-query branch list,
2. confirm `NEXY.ai` still exists,
3. re-query exact HEAD,
4. re-query write permission if the tool exposes it,
5. compare actual HEAD to your expected HEAD,
6. inspect concurrent changes before writing.

Never create another branch.
Never recreate `NEXY-IGNIS`.
Never force-push.
Never overwrite unseen concurrent work.

## 3. AUTHORITATIVE SPEC

Authoritative file:
`แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`

Required SHA-256:
`b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`

AI-CONTEXT baseline matrix:
`EVIDENCE/20261007-NEXY-FULL-SPEC-AUDIT-001.tsv`

Matrix baseline:
- total 98
- VERIFIED 71
- PARTIAL 15
- MISMATCH 5
- NOT_VERIFIED 7

The matrix is a historical defect map, not automatic current truth.

## 4. AUTH-03 RULING

Do NOT treat `AUTH-03` as a normal source-code bug merely because the early prose says OTAC TTL 10–15 minutes while final DOC-C/source uses 5 minutes.

This is an authority/specification conflict.

Required behavior:
- preserve both source statements,
- identify the winning authority using the project's explicit authority ordering,
- record the conflict,
- do NOT alter product code solely to make the older prose win,
- do NOT rewrite the authoritative DOCX,
- do NOT falsely claim the conflict disappeared.

Move on to an executable repair target after recording the ruling.

## 5. FIRST CONCRETE REPAIR TARGET — REQUIRED

The first repair target is a current source-proven evidence-integrity defect:

File:
`scripts/current-head-attestation.ts`

Observed blob SHA at command creation:
`c255f43a3b07b05154cea5448e29b71b4d6f0b9a`

Current source hardcodes historical validation results such as:
- `npm run typecheck:backend` => `pass`
- targeted vitest => `pass`
- `npm test` => `pass`
- `npm run test:experimental` => `pass`
- cargo checks/tests => `pass`
- boundary/doc-c/build results => historical pass text
- browser_e2e => historical blocked text

Those results are embedded in the generator rather than produced by the current execution.

This means the producer can generate a file named `current-head-attestation.json` whose validation section appears evidentiary even when those tests were not executed for that generated attestation.

This is an evidence-integrity defect.

### Required repair semantics

Repair the producer, NOT merely the generated JSON.

After the repair:

1. `scripts/current-head-attestation.ts` MUST NOT contain static/hardcoded PASS claims for validation commands.

2. Validation claims may only enter the generated attestation from real execution results that are explicitly supplied by a trusted current-run mechanism and are bound to the same repository/branch/HEAD.

3. If no trustworthy same-run validation-result mechanism already exists in the repository, use the minimal fail-closed behavior:
   - emit no PASS validation claims,
   - represent validation as empty / NOT_RUN / unavailable using the existing schema style or the smallest compatible schema extension,
   - include an explicit blocker such as `CURRENT_HEAD_VALIDATION_NOT_EXECUTED`,
   - keep `release_authorized=false`,
   - keep `deploy_authorized=false`.

4. `head`, `branch`, repository identity, and dirty-tree state must continue to come from the actual Git repository state, not from historical JSON.

5. Never use `generated_at` alone as freshness proof.

6. Do NOT read old `evidence/current-head-attestation.json` and copy its validation PASS results into the new attestation.

7. Preserve historical evidence provenance. Do NOT hand-edit the historical JSON to pretend those tests ran now.

8. Do NOT promote `AUTH-11` / `EVID-01` to CURRENT_VERIFIED merely because the producer source is fixed. Source repair without execution remains PARTIAL until fresh exact-head generation/validation evidence exists.

## 6. REGRESSION GUARD — REQUIRED

Add the smallest regression test consistent with the repository's existing Vitest/contract structure.

The regression test must prove at source/behavior level that the attestation producer cannot manufacture validation PASS claims without explicitly supplied current-run validation evidence.

At minimum cover:

- default/no-results path cannot contain fabricated PASS entries,
- release/deploy remain false without valid current-head proof,
- stale/historical validation is not silently accepted as current,
- mismatched HEAD validation input is rejected or cannot be promoted,
- repository/branch/HEAD identity remains explicit.

Do not add a new dependency unless unavoidable.
Do not weaken an existing test.
Do not create a test that only asserts a cosmetic string while leaving the false-PASS behavior possible.

If a small refactor is required to make the producer testable, keep it tightly limited to this producer.

## 7. REMOTE WRITE IS A VALID EXECUTION PATH

A local checkout/mount is NOT a prerequisite for this repair if a current authorized remote GitHub write surface exists.

Use the authorized GitHub repository write surface available to you.

Prefer one atomic commit containing:
- producer fix,
- regression test.

If the available API cannot create an atomic multi-file commit:
- re-read HEAD before each write,
- make the minimum safe sequence,
- read back each committed file,
- never force-update refs.

If current GitHub write permission is actually denied when you attempt the write, record the exact tool result and classify `WRITE_CAPABILITY=BLOCKED`.

Do not substitute “repository not locally mounted” for a write-permission check.

## 8. RUNNER-ABSENT SEMANTICS

If no runner exists after the source/test commit:

DO NOT claim:
- test PASS,
- runtime VERIFIED,
- EVID-01 VERIFIED,
- AUTH-11 VERIFIED,
- project completion increase.

Instead report:
- source repair committed,
- regression test authored,
- test execution = NOT_EXECUTED / INFRA_BLOCKED,
- affected row remains CURRENT_PARTIAL or CURRENT_NOT_VERIFIED as justified.

The absence of a runner blocks execution proof, not the safe source-integrity repair itself.

## 9. ROOT-CAUSE-FIRST / NO COSMETIC EVIDENCE PATCH

Forbidden as the first fix:
- manually replacing `head` inside `evidence/current-head-attestation.json`,
- manually changing validation results from historical text to new PASS text,
- regenerating the attestation and calling it current while validation was not run,
- altering timestamps to create apparent freshness.

Fix the producer first.

## 10. SECONDARY TARGET AFTER FIRST COMMIT

After the first repair is written and read back, continue in the SAME run if another safe READY node exists.

Next inspect source-proven stale-evidence replay risks, especially:
- `scripts/phase-f-audit.ts`
- `scripts/regen-evidence.ts`
- `scripts/check-phase-f.ts`

Only mutate them if current source directly confirms a producer/replay defect.

Do not assume the historical AI-CONTEXT description is still correct without reading current source.

If confirmed, repair the smallest producer-integrity issue that allows historical evidence to masquerade as current-head evidence.

If not confirmed, leave it unchanged and continue to the next READY row.

## 11. MULTI-CHAT CONCURRENCY

Other chats may write concurrently.

Before each mutation:
- read current HEAD,
- compare with expected HEAD.

If drift exists:
- inspect changed files/commits,
- determine whether your target files changed,
- recompute the patch,
- do not overwrite concurrent work,
- do not reset or force-update.

## 12. FORBIDDEN BEHAVIOR

DO NOT:
- create/delete/rename branches,
- modify `NEXY.ai` branch protection/settings/secrets/billing/permissions,
- fabricate runner availability,
- fabricate tests,
- fabricate workflow/log/artifact IDs,
- use stale HEAD evidence as current proof,
- weaken tests,
- add required `continue-on-error`,
- add `skip`/`only` to manufacture pass,
- use `as any` / `@ts-ignore` to hide the defect,
- swallow attestation/evidence errors,
- edit the DOCX,
- raise completion percentage without current row evidence,
- claim a test was run when it was merely authored.

## 13. VALIDATION / READ-BACK

After every product write:

1. re-query `NEXY.ai` HEAD,
2. fetch each changed file from the new HEAD,
3. verify expected content exists,
4. verify no unrelated file changed in your commit,
5. record exact commit SHA,
6. record test status honestly.

If a runner becomes available:
- run the targeted regression first,
- then applicable contract/type/static gates,
- bind results to the exact HEAD.

If no runner becomes available:
- do not fake execution,
- continue safe source-proven repair nodes where possible.

## 14. AI-CONTEXT WRITE-BACK

Coordination repository:
`goif74945-crypto/AI-CONTEXT`

Branch:
`main`

Write sanitized records for this cycle under appropriate:
- TASKS/
- EVIDENCE/
- LEDGER/
- FAILURES/ if a path fails
- CASES/ if an integrity incident is identified

Record:
- starting product HEAD,
- ending product HEAD,
- exact changed files,
- commit SHA,
- current capability states,
- tests authored,
- tests actually executed,
- actual results,
- affected requirement classifications,
- unresolved blockers,
- next READY action.

Read back AI-CONTEXT writes and record the new AI-CONTEXT HEAD.

AI-CONTEXT write failure is local; it must not erase already valid product work.

## 15. SCORING LAW

Maintain separately:

AUDIT_COVERAGE = current-classified requirements / controlled requirements

COMPLETION = CURRENT_VERIFIED / (CURRENT_VERIFIED + CURRENT_PARTIAL + CURRENT_MISMATCH)

Do not put CURRENT_NOT_VERIFIED or INFRA_BLOCKED into the completion denominator unless the controlling audit method explicitly changes.

Do not promote completion because a source patch was committed but unexecuted.

## 16. SUCCESS CONDITION FOR THIS EXECUTION CYCLE

This cycle is successful if, at minimum:

1. live branch/HEAD/write state is re-queried,
2. `scripts/current-head-attestation.ts` defect is confirmed against current source,
3. producer source is minimally repaired through an authorized remote write path,
4. a regression guard is added,
5. changes are committed to `NEXY.ai`,
6. commit/files are read back from GitHub,
7. test execution status is reported truthfully,
8. affected matrix rows are reclassified without fake PASS,
9. AI-CONTEXT is updated/read back when available,
10. execution continues to another READY node if one exists.

If write permission is denied, report the exact denial and produce the exact patch/diff required; do not fall back to “repo not mounted” as the explanation.

## 17. OUTPUT FORMAT

MODE:
STATUS:
TARGET_BRANCH:
START_HEAD:
END_HEAD:
WRITE_CAPABILITY:
RUNNER_CAPABILITY:
BROWSER_E2E_CAPABILITY:
DEPLOY_CAPABILITY:
AI_CONTEXT_WRITE_CAPABILITY:
AI_CONTEXT_HEAD:
SPEC_SHA256_STATUS:
MATRIX_SOURCE:
CURRENT_MATRIX_TOTAL:
CURRENT_VERIFIED:
CURRENT_PARTIAL:
CURRENT_MISMATCH:
CURRENT_NOT_VERIFIED:
INFRA_BLOCKED_ROWS:
AUDIT_COVERAGE:
COMPLETION:
ROWS_TOUCHED:
ROOT_CAUSE_CONFIRMED:
CHANGED_FILES:
COMMITS:
TESTS_AUTHORED:
TESTS_EXECUTED:
TEST_RESULTS:
READBACK_PROOF:
LOCAL_BLOCKERS:
NEXT_READY_ACTION:
EVIDENCE_WRITTEN:
VERDICT:

Allowed STATUS:
WORKING
PARTIAL
BLOCKED_LOCAL
FAILED
VERIFIED_WITH_LIMITS
PASS_100

## 18. BEGIN NOW

Do not acknowledge this command and stop.

Re-query live `NEXY.ai` branch/HEAD/write permission.

Read current `scripts/current-head-attestation.ts`.

Confirm or falsify the hardcoded-validation defect from current source.

If confirmed and write capability exists, perform the producer-integrity repair plus regression guard through the authorized remote GitHub write surface in this same run.

Read back the new HEAD and changed files.

Then continue to the next safe READY repair node instead of stopping merely because no local runner exists.