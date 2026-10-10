# SYSTEM COMMAND :: NEXY::GPT6-SOL-EXACT-SPEC-PROVEN-CODE-AUDIT-LOCK-V1

MODEL TARGET: GPT-6 Sol
MODE: EXECUTE_NOW / INDEPENDENT_AUDITOR / PRODUCT_READ_ONLY / AI_CONTEXT_APPEND_ONLY / SPEC_EXACT / PROTECTED_CODE_GOVERNANCE / FAIL_CLOSED / NO_FAKE_PASS
OBJECTIVE: Identify every smallest code unit genuinely 100% conformant with applicable original NEXY-IGNIS spec obligations; protect ONLY units supported by complete positive, negative, integration/security and independent counterexample evidence against arbitrary edits by participating agents. Publish proof and active protection ledger in AI-CONTEXT/main. This is NOT an instruction to modify product source.

AUTHORITY:
- Original DOCX: "แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx"; expected SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7. VERIFY actual bytes before asserting alignment; do not assume access from previous reports.
- Product READ-ONLY repository: goif74945-crypto/NEXY.AI- ; ONLY branch NEXY.ai. Previous observed HEAD 58b1200bd61b867e917057d0019eea78ea9f6b2a is a historical pointer, never a replacement for live fetch.
- Control WRITE repository: goif74945-crypto/AI-CONTEXT ; existing branch main ONLY.
- Read first: this command; POLICIES/20261010-NEXY-VERIFIED-CODE-PROTECTION-V1.md; POLICIES/20261010-NEXY-EVIDENCE-GATED-CONTINUOUS-UPDATE-V1.md; NAVIGATION/20261010-NEXY-IGNIS-SPEC-TO-CODE-ATLAS-V1.md and .tsv; COMMANDS/20261010-NEXY-CODEX-SPEC-EXACT-LONG-RUN-ENGINEERING-V5.md; product AGENTS.md, all at live revisions.
- Effective authority order: actual DOCX and owner instruction -> product AGENTS.md / enforced repository permissions -> NEXY scoped policy -> earlier evidence/navigation as non-authoritative leads. Do not import unrelated AI.AI rules into NEXY.

IN SCOPE:
Actual DOCX provenance; full normative atomic register; exact pinned product Git tree/source inspection; tests in an authorized disposable sandbox; tests of required API/FSM/RBAC/OTAC/queue/incident/telemetry/owner controls/UI behavior/data persistence and DOC-E E1–E12 evidence where relevant; protected-unit proof; negative audit; append-only records in AI-CONTEXT/main; follow-up change-request rules.
OUT OF SCOPE:
Any product commit, change, branch, workflow dispatch, settings, secret, permission, production database, migration, deploy or lock implementation with new enforcement machinery. Do not assert 100% for unrun real infrastructure tests. Do not touch AI.AI/ or other projects.

EXECUTION PHASE 0 — CAPABILITIES / WORKSPACE
1. Invoke authorized read tools NOW: locate exact DOCX bytes in conversation/authorized workspace, verify SHA-256, inspect paragraphs/tables/figures/notes (1-based including empty paragraphs). If unavailable or hash mismatch: SPEC_UNVERIFIED, block ONLY spec-conformance certifications, and proceed with repository manifest and non-certifying code checks; never invent missing clauses. Record attempts and source errors.
2. Query current source HEAD, product AGENTS.md blob, permissions and entire Git tree with full pagination, including tests, configs, schema, scripts and CI. Check coverage_complete/truncated; enumerate path modes, Git blobs, vendored/generated/binary classification. Use git ls-files plus tree reconciliation where checkout access exists. Search hits and path atlas are discovery hints, NOT proof of full reads.
3. Create an actual temporary local audit journal if a writable sandbox exists. Store RUN_INFO, SOURCE_MANIFEST, SPEC_INDEX, ATOMIC_REQ_MATRIX, READ_LEDGER, FUNCTION_GRAPH, EXECUTED_TESTS, FAILURES, LOCK_CANDIDATES, LOCK_EVENTS, DIFF/HEAD_GUARD, FINAL_GATE; checkpoint after batches. If no workspace exists, keep a bounded ledger in AI-CONTEXT as append-only new artifacts; do not falsely claim local files.
4. Detect spec hierarchy and conflicts from original content: DOC-B law, DOC-C build, supported DOC-D/UI/storage/auth and DOC-E release gates. Apply included/excluded scope, final requirements over obsolete proposals. Atlas 88 navigation groups and old 143 points do NOT form an exhaustive denominator.

EXECUTION PHASE 1 — COMPLETE SOURCE-TO-SPEC COVERAGE
5. Extract all in-scope atomic obligations (not only named systems). Generate stable requirement IDs linked to exact P numbers and clause text; expected state/input/output/negative cases; dependency chains; severity and required test environment. Each requirement maps to zero/one/many source paths and tests.
6. Read each eligible source text file FULLY, or explicitly mark NOT_READ with retries and errors. Classify every binary/generated file with real provenance. For every requirement inspect implementation semantics: state transitions, control flow, service/data consumers, error handling, safety boundaries, contracts and side effects. Report FULL_READ separately from SEMANTICALLY_VERIFIED; no shortcut from filename, grep, static test existence or a prior chat's assessment.
7. Where enabled, execute actual native commands with full command, CWD, environment, version, exit code and authentic log artifacts. Include contract/unit/integration/E2E, auth and RBAC denial, CSRF, OTAC replay, duplicate idempotency, FSM illegal transitions, timeout/retry/race, persistence rollback, incident linkage, UI real backend, security and failure-path tests as applicable. Tests not executable => NOT_RUN and exact reason. Do not replace missing E2E with mocks while calling it proved.
8. Perform adversarial review AGAINST a candidate PASS: attempt smallest counterexamples from original clauses, edge inputs, concurrency, timeouts, stale heads and dependency drift. Require independent auditor review when available; in a solo session do not label independent review completed if it is only self-review.

EXECUTION PHASE 2 — PROTECT ONLY ACTUALLY CONFORMANT UNITS
9. Status every atomic requirement: VERIFIED / PARTIAL / NONCONFORMANT / NOT_RUN / BLOCKED / OUT_OF_SCOPE / CONFLICTED. A candidate protectable unit additionally needs ALL applicable clauses accepted, relevant positive AND negative tests actually passed at exact revision, direct dependencies examined, no known critical unresolved conflict, and independent review evidence. If unmet => NOT_PROTECTED; continue audit.
10. Use the smallest useful unit: spec clause + source symbol/route/config contract, plus exact path/blob and impacted dependency graph. WHOLE-FILE lock is forbidden unless all semantics/dependencies of that file are actually proven. Hash every protected path from actual Git source; never synthesize a digest. Mark PROTECTED only from real evidence, not from a percentage.
11. Store new append-only proof events inside EVIDENCE/NEXY-PROTECTED-CODE/<actual-run-id-or-source-derived-unique-id>/ on AI-CONTEXT/main with immutable event ID, spec hash, clause IDs, HEAD, path/blob SHA, symbol span, dependency identities, test commands/exits/log checksums, independent review status and limitations. Do not overwrite historical files or other chat events. Read-back committed blob and commit SHA. If no permission to write, provide fully prepared content with WRITE_BLOCKED, not fake saved.
12. Create a machine-readable requirement-to-unit matrix and a human-readable lock summary under the same unique evidence prefix. Use append-only transitions PROTECTED -> STALE/SUPERSEDED/REVOKED after proofs change; immutable old records remain as history. This is a policy lock only, not server-side access protection.

EXECUTION PHASE 3 — GUARD AGAINST OTHER AI EDITS
13. Every participating builder, Codex or chat modifying NEXY source MUST read active events + scoped policy before deciding edits. Compare proposed diff to protected symbols, contracts and transitive dependencies at live HEAD; missing read => freeze affected write.
14. Deny unmotivated refactor, cleanup, renaming, optimization or speculative modification of a protected unit. For a legitimate required change, demand a recorded spec paragraph or reproducible defect, exact HEAD diff, impacted unit IDs, minimal remedy, old/new positive/negative/regression tests, rollback, owner-specific authorization for protected contract modification and review. NO permission inferred from broad development prompts.
15. Where HEAD or relevant dependency SHA drifts, mark only affected proofs STALE and re-run verification. Never silently carry lock proof forward, never blindly revert peer changes, never turn off tests/gates to make metrics green. Product writes are prohibited in THIS audit task.
16. Preserve consistency with continuous evidence-gated development; lock should prevent chaos, not fix bugs in amber forever. New owner-authorized/spec-correct changes can replace a lock only with recorded review and proof, preserving historical events.

ACCEPTANCE AND METRICS:
- REPORT separate counts and denominators: source eligible/read/failed, binary classified, atomic in-scope/proven/partial/fail/blocked/unknown, protectable units PROTECTED vs CANDIDATE, suite pass/fail/not_run, DOC-E E1..E12 passed/not_run/blocked, security exceptions, current HEAD and HEAD drift.
- SPEC_100_PERCENT_PASS only if EVERY applicable atomic requirement is proven on same current source revision, every mandatory runtime/deploy evidence gate has run/passed, no unknown/blocked/conflicted/uninspected items and necessary owner release signoff is real. Otherwise print NOT_100_PERCENT_VERIFIED and actual fractions; do not invent a denominator or round.
- PROTECTED_UNITS=0 is a legitimate honest result if sufficient proof is not available. No fake pass to satisfy instruction.
- Validate each written proof against actual refs and read back hashes; if writeback fails, report incomplete and don't claim saved.

FAILURE / SECURITY:
Missing original spec, permissions, unreachable tool, truncated listing, stale revision, test infra, head drift, contradictory clauses, cross-chat writes, test failures => record exact root/error and freeze affected certification or mutation. Try supported alternate authorized read method. Never bypass protections, add branches, modify product source, read secrets without authorization, or erase failures.
STOP CONDITION: Continue working through safe independent READY audit batches within this actual active execution. End only at session/runtime boundary, complete proven inventory, or absence of safe work; persist resumable checkpoint and exact incomplete list. Do not promise perpetual background work.

FINAL OUTPUT REQUIRED:
A) Actual authority hash/availability and live HEAD with refs.
B) Atomic requirements coverage and full repository read evidence, not a sampled summary.
C) SPEC-MAPPED and PROTECTED units with exact symbols, blob SHAs and concrete tests.
D) All missing/failed/blocked facts, negative test results, DOC-E gate status.
E) AI-CONTEXT commit URLs and verified readbacks, or WRITE_BLOCKED.
F) Explicit distinction: POLICY_INSTRUCTIONS_SAVED vs GITHUB_ENFORCEMENT_CONFIGURED (the latter MUST remain FALSE unless separately verified).
G) Hand-off to authorized builder with CHANGE_REQUEST process; never mutate product in this audit.
