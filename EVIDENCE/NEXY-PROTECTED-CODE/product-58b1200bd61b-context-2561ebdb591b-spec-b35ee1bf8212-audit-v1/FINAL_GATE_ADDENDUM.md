# Exact-head audit final addendum — append-only
Product exact HEAD: `58b1200bd61b867e917057d0019eea78ea9f6b2a` (requeried unchanged after evidence writes).
Spec SHA-256 directly computed from dated original-byte-equivalent DOCX: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`; 12,537 paragraphs. Physical DOCX content is not copied to control repository.
Status: NOT_100_PERCENT_VERIFIED. PROTECTED_UNITS=0. No full atomic-spec denominator was established. No independent compliance review completed.

## Coverage corrected to latest
- Complete metadata tree: 889 Git blobs and 203 folders, 1092 entries, nontruncated.
- Direct complete UTF-8 content received for 27 distinct Git blobs = 8 original + 6 from corrected batch 02 + 6 batch 03 + 5 batch 04 + 2 correction for batch 04. Each additional receipt checked returned UTF-8 byte count against Git source byte size and recorded source blob SHA.
- 862 blobs remain without direct full content read by this audit. Eligibility/type classification, complete source semantics, dependency audit and test execution remain incomplete. It is FALSE to claim repository full-source verification.
- Repo Code Bridge content scan, separately: inspected metadata 889/889; searched full-text 887/889; skipped package-lock.json SIZE_LIMIT, packages/lo2/engine.ts NON_UTF8_OR_SIZE_LIMIT; content search coverage_complete=false; failed_files=0.
- P9846–P10999 contains 1,149 nonblank *paragraph candidates*; not authoritative number of atomic requirements. Local journal indexes all 12,537 paragraphs but exhaustive atomic partition and acceptance matrix not completed.
- DOC-E E1–E12: current HEAD release acceptance NOT_VERIFIED individually. No current authenticated E11 release signoff verified. 4 head-bound GitHub Actions run conclusions=failure; assertion-level root causes unknown.
- Native repository suite not run: no authorized source checkout accessible in isolated audit container (curl DNS error). Rust cargo unavailable. Independent negative witness ISOLATED_NODE_REPRO only, exit 1, 2 pass / 3 fail; not an in-repository test result.

## Parser-error correction (important)
SOURCE_READ_BATCH_02.jsonl wrongly said READ_FAILED for six source paths solely because the first aggregator attempted JSON.parse on a **valid raw source response**. SOURCE_READ_BATCH_02_CORRECTION.jsonl supersedes those invalid failures; all six files subsequently retrieved in full and byte lengths matched tool-provided size.
SOURCE_READ_BATCH_04.jsonl contains wrong locator apps/web/app/lib/api-handler.ts. An exact HEAD path-glob search showed correct apps/web/lib/api-handler.ts, plus tests/contract/api-handler.test.ts; both were fetched with matching byte sizes and recorded in SOURCE_READ_BATCH_04_CORRECTION.jsonl. The wrong path is not a product-code defect.

## Scoped negative witness and reachability
packages/auth/otac.ts: blob `bb6134ab1946c8cfa8f130eb7eea5a777d02c58e`.
Copied expression from safeEqual throws on UTF-8 byte length mismatch where JS string lengths match. computeDeviceId concatenation creates noninjective tuple collisions. Isolated Node v22.16.0 reproducer: 2 PASS, 3 FAIL, exit 1; test log SHA256 `62611f662351d0f4c8c19108b343c02cbdc577726e7f26b45180b05ac5a4ab98`.
Full-text exact-head search (887 searchable blobs) found computeDeviceId in that module only. The production packages/api/auth.ts (blob e1c8c3edbb219d8d584682983cc0996b8f834934) imports otacCrypto to call generateOtacCode, generateRequestId, generateOtacSalt, generateSessionToken, and imports hashDeviceBindingToken/matchesDeviceBindingToken from separate device-binding module; no direct call to otacCrypto.computeDeviceId or otacCrypto.safeEqual was observed in that source. Session code also calls separate device-binding functions. Dynamic/hidden reachability not proven absent; do not claim a live production exploit. Actual integration tests were not executed.

## Lock / enforcement status
The prior NEXY scoped policies and control AGENTS.md are present; new control evidence is written only in unique append-only path. PROTECTED=0 because no unit meets independent/spec/runtime proof gate. GitHub branch details endpoint for NEXY.ai shows `protected=false` and branch protection `enabled=false` at current HEAD; other repository rulesets are not fully audited. This audit did not configure GitHub enforcement, and it performed zero product writes/CI dispatch/deploy.
`POLICY_INSTRUCTIONS_SAVED=true` as repo-local guidance, `GITHUB_ENFORCEMENT_CONFIGURED_BY_THIS_AUDIT=false`. A policy is not technical prevention against other AIs.
For builders: inspect current active events and scoped policy, re-query HEAD, map impacted symbol/dependencies to actual spec P anchors, require minimal change request, owner-specific authorization for protected contracts, positive/negative/regression test receipts and CAS; no casual refactor, no branch creation, no overwrite of peer changes.

## Resume exactly without inventing proof
1. Requery current NEXY.ai HEAD and reconcile Git tree. If drifted, invalidate affected receipts.
2. Complete remaining 862 direct full-content reads and full binary/generated classifications; resolve the two scanner skips via approved alternate read.
3. Atomize original DOC-C/B/D/auth/storage duties from actual P paragraphs into exhaustive stable requirement IDs; verify conflicts.
4. Trace 12 routes, caller/DB/worker and 12 UI screens, 14 components with negative boundary cases.
5. Run real authorized source tests, native DB/queue/browser/Rust suites and DOC-E gate receipts, not only copied-expression reproductions.
6. Independent challenge each candidate before creating any PROTECTED event. Store new events append-only, never edit historical proof files.
