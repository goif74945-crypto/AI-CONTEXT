# Local Test Evidence

> **AI-PROPOSED / EXPERIMENTAL auxiliary project evidence. NOT evidence of NEXY.AI runtime/deployment correctness.**

## Evidence boundary

This report records only sandbox execution of NEXY ProofGraph Lab. It does not establish implementation, runtime, deployment, security, or robotics claims for NEXY.AI.

## Executed evidence

- Python source/test compilation via `python -m compileall -q src tests`.
- Unit/integration suite via `python -m unittest discover -s tests -v`.
- Integration self-scan on a corpus rooted at `คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-PROOFGRAPH-LAB`.
- Graph generation, impact calculation, truth-lock creation, and truth-lock verification executed locally.

## Defect/recovery history

1. Initial truth-lock traversal test failed because `lstrip("./")` incorrectly transformed `../outside.md`. Root cause fixed by rejecting absolute/`..` path components before normalization.
2. Initial integration self-scan found false positives in Current Build count detection. Root cause fixed by standalone-number tokenization and nearest-number association with the `Current Build` phrase; regression tests added.

## Current local status

Final local verification before repository write:

- compileall: **PASS**;
- unittest suite: **23/23 PASS**;
- integration self-scan: **15 documents, 0 INFO, 0 WARNING, 0 ERROR, 0 CRITICAL**;
- generated link graph: **15 nodes / 18 edges**;
- impact closure for `DESIGN.md`: itself at depth 0, `INDEX.md` and `README.md` at depth 1;
- truth-lock create + verify: **PASS** for two locked files;
- wheel build: **PASS**;
- isolated target install/import/CLI help smoke: **PASS**.

Repository insertion is separate E0 evidence and must be verified against the resulting Git commit.
