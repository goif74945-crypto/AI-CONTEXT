# Forensic Evidence — Wave 1 Canonical Runtime

Evidence ID: EVD-NEXY-W1-FORENSIC-003
Audit Round: ROUND-1
Status: NOT_VERIFIED / BLOCKED
Repository: goif74945-crypto/AI-CONTEXT
Branch under audit: nexy-skill-runtime-canonical-v2
HEAD under audit: ba729b9e9e1b917c942ec19a8f204a10e5b9fe0f
Current main: 3a162ef2eb342ad387d5a7579fbf8c4342380c62
Compare status: diverged
Ahead/behind vs main: +20 / -8
Merge base: fb94c6e1295813564c9574573ea224ffb94e4e93

## Scope

Target Skills (7):
GOV-001, GOV-002, CTX-001, CTX-003, REQ-001, ARC-001, ARC-004

Relevant implementation files:
- skills/nexy/runtime/runtime.py
- skills/nexy/runtime/tests/test_runtime.py
- skills/nexy/runtime/audit.py
- skills/nexy/runtime/completion_proof_v2.py
- skills/nexy/runtime/runtime-contract.json
- skills/nexy/runtime/README.md
- skills/registry/registry.json
- skills/registry/RUNTIME-CONTRACT.md
- 7 target SKILL.md files

## FACT

1. GitHub branch nexy-skill-runtime-canonical-v2 exists and points to ba729b9e9e1b917c942ec19a8f204a10e5b9fe0f.
2. Current main is 3a162ef2eb342ad387d5a7579fbf8c4342380c62; no main modification was made in this audit.
3. GitHub compare reports the branch is diverged from main (+20/-8), with merge base fb94c6e1295813564c9574573ea224ffb94e4e93.
4. The branch contains exactly 7 NEXY target SKILL.md files for the scoped Wave 1 set.
5. The branch contains an executable Python runtime implementation and 21 executable unit tests.
6. GitHub Actions run 35336975250 for HEAD ba729b9e9e1b917c942ec19a8f204a10e5b9fe0f completed with conclusion success.
7. The CI job ran 21 unit tests and reported OK. The structural audit reported PASS. The deterministic completion proof also printed status PASS.
8. The completion proof's success was based on a registry state that itself marked all 7 targets VERIFIED.
9. The current source of truth Master Specification explicitly states that a concrete Skill runtime/loader implementation is not specified and must not be invented.
10. skills/registry/RUNTIME-CONTRACT.md states that the Registry routes and identifies Skills and that an execution backend is required; it does not provide an authoritative backend implementation.
11. The current runtime implementation does not load the target SKILL.md files as execution source for their behavior. Instead, its target execute_* functions consume behavior facts supplied in the caller envelope:
    - GOV-001 consumes data.sources;
    - GOV-002 consumes data.request;
    - CTX-001 consumes context fields already supplied by the caller;
    - CTX-003 consumes data.files and only checks a supplied content hash when content is also supplied;
    - REQ-001 consumes data.requirement;
    - ARC-001 consumes data.architecture;
    - ARC-004 consumes data.impact.
12. Because those inputs are supplied by the caller, passing the current tests demonstrates that the Python functions can process the supplied envelope. It does not demonstrate actual repository/source inspection behavior required by CTX-003, current-context loading required by CTX-001, or architecture inspection required by ARC-001/ARC-004.
13. The branch registry currently records the 7 targets as VERIFIED, with verification metadata pointing to earlier CI evidence. Current forensic evidence shows that this verification is not sufficient to establish canonical runtime behavior.
14. The source repository tree includes projects/NEXY.AI paths as project data inside AI-CONTEXT. No repository outside AI-CONTEXT was modified.

## ROOT CAUSE

Confirmed root cause:
The authoritative Skill specification does not define a concrete Skill runtime/loader/execution mechanism, while the branch implementation introduced a Python runtime and treated that implementation as canonical. The implementation therefore substitutes an invented execution mechanism for the unresolved authoritative runtime contract.

Contributing factor:
The completion proof and registry allowed a green CI result to become VERIFIED without a gate proving canonical runtime provenance and real source-driven execution.

## COUNTER-EVIDENCE

- CI PASS is real but insufficient for canonical verification.
- Registry VERIFIED state conflicts with the requirement that VERIFIED requires behavioral, security, integration, regression, evidence and completion proof.
- The runtime source demonstrates envelope-driven execution rather than actual source inspection.
- The Master Specification explicitly forbids inventing unspecified runtime mechanisms.

## REQUIRED STOP CONDITION

Further implementation of a canonical runtime would require choosing a runtime/loader/execution mechanism that the authoritative specification leaves unspecified. That is an architecture/mechanism invention.

Therefore:
STATUS = BLOCKED / FREEZE
Wave 1 target Skills = 0 VERIFIED
Wave 1 target Skills = 7 MATERIALIZED / NOT VERIFIED

## HASH / INTEGRITY

Primary source SHA-256:
NEXY สกิว.pdf = a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c

Repository file hashes available from GitHub content API are Git blob SHAs, not SHA-256. They are recorded as repository-integrity identifiers, not represented as SHA-256.

runtime.py Git blob SHA: 96c86818867db4ebb0e2cc51aec59171698226a8
test_runtime.py Git blob SHA: 79f763535f313b729d40b0656872b3a7b9e7e78c
audit.py Git blob SHA: 7ef2986cea26c98835b87d96bfa7992a55c8cb1f
completion_proof_v2.py Git blob SHA: ee9aa6f89dfce3904ec648ed7f73ee69dd4fb731
runtime-contract.json Git blob SHA: 88ee160eb7ab6c153772ee9285b9ad4c8aadf87d
README.md Git blob SHA: 1958f9fd89e00c67f82b4e88575cd16d8a5442d6

## LIMITATION

Local filesystem/worktree state outside GitHub is not observable through the connected GitHub API in this audit. GitHub branch, commit, file, compare and workflow state are directly verified.

## DECISION

Do not claim COMPLETE, PASS, or VERIFIED for the 7 target Skills.
Do not merge or update main.
Do not invent a new runtime architecture in this round.
