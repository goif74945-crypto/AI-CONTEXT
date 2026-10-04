# Design — Epistemic Saturation Controller (ESC)

Classification: `AI_PROPOSED_CONCEPT / REFERENCE_IMPLEMENTATION`

## Problem
Multi-agent systems can waste budget by repeating the same claims and evidence. Worse, repetition can look like stronger consensus even when every answer traces to the same provider/domain or the same evidence artifact. Resource allocation alone does not identify this epistemic stagnation.

## Core model
Each round contains structured contributions with explicit:
- `agent_id`;
- `independence_domain` (provider/model/source family chosen by the integrating authority);
- stable `claim_ids`;
- stable `evidence_refs`.

ESC counts only structural novelty:
1. a claim ID never observed before;
2. an evidence reference never observed before;
3. a new `(claim_id, independence_domain)` support pair.

Repeating the same claim/evidence/domain adds **zero novelty**. ESC never uses embeddings or fuzzy semantic similarity.

## Saturation rule
After `min_rounds`, if the final `patience` consecutive rounds have novelty score zero, the controller returns:
- `SATURATED`
- `STOP_EXPANSION`

Otherwise it returns `ACTIVE / CONTINUE`.

Saturation is **not** verification, consensus, correctness or permission to release. It only says additional rounds of the same structural kind are currently adding no declared independent information.

## Integration proposal
Potentially useful inside a NEXY-compatible swarm budget loop, upstream of final JUDGE. LAW/JUDGE still decide whether evidence suffices and whether a result may release.
