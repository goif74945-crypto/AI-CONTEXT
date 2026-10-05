RESULT_TYPE: CONTROL_PLANE_REPRODUCTION
RESULT_ID: R-0DC2D7E4-BRANCH-NAMESPACE
CHAT_ID: C-0DC2D7E4
INCIDENT_ID: INC-BRANCH-NAMESPACE-001
SEVERITY: P0_CONTROL_PLANE
REPOSITORY: local isolated Git reproduction of goif74945-crypto/NEXY.AI- branch architecture
INTEGRATION_BRANCH: NEXY.AI-Test-AI
REQUIRED_WORKER_PREFIX: NEXY.AI-Test-AI/work/
RUNNER: git 2.47.3
RESULT: REPRODUCED
EXIT_CODE: 128
COMMAND_SEQUENCE:
- git init
- create initial commit
- git branch NEXY.AI-Test-AI
- git branch NEXY.AI-Test-AI/work/T-DEMO
OBSERVED:
fatal: cannot lock ref 'refs/heads/NEXY.AI-Test-AI/work/T-DEMO': 'refs/heads/NEXY.AI-Test-AI' exists; cannot create 'refs/heads/NEXY.AI-Test-AI/work/T-DEMO'
FACT:
A Git ref cannot simultaneously be a complete ref and the directory prefix of another ref. The literal V7 worker prefix is structurally incompatible with the existing integration branch.
IMPACT:
All source mutation that requires V7-compliant worker branches is globally blocked. Read/spec/review/test-oracle/control work remains safe.
UNBLOCK:
Authoritative policy must choose a Git-valid sibling namespace or explicitly authorize an equivalent isolated-branch exception. This chat does not silently amend branch policy.
