# TASK CONTRACT — NEXY Preference Sovereignty Lab

contract_revision: 1
mission_id: NPSF-20261005-0122
chat_code: CHAT-20261005-0122-NEXY-PREFERENCE-SOVEREIGNTY-LAB
status: LOCKED_FOR_EXECUTION
proposal_class: AI_PROPOSED_CONCEPT
canonical_nexy_status: NON_GOVERNING_RESEARCH

## OBJECTIVE
Design, implement and verify an isolated reference system that can store and resolve user preferences without allowing unconfirmed inference, stale preference state, hidden profiling, or personalization to override NEXY authority, safety, evidence, permissions, release, or truth rules.

## REQUIRED OUTPUT
A self-contained supplemental project under:
`คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-PREFERENCE-SOVEREIGNTY-LAB/`

It must include architecture, contracts, reference code, tests, adversarial fixtures, validation evidence, proposal/adoption boundaries, and resumable execution state.

## INPUTS / AUTHORITY
1. Explicit current user directive.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/AI-BEHAVIOR.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
4. NEXY source-derived context under `projects/NEXY.AI/`, interpreted by its stated authority hierarchy.
5. Current observed supplemental tree for collision avoidance.
6. This task contract for lab-local implementation choices.

## IN SCOPE
- preference provenance and consent state
- allowlisted preference definitions
- scope and deterministic precedence
- candidate vs active preference separation
- expiry/revocation/supersession/conflict handling
- data minimization
- deterministic replay/snapshot hashing
- explanations of why a preference did or did not apply
- fail-closed behavior
- isolated reference implementation and tests
- future integration proposal explicitly marked non-governing

## OUT OF SCOPE / PROTECTED
- any mutation to any repository whose name contains `NEXY.AI`
- modification of the current 837-row build matrix
- alteration of NEXY law, release thresholds, RBAC, safety or verification policy
- deployment
- production user profiling
- secret/credential/PII persistence
- claiming NEXY currently implements this lab
- editing existing sibling chat folders
- background/asynchronous execution claims

## IMMUTABLE REQUIREMENTS
NPSF-R01: Inference may create a candidate but may never silently become ACTIVE.
NPSF-R02: Only allowlisted preference keys may be stored/resolved by the reference engine.
NPSF-R03: Preference application must never override protected authority/security/evidence/release domains.
NPSF-R04: Every preference record must carry provenance, scope, lifecycle state and source identity.
NPSF-R05: Resolution must be deterministic for the same records, registry and explicit `now`.
NPSF-R06: Expired and revoked records must never apply.
NPSF-R07: Same-precedence contradictory ACTIVE records must fail closed rather than pick arbitrarily.
NPSF-R08: More specific valid scope may override a less specific valid scope only by an explicit deterministic order.
NPSF-R09: Sensitive/unregistered arbitrary profiling keys must be rejected.
NPSF-R10: High-impact preference definitions, when enabled experimentally, require explicit provenance, bounded expiry and a consent receipt.
NPSF-R11: Snapshot/effective-state output must be canonically serializable and hashable.
NPSF-R12: Mutation operations must be auditable and reversible through revocation/supersession semantics.
NPSF-R13: Hidden wall-clock/randomness/network/filesystem state must not influence core resolution.
NPSF-R14: Validation evidence must distinguish E0/E1/E2 from unperformed E3-E7.
NPSF-R15: Every AI-originated architectural extension must be labeled AI_PROPOSED_CONCEPT/HYPOTHESIS, not canonical law.

## ACCEPTANCE CRITERIA
- All R01-R15 map to implementation/docs/tests/evidence.
- Reference package compiles.
- Executed unit/property/adversarial test suite passes.
- Determinism and insertion-order invariance are tested.
- Negative paths are tested: inferred candidate, bad key/value, expiry, revocation, conflict, protected/high-impact rules.
- All committed files are re-read or enumerated after write.
- Tests are re-executed from final committed source contents or exact verified byte-equivalent local copies.
- No protected repository/path is mutated.
- Final audit reports every limitation and does not claim NEXY integration/runtime proof.

## EVIDENCE TARGET
- E0 for repository presence.
- E1 for syntax/static/JSON structural checks.
- E2 for isolated behavior.
- E3/E4/E5/E6/E7 remain NOT_VERIFIED / NOT_CLAIMED.

## RISKS
- Concept collision with concurrent supplemental chats.
- Accidental promotion of inferred preferences into authority.
- Hidden nondeterminism from current time or random IDs.
- Preference scope ambiguity.
- Overcollection of personal data.
- Stale evidence if source changes after tests.
- Concurrent main-branch movement by other chats.

## MITIGATIONS
- unique additive folder
- explicit proposal labels
- caller-supplied `now`
- deterministic content-derived IDs/snapshot hashes
- allowlist registry
- scope lattice
- fail-closed conflict status
- final committed-content read-back and local re-verification
- no shared-file update unless strictly necessary

## STOP / FREEZE CONDITIONS
- required action would mutate a NEXY.AI-named repository
- authority conflict changes an immutable requirement
- target identity becomes uncertain
- secret/sensitive user data would need to be persisted
- execution proof cannot be tied to the final reference source
- a destructive Git action becomes necessary
- completion would require inventing an unverified NEXY behavior

## DELIVERABLE STATUS RULE
Only report COMPLETE when every acceptance criterion has matching evidence. Otherwise report INCOMPLETE / BLOCKED / NOT VERIFIED as applicable.
