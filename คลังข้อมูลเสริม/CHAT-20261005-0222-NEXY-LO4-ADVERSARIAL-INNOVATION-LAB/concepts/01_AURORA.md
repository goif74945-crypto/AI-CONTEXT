# AURORA — Abstention Utility & Risk-Oriented Reliability Analyzer

Status: `Lo4_AI_PROPOSAL_ONLY`

## Problem
Typical agent evaluation rewards answer correctness but often under-measures the decision **whether to answer at all**. For a zero-guess control system, an agent that hallucinates confidently on unanswerable tasks is more dangerous than one that abstains, while an agent that abstains on everything is operationally useless.

## Mechanism
AURORA evaluates weighted cases with:
- answerable vs unanswerable ground truth;
- ANSWER vs ABSTAIN action;
- correctness for answered cases;
- confidence for answered cases;
- risk weight.

It emits unsafe-answer rate, needless-abstention rate, Brier calibration, reliability score and reason-coded admission status.

## Invariants
- ANSWER must have correctness and confidence.
- ABSTAIN cannot smuggle an answer confidence/correctness label.
- all risk weights are positive and finite.
- unsafe answering and needless abstention remain separate diagnostics.

## NEXY value
Can support model/provider/agent admission and routing so SWARM diversity does not reward agents merely for verbosity or willingness to guess.
