# Task Contract — Lo4 Q64 Decision-Space Topology 20

## OBJECTIVE
Produce twenty novel, deterministic, executable Q64.64 decision-topology proposal engines for future optional NEXY.AI integration.

## TARGET
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0229-NEXY-LO4-Q64-DECISION-TOPOLOGY-20`

## AUTHORIZED SCOPE
Only create/update files inside the target folder.

## PROTECTED SCOPE
Every repository whose name contains `NEXY.AI`; every pre-existing path outside the target folder.

## IMMUTABLE REQUIREMENTS
1. Exactly 20 proposal engines.
2. Every decision-relevant numeric computation uses checked signed Q64.64.
3. Float inputs are rejected.
4. Explicit freeze/failure semantics.
5. Deterministic canonical ordering and serialization.
6. No network/provider/model dependency.
7. Design + code + test + evidence retained.
8. Local tests must actually run.
9. Exact tested bytes must be hashed.
10. Persisted bytes must be read back before PASS.
11. Lo4 status remains proposal-only until authorized promotion.
12. No NEXY.AI repository mutation.

## INPUT MODEL
Bounded finite candidate sets, named Q64.64 feature maps, linear constraints, objective directions/weights, finite scenario utility maps, finite transition graphs, bounded perturbation sets, threshold grids, and explicit engine limits.

## REQUIRED BEHAVIOR
- validate schemas and identifiers;
- reject duplicate IDs and missing dimensions;
- fail closed on overflow/invalid arithmetic;
- use deterministic tie-breaking;
- cap combinatorial searches;
- emit structured certificates with witnesses/reasons;
- preserve source IDs/provenance supplied by caller;
- never manufacture missing values.

## FORBIDDEN BEHAVIOR
- binary float conversion;
- implicit unit conversion;
- silent coercion of malformed values;
- random tie-breaking;
- hidden time dependence;
- external I/O in core engines;
- unbounded exponential search;
- claiming Canon/promotion.

## EDGE CASES
Empty candidate set, all-illegal set, duplicate IDs, zero/negative weights where forbidden, ties, disconnected graphs, absent route, overflow, divide-by-zero, k=0, threshold equality, scenario gaps, unreachable descendants, and combinatorial cap exceeded.

## ACCEPTANCE CRITERIA
- E1 compile/static PASS;
- E2 positive/negative/boundary tests cover all 20 engines;
- E3 at least one integrated pipeline across legality -> topology -> selection -> proof capsule;
- deterministic repeatability across repeated runs;
- stress corpus PASS;
- manifest hashes generated from tested bytes;
- GitHub post-write readback matches expected SHA/content;
- protected NEXY.AI scope remains untouched.

## STOP CONDITIONS
FREEZE if a write would leave authorized scope, a protected repository mutation is required, tested bytes cannot be bound to persisted bytes, a critical test remains failing, or Q64.64 semantics cannot be proven for an operation used by an engine.
