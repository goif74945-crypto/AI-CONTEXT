# WORKFLOW — IMPLEMENTATION / REPAIR

## Goal
Produce the smallest complete implementation that satisfies the authorized contract and survives verification.

## Pipeline
`REFRESH → REPRODUCE → REQUIREMENT LEDGER → ROOT CAUSE → DAG → IMPLEMENT → TEST → REGRESSION → RE-AUDIT → EVIDENCE → CONTEXT`

## 1. Refresh
Inspect current target branch/ref/files and relevant tests/config.

## 2. Reproduce
Confirm the missing behavior/failure before repair when practical.

## 3. Requirement ledger
Map:
`requirement → authority → implementation location → evidence → status`

## 4. Root-cause graph
Do not treat every symptom as independent.
Collapse findings that share a root cause.

## 5. Dependency DAG
Order fixes so prerequisites land before dependents.
Parallelize only independent mutations/tests.

## 6. Implementation rules
- preserve existing invariants;
- avoid unrelated refactors;
- no speculative feature expansion;
- no hidden fallback;
- no fake implementation stubs presented as complete behavior;
- preserve compatibility unless change is authorized.

## 7. Validation sequence
1. syntax/schema;
2. type/static;
3. focused tests;
4. integration;
5. E2E/runtime if required;
6. regression;
7. final diff/state inspection.

## 8. Failure loop
If verification fails:
`capture failure → update defect graph → repair root cause → rerun required evidence`

Do not stop after first repair if the requested scope is whole-project convergence.

## 9. Completion
COMPLETE only when:
- all in-scope requirements have valid status;
- required evidence class exists;
- no unresolved regression invalidates result;
- protected scope unchanged;
- final state recorded.

## 10. Context write-back
Persist:
- decisions;
- new invariants;
- current status;
- exact blockers;
- evidence references;
- reproducible commands;
- remaining work.
