# Adversarial Corpus Design

Status: `AI_PROPOSED_CONCEPT_NOT_ADOPTED`

## Threat families
1. **Authority weakening**: must → should, must not → may.
2. **Authority escalation**: may → must.
3. **Polarity inversion**: must → must not, prohibition negation removed.
4. **State erasure**: `FREEZE` paraphrased or dropped.
5. **Quantity drift**: same unit/different number.
6. **Unit drift**: same number/different unit.
7. **Template corruption**: dropped/renamed placeholder.
8. **Reference mutation**: URL/email changed.
9. **Identity mutation**: hash/UUID/backtick/UPPER_SNAKE changed.
10. **Multiplicity drift**: protected literal occurs fewer/more times.
11. **Unsupported-language false confidence**: unvalidated language pair accidentally PASSes.
12. **Unicode normalization noise**: canonically equivalent strings should not false-freeze.
13. **Non-deterministic reporting**: repeated execution produces different report identity.

## Current executable coverage
The test suite covers PASS and FREEZE cases across these families, including EN→TH and TH→EN normative checks.

## Future corpus expansion
- decimal/thousands formatting equivalence;
- Thai digits vs Arabic digits;
- unit conversion with authorized conversion contracts;
- punctuation-induced negation ambiguity;
- mixed-language control surfaces;
- pluralization and classifier effects;
- bidi scripts and directionality marks;
- ICU/message-format placeholders;
- Markdown links and code fences;
- HTML/ARIA attributes;
- accessibility labels;
- date/time/timezone preservation.

Every future fixture should include an expected legal decision before execution. A corpus case with no predeclared oracle is research data, not a verification test.
