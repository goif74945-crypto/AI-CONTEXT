# Design, Novelty and Promotion Contract

**Classification:** `AI-PROPOSED / Lo4 / EXPERIMENTAL / NOT CANON`

## Baseline collision audit

Before concept lock, the current supplemental tree was scanned. Existing work already covered proof/evidence, counterfactual verification, authority, privacy, resource governance, constraint coverage, multi-FSM integrity, model substitution, semantic contracts, trust UX, knowledge decay, replay, recovery assurance, observability, causal analysis and capability routing.

Recent comparison points included:
- `CHAT-20261005-0154-GPT56SOL-FRONTIER-5`: model drift, semantic capability ABI, context taint, effect transaction coordination, authority leases.
- `CHAT-20261005-0155-NEXY-FRONTIER-FIVE`: uncertainty dependency mesh, ambiguity experiments, capability-aware routing, decision patch compression, resilience scenarios.
- `CHAT-20261005-0157-NEXY-FRONTIER-ASSURANCE-LAB`: unsat-core localization, Pareto pruning, hidden dependency detection, recovery equivalence, observability sufficiency.

Exact pre-write GitHub code searches returned zero matches for: `Surprise Budget`, `Anti-Feature Refutation`, `minimax regret`, `minimal relaxation`, `Option Preservation`. This proves no direct phrase collision in the observed AI-CONTEXT state, not universal conceptual novelty.

---

# 1. SBC — Surprise Budget Controller

## Problem
Unbounded AI creativity can accidentally turn “innovate” into “rewrite the authority model.” NEXY needs aggressive Lo4 research without silently spending Canon integrity.

## Input
Named novelty dimensions:
- `name`
- `distance_bps` 0..10000
- `weight_bps` 0..10000
- `authority`

Policy:
- total surprise budget
- max cost per dimension
- protected authority classes

## Algorithm
For each dimension:

`cost = ceil(distance_bps × weight_bps / 10000)`

Costs are deterministic and sorted by dimension name.

## Immutable rules
- Any nonzero distance applied to `USER_LAW` or `CANON` freezes.
- Per-dimension and total budget overruns freeze.
- Duplicate dimension IDs are invalid.
- Rounding is conservative so novelty cost is not understated.

## Output
`ALLOW_EXPERIMENT` or `FREEZE` with reason codes and fingerprint.

## NEXY value
It creates a formal experimental-distance envelope. Lo4 can be weird on purpose without acquiring authority.

---

# 2. AFRE — Anti-Feature Refutation Engine

## Problem
AI systems are naturally good at adding things. They are much less disciplined about proving that a feature should not exist. Unchecked addition creates complexity, slower verification and worse UX.

## Input
- benefit claims with user-value score and evidence level
- proposed complexity and risk
- optional alternatives with coverage, complexity, risk, availability

## Behavior
- `KEEP_EXPERIMENT` when value is sufficiently evidenced and no refutation succeeds.
- `NEED_EVIDENCE` when claimed value lacks the required evidence.
- `REJECT_EXPERIMENT` when value is too low, risk exceeds policy, or a much simpler available alternative substantially subsumes the proposal.

## Immutable rules
- Benefit claims are not added together as marketing arithmetic.
- Missing evidence never becomes high value.
- Rejection targets only the Lo4 candidate, never existing Canon.

## NEXY value
It makes “do not build this” a valid successful result and creates a complexity counterforce against endless AI-generated feature growth.

---

# 3. MRPE — Minimal Relaxation Proposal Engine

## Problem
A proposal may be blocked by conflicting constraints. NEXY must never silently weaken rules, but a human may still benefit from knowing whether a tiny relaxation of explicitly experimental assumptions would unlock progress.

## Model
Each constraint has:
- stable ID
- authority
- explicit `relaxable` flag
- relaxation cost

Each conflict is a set of constraint IDs.

## Algorithm
1. Candidate set = `Authority.EXPERIMENTAL && relaxable`.
2. If any conflict set contains no candidate, `FREEZE`.
3. If candidate count exceeds exact-search bound, `FREEZE`.
4. Enumerate combinations up to configured relaxation-count bound.
5. Keep combinations hitting every conflict set.
6. Choose deterministic minimum tuple:
   `(total_cost, number_of_relaxations, lexical_ids)`.

This is an exact bounded weighted hitting-set proposal.

## Immutable rules
- `USER_LAW`, `CANON`, SYSTEM-level non-experimental constraints and any non-relaxable constraint are never candidates.
- Output is proposal only. It never applies a mutation.
- Unknown references are invalid.
- Bound exhaustion freezes rather than switching to a hidden heuristic.

## NEXY value
It complements conflict localization. A locator says “what conflicts”; MRPE says “what smallest Lo4-only concession could be put in front of an authorized human for review?”

---

# 4. REP — Regret Envelope Planner

## Problem
When scenario probabilities are unknown, expected-value optimization invites guessed probabilities. The planner needs a deterministic policy for choosing a robust next experiment without pretending uncertainty is known.

## Input
Each action has:
- ID
- reversibility
- human-approval gate flag
- hard-constraint status
- explicit utility for exactly the same finite scenario set

## Algorithm
1. Remove hard-constraint-violating actions.
2. Remove irreversible actions lacking the explicit human gate.
3. Compute best utility per scenario using legal actions only.
4. Regret = scenario-best minus candidate utility.
5. Minimize:
   `(worst_case_regret, total_regret, action_id)`.
6. Freeze if the best worst-case regret exceeds policy.

## Immutable rules
- Illegal actions cannot define the regret baseline.
- Scenario sets must match exactly.
- No probability distribution is inferred.
- Irreversible action needs an explicit human gate before it can even be considered.

## Known limitation
Minimax regret depends on the supplied scenario set. Scenario construction therefore remains an upstream evidence responsibility.

## NEXY value
This provides a practical reversible-first action selector under Knightian-style uncertainty without “AI confidence” masquerading as probability.

---

# 5. OPC — Option Preservation Compiler

## Problem
Two architectures can satisfy today’s requirements while leaving radically different ability to adopt future providers, local models, offline execution or policy changes.

## Input
Future options:
- option ID
- explicit importance

Architecture choices:
- current value
- preserved option IDs
- switching cost
- lock-in
- hard-constraint status

## Score
`current_value + future_preservation_component - switching_penalty - lock_in_penalty`

Future preservation is normalized from explicitly supplied option-importance values. No hidden user priorities are invented.

## Immutable rules
- Unknown option IDs are invalid.
- Hard-constraint failures are ineligible.
- Importance weights must be explicit inputs.
- Output is advisory Lo4 planning, not canonical architecture authority.

## NEXY value
It operationalizes “do not spend future freedom casually,” fitting NEXY’s multi-provider/model-independent direction.

---

# Integrated Lo4 pipeline

```text
Lo4 candidate
   ↓
SBC — bounded experimental distance?
   ↓ ALLOW_EXPERIMENT
AFRE — worth existing?
   ↓ KEEP_EXPERIMENT
MRPE — if blocked, is there a review-only Lo4 relaxation proposal?
   ↓ PLAN | PROPOSE_RELAXATION
REP — what legal reversible step minimizes worst-case regret?
   ↓ PLAN
OPC — which legal design preserves explicit future options?
   ↓ PLAN
LO4_EXPERIMENT_READY
   ↓
human/formal promotion process outside this lab
```

Any failed stage returns `FREEZE` at the first failing boundary.

## Shared technical properties
- standard-library Python
- pure-data reference logic
- deterministic fingerprints
- no network/database/provider/repository side effects
- explicit reason codes
- no hidden fallback
- no self-promotion

---

# Promotion gates

## P0 Identity
Stable proposal ID/version and persistent `Lo4 / NOT CANON` label.

## P1 Collision review
Re-scan current AI-CONTEXT and current NEXY spec at promotion time. Historical scans are not enough.

## P2 Authority mapping
Map every behavior to current User Law/DOC-B/DOC-C authority. Any unresolved conflict = `FREEZE`.

## P3 Runtime adapter proof
Build adapters against exact current NEXY runtime types. Require E1 + E2.

## P4 Integration proof
Require E3 integration and negative-path tests for malformed/stale/permission/replay states as applicable.

## P5 User-benefit proof
Demonstrate measurable target-workflow benefit. AFRE must not refute the feature as low-value or simpler-subsumed.

## P6 Operational proof
For runtime decision impact, require E5 operational/fault evidence and observed performance bounds.

## P7 Explicit promotion authority
Only authorized human/governance process may promote. The Lo4 code cannot edit Canon, User Law or declare production readiness.
