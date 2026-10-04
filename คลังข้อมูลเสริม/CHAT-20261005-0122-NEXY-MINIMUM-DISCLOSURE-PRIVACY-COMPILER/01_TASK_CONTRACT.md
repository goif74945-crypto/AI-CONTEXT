# Task Contract

## Objective
Design, implement, and verify an isolated reference system that plans the minimum lawful/authorized disclosure of task data to an identified recipient.

## Target
`goif74945-crypto/AI-CONTEXT` → `คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-MINIMUM-DISCLOSURE-PRIVACY-COMPILER/`

## Authority sources
1. explicit user directive for this chat;
2. AI-CONTEXT execution kernel and global/security/verification rules;
3. NEXY project overview/current authority matrix/human control surface;
4. official external privacy-risk references as non-governing research support;
5. AI-proposed design decisions in this lab.

## Authorized scope
- create new files inside the new supplemental folder;
- design privacy/minimum-disclosure concepts;
- create standard-library reference code and tests;
- run isolated static/unit validation;
- commit the new folder to AI-CONTEXT;
- re-fetch and verify committed artifacts.

## Protected scope
- no write to any repository whose name contains `NEXY.AI`;
- no edits to NEXY current build matrix/canon;
- no edits to sibling supplemental projects;
- no secret, credential, private production value, or auth token persistence;
- no destructive Git operation or force update.

## Success invariants
- project is explicitly AI-proposed, not canonical;
- policy metadata is separated from raw payload values;
- credential values are never placed in disclosure bundles;
- external-model secret disclosure fails closed;
- recipient/purpose ambiguity freezes;
- non-required fields are omitted;
- retention never exceeds task request or field maximum;
- same normalized policy yields deterministic output/fingerprint;
- frozen plan cannot build a payload bundle;
- tests actually execute and pass before COMPLETE.

## Required evidence
- E0: committed files re-fetched from AI-CONTEXT;
- E1: Python compile and JSON fixture validation;
- E2: unit + invariant test execution;
- no E3/E4/E5/E6 claim.

## Stop conditions
- target identity becomes ambiguous;
- any write would touch protected scope;
- a material source conflict invalidates design assumptions;
- exact commit cannot be advanced safely without overwriting concurrent work;
- required verification fails and cannot be repaired in-scope.
