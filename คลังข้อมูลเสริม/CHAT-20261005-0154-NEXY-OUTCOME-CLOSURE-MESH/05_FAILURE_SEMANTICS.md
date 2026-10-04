# Failure Semantics

Status: AI_PROPOSED_REFERENCE

| Module | Condition | Result | Why |
|---|---|---|---|
| Outcome Closure | malformed IDs/duplicate predicates/unknown observed predicate | FREEZE | contract identity is ambiguous |
| Outcome Closure | required UNKNOWN/violated/evidence deficit | OPEN | outcome cannot close |
| Outcome Closure | forbidden SATISFIED | FREEZE | explicit forbidden condition occurred |
| Outcome Closure | forbidden UNKNOWN or absent | OPEN | absence cannot be invented |
| Progress Truth | duplicate/blank obligation identity | FREEZE | progress accounting cannot be trusted |
| Progress Truth | BLOCKED present | BLOCKED | user-facing closure is obstructed |
| Progress Truth | UNKNOWN present | NOT_VERIFIED | evidence status is unresolved |
| Reversible Probe | malformed planning problem | FREEZE | optimization domain is invalid |
| Reversible Probe | irreversible candidate | reject candidate | evidence is not worth destructive guessing |
| Reversible Probe | reversible write without rollback | reject candidate | reversibility is unproven |
| Reversible Probe | insufficient authority | reject candidate | planning cannot mint authority |
| Reversible Probe | no safe cover / exact search bound exceeded | BLOCKED | no legal exact plan proven |
| Benefit Regression | missing required observed metric | INCONCLUSIVE | benefit is not observable |
| Benefit Regression | critical regression beyond tolerance | REJECT | improvement elsewhere cannot average away critical harm |
| Benefit Regression | no declared improvement | REJECT | change alone is not benefit |
| Benefit Regression | malformed axis contract | FREEZE | evaluation semantics are invalid |
| Adoption Readiness | protected scope mutation | FREEZE | task boundary was violated |
| Adoption Readiness | compatibility FAIL/upstream FREEZE | FREEZE | material contradiction |
| Adoption Readiness | compatibility UNKNOWN/missing proof/unverified rollback/unresolved collision | HOLD | review readiness not established |
| Adoption Readiness | all gates pass | READY_FOR_HUMAN_REVIEW | human authority remains required |

## Anti-gaming rules
- Never convert `UNKNOWN` to PASS because other checks are green.
- Never use pass ratio as estimated percent-complete time.
- Never classify irreversible operations as reversible merely because rollback documentation exists.
- Never call an axis “noncritical” after seeing a bad result; criticality belongs in the declared contract.
- Never omit an observed regression from output merely because the overall Benefit result is BENEFICIAL.
- Never interpret `READY_FOR_HUMAN_REVIEW` as approved, merged, deployed, canonical, or production-ready.
