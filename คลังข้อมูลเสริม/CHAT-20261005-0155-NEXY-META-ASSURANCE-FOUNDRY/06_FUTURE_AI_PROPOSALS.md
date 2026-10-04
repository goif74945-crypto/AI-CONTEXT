# Future Systems — AI-Proposed Only

Everything in this file is a **proposal by AI**, not a NEXY requirement, implementation claim or roadmap commitment.

## P1 — Proof Frontier Cache with Revision Invalidation
Memoize EECP proof frontiers by exact graph fingerprint and invalidate only affected ancestors when evidence contracts change. Goal: preserve exactness while reducing repeated planning cost.

## P2 — Unknown-Domain Abstraction Refinement
Extend UIS from explicit finite domains to bounded symbolic partitions. Begin coarse, split only when two values in a partition produce different outputs. Any unresolved abstraction returns NOT_VERIFIED/FREEZE rather than approximate stability.

## P3 — Cross-Stage Conservation Trace
Chain ICK reports into a signed/hashed transition ledger so a downstream reviewer can prove where authority/evidence/constraints changed and which receipt authorized each change.

## P4 — Failure-Witness Semantic Anchors
Allow MFWR elements to carry dependency keys so the reducer can preserve mandatory setup/teardown anchors and minimize only legally removable slices.

## P5 — Saturation Escape Planner
When ESC reports saturation, select a structurally different next evidence source/domain instead of another equivalent agent. This should integrate with a resource governor but remain unable to weaken evidence floors.

## P6 — Proof Fragility Heatmap
Use EECP minimal cutsets to expose claims with single-evidence points of failure. UI can prioritize independent corroboration without presenting a numeric confidence score as truth.

## P7 — Conservation Metamorphic Suite
Generate metamorphic tests from ICK laws: input reorder, stage splitting/merging, redundant evidence, and capability removal should preserve verdict semantics when the protected quantities are unchanged.

## P8 — User-Burden Gate
Combine UIS materiality with a clarification optimizer so the system can prove both: (a) which unknowns matter, and (b) the smallest authorized question set needed to resolve them. No guessed answers.
