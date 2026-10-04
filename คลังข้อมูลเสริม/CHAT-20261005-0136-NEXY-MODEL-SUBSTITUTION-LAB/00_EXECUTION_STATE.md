# NEXY Model Substitution Conformance Lab — Execution State

## Identity
- Mission ID: `NEXY-MSCL-20261005-0136`
- Conversation identifier: `CHAT-20261005-0136-NEXY-MODEL-SUBSTITUTION-LAB`
- Platform ChatGPT internal chat ID: `UNKNOWN_NOT_EXPOSED_TO_AGENT`
- Repository: `goif74945-crypto/AI-CONTEXT`
- Target folder: `คลังข้อมูลเสริม/CHAT-20261005-0136-NEXY-MODEL-SUBSTITUTION-LAB`
- Branch: `main`
- Status: `IN_PROGRESS`
- Classification: `AI_PROPOSED_CONCEPT / FUTURE_OPTION / NOT_CANONICAL_NEXY_REQUIREMENT`

## Objective
Design, implement, execute, verify, and preserve a standalone provider/model substitution conformance laboratory that can test whether hot-swapping external AI workers preserves NEXY-compatible semantic contracts without mutating any repository whose name contains `NEXY.AI`.

## Authority facts used
- NEXY treats external models as workers, not authority.
- Model hot-swapping should not alter the user's conceptual interface.
- Model degradation should be detectable and may reduce a model's role or trigger freeze.
- Provider output is untrusted until filtered/verified.
- Provider independence is a design requirement.
- Final release remains one legal verified output or FREEZE.

## Scope lock
### Authorized
- This mission folder only inside AI-CONTEXT.
- Read-only inspection of AI-CONTEXT project/rules/context.
- Local isolated execution of authored standard-library Python code/tests.
- Additive code, schemas, fixtures, docs, test evidence, and future ideas.

### Protected / forbidden
- Any mutation to a repository whose name contains `NEXY.AI`.
- Changes to canonical NEXY law/spec.
- Changes to sibling supplemental workstreams.
- Production deployment, credentials, secrets, external-provider calls.
- Claiming provider equivalence without executed evidence.

## Deduplication snapshot
Bounded repository checks found no indexed matches for:
- `model hot swap provider substitution conformance`
- `differential testing model provider`
- `metamorphic model behavior`
- `provider neutral contract`
- `model interchangeability`

Adjacent work exists for Oracle Forge, multi-agent adjudication, context/reuse/evidence/UX labs. This mission is specifically about semantic compatibility under model/provider substitution.

## Planned work DAG
- W01 authority + scope + dedupe — PASS
- W02 durable checkpoint/task contract — IN_PROGRESS
- W03 architecture + contracts + threat/failure model — PENDING
- W04 reference engine + CLI — PENDING
- W05 deterministic/unit/negative-path tests — PENDING
- W06 CLI/integration evidence — PENDING
- W07 generated compatibility matrix/example artifacts — PENDING
- W08 repository persistence + read-back verification — PENDING
- W09 final audit + resume record — PENDING

## Core invariants
1. Provider identity cannot alter authority.
2. Equivalent provider outputs are compared by canonical semantics, not wording.
3. Critical semantic disagreement cannot be averaged away.
4. FINAL without required evidence or authority is non-conformant.
5. A FREEZE-required case cannot be converted to FINAL by provider preference.
6. Same input bytes + tool version => byte-stable canonical report.
7. No network/model call is required by the reference engine.
8. Generated IDs/fingerprints are content-derived, never random.

## Resume rule
Re-read this file and the root Execution Kernel, refresh `main`, inspect this mission folder, then continue from the first non-PASS item. Never infer that unrecorded work succeeded.
