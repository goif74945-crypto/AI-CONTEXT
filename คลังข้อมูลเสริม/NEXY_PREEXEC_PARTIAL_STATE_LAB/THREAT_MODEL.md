# PEPSA Threat Model

**Status:** experimental design analysis, not a security certification.

## Assets

- correctness of the preflight verdict;
- integrity of plan/policy identity hashes;
- protected-resource boundary;
- deterministic execution order;
- accurate residual-state detection;
- inability of the analyzer to cause side effects.

## Threats and current controls

| Threat | Current v0.1 control | Residual limitation |
|---|---|---|
| Plan self-authorizes a forbidden boundary | policy is a separate input | caller must supply authentic policy |
| Unknown field hides a typo/bypass | strict unknown-field rejection | semantic mistakes in valid fields remain possible |
| Dependency omission changes execution order | explicit DAG + missing-reference checks | completeness of declared dependencies is not independently proven |
| Cyclic plan deadlocks | cycle rejection | none for declared graph |
| Protected NEXY source is mutated | deterministic protected-resource glob gate in example policy | resource aliases/canonical identity must be solved by integration layer |
| External action retries duplicate an effect | required idempotency-key metadata | provider behavior is not verified |
| Irreversible action strands partial state | nonterminal irreversible mutation freezes | hidden irreversibility falsely declared reversible remains a risk |
| Fake rollback declaration grants safety | rollback string must exist | rollback behavior is not executed or proven in v0.1 |
| Approval ID is forged | structural approval required | authenticity/replay protection not implemented |
| Equivalent plan hashes differ by array order | semantic normalization for step/dependency/evidence/policy set order | textual fields remain exact identity by design |
| Unicode alternate composition changes identity | parser rejects non-NFC strings | confusable characters are not prohibited |
| Control characters hide content | ASCII control characters rejected | full visual-confusable defense is not implemented |
| Floating-point canonical drift | float values rejected | future decimal/fixed-point schema would need explicit law |
| Report tampering | combined SHA-256 identity available | report is not signed in v0.1 |
| Stale policy is used | policy hash binds report | freshness/authority version is caller responsibility |
| TOCTOU resource changes after preflight | none | requires runtime source/resource identity pinning |
| Analyzer gains side-effect capability | implementation has no network/subprocess/execution code; CLI reads JSON and prints report | packaging/runtime sandbox still matters in integration |

## Fail-closed cases implemented

- invalid JSON shape;
- unknown fields;
- invalid enum;
- invalid max-step type/value;
- non-NFC strings;
- control characters;
- duplicate step IDs;
- duplicate dependencies;
- missing dependencies;
- self-dependency;
- graph cycle;
- unauthorized boundary;
- protected-resource mutation;
- missing mutation postcondition;
- missing mutation evidence requirement;
- reversible-without-rollback inconsistency;
- rollback-on-irreversible inconsistency;
- external effect without required idempotency key;
- irreversible mutation without approval;
- nonterminal irreversible mutation;
- unsafe residual partial state;
- plan-size limit violation.

## Required red-team work before promotion

1. resource alias corpus (`./`, `../`, URL encoding, symlink identity, case behavior, Git ref ambiguity);
2. Unicode confusables corpus;
3. stale-policy and downgrade attacks;
4. approval replay/spoofing;
5. dependency under-declaration;
6. rollback false-claim attacks;
7. provider idempotency mismatch;
8. plan/report substitution attacks;
9. TOCTOU between preflight and action execution;
10. executor performs undeclared effects.

A future security claim requires executed abuse tests against the integrated boundary, not this document.
