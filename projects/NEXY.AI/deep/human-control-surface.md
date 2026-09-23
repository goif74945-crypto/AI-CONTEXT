# NEXY.AI — Human / UX / Control Surface Deep Context

## Status
SOURCE-DESIGN. This file consolidates the human-facing architecture, naming/mental model and authority boundaries from repeated source sections. Where older UX concepts conflict with later immutable/canonical law, the later canonical authority must win.

## 1. Identity lock
Repeated late-source identity:
- NEXY = deterministic AI Control Hub / control infrastructure.
- Not a chatbot.
- Not AGI.
- Not a friend system as authority.
- Architect-first.
- Proof > Speed > Emotion.
- Public positioning: **One output. One truth. Or freeze.**
- Core hidden; useful output visible.

The product is conceptually framed as a place/control environment rather than a single chat model.

## 2. Human vs Core authority
### CORE
Core may:
- decide;
- validate;
- verify;
- enforce USER LAW;
- freeze/lock/kill;
- commit authoritative state through the governed path.

Core must not be driven by human emotion, presentation pressure or friendliness.

### Human Gravity Layer
Later strict source limits the Human layer to:
- suggest;
- warn;
- guide attention.

It may not:
- mutate Core state;
- override decisions;
- bypass verification;
- reduce correctness thresholds;
- escalate privilege;
- rewrite truth.

Canonical idea: **Human Gravity exists to attract/help humans, not to decide reality.**

## 3. Imperfection firewall
Permitted only in presentation:
- wording;
- tone;
- pacing;
- light style variation;
- silence.

Forbidden in:
- decision logic;
- validation;
- verification;
- law parsing;
- security;
- safety.

If presentation-layer imperfection crosses into truth/authority, later canon treats it as a freeze-class violation.

## 4. Friend / humanized interaction
Earlier Human Gravity design includes:
- Adaptive Persona Engine;
- Conversation Continuity Illusion;
- Preference Shadow;
- Behavior Trace;
- Smart Silence;
- Mood-aware response;
- opt-in nickname;
- guarded polite teasing;
- “Explain Like I’m Smart”;
- typo/human-error tolerance.

Important later constraint: these are **UX behaviors only**. They cannot become authority, durable ungoverned memory or intent-rewriting logic.

### Friend Mode hard limits
Allowed:
- opt-in name usage;
- light polite teasing;
- concise direct tone;
- style adaptation.

Forbidden:
- emotional dependency loops;
- therapist identity;
- moral authority over the user;
- attachment-seeking behavior;
- using emotion to alter system truth.

Escalation model in source:
stress/attachment/risk signals → neutral/deflect/hard-stop presentation behavior, while Core remains unchanged.

## 5. Output law
Late canon repeatedly states:
- one task → one final output;
- no uncontrolled list of competing answers;
- no “choose yourself” when the system is expected to adjudicate;
- unknown/insufficient proof → silence or freeze;
- silence is preferable to a wrong authoritative output.

This should be read together with later DOC-C release thresholds. Older “confidence must be 100%” prose is aspirational/strict-canon language; DOC-C later defines configurable numeric release thresholds. Do not merge them silently.

## 6. Core human mental model
The source develops a user mental model where:
- **NEXY** = the place/control environment;
- **CORE** = hidden engine/authority;
- **FRIEND** = sandboxed conversational human-facing entity beneath Core;
- **TASK** = real unit of work; no meaningless chat state should become canonical work;
- **VAULT** = persistent truth/artifact store;
- **STATE** = exact resumable position, not emotion/noise memory;
- **COMMAND / COMMAND BAR** = explicit human control;
- **FREEZE_EVENT** = failure is exposed rather than masked;
- **OPERATOR** = human controller, not passive “user”;
- **AGENT** = replaceable AI worker/tool;
- **USER LAW** = top user-defined law within its allowed authority scope.

Design intent: “control AI” rather than “chat with AI.”

## 7. Canonical naming vocabulary
Repeated locked vocabulary includes:
- NEXY
- CORE
- USER LAW
- CANON
- FREEZE
- KILL
- AGENT
- SWARM
- DEBATE
- VERIFY
- CONSENSUS
- REJECT
- PHASE
- LOCK
- OVERRIDE
- FAILSAFE
- TASK
- SUBTASK
- TASK GRAPH
- FINAL OUTPUT
- REASON SUMMARY
- VAULT
- ARTIFACT
- REVISION
- COMMIT
- CRYPTO ERASE
- TASK MEMORY
- SESSION MEMORY
- OTAC
- TTL
- RATE LIMIT
- HARD BAN

Source repeatedly warns that internal vocabulary is part of system architecture, not decoration, because changing terms changes the operator mental model.

## 8. Modes / control surfaces
Two naming sets appear across source evolution.

### Earlier conceptual user modes
- Explore
- Execute
- Build

### Canonical NEXY surfaces
- **NEXY::VIEW** — read/observe capability/results; safe for newcomers, observers and evaluation.
- **NEXY::RUN** — real execution/task submission under Core.
- **NEXY::FORGE** — construct pipelines/rules/automation/system artifacts; advanced/architect-facing.

These are user/control modes, not authority layers.

## 9. NEXY::CORE / LAW / JUDGE / SWARM
Human-facing architecture distinguishes:
- **NEXY::CORE** — central deterministic control/validation/freeze/authority router.
- **NEXY::LAW** — rule authority including User Law/system law.
- **NEXY::JUDGE** — deterministic adjudication after evidence/consensus.
- **NEXY::SWARM** — labor/analysis/debate pool; no final authority.

Canonical mental split:
**SWARM = labor/power. CORE/JUDGE = authority.**

## 10. Experience & Control Surface architecture
The source explicitly separates UI, UX and GUI/control.

### UX
Internal concepts:
- FLOWMAP
- DECISION_PATH
- USER_INTENT_TRACK

Goal: user knows current position, permitted actions and consequences without guessing.

### UI
Internal concepts:
- SURFACE
- VIEW_PORT
- STATE_PANEL

Rules:
- UI reflects real state.
- 1 action → 1 defined result.
- no fake control;
- no decoration that lies about state;
- frozen system must look frozen.

### GUI / graphical control
Internal concepts:
- CONTROL_NODE
- TOGGLE_AUTH
- EXEC_PANEL

Used for actual control such as RUN/FREEZE/LOCK/mode/phase changes. This is architect/operator control, not merely visual display.

## 11. System feedback
Named concepts:
- SYSTEM_PULSE
- HEALTH_INDICATOR
- ERROR_SIGNAL

Purpose: expose whether the system is processing, waiting, frozen or failed, and identify the blocking layer rather than emit vague errors.

Later product naming also includes:
- **NEXY::FRONT** — first-contact/input surface;
- **NEXY::PULSE** — status/feedback;
- **NEXY::DIALOG** — conversational sandbox;
- **NEXY::GUARD** — human safety/boundary;
- **NEXY::COMPANION** — human-facing companion concept under strict authority limits.

## 12. Auth / permission UX
Named UI concepts:
- AUTH_LAYER
- ROLE_VIEW
- VISIBILITY_MASK

Invariant:
**visible ≠ editable ≠ executable**.
Frontend visibility may reduce confusion, but backend authorization remains authoritative.

## 13. Fail-safe experience
Named concepts:
- SAFE_GUARD
- ROLLBACK_VIEW
- CONFIRM_LOCK

Purpose: human error should not directly corrupt Core state. Dangerous actions require explicit confirmation/authority path; user mistakes should fail safely.

## 14. Meta/architect UX
Named concepts:
- ARCHITECT_VIEW
- DEBUG_SURFACE
- TRACE_MODE

Purpose:
- inspect what component made a decision;
- trace prior reasoning/state;
- audit without necessarily rerunning;
- expose proof/conflict/state for an architect while keeping normal UX simpler.

## 15. Task / artifact mental model
The source shifts away from “prompt/answer” terminology:
- user input can be called a **Directive**;
- work is a **Task**;
- output should become an **Artifact** when it is a usable persistent product;
- reason/proof is a structured summary/evidence surface rather than a stream of hidden internals.

This matters for product positioning: NEXY is designed as a control/execution fabric, not a chat transcript manager.

## 16. Output classification
One design section names:
- RAW — unformatted/unvalidated candidate;
- CLEAN — validated/usable but not final authority;
- FINAL — passed JUDGE/release;
- REJECT — failed with explicit reason.

Later DOC-C contracts should be considered authoritative for current build-state enums when there is a naming mismatch.

## 17. Command language
Human-visible command concepts repeatedly include:
- RUN
- FREEZE
- LOCK
- EXPORT
- KILL

Source intentionally avoids “retry until something works” as the default mental model. Failure should be explained as state/evidence/law, not hidden by repeated guesses.

## 18. Human Gravity growth features
The design includes product-growth properties that are architectural rather than advertising-only:
- private by default;
- no feed/distraction;
- share output/artifact rather than exposing internal prompt;
- zero-setup onboarding;
- model hot-swap behind stable interface;
- degradation detection;
- legal/policy firewall;
- hidden enterprise gate;
- regional kill/risk controls.

These are source design directions, not proof of implementation.

## 19. Important canon conflicts / evolution
The full document contains evolving design passes. Preserve rather than erase these differences:
1. Early material allows “intent inference/goal stripping”; a later absolute canon says AI may not infer missing intent or guess missing data. Later strict canon wins when authority is required.
2. Early Human Gravity includes mood/persona/friend behaviors; later law confines all of this to presentation sandbox.
3. Early text sometimes says confidence must be 100%; later DOC-C uses explicit configurable release thresholds and bounded truth. Treat strict 100% prose as an aspiration/legacy canon statement unless current build spec explicitly requires it.
4. Some older naming says OWNER can OVERRIDE “everything”; later constitutional/human-determinism law forbids arbitrary force and limits override to predefined Canon procedures. Later law wins.
5. “AI runtime memory = none” appears in ultra-compressed canon while later L1o/Lo2 designs introduce governed working/verified/experimental memories. Distinguish model/runtime conversational memory from explicit governed system memory.

## 20. Product-law summary
Human-facing NEXY should feel simple while the backend remains strict:
- small surface;
- large backbone;
- user sees state, authority and usable artifacts;
- internal AI/model complexity remains replaceable;
- presentation may be warm/human;
- truth, law and execution never become “humanized” or probabilistic merely for UX.
