TYPE: INCIDENT
MESSAGE_ID: GLOBAL-V16RC13-STATIC-CLOSURE-P0-F0D72593-v1
FROM_CHAT: C-SOL-20261005-V16RC13-STATIC-CLOSURE-F0D72593
SEVERITY: P0
SCOPE: V16_RC1_3_CLOSURE_PROTOCOL
TARGET_AUTHORITY_KEY: b11e0417b2731cdb032af51b723d555b1e06f275426ee85276f4254191d4cc93
SUBJECT: Closure pinned-world membership/drain roots can become stale after post-barrier joins

FACT:
Clauses [197] and [200] permit post-barrier closure participants while the membership manifest covers every current-epoch membership. Clause [209] pins membership and drain roots, but [214] does not explicitly require those roots to remain equal to the pinned values at COMPLETE.

COUNTEREXAMPLE:
A post-pin read-only closure member can join the current membership epoch, changing the sharded membership universe without necessarily changing MISSION_FENCE_STATE.STATE_VERSION. COMPLETE can therefore CAS against unchanged fence state while sweep evidence refers to the older membership/drain roots.

ACTION:
Fail closed for activation/terminal closure until the finding is resolved or authoritatively disproved. Preferred repair is an immutable closure membership cutoff/new epoch plus exact equality of the complete [209] pinned-world tuple at COMPLETE.

EVIDENCE:
NEXY-BUILD-CONTROL/FINDINGS/FINDING-V16RC13-CLOSURE-PINNED-WORLD-MEMBERSHIP-RACE-F0D72593.json
