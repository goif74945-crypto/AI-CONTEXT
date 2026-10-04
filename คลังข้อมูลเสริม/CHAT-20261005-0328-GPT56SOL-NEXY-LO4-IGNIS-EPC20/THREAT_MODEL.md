# THREAT_MODEL

Protected assets: authority boundaries, scope truth, deterministic quantitative decisions, user-visible state/error/replay truth, cancellation/revocation completeness, audit/evidence lineage, ownership export coverage, and secret material.

Threats and controls:
1. Authority confusion: Lo4 PASS is never execution/release authority.
2. Malformed/host-dependent input: strict canonicalization and fail closed.
3. Numeric corruption: checked Q64.64; overflow/div0/float fail closed.
4. Omission attacks: completeness sets where inventories are supplied; production needs sealed inventories.
5. Replay ambiguity: exact identity, explicit replay disclosure, no timeout=failure assumption.
6. Presentation deception: S05/S06/S08/S09/S10/S14/S15/S18.
7. Residual execution/authority: S07/S17.
8. Secret leakage: S11 records offending key only, never secret value.
9. Order nondeterminism: canonical ordering plus S20.
10. Semantic duplication: collision scan and targeted neighbor review; novelty remains PARTIAL/UNKNOWN.

Residual risk: hash identity is not semantic truth; standalone E2 evidence is not live NEXY integration/deployment proof.
