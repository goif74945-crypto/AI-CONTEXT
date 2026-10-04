# NEXY Supplemental Collision Guard — Engineering Specification

Classification: `AI_PROPOSED_CONCEPT / SUPPLEMENTAL_TOOLING / NOT_CURRENT_NEXY_REQUIREMENT`
Work ID: `CHAT-20261005-0122-NEXY-SUPPLEMENTAL-COLLISION-GUARD`

## 1. Objective

Build a deterministic preflight mechanism for `AI-CONTEXT/คลังข้อมูลเสริม` that helps an agent or human detect when a proposed new supplemental project is likely to duplicate or strongly overlap an existing workstream.

The mechanism must reduce wasted parallel effort **without** becoming a semantic authority, automatically merging work, or modifying sibling projects.

## 2. Governing authority

For this project:

1. Explicit current user directive.
2. AI-CONTEXT execution and security rules.
3. Current repository state observed through the connected GitHub repository.
4. Current NEXY context as alignment evidence.
5. This AI-authored specification.

This specification cannot override canonical NEXY authority. Everything novel here remains an AI proposal until explicitly promoted by the user/project authority.

## 3. Inputs

### Scan input
- local filesystem root representing `AI-CONTEXT/คลังข้อมูลเสริม`;
- immediate child project directories;
- supported UTF-8-ish text artifacts below each project directory.

### Candidate input
- required human/agent supplied `title`;
- optional `summary`;
- optional explicit tags.

## 4. In scope

- deterministic project discovery;
- bounded text fingerprinting;
- lexical normalization;
- coarse explainable domain tags;
- candidate-to-project scoring;
- four-level risk classification;
- deterministic report ordering;
- JSON and Markdown report emission;
- machine-useful policy exit codes;
- symlink containment safeguards;
- tests and integrity evidence;
- future-concept design notes.

## 5. Protected / out of scope

- any mutation to a repository whose name contains `NEXY.AI`;
- mutation, deletion, rename, merge, or rewrite of existing supplemental projects;
- changing canonical NEXY requirements/status;
- claiming lexical similarity proves semantic identity;
- automatic deletion or consolidation;
- LLM/embedding/vector-service dependencies in v1;
- network access by the reference engine;
- secrets, private credentials, or deployment operations.

## 6. Design alternatives considered

### A. Static registry only
Maintain manually authored names/descriptions and reject exact names.

**Advantage:** trivial and predictable.  
**Failure:** misses renamed duplicates and becomes stale during concurrent creation.

### B. Deterministic lexical fingerprint guard — selected
Build bounded fingerprints from project name, relative text-file paths, and text content. Compare a candidate brief using containment and Jaccard metrics plus explainable tags.

**Advantage:** offline, standard-library, reproducible, auditable, cheap, easy to integrate before creation.  
**Failure:** lexical similarity cannot fully understand semantics.

### C. Embedding/LLM semantic judge
Use embeddings or a model to compare project intents.

**Advantage:** better paraphrase sensitivity.  
**Failure:** introduces external dependency, cost, model drift, prompt/context attack surface, weaker reproducibility, and an authority problem if a fuzzy model blocks work.

**Decision:** implement B. Keep C only as a future optional advisory layer whose output cannot independently authorize destructive or blocking actions.

## 7. Architecture

```text
Supplemental root
    |
    v
Immediate-project discovery
    |
    v
Bounded text collection
    |  - supported suffixes
    |  - max 80 files/project
    |  - max 32,000 bytes/file
    |  - skip generated/cache dirs
    |  - skip symlink files/directories
    v
Normalized terms + inferred tags + content SHA-256
    |
    +---------------------------+
                                |
Candidate title/summary/tags    |
    |                           |
    v                           v
Candidate terms/tags ----> pairwise scoring
                                |
                                v
              deterministic ranked matches
                                |
                                v
               risk classification + guidance
                                |
                   +------------+-------------+
                   |                          |
                   v                          v
              JSON/Markdown              CI exit gate
```

## 8. Fingerprint contract

Each project record contains:
- `name`;
- relative `path`;
- normalized term set;
- inferred tag set;
- SHA-256 over deterministic collected text;
- `files_read`;
- `bytes_read`.

Relative paths are included in collected text so moving equal text between differently named files can change the fingerprint. Generated/cache directories are excluded so output produced by the guard cannot recursively alter the project fingerprint it is intended to describe.

## 9. Scoring contract

For candidate `C` and project `P`:

```text
term_jaccard = |C_terms ∩ P_terms| / |C_terms ∪ P_terms|
candidate_containment = |C_terms ∩ P_terms| / |C_terms|
tag_jaccard = |C_tags ∩ P_tags| / |C_tags ∪ P_tags|

score = 0.60 * candidate_containment
      + 0.25 * term_jaccard
      + 0.15 * tag_jaccard
```

Score is clamped to `<= 1.0` and rounded to six decimal places.

Classification:
- `LIKELY_DUPLICATE`: score `>= 0.93`;
- `HIGH_OVERLAP`: score `>= 0.62` and `< 0.93`;
- `RELATED`: score `>= 0.38` and `< 0.62`;
- `DISTINCT`: score `< 0.38`.

### Why containment dominates

A candidate brief is normally much shorter than an established project. A pure Jaccard score penalizes a rich existing project for having additional vocabulary. Candidate containment therefore carries the largest weight. The `LIKELY_DUPLICATE` threshold is intentionally high so partial vocabulary coverage is not mislabeled as identity.

## 10. Immutable behavior rules

1. Same filesystem snapshot + same candidate must produce the same ordering and score values.
2. A blank title must fail.
3. A candidate with no discriminating terms after normalization must fail.
4. A missing/non-directory supplemental root must fail.
5. Symlinked project directories must not be scanned.
6. Symlinked files must not be read.
7. Generated/cache directories must not affect fingerprints.
8. The engine must not mutate scanned projects.
9. Classification must expose shared terms/tags for explanation.
10. A lexical `DISTINCT` result is permission only to continue manual review, not proof of global uniqueness.
11. A lexical `LIKELY_DUPLICATE` result is a preflight warning/gate, not authority to delete or merge anything.
12. No output may claim NEXY.AI runtime integration unless separate integration evidence exists.

## 11. CLI contract

### `scan`
Build a stable JSON catalog of immediate project directories.

### `check`
Compare one candidate against the discovered catalog.

Optional outputs:
- JSON file;
- Markdown report;
- stdout JSON if no output file is requested.

### Policy gate
`--fail-at RELATED|HIGH_OVERLAP|LIKELY_DUPLICATE`

If resulting classification meets or exceeds the configured risk, exit `2`. Successful non-blocked execution exits `0`. Argument/input validation also uses argparse-style exit `2`.

## 12. Failure semantics

Fail closed on:
- invalid root;
- blank candidate title;
- candidate with no discriminating vocabulary.

Skip rather than follow:
- symlinked project directory;
- symlinked content file.

Ignore unreadable/undecodable individual files rather than failing the whole root scan. The report retains only terms/hashes/metadata, not raw file contents.

## 13. Security and privacy model

Threats addressed:
- path escape through symlinks;
- accidental scan of generated self-output;
- unbounded file ingestion;
- implicit network/model disclosure.

Controls:
- skip symlinks;
- bounded file count and byte count;
- standard library only;
- no network path in implementation;
- read-only scan/check behavior except explicit result output paths;
- output contains normalized terms and metadata, not raw source contents.

Security claim boundary: these controls are verified only at unit/static level for this reference implementation. They are not proof of production sandboxing or universal data-leak freedom.

## 14. Determinism model

Determinism applies to:
- file candidate sort order;
- project order;
- normalized set-to-list serialization;
- rank tie-breaks by case-folded project/path;
- score rounding;
- catalog serialization when `sort_keys=True` is used by the CLI.

Filesystem content is an explicit input. A changed snapshot is allowed to produce changed output.

## 15. Edge cases

- empty supplemental root → valid scan with zero records;
- no existing projects during candidate check → `DISTINCT` if candidate is valid;
- identical candidate/project vocabulary → high enough for `LIKELY_DUPLICATE` under test fixture;
- rich project with partial overlap → may be `HIGH_OVERLAP` or `RELATED` rather than duplicate;
- Thai continuous text is tokenized coarsely as contiguous Thai runs; v1 does not claim Thai word segmentation;
- files larger than 32,000 bytes contribute only their first bounded segment;
- more than 80 eligible files contribute only the first 80 after deterministic sorting.

## 16. Acceptance criteria

- Python compilation succeeds. `E1`
- JSON schemas parse. `E1`
- Unit/negative/security-boundary suite executes and passes. `E2`
- Test suite proves direct-file invocation loads the complete current suite. `E2`
- Repeated CLI run on the same fixture emits identical JSON bytes. `E2`
- Exact duplicate fixture reaches `LIKELY_DUPLICATE`. `E2`
- Near-duplicate fixture reaches `HIGH_OVERLAP`. `E2`
- Orthogonal fixture reaches `DISTINCT`. `E2`
- `--fail-at HIGH_OVERLAP` returns exit `2` for a high-overlap fixture and `0` for a distinct fixture. `E2`
- Symlink escape fixtures do not contribute external terms. `E2`
- Intended project files are persisted under the authorized AI-CONTEXT directory and read back. `E0`
- No mutation occurs in any repository whose name contains `NEXY.AI`.

## 17. Stop / freeze conditions

Freeze affected work if:
- persistence would require writing outside the authorized AI-CONTEXT directory;
- the target path already exists with unrelated content;
- main branch precondition cannot be updated safely without destructive force;
- a sibling project is discovered that already owns the same responsibility;
- final verification fails;
- persistence would expose a secret.

## 18. Known limitations

This v1 is intentionally lexical. It can miss semantically equivalent work phrased with unrelated vocabulary and can over-score projects sharing domain language. It is a **coordination guard**, not a formal uniqueness oracle. Future semantic assistance must preserve this limitation instead of hiding it behind model confidence.
