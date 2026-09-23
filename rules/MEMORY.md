# MEMORY LAW

## 1. Memory classes

Every persisted context item belongs to one class:

- **CANON** — current authoritative law/spec/decision.
- **PROJECT_STATE** — current verified project/repository state.
- **DECISION** — explicit choice with rationale and authority.
- **EVIDENCE** — proof artifact/reference and what it proves.
- **FAILURE_PATTERN** — reproducible failure/root-cause pattern.
- **WORKFLOW** — reusable procedure.
- **PREFERENCE** — non-sensitive user/project preference that materially affects work.
- **HISTORY** — superseded but useful provenance.
- **EXPERIMENTAL** — unverified hypothesis/proposal.
- **DEPRECATED** — retained only for lineage.

Do not store transient conversation as if it were durable truth.

## 2. Write criteria
Persist only if the information is:
- likely to matter in future work;
- specific enough to act on;
- sourceable/provenance-aware;
- not a secret;
- not redundant with an existing authoritative record.

## 3. Provenance
A durable record should include, where applicable:
- source path or source class;
- commit/version;
- timestamp/date;
- author/actor if relevant;
- evidence reference;
- status.

## 4. Conflict handling
When new information conflicts with existing memory:
1. do not overwrite immediately;
2. identify both authorities;
3. classify the conflict;
4. resolve by authority/evidence if possible;
5. preserve superseded history;
6. mark unresolved cases CONFLICT.

## 5. Promotion
EXPERIMENTAL → CANON/PROJECT_STATE only after the required verification/approval path.

Repeated assertion is not verification.

## 6. Deprecation
When a record is superseded:
- preserve lineage;
- mark deprecated/superseded;
- point to replacement;
- do not silently rewrite history.

## 7. Context compression
Prefer structured compression:
- invariant;
- dependency;
- decision;
- reason;
- evidence;
- failure behavior.

Do not compress away:
- authority;
- exceptions;
- unresolved conflict;
- evidence status.

## 8. Long-source capture
For sources larger than a comfortable model context:
`READ → ANALYZE → WRITE CHECKPOINT → CONTINUE`

Maintain a coverage map so another AI knows what has and has not been processed.

## 9. User/private data
Do not persist sensitive personal data unless the user explicitly requires it for the project and the storage location is appropriate.
Never persist credentials/secrets.

## 10. Memory is not execution truth
Context may be stale.
Before mutation or current-state claims, refresh the real target when freshness matters.
