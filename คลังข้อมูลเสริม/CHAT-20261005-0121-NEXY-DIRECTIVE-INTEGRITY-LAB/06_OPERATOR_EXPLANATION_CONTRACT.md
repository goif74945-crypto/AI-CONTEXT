# Operator Explanation Contract

Status: AI-PROPOSED

## Goal
Expose enough information for an operator to understand what contract is being enforced without exposing hidden model reasoning or pretending that an internal chain of thought is evidence.

## Snapshot view
The reference `operator_explanation(snapshot)` returns:
- stage;
- action;
- target;
- mutation class;
- impact class;
- in/out scope;
- constraints;
- declared side effects;
- ambiguity state;
- deterministic contract digest.

## Transition view
`compare` returns:
- PASS or FREEZE;
- parent and child digests;
- each blocking violation with code/path/parent value/child value/operator message;
- authorization grants actually consumed.

## Forbidden presentation behavior
- no invented user intent;
- no “AI thinks you meant…” promotion to authority;
- no hidden chain-of-thought field;
- no generic success while violations remain;
- no collapsing FREEZE into a warning;
- no omitting a changed protected target/scope merely because downstream work succeeded.

## Product principle
A normal user can see a concise state such as “scope expanded to repo B; explicit authorization required.” An architect/auditor can inspect the structured delta and digests. Both surfaces derive from the same facts.
