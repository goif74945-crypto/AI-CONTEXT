# OXC Adjacent Systems Portfolio

Status: **AI-PROPOSED ONLY / NOT CANON / NOT IMPLEMENTED**
Date: 2026-10-05
Parent experiment: NEXY Operator Experience Compiler (OXC)

These are future system concepts intentionally separated from the implemented OXC reference. Their presence is not authorization to build them into NEXY.

## Proposal A — Accessibility Truth Channel (ATC)

### Problem
A UI can technically show a FREEZE banner yet still fail users who cannot perceive the chosen visual channel.

### Idea
Compile every critical state into a modality-independent semantic signal set:
- textual status;
- ARIA/live-region class;
- focus priority;
- keyboard navigation priority;
- non-color severity token;
- optional haptic/audio semantic key on supported clients.

### Immutable boundary
ATC may duplicate truth across modalities but may not reinterpret truth or permission.

### Value
Makes “truthful UI” testable beyond pixels.

### Required proof before promotion
Accessibility automated checks + screen-reader/manual E4 paths + critical-state non-omission tests.

---

## Proposal B — Friction Policy Auditor (FPA)

### Problem
Risk metadata can drift so that a destructive action is accidentally classified as low-friction.

### Idea
A static/CI auditor checks an authoritative action registry against minimum-risk laws:
```text
action class → minimum risk → minimum reversibility class → minimum friction
```

It rejects impossible combinations such as a known irreversible destructive operation mapped to `NONE`.

### Boundary
FPA audits policy metadata. It does not grant or execute actions.

### Value
Moves dangerous UX safety from scattered component code into inspectable policy checks.

### Required proof
Known-safe/known-unsafe fixtures, mutation testing and integration against the eventual authoritative action registry.

---

## Proposal C — Preference Non-Interference Prover (PNIP)

### Problem
As adaptive UX grows, accidental dependency from a preference field into permission logic becomes increasingly likely.

### Idea
Generate/property-test pairs of inputs that differ only in presentation preferences and prove an authority projection remains identical.

Projection example:
```text
action id + enabled/disabled/hidden + denial reasons + required friction
```

### Boundary
This is an evaluation system, not runtime authority.

### Value
Turns a subtle architectural promise into a regression gate.

### Required proof
Property-based coverage, dependency-taint/static analysis and mutation tests that demonstrate the gate catches an intentional violation.

---

## Proposal D — Cognitive Load Budgeter (CLB)

### Problem
“Minimal but information-dense” becomes subjective once features accumulate.

### Idea
Assign a measurable presentation budget per state:
- number of primary actions;
- number of simultaneous high-severity signals;
- nested disclosure depth;
- control density;
- required decision count before task completion.

Critical truth signals are exempt from hiding, so the budget reduces optional clutter first.

### Boundary
CLB may recommend/hide optional explanatory material, never mandatory truth or authority controls.

### Value
Creates a quantitative guard against dashboard sprawl without weakening safety.

### Required proof
Human usability study and correlation between budget metrics, completion time and operator mistakes.

---

## Proposal E — Stale Surface Replay Harness (SSRH)

### Problem
A surface plan can be correct when rendered and unsafe milliseconds later after FREEZE, permission revocation or version change.

### Idea
A deterministic integration/e2e harness replays:
1. render authoritative state A;
2. mutate backend to state B;
3. attempt action from old plan A;
4. require backend rejection and current-state refresh.

Scenario families:
- READY → FREEZE;
- OWNER → revoked;
- allowed → denied;
- artifact version N → N+1;
- active session → revoked.

### Boundary
SSRH is a test harness only.

### Value
Targets the render-to-click race that pure UI unit tests cannot prove safe.

### Required proof
E3/E4 against a real backend; standalone mocks are insufficient for production claims.

---

## Suggested build order if later authorized

1. PNIP, because it strengthens an invariant already demonstrated by OXC.
2. FPA, once an authoritative action/risk registry exists.
3. SSRH, when integration APIs are stable enough for race testing.
4. ATC alongside real UI work.
5. CLB only after enough real user-flow data exists.

## Stop rule

Do not implement any proposal inside a repository containing `NEXY.AI` without a new explicit user authorization and refreshed project authority/current-state inspection.
