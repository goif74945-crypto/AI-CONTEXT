# Collision Analysis vs Existing Supplemental Work

## Baseline inspected
The `คลังข้อมูลเสริม` tree contained many active experiments through roughly 01:53 local time, including clarification optimization, proof graphs, proof sensitivity, context fidelity, idempotency/replay, handoff/resume, evidence capsules, policy impact, model substitution, concurrency/interleaving, provenance taint, and a competing 01:53 five-concept mission proposing Proof Lattice, Authority Conflict Compiler, Replay Seal, Runtime Capability Gate, and Delta Impact.

## Why these five are orthogonal

### ICG vs Clarification Optimizer
The existing Clarification Optimizer chooses the cheapest question set **after unknowns are already blocking**. ICG asks an earlier question: *does the ambiguity matter to the legal decision at all?* If all admissible interpretations produce the same decision signature, clarification is unnecessary. If not, ICG freezes and can hand the divergent fields downstream to a clarification system.

### CNS vs Context/Privacy Firewalls
A firewall controls what context crosses a boundary. CNS provides a **behavioral noninterference test** over a finite mutation set: changing context declared irrelevant/untrusted must not change the decision signature. It is evidence about influence, not merely an access rule.

### EAP vs Evidence Capsules/Proof Lattices
Capsules/lattices organize evidence already available. EAP solves the upstream optimization problem: *which tests/probes should be executed next to meet exact evidence-class obligations at minimum deterministic cost?* It forbids evidence-class substitution.

### REC vs Existing Handoff/Resume Protocol
Existing handoff/resume validates freshness, HEAD, claims, and recovery policy. REC adds a separate **resumption-equivalence witness**: a reconstructed state must produce the same resume-critical fingerprint and next legal action, while explicitly ignoring ephemeral UI/session noise.

### IEQE vs Proof Graph / Provenance Taint
Proof graphs and taint track derivation. IEQE asks whether a claim has a required count of **independent witnesses after expanding ancestry**, rejecting apparent diversity that shares a producer, failure domain, or dependency ancestor. It targets common-mode proof failure and circular/self-supporting evidence.

## Claim discipline
This analysis establishes design distinction from inspected artifacts, not global mathematical uniqueness across all possible prior work.
