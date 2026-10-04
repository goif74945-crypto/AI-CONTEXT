FAILURE_ID: NEXY-EXACT-HEAD-CI-9E615B04
head: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
status: OPEN / RELEASE_BLOCKING

runs:
- 37222997743 NEXY CI / Deploy Gate: failure
- 37222997798 Exact HEAD test evidence: failure
- 37222997736 Layer8 Cargo lock evidence: failure
- 37222997784 Six-system exact HEAD evidence: failure

job_evidence:
- sampled/current jobs expose steps=null and logs_url=null through connector.
- DOC-C/release-attestation/deploy downstream jobs are skipped where upstream gates fail.
- runner diagnostic run 37221478485, head 88f0b335a06824aed007470ca42bd7312b115684, runner-smoke also failure with steps=null/logs_url=null.

classification: CI_INFRASTRUCTURE_OR_RUNNER_ASSIGNMENT_BLOCK_LIKELY
root_cause: UNKNOWN
forbidden_conclusions:
- do not call assertion/test root cause proven.
- do not call exact-head PASS.
- do not call release/deploy ready.

required_next:
- inspect/repair Actions account/repository/runner availability/settings using a tool with permission.
- rerun required workflows at exact current/future HEAD and capture executable step logs/artifacts.
