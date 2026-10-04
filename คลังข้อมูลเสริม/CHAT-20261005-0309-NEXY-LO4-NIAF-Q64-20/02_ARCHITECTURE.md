# Architecture

## Position

NIAF-20 is a **pre-governance acquisition planner**. It accepts unresolved dimensions plus possible acquisition actions and emits a non-governing recommendation envelope.

```text
IRL / CIRL unresolved state
        |
        v
  [ NIAF-20 Lo4 ]
  entropy / VOI / budgets
  exact bounded portfolio
  stop-or-ask recommendation
        |
        v
AI_PROPOSAL_ONLY acquisition envelope
        |
        v
CORE / JUDGE / LAW remain authoritative
```

NIAF does not convert an unknown into truth. It only estimates which action may reduce unknowns.

## Separation from existing observed work

### NEXY CIRL
Observed source resolves explicit intent and emits `WAIT_FOR_DATA_CLARITY` when intent is missing/conflicting or ambiguity exceeds a threshold. NIAF starts after that unresolved condition. It does not replace CIRL.

### Lo4 Proof Compiler Lab
Observed supplemental Proof Compiler includes a minimum proof planner over declared claims/probes. NIAF is earlier in the epistemic pipeline: it determines whether an unresolved variable is worth acquiring and which clarification action is admissible. It does not compile evidence into proof or release output.

### Counterfactual / Human Agency labs
NIAF does not simulate alternate worlds or infer durable preferences. It evaluates declared dimensions/actions only.

### NCIF / NEIK / consensus-independence work
NIAF does not judge agent independence, quorum or consensus quality.

## Data model

`DimensionState` declares unresolved information:
- uncertainty [0,1]
- criticality [0,1]
- conflict [0,1]
- current entropy [0,1]

`ProbeCandidate` declares one acquisition action:
- expected entropy after acquisition
- reliability, discrimination, relevance, novelty
- user burden, privacy, latency, irreversibility, staleness costs
- explicit latency ticks
- semantic features

No value is inferred from a wall clock, random source or hidden external state.

## Determinism rules
- IDs use bytewise `std::string` ordering.
- Ties resolve lexicographically.
- C13 exact portfolio search is bounded to 20 candidates.
- A single portfolio cannot count more than one probe for the same dimension, preventing double-counted information gain in a simultaneous batch.
- C14 excludes actions violating the declared budget before ranking.
- Canonical output sorts probe IDs and evidence notes before serialization.

## Authority rules
The compiler hard-codes proposal authority and rejects envelopes whose labels attempt Canon effects or CORE mutation.
