# Invariant Mining
Extract properties that must remain true across implementations and refactors. Sources include MUST/MUST_NOT requirements, DB constraints, API contracts, routing rules, authorization boundaries, accounting identities, idempotency rules, incidents, impossible domain states, and compatibility promises.

Forms: state invariant P(state); transition invariant allowed(s1,s2); conservation invariant; uniqueness invariant; authority invariant preventing lower-authority overwrite; evidence invariant where COMPLETE implies required evidence exists.

Workflow: collect candidates, convert vague adjectives into predicates, seek counterexamples, separate hard invariants from SLOs, encode at the cheapest reliable layer, observe drift, and link each invariant to originating RIDs. "Should normally" is not an invariant.