FINDING_ID: F-56D7E2A1-BRANCH-REF-CONFLICT
FROM_CHAT: C-56D7E2A1
TO_CHAT: BROADCAST
TASK_ID: T-56D7E201
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P0
STATUS: SUPERSEDED
TYPE: BRANCH_ARCHITECTURE_CONFLICT

OBSERVATION:
The mandated worker branch name NEXY.AI-Test-AI/work/T-56D7E201 cannot be created while branch NEXY.AI-Test-AI exists.

EXPECTED:
Constitution V7 requires worker branches under NEXY.AI-Test-AI/work/<TASK_ID>, created from current NEXY.AI-Test-AI HEAD.

ACTUAL:
GitHub create-ref for NEXY.AI-Test-AI/work/T-56D7E201 from exact integration SHA 608426cb30398b1f3461866f7079d2a435c96b96 returned HTTP 422 "Reference update failed".

REASON:
Git ref namespaces cannot safely contain both refs/heads/NEXY.AI-Test-AI and refs/heads/NEXY.AI-Test-AI/work/<TASK_ID>, because the former ref occupies the path prefix required as a directory for the latter. This is a ref namespace D/F conflict, not a source/test failure.

REPRODUCTION:
1. Confirm refs/heads/NEXY.AI-Test-AI exists at 608426cb30398b1f3461866f7079d2a435c96b96.
2. Attempt to create refs/heads/NEXY.AI-Test-AI/work/T-56D7E201 from that SHA.
3. GitHub returns 422 Reference update failed.

IMPACT:
Any new source mutation that strictly obeys the mandated worker-branch prefix is blocked. Existing independent review/test/spec work may continue. Direct mutation of NEXY.AI-Test-AI would violate the isolated-worker policy for this task.

UNBLOCK_CONDITION:
Explicitly authorize a Git-compatible worker namespace that does not have NEXY.AI-Test-AI as an existing ref prefix, for example a sibling namespace. Do not silently invent or substitute a branch naming policy.

V16_RC1_3_SUPERSESSION:
- PRIOR_STATUS: OPEN
- SUPERSEDED_BY: NEXY::EQUAL-PEER-FENCED-ATOMIC-DYNAMIC-SCALE-ENGINEERING-CONSTITUTION-V16-RC1.3
- SUPERSESSION_RECORD: NEXY-BUILD-CONTROL/V16/PREACTIVATION/SUPERSESSIONS/SUPERSESSION-V16RC13-LEGACY-WORKER-NAMESPACE-P0-001.json
- REASON: Legacy V7/V8/V11 required the Git-impossible NEXY.AI-Test-AI/work/<TASK_ID> prefix. V16-RC1.3 preserves isolated worker-branch implementation but removes that literal prefix requirement, so this legacy protocol blocker no longer blocks V16 migration/activation.
- PRESERVED_TECHNICAL_FACT: The literal descendant ref remains impossible while refs/heads/NEXY.AI-Test-AI exists.
- PRODUCT_MUTATION_AUTHORIZED: FALSE
