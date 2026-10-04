# Decision Optionality Ledger
**AI-PROPOSED CONCEPT — NOT AUTHORITATIVE — NOT IMPLEMENTED — NOT VERIFIED**

## Idea
Architecture decisions consume or preserve future options. Traditional ADRs record what was chosen; an Optionality Ledger records what choices become harder, impossible, or expensive after the decision.

## Decision record extension
- decision_id
- chosen option
- rejected alternatives
- authority
- evidence
- reversible_until
- reversal_cost estimate + evidence class
- lock-in vectors
- migration path
- data portability impact
- provider portability impact
- protocol compatibility impact
- operational coupling
- skills/tooling coupling
- future options preserved
- future options closed
- re-evaluation triggers

## Lock-in vectors
Data format, identity scheme, provider-specific API, irreversible migration, cryptographic/key hierarchy, external contract, hardware dependency, workflow semantics, observability format and organizational process can each create distinct lock-in.

## Option value
Do not reduce this to a fake precise score. Use ordinal classes with evidence:
HIGH_OPTIONALITY, MODERATE, LOW, IRREVERSIBLE, UNKNOWN.

## Re-evaluation triggers
New authoritative requirement; provider deprecation; cost discontinuity; security finding; scale threshold; regulatory constraint; repeated failure fossil; new migration tooling.

## NEXY relevance
A deterministic control system benefits from knowing not only “is this correct now?” but “what future authority choices will this prevent?” This helps avoid locally optimal decisions that silently constrain future NEXY evolution.

## Safety rule
Optionality cannot override current safety/system law. Preserving future options is subordinate to correctness, authority and evidence.
