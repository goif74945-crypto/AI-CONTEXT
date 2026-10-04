# Invariants and Failure Model

Status: `AI_PROPOSED_CONCEPT_NOT_ADOPTED`

## I-01 Numeric preservation
The source and target numeric lexeme multisets must match exactly under the reference strict policy.

Reason: changing `5` to `6`, `99%` to `90%`, or a sign can change behavior even when grammar remains fluent.

## I-02 Semantic unit preservation
Recognized quantity units are normalized to semantic classes before comparison, allowing `seconds` ↔ `วินาที` while rejecting `ms` ↔ `s`.

## I-03 Placeholder preservation
Template placeholders are duplicate-sensitive and exact. Dropping or renaming one freezes.

## I-04 Address/reference preservation
URLs and email addresses are exact-value invariants.

## I-05 Identifier preservation
SHA-256 values, UUIDs, backtick identifiers, and UPPER_SNAKE identifiers are exact-value invariants.

## I-06 Canonical token preservation
Configured NEXY control/role/status tokens must retain multiplicity. A translator may not silently paraphrase away `FREEZE`, `PASS`, `OWNER`, etc.

## I-07 Caller-protected literal preservation
Callers may add exact literals such as state names, protocol names, command strings, or legal labels.

## I-08 Normative modality preservation
The presence of semantic classes must agree across supported languages:
- PROHIBITION
- OBLIGATION
- PERMISSION
- RECOMMENDATION

This catches both weakening and authority escalation.

## I-09 Negation polarity preservation
Presence/absence of explicit negation must not flip.

## I-10 Unsupported semantics do not PASS
If a configured language is unsupported by the deterministic semantic layer, strict mode freezes rather than treating unchecked text as verified.

## I-11 Deterministic report identity
Equivalent input/policy produces the same sorted issues and SHA-256 report fingerprint.

## Failure classes
- `E_EMPTY_SOURCE`
- `E_EMPTY_TARGET`
- `E_NUMBER_MISMATCH`
- `E_UNIT_MISMATCH`
- `E_PLACEHOLDER_MISMATCH`
- `E_URL_MISMATCH`
- `E_EMAIL_MISMATCH`
- `E_IDENTIFIER_MISMATCH`
- `E_CANONICAL_TOKEN_MISMATCH`
- `E_PROTECTED_LITERAL_MISMATCH`
- `E_MODALITY_MISMATCH`
- `E_NEGATION_MISMATCH`
- `E_UNSUPPORTED_SOURCE_LANGUAGE`
- `E_UNSUPPORTED_TARGET_LANGUAGE`

## Known limitations
- Regex-based language rules are intentionally narrow and can produce false positives/negatives outside tested constructions.
- Exact numeric lexeme preservation rejects equivalent formatting transformations such as `1,000` ↔ `1000`; production policy may need explicit canonical numeric normalization.
- The unit vocabulary is finite.
- The reference model does not detect lexical meaning drift unrelated to protected invariants.
- It cannot prove translation quality, cultural appropriateness, completeness, or full semantic equivalence.
