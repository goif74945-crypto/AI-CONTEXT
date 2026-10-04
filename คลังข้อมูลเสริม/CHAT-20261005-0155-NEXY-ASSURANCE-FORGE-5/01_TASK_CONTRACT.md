# Task Contract — NEXY Assurance Forge 5

Status: LOCKED
Execution ID: `CHAT-20261005-0155-NEXY-ASSURANCE-FORGE-5`

## OBJECTIVE
Produce exactly five materially distinct, AI-proposed assurance systems useful to NEXY.AI, with standalone deterministic reference code, executable positive/negative/integration tests, design records, verification evidence, and a resumable final state.

## REQUIRED OUTPUT
- Five proposal designs.
- Real reference implementation, no placeholders.
- Tests for positive, negative, deterministic and cross-system behavior.
- Temporary memory/checkpoints.
- Requirement/evidence ledger.
- Collision/novelty audit.
- Integration map.
- Hash-bound verification evidence.
- Final audit.

## INPUTS / AUTHORITY
1. Current explicit user directive.
2. AI-CONTEXT Execution Kernel and global/security/verification rules.
3. Current NEXY project context and normalized 837-row source matrix.
4. Current observed sibling work in `คลังข้อมูลเสริม`.
5. Executed local evidence for this standalone implementation.
6. External standards/references only as supporting research, never as NEXY authority.

## IN SCOPE
Additive files only under this execution namespace in AI-CONTEXT; read-only inspection elsewhere; isolated local execution of authored code/tests.

## OUT OF SCOPE / PROTECTED
- Any mutation to any repository whose name contains `NEXY.AI`.
- Mutation of pre-existing AI-CONTEXT files outside this namespace.
- Claims that these proposals are canonical NEXY requirements or existing NEXY features.
- Production deployment, live security, or operational guarantees.
- Secrets/credentials.

## IMMUTABLE RULES
R1 Exactly five concepts.
R2 Every concept labeled AI-PROPOSED / EXPERIMENTAL / NOT CANON.
R3 Deterministic authoritative functions for equal canonical inputs.
R4 Fail closed on malformed/materially insufficient input.
R5 No core network, wall-clock, randomness, subprocess, environment reads, or hidden model calls.
R6 No placeholder implementation presented as complete.
R7 Positive and negative behavior must be executed.
R8 Cross-system composition must be executed.
R9 PASS requires matching evidence class.
R10 Design != implementation != NEXY runtime != deployment.
R11 Protected repositories remain untouched.
R12 Persist exact tested source/tests and bind them by hashes.
R13 Record trade-offs, failure modes, limitations, and adoption gates.
R14 Preserve a durable resumption point.

## ACCEPTANCE / EVIDENCE
- E0: GitHub presence/read-back of persisted mission files.
- E1: `compileall` + AST static policy gate.
- E2: executed unit/adversarial suite.
- E3: executed integration tests across proposal systems.
- Determinism stress: multiple PYTHONHASHSEED runs.
- Scope proof: all writes made only under this namespace.
- Hash binding: manifest over persisted source/tests/docs/evidence.

## STOP CONDITIONS
Freeze mutation if target identity is uncertain, a protected path would need modification, a material authority conflict appears, persisted bytes cannot be matched to tested bytes, or required evidence cannot be obtained.