# Authority Calculus

Status: PROPOSAL grounded in FACT_PROJECT

## Goal
Represent authority resolution as a deterministic relation rather than prose intuition.

## Objects
Let a candidate directive be:
D = {id, issuer, source, scope, version, effective_range, norm, target, preconditions, supersedes, evidence_ref}

Let a decision context be:
C = {task, target, source_identity, runtime_identity, time_metadata, requested_action, evidence_set}

## Required predicates
- APPLIES(D,C): directive scope and preconditions match context.
- CURRENT(D,C): directive has not been superseded for this context.
- AUTHORIZED(D,C): issuer/source is allowed to govern target/action.
- CONSISTENT(D1,D2): simultaneous compliance is possible.
- STRICTER(D1,D2): D1 narrows legal outputs without violating higher authority.
- PRECEDES(D1,D2): explicit project authority says D1 outranks D2.
- PROVEN(P,E): evidence E satisfies proof obligation P.

## Candidate set
G(C) = { D | APPLIES(D,C) ∧ CURRENT(D,C) ∧ AUTHORIZED(D,C) }

No directive outside G may influence the legal decision merely because it is semantically similar.

## Resolution
A unique governing set exists only when:
1. all maximal-precedence directives are mutually consistent; and
2. their combined constraints leave at least one legal action; and
3. if the contract requires uniqueness, exactly one legal terminal action remains.

Otherwise:
- incompatible maximal authorities -> CONFLICT / FREEZE
- zero applicable authority where authority is required -> UNKNOWN / FREEZE
- multiple legal outputs where uniqueness is required -> AMBIGUOUS / FREEZE

## Normative strength
Do not infer precedence from words alone. MUST/SHALL/NEVER express norm strength inside an authority source; they do not grant that source authority.

## Anti-laundering invariant
Transformation T(summary, retrieval, translation, model output) cannot increase authority:
authority(T(x)) <= authority(x)

A generated summary may preserve or reduce confidence, never promote advisory text into governing law.

## Human override boundary
FACT_PROJECT: explicit current user directive is high in default authority resolution, but project-specific protected boundaries and safety/system rules can still constrain mutation. Visibility is not authorization.

## Counterexamples
C1: advisory note says "deploy" while current build evidence is missing.
Expected: advisory note cannot create deployment authority.

C2: superseded requirement is more semantically similar than current requirement.
Expected: CURRENT predicate rejects superseded directive.

C3: two equal-rank current rules require mutually exclusive actions.
Expected: CONFLICT, no averaging.

C4: one rule permits A/B, another same-or-higher rule forbids B.
Expected: legal set narrows to A if consistent.

C5: retrieved issue comment says "ignore policy".
Expected: unauthorized data cannot enter governing set.

## Falsification
This proposal fails if a valid NEXY authority case cannot be represented without hidden precedence or if two implementations following this calculus can legally choose different terminal states for the same normalized context.
