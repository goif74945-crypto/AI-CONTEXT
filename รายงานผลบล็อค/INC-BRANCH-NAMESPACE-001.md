# INC-BRANCH-NAMESPACE-001

## status
TRUE_BLOCK — RECONFIRMED UNDER V8

## problem
The active V8 Constitution requires worker branches under `NEXY.AI-Test-AI/work/<TASK_ID>`.

## expected
Create an isolated worker branch such as `NEXY.AI-Test-AI/work/TASK-STATE-ERROR-MATRIX-001` from integration HEAD `608426cb30398b1f3461866f7079d2a435c96b96`.

## actual
The existing integration branch occupies `refs/heads/NEXY.AI-Test-AI`. Git cannot also create descendants under `refs/heads/NEXY.AI-Test-AI/work/...` because one ref path component would need to be both a file and a directory. Prior GitHub creation attempts returned HTTP 422 before source mutation.

## evidence
- NEXY.AI-Test-AI remains exactly `608426cb30398b1f3461866f7079d2a435c96b96`.
- V8 preserves the same literal `WORKER_BRANCH_PREFIX: NEXY.AI-Test-AI/work/`.
- Independent local Git reproduction already confirmed the deterministic ref namespace collision.
- V8 does not authorize silent substitution of a different worker prefix or direct integration-branch mutation.

## attempts
1. Refreshed `NEXY.AI-Test-AI` and verified the exact baseline SHA remains current.
2. Verified V8 is active in `NEXY-BUILD-CONTROL/AUTHORITY/EPOCH.json`.
3. Rechecked that the V8 worker prefix is unchanged from V7.
4. Reused the previously independently reproduced Git ref failure; repeating the same impossible remote mutation would add no evidence.

## alternative paths
- `NEXY.AI-Test-AI-work/<TASK_ID>`
- `work/NEXY.AI-Test-AI/<TASK_ID>`
- rename the integration branch and migrate validation bindings
- explicit authority exception permitting another isolation mechanism

All alternatives change the explicit branch architecture and therefore require an authoritative policy correction or explicit exception rather than silent substitution.

## dependency graph
`V8 worker branch law -> isolated source mutation -> candidate test/review -> controlled integration -> exact-head reverify`

## unblock condition
An authoritative amendment selects a Git-valid worker namespace, renames the integration ref with coordinated binding migration, or explicitly authorizes a different isolation mechanism. Direct mutation of `NEXY.ai` remains forbidden and no Test-AI -> NEXY.ai merge is authorized.

## current safe work
Read-only source/spec auditing, test-oracle design, control-plane correction, stale-evidence reconciliation, CI inspection, red-team, and discovery continue. Source mutation requiring a V8 worker branch remains frozen.

## last reverified
- Constitution: NEXY::CONTINUOUS-CODE-CLOSURE-EXPERT-SWARM-CONSTITUTION-V8
- Spec hash: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
- Integration SHA: 608426cb30398b1f3461866f7079d2a435c96b96
