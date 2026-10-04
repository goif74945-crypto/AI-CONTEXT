# Verification Evidence — Semantic Localization Integrity Lab

Status: `PASS` for the isolated reference lab at E0/E1/E2 only  
Classification: `AI_PROPOSED_CONCEPT_NOT_ADOPTED`  
Durable session code: `CHAT-20261005-0122-NEXY-SEMANTIC-LOCALIZATION-INTEGRITY-LAB`

## Evidence boundary

This record proves only the isolated reference implementation stored under the dedicated AI-CONTEXT supplemental path. It does **not** prove NEXY.AI integration, runtime behavior, deployment readiness, user impact, translation completeness, or adoption into NEXY authority.

## Environment

- Node.js: `v22.16.0`
- npm: `10.9.2`
- OS: `Linux 6.18.44 x86_64`
- Runtime dependencies: Node built-ins only; no external package dependency required by the implementation/tests.

## E0 — Presence / repository identity

Verified stable reference set: **25/25 files**.

Method:
1. compute local Git blob identity with `git hash-object <file>`;
2. fetch the same path from `goif74945-crypto/AI-CONTEXT` through the GitHub connector;
3. require GitHub `fetch_file.sha` to equal local Git blob SHA for every stable file.

Result: **PASS — 25/25 exact blob matches.**

The complete path/hash ledger is persisted in `IMPLEMENTATION_MANIFEST.json` version `2.0`.
The manifest itself was then updated and GitHub returned blob SHA:
`508783e5ba6063d4ec1c5be5f0888978e07e372d`, exactly matching the local final manifest blob.

Manifest lock commit:
`fca3f33cd287c37d3f92e27b6abef4abe5ee510d`

Corrected compact analyzer-test commit:
`7022efb4e271bdfcaea9aa7597e56c53b8abe2ca`

## E1 — Static / contract validation

Command:

```bash
npm run validate
```

Observed:

```text
VALIDATION_PASS required_files=27 policy=0.1.0
```

The validator checks required artifact presence, JSON parseability, default strict policy invariants, EN/TH reference support, canonical-token uniqueness, and expected PASS/FREEZE fixture behavior.

Result: **PASS**.

## E2 — Executed unit/adversarial behavior

Command:

```bash
npm test
```

Observed final summary:

```text
1..39
# tests 39
# pass 39
# fail 0
# cancelled 0
# skipped 0
# todo 0
```

Covered behaviors include:
- EN→TH and TH→EN normative preservation;
- number drift;
- semantic unit drift and EN/TH unit equivalence;
- placeholder loss;
- canonical token loss;
- permission→obligation escalation;
- obligation→recommendation weakening;
- negation polarity changes;
- URL/email/hash/UUID/backtick identifier drift;
- protected literal presence and multiplicity;
- empty source/target;
- Unicode NFC equivalence;
- unsupported target language freeze;
- 100 identical-run deterministic fingerprints;
- deterministic issue ordering;
- policy-override immutability;
- explicit non-authoritative proposal labeling.

Result: **PASS — 39/39**.

## CLI behavior evidence

PASS fixture:

```text
decision=PASS
issueCount=0
fingerprint=fe427e17972fe8bd416a357d2738741febd2f93e6a753fb25ac8f0a784a27998
exit=0
```

FREEZE fixture:

```text
decision=FREEZE
issueCount=1
fingerprint=2a2d337fcf1deb77656ad7495283e5a3686410091c98c3fce8ea5a7857f71d75
exit=3
```

Invalid CLI invocation:

```text
Usage: node src/cli.js <translation-contract.json>
exit=2
```

Result: **PASS**.

## Failure/recovery evidence from development

The build did not hide failures:

1. First test stage: `34/35` PASS. A test expectation collided with the identifier detector. The test design was corrected rather than suppressing the detector.
2. Second stage: `37/39` PASS. A Thai unit-token boundary defect was found. Unit extraction was corrected to use a Unicode-aware boundary rule.
3. Final stage: `39/39` PASS.
4. Multiple GitHub writes received HTTP 409 because AI-CONTEXT HEAD moved concurrently. Writes were retried additively against fresh repository state. No force update, reset, rebase, or history rewrite was used.
5. One analyzer test transfer was detected as truncated and was replaced using current blob precondition. The final remote test blob was proven identical to the passing local file.

## Mutation-scope audit

Every repository write issued by this session targeted:
`goif74945-crypto/AI-CONTEXT`

Every intended artifact path for this lab is under:
`คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-SEMANTIC-LOCALIZATION-INTEGRITY-LAB/`

No write tool call in this session targeted a repository whose name contains `NEXY.AI`.
This statement is limited to actions executed by this session; it does not claim that unrelated actors made no changes elsewhere.

## NOT_VERIFIED

- NEXY.AI production integration: `NOT_VERIFIED`
- NEXY.AI runtime behavior: `NOT_VERIFIED`
- deployment: `NOT_VERIFIED`
- real product localization corpus false-negative rate: `NOT_VERIFIED`
- cultural/linguistic quality: `NOT_VERIFIED`
- adoption as authoritative NEXY requirement: `NOT_ADOPTED`
