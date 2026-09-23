# FSM Registry Validation

## Result
**PASS — structural FSM registry**

- FSM/state models: **10**
- source/protocol FSMs: **9**
- implementation-only state models: **1**
- DOC-C execution transitions recorded: **23**
- risk/kernel transitions/actions recorded: **17**

Important separations:
- DOC-C 8-state execution FSM ≠ kernel 5-state risk FSM.
- Queue Job FSM ≠ PipelineRun implementation state model.
- Cross-Shard transfer is represented as a protocol-as-FSM and is not merged into app/execution state.

Observed review points:
- DOC-C event `cancel` exists and has OWNER ownership, but observed VNEXT_TRANSITIONS has no cancel row.
- Capability source FSM includes QUORUM_SIGNED/ACTIVE, while observed CapabilityNodeStatus is PROPOSED/REVIEWED/ANCHORED/DEPRECATED.
- PipelineRun setter persists caller-supplied RunState and does not itself enforce a previous→next topology.
