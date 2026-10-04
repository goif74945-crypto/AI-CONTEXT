# Future Adoption and Integration Map

Status: **AI-PROPOSED FUTURE OPTION — NO CURRENT NEXY MODIFICATION**

## Possible boundary placement
A future implementation could emit a snapshot after explicit intent/context normalization, another after constraint/policy compilation, and another immediately before an execution transaction is authorized. Adjacent snapshots would be compared, with any unauthorized material delta causing the normal freeze path.

Conceptual sequence only:

`Directive -> Prompt/Input boundary -> CIRL -> [snapshot A] -> CLE/policy -> [snapshot B] -> execution contract -> [snapshot C] -> transaction preconditions -> execute`

## Candidate integration contracts
CIRL adapter: maps only already-resolved explicit fields; it may not invent target/scope.  
CLE adapter: preserves parent action/target and makes constraint changes explicit.  
API/transaction adapter: declares concrete side effects, mutation class, resource scope, and authority refs.  
OBS/audit adapter: persists transition result/digests, not raw secrets or hidden reasoning.

## Required work before adoption
1. Map snapshot fields to authoritative DOC-C/DOC-B terms instead of assuming this proposal's names.
2. Define production authority for `AuthorizedDelta`.
3. Bind grants to parent/child digests, actor/session, freshness/expiry, and replay law.
4. Decide whether semantic paths are field-level or typed domain capabilities.
5. Add integration tests using actual NEXY transformations and freeze handling.
6. Benchmark overhead and set data-retention/privacy rules.
7. Threat-model malicious but syntactically valid adapters.
8. Perform migration/versioning design before introducing snapshot schema into durable state.

## Explicit non-actions in this session
No NEXY code, workflow, branch, issue, setting, schema, database, or deployment was changed. No PR was opened. No proposal was promoted to canonical scope.
