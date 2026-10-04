# 03 — Requirement Ledger

**Status scope:** rows marked PASS refer only to the standalone NCIK reference implementation and local sandbox evidence.

| ID | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|
| NCIK-001 | Commitment has stable identity and positive revision | `model.py`, `evaluate_commitment` | E2 | PASS |
| NCIK-002 | Missing issuer/beneficiary fails closed | `evaluate_commitment` | E2 | PASS |
| NCIK-003 | Missing objective/deliverable fails closed | `evaluate_commitment` | E2 | PASS |
| NCIK-004 | Empty scope fails closed | `evaluate_commitment` | E2 | PASS |
| NCIK-005 | Protected scope collision fails closed | `evaluate_commitment` | E2 | PASS |
| NCIK-006 | Protected collision is case-insensitive | `evaluate_commitment` | E2 corpus | PASS |
| NCIK-007 | Authority conflict freezes | `evaluate_commitment` | E2 | PASS |
| NCIK-008 | Unresolved authority asks rather than assumes | `evaluate_commitment` | E2 | PASS |
| NCIK-009 | Authority provenance is mandatory | `evaluate_commitment` | E2 | PASS |
| NCIK-010 | Temporal mode must match exact binding type | `_MODE_BINDING` | E2 exhaustive enum matrix | PASS |
| NCIK-011 | Scheduled commitment requires durable scheduler binding | `evaluate_commitment` | E2 | PASS |
| NCIK-012 | Conditional commitment requires durable watch binding | `evaluate_commitment` | E2 | PASS |
| NCIK-013 | Recurring commitment requires durable recurring binding | `evaluate_commitment` | E2 | PASS |
| NCIK-014 | Future schedule/trigger semantics cannot be empty | `evaluate_commitment` | E2 corpus | PASS |
| NCIK-015 | Binding ref + capability proof ref are mandatory | `evaluate_commitment` | E2 | PASS |
| NCIK-016 | Unsupported execution binding freezes | `CapabilityManifest` gate | E2 | PASS |
| NCIK-017 | Unsupported effect freezes | `CapabilityManifest` gate | E2 | PASS |
| NCIK-018 | Required evidence must be producible | evidence capability gate | E2 | PASS |
| NCIK-019 | Evidence classes are exact, not ordinal substitutes | acceptance/completion gates | E2 invariant tests | PASS |
| NCIK-020 | Equivalent set-like ordering gives same fingerprint | `canonical.py`, `fingerprint` | E2 permutations | PASS |
| NCIK-021 | Duplicate set-like values do not alter fingerprint | `fingerprint` | E2 | PASS |
| NCIK-022 | Equivalent whitespace normalizes deterministically | `canonical.py` | E2 | PASS |
| NCIK-023 | Same input gives same evaluation over repeated runs | evaluation engine | E2 x1000 | PASS |
| NCIK-024 | Revision increments exactly by one | `validate_revision` | E2 | PASS |
| NCIK-025 | Revision cannot silently change issuer/beneficiary | `validate_revision` | E2 | PASS |
| NCIK-026 | Revision binds exact prior fingerprint | `validate_revision` | E2 | PASS |
| NCIK-027 | Revised commitment requires resolved authority | `validate_revision` | E2 | PASS |
| NCIK-028 | Completion requires evidence | `transition` | E2 | PASS |
| NCIK-029 | Completion requires evidence result PASS | `transition` | E2 | PASS |
| NCIK-030 | Completion evidence must target exact fingerprint | `transition` | E2 | PASS |
| NCIK-031 | Completion evidence must target exact revision | `transition` | E2 | PASS |
| NCIK-032 | Completion evidence must contain refs | `transition` | E2 | PASS |
| NCIK-033 | All declared evidence classes are required | `transition` | E2 | PASS |
| NCIK-034 | Terminal states are immutable in reference FSM | `transition` | E2 exhaustive event matrix | PASS |
| NCIK-035 | BLOCKED may resume only through explicit transition | `transition` | E2 | PASS |
| NCIK-036 | Illegal state transitions reject | `transition` | E2 | PASS |
| NCIK-037 | Ledger detects event tampering | `ledger.py` | E2 | PASS |
| NCIK-038 | Ledger detects reordering | `ledger.py` | E2 | PASS |
| NCIK-039 | Ledger binds revision and payload | `ledger.py` | E2 | PASS |
| NCIK-040 | Core library has no time/random/network/model/process/env import | AST invariant test | E1/E2 | PASS |
| NCIK-041 | JSON schema/fixtures/examples are syntactically parseable | `run_checks.py` | E1 | PASS |
| NCIK-042 | Adversarial corpus covers >=30 cases | fixture + corpus runner | E2 | PASS |
| NCIK-043 | Real scheduler binding authenticity is cryptographically proven | not implemented | E3+ | NOT_VERIFIED |
| NCIK-044 | Distributed cancellation/revocation propagates before execution | not implemented | E3/E5 | NOT_VERIFIED |
| NCIK-045 | Scheduler survives service/process failure | not implemented | E5 | NOT_VERIFIED |
| NCIK-046 | Cross-agent handoff preserves commitment exactly | not implemented | E3 | NOT_VERIFIED |
| NCIK-047 | Exactly-once side effect fulfillment under retry/crash | not implemented | E3/E5 | NOT_VERIFIED |
| NCIK-048 | Real NEXY LAW/CORE/RUN integration is compatible | no NEXY mutation | E3/E4 | NOT_VERIFIED |
| NCIK-049 | UI never presents unbacked promise language | no UI integration | E4 | NOT_VERIFIED |
| NCIK-050 | Production deployment behaves correctly | no deployment | E6 | NOT_VERIFIED |
