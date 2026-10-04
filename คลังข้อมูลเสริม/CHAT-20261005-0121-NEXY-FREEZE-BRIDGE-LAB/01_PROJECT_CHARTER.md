# Project Charter / Task Contract

Classification: **AI-PROPOSED CONCEPT / ADVISORY REFERENCE IMPLEMENTATION**

## OBJECTIVE

Design, implement and verify an isolated deterministic engine that translates already-decided NEXY freeze/block states into concise human recovery guidance without changing machine truth, authority, evidence status, permissions or legal state transitions.

## TARGET

Only:
`คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-FREEZE-BRIDGE-LAB/`

## AUTHORIZED SCOPE

- new files under the target namespace;
- research/design documents;
- machine-readable schemas;
- standalone Python reference implementation;
- tests, fixtures, self-check and benchmark tools;
- write-back verification.

## PROTECTED SCOPE

- any repository whose name contains `NEXY.AI`;
- existing sibling work under `คลังข้อมูลเสริม`;
- canonical project requirement files;
- live release/deployment state;
- secrets/credentials.

## AUTHORITY SOURCES USED

1. Current user directive.
2. AI-CONTEXT AI Execution Kernel + Security + Verification rules.
3. NEXY project overview/current status.
4. NEXY human-control-surface and constitutional-lock context.
5. Current normalized source matrix.
6. This lab's proposed design, only within this isolated namespace.

## INPUTS

A machine-produced Freeze Event containing:
- stable event identifier;
- status;
- reason code;
- blocking layer;
- recovery owner;
- disclosure class;
- locale;
- retryable flag;
- missing-input identifiers;
- evidence references;
- explicitly authorized recovery actions;
- optional context label that is not reflected to the user.

## REQUIRED OUTPUT

A deterministic Recovery Card containing:
- status;
- reason category;
- human title + summary;
- blocking layer;
- recovery owner;
- safe needed-input list;
- filtered/ordered actions;
- disclosure-safe evidence references;
- effective retryability;
- deterministic SHA-256 fingerprint.

## IMMUTABLE REQUIREMENTS

1. Core decision is input, never recomputed here.
2. No new action may be emitted unless both:
   - upstream explicitly authorizes it; and
   - the reason policy permits it.
3. Unknown reasons must not trigger inferred causes.
4. Security/integrity freeze must never be made retryable by the bridge.
5. Restricted evidence must follow disclosure rules.
6. User-facing wording must not modify legal/system state.
7. Output for semantically equivalent normalized input must be deterministic.
8. No secret value is required by the protocol.
9. No network call is required.
10. No NEXY.AI repository mutation.

## FORBIDDEN BEHAVIOR

- auto-unfreeze;
- force/bypass action generation;
- inventing missing values;
- reclassifying UNKNOWN into a specific failure;
- promoting stale evidence;
- exposing restricted incident references where forbidden;
- using free text as hidden authority;
- allowing localization to alter policy;
- runtime dependency on a model/LLM;
- silent fallback to permissive behavior on invalid protocol versions.

## EDGE CASES

- unknown future reason code → `UNKNOWN_REASON`;
- duplicate actions/inputs → normalized/deduplicated;
- input order differences → same output;
- unsupported protocol version → reject;
- invalid enum/action → reject except unknown reason, which intentionally maps to UNKNOWN_REASON;
- restricted security event → evidence refs suppressed;
- retry requested but action not authorized → non-retryable;
- context label containing markup → not reflected in output.

## ACCEPTANCE CRITERIA

- full unit/negative suite passes;
- compiler/model/policy production code reaches 100% line + branch coverage in the local test run;
- policy self-check passes all generated matrix cases;
- CLI round-trip emits valid JSON;
- malformed top-level input returns non-zero;
- example Thai output renders correctly;
- write-back is verified by re-fetch;
- final audit records limitations and makes no NEXY implementation claim.

## REQUIRED EVIDENCE

- E0 repository presence/read-back;
- E1 compile/static syntax + coverage instrumentation;
- E2 executed unit/negative tests;
- local microbenchmark for reference only;
- no E3/E4/E5/E6/E7 claims because integration/runtime/deployment/physical testing is out of scope.

## RISKS

- **Authority confusion:** presentation layer could be mistaken for Core.
  - Mitigation: explicit advisory label and action intersection.
- **Information leakage:** freeze details may expose incident data.
  - Mitigation: disclosure class + restricted filtering.
- **False recovery:** retry may be suggested when unsafe.
  - Mitigation: reason policy can force non-retryable.
- **Future taxonomy mismatch:** real NEXY may use different reason codes.
  - Mitigation: protocol versioning + UNKNOWN_REASON fail-safe.
- **Localization drift:** translated wording might imply different authority.
  - Mitigation: action codes and policy remain language-independent.

## STOP CONDITIONS

Freeze this lab if:
- the next step requires editing NEXY.AI;
- target namespace identity becomes ambiguous;
- an existing file must be destructively overwritten without explicit need;
- evidence cannot verify write-back;
- a canonical authority conflict would need guessing.
