# Adoption Gates

This prototype should remain outside NEXY.AI until all applicable gates pass.

1. **Schema gate**: versioned schema + compatibility tests exist.
2. **Adapter equivalence gate**: stable/candidate inputs are proven semantically equivalent before comparison.
3. **Isolation gate**: shadow path has no execution credentials/capability.
4. **Scale gate**: memory/time behavior measured on representative corpus sizes.
5. **False-block analysis**: authorized positive divergences have a governed rebaseline workflow.
6. **False-pass mutation suite**: deliberately remove authority/evidence/freeze semantics and confirm gate fails.
7. **Privacy gate**: report/record fields are reviewed for sensitive metadata leakage.
8. **Exact-revision gate**: every report is bound to stable/candidate revision and policy fingerprint.
9. **Operational gate**: timeout/partial-data semantics defined; partial comparison cannot PASS.
10. **Human authority gate**: promotion remains an explicit controlled decision, not an automatic side effect of PASS.

Current state: prototype satisfies only a subset via local E1/E2 tests; production gates remain NOT_VERIFIED.
