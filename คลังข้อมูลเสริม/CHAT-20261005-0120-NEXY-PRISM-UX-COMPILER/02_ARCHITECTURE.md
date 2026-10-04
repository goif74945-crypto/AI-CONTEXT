# NEXY::PRISM Architecture

## Classification
`AI_PROPOSED_CONCEPT / FUTURE_OPTION / NOT_CURRENT_BUILD_REQUIREMENT`

## Architectural purpose
PRISM is a deterministic **presentation-policy compiler** between an authoritative backend truth surface and a user-interface renderer.

```text
CORE / LAW / JUDGE / AUTH / VAULT / OBS
                |
                | authoritative state + authorization + release facts
                v
        SystemEnvelope / ViewFacts
                |
                v
        +------------------+
        |   NEXY::PRISM    |
        | presentation only|
        +------------------+
           |          |
           |          +--> mandatory disclosures
           +-------------> action affordance + detail floor
                |
                v
           NEXY::VIEW/UI
```

PRISM cannot mutate the boxes above it. It cannot create a release token, grant RBAC, recover a freeze, change a state transition, create evidence, or rewrite an incident.

## Input contract
The prototype accepts canonical system state, role, evidence status, requested visible action, action risk, user detail preference, backend authorization, backend release authorization, backend recoverable flag, irreversible-action flag, and optional incident/blocking metadata.

The critical design choice is that **authorization is input, not computed authority**. PRISM may apply a defense-in-depth UI deny, but it never converts backend deny to allow.

## Output contract
A compiled `SurfacePlan` contains trust label, effective detail level, authoritative banner, action state, reason code, confirmation strength, mandatory disclosures, optional detail sections, conflict codes, and deterministic SHA-256 fingerprint.

## Truth floor
`effective_detail = max(user_preference, required_truth_floor)`

- normal verified low-risk view -> COMPACT may stay compact;
- high risk -> at least STANDARD;
- FREEZE/STOP/critical/irreversible/conflict -> FORENSIC.

Mandatory disclosures are independent of optional detail level.

## Precedence law
1. FREEZE banner remains FREEZE even when upstream input also conflicts.
2. STOP banner remains STOP even when upstream input also conflicts.
3. Conflict remains visible as trust classification + mandatory disclosure.

This prevents a secondary diagnostic condition from masking the authoritative blocked state.

## Determinism
No clocks, random values, network calls, or model inference participate in compilation. The fingerprint covers canonical input plus canonical output excluding the fingerprint itself.

## Non-goals
Natural-language generation, deciding correctness, deciding user intent, provider selection, backend RBAC, release policy, hidden personalization, production integration.
