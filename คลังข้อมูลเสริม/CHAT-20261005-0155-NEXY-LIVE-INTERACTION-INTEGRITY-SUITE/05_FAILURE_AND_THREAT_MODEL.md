# Failure & Threat Model

Classification: **AI_PROPOSED_CONCEPT / EXPERIMENTAL**.

| Failure / threat | Unsafe naive behavior | Suite control | Fail result |
|---|---|---|---|
| user supersedes directive while tool work continues | stale action commits after correction | epoch token + single-use action lease | FREEZE / reject stale lease |
| cancel arrives during work | worker continues from obsolete state | logical epoch advances on cancel | stale token invalid |
| cache entry belongs to different user/project | cross-context result leaks or is reused | namespace binds project + user scope | miss/freeze |
| policy/model/tool contract changes | stale result appears valid | contract hashes are cache-key material | cache miss |
| cache value is tampered | altered value returned as trusted hit | envelope value digest verification | FREEZE |
| text and voice adapters disagree on target | convenient modality changes action | exact critical-field intent comparison | FREEZE |
| modality omits external-access flag | default may silently expand authority | required modality/field contract | FREEZE |
| attachment referenced by directive is missing | model guesses around absent file | explicit input requirements | FREEZE |
| two resources share a required id | arbitrary file chosen | uniqueness requirement | FREEZE |
| extra attachment exists | unrelated/private data silently consumed | quarantine unreferenced resources | excluded |
| stream transport closes early | partial output released as FINAL | explicit tail final marker required | FREEZE |
| one chunk is lost or duplicated | corrupted artifact passes through | contiguous sequence check | FREEZE |
| chunks from another run are interleaved | mixed output assembled | one run_id + contract_hash invariant | FREEZE |
| final marker lies about content | truncated/modified bytes accepted | full assembled payload SHA-256 | FREEZE |
| caller treats hash as authenticity proof | malicious source may still produce a valid hash | explicit trust-boundary documentation | downstream auth/JUDGE still required |

## Non-goals
This suite does not prove model factual correctness, authenticate users, authorize side effects, solve prompt injection globally, provide distributed consensus, replace transaction orchestration, or prove NEXY deployment safety.
