# PAREX Metric Integrity Admission — Evidence

**Status: PASS for the standalone experimental artifact at the tested bytes**  
**Classification: AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION**

## Target lock

- Repository: `goif74945-crypto/AI-CONTEXT`
- Writable root: `คลังข้อมูลเสริม/CHAT-20261005-0157-NEXY-FRONTIER-ASSURANCE-LAB/`
- Tested code commit: `14d810a151851f155b41ac3bc67f0ea77c3cb176`
- Execution source: detached Git worktree checked out at that exact commit
- Environment: Python 3.12.14; Linux 6.18.44 x86_64
- Protected repository write actions: none

## Reproduced gap

Before the extension existed, fresh execution constructed the original PAREX
`Plan` once with `float("nan")` and once with `True` in `benefit`. Both calls
returned `PASS`, frontier `['candidate']`, and the same result hash
`35a24e8d9976f30969ac1db4c0ac9b6939232038881c2ab1dc579bdcea18daca`.
This proves the narrow admission/binding gap; it does not invalidate valid
integer results from the original Pareto algorithm.

## TDD and repair record

1. The new 18-test suite was executed before implementation and failed 18/18
   because `parex_metric_integrity` was absent.
2. Minimal implementation made the focused suite pass 18/18.
3. Self-audit added two fail-closed cases. They exposed `AttributeError` for a
   foreign candidate and `TypeError` for an unhashable evidence axis.
4. Validation was reordered ahead of sorting/set conversion. Both regression
   cases then passed, and the focused suite passed 20/20.

No assertion, test selection, or acceptance threshold was weakened.

## Fresh exact-commit verification

Executed from the mission root in detached commit
`14d810a151851f155b41ac3bc67f0ea77c3cb176`:

```text
python3 -m compileall -q frontier_assurance_lab.py obsure_runtime_assurance.py recert_path_integrity.py ghostedge_campaign_assurance.py parex_metric_integrity.py test_frontier_assurance_lab.py test_obsure_runtime_assurance.py test_recert_path_integrity.py test_ghostedge_campaign_assurance.py test_parex_metric_integrity.py

python3 -m unittest -v test_frontier_assurance_lab.py test_obsure_runtime_assurance.py test_recert_path_integrity.py test_ghostedge_campaign_assurance.py test_parex_metric_integrity.py
```

Observed:

- compile: `PASS` (exit 0)
- tests: `96/96 PASS` (20 new + 76 regression; exit 0)
- positive, negative, adversarial, determinism, and original-PAREX integration:
  `PASS`
- 100 input permutations returned an identical normalized result

Evidence classes: E1 compile, E2 unit/adversarial/determinism, E3 integration
with the original `ParetoPruner` inside this standalone artifact.

## Tested byte identity and persisted read-back

All three code-commit artifacts were read back through GitHub at the exact
tested commit and matched local tested bytes exactly:

| Artifact | Git blob SHA-1 | SHA-256 | Read-back |
|---|---|---|---|
| `PAREX_METRIC_INTEGRITY_DESIGN.md` | `95b3d4c3c20769db7a78628acb8b7de3ac73808a` | `fcd526fad89424ef75d563449d36bac4cc7609a07beba613a6cb78e04193c955` | EXACT_MATCH |
| `parex_metric_integrity.py` | `63dfdf1e88c290d2d651fefd424076dfa8fce456` | `dd8936bc175a1da5ff7672016d8fe3f5b92e0a94667b64a2781186d01c8be2e` | EXACT_MATCH |
| `test_parex_metric_integrity.py` | `3cc92dd05ca4b42bba08bbeb78817b0c8fbc83c2` | `bbca11ed63b87b43936119b19aeeaa300d4f155d7f40e9ea62c158a4fddd84de` | EXACT_MATCH |

## Claim boundary

This evidence proves only the standalone experimental artifact at the tested
bytes. It does not authenticate evidence references, prove metric truth, choose
a plan, authorize execution, establish deployment, promote Canon, or establish
implementation by NEXY.AI.
