# Architecture

## Classification

`AI_PROPOSED_SUPPLEMENTAL_CONCEPT`

This design is intentionally orthogonal to the existing NEXY evidence/control work: it focuses on **what is allowed to leave a trust boundary at all**, before model quality or downstream verification becomes relevant.

## Design goals

1. Deterministic decision structure for equivalent normalized inputs.
2. Fail closed on missing or malformed authority metadata.
3. Minimum disclosure by explicit task purpose.
4. Destination-specific admission and classification ceilings.
5. External egress deny rules for high-risk classes.
6. Bounded retention expressed as leases rather than indefinite storage assumptions.
7. Receipts that prove the decision material without copying denied raw data.
8. No dependency on a specific LLM vendor.

## Non-goals

- automatic PII/secret discovery;
- legal compliance certification;
- encryption/key-management service;
- provider-side deletion enforcement;
- NEXY production integration;
- replacing authorization, sandboxing, or output verification.

## Pipeline

```text
1. AUTHORITY CHECK
   receipt key / policy version / known purpose / destination identity

2. STRUCTURAL CHECK
   policy/profile/envelope types, classification vocabulary, retention bounds

3. FIELD NORMALIZATION
   unique field IDs, canonical stable processing order

4. PURPOSE PROJECTION
   remove fields that are not required for the declared task purpose

5. EGRESS ADMISSION
   field destination ACL + destination classification ceiling + boundary policy

6. RETENTION COMPILATION
   effective TTL = min(field request, policy max, destination max)
   or TTL = 0 when the destination cannot retain

7. DECISION
   any blocking violation => FREEZE and payload = null
   otherwise => ALLOW minimized payload

8. RECEIPT
   HMAC-SHA256 over canonical decision material
```

## Why a compiler instead of a filter

A conventional filter often says "remove sensitive strings" after payload construction. PCF reverses the authority direction: a field must earn admission through a declared purpose and destination contract. The output is built from admitted fields rather than subtracting known-bad values from a broad payload.

That gives the system useful negative guarantees:
- irrelevant fields are pruned by default;
- unknown metadata does not silently survive;
- destination rules are evaluated before egress;
- audit material can describe the decision without replaying denied content.

## State semantics

PCF has no mutable application state in the reference implementation. Every invocation is a pure decision relative to:
- explicit envelope;
- explicit destination profile;
- explicit policy;
- explicit receipt key.

Time used for leases comes from `decision_time` in the envelope, not ambient wall-clock time. This makes replay deterministic and separates "when the caller says this decision is evaluated" from the process clock.

## Trust boundaries

### Caller/NEXY control plane
Owns:
- purpose declaration;
- data classification authority;
- required field set;
- policy selection/version;
- destination profile selection;
- receipt-key custody.

### PCF
Owns:
- contract validation;
- deterministic projection;
- enforcement and freeze semantics;
- lease calculation;
- safe decision receipt construction.

### External provider/tool
Is treated as a destination with explicit capabilities and constraints, never trusted merely because it has a familiar name.

## Failure philosophy

A failure to prove admission is not equivalent to permission. PCF therefore chooses false-negative utility loss over false-positive disclosure when authority metadata is incomplete.
