FINDING_ID: F-6E3A91D4-RAILWAY
FROM_CHAT: C-6E3A91D4
TO_CHAT: C-7D1527AD
TASK_ID: T-1AB7ABF2
HEAD_SHA: 6597a53485e78021ebbca61f9a8ecc74cb90c084
SEVERITY: P1
OBSERVATION: Railway branch-validation service follows NEXY.AI-Test-AI, but its source-identity gate still compares RAILWAY_GIT_COMMIT_SHA against stale DOC_E_TESTED_SHA=9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.
EXPECTED: Exact-work-branch validation must bind DOC_E_TESTED_SHA and DOC_E_TESTED_TREE to the deployment commit/tree so test and coverage gates can execute.
ACTUAL: Deployment 3df8648e-cedf-4e53-923f-5234b04d3638 for commit 6597a53485e78021ebbca61f9a8ecc74cb90c084 fails at Docker build step 9 before repository tests because 6597a534... != 9e615b04.... Deployment 346815e2-d01e-4741-837a-9c389374fab5 for 47a4ab8... failed identically.
REPRODUCTION: Railway get_logs(build,error) for deployments 3df8648e-cedf-4e53-923f-5234b04d3638 and 346815e2-d01e-4741-837a-9c389374fab5.
EVIDENCE: Railway exact build logs show the failing shell equality test and exit code 1.
SUGGESTED_DIRECTION: Rebind exact-head source-identity inputs before interpreting Railway failures as test/coverage failures. Do not weaken or remove the identity gate.