FINDING_ID: F-B07C4A91-WORKER-BRANCH-PREFIX
REQ_ID: CONTROL-V7-BRANCH-ARCHITECTURE
TASK_ID: T-B07C4A91
FROM: C-B07C4A91
TO: GLOBAL
SHA_NEXY_AI_TEST_AI: 608426cb30398b1f3461866f7079d2a435c96b96
SHA_NEXY_AI: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
SEVERITY: P0
STATUS: SUPERSEDED

OBSERVED:
Constitution V7 requires worker branches named NEXY.AI-Test-AI/work/<TASK_ID>, while branch NEXY.AI-Test-AI already exists.

EXPECTED:
An isolated worker branch namespace that can coexist with the integration branch.

REPRODUCTION:
In a clean local Git repository:
1. create branch NEXY.AI-Test-AI
2. attempt to create NEXY.AI-Test-AI/work/T-PROOF

RESULT:
exit_code=128
Git reports that refs/heads/NEXY.AI-Test-AI already exists and the child ref cannot be created.

REASONED_PROOF:
Git branch refs cannot use a path beneath an existing branch ref. This is a ref namespace constraint rather than a repository permission issue.

IMPACT:
Source mutation that follows V7 worker-branch rules is blocked. Direct mutation of NEXY.AI-Test-AI would bypass the required isolated worker branch, while NEXY.ai is protected.

SAFE_ALTERNATIVES_REQUIRING AUTHORITY CHANGE:
- work/NEXY.AI-Test-AI/<TASK_ID>
- NEXY.AI-Test-AI-work/<TASK_ID>

No alternative was selected without authorization.

V16_RC1_3_SUPERSESSION:
- PRIOR_STATUS: REPRODUCED
- SUPERSEDED_BY: NEXY::EQUAL-PEER-FENCED-ATOMIC-DYNAMIC-SCALE-ENGINEERING-CONSTITUTION-V16-RC1.3
- SUPERSESSION_RECORD: NEXY-BUILD-CONTROL/V16/PREACTIVATION/SUPERSESSIONS/SUPERSESSION-V16RC13-LEGACY-WORKER-NAMESPACE-P0-001.json
- REASON: The legacy literal worker prefix is no longer mandated by V16-RC1.3; isolated workers remain mandatory and direct implementation on NEXY.AI-Test-AI remains forbidden.
- PRODUCT_MUTATION_AUTHORIZED: FALSE
