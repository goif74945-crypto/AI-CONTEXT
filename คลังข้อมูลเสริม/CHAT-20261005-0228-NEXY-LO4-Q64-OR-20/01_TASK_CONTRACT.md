# Task Contract — Lo4 Q64 Operations Research 20

## OBJECTIVE
Produce twenty deterministic, NEXY-compatible, AI-proposed advisory optimization/planning engines with a shared signed Q64.64 arithmetic kernel, executable reference code, tests, evidence, and integration guidance.

## TARGET
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0228-NEXY-LO4-Q64-OR-20/`

## AUTHORIZED_SCOPE
- create/update files only inside the target namespace;
- execute authored reference code/tests in isolated local runtime;
- read AI-CONTEXT context required for compatibility and collision analysis;
- create durable checkpoints/evidence under the target namespace.

## PROTECTED_SCOPE
- every repository whose name contains `NEXY.AI`;
- all pre-existing AI-CONTEXT paths outside this target namespace;
- secrets, credentials, private tokens, unrelated user data;
- NEXY Canon and the current 837-row source matrix.

## IMMUTABLE_REQUIREMENTS
1. Every engine remains `Lo4_AI_PROPOSAL_ONLY` until explicit formal promotion.
2. Human/User Law and canonical NEXY authority remain superior.
3. Every decision-relevant real-valued score, weight, cost, threshold, utility, penalty, ratio, load, slack, regret, or reserve uses signed Q64.64.
4. No Python float accepted by public numeric APIs.
5. Overflow, invalid contract, division by zero, duplicate identity where identity must be unique, and impossible hard constraints fail explicitly.
6. Canonical ordering/tie-breaking makes equivalent inputs deterministic.
7. No hidden I/O, provider/model calls, subprocess execution, or credential access in production reference modules.
8. Tests include negative paths; integration success cannot erase an upstream failure.
9. Design/code/test/runtime/deployment/Canon statuses remain separate.
10. No completion claim without fresh matching evidence.

## REQUIRED_DELIVERABLES
- 00_TEMP_MEMORY.md
- 01_TASK_CONTRACT.md
- 02_CONCEPTS.md
- README.md
- DESIGN.md
- NOVELTY_MATRIX.md
- REQUIREMENT_LEDGER.md
- src/lo4or/*.py and src/lo4or/engines/*.py
- tests/*
- evidence/RED.txt
- evidence/GREEN.txt
- evidence/STATIC.txt
- evidence/STRESS.txt
- evidence/INTEGRATION.txt
- evidence/REVIEW.txt
- SHA256SUMS.txt
- FINAL_AUDIT.md

## EVIDENCE_REQUIREMENTS
- E0 remote presence + readback.
- E1 `python -m compileall` and import checks.
- E2 `pytest` unit/boundary/adversarial tests.
- E3 local cross-engine integration flow.
- deterministic stress/replay using fixed seeded generated cases.
- exact file hash manifest tied to tested bytes.

## STOP_CONDITIONS
FREEZE affected work if a required action would mutate NEXY.AI, leave this namespace, require guessing a critical contract, conceal a failure, or claim integration/deployment/Canon status without matching evidence.
