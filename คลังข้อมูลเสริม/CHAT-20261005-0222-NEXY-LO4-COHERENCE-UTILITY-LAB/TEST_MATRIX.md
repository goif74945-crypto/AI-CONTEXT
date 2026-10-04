# Test Matrix

| Concept | Positive proof | Negative/adversarial proof |
|---|---|---|
| BKR | valid-time split, correction via explicit supersession | future-knowledge leakage blocked, equal-authority disagreement conflicts, cycle rejected, no data stays UNKNOWN |
| CEML | permutation-invariant merge, idempotent replay, tombstones | equal-authority conflict preserved, claim-ID collision rejected, unknown retraction rejected |
| CUVL | higher/lower-is-better primary and guard metric direction detection | insufficient evidence NOT_VERIFIED, either-direction guard regression/falsifier FALSIFIED, invalid direction rejected, weak effect not mislabeled benefit |
| STCE | parent and most-specific scope resolution, scoped aliases | unknown term UNKNOWN, exact-definition conflict, alias collision and ambiguous alias rejected |
| FSA | PASS identity, commutative/idempotent join | CONFLICT dominance, unresolved required dependency blocks local PASS, empty join rejected |
| Integration | all five compose in an advisory path | concurrent conflict propagates to final FSA gate |
