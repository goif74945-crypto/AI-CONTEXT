# Architecture — NEXY User Leverage Fabric

## Classification

`AI_PROPOSED / NON_GOVERNING / REFERENCE_IMPLEMENTATION`

The “fabric” is only a packaging boundary for five independent engines. No engine becomes an authority layer merely because it shares a repository folder with the others.

## Design laws shared by all engines

1. Pure deterministic verdict paths: no network, wall-clock, randomness, subprocess or hidden model calls.
2. Explicit inputs; no inference of missing authority or user state.
3. Stable reason codes and canonical SHA-256 fingerprints.
4. Fail closed on invalid or materially incomplete inputs.
5. No direct mutation of NEXY state.
6. No engine may upgrade evidence/authority by prose.
7. Set-like/ordering-insensitive inputs are canonicalized so permutations do not alter results.

---

## Engine A — Goal Contribution Graph (GCG)

### Purpose
Prevent scope creep and “busy work” by requiring a trace from each work item to explicit acceptance criteria.

### Inputs
- objective ID;
- acceptance criteria;
- forbidden scope prefixes;
- work-item IDs;
- contribution edges;
- dependency edges;
- work scopes.

### Output
- `PASS` or `FREEZE`;
- criterion coverage;
- orphan items;
- uncovered criteria;
- forbidden-scope items;
- unknown dependencies/contributions;
- dependency cycle witness;
- canonical fingerprint.

### Failure semantics
Any orphan, uncovered criterion, forbidden scope, unknown dependency, unknown criterion, duplicate ID or cycle freezes the plan.

### NEXY integration proposal
Could be an advisory preflight before FORGE/RUN planning. It would never execute or authorize the plan. CORE/JUDGE remain authoritative.

---

## Engine B — Verified Capability Composer (VCC)

### Purpose
Turn a requested output type into a feasible capability chain using only explicit capability manifests that satisfy data, permission, risk and cost constraints.

### Inputs
- available starting types;
- target type;
- allowed data classes;
- allowed permissions;
- risk/cost/step budgets;
- capability manifests with typed inputs/outputs and status.

### Selection law
Only `AVAILABLE` capabilities are eligible. The deterministic frontier prioritizes:

1. lower total risk units;
2. lower total cost units;
3. fewer steps;
4. lexicographically smaller capability-ID sequence.

### Failure semantics
If no policy-compliant chain reaches the target within budgets, return `FREEZE / NO_POLICY_COMPLIANT_COMPOSITION`.

### NEXY integration proposal
Could read the existing capability registry and emit a candidate composition for the control plane. Scheduler/admission layers would still decide actual execution legality.

---

## Engine C — Artifact Consumer Fitness Gate (ACFG)

### Purpose
Ensure a completed artifact is not merely “correct” but usable by the declared downstream consumer.

### Inputs
- consumer profile;
- required files;
- allowed media types;
- required metadata;
- forbidden classifications;
- package byte budget;
- exact artifact content and declared SHA-256.

### Output checks
- missing/duplicate files;
- unsupported media;
- forbidden classification;
- missing/empty metadata;
- package oversize;
- content hash mismatch.

### Failure semantics
Any contract violation freezes delivery to that consumer profile.

### NEXY integration proposal
Could sit after artifact production/verification but before export or tool handoff. It does not judge factual correctness; it checks the declared consumption contract.

---

## Engine D — Supply-Chain Trust Gate (SCTG)

### Purpose
Stop untrusted or over-privileged dependencies from silently entering a NEXY-adjacent workflow.

### Inputs
- dependency identity/version/source;
- pinning state;
- SHA-256;
- signature state;
- requested permissions;
- outbound network domains;
- trust policy.

### Failure semantics
Freeze on untrusted source, unpinned version where pinning is required, invalid SHA-256, unacceptable signature state, excessive permission or disallowed network domain.

### NEXY integration proposal
Could be used at plugin/adapter/dependency admission before a capability is marked AVAILABLE. It is not a vulnerability scanner and does not claim that a valid hash means safe code.

---

## Engine E — Mastery Path Compiler (MPC)

### Purpose
Generate a minimal deterministic onboarding/mastery path for a declared goal skill without guessing what the user knows.

### Inputs
- explicit skill graph;
- prerequisite edges;
- user-declared known skills;
- goal skill;
- maximum step budget.

### Output
- ordered missing prerequisite steps;
- action/evidence for each step;
- cycle/missing-reference diagnostics;
- canonical fingerprint.

### Failure semantics
Unknown goal, unknown declared skill, missing prerequisite definition, cycle, duplicate skill ID or step-budget overflow freezes the path. Step overflow never silently truncates and pretends the user is ready.

### NEXY integration proposal
Could power guided learning around VIEW/RUN/FORGE or advanced operator features. It stays presentation/training-side and cannot alter CORE truth or permissions.

---

## Composite demo

`nulf.demo` invokes one valid scenario per engine and emits a deterministic JSON report. This proves package-level coexistence only. It is not production or NEXY integration evidence.
