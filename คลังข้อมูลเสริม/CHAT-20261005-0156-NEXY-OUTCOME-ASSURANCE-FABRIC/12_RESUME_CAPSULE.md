# Resume Capsule

Execution namespace: `CHAT-20261005-0156-NEXY-OUTCOME-ASSURANCE-FABRIC`

## Durable state
- Target repository: `goif74945-crypto/AI-CONTEXT`.
- Mutable scope: this namespace only.
- Every repository whose name contains `NEXY.AI` is protected from mutation.
- Theme: user-level post-execution Outcome Assurance.
- Five engines: OCC, ODV, OSF, BRG, ORP.
- Reference implementation language: Python 3.11+ stdlib only.
- All concepts are AI-proposed experimental context, not NEXY canon.

## Known repaired defects
- Pareto unit-test oracle was wrong; corrected without engine weakening.
- Non-finite invalid observation corrupted canonical report hashing; repaired with normalized null + explicit invalid-observation path.

## Reproduction

```bash
PYTHONPATH=src python -m compileall -q src tests tools
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python tools/benchmark.py
```

## Integration boundary
Use OAF only through a future adapter that preserves NEXY authority, observation provenance, User Law, evidence requirements, and side-effect authorization. ORP never executes its plans.
