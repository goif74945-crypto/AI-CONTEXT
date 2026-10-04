# Future Ideas

> **ALL ITEMS IN THIS FILE ARE AI-PROPOSED CONCEPTS.**
>
> They are not current NEXY requirements, not implementation facts and not authorized scope expansion.

## 1. Recovery Graph

Represent multi-step recovery as a deterministic graph:
- node = current freeze state;
- edge = authorized recovery action;
- guard = required evidence/authority;
- terminal = recovered, permanently blocked or escalated.

Benefit: UI can show exact next safe step without inventing a workflow.

Risk: graph could accidentally become an alternate state machine. It must remain derived from authoritative runtime state.

## 2. Freeze Explainability Budget

Define a maximum disclosure budget per freeze class:
- user-facing cause granularity;
- evidence-ref granularity;
- internal detail ceiling;
- security redaction mode.

Benefit: predictable disclosure and less accidental leakage.

## 3. Recovery Outcome Telemetry

Measure whether recovery guidance actually helps:
- median time to valid correction;
- repeated invalid input rate;
- action-selection dead ends;
- UNKNOWN_REASON frequency;
- percentage of freezes resolved without operator escalation.

Benefit: optimize UX using real outcomes rather than stylistic opinions.

## 4. Action Capability Tokens

Instead of plain action codes, upstream could issue short-lived signed capability tokens bound to:
- event;
- action;
- actor;
- scope;
- expiry;
- policy version.

Benefit: a rendered button could carry cryptographic evidence that the action was authorized.

This requires real security design and is not implemented here.

## 5. Semantic Localization Verification

Machine action policy remains language-independent, but translated text can still mislead users.

Future gate:
- bilingual semantic equivalence fixtures;
- forbidden-authority phrase scanner;
- human review for high-risk freeze classes.

## 6. Freeze Replay Corpus

Build a privacy-safe fixture corpus of historical freeze categories and expected recovery cards.

Benefit:
- regression testing;
- policy migration tests;
- UI snapshot tests;
- unknown-reason compatibility.

Do not copy secrets/raw incidents into the corpus.

## 7. Recovery Simulation Sandbox

Before policy deployment:
- feed synthetic freeze events;
- simulate roles/disclosures/locales;
- inspect exact cards/actions;
- diff fingerprints between policy versions.

Benefit: policy changes become reviewable artifacts.

## 8. User Friction Classifier

Classify whether a freeze requires:
- user correction;
- operator intervention;
- external dependency recovery;
- system-only recovery;
- permanent stop.

This must be derived from authoritative reason/recovery metadata, not guessed by an LLM.

## 9. Accessible Freeze Surface

Future UI acceptance:
- keyboard-first actions;
- screen-reader status announcements;
- no color-only state semantics;
- concise action labels;
- stable focus after correction.

## 10. Policy Diff Compiler

Given policy vN and vN+1, produce:
- reasons whose action set changed;
- retryability changes;
- disclosure changes;
- localization-only changes;
- fixtures needing revalidation.

Benefit: safer evolution of a strict presentation-policy layer.

## Promotion rule

Any idea above requires:
1. explicit promotion authorization;
2. mapping to current NEXY authority/build spec;
3. dedicated task contract;
4. correct evidence class;
5. no silent inheritance of this lab's PASS status.
