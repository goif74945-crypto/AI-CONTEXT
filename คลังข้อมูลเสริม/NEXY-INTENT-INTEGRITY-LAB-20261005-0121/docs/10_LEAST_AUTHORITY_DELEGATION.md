# 10 — Least-Authority Delegation Capsule

**Classification:** AI-PROPOSED EXECUTABLE RESEARCH / ADVISORY ONLY

## Goal

Prevent privilege amplification when a task is decomposed across agents or workers. A child should receive the minimum authority needed for its subtask, and a machine should be able to prove that the child did not silently gain new inputs, outputs, scope, or weaker guardrails.

## Capsule relation

A capsule is explicitly tagged:

`relation = LEAST_AUTHORITY_DELEGATION`

It binds to `parentContractSeal` and receives its own deterministic SHA-256 `seal`.

A delegation is not a normal contract revision. Its objective may differ because a child performs a subtask. That is why delegation has a separate verifier rather than reusing revision-drift rules that correctly treat objective changes as unsafe for same-contract revisions.

## Monotonic authority law

Let parent authority envelope be `A` and delegated envelope be `D`.

For delegated inputs, outputs, and executable scope:

`D <= A`

For restrictive guardrails, the direction reverses because adding restrictions is safe attenuation:

`Guard(D) >= Guard(A)`

In practical terms:

- capabilities are subset-only;
- restrictions are superset-only;
- authority ordering is identity-preserving;
- lineage is exact-seal-bound.

## Why parent REVIEW cannot delegate

The prototype requires the parent contract to be `ADMIT`. A parent with unresolved noncritical uncertainty is not allowed to produce execution-authority child capsules. This is intentionally conservative. A production design could define narrower rules, but doing so would require authoritative policy rather than convenience.

## Example

A parent may authorize all work under:

`AI-CONTEXT/คลังข้อมูลเสริม/project/**`

A child may be delegated:

`AI-CONTEXT/คลังข้อมูลเสริม/project/evidence/**`

but not:

`AI-CONTEXT/another-project/**`

The child may inherit all parent forbidden rules and add “do not edit source files.” It may not remove any parent forbidden rule.

## Non-goals

- The lexical path checker does not resolve symlinks or repository aliases.
- The capsule is not an identity credential.
- The hash seal is not a digital signature.
- The subsystem does not choose which child agent should receive a capsule.
- It does not perform any NEXY.AI mutation.
