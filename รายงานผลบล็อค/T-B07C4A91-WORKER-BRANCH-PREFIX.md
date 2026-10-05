# TRUE_BLOCK - Worker branch namespace

TASK: T-B07C4A91
CHAT: C-B07C4A91
EPOCH: EPOCH-20261005-b35ee1bf-608426cb
STATUS: TRUE_BLOCK
AFFECTED_SCOPE: SOURCE MUTATION REQUIRING V7 WORKER BRANCH

## problem
Constitution V7 requires NEXY.AI-Test-AI/work/<TASK_ID>, but NEXY.AI-Test-AI already exists as the integration branch.

## expected
Create an isolated worker branch from integration HEAD 608426cb30398b1f3461866f7079d2a435c96b96.

## actual
Git rejects a branch path nested beneath an existing branch ref.

## evidence
Clean local reproduction:
- attempted ref: NEXY.AI-Test-AI/work/T-PROOF
- exit code: 128
- result: existing refs/heads/NEXY.AI-Test-AI prevents creation of the nested worker ref

## attempts
- verified integration branch exists on GitHub
- searched worker branches and found none
- reproduced the ref constraint in a clean local Git repository without changing project refs

## alternative paths
Technically valid alternatives include work/NEXY.AI-Test-AI/<TASK_ID> and NEXY.AI-Test-AI-work/<TASK_ID>. Selecting either changes an explicit Constitution rule, so neither was selected.

## dependency graph
worker branch law -> worker branch creation -> source mutation -> test/review -> integration

Only the source-mutation path is blocked. Spec analysis, review, red-team, and control-plane work can continue.

## unblock condition
An authoritative correction changes the worker branch naming rule to a Git-valid namespace, or authorizes a named exception for this epoch.
