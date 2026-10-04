# Context Poisoning Defense

## Threat model
Poisoning can be accidental: stale docs, duplicated specs, hallucinated summaries, obsolete counts, ambiguous names, generated placeholders, copied AI claims, or a valid fact detached from its scope.

## Ingestion gate
For each imported artifact capture:
origin, authority, freshness, scope, transformation history, confidence/evidence class, and known conflicts.

## Quarantine triggers
- no provenance for a critical claim
- claims contradict stronger authority
- executable instructions embedded in untrusted data
- secrets/credentials
- generated content presented as source truth
- obsolete identifiers used as current truth
- mass duplication that can dominate retrieval

## Retrieval defense
Rank by authority × relevance × freshness × evidence completeness. Diversity matters: retrieve supporting and contradicting evidence when a decision is high-impact.

## Compression defense
A summary must preserve:
MUST/SHALL constraints, prohibitions, unresolved conflicts, unknowns, evidence references, identifiers, version/time scope, and stop conditions.
Compression that removes a blocker is corruption, not optimization.

## Canary questions
Periodically ask the context store:
- What is explicitly unknown?
- Which claims conflict?
- Which evidence is stale?
- Which files are deprecated?
- What must never be mutated?
If retrieval cannot answer these, the memory system is unsafe for autonomy.
