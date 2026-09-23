FAILURE_ID: NEXY-ASTRA-20260923-5c3cad-ENV
context: NEXY current-head validation
cause: GitHub Actions jobs terminate with steps=null; job log retrieval returns BlobNotFound. Desktop execution device is offline. Isolated container cannot resolve github.com for clone.
failed_approach:
  - GitHub Actions current-head run 35886459382
  - Remote Desktop Commander local runner
  - container git clone of target branch
recovery: restore an authorized executable runner, then rerun the repository-defined command set and migration/browser gates.
boundary: This is NOT evidence of application-test failure and NOT a PASS.
prevention: retain NOT_EXECUTED/BLOCKED_ENVIRONMENT until commands actually start and produce step/log evidence.
status: ACTIVE
trace_id: NEXY-ASTRA-20260923-5c3cad
