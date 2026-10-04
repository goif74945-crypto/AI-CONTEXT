# Durable Record — NEXY EPC Mutation Adversary Laboratory 20

STATUS: `STANDALONE_VERIFIED / Lo4_AI_PROPOSAL_ONLY / NON_CANONICAL / NON_GOVERNING`
CHAT_ID: `CHAT-20261005-0311-NEXY-EPC-MUTATION-ADVERSARY-LAB-20`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`

## Objective

Build an isolated deterministic mutation-testing laboratory that measures whether EPC/NEXY verification policies detect deliberately invalid behaviors. It is not an alternative CORE/JUDGE/LAW, cannot publish Canon state, and cannot mutate NEXY.AI.

## Authority / source pins

- Spec: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Canonical source SHA-256 observed in current NEXY code/evidence: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- NEXY repo: `goif74945-crypto/NEXY.AI-`
- NEXY branch: `NEXY.ai`
- NEXY exact inspected head: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- Current NEXY read-only evidence used includes numeric-law Q64.64/fail-closed boundaries, JUDGE SWARM-candidate revalidation, Trinity authority map, SWARM JUDGE_PENDING boundary, and sovereign versioning ratification gates.

## Semantic collision boundary

Explicitly excluded rather than recreated:
- EPC causal/evidence governance WIP `CHAT-20261005-0308-NEXY-LO4-EPC-CAUSAL-PROOF-20`;
- EPC court mechanics WIP `CHAT-20261005-0309-NEXY-EPC-LO4-COURT-FOUNDRY-20`;
- Deterministic Swarm Mechanism Fabric 20 diversity/collusion mechanisms;
- Minimal Blocker Core repair-set solver;
- Authority-Preserving Causal Merge / Concurrency Integrity work.

Current AI-CONTEXT search at the verification checkpoint returned no direct matches for `mutation testing`, `mutant kill`, `mutation score`, or `verification adequacy mutant`. This is bounded novelty evidence, not proof of universal uniqueness.

## Architecture

- signed Q64.64 raw integer implementation with i128 deterministic saturation;
- division by zero fails closed;
- binary float rejected from authoritative canonical data;
- deterministic canonical JSON identity;
- mutation operators separated from invariant oracle;
- kill counts only when the exact intended invariant is detected;
- campaign runner emits canonical digest and raw Q64 score;
- independent verifier re-checks structure, count, exact kills, score and report digest;
- static AST audit forbids `random`, `secrets`, and `time` imports in the decision package.

## Implemented 20 mutation families

See `MUTATION_CATALOG.md`. They cover authority bypass, JUDGE skip, SWARM self-approval, auto-promotion, destructive CUT, WIP-as-CUT, vote double-spend, historical rewrite, name-only duplicate detection, missing pins, stale evidence, float injection, wrap overflow, divide-by-zero default, wall-clock/RNG decision inputs, canonicalization drift, counterevidence suppression, dependency truncation, and evidence-class substitution.

## Failure → repair → re-test

A real defect was discovered in mutant composition: M07 overwrote the active round and hid M06. The smallest correction made M07 consume another right for the already-active round without rewriting it. The entire verification pipeline was rerun after the repair.

## Verified standalone evidence

- compileall: PASS;
- static audit: PASS, 9 package files;
- unit/adversarial suite: 39/39 PASS;
- pairwise mutation compositions: all 190 pairs exercised;
- all 20 combined: exact expected invariant detections preserved;
- mutation campaign: 20/20 killed, 0 escaped;
- score: Q64.64 raw `18446744073709551616` = exact 1.0;
- independent verifier: PASS;
- archive SHA-256: `a4ce20cd6d25bb1170017de8cab1e59a17ff0f2a1be61f0b1d88050a7cb1fc89`;
- manifest SHA-256: `55d96963950a5db3bc8896b9b267bf8ee81dbbf2818d87f5f76ec7a7b14fab38`;
- published base64 bundle parts: 8/8 read back with Git blob SHA and byte length identical to the locally tested bundle pieces.

## Evidence class boundary

E1/E2 standalone proof: PASS.

NEXY exact-workspace integration, actual runtime, deployment, release, and Canon promotion: `NOT_VERIFIED`.

## Protection record

No mutation action was invoked against any repository whose name contains `NEXY.AI`.
WIP sibling projects were not CUT.
No automatic promotion or Core/JUDGE/LAW state mutation exists in this package.

## Bundle

See `BUNDLE_README.md` for exact reconstruction. The sealed archive contains 35 manifest-tracked design/code/test/evidence files.
