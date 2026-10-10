# NEXY :: Verified Conformant Code Protection Constitution V1
STATUS: OWNER-REQUESTED / ACTIVE INSTRUCTION FOR PARTICIPATING AGENTS / NO PRODUCT MUTATION AUTHORITY
DATE: 2026-10-10 (Asia/Bangkok)
SCOPE: NEXY product repo goif74945-crypto/NEXY.AI-, existing branch NEXY.ai; control repo goif74945-crypto/AI-CONTEXT, existing main.
PURPOSE: Prevent arbitrary AI modifications to source behavior demonstrably conformant with the NEXY-IGNIS authoritative specification. Preserve legitimate, authorized, evidence-backed corrections. This is a coordination policy, NOT server-side GitHub access enforcement.

## 0. Authority, dependencies and non-interference
1. Top substantive authority: original actual bytes of "แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx", verified SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7. Hash value derives from earlier evidence; EACH audit must verify the bytes again. Never substitute previous chat summaries, atlases, approximate paraphrases or generated spec.
2. Interpret final DOC-B SYSTEM LAW, DOC-C BUILD SPEC, supported DOC-D PRODUCT DESIGN and DOC-E DEPLOYMENT EVIDENCE within the original DOCX authority hierarchy (P9837–P9845, one-based paragraphs including empty paragraphs). Reconcile conflicts from the actual text. DOC-A is vision; explicitly excluded/deferred functionality is not a build obligation.
3. Live product AGENTS.md and owner authorizations govern repo/branch permissions. No new product branches, hidden branches, force push, destructive rewrite, bypass of protections, unsafe deployment or secret exposure.
4. Coexist with POLICIES/20261010-NEXY-EVIDENCE-GATED-CONTINUOUS-UPDATE-V1.md. This policy forbids ARBITRARY CHURN, not legitimate required repairs. If authenticated source or ownership instructions conflict, freeze disputed action and present both citations.
5. This policy applies ONLY to the NEXY project. Do not override AI.AI/CONSTITUTION.md or unrelated folders. No policy file alone makes other chats or GitHub automatically obey.

## 1. Normative protected-unit and exact revision rule
A protectable unit is the SMALLEST semantic contract proven compliant: atomic spec clause + source symbol/function/route/schema/event/transition/test and its direct dependencies; a complete file only if ALL active semantic content is proven in-scope and conformant. "One passing test", "file exists", "143 checked", "88 atlas rows", "AI says PASS", and "same path at prior HEAD" are NOT sufficient.
Lock identifiers MUST use:
- SPEC_SHA256, SPEC_PARAGRAPH_ANCHORS, REQUIREMENT_ATOMIC_IDS and normative acceptance assertions;
- PRODUCT_REPO, PRODUCT_BRANCH, EXACT_PRODUCT_COMMIT, TREE_SHA if available, path and current Git blob SHA, symbol or region and dependency/caller map;
- test IDs, test command+arguments, runner OS/tool versions, observed exit, stdout/stderr evidence digests, meaningful positive/negative/property/race/security tests as relevant;
- independent review/evidence and unresolved limitations; verification timestamp if reliably supplied by infrastructure, not invented.
Hash stability alone proves byte identity, NOT behavioral compliance, security, runtime correctness or deployment signoff.

## 2. Auditable statuses, no fake 100%
DISCOVERED -> SPEC_MAPPED -> SOURCE_REVIEWED -> TESTED_PARTIAL -> BEHAVIOR_VERIFIED -> PROTECTED.
Alternate states: NONCONFORMANT, UNVERIFIED, BLOCKED_PERMISSION, BLOCKED_INFRA, OUT_OF_SCOPE, CONFLICTED, STALE, SUPERSEDED, REVOKED.
- PROTECTED may be assigned only when all relevant normative acceptance checks for the unit are proven on pinned actual source and test environment, including negative/adversarial cases, direct callers/consumers and boundary behavior, with independent adversarial review. No unreviewed critical risk or unresolved known applicable contradiction.
- Source-level VERIFIED is not DOC-E RELEASE_APPROVED. Production tests/signoff required by DOC-E are separate gates; unrun gates remain NOT_RUN, not PASS.
- Record denominators separately: eligible source files fully read, binary/generated classifications, atomic in-scope requirements, runtime behaviors verified, and E1–E12 release evidence. Global 100% means EVERY in-scope atomic requirement is accepted on SAME exact HEAD with all necessary gates and no UNKNOWN/BLOCKED/CONFLICTED/NOT_RUN; otherwise status NOT_100_PERCENT_VERIFIED, include measured counts. Never round upward or exclude failures.
- Prior evidence may be reused only if source blob + relevant dependency/environment invariants still hold, proven after HEAD change. Otherwise set STALE and retest.

## 3. Required evidence register and append-only behavior
Create independent proof events under EVIDENCE/NEXY-PROTECTED-CODE/<unique verified run ID or deterministic collision-free source-derived path>/; if no supplied run ID, derive non-fabricated identifier from current revision and exact evidence digest. Do not overwrite existing peer evidence.
Each event:
  event_type, unit_id, spec_hash, atomic_spec_ids, spec_quote_locations,
  product_head, files[{path,blob_sha,symbol_or_range}], dep_hashes,
  acceptance_tests[{id,command,environment,exit_code,artifact_sha,scope}],
  adversarial_review, coverage_status, verdict, limitation,
  previous_event_ref, requesting_agent, authorization_ref, raw_tool_refs.
Use an append-only log of transitions. No silent alteration of previously issued PROTECTED proofs. For revisions, append SUPERSEDED/STALE/REVOKED events with reason and fresh evidence; never rewrite history. If a central index exists or is proposed, treat it as derived/cache, not as evidence or authority.
No credentials, private data or sensitive runtime secrets in this public repo.

## 4. Mandatory guard before ANY NEXY product change by participating agents
(1) READ this policy, current product AGENTS.md, current spec bytes and all relevant active protection events. No read access => fail closed for an affected mutation; don't interpret absence of evidence as permission.
(2) REFRESH exact NEXY.ai HEAD, complete intended diff, blob SHA, spec clauses and active protected units; inspect transitive callers and tests. Make a change-impact map even for refactor, dependency/config/test/schema changes.
(3) DENY changes with no cited normative unmet clause or reproducible defect, no meaningful minimal diff, unclear branch, speculative optimization, aesthetic-only churn or fabricated approval. If unrelated to proven spec work, keep protected units unchanged.
(4) For ANY change that touches a PROTECTED unit or breaks its invariant, require a recorded SPEC-BASED CHANGE REQUEST: problem/owner directive, exact affected unit, reproduced failing case or superseding spec paragraph, alternatives, smallest diff, risk/rollback, explicit owner approval for modification of a protected contract, and reviewer acknowledgment where available. A general "keep developing" request is not a specific approval to rewrite protected units.
(5) Run RED/positive/negative/integration/adversarial/regression tests relevant to old and new behavior. Do not delete/weaken tests or alter specs, status labels, threshold, denominator, CI/branch policy to manufacture PASS. If test capacity unavailable, draft repair in isolated scratch and mark NOT_RUN; no claim of protected acceptance.
(6) Only an agent separately authorized to write product source may commit; use existing NEXY.ai branch ONLY, with expected HEAD / CAS, preserve peer changes and recheck after commit. This document grants NO GitHub/product write permission by itself.
(7) After product SHA changes, update or invalidate affected protection events with source-specific revalidation and linked before/after proof. Preserve unaffected locks where exact dependencies demonstrably hold. Report every removed/revoked status.
(8) If only a single path/permission/runner is blocked, continue READ-ONLY audit of independent units; freeze only the affected write. Never bypass owner restrictions.

## 5. Forbidden regardless of agent/model
No mass formatting, renaming, rewriting or "cleaning" conformant code just to improve aesthetics; no overwriting work of other chats; no fake 100%; no mass protection of unchecked files; no secret/permission alteration; no test disabling; no inferred green CI; no changing README instead of runtime to hide a defect; no automatic branching, forced pushes, production deployment or destructive migration without exact owner consent.

## 6. Verification and limitations
An independent auditor must challenge each PROTECTED decision with spec-counterexamples, input abuse, path- or field-level dependency drift and untested paths. A reviewer cannot self-certify an entire product simply because a test suite ran.
Effective only for agents instructed to read/obey these documents. Actual mechanical denial requires separately authorized GitHub branch protections, rulesets, required checks and/or a CI gate reading a committed registry. A Markdown document alone does not enforce writes against all external AIs.

## 7. Stop conditions
Stop and preserve checkpoint on missing/mismatched spec bytes, stale product head, ambiguity of authority, unverified dependent behavior, conflicting evidence or permissions. Do NOT force a PASS or guess. Existing verified implementation must remain unchanged until documented proper authorization and proof.
