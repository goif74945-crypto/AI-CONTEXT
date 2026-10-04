# Research Backlog

All entries are **AI_PROPOSED_CONCEPTS**, not current NEXY requirements.

| ID | Research item | Why it matters | Promotion blocker |
|---|---|---|---|
| R-01 | Unicode canonicalization profile | Hash equality can differ across equivalent Unicode forms | cross-language vectors |
| R-02 | Scope grammar v2 | `namespace:*` may be too coarse for nested resources | formal grammar + ambiguity proof |
| R-03 | Consent expiry semantics | Hash binding alone does not model time validity | approved time authority model |
| R-04 | Authenticated authority provenance | Role/state fields must not be caller-forgeable | integration architecture |
| R-05 | Contract evolution/versioning | Hash behavior must survive schema upgrades safely | migration law |
| R-06 | Outcome graph instead of flat IDs | Multi-step tasks need dependency-aware objective mapping | deterministic graph semantics |
| R-07 | Question information-gain model | One question should maximize blocker resolution without guessing | deterministic, auditable scoring |
| R-08 | Accessibility study | Minimal surfaces can still exclude users | E4/usability evidence |
| R-09 | Localization/freeze wording | Direct deterministic copy must remain clear across languages | approved localization contract |
| R-10 | Mobile dangerous-control study | Owner drawer can hide complexity but not state | interaction tests |
| R-11 | Trace privacy minimization | Integrity telemetry must not become unnecessary profiling | privacy schema |
| R-12 | Large-contract resource bounds | Malformed/huge inputs can create evaluation DoS | benchmarks and hard limits |
| R-13 | Differential implementation tests | Multiple language implementations should produce same decision/hash | shared conformance vectors |
| R-14 | Model-assisted contract drafting sandbox | AI can suggest fields but must not authorize its own guesses | authority separation proof |
| R-15 | Ambiguity taxonomy | Distinguish material blockers from harmless presentation choices | source-grounded classification |
| R-16 | Interruption budget ownership | Who may set/override the budget under critical tasks? | policy authority |
| R-17 | External-I/O subscopes | Boolean permission may be too broad | provider/data/action lattice |
| R-18 | Consent explanation UX | Explicit consent should explain exact consequence without dark patterns | user-study evidence |
| R-19 | Acceptance evidence resolver | Evidence refs need exact revision/environment validation | evidence graph integration |
| R-20 | Recovery-action disclosure | Owner recovery controls must remain clear without encouraging unsafe retry loops | incident UX tests |
| R-21 | Control discoverability vs least authority | Hiding forbidden controls may reduce understanding of role boundaries | comparative study |
| R-22 | Objective-drift fuzzing | Explicit tags can still be incorrectly assigned upstream | adversarial generator |
| R-23 | Contract diff surface | Operators should see what changed before re-consenting | deterministic diff spec |
| R-24 | Multi-actor handoff | Intent/consent ownership across OWNER/OPERATOR transitions | lineage contract |
| R-25 | Evidence-aware completion copy | UI wording should distinguish done, blocked, and not verified | copy conformance suite |
