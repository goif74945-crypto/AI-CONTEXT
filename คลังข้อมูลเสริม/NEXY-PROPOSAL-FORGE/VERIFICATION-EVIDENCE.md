# Verification Evidence

## Status

`PASS` for the supplemental tool's stated local acceptance criteria.

This is **not** evidence that NEXY.AI itself is implemented, correct, deployable, or changed. The NEXY.AI repository was not mutated.

## Environment observation

- Python: `3.13.5`
- Execution environment: isolated task container
- Network dependency for core/tests: none
- Third-party runtime dependencies: none

## Commands executed

```bash
python3 -m compileall -q src tests scripts
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m nexy_proposal_forge evaluate examples/proposal-forge-self.json --catalog examples/catalog.synthetic.json
PYTHONPATH=src python3 -m nexy_proposal_forge collide examples/work-manifest.current.json --catalog examples/work-manifests.synthetic.json
PYTHONPATH=src python3 scripts/benchmark_catalog.py
```

## Results

- Python compileall: `PASS`
- JSON parse for schema, work manifest, and all JSON examples: `PASS`
- Unit/CLI regression tests: `29/29 PASS`
- Valid self-proposal result: `PROMOTE_FOR_HUMAN_REVIEW`
- Self-proposal advisory-only: `true`
- Self-proposal authoritative: `false`
- Self-proposal evidence gaps: `0`
- Self-proposal SHA-256 fingerprint: `4cae16464022fb59c8ded107656c8e343b4b22ddfcd7c8af5cbe7be1535f2b6f`
- Synthetic work-manifest collision result: `CLEAR`
- 837-entry synthetic catalog deterministic repeat: `true`
- 837-entry local elapsed observation: `70,079,619 ns` (~70.08 ms)

## Evidence boundary

The 837-entry benchmark catalog is synthetic. Its size intentionally matches the current normalized NEXY requirement-row denominator only as a scale probe. The synthetic entries are **not** NEXY requirements and the timing is **not** a production SLA.

The low-overlap score for the self-proposal is also not proof of global novelty. It proves only the behavior of the deterministic comparison algorithm against the supplied catalog.

## Tested failure behavior

The suite verifies that:

- invalid approved-like proposal status is rejected;
- unknown proposal/evidence/manifest fields are rejected;
- duplicate evidence IDs are rejected;
- floating-point canonical data is rejected;
- normalized key collisions are rejected;
- exact duplicate candidates are rejected;
- near duplicates cannot silently pass as novel;
- reused proposal identity with divergent content freezes;
- missing evidence yields `NEEDS_EVIDENCE`;
- declared authority conflict yields `FREEZE_CONFLICT`;
- overlapping active write scopes produce `COLLISION`;
- inactive completed manifests do not masquerade as active locks;
- parent-traversal write scopes are rejected;
- repeated evaluation serializes identically.
