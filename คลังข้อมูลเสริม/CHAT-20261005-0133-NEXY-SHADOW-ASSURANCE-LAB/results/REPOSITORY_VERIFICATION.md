# Repository Publication Verification

Status: VERIFIED for AI-CONTEXT publication of this standalone lab.

## Target
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0133-NEXY-SHADOW-ASSURANCE-LAB/`

## Publication path
- Collision-isolated staging branch: `work/chat-20261005-0133-nexy-shadow-assurance-lab`
- Pull request: `#32`
- Merge commit: `e99c31025eb98fb80ddac6ac3b9da0d21d29e546`
- Merge was performed by GitHub without forcing `main`.

## Pre-merge scope evidence
GitHub compare reported the staging branch as one commit ahead and 46 commits behind at the observation point. It reported 28 changed files, and every changed file was under this lab path. Zero out-of-scope changed files were observed. Four code files had already landed during an earlier contents-API attempt before concurrent movement caused a 409; the final merge preserved them with matching blob identities.

## Post-merge evidence
The immutable merge commit was re-fetched and its recursive tree inspected. The target subtree contained exactly 33 blob files, `truncated=false`, with the expected Git blob SHA for every published file.

## Concurrency evidence
Direct writes to `main` encountered both `409` branch-moved conflicts and `422 Update is not a fast forward`. Those failures were not bypassed with force. Publication switched to an isolated branch plus server-side PR merge to preserve concurrent work.

## Boundary
No repository whose name contains `NEXY.AI` was mutated. NEXY runtime integration remains NOT_VERIFIED and was not attempted.
