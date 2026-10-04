# 06 — Proposed NEXY Integration Map

## Status
AI-PROPOSED ONLY. No NEXY.AI source repository was modified.

## Source alignment
The proposal intentionally aligns with source-derived NEXY concepts already recorded in AI-CONTEXT:
- explicit directives and operator authority;
- deterministic control over replaceable AI workers;
- queue/idempotency support;
- freeze on integrity failure;
- pending work invalidation on freeze/recovery;
- replayable/auditable state-changing human operations.

## Proposed placement

```text
UI / command surface
      |
      v
AUTH + API validation
      |
      v
CORE accepts structured directive
      |
      +--> DEF authority epoch register <-------------------+
      |                                                     |
      +--> SWARM / workers --> PreparedAction envelope      |
                                  |                         |
                                  v                         |
                           DEF commit gate ---- current -----+
                                  |
                                ALLOW
                                  |
                                  v
                            governed executor
                                  |
                                  v
                           VAULT / tool / queue
```

## Suggested ownership
- **CORE/Law boundary:** owns directive transition authorization and epoch mutation.
- **SWARM/worker adapter:** receives immutable authority snapshot and returns prepared action envelopes.
- **Executor boundary:** cannot perform mutation without current DEF authorization.
- **OBS/Audit:** records directive transition, prepared action identity, commit decision and journal lineage.
- **AUTH:** authenticates operator/approval; DEF never replaces AUTH.

## Integration invariants
1. Worker output never becomes authority merely because it was prepared earlier.
2. Every mutating queued job includes its prepared epoch and authority lineage.
3. Queue retries retain the original authority tuple; retry does not silently refresh authorization.
4. A newer directive cannot be bypassed by a delayed worker result.
5. Recovery never resumes old queue jobs without a new preparation cycle.
6. Commit authorization must be transactionally close enough to dispatch that an epoch change cannot race between check and side effect.

## Suggested error vocabulary if promoted later
Do not add these to current NEXY law without spec authority. Candidate explicit codes:
- `STALE_DIRECTIVE_EPOCH`
- `DIRECTIVE_LINEAGE_MISMATCH`
- `ACTION_DIGEST_MISMATCH`
- `DIRECTIVE_REVOKED`
- `IRREVERSIBLE_APPROVAL_REQUIRED`
- `DIRECTIVE_EVENT_ID_COLLISION`

## Adoption gate
Before any real NEXY adoption:
- map to current authoritative DOC-C schemas/API/state enums;
- choose durable epoch storage/transaction semantics;
- bind approvals to real AUTH identity/signatures;
- integrate queue cancellation/leases;
- run DB/queue integration tests;
- run E2E supersession races;
- run crash/restart and split-brain fault injection;
- obtain deployment evidence at the exact revision.
