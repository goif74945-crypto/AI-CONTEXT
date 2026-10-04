# Architecture

Status: `AI_PROPOSED_CONCEPT_NOT_ADOPTED`

## Pipeline

```text
TRANSLATION CONTRACT
  ↓
NFC NORMALIZATION
  ↓
STRUCTURAL EXTRACTORS
  ├─ numbers
  ├─ semantic units
  ├─ placeholders
  ├─ URLs / emails
  ├─ identifiers / hashes / UUIDs
  ├─ canonical NEXY tokens
  └─ caller-protected literals
  ↓
LANGUAGE SEMANTIC EXTRACTOR
  ├─ prohibition
  ├─ obligation
  ├─ permission
  ├─ recommendation
  └─ negation
  ↓
MULTISET + SEMANTIC-CLASS COMPARISON
  ↓
DETERMINISTIC ISSUE SORT
  ↓
BLOCK? ─ yes → FREEZE
  └─ no → PASS
  ↓
STABLE SHA-256 REPORT FINGERPRINT
```

## Modules
- `src/extract.js`: deterministic structural extractors and semantic unit normalization.
- `src/language.js`: EN/TH normative-class and negation detection.
- `src/multiset.js`: duplicate-sensitive preservation comparison.
- `src/policy.js`: default policy loading and controlled override merge.
- `src/index.js`: orchestration, failure decisions, deterministic report/fingerprint.
- `src/cli.js`: minimal executable interface with meaningful exit codes.
- `config/default-policy.json`: default strict policy.
- `schema/*.schema.json`: machine-readable contract descriptions.
- `tests/*.test.js`: executable E2 behavior evidence for the isolated module.
- `fixtures/*.json`: example PASS/FREEZE inputs.

## Authority boundary
This gate does not decide NEXY system law. It checks a proposed localization invariant policy. Any production adoption would require an authorized policy owner to define which literals, canonical tokens, languages, severity levels, and surfaces are legally protected.

## Determinism
The implementation avoids network calls, model calls, timestamps, randomness, locale-dependent sorting, and external packages. Identical normalized input + policy produces deterministic issue ordering and fingerprint.

## Failure behavior
- malformed CLI input: process exit `2`;
- invariant violation: decision `FREEZE`, process exit `3`;
- all checked invariants preserved: decision `PASS`, process exit `0`;
- unsupported language under strict policy: `FREEZE`.

## Evolution law proposal
New language support must add:
1. explicit language rules;
2. adversarial fixtures for prohibition/obligation/permission/recommendation/negation;
3. unit aliases when language-specific names are supported;
4. regression against all prior language pairs;
5. an authorized adoption decision outside this lab.
