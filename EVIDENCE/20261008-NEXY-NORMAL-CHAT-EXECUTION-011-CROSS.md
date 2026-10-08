# Execution 011 CROSS
Product NEXY.ai HEAD 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
DOCX SHA-256 verified this turn: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
DOC-C paragraph indices zero-based P9885 (BUILD SPEC) and P9915 (release.quorum_min=2) / P9916 (evidence_min=2).
LAW initial source Git blob f0ae1b06774e11cb2c0f417bc36c0d398347b036; isolated patched source 696acae9428a347e91eb32a26b692f6d913f1bf0.
LAW patch blob d9247cf4f91c624683d21c3a4225510cd32b0822; LAW test blob 417f3932f3eaf649eb11e56963838727f3537f67.

Source bug: prereleaseGate accepted candidate quorumCount=2 with only one distinct agentIds element when confidence, evidence and thresholds otherwise passed. A second malformed candidate claimed 10 votes with only 2 agentIds. isReleaseCandidate returned true, gate allowed both. Proposed minimal guard: quorumCount <= agentIds.length AFTER existing agentId uniqueness checks. Normal verified JUDGE candidate source blob eb9e261006c6496c78256d0ad1b287425cd2a8e8 derives both from same votes; no proof normal JUDGE emits the inconsistent input.

RED actual Product import, before patch, command: node node_modules/vitest/vitest.mjs run tests/contract/ex011-law-quorum-cardinality.test.ts --reporter=verbose => exit=1, 2 fail 3 pass.

GREEN patch in isolated checkout, command: node node_modules/vitest/vitest.mjs run tests/contract/ex011-law-quorum-cardinality.test.ts tests/contract/release-spine.test.ts tests/contract/runtime-config-consumers.test.ts tests/coverage/core-state-matrix.test.ts tests/coverage/judge-law.test.ts --reporter=dot => exit=0; 58/58 pass.

Backend TypeScript: node node_modules/typescript/bin/tsc --noEmit -p tsconfig.json => exit=0. git diff --check exit=0; git apply --reverse --check law patch exit=0; patch LF read-back verified.

Broad suite command: node node_modules/vitest/vitest.mjs run tests/contract tests/coverage --reporter=dot => exit=1, 910/916 pass, 6 fail. Independent JSON rerun: --reporter=json --outputFile=EX011-LAW-BROAD-RESULTS.json => exit=1, 909/916 pass, 7 fail. Cases in core-kernel-no-authoritative-rng.test.ts (cargo ENOENT), core-kernel-rust.test.ts (cargo ENOENT), core-kernel-tier-depth-compile.test.ts (2), current-head-attestation.test.ts (2), sandbox-depth-buildtime-law.test.ts (1). Do not assert exact root cause of all failing tests. No full suite PASS.

Runner: authorized DESKTOP-FOB7IK8 Windows Node24 online; docker/podman/postgres/pg_ctl/psql/redis-server absent; Termalin hosts zero. Local isolated Linux tool sandbox lacks DB/Redis/Docker binaries. Railway existing NEXY Validation R2 had ONLY production environment with PG+Redis; NOT USED. CI current-head E7 37741650376 attempt2 six failed jobs steps unavailable. No production runner test or billing/secret changes.

G3_REAL_POSTGRES_REDIS NOT_RUN. No new Queue harness this execution. Canonical OWNER cancellation uses shared pg advisory transaction lock and freezes dispatch atomically (historically verified, not independently concurrency-tested this run). Standalone cancel/emit uncertainty remains NOT_VERIFIED.

Verdict: independent executable LAW boundary defect reproduced and minimally patched locally with 58/58 related green, backend typecheck green, broad suite failed. Product source unchanged and NOT_COMMITTED because global validation gate not green. DOC-E release NOT_AUTHORIZED. Audit coverage not completion.
