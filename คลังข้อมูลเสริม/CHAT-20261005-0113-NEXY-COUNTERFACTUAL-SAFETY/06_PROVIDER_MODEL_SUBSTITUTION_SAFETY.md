# Model / Provider Substitution Safety
Status: AI-PROPOSED CONCEPT — NOT CURRENT NEXY REQUIREMENT

SOURCE CONTEXT: NEXY direction treats external models as workers/generators, not final authority, and describes provider hot-swapping.

Similar APIs do not imply behavioral equivalence.

Capability fingerprint records only verified/configured facts: provider/model identity/version when available, modalities, context boundary, tool contract, structured-output behavior, refusal/failure semantics, latency/error envelope, determinism controls, data boundary and eval revision. Unknown fields remain UNKNOWN.

A→B substitution requires interface compatibility, policy compatibility, required capability coverage, task-specific eval, negative-path eval, output-normalization proof, preserved external authority and rollback route.

A semantic canary uses a bounded corpus and compares contract validity, unsupported claims, tool-call correctness, constraint adherence, freeze behavior and repeated-trial variance.

Provider success never grants authority. Worker output remains candidate material until the required verification/adjudication path accepts it.

"API-compatible" MUST NOT be promoted to "behavior-compatible" without evidence.
