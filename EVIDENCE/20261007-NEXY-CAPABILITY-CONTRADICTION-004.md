# Evidence — NEXY Gateway Capability Contradiction

EVIDENCE_ID: EVIDENCE-20261007-NEXY-CAPABILITY-CONTRADICTION-004
TASK_ID: 20261007-NEXY-CAPABILITY-CONTRADICTION-004
MODE: EXECUTE_NOW / ENGINEERING / EVIDENCE_DRIVEN / FAIL_CLOSED
STATUS: BLOCKED_WITH_RESUME
OBSERVED_UTC: 2026-10-07T16:04:52Z

## Target

- Repository: `goif74945-crypto/NEXY.AI-`
- Branch: `NEXY.ai`
- Product HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- AI-CONTEXT parent: `ee9ad9a561d64241fc93f3da37709b76cd070489`
- Spec SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`

## Contradictory observations

| Probe | Observed result | Interpretation |
|---|---|---|
| runtime_status | read_only_repository_count=0; write/CI backends READY | Snapshot appears permissive |
| repo_status | read_only=false; gateway_write_policy=ALLOW | Snapshot appears permissive |
| ci_dispatch | HTTP 403 `REPOSITORY_READ_ONLY`; operation denied | Actual CI capability is unavailable |

The actual dispatch response is the only direct proof of CI permission for the required operation. Therefore the mandatory precondition is not satisfied.

## Integrity

- Product files changed: NO
- Product commit: NO
- Product CI run: NO
- Product branch changed: NO
- Backend bypass: NO
- PASS_100: NO

## Resume condition

After the gateway is repaired, dispatch an authorized diagnostic workflow successfully, re-query the product HEAD, then start the first TDD RED test. Do not reuse this blocked evidence as proof of a repaired product.
