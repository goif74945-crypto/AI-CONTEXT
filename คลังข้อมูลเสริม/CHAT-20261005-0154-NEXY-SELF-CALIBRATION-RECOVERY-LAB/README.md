# NEXY Self-Calibration & Recovery Lab

**Status:** EXPERIMENTAL / AI_PROPOSAL / NOT_NEXY_CANON  
**Repository target:** AI-CONTEXT supplemental knowledge only  
**Conversation identifier:** `PROJECT-CONVERSATION-2026-10-05T01:54+07:00`

This mission implements five standalone deterministic reference systems:

1. Contract Archaeologist
2. PauseSafe Kernel
3. Evidence Genealogy Engine
4. Failure Atomizer
5. Calibration Observatory

The code is designed for future adapter-based compatibility with NEXY.AI but is **not** installed into, imported by, or authoritative over any NEXY.AI repository.

## Local verification
Run from this directory:

```bash
python -m compileall -q .
python -m unittest discover -s . -p 'test_*.py' -v
python demo.py
python -m integration.benchmark_smoke
```

The benchmark is a local engineering smoke test, not a production SLA.

## Evidence classes
- E0: file presence and repository read-back
- E1: Python compileall
- E2: unit/adversarial tests
- E3-local: portfolio integration test and demo composition

Production NEXY integration/runtime/deployment evidence remains NOT_VERIFIED.
