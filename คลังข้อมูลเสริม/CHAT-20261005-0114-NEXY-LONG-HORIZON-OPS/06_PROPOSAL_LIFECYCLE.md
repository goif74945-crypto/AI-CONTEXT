# Proposal Lifecycle
Status: PROPOSAL_AI

Prevent AI-generated ideas from becoming requirements merely because they were written into a repository.

IDEA → TRIAGED → EXPERIMENT_DEFINED → TESTED → REVIEWED → ADOPTED | REJECTED | DEFERRED → SUPERSEDED.

Only ADOPTED items may be promoted into authoritative planning, and adoption requires authorized project authority.

## Record
proposal_id, origin, problem, motivating evidence, expected benefit, affected invariants, compatibility/security impact, cost, reversibility, experiment, falsification condition, owner, status, adoption authority, decision evidence.

## Separation laws
FACT_PROJECT != PROPOSAL_AI.
Repetition does not increase authority.
An experiment implementation does not adopt its proposal.
A successful benchmark does not prove production suitability.

Rejected proposals should retain reason/evidence to prevent repeated rediscovery.
