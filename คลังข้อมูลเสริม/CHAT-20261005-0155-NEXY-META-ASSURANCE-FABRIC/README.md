# NEXY Meta-Assurance Fabric

**Status:** PROPOSAL + standalone tested prototype. Not a NEXY.AI requirement, implementation, runtime feature, or deployment claim.

**Chat reference:** `CHATREF-20261005-0155-NEXY-META-ASSURANCE-FABRIC`  
**Mission:** `MISSION-NEXY-META-ASSURANCE-20261005-0155-A`

This package contains five deliberately orthogonal assurance mechanisms intended for possible future integration around a deterministic, verify-only control hub such as NEXY. It lives only in `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/` and does not modify a repository whose name contains `NEXY.AI`.

## The five proposals

1. **Metamorphic Verification Synthesizer (MVS)**  
   Verifies relations between multiple executions when a full expected-output oracle is unavailable or too expensive. It never treats a relation as authority merely because it was generated; relations must be explicitly supplied/approved.

2. **Conservation-Law Ledger (CLL)**  
   Detects undeclared creation or destruction of conserved state such as budget units, quota, ownership units, credits, capability counts, or balances across transitions.

3. **Minimal Proof Witness Extractor (MPWE)**  
   Computes a deterministic minimum-cost evidence cover for a bounded requirement set. It can reduce evidence volume without reducing declared coverage. Exact weighted set cover is NP-hard; this prototype is intentionally bounded by practical input size rather than pretending complexity disappeared.

4. **Behavioral Fingerprint Kernel (BFK)**  
   Produces canonical SHA-256 fingerprints of scenario→outcome behavior and a precise added/removed/changed/unchanged diff. It is designed to detect semantic drift across versions independent of source-file layout.

5. **Specification Mutation Sentinel (SMS)**  
   Mutation-tests policy/spec validators by generating controlled invalid variants and checking that the validator rejects every one. Surviving mutations expose guardrails that look present in prose but are not actually enforced.

## Why this is useful to NEXY-style systems

These mechanisms target five different blind spots:
- incomplete test oracle;
- hidden state creation/destruction;
- evidence overload;
- behavior drift hidden by implementation changes;
- guardrails that are never challenged by negative tests.

They complement, rather than replace, normal unit/integration/E2E/runtime verification. A PASS here proves only the proposition tested by the relevant mechanism.

## Core invariants
- deterministic output for identical input;
- explicit malformed-input failure;
- no hidden network, filesystem, environment, process, clock, or randomness in core modules;
- canonical ordering where result order matters;
- explicit negative-path behavior;
- no silent fallback from invalid definitions;
- proposal status never promoted into NEXY authority by this package.

## Run

```bash
PYTHONPATH=src python3 -m compileall -q src tests
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Observed during development: Python 3.13.5, compileall PASS, 31/31 unittest methods PASS.

See `04_TEST_EVIDENCE.md` for evidence scope and limitations.
