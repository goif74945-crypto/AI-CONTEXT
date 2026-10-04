# Persistence Evidence

**Trace:** `CHAT-20261005-0222-NEXY-EPISTEMIC-INTEGRITY-QUINTET`

## Mutation boundary
Every write performed for this package targeted only:
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0222-NEXY-EPISTEMIC-INTEGRITY-QUINTET/`

No write action was issued to any repository whose name contains `NEXY.AI`.

## Publication-bundle runtime evidence
The compact bundle that was selected for GitHub publication was executed separately from the larger working lab before upload.

Environment: Python 3.13.5.

- `python run_tests.py` → compile gate PASS + 7/7 test methods PASS.
- `PYTHONHASHSEED=1 python -m unittest discover -s tests -v` → 7/7 PASS.
- `PYTHONHASHSEED=777 python -m unittest discover -s tests -v` → 7/7 PASS.
- The determinism property method contains 500 total seeded iterations: 100 each for ECOF, DMAG, PDZA, RKM and ACE.

The larger pre-publication working lab additionally executed 37/37 tests with two hash seeds and was used to discover/repair the two DMAG input-validation defects documented in `05_EVIDENCE_AND_LIMITATIONS.md`.

## Exact byte identity proof
Local Git-blob SHA calculations for the publication bytes were:

| Path | Local git-blob SHA | GitHub read-back blob SHA | Result |
|---|---|---|---|
| `epistemic_integrity.py` | `30e39979f0770cd021369a3a1f114894d4c2108a` | `30e39979f0770cd021369a3a1f114894d4c2108a` | PASS |
| `tests/test_reference.py` | `5cad700cfed98c03845e8fb236f8e24fc3ab0db8` | `5cad700cfed98c03845e8fb236f8e24fc3ab0db8` | PASS |
| `run_tests.py` | `8c2321e35f5218c1db2f11a64c154766f489d548` | `8c2321e35f5218c1db2f11a64c154766f489d548` | PASS |

This proves the executable code/tests/runner persisted on GitHub are byte-identical to the locally executed publication bundle.

## Read-back presence
GitHub directory read-back confirmed the design, mission memory, task contract, novelty audit, integration proposal, evidence/limitations, README, implementation, runner and tests directory on `main`.

## Evidence boundary
Persistence/read-back proves E0 identity/presence for the stored bundle and links it to local E1/E2 execution. It does not create NEXY E3/E4/E5/E6 integration/runtime/deployment evidence.
