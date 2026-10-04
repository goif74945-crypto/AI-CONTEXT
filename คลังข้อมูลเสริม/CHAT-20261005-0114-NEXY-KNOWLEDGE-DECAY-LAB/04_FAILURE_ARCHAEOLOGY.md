# Failure Archaeology
**AI-PROPOSED CONCEPT — NOT AUTHORITATIVE — NOT IMPLEMENTED — NOT VERIFIED**

## Thesis
A failure log says what broke. Failure archaeology preserves why the system was vulnerable, what earlier signals existed, what repair actually changed, and whether the same structural defect can reappear under a new symptom.

## Proposed Failure Fossil
Fields: fossil_id; symptom; first_observed; target identity; triggering condition; violated invariant; root cause status (VERIFIED|INFERRED|UNKNOWN); causal ancestors; misleading signals; attempted fixes/outcomes; final verified repair; regression evidence; recurrence signature; blast radius; recovery cost; prevention control; confidence boundaries.

## Failure families
stale-evidence promotion; authority inversion; identity mismatch; partial-success masking; hidden fallback; nondeterministic ordering; schema drift; concurrency race; provider semantic drift; environment divergence; verification substitution; incomplete denominator; rollback illusion; observability blind spot.

## Counterfactual retrieval
Before mutation ask: “If this change were wrong, which historical failure family would it resemble?” This is a heuristic, never proof.

## Near misses
Preserve prevented failures separately. A near miss is not a runtime failure but can create prevention obligations.

## Metrics
recurrence by family; time to verified root cause; repairs with regression evidence; incidents caused by stale assumptions; prevention-control escape rate; UNKNOWN root-cause backlog age.

## Integrity rule
If root cause is unverified, preserve UNKNOWN. Never rewrite inference as history. Competing causal models may coexist until discriminating evidence exists.

## Future payoff
A multi-year fossil corpus can prevent structurally identical mistakes even when technologies and error messages change.
