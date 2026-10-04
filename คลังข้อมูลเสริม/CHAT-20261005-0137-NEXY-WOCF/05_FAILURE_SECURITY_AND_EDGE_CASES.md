# Failure, Security, and Edge Cases

## Fail-closed conditions
- proposal missing required fields;
- unsupported status or invalid identifier;
- insufficient concept tags under policy;
- path traversal or absolute path;
- write path outside namespace when containment is enabled;
- malformed catalog element;
- policy threshold contradiction;
- protected repository match;
- hard ownership collision.

## Deliberate conservative choices
- Parent and child write paths collide even if a human suspects they refer to distinct file/directory intents.
- Exact concept fingerprint blocks automatically.
- High lexical overlap blocks instead of auto-allowing based on free-text differentiators.
- Catalog corruption blocks admission because partial comparison could miss a collision.

## Known false-positive/false-negative risks
Lexical Jaccard is intentionally simple. Synonyms can evade it; generic vocabulary can inflate overlap. Future extensions may add a separately evidenced semantic classifier, but such a classifier must never silently replace deterministic hard-collision checks.

## Security notes
- No `eval`, dynamic manifest code, subprocess execution from manifest data, or network request exists in the core engine.
- CLI file paths are operator-provided local inputs; contents are parsed as JSON only.
- Output hashes are integrity fingerprints, not signatures and not proof of authorship.
- Protected-repository substrings are configurable policy inputs; production policy ownership belongs above WOCF.

## Resource lifetime rule
Exclusive-resource collisions are enforced only against `ACTIVE` and `IN_PROGRESS` catalog entries. `COMPLETE`, `ARCHIVED`, and `REFERENCE` entries still participate in namespace/write/concept checks, but they do not indefinitely retain runtime-exclusive resources.
