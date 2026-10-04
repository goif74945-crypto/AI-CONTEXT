# NEXY Intent Integrity & Least-Authority Delegation Lab (IIL)

**Status:** AI-PROPOSED / ADVISORY ONLY / STANDALONE PROTOTYPE  
**Session code:** `NEXY-IIL-20261005-0121-TH`  
**Platform chat ID:** `UNKNOWN` (not exposed by available tools)  
**Storage target:** `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/NEXY-INTENT-INTEGRITY-LAB-20261005-0121`  
**Protected evidence source:** `goif74945-crypto/NEXY.AI-` (READ-ONLY in this work)

This project explores two connected control surfaces: (1) an explicit, deterministic **Intent Contract** that can be sealed, validated, and compared across revisions; and (2) a **Least-Authority Delegation Capsule** that attenuates an admitted parent contract into a sealed child-agent handoff without privilege amplification.

It is **not** a NEXY.AI requirement, implementation, integration, release artifact, or deployment. Any future adoption requires a separate authorized task and authoritative promotion.

## Why this exists

Observed NEXY orientation describes bounded intent resolution, rejection of ambiguous intent rather than guessing, and separation of presentation-only dialog from task handoff. This lab asks a narrower question:

> How can an execution agent prove that the task it is about to perform still matches the user's explicit objective, scope, constraints, and authority after planning, handoff, or revision?

The prototype answers with a machine-inspectable contract and three statuses:

- `ADMIT` — no detected contract blocker.
- `REVIEW` — noncritical uncertainty or a tightening/additive revision exists and deserves explicit review.
- `FREEZE` — critical ambiguity, contradiction, protected-scope collision, tampering, unsafe drift, or invalid lineage exists.

## Contract surface

A v1.1 manifest requires explicit sections for:

`OBJECTIVE`, `INPUT`, `CONSTRAINT`, `REQUIRED_OUTPUT`, `IN_SCOPE`, `OUT_OF_SCOPE`, `IMMUTABLE`, `REQUIRED_BEHAVIOR`, `FORBIDDEN`, `EDGE_CASE`, `FAILURE_CONDITION`, `VALIDATION`, `ACCEPTANCE`, `AUTHORITY`, and `STOP_CONDITION`.

Optional sections are `PROTECTED_SCOPE`, `EVIDENCE`, `ASSUMPTION`, `UNKNOWN`, `CONFLICT`, and `PARENT_SEAL`.

Missing required sections are rejected rather than filled with defaults.

## Deterministic integrity model

1. Parse the explicit manifest with hard resource bounds.
2. Normalize line endings and set-like fields.
3. Preserve authority ordering as semantically significant.
4. Canonically serialize the normalized contract.
5. Seal it with SHA-256.
6. Validate critical unknowns, conflicts, scope collisions, lineage, and seal integrity.
7. Compare revisions to detect scope or authority drift.

No model call, clock, randomness, network request, database, or mutable global state is used by the engine.

## CLI

```bash
npm run cli -- compile examples/valid.iil /tmp/contract.json
npm run cli -- verify /tmp/contract.json
npm run cli -- diff baseline.json candidate.json
```

Exit codes:

- `0`: ADMIT
- `2`: REVIEW
- `3`: FREEZE / unsafe drift
- `64`: CLI usage error
- `65`: malformed/unparseable data

## Verification

Run:

```bash
npm run verify
```

Current verified local result for the artifact produced by this session: strict TypeScript typecheck PASS; 45 automated tests PASS; 0 FAIL. The suite includes deterministic child-delegation, privilege-escalation, guardrail-removal, CLI, parser-bound, tamper, and drift tests. Exact evidence is recorded under `evidence/`.

## Least-authority delegation

A parent contract with `ADMIT` status can be projected into a child capsule. Child inputs and required outputs must be subsets, child scope must remain inside parent scope, all restrictive guardrails are inherited, and only tighter constraints/forbidden/stop conditions may be added. The capsule is independently sealed and re-verifiable against the exact parent contract seal.

The subsystem exists specifically to prevent multi-agent delegation from becoming accidental authority expansion. See `docs/10_LEAST_AUTHORITY_DELEGATION.md`.

## Important limitations

- It processes an explicit manifest, not arbitrary natural language. Natural-language-to-contract translation remains outside this prototype because silently guessing intent would defeat the design goal.
- SHA-256 seals detect mutation but do not prove signer identity. Cryptographic signatures are future work.
- Path overlap logic is intentionally conservative and lexical; it is not a filesystem resolver.
- Revision diff rules are policy proposals, not canonical NEXY law.
- `REVIEW` is not release authorization.
