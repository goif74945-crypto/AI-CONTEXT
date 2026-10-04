# Portfolio Architecture — Five Auxiliary Systems

Classification: **AI_PROPOSAL / EXPERIMENTAL / NOT_NEXY_CANON**.

## System purpose
This portfolio targets a meta-integrity loop around autonomous work:

`OBSERVE → CHALLENGE EVIDENCE → MINIMIZE FAILURE → CALIBRATE CONFIDENCE → CHECKPOINT/RESUME`

It is deliberately auxiliary. No module is allowed to become final authority merely by existing.

## Modules
1. **Contract Archaeologist** receives finite trace events and reports exact observed regularities. Every pattern is branded `OBSERVED_PATTERN_NOT_REQUIREMENT`. It never infers causality or promotes behavior to law.
2. **Evidence Genealogy Engine** receives evidence metadata for one claim and finds correlation components caused by shared source roots, identical content, and optionally method family. It prevents duplicated derivations from masquerading as independent corroboration.
3. **Failure Atomizer** receives a concrete failing sequence and a deterministic predicate, then delta-reduces it and performs a single-removal post-proof so `MINIMIZED_1_MINIMAL` means exactly that. It never claims global cardinality minimum.
4. **Calibration Observatory** compares declared probabilities against verified outcomes using Brier score, fixed-bin ECE, and signed bias. Its output is advisory and explicitly is not evidence that a decision is correct.
5. **PauseSafe Kernel** models running steps, idempotence, checkpoints, and compensation before interruption; creates a content-derived resume token only from a safe checkpoint and detects state drift on resume.

## Shared invariants
- Canonical JSON + SHA-256 fingerprints are content-derived.
- Equivalent unordered input semantics produce deterministic reports.
- Malformed IDs, duplicate identity keys, invalid probabilities, or non-finite trace numbers fail explicitly.
- No module performs network I/O, model calls, shell execution, database writes, environment reads, or secret access.
- No proposal output can override NEXY LAW/CORE/JUDGE or a canonical project source.

## Future NEXY integration boundary
A possible future adapter may map NEXY-owned records into these narrow input types. Integration must remain one-way advisory unless NEXY authority explicitly adopts a gate. Suggested order:

`NEXY-owned source → schema adapter → auxiliary module → signed/advisory report → NEXY-owned adjudication`

The adapter must reject unknown schema versions. These libraries must not read NEXY internals directly, and they must not mutate NEXY state.

## Adoption gates
Before production adoption, each concept requires: schema/version contract, exact NEXY integration tests, performance limits on representative data, security review, replay fixtures, and an authority decision describing whether the report is informational or release-blocking. Current work does **not** satisfy those production gates.

## Failure semantics
- Observation without data → explicit no-data result.
- Insufficient independent evidence → explicit insufficiency, not fake corroboration.
- Non-failing baseline → atomizer refuses to invent a cause.
- Too little calibration data → `NOT_ENOUGH_DATA`.
- Unsafe in-flight step → interruption is blocked or draining is required.
- Resume-state drift → `STATE_DRIFT`, never silent continuation.
