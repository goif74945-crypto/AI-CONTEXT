# NEXY Lo4 Radical Innovation Foundry

**WORK_CHAT_ID:** `CHAT-20261005-0221-NEXY-LO4-RADICAL-INNOVATION-FOUNDRY`

**Classification:** `AI-PROPOSED / Lo4 / EXPERIMENTAL / NOT CANON`

This bundle contains five executable reference systems designed to add new planning primitives around innovation itself, rather than repeating the existing proof/assurance-heavy supplemental work.

## Five systems
1. **SBC — Surprise Budget Controller**: permits bounded experimental deviation while making any User Law/Canon drift an immediate freeze.
2. **AFRE — Anti-Feature Refutation Engine**: tries to prove a proposed feature should not be built when value is weak, risk is excessive, or a simpler alternative subsumes it.
3. **MRPE — Minimal Relaxation Proposal Engine**: computes exact lowest-cost proposals over explicitly relaxable Lo4 constraints only; it never mutates rules or relaxes Canon.
4. **REP — Regret Envelope Planner**: picks a legal, preferably reversible next action by minimax regret across explicit scenarios without inventing probabilities.
5. **OPC — Option Preservation Compiler**: values current utility together with preserved future maneuverability and penalizes switching cost/lock-in.

## Why this is useful to NEXY
NEXY is a deterministic control hub where AI may generate candidates without becoming authority. These mechanisms let Lo4 be aggressive while keeping creativity, complexity, uncertainty and architectural lock-in bounded and inspectable.

## Run
```bash
./verify.sh
```

## Repository boundary
This code is deliberately stored outside the NEXY.AI implementation repository. It performs no production integration and does not prove compatibility with the current NEXY runtime.
