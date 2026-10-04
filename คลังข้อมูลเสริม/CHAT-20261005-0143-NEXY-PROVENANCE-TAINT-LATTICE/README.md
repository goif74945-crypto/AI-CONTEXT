# NEXY Provenance Taint Lattice Lab

**AI-PROPOSED CONCEPT. Not canonical NEXY.AI law. Not integrated into the NEXY.AI runtime.**

A standalone deterministic reference kernel that prevents authority, provenance, and assurance laundering through chained AI/tool transformations.

## Why it exists

A model output can be rewritten, summarized, merged, translated, cached, re-ranked, and passed through many tools. None of those transforms should silently convert weak or unknown provenance into trusted evidence. The lab treats trust as lineage-bound state rather than presentation metadata.

## Core invariants

1. Authority floor never increases through ordinary transforms.
2. Derived assurances are the intersection of parent assurances and an explicit transform preservation allowlist.
3. Taints propagate monotonically through ordinary transforms.
4. Protected taints cannot be erased by a generic verification receipt.
5. Verification receipts bind to the exact content-addressed artifact identity.
6. Verification may add assurances but does not rewrite source authority.
7. Release is deterministic: `ALLOW` or `FREEZE` plus stable reason codes.
8. Evidence requirements are exact assurance tags; E0–E7 are not treated as a universal numeric ladder.

## Run

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

No third-party runtime dependency is required.

## Verified lab state

Final local verification for this snapshot:
- compile/static import path: PASS;
- unit/property/wire tests: 53/53 PASS;
- deterministic demo: PASS across two executions;
- placeholder audit: PASS;
- integration into NEXY.AI: NOT VERIFIED / intentionally out of scope.

See `EVIDENCE.md` and `FINAL_AUDIT.md` for exact limits.
