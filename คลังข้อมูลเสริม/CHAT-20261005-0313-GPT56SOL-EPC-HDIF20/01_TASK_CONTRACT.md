# TASK CONTRACT — EPC HDIF-20

## OBJECTIVE
Produce a standalone, integration-ready Lo4 advisory package containing exactly 20 novel human-deliberation integrity mechanisms for the proposed NEXY Evolutionary Proposal Court.

## REQUIRED OUTPUT
- architecture/design specification
- Q64.64 deterministic implementation
- exactly 20 implemented mechanisms
- executable tests including negative and deterministic replay cases
- integration adapter contract for NEXY
- novelty/collision analysis
- test/evidence logs and hash manifest
- durable execution state

## INPUTS
- current user EPC law
- NEXY-IGNIS canonical source identity and normalized AI-CONTEXT context
- exact read-only NEXY implementation head
- current AI-CONTEXT supplemental corpus

## IMMUTABLE REQUIREMENTS
- never mutate NEXY.AI-
- no auto-promotion, Canon override or Core/JUDGE state mutation
- Q64.64 for quantitative decision support
- UNKNOWN/WIP is not CUT evidence
- human-facing outputs remain advisory
- no floating point in decision logic
- deterministic tie-breaking
- fail closed on malformed critical input
- exactly 20 systems

## ACCEPTANCE CRITERIA
1. compile/static validation passes
2. all executable tests pass
3. tests cover Q64 range/zero-divide/overflow boundaries
4. all 20 systems have at least one positive and one negative/edge test
5. aggregate compiler is deterministic under input permutation where semantics are order-independent
6. no exported function performs KEEP/CUT, promotion, Canon mutation or NEXY state transition
7. design maps each system to code and test evidence
8. persisted bytes are read back after GitHub write

## STOP CONDITIONS
- required correctness would need a NEXY.AI mutation
- authoritative source conflict changes the intended authority boundary
- test failure cannot be fixed without weakening immutable requirements
- current repo identity changes materially and invalidates evidence

## STATUS
IN_PROGRESS
