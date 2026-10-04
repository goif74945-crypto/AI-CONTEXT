FINDING_ID: F-4A9C7E21-GHA-RUNNER
FROM_CHAT: C-4A9C7E21
TO_CHAT: C-7D1527AD; C-7B5E20D1
TASK_ID: T-1AB7ABF2; T-7B5E20D1
HEAD_SHA: cf2f5e44032de0b241f4068b5ff919bf1499a800
SEVERITY: P1
OBSERVATION: GitHub Actions deploy workflow failures on source SHA 9e615b04 are runner/startup-plane failures, not executed test failures: original run 37222997743 and rerun attempt 2 produced failed jobs with zero steps and no downloadable logs.
EXPECTED: jobs receive a runner and execute checkout/setup/test steps.
ACTUAL: failed jobs have steps=[] and log download returns BlobNotFound.
REPRODUCTION: reran failed TypeScript typecheck job 111496919063; run attempt advanced to 2; replacement job 111540274599 completed failure with zero steps; log blob absent. Static determinism replacement job 111540275560 behaved the same.
EVIDENCE: GitHub run 37222997743 attempt 2; jobs 111540274599 and 111540275560; Railway deployment 6ebf2acb-1889-450c-874a-1114b4f51531 separately executed and failed at check:coverage.
SUGGESTED_DIRECTION: keep GitHub runner-plane failure separate from repository test failures. Use Railway exact-revision evidence for executable source-gate diagnosis until GitHub runner execution is restored.
