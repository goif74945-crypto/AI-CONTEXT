# MMCRC20 Integration Contract

MMCRC20 is designed as an external/shadow verifier around captured adapter manifests and provider traces. A future NEXY integration may export read-only normalized adapter metadata and execution receipts into this court and hand the resulting capsule to the existing authority path. MMCRC20 itself must never import a mutable NEXY repository interface or own a state transition.

Inputs: canonical adapter manifest; exact NEXY commit; canonical NEXY-IGNIS SHA-256; captured trace fields relevant to current AgentAdapter; explicit mode/context/timeout/criticality policy; provenance-bearing evidence; explicit model identity pins/approval.

Outputs: per-mechanism PASS/FAIL + Q64 measurements; differential witnesses; deterministic replay SHA-256; `QUALIFIED_FOR_EXTERNAL_REVIEW` or `FREEZE_NOT_QUALIFIED`; always `authority_mutation_allowed=false` and `promotion_allowed=false`.

Failure semantics are fail-closed. Missing authority, malformed evidence, invalid Q64, insufficient failover diversity, unapproved model drift, untested cancel behavior, or hard contract divergence cannot be repaired by score or hidden fallback.

Compatibility pins:
- NEXY repo: goif74945-crypto/NEXY.AI-
- branch: NEXY.ai
- commit: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
- NEXY-IGNIS SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
- normalized matrix: 837 rows

Any relevant contract change after those pins makes compatibility evidence stale and requires rerun.
