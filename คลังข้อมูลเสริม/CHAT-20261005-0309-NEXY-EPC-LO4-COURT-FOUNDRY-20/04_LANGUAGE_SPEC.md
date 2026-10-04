# CourtScript-Q64 Language Profile v0.1

## Grammar shape
```text
POLICY <ID>
AUTHORITY ADVISORY_ONLY
PIN <SPEC_HASH|NEXY_COMMIT_SHA|AI_CONTEXT_COMMIT_SHA>
PROOF <proof-name>
GUARD <guard-name>
REQUIRE <metric> <GE|LE> <unit-Q64-decimal> CODE <ID>
SCORE <ID> WEIGHTED <metric> <positive-int-weight> ...
RECOMMEND <KEEP_REVIEW|CUT_REVIEW> IF <score-id> <GE|LE> <unit-Q64-decimal> ELSE DEFER
END
```

## Example KEEP review policy
```text
POLICY EPC_KEEP_REVIEW_V1
AUTHORITY ADVISORY_ONLY
PIN SPEC_HASH
PIN NEXY_COMMIT_SHA
PIN AI_CONTEXT_COMMIT_SHA
PROOF PINNED_EVIDENCE
PROOF EXECUTED_TEST
GUARD NONCOMPENSATORY
REQUIRE CANON_COMPATIBILITY GE 0.90 CODE CANON_FLOOR
REQUIRE SECURITY_IMPACT GE 0.80 CODE SECURITY_FLOOR
REQUIRE DETERMINISM_IMPACT GE 0.90 CODE DETERMINISM_FLOOR
SCORE COURT WEIGHTED ARCHITECTURE_FIT 7 CANON_COMPATIBILITY 10 NOVELTY 5 OVERLAP 5 IMPLEMENTATION_VALUE 8 VERIFICATION_VALUE 8 SECURITY_IMPACT 10 DETERMINISM_IMPACT 10 MAINTENANCE_COST 4
RECOMMEND KEEP_REVIEW IF COURT GE 0.72 ELSE DEFER
END
```

## Forbidden semantics
There is no syntax/opcode for Canon write, CORE/JUDGE/LAW mutation, deployment, filesystem/network/process access, arbitrary function execution, automatic vote consumption, physical deletion, or auto-promotion.

## Resource bounds
- source ≤ 65,536 characters;
- tokens ≤ 4,096;
- requirements ≤ 128;
- score terms ≤ 64;
- VM bytecode instructions ≤ 512.
