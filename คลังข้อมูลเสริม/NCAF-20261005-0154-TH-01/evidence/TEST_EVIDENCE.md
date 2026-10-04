# NCAF Verification Evidence

classification: `AI_PROPOSED_CONCEPT_NOT_ADOPTED`
work_session_id: `NCAF-20261005-0154-TH-01`

## E1 — Static compilation
Claim: all Python source/test files parse and compile under the available Python runtime.
Command: `python -m compileall -q src tests`
Observed: `COMPILEALL_OK`
Status: PASS
Limit: this does not prove runtime behavior.

## E2 — Unit + adversarial behavior
Command: `PYTHONPATH=src python -m unittest discover -s tests -v`
Observed: `Ran 19 tests ... OK`
Status: PASS
Coverage themes:
- CBA dependency closure, mandatory overflow, cycle rejection.
- ECR strong resolution, conflict freeze, mixed-key rejection.
- PRP Pareto dominance and hard no-eligible failure.
- REJ valid replay, illegal transition atomic rejection, hash tamper detection.
- FCE open/block/probe/recovery and failed-probe reopen.
- advisory envelope authority and non-mutation boundary.

## Seeded randomized invariant campaign
Deterministic seeds were used for reproducibility.
- CBA: 1,000 randomized cases.
- ECR: 1,000 randomized cases.
- PRP: 1,000 randomized cases.
- FCE: 1,000 randomized cases.
- REJ: targeted multi-position hash tamper cases.
Observed: all passed inside the same 19-test suite.
Status: PASS (E2 reference lab)

## E3-like local cross-module smoke
Command executed a single process path: CBA → ECR → PRP → REJ → FCE.
Observed payload:
`{'context': ('system_spec', 'task_context'), 'resolved': 'safe-route', 'route': 'remote', 'journal_events': 3, 'circuit': 'CLOSED'}`
Status: PASS for local component composition only.
Evidence class note: this is not NEXY runtime integration and must not be promoted as production E3.

## Regression boundary
No code in `goif74945-crypto/NEXY.AI-` was changed. Therefore NEXY regression testing is out of scope and no claim is made about it.
