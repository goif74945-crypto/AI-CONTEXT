# 06 — AI-PROPOSED NEXY Integration Proposal

**This document is a proposal only. It is not canonical NEXY architecture, not an implementation claim, and not authorization to modify the NEXY.AI repository.**

## Product behavior hypothesis

Before NEXY emits language that implies a future obligation, a future integration could classify the candidate statement as one of:
- present capability statement;
- offer to create a durable task;
- accepted commitment;
- blocked/unsupported commitment.

Only the third class would require an NCIK acceptance record.

This prevents a common trust failure: wording that sounds like a durable promise when the system only has a transient chat turn.

## Candidate integration boundary

```text
DIALOG / assistant draft
       |
       v
Commitment Candidate Compiler
       |
       +-- no future obligation --> normal response path
       |
       +-- future obligation --> NCIK gate
                                  |
                  +---------------+---------------+
                  |                               |
               ALLOW                           ASK/FREEZE
                  |                               |
          bind task/watch                rewrite as offer/blocker
                  |
             CORE/RUN path
                  |
          execution + verification
                  |
          evidence-bound transition
                  |
                VIEW
```

## Required authority boundaries

- USER LAW and canonical LAW/CORE always dominate NCIK.
- NCIK cannot grant execution authority.
- A valid NCIK commitment cannot bypass RBAC, safety, privacy, policy, side-effect, or provider controls.
- A scheduler task ID is not authority by itself; its provenance must be authenticated.
- A UI badge is not fulfillment evidence.

## Interaction with automations

A future implementation could use actual automation/task creation as the capability-binding event:

1. normalize commitment candidate;
2. validate user authority and exact task semantics;
3. create durable automation using the authorized scheduling subsystem;
4. receive immutable task identity/capability receipt;
5. bind that receipt into the commitment;
6. only then allow promise wording such as “I’ll notify you when …”.

If step 3 fails, the system must not emit accepted-promise language.

## Cancellation and revision

User cancellation should produce a terminal commitment state and propagate to the scheduler. A material change in time, trigger, deliverable, beneficiary, scope, effect, or evidence requirement should produce a new revision, not mutate the historical obligation in place.

## User-facing value hypothesis

Potential benefits, requiring future E4/usability evidence:
- fewer fake “I’ll do it later” statements;
- visible history of what NEXY actually promised;
- explicit cancellation/edit controls;
- fewer forgotten follow-ups;
- proof-backed completion instead of optimistic success copy;
- easier debugging when a commitment is blocked or expired.

## Adoption gates

Do not promote this proposal until:
- current NEXY authority/requirement mapping is performed;
- scheduler/automation integration has transactional evidence;
- cancellation and crash recovery are tested;
- E2E UX proves language/state consistency;
- privacy/security review covers retained commitment metadata;
- rollback/migration behavior is specified;
- product authority explicitly adopts the feature.
