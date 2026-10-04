# NEXY Meta-Assurance Foundry — Five AI-Proposed Reference Systems

Status: `AI_PROPOSED / EXPERIMENTAL / NON_AUTHORITATIVE`
Work tag: `CHAT-20261005-0155-NEXY-META-ASSURANCE-FOUNDRY`

This foundry intentionally targets five gaps that are orthogonal to the inspected supplemental labs. It does not claim that NEXY.AI currently lacks equivalent mechanisms, and it does not modify NEXY.AI.

## The five systems

1. **Invariant Conservation Kernel (ICK)** — verifies that authority, evidence, uncertainty, constraints and capabilities cannot silently inflate or weaken across a transformation pipeline.
2. **Minimal Failure Witness Reducer (MFWR)** — deterministically shrinks a failing trace/case to a 1-minimal reproducible witness while detecting unstable/nondeterministic oracles.
3. **Epistemic Saturation Controller (ESC)** — detects when additional swarm rounds add no independent evidence/claims and prevents consensus-by-repetition from masquerading as progress.
4. **Exact Evidence Cut Planner (EECP)** — computes exact bounded minimal evidence sets that can prove a claim and minimal evidence cutsets whose loss would break proof.
5. **Unknown Impact Slicer (UIS)** — exhaustively proves whether unresolved variables can change a legal output, so harmless unknowns need not block while material unknowns remain explicit.

## Integration philosophy
Each module is an adapter-friendly pure reference core. Future integration should place it behind NEXY authority boundaries. None of these modules may override USER LAW, CORE, LAW or JUDGE. Their outputs are advisory/proof artifacts only until separately promoted by authoritative specification and verified integration evidence.
