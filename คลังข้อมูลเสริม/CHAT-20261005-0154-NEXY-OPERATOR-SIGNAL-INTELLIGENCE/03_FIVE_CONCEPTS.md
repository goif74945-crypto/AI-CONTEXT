# Five AI-Proposed Concepts

> These are proposals, not current NEXY law or implementation.

## 1. Salience Gate
Converts an explicit `OperatorSignal` into LOW/NORMAL/HIGH/CRITICAL using deterministic rules. FREEZE and SECURITY are always CRITICAL. Blocking authority conflicts are CRITICAL. User-required/blocking/error events are HIGH. State/evidence transitions are at least NORMAL.

**User value:** reduces equal-weight noise and makes genuinely important events hard to miss.

## 2. Interruption Governor
Routes each signal to `NOW`, `BATCH`, or `SILENT_LOG`. Quiet mode may silence only routine LOW signals. FREEZE/SECURITY/CRITICAL are non-suppressible, and acknowledgement-required signals cannot disappear into silent logs.

**User value:** fewer pointless interruptions without weakening safety or human authority.

## 3. Milestone Compressor
Consumes a deterministic ordered event stream and collapses repetitive routine events while preserving component state/evidence transitions, user-required decisions, acknowledgement-requiring signals, immediate alerts, and completion events. It records collapsed counts instead of pretending the events never existed.

**User value:** long tasks become readable as meaningful milestones rather than a firehose.

## 4. Outcome Delta Compiler
Produces canonical before/after deltas using JSON Pointer paths, stable content hashes, explicit `UNKNOWN` classification, and output redaction. UNKNOWN/NOT_VERIFIED/CONFLICT markers are never silently promoted to ordinary verified changes.

**User value:** the user can see exactly what changed, what remains uncertain, and what is redacted.

## 5. Acknowledgement Debt Ledger
Tracks only signals explicitly marked `requires_ack`, with logical-sequence deadlines by severity. High/critical unresolved debt prevents `all_clear`; acknowledgements referencing unknown/future events fail closed.

**User value:** important warnings cannot vanish merely because the interface moved on.

## Composition
`system events -> Salience Gate -> Interruption Governor -> Milestone Compressor / operator surface`

`before/after state -> Outcome Delta Compiler -> completion summary`

`ack-required routed signals -> Acknowledgement Debt Ledger -> unresolved attention state`
