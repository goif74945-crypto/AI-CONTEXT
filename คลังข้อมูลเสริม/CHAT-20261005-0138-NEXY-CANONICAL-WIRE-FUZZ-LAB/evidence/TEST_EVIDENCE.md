# Verification Evidence

Target: distilled release set intended for `goif74945-crypto/AI-CONTEXT`.

## E1 static
Command: `python -m compileall -q src tests`  
Expected: exit 0.  
Observed: PASS.

Static purity check inside unit suite parses `src/ncw.py` AST and rejects imports from a named side-effect set including filesystem/process/network/clock/random/database modules. Observed: PASS. Limitation: not a formal non-interference proof.

## E2 unit
Command: `PYTHONPATH=src python -m unittest discover -s tests -v`  
Observed: PASS — 21/21 tests.  
Coverage families include supported round-trip, 720 map permutations, i128 boundaries, strict duplicate JSON keys, NFC collisions, float/NaN/Infinity rejection, malformed wire, noncanonical map order, resource limits, golden vectors, and >150 generated small-domain cases.

## Evidence boundary
These results prove only this reference release content in the local sandbox. Cross-language, cross-architecture, integration, production runtime, WAL durability, and deployment remain NOT_VERIFIED.
