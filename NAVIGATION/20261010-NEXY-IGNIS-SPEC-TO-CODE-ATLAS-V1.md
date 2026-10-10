# NEXY-IGNIS authoritative spec → code navigation atlas (read-first)

**Atlas version:** 2026-10-10 / SNAPSHOT ONLY. **Source spec SHA-256:** `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7` (byte-verified original DOCX). **Source product HEAD:** `58b1200bd61b867e917057d0019eea78ea9f6b2a` (recheck live). **Spec P anchors:** 1-based `python-docx Document.paragraphs` sequence including empty paragraphs; P00001 corresponds to `paragraphs[0]`. **Git tree:** 1,092 entries, 889 tracked blobs, `truncated=false` at this HEAD.

**Status:** NAVIGATION ONLY / PATH_EXISTENCE_VERIFIED / BEHAVIOR_NOT_VERIFIED. Atlas associates candidate source and tests with spec anchors. It never claims an implementation meets the spec. A future HEAD requires path revalidation, diff and proof refresh. Raw 2.1 MB DOCX is NOT copied into this public control repository; obtain the actual byte-identical source through authorized attachments/owner workspace and hash it before any acceptance decision.

**Authority navigation:** P09837–P09845 defines DOC-A vision, DOC-B law, DOC-C build, DOC-D supported product design, DOC-E deployment proof. P09846–P09885 DOC-B; P09886–P10499 DOC-C; P10500–P10722 DOC-D; P10723–P10835 storage supplement; P10836–P10916 auth hardening; P10917–P10999 DOC-E. Cross references outside these ranges are not automatically DOC-C build obligations. Historical broader scope fence P09644–P09689, including exclusions/deferred features, must be reconciled against final DOC-C scope. The map is an accelerator, not an exhaustive atomic requirement register.

## Quick access for every new Codex session and cooperating chat
1. Read `COMMANDS/20261010-NEXY-CODEX-SPEC-EXACT-LONG-RUN-ENGINEERING-V5.md` and the newer map-aware Codex command.
2. Read `POLICIES/20261010-NEXY-EVIDENCE-GATED-CONTINUOUS-UPDATE-V1.md` and product `AGENTS.md` at live HEAD.
3. Verify SHA of original DOCX; retrieve exact P anchors below and crosswalk to 143 historical checkpoints in `COMMANDS/20261009-NEXY-GPT6-SOL-143-ACCEPTANCE-REGISTER-V4.md`. Do not mistake 143 as exhaustive.
4. Resolve paths against current `git ls-files` and revision-bound Git tree. Never treat 'found' as tested.
5. Update run-specific ledger and append new verified evidence into `AI-CONTEXT/EVIDENCE`, avoid overwriting peer records; only evidence-backed product changes on branch `NEXY.ai`.

**Rows:** 88 locator groups, including 12 canonical API routes, 12 design screens, 14 canonical components, 12 DOC-E deliverables. Product Git tree matched 88 rows with all code candidate paths present; 0 code-path hints missing, 0 test-path hints missing. This count is path-hint validity, NOT spec coverage or functional pass.

## Spec-to-source route map
| Key | Authority anchor | Spec topic | Source candidates (existing at frozen HEAD) | Test/proof candidates | Notes |
|---|---|---|---|---|---|
| AUTHORITY | P9837-P9845 | DOC-A/B/C/D/E authority hierarchy | `AGENTS.md`, `README.md` | `tests/contract/scope-boundary.test.ts` | Spec DOCX owns authority; README is not authoritative |
| B-IDENTITY | P9846-P9863 | DOC-B identity and authority lock | `packages/law/precheck.ts`, `packages/core/vnext-state-matrix.ts` | `tests/contract/state-matrix.test.ts` | DOC-B system law |
| B-FREEZE | P9864-P9885 | DOC-B output/freeze law | `packages/law/freeze.ts`, `packages/api/canonical.ts` | `tests/integration/freeze-all-causes.spec.ts` | Check semantics at exact HEAD |
| C-SCOPE | P9886-P9909 | vNEXT included/excluded scope | `config/experimental-scope.ts`, `scripts/check-phase-f.ts` | `tests/contract/scope-boundary.test.ts` | Feature presence ≠ included requirement; explicit exclusions must remain isolated |
| C-DEFAULTS | P9910-P9949 | 26 canonical numeric defaults | `packages/api/vnext-config.ts`, `packages/config/runtime-config.ts` | `tests/contract/ex017-config-defaults.test.ts`, `tests/contract/vnext-defaults.test.ts` | Compare exact values and every consumer, not only exported constants |
| C-TYPES | P9950-P9994 | Statuses/states/error codes | `packages/contracts/state.ts`, `packages/contracts/errors.ts` | `tests/contract/ex017-wire-vocabulary.test.ts` | Check semantics at exact HEAD |
| C-ENVELOPE | P9995-P10013 | SystemEnvelope, audit and error payloads | `packages/contracts/envelope.ts`, `packages/api/canonical.ts` | `tests/contract/envelope.test.ts` | Check semantics at exact HEAD |
| C-RELEASE-RESULT | P10014-P10025 | Release policy result contract | `packages/contracts/release-policy.ts`, `packages/orch-core/release-policy.ts` | `tests/contract/release-spine.test.ts` | Check semantics at exact HEAD |
| C-API-LAW | P10026-P10038 | Envelope/auth/RBAC/CSRF/idempotency/audit/retries | `packages/validation/api.schema.ts`, `packages/api/canonical.ts` | `tests/contract/canonical-api.test.ts` | Check semantics at exact HEAD |
| C-API01 | P10039-P10070 | POST /api/auth/request-otac | `apps/web/app/api/auth/request-otac/route.ts` | `tests/integration/auth/request-otac.spec.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API02 | P10071-P10105 | POST /api/auth/verify-otac | `apps/web/app/api/auth/verify-otac/route.ts` | `tests/integration/auth/verify-otac.spec.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API03 | P10106-P10127 | GET /api/session/me | `apps/web/app/api/session/me/route.ts` | `tests/contract/canonical-api.test.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API04 | P10128-P10152 | POST /api/auth/logout | `apps/web/app/api/auth/logout/route.ts` | `tests/integration/auth/logout.spec.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API05 | P10153-P10202 | POST /api/directives | `apps/web/app/api/directives/route.ts` | `tests/integration/directives/create.spec.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API06 | P10203-P10221 | GET /api/directives/:id | `apps/web/app/api/directives/[id]/route.ts` | `tests/integration/directives/read-auth.spec.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API07 | P10222-P10242 | GET /api/runs/:id | `apps/web/app/api/runs/[id]/route.ts` | `tests/contract/canonical-api.test.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API08 | P10243-P10268 | POST /api/freeze/recover | `apps/web/app/api/freeze/recover/route.ts` | `tests/integration/freeze/recover.spec.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API09 | P10269-P10301 | POST /api/vault/commit | `apps/web/app/api/vault/commit/route.ts` | `tests/integration/vault/commit.spec.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API10 | P10302-P10330 | GET /api/artifacts/:id/revisions | `apps/web/app/api/artifacts/[id]/revisions/route.ts` | `tests/contract/canonical-api.test.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API11 | P10331-P10340 | GET /api/incidents/:id | `apps/web/app/api/incidents/[id]/route.ts` | `tests/contract/incident-semantics.test.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-API12 | P10341-P10352 | GET /api/audit-logs | `apps/web/app/api/audit-logs/route.ts` | `tests/e2e/audit-trail.spec.ts` | Endpoint inventory candidate; verify handler -> service -> DB/worker & negative runtime |
| C-FSM-EVENT | P10353-P10367 | Event vocabulary | `packages/core/vnext-state-matrix.ts` | `tests/contract/state-matrix.test.ts` | Check semantics at exact HEAD |
| C-FSM-MATRIX | P10368-P10452 | State/event transition matrix | `packages/core/vnext-state-matrix.ts`, `core-kernel/src/kernel/vnext_matrix.rs` | `tests/contract/state-matrix.test.ts` | Check semantics at exact HEAD |
| C-ILLEGAL | P10453-P10469 | Illegal event denial | `packages/law/freeze.ts`, `packages/core/vnext-state-matrix.ts` | `tests/contract/fatal-state-law.test.ts` | Check semantics at exact HEAD |
| C-OWNER | P10470-P10485 | Owner actions and rights | `packages/api/owner-recovery.ts`, `packages/api/owner-cancel.ts` | `tests/contract/owner-role-management.test.ts` | Check semantics at exact HEAD |
| C-TIMEOUT | P10486-P10493 | Timeout behavior | `packages/swarm/pipeline.ts`, `packages/queue/workers.ts` | `tests/contract/swarm-timeouts.test.ts` | Check semantics at exact HEAD |
| C-INCIDENT | P10494-P10499 | EventLog, primary/secondary incident and audit linkage | `packages/obs/incidents.ts`, `packages/obs/event-log.ts`, `packages/obs/audit-log.ts` | `tests/contract/pipeline-failure-incident-linkage.test.ts` | Check semantics at exact HEAD |
| D-S1 | P10506-P10509 | Front Door | `apps/web/app/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S2 | P10510-P10513 | OTAC Verify | `apps/web/app/login/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S3 | P10514-P10517 | Home / Front | `apps/web/app/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S4 | P10518-P10521 | Directive Create | `apps/web/app/directives/new/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S5 | P10522-P10525 | Directive Detail | `apps/web/app/directives/[id]/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S6 | P10526-P10529 | Pipeline Run Detail | `apps/web/app/runs/[id]/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S7 | P10530-P10533 | Freeze Incident | `apps/web/app/incidents/[id]/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S8 | P10534-P10537 | Artifact List | `apps/web/app/vault/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S9 | P10538-P10541 | Revision History | `apps/web/app/vault/[id]/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S10 | P10542-P10545 | Audit Viewer | `apps/web/app/audit/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S11 | P10546-P10549 | Owner Controls | `apps/web/app/owner/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-S12 | P10550-P10553 | I-Don't-Know Mode | `apps/web/app/unknown/page.tsx` | `tests/browser/critical-flows.spec.mjs` | Screen candidate only; verify CTA, permission and real backend state |
| D-LAYOUT | P10554-P10580 | Per-screen layout contract | `apps/web/app/layout.tsx`, `apps/web/components/LayoutInner.tsx` | `tests/contract/doc-d-actions.test.ts` | Check semantics at exact HEAD |
| D-COMP01 | P10583-P10583 | StatusChip | `apps/web/components/StatusChip.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP02 | P10584-P10584 | ModeTabs | `apps/web/components/ModeTabs.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP03 | P10585-P10585 | DirectiveInput | `apps/web/components/DirectiveInput.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP04 | P10586-P10586 | ConstraintPanel | `apps/web/components/ConstraintPanel.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP05 | P10587-P10587 | SubmitButton | `apps/web/components/SubmitButton.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP06 | P10588-P10588 | FreezeBanner | `apps/web/components/FreezeBanner.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP07 | P10589-P10589 | IncidentCard | `apps/web/components/IncidentCard.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP08 | P10590-P10590 | RevisionTable | `apps/web/components/RevisionTable.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP09 | P10591-P10591 | AuditTable | `apps/web/components/AuditTable.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP10 | P10592-P10592 | EmptyStateCard | `apps/web/components/EmptyStateCard.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP11 | P10593-P10593 | PermissionGate | `apps/web/components/PermissionGate.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP12 | P10594-P10594 | OwnerActionBar | `apps/web/components/OwnerActionBar.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP13 | P10595-P10595 | LoadingSkeleton | `apps/web/components/LoadingSkeleton.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-COMP14 | P10596-P10596 | TrustExplainer | `apps/web/components/TrustExplainer.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Component name exists; interactive behavior not assumed |
| D-TABLES | P10597-P10616 | Table definitions | `apps/web/components/RevisionTable.tsx`, `apps/web/components/AuditTable.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Check semantics at exact HEAD |
| D-FORMS | P10617-P10649 | Form field contract | `apps/web/components/DirectiveInput.tsx`, `apps/web/components/OtacLoginForm.tsx` | `tests/contract/doc-d-validation-copy.test.ts` | Check semantics at exact HEAD |
| D-VALIDATION | P10650-P10659 | Validation messages | `packages/validation/directive.schema.ts`, `apps/web/components/DirectiveInput.tsx` | `tests/contract/doc-d-validation-copy.test.ts` | Check semantics at exact HEAD |
| D-VISIBILITY | P10660-P10684 | Permission matrix | `apps/web/components/PermissionGate.tsx`, `apps/web/lib/mode-guard.ts` | `tests/contract/ui-truth-boundary.test.ts` | Check semantics at exact HEAD |
| D-RESPONSIVE | P10685-P10696 | Mobile/desktop | `apps/web/app/globals.css`, `apps/web/app/layout.tsx` | `tests/browser/critical-flows.spec.mjs` | Check semantics at exact HEAD |
| D-LOADING | P10697-P10701 | Loading skeleton | `apps/web/components/LoadingSkeleton.tsx` | `tests/contract/doc-d-component-inventory.test.ts` | Check semantics at exact HEAD |
| D-EMPTY | P10702-P10708 | Empty state | `apps/web/components/EmptyStateCard.tsx` | `tests/contract/doc-d-validation-copy.test.ts` | Check semantics at exact HEAD |
| D-FIRST | P10709-P10715 | First session walkthrough | `apps/web/components/TrustExplainer.tsx` | `tests/browser/critical-flows.spec.mjs` | Check semantics at exact HEAD |
| D-TRUST | P10716-P10722 | Trust-building loop | `apps/web/components/TrustExplainer.tsx` | `tests/contract/ui-truth-boundary.test.ts` | Check semantics at exact HEAD |
| ST-ENUM | P10723-P10729 | Storage enum | `prisma/schema.prisma` | `tests/contract/raw-sql-schema-alignment.test.ts` | Supplement requires DOC-C dependency determination |
| ST-UNIQUE | P10730-P10738 | Unique constraints | `prisma/schema.prisma` | `tests/contract/storage-fk-contract.test.ts` | Check semantics at exact HEAD |
| ST-FK | P10739-P10747 | FK and cascade policies | `prisma/schema.prisma` | `tests/contract/storage-fk-contract.test.ts` | Check semantics at exact HEAD |
| ST-SOFT | P10748-P10781 | Soft delete | `packages/storage/soft-delete.ts` | `tests/contract/storage-soft-delete.test.ts` | Check semantics at exact HEAD |
| ST-REV | P10782-P10798 | Versioning and atomicity | `packages/vault/versioning.ts`, `packages/vault/integrity.ts` | `tests/contract/vault-revision-monotonic.test.ts` | Check semantics at exact HEAD |
| ST-ARCHIVE | P10799-P10817 | Restore, blob retention and archival | `packages/storage/lifecycle.ts`, `packages/api/cold-snapshot.ts` | `tests/contract/cold-archive-snapshot.test.ts` | Check semantics at exact HEAD |
| ST-QUERY | P10818-P10835 | Index and query patterns | `packages/storage/query-patterns.ts`, `prisma/schema.prisma` | `tests/contract/storage-query-patterns.test.ts` | Check semantics at exact HEAD |
| AUTH-SESSION | P10836-P10852 | Auth classification, invalidation and session limits | `packages/auth/session.ts`, `packages/auth/device-binding.ts` | `tests/contract/auth-fail-closed-boundary.test.ts` | Check semantics at exact HEAD |
| AUTH-OTAC | P10853-P10864 | OTAC replay and brute force | `packages/auth/otac.ts`, `packages/auth/security-runtime.ts` | `tests/integration/auth/rapid-retry-abuse.spec.ts` | Check semantics at exact HEAD |
| AUTH-COOKIE | P10865-P10883 | Metadata and cookie renewal | `packages/auth/session.ts`, `packages/api/session-refresh.ts` | `tests/integration/auth/session-refresh.spec.ts` | Check semantics at exact HEAD |
| AUTH-AUDIT | P10884-P10916 | Auth security log and escalation | `packages/auth/security-incident.ts`, `packages/obs/audit-log.ts` | `tests/contract/auth-security-incident.test.ts` | Check semantics at exact HEAD |
| E-LAW | P10917-P10924 | DOC-E evidence and deploy gate | `scripts/doc-e/verify-doc-e.ts` | `tests/contract/doc-e-verifier.test.ts` | Evidence presence alone is not deployment authorization |
| E1 | P10925-P10926 | DOC-E E1: Contract report | `docs/evidence/current/E01-contract-test-report.md` | `tests/contract/doc-e-evidence.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E2 | P10927-P10928 | DOC-E E2: API schema | `docs/evidence/current/E02-api-schema-snapshot.md` | `tests/contract/doc-e-api-schema-snapshot.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E3 | P10929-P10930 | DOC-E E3: Migration+rollback | `docs/evidence/current/E03-migration-roundtrip.md` | `tests/contract/doc-e-e3-migration-roundtrip.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E4 | P10931-P10932 | DOC-E E4: FSM | `docs/evidence/current/E04-state-machine.md` | `tests/contract/state-matrix.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E5 | P10933-P10934 | DOC-E E5: RBAC | `docs/evidence/current/E05-rbac-tests.md` | `tests/contract/canonical-api.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E6 | P10935-P10936 | DOC-E E6: Auth abuse | `docs/evidence/current/E06-auth-abuse.md` | `tests/integration/auth/rapid-retry-abuse.spec.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E7 | P10937-P10938 | DOC-E E7: Queue worker | `docs/evidence/current/E07-queue-worker-readiness.md` | `tests/contract/doc-e-e7-e8-evidence.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E8 | P10939-P10940 | DOC-E E8: Observability | `docs/evidence/current/E08-observability-alarm.md` | `tests/contract/observability-alarm-wiring.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E9 | P10941-P10942 | DOC-E E9: Incident drill | `docs/evidence/current/E09-incident-drill.md` | `tests/contract/doc-e-e9-incident-lifecycle.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E10 | P10943-P10944 | DOC-E E10: Runbook | `docs/evidence/current/E10-deploy-runbook.md` | `tests/contract/doc-e-e10-e12-external-gates.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E11 | P10945-P10946 | DOC-E E11: Signoff | `docs/evidence/current/E11-release-signoff.md` | `tests/contract/doc-e-e10-e12-external-gates.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E12 | P10947-P10948 | DOC-E E12: Rollback | `docs/evidence/current/E12-rollback-execution.md` | `tests/contract/doc-e-e10-e12-external-gates.test.ts` | Must include exact-HEAD real log, environment, commands, human approvals as required; file alone not sufficient |
| E-FORMAT | P10949-P10999 | Proof schema, release signoff and operational checks | `packages/contracts/doc-e-evidence.ts`, `scripts/doc-e/aggregate-evidence.ts` | `tests/contract/doc-e-evidence.test.ts` | Check semantics at exact HEAD |

## Stop conditions and map update protocol
- If DOCX SHA mismatch: do not compare or edit based on it. If HEAD changes: recompute path existence and mark stale proof, then reconcile changed files.
- A path listed here is **a navigation hint only**. Inspect full source and relevant callers, boundary/runtime behavior, database/worker/CI and positive/negative tests; missing path is not proof the system is absent.
- Preserve append-only run evidence, no silent change to this frozen snapshot. New HEAD => new atlas version or explicit diff with exact tree SHA. No '100%' until every current in-scope atomic requirement has source + executable evidence and all required DOC-E gates pass.

## Path verification anomalies
- No selected source-candidate path is missing at frozen HEAD.
- No selected test-candidate path is missing at frozen HEAD.
