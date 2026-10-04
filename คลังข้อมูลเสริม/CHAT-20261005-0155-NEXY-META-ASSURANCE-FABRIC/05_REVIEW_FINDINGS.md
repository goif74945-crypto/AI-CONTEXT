# Independent Logical Review Record

Execution mode: LOGICAL_ISOLATION (no separate agent runtime was available).

## Reviewer findings

### F-001 — SMS validator return type was underspecified
Severity: medium for prototype correctness.  
Observed: the original implementation used truthiness, so a validator returning `"yes"` could be treated as approval.  
Risk: ambiguous external validator contract could convert malformed output into acceptance.  
Repair: require `isinstance(result, bool)` for baseline and mutated runs; otherwise raise `SpecMutationError`.  
Regression evidence: `test_non_boolean_validator_result_fails_closed` PASS.  
Status: RESOLVED.

### F-002 — MPWE general-case scalability
Severity: architectural limitation, not an implementation defect for current bounded prototype.  
Observed: exact weighted set cover is NP-hard; bitmask dynamic programming can grow exponentially with requirement count.  
Decision: retain exact implementation as a correctness/reference prototype; production integration needs bounded partitioning, branch-and-bound/ILP backend, or deterministic approximate mode with explicit non-optimal status.  
Status: KNOWN LIMITATION.

### F-003 — BFK corpus completeness
Observed: unchanged fingerprints prove unchanged behavior only for represented scenarios.  
Decision: require an external coverage contract; do not equate unchanged fingerprint with universal equivalence.  
Status: KNOWN LIMITATION.

### F-004 — MVS relation authority
Observed: metamorphic correctness is conditional on relation correctness.  
Decision: relation generation/approval is outside MVS authority; production use must bind relation provenance and authority.  
Status: DESIGN GUARD.

### F-005 — CLL scope selection
Observed: only declared keys participate in conservation.  
Decision: conservation rules must be authority-controlled and source/sink deltas explicit.  
Status: DESIGN GUARD.

## Security review
- no credentials or secrets embedded;
- no network/filesystem/process/env/clock/random imports in core modules;
- no dynamic code execution;
- no deserialization of executable formats;
- hash use is integrity/fingerprint only, not authentication.

## Truth Sentinel summary
Supported: local deterministic prototype behavior under executed tests.  
Not supported: production readiness, NEXY integration, deployment safety, global novelty, universal correctness.
