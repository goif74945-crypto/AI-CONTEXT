# MPAL Verification Evidence

Status: `POST-WRITE VERIFIED / STANDALONE_REFERENCE_ONLY`

## Target
Standalone reference prototype only. No NEXY.AI implementation repository was tested or modified by this workstream.

## E1 compile proof
`python -m py_compile mpal_engine.py model_check.py tests/test_mpal_engine.py` → PASS.

## E2 unit/negative-path proof
`python -m unittest discover -s tests -v` → **49/49 PASS**.

Covered behaviors include policy/request validation, quorum satisfiability, requester authorization, ALLOW/PENDING/DENY/FREEZE paths, veto, duplicate/contradictory evidence, stale/future/inactive/self approvals, hash/version binding, role/group/domain mismatch, fingerprint stability, approval-order permutation invariance, and multiple rule examples.

## Coverage
Measured by unittest + model-check execution under branch coverage:
- `mpal_engine.py`: 90%
- `model_check.py`: 96%
- tests: 99%
- TOTAL: 94%

Coverage is not correctness proof.

## Bounded exhaustive model
Four evidence states for four principals: `NONE`, `APPROVE`, `DENY`, `EXPIRED_APPROVE`; total `4^4 = 256` vectors.

Observed:
- ALLOW: 4
- DENY: 112
- PENDING: 140
- FREEZE: 0 in the deliberately structurally-valid bounded model

Invariants PASS:
- input order invariance;
- veto dominance;
- ALLOW requires all configured quorums;
- requester self-approval excluded.

This is bounded exhaustive evidence for the fixture, not formal proof for arbitrary policies.

## Completion gate
After GitHub persistence: re-fetch committed bytes, rebuild a clean local workspace from them, rerun compile/tests/model-check, then record exact commit/file evidence in `99_FINAL_AUDIT.md`.


## Post-write closure
Critical GitHub blob identities were re-fetched and matched to the clean verification workspace. From those byte-identical inputs: py_compile PASS, unittest 49/49 PASS, bounded model 256 vectors PASS, engine coverage 90%, total coverage 94%, and CLI example ALLOW. See `08_GITHUB_BYTE_IDENTITY.json` and `99_FINAL_AUDIT.md`.
