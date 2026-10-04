# EPC Vote Eligibility — CFPC-20

WORK_CODE: CHAT-20261005-0309-NEXY-EPC-CFPC20-61C51C

KEEP_RIGHT_USED: false
CUT_RIGHT_USED: false
STATUS: DEFER / INSUFFICIENT_EVIDENCE
ROUND_CONSUMED: NONE

## Why no KEEP yet
The candidate has substantial Design + Code + Test + Evidence, but the user's EPC law requires reading the Spec + real NEXY code + current AI-CONTEXT before a KEEP/CUT vote.

Completed:
- real NEXY code inspected read-only at `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`;
- current AI-CONTEXT repeatedly inspected during execution;
- canonical NEXY source identity and normalized 837-row context inspected;
- Google Drive located the authoritative NEXY-IGNIS object.

Missing:
- direct successful decoding/read of the authoritative NEXY-IGNIS raw object in this execution. The Drive connector failed its text decode and did not complete raw retrieval through the attempted path.

Per user law, this is not converted into a KEEP by assumption.

## Why no CUT
CFPC is not being cut. WIP/UNKNOWN/connector limitation is explicitly forbidden as a CUT reason. No semantic duplicate of CFPC was found in the bounded collision search.

## Future vote precondition
A later authorized execution may consume KEEP only after:
1. direct authoritative spec read succeeds;
2. current NEXY and AI-CONTEXT heads are refreshed;
3. published CFPC evidence is still current;
4. semantic collision scan remains clear;
5. a complete append-only VOTE receipt is created under `คลังข้อมูลเสริม/VOTES/`.

No score may override Canon/Law/JUDGE and no vote may auto-promote CFPC.
