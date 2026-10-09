# AI.AI Review and Engineering Constitution v1

## Authority and exact scope

Owner directive, 2026-10-09: create a NEW root AI.AI/ review workspace in goif74945-crypto/AI-CONTEXT, existing main branch. All writes must remain strictly inside this new prefix.

IN SCOPE: evidence-based criticism of AI.AI, analysis of actual implementation, new system concepts, executable integration code, regression tests, independent test evidence, and unique proposal coordination within AI.AI/.

OUT OF SCOPE: changing, deleting, moving, renaming, or writing into any folder named exactly โค้ดโปรเจคปัจจุบัน, even indirectly; changing existing PROJECTS/AI.AI or any other path in AI-CONTEXT; changing any product repository, CI, branch, setting or secret; mutating any NEXY.AI- repository; and claiming unsupervised deployment. A patch is a deliverable, not permission to apply it to protected code.

## Four binding mission rules

RULE 1 CRITIQUE: Every contributing chat MUST identify an original defect or important gap in AI.AI, with pinned source location, reproducible observation, expected behavior, severity, impact, and verification evidence. Criticism without real source or tests is UNKNOWN, not fact.

RULE 2 INNOVATION: Every chat MUST introduce an original useful system idea or repair, defining API, authorization boundaries, input/output contract, dependencies, edge cases, security and acceptance criteria. A repair can address the same defect as that chat's critique.

RULE 3 WORKING CODE: Every accepted idea MUST include directly integrable, complete working code (preferably an integration.patch) and automated positive/negative tests. Apply and run the patch only in an isolated copy at the exact pinned AI.AI product revision. Record commands, actual pass/fail totals and artifact hashes. No pseudocode, placeholder implementation, fake green results, or treating mock passes as physical-device passes. Product merge is a separate, expressly authorized step.

RULE 4 CROSS-CHAT NONDUPLICATION: Every chat MUST compare its criticism signature AND its proposed system behavior against REGISTRY.md, all existing proposal manifests/source and related AI.AI product records before claiming a new idea. Change of title or ID does NOT produce originality. A prior equivalent critique/idea blocks the new one. If a complete search is impossible, report BLOCKED_UNIQUE_IDEA; never invent uniqueness.

## Concurrent-chat protocol

1. Read current main HEAD and enumerate entire AI.AI/ proposals and REGISTRY.md.
2. Pin actual product branch/commit and source/archive SHA-256. Mark older reports as history, not current code.
3. Select a genuinely new critique signature (problem + subsystem + observed effect) and idea fingerprint (problem class + target + change in behavior), then reserve an unused AAI-YYYYMMDD-NNN directory.
4. Write manifest.json, README.md, integration.patch (including tests), TEST_EVIDENCE.md and index entry. No changes outside AI.AI/.
5. Run an isolated patch check, targeted tests, project tests, and offline catalog validation; report failures without concealing them.
6. Refresh current main HEAD and redo semantic collision detection immediately before publication. Atomically commit with HEAD concurrency check. If HEAD moved, reread and restart collision review. Never overwrite another chat.
7. Fetch committed files and changed-path list from GitHub; if any non-AI.AI path changed, fail the acceptance.

This is a coordination rule, NOT automatic global synchronization between chats. A static fingerprint validator cannot prove semantic nonduplication; manual independent review of scope and code is mandatory.

## Package required per chat

- manifest.json: unique ID/title, critique signature, idea fingerprint, pinned product revision, artifact hash, test count, exact status.
- README.md: source-cited criticism, real code design, risks and integration procedure.
- integration.patch: directly applicable to pinned product copy, including new executable tests; alternatively a full ready-to-copy source tree paired with explicit test integration, but its compatibility must be proven.
- TEST_EVIDENCE.md: actual command outputs, failures/skips, before/after repro, environment, SHA hashes, platform and limitations.
- REGISTRY.md entry referencing that package.

## Acceptance states (never skip evidence)

PROPOSED -> IMPLEMENTED_UNTESTED -> TESTED_ON_PINNED_REVISION -> MERGE_READY -> MERGED.

TESTED_ON_PINNED_REVISION means its exact artifact passed test on the recorded source only. MERGE_READY requires validation against the current product HEAD. MERGED requires an actual authorized product commit plus postmerge tests. On conflict, missing source, missing dependencies, failed test, stale revision, duplicate or impossible verification, use BLOCKED/REJECTED_DUPLICATE/REJECTED_INVALID, not PASS.

## Security and immutable gates

Do not touch any โค้ดโปรเจคปัจจุบัน folder. Do not run untrusted code with elevated privileges or expose tokens/data. Verify path traversal/symlink and unauthorized actions remain rejected. Preserve approved action contracts, explicit user consent, policy guards, cancellation and audit behavior. Regression or evidence mismatch blocks promotion. Name mocks and environment restrictions explicitly. Never fabricate time, coverage, tools or results.

## Stop conditions

A chat is complete only when it has unique criticism plus idea, complete code, passing applicable tests, hashes, registry entry, strict path audit and GitHub read-back. If any are missing, report precise failure/unknown and leave previously protected code unchanged.
