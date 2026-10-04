# Architecture and Integration Boundary

> **AI_PROPOSED_CONCEPT / NON-CANONICAL**

## System shape

```text
External explicit records
        |
        v
+---------------------+
| canonical.py        |  deterministic JSON + SHA-256 identity
+----------+----------+
           |
   +-------+--------+----------------+----------------+----------------+
   v                v                v                v                v
  C1               C2               C3               C4               C5
Contract        Emergent         Evidence         Correction        Failure
Composition     Risk             Portability      Compiler          Distiller
   |                |                |                |                |
   +----------------+----------------+----------------+----------------+
                                    |
                                    v
                              integration.py
                       (C2 finding -> C5 minimizer)
                                    |
                                    v
                                  CLI
```

## Boundary law
The package is an auxiliary decision aid. It accepts explicit structured facts and produces deterministic classifications. It does **not** discover NEXY law, infer hidden user intent, prove tool contracts, or mutate a target system.

A future NEXY integration would need adapters that bind these records to authoritative NEXY objects. Those adapters are intentionally absent here so this repository cannot masquerade as production integration evidence.

## Shared invariants
1. Same structured input produces the same canonical serialization and fingerprints.
2. Missing material information freezes or invalidates; it is never silently guessed.
3. Evidence class is an exact contract, not a numeric hierarchy that can be substituted casually.
4. A user correction cannot become global unless it is explicitly marked `GLOBAL_EXPLICIT` and carries `USER_LAW` authority.
5. Failure minimization refuses a flaky oracle.
6. Tool-chain safety transformations are only trusted if the caller supplies verified capability labels; the analyzer itself does not certify a tool implementation.
7. No module performs network I/O, filesystem mutation, subprocess execution, provider calls, or NEXY.AI repository mutation.

## Complexity notes
- C1 is monotone fact closure over components; deterministic admission order is sorted by component id.
- C2 is a linear sequential taint pass over tool steps plus artifact bookkeeping.
- C3 is linear in declared portability dimensions.
- C4 compilation is linear in assertions per correction; cross-correction conflict checking is quadratic in corrections within an identical scope, intentionally acceptable for small correction sets and auditable behavior.
- C5 uses classic ddmin plus a final 1-minimality pass. Every candidate is confirmed twice to detect oracle nondeterminism, trading roughly 2x oracle cost for fail-closed reliability.

## Integration candidates for NEXY
These are proposals, not current build requirements:

- Pre-execution: run C1 on component contracts and C2 on an intended tool plan before execution.
- Evidence gate: run C3 before reusing proof across provider/runtime/code/environment changes.
- Learning loop: after a user correction is confirmed and authorized, use C4 to create a bounded regression contract for future verification.
- Incident/debug loop: feed a stable C2/JUDGE/LAW failure signature into C5 to generate a minimal reproducer for audit and regression tests.

No integration should be adopted unless mapped to current DOC-C contracts and verified against the actual implementation revision.
