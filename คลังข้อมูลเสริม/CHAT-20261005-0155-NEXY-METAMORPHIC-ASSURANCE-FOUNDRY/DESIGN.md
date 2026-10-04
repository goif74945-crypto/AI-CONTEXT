# Design Contract

## Objective
Detect semantic regression and verification circularity while preserving deterministic behavior, bounded work, explicit evidence and fail-closed proof budgeting.

## In scope
Canonical JSON identity; metamorphic execution; bounded counterexample shrinking; oracle-dependency overlap detection; deterministic risk/coverage test scheduling; semantic failure fingerprinting; strict extraction of selected DOC-C truth-surface fields.

## Out of scope
Changing NEXY requirements; mutating a repository whose name contains \`NEXY.AI\`; production deployment; provider/network execution; automatic semantic-relation invention; replacing LAW/JUDGE/release policy; claiming physical/security assurance.

## Invariants
- Mapping insertion order does not change canonical identity.
- Non-finite numbers and non-string JSON object keys are rejected.
- Executor exceptions remain runtime failures, not invariant failures.
- Shrinking is evaluation-budget bounded.
- Mandatory proof tests are never silently removed for budget reasons.
- Scheduling is deterministic under reordered candidate input.
- Oracle contamination is explicit via reason codes.
- Failure fingerprints retain fields unless volatility is explicitly declared.
- Missing truth-surface status/state is rejected, never defaulted.

## Failure semantics
Invalid config -> exception; relation mismatch -> \`passed=false\`; shrink budget exhaustion -> best witness plus \`exhausted_budget=true\`; mandatory proof over budget -> \`freeze_required=true\`; oracle contamination -> \`independent=false\`; unsupported canonical value -> \`CanonicalizationError\`.

## Security boundary
Library code imports no networking, subprocess, database, environment or filesystem APIs. A caller-provided executor remains outside this guarantee and must be sandboxed/authorized by the integration layer.

## NEXY compatibility basis
AI-CONTEXT currently describes NEXY as verified-output-only, bounded, evidence-first, deterministic/freeze-oriented, with DOC-C truth envelopes and explicit release gates. NMAF complements those principles but is not part of DOC-C unless separately promoted through authorized governance.
