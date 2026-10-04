# Future Ideas

Everything in this file is AI-PROPOSED CONCEPT ONLY. Nothing here is claimed implemented.

## F-01 Signed adapter receipts

Bind every executor receipt to an adapter identity and signature so evidenceHash cannot be fabricated by an untrusted caller.

## F-02 Residual scanner

After an erasure plan is executed, independently scan canonical storage, cache/index projections and export registries for residual references. Treat any residual as NOT VERIFIED or FAIL rather than silent success.

## F-03 Replica and backup horizon

Represent replicas, snapshots and backups as graph nodes with retention windows. Completion would distinguish immediate online erasure from bounded backup expiry rather than falsely claiming instant universal deletion.

## F-04 Privacy-preserving tombstones

Use non-reversible subject handles and minimal metadata so audit evidence proves that an erasure workflow occurred without recreating erased content.

## F-05 Erasure closure certificate

Build a Merkle-like root over the reachable erasure closure plus action receipts. This could provide compact third-party verification that the planned closure and observed evidence match.

## F-06 Restore-versus-erasure conflict guard

Prevent restore workflows from resurrecting content whose erasure intent is newer than the restore snapshot. Resolve by causal order rather than wall-clock guessing.

## F-07 Model-derived data policy

Define separate policy for data that influenced models or aggregate artifacts where direct record deletion cannot literally reverse training. The system must describe the real mitigation boundary instead of promising impossible retroactive unlearning.
