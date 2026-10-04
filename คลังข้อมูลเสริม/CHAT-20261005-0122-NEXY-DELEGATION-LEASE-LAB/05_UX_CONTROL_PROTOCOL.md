# 05 — UX Control Protocol

## Goal
Make authority visible without turning execution into a confirmation-dialog factory.

## Principle
Authorize **effects**, not internal model chatter.

A compact pre-execution summary may show read/write/send/delete effects, resource/destination scope, maximum actions/cost, authorization window, and a short plan fingerprint. The UI is AI-proposed and must obey NEXY's UI Truth Contract.

## Confirmation policy
Do not prompt per action while plan fingerprint, resource/effect/destination scope, remaining budget, active lease, and higher-authority state remain unchanged.

Require a new authorization path when:
- plan hash changes;
- a new resource/destination appears;
- effect class becomes higher impact;
- budget increases;
- lease expires/revokes;
- policy version changes;
- upstream law requires it.

## Freeze message
Expose the exact blocking boundary without hidden chain-of-thought. State what changed, whether any external action occurred, and that a new authorization is required when applicable.

## Anti-dark-pattern rules
Do not preselect high-impact authority, minimize irreversible effects, hide destinations, auto-renew authority, retry around FREEZE, imply refusal harms the account, or show success before backend confirmation.

## Candidate metrics
Prompts per successful task; percent caused by real authority change; unsafe attempts blocked; false-freeze rate; time-to-understand freeze; reauthorization abandonment; ability to predict effects before approval.
