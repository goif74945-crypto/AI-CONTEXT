# Vote Format and Rights

## Lifetime right model
For each `CHAT_ID`:
- `KEEP`: at most one finalized vote.
- `CUT`: at most one finalized vote.
- `DEFER`, `INSUFFICIENT_EVIDENCE`, `WIP`: do not consume either right.
- Evidence revisions do not create a new right and cannot change old round/verdict.

## Required record surface
The external VoteRequest preserves:
`VOTE_ID`, `CHAT_ID`, `ROUND`, `TIMESTAMP`, `SPEC_ID`, `SPEC_HASH`, `NEXY_REPO`, `NEXY_BRANCH`, `NEXY_COMMIT_SHA`, `AI_CONTEXT_COMMIT_SHA`, `CANDIDATE_ID`, `CANDIDATE_PATH`, `STATUS_BEFORE`, `VERDICT`, `SPEC_EVIDENCE`, `CODE_EVIDENCE`, `AI_CONTEXT_EVIDENCE`, all nine scoring axes, `CONFLICTS`, `DUPLICATES`, `DEPENDENCIES`, `FACT`, `ASSUMPTION`, `UNKNOWN`, `REASON`, `COUNTERARGUMENT`, and `FINAL_JUSTIFICATION`.

## CUT burden
A CUT cannot be justified merely because a candidate has few files, is WIP, or has UNKNOWN fields. Duplicate-based CUT must identify exact other candidate path/symbol/commit, bind factual evidence, and demonstrate semantic overlap across at least two dimensions. Canon-conflict CUT must cite exact Canon location, commit, and evidence.

## Physical deletion
`PHYSICAL_DELETION_ALLOWED` is hard-coded `false`. CUT is classification only: archive, rejected, or superseded.

## Authority
Vote score has no ability to override Canon or LAW. KEEP cannot self-promote. CUT cannot delete. Human/AI auxiliary layers cannot change NEXY Core state through EPC.

## Current chat rights
`CHAT-20261005-0309-NEXY-EPC-Q64-COURT`: KEEP = UNUSED, CUT = UNUSED. Building EPC itself does not cast a vote.
