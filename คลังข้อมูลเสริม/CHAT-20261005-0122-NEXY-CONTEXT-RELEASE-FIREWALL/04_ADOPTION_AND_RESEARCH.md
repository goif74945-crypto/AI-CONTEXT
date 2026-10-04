# Adoption Gates and Research Backlog

Classification: AI_PROPOSED_CONCEPT / HYPOTHESES

## Adoption gate A — Source-law compatibility
Before promotion into any NEXY build:
- map every CRF invariant to current DOC-B/DOC-C authority;
- identify naming conflicts with existing policy/Vault contracts;
- reject any CRF rule that would contradict a higher-authority law;
- keep CRF optional/proposal status until explicitly promoted.

Status now: NOT_VERIFIED.

## Adoption gate B — Data classification contract
A release firewall is only as useful as its labels.
Required future work:
- canonical sensitivity taxonomy;
- canonical compartment naming/ownership;
- provenance contract;
- label lifecycle/versioning;
- conflict behavior when two classifiers disagree;
- explicit rule for unlabeled context (recommended default: freeze/deny).

## Adoption gate C — Context request compiler
The reference engine assumes required/optional keys are already explicit.
Future component should convert task contracts into context-key requirements without inferring missing intent.
Research question: how to minimize user interruptions while preserving zero-guess behavior?

This deliberately remains separate from the concurrent Human Authority lab.

## Adoption gate D — Cryptographic grant authority
Replace the reference trusted-digest registry with a governed signed object flow:
- signer identity/role;
- canonical serialization version;
- signature verification;
- revocation/sunset semantics;
- replay protection;
- audit/event anchoring where required by NEXY law.

No fake signature implementation should be promoted merely to tick a security checkbox.

## Adoption gate E — Authoritative time
Reference tests inject `evaluated_at` for determinism.
Production should bind grant/context expiry to a trusted time source and define behavior under clock disagreement or time unavailability.

## Adoption gate F — Provider capability/privacy profile
A consumer policy can later incorporate provider attributes such as:
- retention policy class;
- geographic boundary;
- enterprise/private endpoint;
- tool/plugin permissions;
- model data-handling guarantees;
- local vs external execution.

These attributes must be verified/configured facts, not brand assumptions.

## Adoption gate G — Taint transformation proofs
Conservative monotonic taint is safe but can be over-restrictive.
Research formal/verified transformation classes that may reduce sensitivity, for example:
- approved aggregation;
- k-anonymized release;
- deterministic tokenization;
- schema-only extraction;
- controlled synthetic transformation.

Promotion requires a proof/evidence class appropriate to the transformation. “The model summarized it” is not a declassification proof.

## Adoption gate H — Nested agent boundaries
For SWARM workflows, context may traverse:
`CORE → orchestrator → agent → tool/service`.

Future design should attach a release receipt at every boundary and enforce non-escalation:
`downstream authority <= upstream released authority`.

Research a receipt chain/Merkle commitment that proves each hop without storing blocked values.

## Adoption gate I — Context budget optimizer
Once legality is established, optimize for utility and token cost:
- minimize duplicated context;
- prefer canonical references over raw repetition;
- cache safe reusable public/internal slices;
- measure quality degradation from context removal;
- never trade privacy authority for model convenience.

## Adoption gate J — Abuse/eval corpus
Expand adversarial corpus with:
- prompt injection requesting hidden fields;
- alias/key confusion;
- Unicode confusables in compartment names;
- time-boundary behavior;
- huge nested values / resource exhaustion;
- receipt correlation attacks;
- malicious provenance strings;
- declassification replay;
- downgrade across version migration;
- multi-hop agent laundering.

## Hypothesized product benefits
These are hypotheses, not measured facts:
- lower accidental context leakage across providers;
- easier enterprise/privacy review;
- clearer “why this model received this data” auditability;
- safer provider hot-swap;
- lower token usage by sending only requested context;
- more trustworthy multi-agent orchestration.

Each benefit requires instrumentation and experiment before being treated as proven.
