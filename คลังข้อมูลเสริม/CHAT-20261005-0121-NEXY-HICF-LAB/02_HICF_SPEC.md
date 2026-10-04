# 02 — HICF REFERENCE SPECIFICATION v0

**Authority:** AI-PROPOSED, supplementary only.

## 1. Inputs

HICF consumes an `IntentEnvelope` and an `ActionCandidate`.

### IntentEnvelope

Required semantic fields:
- `objective`
- `constraints[]`
- `immutables[]`
- `prohibited[]`
- `unknowns[]`
- `authority_state`
- `authority_refs[]`

Unknowns are classified as:
- `NON_MATERIAL`: does not affect correctness/safety/authority of the immediate action;
- `MATERIAL`: can alter the correct action or its contract;
- `CRITICAL`: proceeding is unacceptable without resolution.

Authority state:
- `RESOLVED`
- `UNRESOLVED`
- `CONFLICT`

### ActionCandidate

Required fields:
- action identifier;
- capability description;
- impact (`LOW|MEDIUM|HIGH|CRITICAL`);
- reversibility (`REVERSIBLE|PARTIALLY_REVERSIBLE|IRREVERSIBLE`);
- mutation flag.

## 2. Outputs

The clarification gate emits exactly one decision:
- `PROCEED`
- `ASK`
- `FREEZE`

and structured reason codes plus required clarification keys.

## 3. Decision precedence

1. Authority conflict → `FREEZE`.
2. Prohibited capability → `FREEZE`.
3. Critical unknown → `FREEZE`.
4. Material unresolved authority for mutation/high-impact/irreversible action → `ASK`.
5. Material unknown → `ASK`.
6. Irreversible action with unresolved unknowns → `ASK`.
7. Critical-impact action with unresolved unknowns → `ASK`.
8. Otherwise → `PROCEED`.

## 4. Determinism

Canonicalization rules:
- normalize whitespace;
- sort set-like string collections case-insensitively;
- de-duplicate unknown keys;
- serialize with sorted JSON keys;
- fingerprint using SHA-256.

Equivalent semantic inputs SHOULD yield the same intent fingerprint.

## 5. Friction budget

The friction budget is advisory. It may emit:
- `CLARIFICATION_BUDGET_EXCEEDED`
- `REPEATED_QUESTION`

It MUST NOT convert an `ASK` or `FREEZE` required by correctness/authority into `PROCEED`.

## 6. Preference handling

Preference scopes:
- `EPHEMERAL`
- `PROJECT`
- `DURABLE`

A durable preference MUST be explicit and MUST carry provenance. Behavioral inference alone is insufficient authority for durable persistence.

## 7. Drift classes

- `NONE`: no material intent change;
- `LOW`: constraint/unknown set changed without changing objective/immutables/prohibitions;
- `MATERIAL`: objective or prohibition set changed;
- `AUTHORITY_BREAK`: immutable contract changed or authority entered conflict.

## 8. Stop conditions

HICF processing stops with `FREEZE` on authority conflict, explicit prohibited capability, or critical unknown under this reference policy.

## 9. Forbidden behavior

- invent missing user authority;
- erase an immutable constraint to make execution easier;
- infer durable preference from usage frequency;
- ask the same resolved question without new material evidence;
- optimize away a clarification that materially changes correctness;
- represent HICF as canonical NEXY implementation without adoption evidence.
