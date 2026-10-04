# Design — NEXY Lo4 Reality Five

Classification: **AI-proposed Lo4 innovation, not Canon**.

## Design objective

Create five deterministic, composable mechanisms that improve real-world operability without weakening NEXY's core principles: zero-guess, explicit authority, proof/evidence boundaries, one legal verified output or freeze, human authority, and fail-closed behavior.

## Shared contracts

### Numeric representation
`Q64` is signed Q64.64 with raw range `[-2^127, 2^127-1]`. Multiplication/division use deterministic integer arithmetic and division truncates toward zero. No binary float is accepted by the fixed-point constructors.

### Determinism
Canonical tie-breaks are lexical IDs after numeric criteria. Input order must not change material decisions or digests. Stress verification explicitly reverses major input sequences and compares digests.

### Authority
All thresholds/weights/policies are caller-supplied contracts. The library does not invent legal residency rules, accessibility requirements, provider retention truth, approval law, or production risk thresholds.

### Side effects
The library is pure data logic. It has no network calls, provider SDKs, credentials, filesystem writes, or external execution paths.

## Cross-system architecture

```text
User objective / action
        |
        +--> HIG --------> AUTO / ASK / APPROVAL / FREEZE
        |
        +--> JCPP -------> legal placement candidate or FREEZE
        |
        +--> VIBA -------> funded verification plan or FREEZE
        |
Canonical result --------> SAEM ----> accessible representation PASS/FAIL
        |
        +--> OAC --------> bounded operator attention plan

Final integration adapter releases only when authoritative NEXY gates permit it.
```

## Why the five systems compose well

- HIG prevents autonomy from becoming accidental authority.
- JCPP prevents optimization from routing data through a disallowed compute location/provider.
- VIBA prevents finite compute from silently dropping mandatory proof obligations.
- SAEM prevents alternate UI modes from dropping decision-critical meaning.
- OAC prevents information density from hiding critical facts while controlling optional noise.

The composition attacks five different boundary failures rather than five variants of the same assurance primitive.

## Complexity notes

- OAC: `O(n log n)` due deterministic ranking.
- JCPP: `O(n log n)` with hard filtering followed by deterministic ranking.
- SAEM: expected `O(n)` maps plus sorted failure lists.
- HIG: `O(1)`.
- VIBA: exact multiple-choice Pareto-frontier dynamic programming. Runtime depends on frontier width, not only item count; no polynomial production SLA is claimed.

## Promotion conditions

No proposal may be promoted merely because this isolated lab passes. Promotion would require at minimum:
1. authoritative NEXY interface mapping;
2. production data schemas and policy ownership;
3. threat model and abuse tests;
4. exact-head integration tests;
5. user/UX validation for OAC/HIG/SAEM;
6. compliance/legal validation where JCPP inputs originate from legal policy;
7. performance profiling with representative workloads;
8. explicit versioned governance approval.
