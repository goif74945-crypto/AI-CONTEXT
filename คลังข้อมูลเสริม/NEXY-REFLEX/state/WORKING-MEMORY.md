# NEXY-REFLEX Working Memory / Resume Capsule

## Mission
- mission_id: `NXR-20261005-0137-REFLEX`
- chat_platform_id: `UNKNOWN_NOT_EXPOSED_TO_MODEL`
- persistence_mode: `DURABLE_RESUMABLE` once GitHub read-back succeeds
- target_repository: `goif74945-crypto/AI-CONTEXT`
- write_root: `คลังข้อมูลเสริม/NEXY-REFLEX/`
- protected_repositories: any repository name containing `NEXY.AI`

## Current architecture
Standalone Python 3.11+ verifier. No runtime dependencies. JSON input/output. Core modules:
- `canonical.py`: stable canonical JSON and SHA-256;
- `models.py`: immutable typed snapshot/evidence/decision models;
- `engine.py`: structural, authority, dependency and evidence gate;
- `impact.py`: conservative dependency-aware evidence invalidation;
- `cli.py`: evaluate/replay/diff interface.

## Locked semantics
- authority_order is explicit caller input; REFLEX never invents it;
- same highest authority + different values => CONFLICT;
- exact evidence class acceptance; no E-number substitution heuristic;
- revision/digest mismatch => stale;
- non-current/deferred scopes are traceable but non-gating;
- any non-PASS gate verdict => FREEZE_RECOMMENDED;
- no mutation of NEXY.

## Verification required before COMPLETE
1. `python -m compileall -q src tests`
2. `PYTHONPATH=src python -m unittest discover -s tests -v`
3. CLI PASS example returns 0 and PASS.
4. CLI conflict example returns 2 and CONFLICT.
5. replay digest is stable.
6. post-write GitHub read-back matches tested source bundle hashes.

## Resume rule
If source changes after tests, invalidate prior static/unit evidence and rerun all checks before claiming PASS.
