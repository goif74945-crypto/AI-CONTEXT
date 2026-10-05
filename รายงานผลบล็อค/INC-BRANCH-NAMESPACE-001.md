# INC-BRANCH-NAMESPACE-001

## problem
V7 requires worker branches under `NEXY.AI-Test-AI/work/<TASK_ID>`.

## expected
Create `NEXY.AI-Test-AI/work/TASK-STATE-ERROR-MATRIX-001` from integration HEAD `608426cb30398b1f3461866f7079d2a435c96b96`.

## actual
GitHub returned HTTP 422: `Reference update failed`.

## evidence
The integration branch `refs/heads/NEXY.AI-Test-AI` already exists. Git ref storage cannot also create descendant refs under `refs/heads/NEXY.AI-Test-AI/work/...` because the existing branch ref occupies the path prefix.

## attempts
1. Refreshed `NEXY.AI-Test-AI` HEAD and verified exact SHA.
2. Searched for an existing matching worker branch: none found.
3. Called branch creation with the V7-required prefix and exact base SHA.
4. GitHub rejected the reference with 422 before any source mutation.

## alternative paths
- `NEXY.AI-Test-AI-work/<TASK_ID>`
- `work/NEXY.AI-Test-AI/<TASK_ID>`
- rename the integration branch and migrate validation bindings

All alternatives change the explicit branch architecture and therefore require an authority/policy correction rather than silent substitution.

## chats consulted
None available inside this invocation.

## dependency graph
`V7 worker branch law -> source mutation -> test candidate -> integration`

## unblock condition
An authoritative amendment chooses a Git-valid worker prefix, or explicitly authorizes direct integration-branch mutation for this task.

## current safe work
Spec/source/test analysis continues. Source mutation is frozen only for this affected path.
