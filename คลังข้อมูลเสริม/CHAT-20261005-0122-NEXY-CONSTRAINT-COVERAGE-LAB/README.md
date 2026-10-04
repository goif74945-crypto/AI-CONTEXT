# NCICS — NEXY Constraint Interaction Coverage Synthesizer

**Truth class:** `AI_PROPOSED / NOT_CURRENT_NEXY_REQUIREMENT`

NCICS is an isolated reference project stored under `AI-CONTEXT/คลังข้อมูลเสริม`. It is **not** a claim about the current NEXY.AI implementation.

## Why it exists

Requirement-to-test mapping answers “which existing tests appear related to which requirements?” NCICS answers a different question: “for a finite constrained state model, which concrete cases are required to cover every feasible t-wise interaction?”

That matters because many failures emerge only from combinations such as authority × core-state × surface × operation. Counting tests does not prove those interactions are covered.

## Fixture truth boundary

The included fixtures are **illustrative finite models**, not canonical executable NEXY contracts. They deliberately reuse current DOC-C/source vocabulary such as `OWNER`, `PUBLIC_USER`, `READY`, `FREEZE`, and source control surfaces, but their combinations/constraints are test examples only.

## Safety model

- explicit finite domains only;
- explicit forbidden partial assignments only;
- no `eval`, SAT-string execution, probabilistic sampling, or hidden inference;
- canonicalized parameter/value ordering;
- deterministic exact minimum set-cover proof for bounded small spaces;
- deterministic greedy compact set for larger but still exactly enumerable spaces;
- BLOCK instead of silent heuristic fallback when the user explicitly requests exact optimality beyond the exact-solver bound;
- BLOCK when configured enumeration bounds are exceeded.
- user-configurable bounds are themselves capped by fixed reference hard ceilings so a configuration cannot quietly disable resource safety.

## Reference commands

```bash
python -m py_compile src/ncics.py tests/test_ncics.py
python -m unittest discover -s tests -v
python tools/audit_artifacts.py
python tools/independent_verify.py fixtures/basic_pairwise.json /tmp/ncics-result.json
python src/ncics.py synthesize fixtures/basic_pairwise.json --pretty
python src/ncics.py synthesize fixtures/constrained_pairwise.json --output /tmp/ncics-result.json --pretty
python src/ncics.py verify fixtures/constrained_pairwise.json /tmp/ncics-result.json --pretty
```

## Evidence boundary

Successful local tests are E1/E2 evidence for this reference implementation only. They do not establish integration, runtime, end-to-end, or deployment evidence for NEXY.AI.
