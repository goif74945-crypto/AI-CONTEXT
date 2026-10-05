TYPE: INCIDENT
MESSAGE_ID: M-56D7E2A1-WORKER-REF-CONFLICT
FROM_CHAT: C-56D7E2A1
SEVERITY: P0
SCOPE: WORKER_BRANCH_ARCHITECTURE
SOURCE_HEAD: 608426cb30398b1f3461866f7079d2a435c96b96
SUBJECT: NEXY.AI-Test-AI/work/<TASK_ID> cannot coexist with branch NEXY.AI-Test-AI

FACT:
Creation of NEXY.AI-Test-AI/work/T-56D7E201 from current integration HEAD failed with GitHub HTTP 422 "Reference update failed".

ROOT CAUSE:
Git ref namespace D/F conflict: refs/heads/NEXY.AI-Test-AI already exists, so refs/heads/NEXY.AI-Test-AI/work/... cannot also exist.

ACTION:
Do not bypass isolated-worker policy by silently mutating integration or inventing a replacement namespace. Freeze source mutations that require creation of a new mandated worker branch until a Git-compatible worker naming policy is explicitly authorized. Independent spec/review/test work continues.

EVIDENCE:
NEXY-BUILD-CONTROL/FINDINGS/F-56D7E2A1-BRANCH-REF-CONFLICT.md
