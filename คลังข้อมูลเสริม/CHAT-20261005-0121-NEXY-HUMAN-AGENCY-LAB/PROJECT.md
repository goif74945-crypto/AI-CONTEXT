# NEXY Human Agency Lab — Durable Project Record

---

## SOURCE: README.md

# NEXY Human Agency Lab

**Classification: AI-PROPOSED CONCEPT + STANDALONE PROTOTYPE. NOT CANONICAL NEXY LAW. NOT INTEGRATED INTO NEXY.AI.**

Chat / mission code: `CHAT-20261005-0121-NEXY-HUMAN-AGENCY-LAB`

## Objective

Operationalize a missing human-facing control layer between "execute autonomously" and "freeze everything": a deterministic mechanism that protects human authority while minimizing needless interruption.

The prototype answers four questions for any proposed action:

1. Can the AI proceed without interrupting the user?
2. Should it show a preview first?
3. Must it explicitly ask for confirmation?
4. Must it freeze because authority/recovery/evidence conditions are insufficient?

## Why this is useful to NEXY

NEXY's current context says human authority must be preserved, ambiguity must not be guessed through, complexity should stay behind a small UI surface, and the product should expose useful results rather than hidden machinery. Those principles create a practical UX tension: excessive confirmation destroys usability, but excessive autonomy destroys control.

This lab turns that tension into deterministic, testable policy.

## Prototype components

- `human_agency_lab.py` — consolidated standard-library implementation.
- `test_human_agency_lab.py` — 34 unit/regression/invariant tests.
- `fixtures/scenarios.json` — 11 executable reference scenarios.
- `00_MISSION_STATE.md` — initial durable mission checkpoint.
- `PUBLICATION_MANIFEST.sha256` — local staging SHA-256 provenance.
- `FINAL_STATE.md` — post-publication read-back status when available.

## Non-goals / protected boundary

- Does not modify `goif74945-crypto/NEXY.AI-` or any repository whose name contains `NEXY.AI`.
- Does not claim to be part of DOC-B, DOC-C, DOC-D or DOC-E.
- Does not claim current NEXY runtime support.
- Does not replace NEXY::LAW, NEXY::JUDGE, NEXY::GUARD or deployment evidence.
- Does not store secrets or private user data.

---

## CONSOLIDATED SPECIFICATION

**Status: AI-PROPOSED / NON-CANONICAL / STANDALONE RESEARCH PROTOTYPE.**

### Problem

A control system that asks for confirmation on every action is technically cautious but operationally miserable. A system that rarely asks can be fast while quietly eroding user authority. The useful target is not maximum autonomy or maximum confirmation. It is **minimum interruption subject to hard authority, reversibility and risk constraints**.

### Proposed principles

1. **Human authority is a hard boundary.** High-impact actions without explicit authority freeze.
2. **Irreversible destructive action without rollback freezes.** No attention optimization may weaken this.
3. **Hard gates beat UX optimization.** A depleted attention budget cannot downgrade required confirmation.
4. **Preview is a first-class state.** It handles uncertainty that deserves visibility but not a blocking confirmation ceremony.
5. **Low-risk reversible work should flow.** Safe, scoped work should not become paperwork.
6. **Recovery is part of action design.** External or broad actions need checkpoints; destructive actions need rollback.
7. **Decision logic is deterministic and auditable.** Identical normalized input and policy generate identical structural output and digest.
8. **Reasons are machine-readable.** The UI can remain small while evidence remains inspectable.
9. **User attention is a scarce resource, not an excuse to bypass control.** Soft previews may be optimized; hard gates may not.
10. **Integration is opt-in.** This prototype has no authority over NEXY until promoted by an authoritative specification.

### Architecture

```text
Normalized Proposed Action
        |
        v
RequestProfile validation
        |
        v
AgencyDecisionEngine
  | hard authority / rollback gates
  | mandatory confirmation gates
  | soft preview gates
  v
InteractionDecision
(PROCEED / PREVIEW / CONFIRM / FREEZE)
        |
        +--> Recovery planner
        |
        +--> Attention budget (soft gates only)
        |
        +--> Human-readable summary
        |
        +--> Metrics / simulator / audit digest
```

### Determinism boundary

The engine contains no network access, clock reads, randomness, hidden model call, locale-dependent ordering or mutable global state. Decision reasons are sorted before canonical serialization. Digests use SHA-256 over canonical JSON.

### Authority boundary

The engine is not an authority source. It consumes an already-normalized action profile and an explicit policy. A future NEXY integration would need the canonical NEXY authority layer to construct those inputs.

### Failure semantics

- Invalid profile/policy values fail closed via `ValueError`.
- Unknown policy keys are rejected, preventing typo-driven silent behavior.
- High-impact action without explicit user authority -> `FREEZE`.
- Destructive action lacking adequate rollback/reversibility -> `FREEZE`.
- Authentication boundary crossing -> `CONFIRM`.
- Sensitive or material-cost external effects -> `CONFIRM`.
- Material but reversible uncertainty -> `PREVIEW`.
- Low-risk reversible work -> `PROCEED`.

### Input contract

`RequestProfile` uses normalized dimensions from 0 to 1 for ambiguity, reversibility, confidence, scope breadth, data sensitivity and monetary impact. Booleans describe external effects, destructive intent, rollback availability, explicit authority and authentication-boundary crossing.

The dimensions are deliberately generic. The prototype does not pretend that a numeric value is automatically objective. In a real integration, each value would need an authoritative normalization rule and evidence source.

### Decision precedence

1. `FREEZE` hard gates.
2. `CONFIRM` hard gates.
3. `PREVIEW` soft gates.
4. `PROCEED` default for bounded low-risk reversible work.

A lower-precedence mechanism cannot override a higher-precedence decision.

### Output contract

Each result contains:

- decision enum;
- stable reason-code set;
- attention cost;
- hard-gate boolean;
- action ID;
- canonical SHA-256 digest.

The digest proves deterministic serialization of the decision record, not correctness or real-world safety of the proposed action.

### Core metrics

- autonomy rate;
- human interruption count;
- hard-gate count;
- attention cost;
- decision distribution;
- recovery coverage.

### Optimization target

```text
minimize unnecessary interruption
subject to:
  zero hard-gate downgrades in the bounded scenario corpus
  deterministic repeatability
  explicit authority preservation
  rollback/recovery requirements for risky actions
```

---

## FAILURE MODEL

### F1 — Score laundering
A caller invents reassuring numeric scores to force PROCEED.

Mitigation: real integration must bind score provenance to an authoritative normalization process. The standalone prototype makes no claim that input scores are true.

### F2 — Attention-budget bypass
A UX optimizer treats depleted attention as permission to weaken safety/authority gates.

Mitigation: hard CONFIRM/FREEZE decisions are structurally immune to budget downgrades and covered by bounded tests.

### F3 — Hidden compound action
One request contains several actions and hides a risky sub-action behind a benign aggregate profile.

Mitigation: future work should normalize actions into a dependency graph before evaluation.

### F4 — Policy drift
Threshold changes silently alter behavior.

Mitigation: future integration should bind policy version/digest to every decision record and regression corpus.

### F5 — Ambiguity normalization error
A low ambiguity score hides missing requirements.

Mitigation: score construction must inherit NEXY zero-guess/freeze rules.

### F6 — UI semantic collapse
PREVIEW and CONFIRM are rendered identically, causing fatigue.

Mitigation: preserve structural state and reason codes through the UI boundary.

### F7 — Confirmation fatigue
Too many mandatory prompts cause habitual approval.

Mitigation: minimize only soft prompts, batch independent interruptions, and keep mandatory prompts materially specific.

### F8 — False sense of safety
The deterministic engine is mistaken for a complete safety system.

Mitigation: documentation limits claims. This engine is one control layer, not evidence that an action is correct or safe.

---

## RESEARCH BACKLOG

Everything below is **AI-proposed future work**, not implemented product behavior.

- **R1 Authority provenance binding:** replace `explicit_user_authority: bool` with a traceable authority-reference object.
- **R2 Policy version digest:** bind every decision digest to exact policy and normalization schema versions.
- **R3 Multi-action transaction planner:** evaluate dependency graphs so risky actions cannot hide inside benign batches.
- **R4 Confirmation coalescing:** merge compatible confirmations without losing per-action auditability.
- **R5 Counterfactual UX score:** calculate the smallest change in reversibility, ambiguity or scope that would remove a hard gate.
- **R6 Preference overlays:** let user preferences increase interaction strictness without weakening canonical hard gates.
- **R7 Property-based boundary testing:** expand randomized invariants and monotonicity tests.
- **R8 Real UI prototype:** prototype concise four-state interaction semantics for NEXY VIEW/DIALOG.

---

## VERIFICATION RECORD

**Target:** standalone prototype in this mission directory only.  
**Not evidence for:** NEXY.AI implementation/runtime/release status.

### Environment

- Python observed during local verification: `3.13.5`.
- Local staging path: `/mnt/data/nexy-human-agency-lab-durable`.
- Third-party runtime dependencies: none used.

### V-001 — Static compilation

Commands executed after consolidated-path repair:

```bash
python -m py_compile human_agency_lab.py test_human_agency_lab.py
```

Observed result: exit code `0`.

Evidence class: `E1 Static`.

### V-002 — Unit + regression + invariant tests

Command:

```bash
python -m unittest -v test_human_agency_lab.py
```

Observed result:

- tests executed: `34`
- failures: `0`
- errors: `0`
- final status: `OK`

The suite includes bounded invariants for:

- high-impact actions without explicit authority freeze across an enumerated score grid;
- destructive actions without rollback freeze across an enumerated grid;
- attention budgeting never weakens hard gates across capacities `0,1,2,3,100`;
- external ambiguity yields non-decreasing restrictiveness across tested threshold points;
- `500` repeated evaluations of one normalized deterministic input yield one decision digest.

Evidence class: `E2 Unit / bounded property-regression evidence`.

### V-003 — Reference scenario corpus

Command:

```bash
python human_agency_lab.py simulate fixtures/scenarios.json
```

Observed result:

- scenarios: `11`
- passed: `11`
- failed: `0`
- process exit code: `0`
- distribution: PROCEED `1`, PREVIEW `3`, CONFIRM `4`, FREEZE `3`
- hard gates: `7`
- human interruptions: `10`
- attention cost: `18`
- autonomy rate on the intentionally risk-heavy corpus: `1/11` = `0.09090909090909091`

Evidence class: `E2 executable scenario regression evidence`.

### Regression repaired during packaging

The first consolidated test run failed two scenario tests because the consolidated test file still used the modular package path assumption `parents[1]`. The engine itself was not the failing surface. The harness was corrected to resolve fixtures from the consolidated file's own parent directory. The full compile, 34-test suite and 11-scenario CLI were then re-run and passed.

This failure is intentionally retained in the durable record rather than airbrushed away. Apparently even deterministic systems still need someone to notice when a path climbed one directory too far. Humans did invent filesystems, after all.

### What the verification proves

For the exact locally verified consolidated artifact before publication:

- the two Python files compile;
- all 34 committed tests pass;
- all 11 committed reference scenarios match expected structural decisions;
- tested attention-budget paths do not weaken tested hard gates;
- the selected deterministic request repeats to one digest over 500 iterations.

### What it does not prove

- correctness of a future NEXY.AI integration;
- correctness of real-world score normalization;
- production security;
- completeness against DOC-B/C/D/E;
- runtime/E2E/deployment behavior;
- universal absence of bugs outside the enumerated tests.

---

## EVIDENCE LEDGER

| ID | Claim | Method | Evidence class | Result | Limitation |
|---|---|---|---|---|---|
| E-001 | consolidated Python artifact compiles | `py_compile` | E1 | PASS | Python 3.13.5 local environment |
| E-002 | committed consolidated test suite passes | `unittest` | E2 | PASS, 34/34 | bounded committed tests |
| E-003 | reference scenarios match expected decisions | CLI simulator | E2 | PASS, 11/11 | synthetic corpus |
| E-004 | tested hard gates survive attention-budget pressure | invariant test | E2 | PASS | bounded requests/capacities |
| E-005 | selected deterministic input digest repeats | 500-iteration test | E2 | PASS | one normalized input/policy pair |
| E-006 | NEXY context contains human-authority, zero-guess/freeze and small-surface principles | read `projects/NEXY.AI/overview.md` | SOURCE_FACT | verified as source content | context/design, not implementation proof |
| E-007 | targeted supplemental searches returned no matches for chosen human-agency/friction query set | GitHub code search | REPO_SEARCH_OBSERVATION | no matches returned | not exhaustive absence proof |
| E-008 | target mission directory did not exist before creation | GitHub contents fetch | REPO_FACT | 404 before writes | point-in-time observation |

Truth boundary: the project is described as novel relative to the inspected/searchable supplemental surface, not universally unique across every possible file or external project.

---

## DECISION LOG

### D-001 — Human Agency / Interaction Friction domain
Selected because the inspected supplemental surface is already dense in evidence, epistemic control, counterfactual verification, resilience and long-horizon reliability, while targeted human-agency/friction searches returned no matches.

### D-002 — Standard-library Python
Chosen for portability, deterministic execution and reduced dependency/supply-chain noise.

### D-003 — Four-state interaction contract
`PROCEED -> PREVIEW -> CONFIRM -> FREEZE` creates a structural middle layer between unrestricted autonomy and total stop.

### D-004 — Hard gates are immune to attention optimization
User attention is scarce. Scarcity is not lawful authority bypass.

### D-005 — Explicit non-canonical classification
Nothing here is promoted into NEXY DOC-B/C/D/E or presented as current NEXY implementation behavior.

### D-006 — NEXY.AI remains read-only
All mutation is confined to this new AI-CONTEXT supplemental mission directory.

---

## CHECKPOINT 001 — LOCALLY VERIFIED

Mission: `NEXY-HAL-20261005-0121`  
Chat/work code: `CHAT-20261005-0121-NEXY-HUMAN-AGENCY-LAB`

Completed before durable write:

- authority/context read;
- supplemental inventory inspected;
- targeted novelty searches executed;
- architecture/spec produced;
- deterministic prototype implemented;
- 34-test suite implemented and passing;
- 11-scenario corpus passing;
- packaging regression found, repaired and re-verified.

Protected scope status: no NEXY.AI implementation repository mutation was performed by this mission.

Next durable step at this checkpoint: persist files, read them back and issue a post-publication final state.

---

## RESUME CAPSULE

Mission: `NEXY-HAL-20261005-0121`  
Target: `AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-HUMAN-AGENCY-LAB/`

On resume:

1. Read AI-CONTEXT root `INDEX.md` and `AI-EXECUTION-KERNEL.md`.
2. Read this `PROJECT.md`, `FINAL_STATE.md` if present, and current mission files.
3. Verify target repository/ref freshness before mutation.
4. Never mutate any repository whose name contains `NEXY.AI`.
5. Keep all future-system material explicitly AI-proposed unless authoritative NEXY specification promotes it.
6. Re-run tests if implementation/test/scenario files change.
7. Do not claim universal uniqueness from search absence.
8. Continue from the latest durable checkpoint rather than reconstructing from model memory.
