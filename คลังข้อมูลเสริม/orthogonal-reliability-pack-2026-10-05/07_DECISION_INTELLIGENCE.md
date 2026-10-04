# Architecture Decision Intelligence
ADR fields: adr_id, status, context, decision, alternatives, constraints, invariants_preserved, tradeoffs, failure_modes, reversal_cost, migration_path, verification, evidence, supersedes, superseded_by.

Decision questions: Which requirement motivates it? Does it remain justified if a constraint disappears? Which failures are accepted? What is blast radius? How is reversal done? Which observable signal invalidates the assumption?

Reversibility: R0 config/trivial; R1 localized migration; R2 multi-component migration; R3 data/protocol migration; R4 externally committed ecosystem contract. Higher reversal cost requires stronger evidence and authority.

Anti-cargo-cult rule: no pattern is selected merely because it is called best practice. It must be justified by actual constraints and measurable tradeoffs.
