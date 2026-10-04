# Conflict Resolution Engine

## Problem
Multi-source AI systems inevitably ingest incompatible statements. Silently choosing one creates invisible corruption.

## Conflict classes
- TEMPORAL: both claims may be true at different times.
- SCOPE: claims apply to different environments, branches, tenants, regions, versions, or users.
- IDENTITY: same label refers to different entities.
- DEFINITION: metrics or terms use different definitions.
- AUTHORITY: sources disagree and one has stronger governing authority.
- MEASUREMENT: observations disagree under nominally same conditions.
- EXTRACTION: one claim likely resulted from parsing or transcription error.
- INFERENCE: evidence is shared but conclusions differ.

## Resolution pipeline
1. Normalize entity identity without deleting original text.
2. Normalize units, timestamps, versions, and scope.
3. Split compound claims into atomic propositions.
4. Test whether conflict disappears after temporal/scope separation.
5. Rank governing authority for the exact question.
6. Prefer direct current observation for runtime-state questions.
7. Require independent verification when impact is high.
8. If unresolved, preserve both claims and return CONFLICTED/UNKNOWN rather than inventing consensus.

## Forbidden behavior
- majority vote across copied sources
- confidence averaging across dependent sources
- treating recency as universal superiority
- overwriting old evidence without lineage
- selecting the answer that best matches prior model output

## Dependency detection
Ten websites repeating the same press release are one evidence lineage, not ten independent confirmations. Store provenance parents where possible.

## Resolution record
Every resolution SHOULD record conflict_id, participating claim IDs, rule applied, decisive evidence, resolver, timestamp, result, and residual uncertainty.

## Stop condition
If a conflict affects a critical action and cannot be resolved with available evidence, block mutation and surface the unresolved conflict.