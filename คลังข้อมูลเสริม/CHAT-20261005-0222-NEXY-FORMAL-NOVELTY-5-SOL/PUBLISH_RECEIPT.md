# Publish Receipt

**Execution code:** `CHAT-20261005-0222-NEXY-FORMAL-NOVELTY-5-SOL`  
**Classification:** POST-PUBLISH EVIDENCE / NON-CANONICAL  
**Sealed artifact manifest scope:** the original 31 files listed by `MANIFEST.sha256`. This receipt is intentionally added after the seal and is not part of that manifest.

## Publication evidence
- Pull request: #70
- PR head commit: `7e5429fd91c14806855d1e45b205ac245ac486b0`
- Merge commit: `d0e4bad832575384774c927779ee9c232a0f8806`
- Merge result: PASS
- PR diff audit: 31 changed files, all under this folder; 0 files outside target prefix; 1536 additions; 0 deletions.
- Sealed target subtree SHA before merge: `7150c4c4a9bf3f60a3ee8dbffa565a8b0342e97b`
- Target subtree SHA observed inside merge commit: `7150c4c4a9bf3f60a3ee8dbffa565a8b0342e97b`
- Subtree identity: PASS — exact Git tree identity proves the merged 31-file artifact equals the staged/tested artifact bytes and paths.
- Target blob count at merge commit: 31.
- Re-read from immutable merge commit: `README.md`, `MANIFEST.sha256`, `TEST_OUTPUT.txt` PASS.
- Later main observation: `279929d5a6ffc020c10281f2291ac2373c62dc17` was 19 commits ahead of the merge commit and 0 behind; merge commit was the merge base, proving the published work remained in main history at that observation.

## Verification status
- Design artifacts: PASS
- Python static compilation: PASS (E1, recorded in TEST_OUTPUT.txt)
- Unit/negative-path tests: PASS, 20/20 (E2)
- Stress/determinism checks: PASS
- Manifest verification on the staged 31-file artifact: PASS
- AI-CONTEXT publication: PASS
- Post-publish immutable re-read: PASS
- NEXY.AI repository mutation: NONE
- NEXY.AI runtime integration: NOT_VERIFIED / NOT PERFORMED
- Canonical promotion: NOT PERFORMED; all five systems remain Lo4 AI proposals.

## State clarification
`00_EXECUTION_STATE.md` and `REQUIREMENT_LEDGER.md` were sealed before publication and therefore retain PENDING markers for the publication step. This receipt is the later evidence record and supersedes those two pre-publish PENDING markers only for publication/post-publish status. It does not alter any other claim or promote any proposal into NEXY canon.
