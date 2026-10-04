# NCIF Validation Plan

**Classification:** REFERENCE ARTIFACT VALIDATION

## Claim classes

### C1 — static validity
Required: E1.

Checks:
- Python compile for `src`, `tests`, `scripts`;
- JSON parse for schema and fixtures.

### C2 — defined reference behavior
Required: E2.

Checks include:
- distinct roots produce distinct support groups;
- same root cannot multiply independence;
- evidence ancestry propagates root correlation;
- same source identity under cloned evidence IDs collapses;
- explicit correlation key collapse;
- transitive bridge collapse;
- missing parent / cycle fail closed;
- evidence-less material vote freezes;
- independent opposition blocks under default policy;
- abstention is neutral;
- duplicate identity / unknown references reject;
- input order invariance and deterministic fingerprint;
- single-root resilience behavior;
- same-root stance conflict;
- deep lineage does not depend on recursion;
- raw provenance identity/key is not echoed.

### C3 — bounded broader behavior
Evidence: local deterministic audit, not universal proof.

`bounded_audit.py` enumerates 6,561 bounded combinations and validates invariants around independent-root counting and correlated-agent inflation.

### C4 — structural stress
Evidence: local stress only.

`stress_audit.py` checks:
- 5,000-node deep lineage;
- 5,000 support votes distributed over 500 unique roots;
- expected 500 independent groups.

This is not a latency benchmark, memory guarantee, production load test, or DoS proof.

### C5 — CLI contract

- independent fixture returns JSON candidate and exit 0;
- correlated false-consensus fixture returns JSON freeze and exit 2.

## Regression law

Any material source/policy change invalidates prior E1/E2 evidence. Re-run `python scripts/verify.py` and regenerate evidence before claiming PASS.

## Evidence exclusions

The following are explicitly not proven:

- NEXY integration;
- production runtime behavior;
- production deployment;
- correctness/authenticity of caller-declared provenance;
- hidden common-cause discovery;
- unbounded graph behavior;
- universal security;
- WCAG/UI behavior;
- policy suitability for a real deployment.
