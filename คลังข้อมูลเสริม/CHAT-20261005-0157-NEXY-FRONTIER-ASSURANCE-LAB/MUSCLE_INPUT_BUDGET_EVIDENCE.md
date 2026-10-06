# MUSCLE Input & Search-Budget Assurance — Evidence

**Status: PASS for the standalone experimental artifact at the tested bytes**  
**Classification: AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION**

## Target lock

- Repository: `goif74945-crypto/AI-CONTEXT`
- Writable root: `คลังข้อมูลเสริม/CHAT-20261005-0157-NEXY-FRONTIER-ASSURANCE-LAB/`
- Tested code commit: `dd52f6a8668b402272d585528e0ea3dda25c2942`
- Execution source: detached Git worktree checked out at that exact commit
- Environment: Python 3.12.14; Linux 6.18.44 x86_64
- Protected repository write actions: none

## Reproduced gaps

Fresh execution against the original MUSCLE established:

1. `NEQ("saef")` against domain `("safe", "fast")` returned `SAT` with the
   domain unchanged instead of rejecting the unknown literal.
2. Two semantically different constraints using the same IDs and equivalent
   final behavior can produce the same original result hash because constraint
   definitions are absent from the output hash.
3. The original maximum of 22 constraints per variable permits a theoretical
   upper bound of `2^22 - 1 = 4,194,303` non-empty subset checks without a
   caller-declared subset-check budget.

These findings are bounded to the inspected standalone implementation.

## TDD and remediation record

1. The new 20-test suite was executed before implementation and failed 20/20
   because `muscle_input_assurance` was absent.
2. Minimal implementation made the focused suite pass 20/20.
3. Logical Role Court security/resource review found that arbitrary iterables
   could hang before budget admission. A new regression test failed because a
   generator was accepted.
4. The adapter was restricted to finite built-in list/tuple collections. The
   regression passed and the focused suite passed 21/21.

No assertion, test selection, or budget threshold was weakened.

## Fresh exact-commit verification

Executed from the mission root in detached commit
`dd52f6a8668b402272d585528e0ea3dda25c2942`:

```text
python3 -m compileall -q frontier_assurance_lab.py obsure_runtime_assurance.py recert_path_integrity.py ghostedge_campaign_assurance.py parex_metric_integrity.py muscle_input_assurance.py test_frontier_assurance_lab.py test_obsure_runtime_assurance.py test_recert_path_integrity.py test_ghostedge_campaign_assurance.py test_parex_metric_integrity.py test_muscle_input_assurance.py

python3 -m unittest -q test_frontier_assurance_lab.py test_obsure_runtime_assurance.py test_recert_path_integrity.py test_ghostedge_campaign_assurance.py test_parex_metric_integrity.py test_muscle_input_assurance.py
```

Observed:

- compile: `PASS` (exit 0)
- tests: `117/117 PASS` (21 new + 96 regression; exit 0)
- positive, negative, adversarial, determinism, budget-boundary, and
  original-MUSCLE integration: `PASS`
- 100 input permutations returned an identical normalized result

Evidence classes: E1 compile, E2 unit/adversarial/determinism, E3 integration
with the original `ConstraintEngine` inside this standalone artifact.

## Tested byte identity and persisted read-back

All three code-commit artifacts were read back through GitHub at the exact
tested commit and matched local tested bytes exactly:

| Artifact | Git blob SHA-1 | SHA-256 | Read-back |
|---|---|---|---|
| `MUSCLE_INPUT_BUDGET_DESIGN.md` | `eb1495536ed57156660109e352a0d1c827b87d33` | `36408a25835049f9c7d6ec339758f1e0e2ee336af4c716b92b177d12d07c0187` | EXACT_MATCH |
| `muscle_input_assurance.py` | `6440d97ef733fce6ad62e223e96bb1372550c504` | `2e2e851719f760f216257a2897f26aefefa12364cedc6ee714d9b7a10f2be26c` | EXACT_MATCH |
| `test_muscle_input_assurance.py` | `93a7c4d3c899ec86a8d88be7d8f7ab0f1465f7b6` | `6482dd8192b428bdc1d05958ff3c8eb961d0f8f87998ce4f54869f07c3fb66df` | EXACT_MATCH |

## Court record and claim boundary

- Execution mode: `LOGICAL_ISOLATION` (no claim of independent agents).
- Independent finding: arbitrary-iterable resource boundary; resolved and
  reverified.
- Truth Sentinel: material claims above bind to command output, commit, and
  read-back receipts; `TRUTH_PASS` for this narrow standalone slice.
- Judge: `PASS` for the stated design/test contract at the tested bytes.

This evidence does not prove caller policy truth, runtime performance,
deployment, Canon promotion, or implementation by NEXY.AI. The subset count is
a conservative deterministic upper bound, not measured operational work.
