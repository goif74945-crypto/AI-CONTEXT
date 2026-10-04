# Task Contract — EPC Computational Feasibility Proof Court 20

WORK_CODE: CHAT-20261005-0309-NEXY-EPC-CFPC20-61C51C
PLATFORM_NATIVE_CHAT_ID: UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS
AUTHORITY_CLASS: Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING

## Objective
Create exactly 20 deterministic Q64.64 proposal-feasibility proof mechanisms, execute real tests, preserve evidence, and publish only to a unique AI-CONTEXT namespace. The system must be reusable later as an advisory adapter for NEXY without modifying NEXY.AI.

## Protected scope
Every repository whose name contains NEXY.AI is read-only. Canon/Law/Core/JUDGE and production state are out of mutation scope.

## Immutable rules
- no automatic promotion or authority override;
- no binary floating point in authoritative resource math;
- overflow/divide-by-zero/unbound variables/unsupported grammar fail closed;
- hard resource limits are non-compensatory;
- no resource optimization may remove required verification;
- unsafe degradation freezes;
- published bytes must match tested bytes before PASS;
- design/standalone runtime/NEXY integration/deployment remain separate claims.

## Acceptance
Strict warning-as-error build under two compilers, unit/property/negative tests, deterministic replay, ASan/UBSan, source float scan, exact hashes, GitHub read-back and protected-repo recheck.
