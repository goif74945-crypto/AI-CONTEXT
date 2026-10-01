TASK_ID: NEXY-CONSOLIDATED-REPAIR-A93C7809-20261002
title: Consolidated remaining repair/build block after sandbox import repair
mode: AUDIT/CROSS
timestamp_source: 2026-10-02T03:29+07:00
target_repo: goif74945-crypto/NEXY.AI-
target_branch: NEXY.ai
target_head: a93c780972ed7464bfc5f182d54129c54d0393cc
target_tree: 07b19ad2e0ffb63ffdc958197d8e7d1bfd9654f9
canonical_design_sha256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
sanitization: no secrets, credentials, private personal data, or provider secret values stored

scope:
- exclude the already-fixed corrupted import token
- consolidate all remaining repair, validation, evidence, release, external-proof and branch-governance work into one execution block
facts:
- sandbox test import is restored to "vitest"
- current source tree has no file diff versus previously successful parent ab616cd20f83024bd539d4326e5c5f5942f800fd
- current exact-head Railway validation still fails before tests because DOC_E_TESTED_SHA remains bound to ab616cd20f83024bd539d4326e5c5f5942f800fd while RAILWAY_GIT_COMMIT_SHA is a93c780972ed7464bfc5f182d54129c54d0393cc
- DOC_E_TESTED_TREE already equals current tree 07b19ad2e0ffb63ffdc958197d8e7d1bfd9654f9
- current HEAD has no GitHub Actions workflow run
- docs/evidence/current remains bound to old revision 0d0d82bdc7d04ef8248f310d106cf5e4c1dd7a3d
- E11 authorized release signoff remains absent; E12 rollback evidence remains blocked/stale
- only branch at close is NEXY.ai; branch is reported protected=false and provider-side branch creation prevention is not proven
remaining_work:
1. bind exact-head validation identity to current SHA/tree with a new nonce
2. run complete exact-head validation without changing HEAD during execution
3. regenerate current evidence namespace and attestations from that exact run
4. produce/collect all DOC-E required artifacts including rollback and external authorization evidence
5. collect trusted external proofs for host/hardware/runtime identity/global anchor/TSA/mirrors/public mode/robotics where required
6. rerun full 837 normalized requirement + 935-record inventory audit against exact-head evidence
7. implement real provider-side no-new-branch enforcement when platform capability permits; do not claim AGENTS.md alone is enforcement
8. keep NEXY.ai as the only mutation branch; create no branches
acceptance:
- tested SHA == canonical HEAD
- tested tree == canonical tree
- exact-head test/build/coverage/static/spec gates pass with durable logs/artifacts
- evidence namespace references the same SHA/tree
- no stale evidence promoted
- external-only claims remain blocked until trusted proof exists
- final release status remains blocked until all applicable gates close
final_status: PARTIAL / CONSOLIDATED_WORKLIST_READY
version: 1
hash: HASH_UNAVAILABLE
