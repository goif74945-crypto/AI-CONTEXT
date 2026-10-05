BLOCK_ID: BLOCK-V7-WORKER-REF-NAMESPACE-C-8B3F6D21
REPORTER_CHAT: C-8B3F6D21
STATUS: TRUE_BLOCK
SEVERITY: P0
AFFECTED_SCOPE: Source mutations requiring worker branches under NEXY.AI-Test-AI/work/<TASK_ID>
BLOCKED_TASKS:
- T-D4A71C2E source mutation by this chat
PROBLEM: V7 requires worker branch prefix NEXY.AI-Test-AI/work/, while an existing integration branch is exactly NEXY.AI-Test-AI.
EXPECTED: Create NEXY.AI-Test-AI/work/T-D4A71C2E-C-8B3F6D21 from 608426cb30398b1f3461866f7079d2a435c96b96.
ACTUAL: GitHub create-reference rejected the branch with HTTP 422 Reference update failed. Branch search confirms no such worker branch exists and integration head remains 608426cb30398b1f3461866f7079d2a435c96b96.
EVIDENCE:
- integration ref: refs/heads/NEXY.AI-Test-AI at 608426cb30398b1f3461866f7079d2a435c96b96
- attempted child ref: refs/heads/NEXY.AI-Test-AI/work/T-D4A71C2E-C-8B3F6D21
- Git ref namespace invariant: a ref path component cannot simultaneously be a complete ref and a directory containing child refs.
ATTEMPTS:
- create worker branch from exact integration SHA: rejected 422
- search exact task/chat/prefix branches: none
- refresh integration branch: unchanged
ALTERNATIVE_PATHS:
- Direct mutation of NEXY.AI-Test-AI: technically possible but forbidden by V7 worker-isolation policy for coding work.
- Rename integration branch: forbidden without explicit policy change and high integration risk.
- Use sibling prefix such as NEXY.AI-Test-AI-work/<TASK_ID> or work/NEXY.AI-Test-AI/<TASK_ID>: technically viable but not authorized by current literal V7 prefix.
CHATS_CONSULTED: none required; failure is directly reproducible from Git ref namespace semantics and GitHub API evidence.
DEPENDENCY_GRAPH: WORKER_BRANCH_POLICY -> SOURCE_MUTATION -> TEST/REVIEW_CANDIDATE -> INTEGRATION
UNBLOCK_CONDITION: Authoritative coordination policy adopts a non-colliding worker branch namespace, or explicitly authorizes an equivalent isolated branch naming scheme.
SAFE_INDEPENDENT_WORK: Spec audit, source review, test-oracle review, CI/status inspection, red-team, control-plane evidence.
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
