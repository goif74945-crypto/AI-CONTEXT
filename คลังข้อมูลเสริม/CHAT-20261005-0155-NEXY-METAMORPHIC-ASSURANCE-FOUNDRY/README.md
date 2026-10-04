# NEXY Metamorphic Assurance Foundry (NMAF)

Chat reference: `CHAT-20261005-0155-NEXY-METAMORPHIC-ASSURANCE-FOUNDRY`
Status: **EXPERIMENTAL / PROPOSAL / standalone**
Storage: AI-CONTEXT `คลังข้อมูลเสริม` only
NEXY.AI mutation in this task: **FORBIDDEN**

NMAF is a deterministic assurance toolkit for finding semantic regressions that ordinary example tests can miss. It is deliberately decoupled from NEXY implementation and integrates only through caller-owned fixtures/executor adapters.

Implemented proposals: Metamorphic Relation Engine, Deterministic Counterexample Minimizer, Oracle Independence Auditor, Proof-Weighted Deterministic Test Scheduler, and Semantic Failure Fingerprint.

Run:
```bash
python -m py_compile nmaf.py test_nmaf.py demo.py
python -m unittest -v test_nmaf.py
python demo.py
```

A metamorphic relation is legal only when an authoritative contract establishes what the transformation means. NMAF must not invent semantics. It produces evidence; NEXY authority decides release/freeze.
