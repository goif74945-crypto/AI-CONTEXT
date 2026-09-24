# NEXY.AI Error Taxonomy

Canonical file:
- `error-taxonomy.jsonl`

Distinguishes:
- wire-canonical errors exposed through SystemEnvelope;
- broader internal VNext failure codes.

Fields map:
ERROR → severity → response → user surface → incident policy → recovery.

Important: internal codes are not automatically valid wire errors. Translation must be explicit.
