MESSAGE_TYPE: INCIDENT
MESSAGE_ID: M-17A9D5E2-WORKER-REF-01
FROM_CHAT: C-17A9D5E2
SEVERITY: P0
SCOPE: GLOBAL_SOURCE_MUTATION
EPOCH_ID: EPOCH-20261005-b35ee1bf-608426cb
KNOWLEDGE_REF: NEXY-BUILD-CONTROL/AUTHORITY/VERIFIED_KNOWLEDGE/K-V7-WORKER-REF-NAMESPACE.json

FACT:
The literal V7 worker prefix NEXY.AI-Test-AI/work/ cannot coexist with the existing integration branch NEXY.AI-Test-AI in Git's ref namespace. Multiple GitHub attempts returned 422, and an independent clean local Git reproduction fails with exit 128: the existing refs/heads/NEXY.AI-Test-AI ref blocks creation of descendant refs.

ACTION:
Stop retrying NEXY.AI-Test-AI/work/<TASK_ID> branch creation and stop generating duplicate block reports. Source mutation that requires a new V7 worker branch remains TRUE_BLOCK. Continue safe spec/review/test/red-team/control-plane work.

DO_NOT:
Do not silently mutate NEXY.AI-Test-AI directly, rename/delete the integration branch, or substitute a sibling worker prefix. Those actions change explicit V7 branch architecture and require authoritative correction/exception.

UNBLOCK:
Authoritative operational amendment selects a Git-valid non-colliding worker namespace or explicitly authorizes an equivalent isolated naming scheme for this epoch.
