# Task Contract — NEXY Meta-Assurance Foundry

## OBJECTIVE
Design, implement, execute, test, audit and persist five new standalone engineering systems under AI-CONTEXT `คลังข้อมูลเสริม` that are useful to future NEXY.AI work while never modifying a repository whose name contains `NEXY.AI`.

## AUTHORIZED SCOPE
Only new files under:
`คลังข้อมูลเสริม/CHAT-20261005-0155-NEXY-META-ASSURANCE-FOUNDRY/**`

Read-only inspection of AI-CONTEXT and NEXY project context is authorized for compatibility and de-duplication.

## PROTECTED SCOPE
- every repository whose name contains `NEXY.AI`;
- existing sibling supplemental labs;
- canonical NEXY project requirements/specifications;
- secrets, credentials and private data;
- production deployment or external side effects.

## IMMUTABLE REQUIREMENTS
1. Every concept is labeled AI-proposed and non-authoritative.
2. Deterministic core behavior for equivalent normalized inputs.
3. No hidden clock/random/network/filesystem/process/environment dependency in core verdict logic.
4. No arbitrary eval/exec of untrusted expressions.
5. Invalid or incomplete proof preconditions fail closed.
6. Tests must include negative paths and determinism/order invariance where applicable.
7. PASS claims require executed evidence matching the claim class.
8. Each concept has its own Design, Code, Test and Evidence files.
9. No NEXY.AI repository write, branch, commit, PR, issue, workflow or setting change.

## REQUIRED EVIDENCE
- E0: persisted files exist and can be re-read.
- E1: Python compilation succeeds for exact authored source.
- E2: unit/adversarial tests execute successfully.
- E3: suite-level integration smoke that imports/runs all five systems.
- NEXY runtime/integration/deployment evidence: explicitly NOT_VERIFIED.

## STOP CONDITIONS
FREEZE affected completion claims if protected scope would be touched, exact tested bytes cannot be published/re-read, tests remain failing, or branch drift prevents safe additive publication.
