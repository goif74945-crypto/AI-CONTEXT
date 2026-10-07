# NEXY Locked Builder Execution Command

SYSTEM: NEXY::SPEC-LOCKED-FULL-REPAIR-AND-VERIFIED-100-V2
MODE: EXECUTE_NOW / ENGINEERING / EVIDENCE_DRIVEN / FAIL_CLOSED / EXACT_HEAD_ONLY

## Objective

Repair `goif74945-crypto/NEXY.AI-` on branch `NEXY.ai` so every controlled requirement is implemented and proven against one exact product commit. The only acceptable release result is PASS_100 under the acceptance gate below. Until every gate passes, report BLOCKED_WITH_RESUME or FAILED.

## Authority

- Authoritative specification: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Required specification SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- Product repository: `goif74945-crypto/NEXY.AI-`
- Only product branch: `NEXY.ai`
- Coordination repository: `goif74945-crypto/AI-CONTEXT`
- Only coordination branch: `main`
- Frozen starting product HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- Frozen starting AI-CONTEXT HEAD: `80b76d987f1b5fbaa5cf81bd9ecfb4408e18970e`
- Starting audit matrix: `EVIDENCE/20261007-NEXY-FULL-SPEC-AUDIT-001.tsv`

## Hard preconditions

Before any code edit:

1. Re-query live runtime, repository catalog, product status, and AI-CONTEXT status.
2. Confirm product branch is exactly `NEXY.ai`; if not, stop.
3. Confirm product write and CI dispatch are actually ALLOW. If either is DENY/read-only, stop with BLOCKED and do not use a second backend to bypass the boundary.
4. Confirm the DOCX SHA-256 exactly matches the authority.
5. Read the DOCX from first through last paragraph. Reconcile P10970-P10981 release-signoff paragraphs separately from P12532-P12536 closing-design paragraphs.
6. Read the current audit report and matrix at the current AI-CONTEXT HEAD.
7. Freeze a new target product HEAD. Never mix evidence from another SHA.
8. Verify unique requirement IDs and preserve every row; never delete or merge rows to improve scores.

## Scope

In scope: product source, tests, workflows, and exact-head evidence on `NEXY.ai`; task/evidence/case/failure/ledger records on AI-CONTEXT `main`.

Out of scope: any other repository or branch, new product branches, force-push, production deployment without separate approval, rewriting the DOCX, deleting history, and any experimental change not required by the authority.

## Required repair order

### Phase A — authority and evidence integrity

Close AUTH-03, AUTH-11, EVID-01, EVID-02, EVID-03.

- Resolve every authority conflict by the DOCX precedence order; record both texts, winning authority, reason, source path, and target SHA.
- Replace stale current-head attestation with a fresh attestation for the new target SHA and clean tree.
- Regenerate all evidence records whose source blob, execution SHA, or timestamp is stale.
- Preserve superseded records as obsolete; do not edit history to make it look current.

### Phase B — build and static gates

Close CFG-04, VAL-04, ARCH-03, SCOPE-04.

- Add or repair regression tests before production changes.
- Run the real typecheck, lint, boundary, canonical-source, static-determinism, and build commands declared by the repository.
- Do not weaken assertions, skip jobs, add `continue-on-error` to required gates, add `as any` or `@ts-ignore`, or alter acceptance criteria.

### Phase C — runtime and pipeline

Close FSM-05, PIPE-07, API-08, AUTH-10, STORE-06, RBAC-04, OBS-05, QUEUE-06.

- Test real state transitions, freeze/recovery, pipeline sequencing, canonical API envelopes, auth abuse paths, durable storage/migration, RBAC denial, alarm emission, queue readiness, retries, idempotency, and worker behavior.
- Use deterministic fixtures and real code paths. Mocks are allowed only where the repository's existing test contract proves they are unavoidable and they must not replace production behavior.
- For each failing row: identify root cause, write a targeted regression test, run RED, make the minimal implementation fix, run GREEN, then run the full applicable suite.

### Phase D — UI and operational proof

Close UI-06, UI-07, STORE-07, GATE-04, GATE-05, GATE-06.

- Prove UI truth/pending/error/freeze states with real browser E2E.
- Prove mobile/responsive and low-resource behavior where required by the DOCX.
- Prove migration apply/rollback, object/blob behavior, deployment signoff, security signoff, engineering signoff, rollback verification, and monitoring verification.
- Do not call local-only or branch-only output release evidence.

### Phase E — experimental systems

Close EXP-05 and EXP-06.

- Keep experimental code outside the main vNEXT build unless the authority explicitly promotes it.
- Prove required experimental rows with real exact-head evidence.
- Do not use advisory or `continue-on-error` results as required proof.

### Phase F — DOCX paragraph reconciliation

- Record P10970-P10981 as release-runbook/signoff requirements.
- Record P12532-P12536 as remaining implementation/optimization/scaling/hardware work.
- If any additional normative paragraph is not represented in the controlled matrix, add a new unique row with source paragraph and reason. Do not suppress it.

## Atomic repair loop

For every non-VERIFIED row:

1. Read authoritative source and current product source at the target SHA.
2. Identify root cause and exact source paths.
3. Write a regression test first when the row is behavioral.
4. Run the new test and observe the expected RED failure.
5. Make the smallest spec-conforming implementation change.
6. Inspect the diff and forbidden-pattern scan.
7. Run targeted tests.
8. Run all applicable repository gates.
9. Run integration/E2E/security/negative tests required by the row.
10. Record command, exit code, environment, UTC time, target SHA, source blob SHA, workflow/run/job IDs, logs, artifacts, and reviewer result.
11. Re-audit the row. Only then change status to VERIFIED.

## Forbidden behavior

- No guessing, placeholder, fake pass, simulated hardware proof, invented API, fabricated workflow/run/log/artifact, or stale-head evidence.
- No deleting or merging rows, changing status names, weakening tests, hiding errors, `if:false`, new `skip`/`only`, new `as any`, new `@ts-ignore`, or required `continue-on-error`.
- No direct GitHub/raw API/backend bypass if the configured product gateway says read-only.
- No product write or CI dispatch when capability precondition is DENY.
- No release/deploy claim from a failed, skipped, pending, cancelled, neutral, missing, partial, branch-only, or local-only result.

## Exact-head evidence contract

Every VERIFIED row must include:

`requirement_id, system, status, authoritative_spec_sha256, target_product_head, exact source paths, immutable source blob proof, test command, workflow/run/job IDs, job result, log/artifact reference, UTC timestamp, environment/runtime, negative-test result when applicable, reviewer check, authority reason`.

All code, tests, workflows, logs, artifacts, attestations, and matrix rows used for PASS_100 must reference the same product HEAD.

## Acceptance gate

PASS_100 is permitted only if all are true:

- The controlled matrix contains every independently identified normative row; IDs are unique.
- VERIFIED equals the full controlled row count.
- PARTIAL, MISMATCH, NOT_VERIFIED, and BLOCKED equal zero.
- Every row has exact source mapping and semantic conformance.
- Targeted, unit, integration, API, auth/security, queue/storage, state-machine, negative/adversarial, and required browser/E2E tests pass.
- Required workflows pass on the same product SHA; no required job is skipped.
- Release attestation is fresh, clean-tree, exact-head, and independently readable.
- Evidence and matrix are written to AI-CONTEXT/main and read back at the new AI-CONTEXT HEAD.
- P10970-P10981 and P12532-P12536 are reconciled and evidenced.
- Rollback path, logs, artifacts, and signoffs are present and linked.
- No critical unknown remains.

## Mandatory stop conditions

Stop and report BLOCKED_WITH_RESUME if:

- product write or CI dispatch is DENY/read-only;
- product branch or target SHA is ambiguous;
- authoritative SHA mismatches;
- required workflow/log/artifact is missing;
- an evidence record points to another HEAD;
- a conflict cannot be resolved by authority;
- a required external service/hardware resource is unavailable;
- any security, permission, or integrity boundary would be bypassed.

## Final response schema

MODE:
STATUS:
TARGET_PRODUCT_HEAD:
AI_CONTEXT_HEAD:
SPEC_SHA256:
MATRIX_TOTAL:
VERIFIED:
PARTIAL:
MISMATCH:
NOT_VERIFIED:
BLOCKED:
CI_RUNS:
CHANGED_FILES:
EVIDENCE_FILES:
REMAINING_BLOCKERS:
VERDICT:

Allowed statuses: PASS_100, BLOCKED, BLOCKED_WITH_RESUME, FAILED.
