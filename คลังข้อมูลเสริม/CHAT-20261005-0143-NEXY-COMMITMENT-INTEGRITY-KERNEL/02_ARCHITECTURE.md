# 02 — NCIK Architecture

**Status:** AI-PROPOSED / SUPPLEMENTARY / NON-GOVERNING.

## 1. Design objective

Make outward AI commitments mechanically honest.

The system should reject or freeze a commitment when the execution environment cannot prove that it has the capability needed to keep that commitment. It should also reject a later “complete” transition unless evidence is bound to the exact commitment fingerprint and revision.

This solves a different problem from ordinary task execution. A task can be well-scoped while the assistant still falsely implies future persistence. Conversely, a scheduler can exist while the promised deliverable is too vague to verify. NCIK binds both sides.

## 2. Core model

```text
USER DIRECTIVE / AUTHORITY
          |
          v
  COMMITMENT COMPILER
          |
          +---- exact obligation fingerprint ----+
          |                                       |
          v                                       v
 CAPABILITY BINDER                         EVIDENCE CONTRACT
          |                                       |
          +---------------+-----------------------+
                          v
                    COMMITMENT GATE
              ALLOW | ASK_AUTHORITY | FREEZE
                          |
                          v
                   LIFECYCLE CONTROLLER
 DRAFT -> ACCEPTED -> ACTIVE -> FULFILLED
                     |   |  \-> FAILED
                     |   \----> BLOCKED -> ACTIVE
                     \--------> CANCELLED / EXPIRED
 ACCEPTED/ACTIVE/BLOCKED ------> SUPERSEDED
                          |
                          v
                   HASH-CHAIN RECEIPTS
```

The lifecycle model is intentionally strict. Terminal states do not silently reopen.

## 3. Commitment contract

A commitment contains the minimum information needed to decide whether it is truthful and later provable.

### Identity
- `commitment_id`
- `revision`
- `issuer`
- `beneficiary`

### Meaning
- `objective`
- `deliverable`
- `scope[]`
- `protected_scope[]`
- `effect`

### Authority
- `authority_state = RESOLVED | UNRESOLVED | CONFLICT`
- `authority_refs[]`

The engine does not infer authority from fluent text. Missing provenance is a hard failure in this reference model.

### Temporal semantics
- `IMMEDIATE`
- `SCHEDULED`
- `CONDITIONAL`
- `RECURRING`

Each mode has one legal binding type:

| Temporal mode | Required binding |
|---|---|
| IMMEDIATE | INLINE_SESSION |
| SCHEDULED | SCHEDULED_TASK |
| CONDITIONAL | CONDITION_WATCH |
| RECURRING | RECURRING_TASK |

Non-immediate bindings must be marked durable and carry a non-empty capability proof reference.

### Evidence
`required_evidence[]` is an exact set requirement. The reference engine deliberately does **not** assume that a numerically “higher” evidence class substitutes for another class. E6 deployment does not prove E4 user-flow behavior unless the required E4 evidence itself exists.

## 4. Capability manifest

NCIK accepts an explicit capability manifest supplied by a trusted upstream integration layer:
- supported binding types;
- supported effect classes;
- evidence classes the current environment can produce.

The reference package does not discover capabilities from ambient environment variables, installed SDKs, model self-description, or natural-language claims. Discovery belongs to an upstream verified capability registry.

## 5. Commitment evaluation precedence

The engine applies a fail-closed gate:

1. structural validity;
2. scope/protected-scope collision;
3. authority conflict;
4. unresolved authority;
5. temporal-mode / binding equality;
6. execution capability existence;
7. future durability;
8. trigger/schedule completeness;
9. effect capability;
10. evidence producibility;
11. allow.

An earlier hard failure is never “repaired” by a lower-priority convenience rule.

## 6. Fingerprinting

Fingerprint input is normalized before SHA-256:
- object keys sorted;
- set-like fields sorted and deduplicated;
- whitespace collapsed in strings;
- enums serialized by explicit value;
- JSON emitted with stable separators and UTF-8.

Equivalent normalized obligations therefore produce the same tested fingerprint.

The fingerprint includes the execution binding. A promise bound to scheduler task A is not the same commitment as one bound to scheduler task B.

## 7. Revision and supersession

Commitments are immutable once issued.

A revised commitment must:
- keep the same logical commitment ID;
- increment revision by exactly one;
- preserve issuer and beneficiary;
- carry the exact prior fingerprint in `supersedes_fingerprint`;
- have resolved authority;
- pass commitment evaluation again.

This prevents silent widening of scope, deliverable, deadline, evidence, or execution semantics.

## 8. Completion gate

`FULFILLED` is legal only from `ACTIVE` and only when an evidence bundle satisfies all of:
- `result == PASS`;
- exact target fingerprint;
- exact commitment revision;
- non-empty evidence references;
- every declared required evidence class is present.

Text such as “done,” a UI green check, or a file existing somewhere is not completion evidence unless it satisfies the declared contract.

## 9. Receipt ledger

The reference ledger chains every event using:
- sequence;
- commitment identity/revision;
- event type;
- state;
- payload;
- previous event hash.

Tampering or reordering invalidates verification. This is an integrity experiment, not a production signature, WAL, immutable audit service, or transparency log.

## 10. Determinism boundary

Core package imports no clock, randomness, process execution, network client, model SDK, environment access, or filesystem API.

This gives the reference decision logic a narrow deterministic boundary. Real integration will need explicit authoritative inputs for time, scheduler state, cancellation state, and distributed execution receipts.

## 11. Proposed NEXY placement

If adopted in the future, a safe conceptual placement is:

```text
DIALOG / agent candidate wording
          |
          v
COMMITMENT EXTRACTION / NORMALIZATION  (future authoritative compiler required)
          |
          v
NCIK COMMITMENT GATE
   | ALLOW                 | FREEZE/ASK
   v                       v
CORE/RUN binding       non-commitment wording or explicit blocker
   |
   v
scheduler / watch / inline executor
   |
   v
verification + receipt
   |
   v
VIEW may present FULFILLED only with evidence
```

NCIK must remain subordinate to USER LAW, canonical LAW/CORE, authorization, safety, and existing freeze behavior.

## 12. Non-goals

NCIK does not:
- parse natural language into trusted authority;
- create scheduler tasks;
- authenticate users;
- replace RBAC or delegation leases;
- prove real provider durability;
- guarantee exactly-once distributed effects;
- define canonical product copy;
- replace AI-CONTEXT verification law;
- modify NEXY.AI.
