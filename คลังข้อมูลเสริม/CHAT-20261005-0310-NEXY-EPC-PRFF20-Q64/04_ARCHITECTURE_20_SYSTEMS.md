# PRFF20 Architecture: Twenty Executable Mechanisms

## System model
Input is a directed acyclic support graph:
`ROOT -> EVIDENCE -> ... -> CLAIM`.

ROOT represents an upstream proof/source root. EVIDENCE represents proof artifacts or transformations. CLAIM is a target proposition/candidate claim. PRFF treats these labels as supplied metadata; it verifies graph structure/resilience, not real-world truth.

Hard bounds default to 96 nodes, 512 edges and 1,000,000 exact-search states.

### Numeric substrate
All authoritative normalized metrics are Q64.64 using signed `__int128_t` raw storage and `boost::multiprecision::int256_t` intermediates. Overflow is checked. Ratios intended for `[0,1]` reject out-of-domain values unless the metric explicitly defines clamping. Connectivity/cut cardinalities are exact integers; Q64.64 is used when cardinalities are normalized into scores.

### Flow substrate
Deterministic Dinic max-flow with integer capacities is used. `INF_CAP = 1,000,000,000`, safely above every possible finite flow under the hard node/edge bounds. Evidence vertex cuts use node splitting. Root-and-edge channel analysis caps roots and support edges. Residual reachability extracts canonical cut witnesses.

## C01 — Graph Contract Integrity
Rejects empty IDs, duplicates, missing endpoints, self edges, edge emission from CLAIM, edge ingress into ROOT, target-kind mismatch, bounds violations and cycles. Successful evaluation proves only structural admissibility.

## C02 — Target Reachability Closure
Every declared target must have at least one reachable ROOT. Unrooted targets cannot enter the resilience certificate.

## C03 — Root Support Diversity
Counts distinct roots reaching each target and compares against policy. This is source-count evidence only; C04 checks whether those roots actually have separate transport channels.

## C04 — Root-and-Edge-Disjoint Channel Count
Max-flow caps each ROOT and each support edge at one while evidence nodes are not capacity-limited. Three roots that merge through one support edge therefore count as one channel, preventing root-count theater.

## C05 — Evidence Vertex Connectivity
Caps EVIDENCE nodes at one and support edges at effectively infinite capacity. The result is the number of evidence-node-disjoint proof paths available to the target.

## C06 — Minimum Evidence Vertex Cut
Extracts the canonical residual minimum set of evidence nodes whose removal disconnects all root support. It is a concrete fracture certificate, not a vague confidence value.

## C07 — Edge Connectivity
Computes exact minimum number of support edges whose removal can disconnect root support from the target.

## C08 — Minimum Edge Cut
Extracts canonical minimum support-edge cut witnesses from the residual network.

## C09 — Universal Dominator Guard
Removes each evidence node deterministically. Any node whose removal disconnects all roots is a universal evidence dominator and a hard single point of proof failure.

## C10 — Fracture Node Impact
For every evidence node, measures the reduction in evidence vertex connectivity caused by its removal. Score is `1 - worst_loss/baseline` for finite baseline connectivity. Advisory only.

## C11 — Hard Bridge Guard
Removes each support edge. If one edge alone disconnects every root from a target, it is a hard support bridge and blocks review readiness.

## C12 — Root Ablation Survival
Removes every relevant root one at a time and requires all target topology thresholds to remain satisfied. This distinguishes “currently enough roots” from “still enough after one root disappears”.

## C13 — Evidence Ablation Survival
Removes every evidence node one at a time and requires the graph to remain above policy thresholds.

## C14 — Exact k-Ablation Failure Threshold
Enumerates evidence subsets in increasing cardinality until the first subset causes topology policy failure. Search is exact within the declared state budget; exhaustion produces `EXACT_ABLATION_BUDGET_EXHAUSTED` and blocks C20 instead of estimating.

## C15 — Minimum Cut Family Enumeration
For each finite minimum evidence-disconnect cut size, enumerates all minimum-cardinality evidence cutsets in deterministic order within budget. This exposes whether one canonical cut hides multiple equivalent fracture surfaces.

## C16 — Cut Family Concentration
Measures how often the most recurrent evidence node appears across the exact minimum-cut family. Score is one minus that appearance fraction. Advisory, because concentration can be informative without itself violating a hard policy.

## C17 — Multi-Claim Shared Bottleneck
Counts evidence nodes whose removal reduces evidence connectivity for at least two target claims. Under `requireMultiClaimIsolation`, any shared bottleneck blocks C20.

## C18 — Cross-Claim Cut Overlap
Computes pairwise Jaccard overlap between canonical minimum evidence cuts. Under multi-claim isolation policy, non-zero overlap blocks readiness.

## C19 — Repair Priority Advisory
Ranks evidence nodes deterministically by aggregate marginal connectivity impact plus minimum-cut-family membership. It emits advice only; no node, file, state or Canon is modified.

## C20 — Review Resilience Certificate
Aggregates hard mechanisms and emits exactly one of:
- `READY_FOR_JUDGE_LAW_REVIEW_ONLY`
- `NOT_READY_FOR_JUDGE_LAW_REVIEW`

It never emits KEEP, CUT, ACCEPT, PROMOTE, STABLE, FINAL or a Core transition. C20 is evidence for a higher authority, not authority itself.

## Hard C20 set
C01, C02, C03, C04, C05, C06, C07, C08, C09, C11, C12, C13, C14, C15, C17 and C18 are hard when their relevant policy applies. C10, C16 and C19 are advisory diagnostics.
