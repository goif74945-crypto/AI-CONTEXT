FINDING_ID: F-7E4D2B19-DOC-E-SHA
FROM_CHAT: C-7E4D2B19
TO_CHAT: C-7D1527AD
TASK_ID: T-1AB7ABF2
HEAD_SHA: c8e9fa3e108feb482a87920a6cc6b22008a62ff5
SEVERITY: P1
OBSERVATION: Railway branch-validation source has been corrected to NEXY.AI-Test-AI, but recent work-branch builds fail before any repository test/coverage gate because DOC_E_TESTED_SHA remains bound to protected upstream SHA 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.
EXPECTED: For an exact work-branch validation deployment, RAILWAY_GIT_COMMIT_SHA and DOC_E_TESTED_SHA must identify the same exact NEXY.AI-Test-AI commit, with matching DOC_E_TESTED_TREE evidence.
ACTUAL: Deployment faf07044-ff27-401d-b3cb-b11060f59219 built RAILWAY_GIT_COMMIT_SHA=1adfc1c3782f63c32eaa535c05a975bd932a7015 while DOC_E_TESTED_SHA=9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43; Dockerfile source-identity RUN exited 1. Therefore coverage/typecheck/test gates did not execute in that deployment.
REPRODUCTION:
- Railway project 01537473-6a6d-42a0-856f-40d8a4e6a712
- service nexy-validation-branch / 3c290782-e2f0-4e5b-87d9-58bae4d4dba8
- deployment faf07044-ff27-401d-b3cb-b11060f59219
- fetch build logs; inspect Dockerfile source-identity RUN after COPY.
EVIDENCE:
- Railway service source.branch=NEXY.AI-Test-AI and no staged service changes.
- Build log prints tested_sha=9e615b04... and git commit=1adfc1c... immediately before exit 1.
- Dockerfile intentionally requires test "$RAILWAY_GIT_COMMIT_SHA" = "$DOC_E_TESTED_SHA".
- Current work HEAD observed during investigation: c8e9fa3e108feb482a87920a6cc6b22008a62ff5; exact-head deployment e1dd02e8-d1ac-4af1-a2c0-eb2949a1e358 was QUEUED, so no exact-head PASS exists yet.
SUGGESTED_DIRECTION: Treat this as provider validation-context staleness, not application/coverage failure. Refresh DOC_E_TESTED_SHA, DOC_E_TESTED_TREE, and rerun nonce atomically for the intended exact work-branch SHA, then inspect terminal build output. Preserve the fail-closed Dockerfile equality check.
