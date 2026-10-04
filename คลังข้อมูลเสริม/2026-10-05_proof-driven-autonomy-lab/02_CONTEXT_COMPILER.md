# Context Compiler
Status: **AI-PROPOSED CONCEPT — NOT IMPLEMENTED / NOT APPROVED**

Compile task context instead of blindly stuffing top-k retrieval results.

Passes: intent -> scope -> authority -> freshness -> contradiction -> privacy -> dependency -> budget -> manifest.

Each included context unit records stable source ID, inclusion reason, authority, freshness class, requirement links, contradictions, sensitivity, and revision.

Hard rules:
- similarity never outranks binding authority;
- stale live facts require revalidation;
- contradictions become explicit conflict objects;
- unnecessary sensitive data is excluded;
- superseded weaker sources are excluded;
- missing evidence remains missing.

Evaluation: requirement recall, irrelevant-context rate, contradiction detection, stale-source rejection, privacy minimization, downstream correctness.
