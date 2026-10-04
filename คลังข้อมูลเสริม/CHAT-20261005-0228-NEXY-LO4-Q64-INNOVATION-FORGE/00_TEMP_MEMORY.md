# Temporary Execution Memory

Classification: `AI_PROPOSED_LO4_ONLY / NON_CANONICAL / RESUMABLE_CHECKPOINT`

## Identity
- Durable work ID: `CHAT-20261005-0228-NEXY-LO4-Q64-INNOVATION-FORGE`
- Platform-native ChatGPT conversation ID: `UNKNOWN_NOT_EXPOSED_BY_AVAILABLE_TOOLS`
- Repository target: `goif74945-crypto/AI-CONTEXT`
- Authorized root: `คลังข้อมูลเสริม/CHAT-20261005-0228-NEXY-LO4-Q64-INNOVATION-FORGE/`
- Protected repositories: every repository whose name contains `NEXY.AI`
- Protected sibling content: all pre-existing supplemental projects

## Current state
The project implements one deterministic Q64.64 substrate and twenty non-governing Lo4 quantitative control proposals. All project code is standalone and has no write path into NEXY.AI.

## Verified local runtime evidence
- Node.js: v22.16.0
- npm: 10.9.2
- Python: 3.13.5
- static/domain rule gate: PASS
- Node tests: 107/107 PASS
- independent Python Q64 oracle: 16/16 PASS
- deterministic replay: 10,000 executions, zero observed digest drift
- benchmark workload: 20,000 evaluations completed
- CLI smoke: PASS

## Historical failure retained
One post-refactor run failed because `tests/integration-chain.test.js` contained a stale closing block after replacing an overlapping experiment-gate concept. The test file was minimally repaired and the complete verification stack was rerun. See `evidence/iteration-01-failure.txt`.

## Authority boundary
Nothing in this directory is Canon, DOC-B, DOC-C, or promotion authority. Every new mechanism is an AI proposal. A future NEXY integration requires explicit authority review and independent integration evidence.

## Resume rule
1. Re-read root AI-CONTEXT execution/security/verification laws.
2. Re-read this file and `01_TASK_CONTRACT.md`.
3. Confirm the repository/ref and this exact directory state.
4. Re-run the full verification commands before changing a correctness claim.
5. Never edit a repository whose name contains `NEXY.AI` from this workstream.
