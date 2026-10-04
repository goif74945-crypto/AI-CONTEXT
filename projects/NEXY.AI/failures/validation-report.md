# Failure / Recovery Library Validation

## Result
**PASS — engineering failure intelligence registry**

Records: **21**

Rules:
- failure records preserve failed approaches, not only successful fixes;
- recovery never erases provenance;
- REVIEW_REQUIRED records are not treated as proven defects until dedicated audit;
- every recovery must point to regression/prevention obligations;
- stale evidence is itself a reusable failure class.

This library is not conversational memory. It is structured engineering experience for builder/auditor workflows.


## 2026-10-05 exact-head audit additions

Added four revision-bound engineering failure classes from the read-only audit at NEXY.AI- commit `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`:

- `FAIL-TSA-INGRESS-001` — fail-closed TSA elapsed-time consumers without an observed production injection path; runtime impact remains not E5-verified.
- `FAIL-VALIDATION-EXPERIMENTAL-COUPLING-001` — blocking Docker validation conflicts with advisory Phase-F workflow authority.
- `FAIL-EVIDENCE-SKIPPED-STATUS-002` — green status is non-proof when the exact-commit provider deployment is SKIPPED.
- `FAIL-COVERAGE-TIME-AUTHORITY-001` — exact-head validation can remain blocked after all measured tests pass because Core branch coverage is below its configured threshold.

Validation discipline:
- source blocker claims remain revision-bound;
- runtime consequences are not promoted beyond observed evidence level;
- recovery designs preserve fail-closed determinism and do not reintroduce host-clock authority;
- exact-head release truth requires executed artifact binding, not status color alone.
