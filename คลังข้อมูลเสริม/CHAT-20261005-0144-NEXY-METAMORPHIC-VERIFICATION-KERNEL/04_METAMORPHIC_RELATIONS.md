# Metamorphic Relation Catalog v0.1

## MR-DETERMINISTIC-REPLAY
Same relevant case is executed twice. The configured structural projection must remain equal.

## MR-IRRELEVANT-CONTEXT-INVARIANCE
A caller-designated irrelevant context key/value is added. The configured projection must remain equal. The relation does not itself decide what is irrelevant; that assertion belongs to the test author.

## MR-SEMANTIC-VARIANT-INVARIANCE
A caller-provided prompt variant asserted to preserve intent replaces the seed prompt. The configured structural projection must remain equal. Semantic equivalence is an input assumption to this relation, not model-generated truth.

## MR-PERMISSION-REDUCTION-MONOTONICITY
A strict subset of permissions is produced. The derived run must not introduce new side effects and must not turn an unreleased baseline into a released output.

## MR-EVIDENCE-REMOVAL-SAFETY
Evidence tokens are removed. Less evidence must not introduce new side effects or transform an unreleased baseline into a released output.

## Future relation families (AI-proposed only)
- localization round-trip relation with human-verified semantic anchors;
- context-compaction preservation relation;
- tool-substitution contract relation;
- timeout/dependency-loss degraded-mode relation;
- idempotent duplicate-request relation with effect receipts;
- order-independence relation for explicitly commutative facts;
- secret-redaction noninterference relation;
- stale-evidence downgrade relation.
